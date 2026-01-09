"""
Aura Lead Hunter 2.0 - Scraper Engine
======================================
High-velocity message scraper with:
- Bio fetching for profile intelligence
- Smart keyword pre-filter
- User cache for optimization
"""

import asyncio
import re
from typing import Optional, List, Dict, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict

from telethon.tl.types import Message, User, Channel, Chat, PeerUser
from telethon.errors import FloodWaitError, ChatAdminRequiredError, ChannelPrivateError

from core.telegram_client import TelegramClientWrapper
from core.rate_limiter import RateLimiter
from utils.logger import AuraLogger, ThoughtType


# Keywords that indicate a potential lead - CHECK BEFORE AI
LEAD_KEYWORDS = [
    # Traffic & Arbitrage
    'traff', 'трафик', 'трафф', 'арбитраж', 'arbitrage', 'ads', 'реклама',
    # Business roles
    'менеджер', 'manager', 'владелец', 'owner', 'admin', 'founder', 'ceo', 'cmo',
    # Lead intent
    'куплю', 'продам', 'лиды', 'leads', 'buy', 'sell', 'ищу', 'looking for',
    # Affiliate
    'cpa', 'партнерка', 'affiliate', 'партнёрка', 'оффер', 'offer',
    # Influence
    'канал', 'channel', 'подписчик', 'subscriber', 'followers', 'аудитория',
    # Crypto specific
    'ton', 'crypto', 'defi', 'nft', 'web3', 'крипто', 'токен', 'token',
    # Action words
    'сотрудничество', 'collaboration', 'partnership', 'размещение', 'promotion'
]

# Compile regex for fast matching
KEYWORDS_PATTERN = re.compile('|'.join(LEAD_KEYWORDS), re.IGNORECASE)

# Discovery Mode: Regex to find Telegram links in messages
# Matches: t.me/username, t.me/joinchat/xxx, t.me/+xxx, telegram.me/xxx
TELEGRAM_LINK_PATTERN = re.compile(
    r'(?:https?://)?(?:t\.me|telegram\.me)/(?:\+|joinchat/)?([a-zA-Z0-9_\-]+)',
    re.IGNORECASE
)


@dataclass
class UserMessageData:
    """Aggregated message data for a user."""
    user_id: int
    username: Optional[str]
    display_name: Optional[str]
    bio: Optional[str] = None  # NEW: User bio
    messages: List[str] = field(default_factory=list)
    message_count: int = 0
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    has_keywords: bool = False  # NEW: Flag for keyword match
    matched_keywords: List[str] = field(default_factory=list)  # NEW: Which keywords matched
    
    def add_message(self, text: str, date: datetime) -> None:
        """Add a message to the user's collection."""
        if text and len(text.strip()) > 10:
            self.messages.append(text.strip())
            self.message_count += 1
            
            if self.first_seen is None or date < self.first_seen:
                self.first_seen = date
            if self.last_seen is None or date > self.last_seen:
                self.last_seen = date
    
    def check_keywords(self) -> bool:
        """Check if messages or bio contain lead keywords."""
        text_to_check = ' '.join(self.messages)
        if self.bio:
            text_to_check += ' ' + self.bio
        
        matches = KEYWORDS_PATTERN.findall(text_to_check.lower())
        if matches:
            self.has_keywords = True
            self.matched_keywords = list(set(matches))[:5]  # Top 5 unique
            return True
        return False


@dataclass
class ChatScrapeResult:
    """Result of scraping a single chat."""
    chat_id: int
    chat_title: str
    chat_username: Optional[str]
    total_messages: int
    unique_users: int
    keyword_matches: int  # NEW: Users with keyword matches
    users_data: List[UserMessageData]
    scraped_at: datetime = field(default_factory=datetime.now)
    errors: List[str] = field(default_factory=list)


class ScraperEngine:
    """
    Hunter 2.0 - High-velocity Telegram chat scraper with:
    - Bio fetching for profile intelligence
    - Smart keyword pre-filter before AI
    - User cache to avoid duplicate fetches
    """
    
    def __init__(
        self,
        client: TelegramClientWrapper,
        rate_limiter: RateLimiter,
        logger: Optional[AuraLogger] = None,
        messages_per_chat: int = 1000
    ):
        self.client = client
        self.rate_limiter = rate_limiter
        self.logger = logger
        self.messages_per_chat = messages_per_chat
        
        # Track processed chats
        self.processed_chats: Set[int] = set()
        self.total_messages_scraped = 0
        self.total_users_found = 0
        
        # User cache to avoid fetching same user twice
        self._user_cache: Dict[int, Dict[str, Any]] = {}
        self._analyzed_users: Set[int] = set()
        
        # Discovery Mode: Collect new Telegram links found in messages
        self._discovered_links: Set[str] = set()
        
        self._log(ThoughtType.SYSTEM, "ScraperEngine 2.0 initialized", {
            "messages_per_chat": messages_per_chat,
            "keywords_count": len(LEAD_KEYWORDS),
            "discovery_mode": True
        })
    
    def _log(self, thought_type: ThoughtType, action: str, details: dict = None) -> None:
        """Log scraper action."""
        if self.logger:
            self.logger.thought(thought_type, "ScraperEngine", action, details)
    
    def _extract_telegram_links(self, text: str, current_chat: str = None) -> List[str]:
        """
        Discovery Mode: Extract Telegram links from message text.
        Returns list of discovered chat identifiers.
        """
        if not text:
            return []
        
        links = []
        matches = TELEGRAM_LINK_PATTERN.findall(text)
        
        for match in matches:
            # Clean up the match
            identifier = match.strip()
            
            # Skip common non-chat links
            skip_patterns = ['share', 'msg', 'socks', 'proxy', 'addstickers', 'addemoji', 'setlanguage']
            if any(p in identifier.lower() for p in skip_patterns):
                continue
            
            # Skip if it's the current chat
            if current_chat and identifier.lower() == current_chat.lower():
                continue
            
            # Skip very short identifiers (likely invalid)
            if len(identifier) < 3:
                continue
            
            links.append(identifier)
        
        return links
    
    async def _fetch_user_bio(self, user_id: int) -> Optional[str]:
        """
        Fetch user bio from Telegram.
        Uses cache to avoid duplicate requests.
        """
        # Check cache first
        if user_id in self._user_cache:
            return self._user_cache[user_id].get('bio')
        
        try:
            await self.rate_limiter.wait("user_info")
            entity = await self.client.client.get_entity(user_id)
            
            if isinstance(entity, User):
                # Get full user info for bio
                full_user = await self.client.client.get_entity(user_id)
                bio = getattr(full_user, 'about', None)
                
                # Cache the result
                self._user_cache[user_id] = {
                    'bio': bio,
                    'username': entity.username,
                    'display_name': self._get_display_name(entity)
                }
                
                return bio
        except Exception as e:
            self._log(ThoughtType.WARNING, f"Failed to fetch bio for {user_id}", {
                "error": str(e)[:100]
            })
        
        return None
    
    async def join_target_chats(
        self,
        chat_links: List[str],
        skip_joined: bool = True
    ) -> List[Any]:
        """Join a list of target chats/channels."""
        joined_chats = []
        
        self._log(ThoughtType.JOIN_CHAT, f"Starting to join {len(chat_links)} chats")
        
        for i, link in enumerate(chat_links):
            try:
                await self.rate_limiter.wait("join_chat")
                
                self._log(ThoughtType.JOIN_CHAT, f"Joining chat {i+1}/{len(chat_links)}", {
                    "link": link[:30] + "..." if len(link) > 30 else link
                })
                
                chat = await self.client.join_chat(link)
                
                if chat:
                    chat_title = getattr(chat, 'title', str(chat.id))
                    joined_chats.append(chat)
                    self.rate_limiter.report_success()
                    
                    self._log(ThoughtType.SUCCESS, f"Joined: {chat_title}", {
                        "chat_id": chat.id
                    })
                    
            except FloodWaitError as e:
                self._log(ThoughtType.ERROR, f"Flood wait: {e.seconds}s", {"link": link})
                await self.rate_limiter.handle_flood_wait(e.seconds)
                try:
                    chat = await self.client.join_chat(link)
                    if chat:
                        joined_chats.append(chat)
                except Exception as retry_e:
                    self._log(ThoughtType.ERROR, f"Retry failed: {retry_e}")
                    
            except (ChatAdminRequiredError, ChannelPrivateError) as e:
                self._log(ThoughtType.WARNING, f"Cannot join chat: {e}", {"link": link})
                
            except Exception as e:
                self._log(ThoughtType.ERROR, f"Failed to join: {e}", {"link": link})
                self.rate_limiter.report_error()
        
        self._log(ThoughtType.SUCCESS, f"Join phase complete", {
            "joined": len(joined_chats),
            "total": len(chat_links)
        })
        
        return joined_chats
    
    async def scrape_chat(
        self,
        chat: Any,
        min_message_length: int = 15,
        min_messages_per_user: int = 1,  # Lowered for Hunter 2.0
        fetch_bios: bool = True
    ) -> ChatScrapeResult:
        """
        Scrape messages from a single chat with bio fetching.
        """
        chat_id = chat.id
        chat_title = getattr(chat, 'title', str(chat_id))
        chat_username = getattr(chat, 'username', None)
        
        self._log(ThoughtType.SCRAPE, f"Starting scrape: {chat_title}", {
            "chat_id": chat_id,
            "limit": self.messages_per_chat,
            "fetch_bios": fetch_bios
        })
        
        users_messages: Dict[int, UserMessageData] = {}
        total_messages = 0
        errors = []
        
        try:
            await self.rate_limiter.wait("message_fetch")
            
            async for message in self.client.iter_messages(
                chat,
                limit=self.messages_per_chat
            ):
                if not isinstance(message, Message):
                    continue
                    
                total_messages += 1
                
                if not message.sender_id:
                    continue
                
                sender = message.sender
                if not isinstance(sender, User):
                    continue
                    
                if sender.bot:
                    continue
                
                text = message.text or message.raw_text or ""
                
                # Discovery Mode: Extract Telegram links from message text
                discovered = self._extract_telegram_links(text, chat_username)
                for link in discovered:
                    self._discovered_links.add(link)
                
                # Discovery Mode: Also extract from message entities (buttons, links)
                if message.entities:
                    for entity in message.entities:
                        if hasattr(entity, 'url') and entity.url:
                            url = entity.url
                            if 't.me/' in url or 'telegram.me/' in url:
                                entity_links = self._extract_telegram_links(url, chat_username)
                                for link in entity_links:
                                    self._discovered_links.add(link)
                
                # Discovery Mode: Also extract from inline buttons
                if message.reply_markup and hasattr(message.reply_markup, 'rows'):
                    for row in message.reply_markup.rows:
                        for button in row.buttons:
                            if hasattr(button, 'url') and button.url:
                                url = button.url
                                if 't.me/' in url or 'telegram.me/' in url:
                                    btn_links = self._extract_telegram_links(url, chat_username)
                                    for link in btn_links:
                                        self._discovered_links.add(link)
                
                if len(text.strip()) < min_message_length:
                    continue
                
                user_id = sender.id
                
                # Skip already fully analyzed users (global cache)
                if user_id in self._analyzed_users:
                    continue
                
                if user_id not in users_messages:
                    users_messages[user_id] = UserMessageData(
                        user_id=user_id,
                        username=sender.username,
                        display_name=self._get_display_name(sender)
                    )
                
                users_messages[user_id].add_message(text, message.date)
                
                # Log progress every 100 messages
                if total_messages % 100 == 0:
                    self._log(ThoughtType.SCRAPE, f"Progress: {total_messages} messages", {
                        "users_found": len(users_messages)
                    })
                
                # Batch delay every 200 messages
                if total_messages % 200 == 0:
                    await self.rate_limiter.batch_delay(200, total_messages)
                    
        except FloodWaitError as e:
            errors.append(f"FloodWait: {e.seconds}s")
            await self.rate_limiter.handle_flood_wait(e.seconds)
            
        except Exception as e:
            errors.append(str(e))
            self._log(ThoughtType.ERROR, f"Scrape error: {e}", {"chat": chat_title})
        
        # Filter by minimum messages
        active_users = [
            user_data for user_data in users_messages.values()
            if user_data.message_count >= min_messages_per_user
        ]
        
        # NEW: Fetch bios for users (with rate limiting)
        if fetch_bios and active_users:
            self._log(ThoughtType.SCRAPE, f"Fetching bios for {len(active_users)} users")
            
            for i, user_data in enumerate(active_users[:50]):  # Limit to 50 bio fetches
                bio = await self._fetch_user_bio(user_data.user_id)
                if bio:
                    user_data.bio = bio
                
                # Progress log
                if (i + 1) % 10 == 0:
                    self._log(ThoughtType.SCRAPE, f"Bio fetch progress: {i+1}/{min(50, len(active_users))}")
        
        # NEW: Check keywords for each user
        keyword_matches = 0
        for user_data in active_users:
            if user_data.check_keywords():
                keyword_matches += 1
        
        # Sort: keyword matches first, then by message count
        active_users.sort(key=lambda x: (x.has_keywords, x.message_count), reverse=True)
        
        result = ChatScrapeResult(
            chat_id=chat_id,
            chat_title=chat_title,
            chat_username=chat_username,
            total_messages=total_messages,
            unique_users=len(active_users),
            keyword_matches=keyword_matches,
            users_data=active_users,
            errors=errors
        )
        
        self.processed_chats.add(chat_id)
        self.total_messages_scraped += total_messages
        self.total_users_found += len(active_users)
        
        self._log(ThoughtType.SUCCESS, f"Scrape complete: {chat_title}", {
            "total_messages": total_messages,
            "active_users": len(active_users),
            "keyword_matches": keyword_matches,
            "errors": len(errors)
        })
        
        return result
    
    async def scrape_multiple_chats(
        self,
        chats: List[Any],
        min_message_length: int = 15,
        min_messages_per_user: int = 1,
        fetch_bios: bool = True
    ) -> List[ChatScrapeResult]:
        """Scrape multiple chats sequentially with rate limiting."""
        results = []
        
        self._log(ThoughtType.SCRAPE, f"Starting multi-chat scrape", {
            "chat_count": len(chats)
        })
        
        for i, chat in enumerate(chats):
            chat_title = getattr(chat, 'title', str(chat.id))
            
            self._log(ThoughtType.SCRAPE, f"Processing chat {i+1}/{len(chats)}: {chat_title}")
            
            result = await self.scrape_chat(
                chat,
                min_message_length,
                min_messages_per_user,
                fetch_bios
            )
            results.append(result)
            
            if i < len(chats) - 1:
                await self.rate_limiter.wait("message_fetch")
        
        total_users = sum(r.unique_users for r in results)
        total_messages = sum(r.total_messages for r in results)
        total_keyword_matches = sum(r.keyword_matches for r in results)
        
        self._log(ThoughtType.SUCCESS, "Multi-chat scrape complete", {
            "chats_processed": len(results),
            "total_messages": total_messages,
            "total_users": total_users,
            "keyword_matches": total_keyword_matches
        })
        
        return results
    
    def _get_display_name(self, user: User) -> str:
        """Get user's display name."""
        parts = []
        if user.first_name:
            parts.append(user.first_name)
        if user.last_name:
            parts.append(user.last_name)
        return " ".join(parts) if parts else f"User {user.id}"
    
    def prepare_for_analysis(
        self,
        scrape_results: List[ChatScrapeResult],
        keyword_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Prepare scraped data for AI analysis.
        
        Args:
            scrape_results: List of ChatScrapeResult
            keyword_only: Only return users with keyword matches
        """
        analysis_data = []
        seen_users: Set[int] = set()
        
        for result in scrape_results:
            for user_data in result.users_data:
                # Skip duplicates
                if user_data.user_id in seen_users:
                    continue
                seen_users.add(user_data.user_id)
                
                # Skip already analyzed (global)
                if user_data.user_id in self._analyzed_users:
                    continue
                
                # Filter by keywords if requested
                if keyword_only and not user_data.has_keywords:
                    continue
                
                analysis_data.append({
                    "user_id": user_data.user_id,
                    "username": user_data.username,
                    "display_name": user_data.display_name,
                    "bio": user_data.bio,
                    "messages": user_data.messages,
                    "source_chat": result.chat_title,
                    "message_count": user_data.message_count,
                    "has_keywords": user_data.has_keywords,
                    "matched_keywords": user_data.matched_keywords
                })
        
        # Sort: keyword matches first, then by message count
        analysis_data.sort(key=lambda x: (x["has_keywords"], x["message_count"]), reverse=True)
        
        self._log(ThoughtType.SYSTEM, "Data prepared for analysis", {
            "total_users": len(analysis_data),
            "with_keywords": sum(1 for x in analysis_data if x["has_keywords"])
        })
        
        return analysis_data
    
    def mark_as_analyzed(self, user_id: int) -> None:
        """Mark user as analyzed to skip in future runs."""
        self._analyzed_users.add(user_id)
    
    def get_discovered_links(self) -> List[str]:
        """
        Discovery Mode: Get list of discovered Telegram links.
        """
        return sorted(list(self._discovered_links))
    
    def save_discovered_links(self, filepath: str = "data/potential_chats.txt") -> int:
        """
        Discovery Mode: Save discovered links to file.
        Appends to existing file, avoiding duplicates.
        
        Returns:
            Number of new links added
        """
        from pathlib import Path
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing links
        existing = set()
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        existing.add(line)
        
        # Find new links
        new_links = self._discovered_links - existing
        
        if new_links:
            # Append new links to file
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"\n# Discovered on {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                for link in sorted(new_links):
                    f.write(f"{link}\n")
            
            self._log(ThoughtType.SUCCESS, f"Discovery Mode: Saved {len(new_links)} new links", {
                "filepath": str(filepath),
                "total_discovered": len(self._discovered_links),
                "new_links": len(new_links)
            })
        
        return len(new_links)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scraper statistics including Discovery Mode."""
        return {
            "processed_chats": len(self.processed_chats),
            "total_messages_scraped": self.total_messages_scraped,
            "total_users_found": self.total_users_found,
            "cached_users": len(self._user_cache),
            "analyzed_users": len(self._analyzed_users),
            "discovered_links": len(self._discovered_links)
        }
