"""
Aura Lead Hunter 2.0 - Main Entry Point
=========================================
High-velocity Telegram Lead Generation & Intent Analysis Engine
with Bio fetching, keyword pre-filter, and optimized AI analysis.

Usage:
    py main.py                    # Run with default settings
    py main.py --chats chat1,chat2  # Override target chats
    py main.py --keywords-only    # Only analyze users with keyword matches
"""

import asyncio
import argparse
from datetime import datetime
from pathlib import Path

from config.settings import settings
from core.telegram_client import TelegramClient
from core.scraper import ScraperEngine
from core.intent_analyzer import IntentAnalyzer
from core.rate_limiter import RateLimiter
from storage.csv_exporter import CSVExporter
from storage.report_generator import generate_html_report
from utils.logger import get_logger, ThoughtType


async def run_lead_hunter(target_chats: list[str] = None, keywords_only: bool = False):
    """
    Hunter 2.0: Main execution flow with bio fetching and keyword pre-filter.
    """
    # Initialize logger
    settings.ensure_directories()
    logger = get_logger(settings.logging.log_file, settings.logging.level)
    logger.startup_banner()
    
    # Validate configuration
    try:
        settings.validate()
    except ValueError as e:
        logger.error("Configuration", str(e))
        return
    
    # Use provided chats or from settings
    chats_to_scrape = target_chats or settings.scraper.target_chats
    
    if not chats_to_scrape:
        logger.error("Configuration", "No target chats specified")
        return
    
    logger.thought(
        ThoughtType.SYSTEM,
        "Starting Lead Hunter 2.0",
        {
            "target_chats": len(chats_to_scrape),
            "messages_per_chat": settings.scraper.messages_per_chat,
            "keywords_only": keywords_only
        }
    )
    
    # Initialize components
    rate_limiter = RateLimiter(
        min_delay=settings.scraper.delay_min,
        max_delay=settings.scraper.delay_max,
        logger=logger
    )
    
    intent_analyzer = IntentAnalyzer(settings.llm, logger)
    csv_exporter = CSVExporter(settings.export.export_dir, logger)
    
    all_leads = []
    
    # Connect to Telegram
    async with TelegramClient(settings.telegram, logger) as client:
        scraper = ScraperEngine(
            client,
            rate_limiter,
            logger,
            settings.scraper.messages_per_chat
        )
        
        # Phase 1: Join target chats
        logger.panel("PHASE 1", "Joining target chats...", "cyan")
        joined_chats = await scraper.join_target_chats(chats_to_scrape)
        
        if not joined_chats:
            logger.error("Scraper", "Could not join any chats")
            return
        
        # Phase 2: Scrape messages with bio fetching
        logger.panel("PHASE 2", "Scraping messages + fetching bios...", "yellow")
        scrape_results = await scraper.scrape_multiple_chats(
            joined_chats,
            min_message_length=15,
            min_messages_per_user=1,
            fetch_bios=True
        )
        
        # Phase 3: Prepare data for analysis
        logger.panel("PHASE 3", "Analyzing users with AI...", "green")
        users_data = scraper.prepare_for_analysis(
            scrape_results, 
            keyword_only=keywords_only
        )
        
        # Stats
        total_users = len(users_data)
        keyword_users = sum(1 for u in users_data if u.get("has_keywords", False))
        
        logger.thought(ThoughtType.SYSTEM, "Analysis queue prepared", {
            "total_users": total_users,
            "with_keywords": keyword_users,
            "with_bio": sum(1 for u in users_data if u.get("bio"))
        })
        
        # Limit total users to analyze (prioritize keyword matches)
        max_users = 100
        if len(users_data) > max_users:
            # Sort by keywords first, then message count
            users_data.sort(key=lambda x: (x.get("has_keywords", False), x.get("message_count", 0)), reverse=True)
            users_data = users_data[:max_users]
            logger.thought(ThoughtType.SYSTEM, "User limit applied", {"max_users": max_users})
        
        # Phase 4: AI Analysis
        if users_data:
            all_leads = await intent_analyzer.batch_analyze(users_data)
        
        # Discovery Mode: Save discovered chat links
        new_links = scraper.save_discovered_links()
        discovered_total = len(scraper.get_discovered_links())
        
        await rate_limiter.wait("message_fetch")
    
    # Phase 5: Export results
    logger.panel("PHASE 5", "Exporting leads to CSV...", "magenta")
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Leads: is_lead=True and score >= 5
    positive_leads = [l for l in all_leads if l.is_lead and l.score >= 5]
    
    if positive_leads:
        csv_path = csv_exporter.export_leads(
            positive_leads,
            f"leads_{timestamp}.csv"
        )
        logger.success("Export", f"Leads saved to {csv_path}", {
            "leads_count": len(positive_leads)
        })
    
    # All users export
    all_users_path = csv_exporter.export_all_users(
        all_leads,
        f"all_users_{timestamp}.csv"
    )
    
    # Category breakdown
    categories = {}
    for lead in all_leads:
        cat = lead.category
        categories[cat] = categories.get(cat, 0) + 1
    
    # Final summary
    logger.panel(
        "🎉 HUNTER 2.0 ЗАВЕРШЕНО",
        f"✅ Обработано чатов: {len(joined_chats)}\n"
        f"👥 Проанализировано пользователей: {len(all_leads)}\n"
        f"🔑 С ключевыми словами: {keyword_users}\n"
        f"🎯 Найдено лидов (score≥5): {len(positive_leads)}\n"
        f"📊 Категории: {categories}\n"
        f"🔍 Discovery Mode: найдено {discovered_total} ссылок (+{new_links} новых)\n"
        f"💾 Экспортировано в: {settings.export.export_dir}",
        "green"
    )
    
    # Show API stats
    ai_stats = intent_analyzer.get_stats()
    logger.thought(ThoughtType.SYSTEM, "AI API Usage", {
        "total_requests": ai_stats["total_requests"],
        "total_tokens": ai_stats["total_tokens"]
    })
    
    # Generate HTML Report
    if all_leads:
        report_path = generate_html_report(
            all_leads,
            f"data/report_{timestamp}.html",
            chats_processed=len(joined_chats),
            discovered_links=discovered_total
        )
        logger.success("Report", f"HTML отчёт создан: {report_path}")
        
        # Auto-open in browser
        import webbrowser
        import os
        webbrowser.open('file://' + os.path.realpath(report_path))


def parse_args():
    parser = argparse.ArgumentParser(description="Aura Lead Hunter 2.0")
    parser.add_argument(
        "--chats",
        type=str,
        help="Comma-separated list of chat usernames to scrape"
    )
    parser.add_argument(
        "--keywords-only",
        action="store_true",
        help="Only analyze users with keyword matches (faster)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    target_chats = None
    if args.chats:
        target_chats = [c.strip() for c in args.chats.split(",")]
    
    asyncio.run(run_lead_hunter(target_chats, args.keywords_only))
