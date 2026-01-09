"""
Aura Lead Hunter - AI Intent Analyzer
=======================================
LLM integration for analyzing user messages and
identifying potential affiliate partners.
"""

import json
import asyncio
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime

import httpx
from openai import AsyncOpenAI

from config.settings import LLMConfig
from utils.logger import AuraLogger, ThoughtType


@dataclass
class LeadAnalysis:
    """Result of AI intent analysis - Hunter 2.0."""
    is_lead: bool
    reason: str
    confidence: float  # Kept for backward compatibility
    score: int  # NEW: 1-10 score
    category: str  # NEW: lead category
    user_id: int
    username: Optional[str]
    display_name: Optional[str]
    bio: Optional[str]  # NEW: User bio
    message_samples: List[str]
    source_chat: str
    has_keywords: bool = False  # NEW: Keyword match flag
    matched_keywords: List[str] = field(default_factory=list)
    analyzed_at: str = ""
    
    def __post_init__(self):
        if not self.analyzed_at:
            self.analyzed_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# Hunter 2.0 System prompt - Headhunter for crypto affiliate network
SYSTEM_PROMPT = """Ты — хедхантер для крипто-партнёрки. Твоя задача — находить лидов среди пользователей Telegram.

АНАЛИЗИРУЙ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ (Сообщения + Bio) И ОТМЕЧАЙ КАК ЛИД ЕСЛИ ОН:

🎯 HIGH-VALUE LEADS (score 8-10):
- Инфлюенсер с аудиторией (владелец канала, блогер)
- Баер трафика/арбитражник ищущий офферы
- Рекламодатель который закупает размещения
- Овнер комьюнити/админ с активом
- Маркетолог или CMO крипто-проекта

✅ MEDIUM LEADS (score 5-7):
- Активный участник спрашивающий про рекламу/трафик
- Кто-то ищущий партнёров или коллабы
- Обсуждает партнёрки, CPA, офферы
- Упоминает что льёт траф или имеет аудиторию
- Даже если просто СПРАШИВАЕТ про рекламу — это лид!

❌ NOT A LEAD (score 1-4):
- Обычные юзеры без бизнес-интента
- Спамеры без реальной аудитории
- Боты
- Просто болтают

ВАЖНО: Будь ИНКЛЮЗИВЕН! Любой намёк на:
- Покупку/продажу трафа
- Залив рекламы
- Владение каналом
- Поиск офферов
- Опыт в крипто-маркетинге
→ ОТМЕЧАЙ КАК ЛИД!

📝 ПИШИ REASON НА РУССКОМ используя арбитраж-сленг:
- "депы", "капперский траф", "схемы", "льёт", "крео", "оффер", "конверт"

Respond ONLY with valid JSON:
{
    "is_lead": true/false,
    "score": 1-10,
    "category": "influencer" | "traffic_buyer" | "advertiser" | "community_owner" | "marketing_pro" | "potential" | "not_lead",
    "reason": "Краткое пояснение НА РУССКОМ (макс 100 символов)"
}"""


class IntentAnalyzer:
    """
    AI-powered intent analyzer for identifying potential affiliate partners.
    Uses OpenRouter/OpenAI compatible API for analysis.
    """
    
    def __init__(
        self,
        config: LLMConfig,
        logger: Optional[AuraLogger] = None
    ):
        self.config = config
        self.logger = logger
        
        # Initialize async OpenAI client
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=60.0
        )
        
        # Track API usage
        self.total_requests = 0
        self.total_tokens = 0
        
        self._log(ThoughtType.SYSTEM, "IntentAnalyzer initialized", {
            "model": config.model,
            "base_url": config.base_url[:30] + "..."
        })
    
    def _log(self, thought_type: ThoughtType, action: str, details: dict = None) -> None:
        """Log analyzer action."""
        if self.logger:
            self.logger.thought(thought_type, "IntentAnalyzer", action, details)
    
    def _repair_json(self, raw_content: str) -> Optional[Dict[str, Any]]:
        """
        Bulletproof JSON repair function.
        Extracts valid JSON from potentially messy LLM output.
        """
        import re
        
        if not raw_content:
            return None
        
        # Clean up common issues
        content = raw_content.strip()
        
        # Try direct parse first
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        
        # Find first { and last } to extract JSON object
        first_brace = content.find('{')
        last_brace = content.rfind('}')
        
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_str = content[first_brace:last_brace + 1]
            
            # Try to parse extracted JSON
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
            
            # Try fixing common issues
            # Replace single quotes with double quotes
            fixed = json_str.replace("'", '"')
            try:
                return json.loads(fixed)
            except json.JSONDecodeError:
                pass
            
            # Try removing trailing commas
            fixed = re.sub(r',\s*}', '}', fixed)
            fixed = re.sub(r',\s*]', ']', fixed)
            try:
                return json.loads(fixed)
            except json.JSONDecodeError:
                pass
        
        # Try regex extraction for key fields
        is_lead_match = re.search(r'"?is_lead"?\s*:\s*(true|false)', content, re.IGNORECASE)
        reason_match = re.search(r'"?reason"?\s*:\s*"([^"]*)"', content)
        confidence_match = re.search(r'"?confidence"?\s*:\s*([0-9.]+)', content)
        
        if is_lead_match:
            return {
                "is_lead": is_lead_match.group(1).lower() == "true",
                "reason": reason_match.group(1) if reason_match else "Extracted from malformed response",
                "confidence": float(confidence_match.group(1)) if confidence_match else 0.5
            }
        
        return None
    
    def _get_default_analysis(
        self,
        user_id: int,
        username: Optional[str],
        display_name: Optional[str],
        messages: List[str],
        source_chat: str,
        error_reason: str,
        bio: Optional[str] = None,
        has_keywords: bool = False,
        matched_keywords: List[str] = None
    ) -> LeadAnalysis:
        """Return default 'not a lead' analysis when parsing fails."""
        return LeadAnalysis(
            is_lead=False,
            reason=f"Analysis failed: {error_reason}",
            confidence=0.0,
            score=0,
            category="not_lead",
            user_id=user_id,
            username=username,
            display_name=display_name,
            bio=bio,
            message_samples=messages[:5],
            source_chat=source_chat,
            has_keywords=has_keywords,
            matched_keywords=matched_keywords or []
        )
    
    async def analyze_user(
        self,
        user_id: int,
        username: Optional[str],
        display_name: Optional[str],
        messages: List[str],
        source_chat: str,
        bio: Optional[str] = None,
        has_keywords: bool = False,
        matched_keywords: List[str] = None
    ) -> LeadAnalysis:
        """
        Hunter 2.0: Analyze user with messages + bio.
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            display_name: User's display name
            messages: List of recent messages
            source_chat: Name of source chat
            bio: User's Telegram bio (About)
            has_keywords: Whether keywords were found
            matched_keywords: List of matched keywords
        """
        start_time = asyncio.get_event_loop().time()
        
        keywords_str = ", ".join(matched_keywords or [])
        
        self._log(ThoughtType.ANALYZE, f"Analyzing user @{username or user_id}", {
            "message_count": len(messages),
            "has_bio": bio is not None,
            "keywords": keywords_str[:50] if keywords_str else "none",
            "source": source_chat
        })
        
        # Prepare messages for analysis (limit to 15 for Hunter 2.0)
        messages_text = "\n---\n".join(messages[:15])
        
        # Hunter 2.0 prompt with Bio
        user_prompt = f"""Analyze this Telegram user:

👤 USER INFO:
- Username: @{username or 'unknown'}
- Display Name: {display_name or 'N/A'}
- Source Chat: {source_chat}
- Bio: {bio or 'Not available'}
- Matched Keywords: {keywords_str or 'None'}

💬 RECENT MESSAGES ({len(messages)} total):
{messages_text}

Respond with JSON: {{"is_lead": bool, "score": 1-10, "category": str, "reason": str}}"""

        try:
            # Try with response_format first (may not be supported by all models)
            try:
                response = await self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500,
                    response_format={"type": "json_object"}
                )
            except Exception:
                # Fallback without response_format if not supported
                response = await self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
            
            self.total_requests += 1
            if response.usage:
                self.total_tokens += response.usage.total_tokens
            
            # Parse response using bulletproof JSON repair
            raw_content = response.choices[0].message.content
            result = self._repair_json(raw_content)
            
            if result is None:
                self._log(ThoughtType.WARNING, f"JSON repair failed for @{username or user_id}", {
                    "raw_response": raw_content[:200] if raw_content else "empty"
                })
                return self._get_default_analysis(
                    user_id, username, display_name, messages, source_chat,
                    "Could not parse JSON from AI response",
                    bio, has_keywords, matched_keywords
                )
            
            duration_ms = (asyncio.get_event_loop().time() - start_time) * 1000
            
            # Validate and sanitize result values (Hunter 2.0)
            is_lead = bool(result.get("is_lead", False))
            reason = str(result.get("reason", "No reason provided"))[:200]
            category = str(result.get("category", "not_lead"))
            
            # Score handling
            try:
                score = int(result.get("score", 0))
                score = max(1, min(10, score))  # Clamp to 1-10
            except (ValueError, TypeError):
                score = 5 if is_lead else 2
            
            # Confidence from score
            confidence = score / 10.0
            
            analysis = LeadAnalysis(
                is_lead=is_lead,
                reason=reason,
                confidence=confidence,
                score=score,
                category=category,
                user_id=user_id,
                username=username,
                display_name=display_name,
                bio=bio,
                message_samples=messages[:5],
                source_chat=source_chat,
                has_keywords=has_keywords,
                matched_keywords=matched_keywords or []
            )
            
            self._log(ThoughtType.ANALYZE, f"Analysis complete for @{username or user_id}", {
                "is_lead": analysis.is_lead,
                "score": f"{analysis.score}/10",
                "category": analysis.category,
                "duration_ms": round(duration_ms, 2)
            })
            
            # Special logging for leads (score >= 5)
            if analysis.is_lead and analysis.score >= 5 and self.logger:
                self.logger.lead_found(
                    username or str(user_id),
                    analysis.confidence,
                    f"[{category}] {analysis.reason}",
                    source_chat
                )
            
            return analysis
            
        except Exception as e:
            self._log(ThoughtType.ERROR, f"Analysis failed for @{username or user_id}", {
                "error": str(e)[:200]
            })
            
            # Return default analysis on any error - never crash the loop
            return self._get_default_analysis(
                user_id, username, display_name, messages, source_chat,
                str(e)[:200], bio, has_keywords, matched_keywords
            )
    
    async def batch_analyze(
        self,
        users_data: List[Dict[str, Any]],
        source_chat: str = None,  # Can be overridden per-user
        concurrency: int = 1  # Sequential for safety
    ) -> List[LeadAnalysis]:
        """
        Hunter 2.0: Analyze multiple users with bio and keywords.
        
        Args:
            users_data: List of dicts with user_id, username, display_name, messages, bio, etc.
            source_chat: Default source chat (can be overridden per-user)
            concurrency: Max concurrent API requests (default 1 for safety)
        """
        keyword_users = sum(1 for u in users_data if u.get("has_keywords", False))
        
        self._log(ThoughtType.ANALYZE, f"Starting batch analysis", {
            "user_count": len(users_data),
            "with_keywords": keyword_users,
            "concurrency": concurrency
        })
        
        semaphore = asyncio.Semaphore(concurrency)
        
        async def analyze_with_limit(user_data: Dict, index: int) -> LeadAnalysis:
            async with semaphore:
                # Add delay between requests to avoid rate limits
                if index > 0:
                    delay = 4.0  # 4 seconds between requests
                    self._log(ThoughtType.RATE_LIMIT, f"Waiting {delay}s before next AI request")
                    await asyncio.sleep(delay)
                
                return await self.analyze_user(
                    user_id=user_data["user_id"],
                    username=user_data.get("username"),
                    display_name=user_data.get("display_name"),
                    messages=user_data.get("messages", []),
                    source_chat=user_data.get("source_chat", source_chat or "Unknown"),
                    bio=user_data.get("bio"),
                    has_keywords=user_data.get("has_keywords", False),
                    matched_keywords=user_data.get("matched_keywords", [])
                )
        
        # Process sequentially to avoid rate limits
        results = []
        for i, ud in enumerate(users_data):
            result = await analyze_with_limit(ud, i)
            results.append(result)
        
        # Filter out exceptions
        valid_results = []
        for r in results:
            if isinstance(r, LeadAnalysis):
                valid_results.append(r)
            elif isinstance(r, Exception):
                self._log(ThoughtType.ERROR, "Batch analysis error", {"error": str(r)})
        
        leads_found = sum(1 for r in valid_results if r.is_lead)
        self._log(ThoughtType.SUCCESS, "Batch analysis complete", {
            "total_analyzed": len(valid_results),
            "leads_found": leads_found
        })
        
        return valid_results
    
    def get_stats(self) -> Dict[str, int]:
        """Get API usage statistics."""
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens
        }
