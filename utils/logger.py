"""
Aura Lead Hunter - Advanced Logging System
===========================================
Detailed logging for every step of the 'Thought Process'
designed to integrate with Aura AI Hub dashboard.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from enum import Enum
from dataclasses import dataclass, field, asdict
import json

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text


class ThoughtType(str, Enum):
    """Types of thoughts/steps in the lead hunting process."""
    SYSTEM = "🔧 SYSTEM"
    CONNECT = "🔌 CONNECT"
    JOIN_CHAT = "📢 JOIN_CHAT"
    SCRAPE = "🔍 SCRAPE"
    ANALYZE = "🧠 ANALYZE"
    RATE_LIMIT = "⏱️ RATE_LIMIT"
    LEAD_FOUND = "🎯 LEAD_FOUND"
    EXPORT = "💾 EXPORT"
    ERROR = "❌ ERROR"
    WARNING = "⚠️ WARNING"
    SUCCESS = "✅ SUCCESS"


@dataclass
class ThoughtLog:
    """Structured thought log entry for Aura Hub integration."""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    thought_type: str = ""
    component: str = ""
    action: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    duration_ms: Optional[float] = None
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


class AuraLogger:
    """
    Advanced logger with structured output for Aura AI Hub.
    Provides both console and file logging with rich formatting.
    """
    
    def __init__(
        self,
        name: str = "AuraLeadHunter",
        log_file: Optional[Path] = None,
        level: str = "DEBUG"
    ):
        self.name = name
        self.console = Console()
        self.log_file = log_file
        
        # Setup standard logging
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.logger.handlers.clear()
        
        # Rich console handler
        console_handler = RichHandler(
            console=self.console,
            show_time=True,
            show_path=False,
            rich_tracebacks=True,
            markup=True
        )
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)
        
        # File handler for structured JSON logs
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # JSON log file for Aura Hub
        self.json_log_file = log_file.with_suffix('.jsonl') if log_file else None
    
    def _write_json_log(self, thought: ThoughtLog) -> None:
        """Write structured log to JSONL file for Aura Hub."""
        if self.json_log_file:
            with open(self.json_log_file, 'a', encoding='utf-8') as f:
                f.write(thought.to_json() + '\n')
    
    def thought(
        self,
        thought_type: ThoughtType,
        component: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[float] = None
    ) -> None:
        """
        Log a thought process step with rich formatting.
        This is the main logging method for Aura Hub integration.
        """
        thought_log = ThoughtLog(
            thought_type=thought_type.value,
            component=component,
            action=action,
            details=details or {},
            duration_ms=duration_ms
        )
        
        # Console output with rich formatting
        message = f"[bold]{thought_type.value}[/bold] [{component}] {action}"
        if details:
            details_str = " | ".join(f"{k}={v}" for k, v in details.items())
            message += f" | {details_str}"
        if duration_ms:
            message += f" | ⏱️ {duration_ms:.2f}ms"
        
        self.logger.info(message)
        
        # Write to JSON log
        self._write_json_log(thought_log)
    
    def panel(self, title: str, content: str, style: str = "blue") -> None:
        """Display a rich panel for important information."""
        self.console.print(Panel(content, title=title, border_style=style))
    
    def lead_found(
        self,
        username: str,
        confidence: float,
        reason: str,
        chat_source: str
    ) -> None:
        """Special logging for found leads."""
        self.thought(
            ThoughtType.LEAD_FOUND,
            "IntentAnalyzer",
            f"Potential affiliate partner identified: @{username}",
            {
                "confidence": f"{confidence:.2%}",
                "reason": reason[:100],
                "source_chat": chat_source
            }
        )
        
        # Visual highlight
        lead_text = Text()
        lead_text.append("🎯 LEAD FOUND: ", style="bold green")
        lead_text.append(f"@{username}", style="bold cyan")
        lead_text.append(f" | Confidence: {confidence:.2%}", style="yellow")
        self.console.print(lead_text)
    
    def error(self, component: str, message: str, exception: Optional[Exception] = None) -> None:
        """Log an error with optional exception details."""
        details = {"error": message}
        if exception:
            details["exception_type"] = type(exception).__name__
            details["exception_msg"] = str(exception)
        
        self.thought(ThoughtType.ERROR, component, message, details)
        self.logger.error(f"[{component}] {message}", exc_info=exception)
    
    def warn(self, component: str, message: str) -> None:
        """Log a warning."""
        self.thought(ThoughtType.WARNING, component, message)
    
    def success(self, component: str, message: str, details: Optional[Dict] = None) -> None:
        """Log a success event."""
        self.thought(ThoughtType.SUCCESS, component, message, details)
    
    def startup_banner(self) -> None:
        """Display startup banner."""
        banner = """
   ▄▀█ █░█ █▀█ ▄▀█   █░░ █▀▀ ▄▀█ █▀▄   █░█ █░█ █▄░█ ▀█▀ █▀▀ █▀█
   █▀█ █▄█ █▀▄ █▀█   █▄▄ ██▄ █▀█ █▄▀   █▀█ █▄█ █░▀█ ░█░ ██▄ █▀▄
   
   🚀 Crypto Affiliate Lead Generation Engine
   🔥 Powered by Telethon + AI Intent Analysis
"""
        self.console.print(Panel(banner, title="[bold cyan]AURA LEAD HUNTER[/bold cyan]", border_style="cyan"))


# Global logger instance
def get_logger(log_file: Optional[Path] = None, level: str = "DEBUG") -> AuraLogger:
    """Get or create the global logger instance."""
    return AuraLogger(log_file=log_file, level=level)
