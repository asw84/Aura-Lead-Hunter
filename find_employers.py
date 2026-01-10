"""
Aura Lead Hunter - Find Employers Mode
=======================================
Специальный режим для поиска РАБОТОДАТЕЛЕЙ в арбитраже:
- Тимлиды, которые ищут байеров
- Владельцы команд с вакансиями
- Агентства, которые набирают людей

Usage:
    py find_employers.py                    # Поиск по дефолтным чатам
    py find_employers.py --chats chat1,chat2  # Свои чаты
"""

import asyncio
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass, field

from config.settings import settings
from core.telegram_client import TelegramClient
from core.rate_limiter import RateLimiter
from core.intent_analyzer import IntentAnalyzer, LeadAnalysis
from storage.csv_exporter import CSVExporter
from storage.report_generator import generate_html_report
from utils.logger import get_logger, ThoughtType

from telethon.tl.types import Message, User
from telethon.errors import FloodWaitError


# ===== КЛЮЧЕВИКИ ДЛЯ ПОИСКА РАБОТОДАТЕЛЕЙ =====
EMPLOYER_KEYWORDS = [
    # Прямой найм (RU)
    'ищу баера', 'ищу байера', 'нужен баер', 'нужен байер', 
    'ищу арбитражника', 'нужен арбитражник',
    'ищу в команду', 'ищем в команду', 'нужен в команду',
    'набор в команду', 'набираю команду', 'набираем',
    'ищу фармера', 'нужен фармер', 'требуется фармер',
    'ищу креативщика', 'нужен дизайнер', 'ищу дизайнера',
    'вакансия', 'вакансии', 'открыта вакансия',
    'ищу менеджера', 'нужен менеджер',
    'ищу обработчика', 'нужен обработчик',
    
    # Прямой найм (EN)
    'hiring', 'looking for buyer', 'need media buyer',
    'join our team', 'we are hiring', 'looking for affiliate',
    'seeking traffic', 'need trafficker', 'open position',
    'media buyer', 'sales manager',
    
    # 🇺🇦 Украинские ключевики
    'шукаємо', 'шукають', 'шукаю',  # ищем/ищут/ищу
    'потрібен', 'потрібна', 'потрібні',  # нужен/нужна/нужны
    'запрошуємо', 'запрошую',  # приглашаем
    'приєднуйся', 'приєднуйтесь',  # присоединяйся
    'працювати з нами', 'до нас',  # работать с нами
    'вакансія', 'вакансії',  # вакансия
    'команда професіоналів',  # команда профессионалов
    'тобі до нас', 'тебе к нам',  # тебе к нам
    'чекаємо', 'пиши @',  # ждём, пиши @
    'media buyer', 'медіа баєр',
    
    # Тим лид / Команда
    'тимлид', 'team lead', 'тим лид', 'наша команда',
    'у нас команда', 'моя команда', 'есть команда',
    'тима', 'тимка', 'наша тима',
    'сильные тимлиды', 'наставничество',
    
    # Предложения работы / Условия
    'предлагаю работу', 'предлагаем работу', 'оффер для баера',
    'готов платить', 'платим от', 'зп от', 'з/п',
    'ставка', 'фикс +', 'фикс+', 'процент от профита', 
    'доход от', 'заработок от', 'оплата',
    'реальный доход', 'доход от $', 'від $',
    'карьерный рост', 'кар\'єрний ріст',
    'оплачувана відпустка', 'отпуск',
    'топові умови', 'топовые условия',
    'гнучкий формат', 'віддалено', 'удалённо',
    
    # Обработчик трафика / Sales
    'обработчик трафика', 'закрывать возражения',
    'схемный трафик', 'закрытие лидов',
    'обробник трафіку',
    
    # Партнёрство с командой
    'ищем партнера', 'ищу партнёра', 'нужен партнер',
    'коллаборация', 'совместный проект',
    
    # Ресурсы / Признаки большого игрока
    'аккаунты под ключ', 'готовые аки', 'крео под ключ',
    'закупаем трафик', 'закуп трафика', 'льём от',
    'обьемы от', 'объёмы от', 'спенд от', 'бюджет от',
    'даём бюджет', 'выделяем бюджет',
    'топ-бюджетами', 'великими бюджетами',
    
    # Признаки владельца команды
    'owner', 'владелец', 'основатель', 'founder', 'ceo',
    'руковожу командой', 'моя агенция', 'наше агентство',
    
    # HR / Рекрутинг
    'hr_', '@hr', 'рекрутер', 'recruiter',
    'ти нам підходиш', 'ты нам подходишь',
    'готовий підкорювати', 'готов покорять'
]

# Компилируем regex для быстрого поиска
EMPLOYER_PATTERN = re.compile('|'.join(map(re.escape, EMPLOYER_KEYWORDS)), re.IGNORECASE)


# Кастомный системный промпт для анализа работодателей
EMPLOYER_SYSTEM_PROMPT = """You are a recruiter scout analyzing Telegram users. Your task is to find EMPLOYERS - people who are HIRING staff for affiliate marketing teams.

🎯 HIGH-VALUE TARGETS (score 8-10):
- Team leads actively looking for media buyers
- Team owners posting job openings
- Agency owners recruiting staff
- People offering salaries, budgets, or profit shares
- Anyone saying "ищу баера", "набираем в команду", "hiring"

✅ MEDIUM TARGETS (score 5-7):
- People mentioning they have a team
- Those discussing staff requirements
- People looking for partners with experience
- Anyone talking about team expansion

❌ NOT A TARGET (score 1-4):
- Regular affiliates looking for offers
- People looking for work themselves
- Spammers, bots
- Just chatting

📝 PROVIDE REASON IN BOTH LANGUAGES:
- reason_en: Why this person is hiring (max 80 chars)
- reason_ru: Почему это работодатель (макс 80 символов), используй сленг: тимлид, тима, байер

Respond ONLY with valid JSON:
{
    "is_lead": true/false,
    "score": 1-10,
    "category": "team_lead" | "agency_owner" | "recruiter" | "partner_seeker" | "potential_employer" | "not_employer",
    "reason_en": "Brief explanation IN ENGLISH",
    "reason_ru": "Краткое пояснение НА РУССКОМ"
}"""


@dataclass
class EmployerData:
    """Data for potential employer."""
    user_id: int
    username: Optional[str]
    display_name: Optional[str]
    bio: Optional[str] = None
    messages: List[str] = field(default_factory=list)
    matched_keywords: List[str] = field(default_factory=list)
    source_chat: str = ""
    
    def check_employer_keywords(self) -> bool:
        """Check if messages contain employer keywords."""
        text_to_check = ' '.join(self.messages)
        if self.bio:
            text_to_check += ' ' + self.bio
        
        matches = EMPLOYER_PATTERN.findall(text_to_check.lower())
        if matches:
            self.matched_keywords = list(set(matches))[:5]
            return True
        return False


async def scrape_for_employers(
    client,
    chat,
    rate_limiter,
    logger,
    messages_limit: int = 1000
) -> List[EmployerData]:
    """Scrape chat for potential employers."""
    
    chat_title = getattr(chat, 'title', str(chat.id))
    chat_username = getattr(chat, 'username', None)
    
    logger.thought(ThoughtType.SCRAPE, "EmployerScraper", f"🔎 Scanning for employers: {chat_title}", {
        "limit": messages_limit
    })
    
    users_data: Dict[int, EmployerData] = {}
    total_messages = 0
    
    try:
        await rate_limiter.wait("message_fetch")
        
        async for message in client.iter_messages(chat, limit=messages_limit):
            if not isinstance(message, Message):
                continue
            
            total_messages += 1
            
            if not message.sender_id:
                continue
            
            sender = message.sender
            if not isinstance(sender, User) or sender.bot:
                continue
            
            text = message.text or message.raw_text or ""
            if len(text.strip()) < 20:  # Минимум 20 символов для вакансий
                continue
            
            user_id = sender.id
            
            if user_id not in users_data:
                display_name = ""
                if sender.first_name:
                    display_name = sender.first_name
                if sender.last_name:
                    display_name += " " + sender.last_name
                
                users_data[user_id] = EmployerData(
                    user_id=user_id,
                    username=sender.username,
                    display_name=display_name.strip() or f"User {user_id}",
                    source_chat=chat_title
                )
            
            users_data[user_id].messages.append(text)
            
            # Progress log
            if total_messages % 200 == 0:
                logger.thought(ThoughtType.SCRAPE, "EmployerScraper", f"Progress: {total_messages} messages", {
                    "users": len(users_data)
                })
            
            # Rate limit delay
            if total_messages % 200 == 0:
                await rate_limiter.batch_delay(200, total_messages)
                
    except FloodWaitError as e:
        logger.thought(ThoughtType.ERROR, "EmployerScraper", f"FloodWait: {e.seconds}s")
        await rate_limiter.handle_flood_wait(e.seconds)
    except Exception as e:
        logger.thought(ThoughtType.ERROR, "EmployerScraper", f"Error scraping: {e}")
    
    # Filter: only users with employer keywords
    employers = []
    for user_data in users_data.values():
        if user_data.check_employer_keywords():
            employers.append(user_data)
    
    # Sort by keyword count
    employers.sort(key=lambda x: len(x.matched_keywords), reverse=True)
    
    logger.thought(ThoughtType.SUCCESS, "EmployerScraper", f"✅ Found {len(employers)} potential employers in {chat_title}", {
        "total_messages": total_messages,
        "total_users": len(users_data),
        "with_keywords": len(employers)
    })
    
    return employers


async def run_employer_hunt(target_chats: list[str] = None):
    """Main execution flow for finding employers."""
    
    # Initialize
    settings.ensure_directories()
    logger = get_logger(settings.logging.log_file, settings.logging.level)
    
    logger.panel(
        "🏢 EMPLOYER HUNT MODE",
        "Поиск работодателей в арбитраже:\n"
        "• Тимлиды с вакансиями\n"
        "• Владельцы команд\n"
        "• Агентства на найме",
        "magenta"
    )
    
    # Validate config
    try:
        settings.validate()
    except ValueError as e:
        logger.error("Configuration", str(e))
        return
    
    # Target chats
    chats_to_scrape = target_chats or settings.scraper.target_chats
    if not chats_to_scrape:
        logger.error("Configuration", "No target chats specified")
        return
    
    logger.thought(ThoughtType.SYSTEM, "EmployerHunt", "Starting Employer Hunt", {
        "target_chats": len(chats_to_scrape),
        "employer_keywords": len(EMPLOYER_KEYWORDS)
    })
    
    # Initialize components
    rate_limiter = RateLimiter(
        min_delay=settings.scraper.delay_min,
        max_delay=settings.scraper.delay_max,
        logger=logger
    )
    
    intent_analyzer = IntentAnalyzer(settings.llm, logger)
    # Override system prompt for employer detection
    from core import intent_analyzer as ia_module
    original_prompt = ia_module.BILINGUAL_SYSTEM_PROMPT
    ia_module.BILINGUAL_SYSTEM_PROMPT = EMPLOYER_SYSTEM_PROMPT
    
    csv_exporter = CSVExporter(settings.export.export_dir, logger)
    
    all_employers: List[EmployerData] = []
    
    # Connect to Telegram
    async with TelegramClient(settings.telegram, logger) as client:
        
        # Phase 1: Join chats
        logger.panel("PHASE 1", "Joining target chats...", "cyan")
        joined_chats = []
        
        for i, link in enumerate(chats_to_scrape):
            try:
                await rate_limiter.wait("join_chat")
                logger.thought(ThoughtType.JOIN_CHAT, "EmployerHunt", f"Joining {i+1}/{len(chats_to_scrape)}: {link}")
                chat = await client.join_chat(link)
                if chat:
                    joined_chats.append(chat)
                    logger.thought(ThoughtType.SUCCESS, "EmployerHunt", f"Joined: {getattr(chat, 'title', link)}")
            except Exception as e:
                logger.thought(ThoughtType.WARNING, "EmployerHunt", f"Failed to join {link}: {e}")
        
        if not joined_chats:
            logger.error("Scraper", "Could not join any chats")
            return
        
        # Phase 2: Scrape for employers
        logger.panel("PHASE 2", "Scanning for employers...", "yellow")
        
        for chat in joined_chats:
            employers = await scrape_for_employers(
                client,
                chat,
                rate_limiter,
                logger,
                settings.scraper.messages_per_chat
            )
            all_employers.extend(employers)
            await rate_limiter.wait("message_fetch")
    
    # Remove duplicates by user_id
    seen_ids: Set[int] = set()
    unique_employers = []
    for emp in all_employers:
        if emp.user_id not in seen_ids:
            seen_ids.add(emp.user_id)
            unique_employers.append(emp)
    
    logger.panel("PHASE 3", f"Analyzing {len(unique_employers)} potential employers with AI...", "green")
    
    # Prepare for AI analysis
    users_data = []
    for emp in unique_employers[:50]:  # Limit to 50 for API costs
        users_data.append({
            "user_id": emp.user_id,
            "username": emp.username,
            "display_name": emp.display_name,
            "bio": emp.bio,
            "messages": emp.messages[:10],  # Top 10 messages
            "source_chat": emp.source_chat,
            "message_count": len(emp.messages),
            "has_keywords": True,
            "matched_keywords": emp.matched_keywords
        })
    
    # AI Analysis
    all_leads = []
    if users_data:
        all_leads = await intent_analyzer.batch_analyze(users_data)
    
    # Restore original prompt
    ia_module.BILINGUAL_SYSTEM_PROMPT = original_prompt
    
    # Phase 4: Export results
    logger.panel("PHASE 4", "Exporting employer leads...", "magenta")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Filter: score >= 5
    employer_leads = [l for l in all_leads if l.is_lead and l.score >= 5]
    
    if employer_leads:
        # Export to CSV
        csv_path = csv_exporter.export_leads(
            employer_leads,
            f"employers_{timestamp}.csv"
        )
        logger.success("Export", f"Employers saved to {csv_path}")
        
        # Export contacts for outreach
        export_dir = Path(settings.export.export_dir)
        
        hot_employers = [l for l in employer_leads if l.score >= 7]
        warm_employers = [l for l in employer_leads if 5 <= l.score < 7]
        
        # Hot employers file
        hot_file = export_dir / f"employers_hot_{timestamp}.txt"
        with open(hot_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🏢 HOT EMPLOYERS (Score >= 7) - {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write(f"# Total: {len(hot_employers)} contacts\n")
            f.write("# " + "─" * 50 + "\n\n")
            
            for lead in hot_employers:
                if lead.username:
                    f.write(f"@{lead.username}\n")
                else:
                    f.write(f"tg://user?id={lead.user_id}\n")
            
            f.write("\n# " + "─" * 50 + "\n")
            f.write("# Details:\n")
            for lead in hot_employers:
                contact = f"@{lead.username}" if lead.username else f"ID:{lead.user_id}"
                f.write(f"# {contact:25} | {lead.score}/10 | {lead.category:18} | {lead.reason_ru[:60]}\n")
        
        # Warm employers file
        warm_file = export_dir / f"employers_warm_{timestamp}.txt"
        with open(warm_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🟡 WARM EMPLOYERS (Score 5-6) - {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write(f"# Total: {len(warm_employers)} contacts\n\n")
            for lead in warm_employers:
                if lead.username:
                    f.write(f"@{lead.username}\n")
                else:
                    f.write(f"tg://user?id={lead.user_id}\n")
        
        logger.success("Export", f"📤 Hot employers: {hot_file}")
        logger.success("Export", f"📤 Warm employers: {warm_file}")
    
    # Generate HTML Report
    if all_leads:
        report_path = generate_html_report(
            all_leads,
            f"data/report_employers_{timestamp}.html",
            chats_processed=len(joined_chats),
            discovered_links=0
        )
        logger.success("Report", f"HTML report: {report_path}")
        
        # Auto-open
        import webbrowser
        import os
        webbrowser.open('file://' + os.path.realpath(report_path))
    
    # Final summary
    hot_count = len([l for l in employer_leads if l.score >= 7])
    warm_count = len([l for l in employer_leads if 5 <= l.score < 7])
    
    # Category breakdown
    categories = {}
    for lead in all_leads:
        cat = lead.category
        categories[cat] = categories.get(cat, 0) + 1
    
    logger.panel(
        "🏢 EMPLOYER HUNT ЗАВЕРШЁН",
        f"✅ Обработано чатов: {len(joined_chats)}\n"
        f"👥 Найдено с ключевиками: {len(unique_employers)}\n"
        f"🤖 Проанализировано AI: {len(all_leads)}\n"
        f"🔥 Горячих работодателей: {hot_count}\n"
        f"🟡 Тёплых работодателей: {warm_count}\n"
        f"📊 Категории: {categories}\n"
        f"💾 Экспортировано в: {settings.export.export_dir}",
        "green"
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Aura Lead Hunter - Employer Hunt Mode")
    parser.add_argument(
        "--chats",
        type=str,
        help="Comma-separated list of chat usernames to scan"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    target_chats = None
    if args.chats:
        target_chats = [c.strip() for c in args.chats.split(",")]
    
    asyncio.run(run_employer_hunt(target_chats))
