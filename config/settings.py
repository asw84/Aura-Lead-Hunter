"""
Aura Lead Hunter - Configuration Settings
==========================================
Centralized configuration loaded from environment variables.
All sensitive data is stored in .env file.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class TelegramConfig:
    """Telegram API configuration."""
    api_id: int = field(default_factory=lambda: int(os.getenv("TELEGRAM_API_ID", "0")))
    api_hash: str = field(default_factory=lambda: os.getenv("TELEGRAM_API_HASH", ""))
    phone: str = field(default_factory=lambda: os.getenv("TELEGRAM_PHONE", ""))
    session_name: str = field(default_factory=lambda: os.getenv("TELEGRAM_SESSION_NAME", "aura_session"))
    
    @property
    def session_path(self) -> Path:
        return Path("sessions") / self.session_name


@dataclass
class LLMConfig:
    """LLM/AI configuration for intent analysis."""
    api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", ""))
    base_url: str = field(default_factory=lambda: os.getenv("OPENROUTER_BASE_URL") or os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "google/gemini-2.0-flash-exp:free"))


@dataclass
class ScraperConfig:
    """Scraper behavior configuration."""
    delay_min: float = field(default_factory=lambda: float(os.getenv("SCRAPE_DELAY_MIN", "2.0")))
    delay_max: float = field(default_factory=lambda: float(os.getenv("SCRAPE_DELAY_MAX", "5.0")))
    messages_per_chat: int = field(default_factory=lambda: int(os.getenv("MESSAGES_PER_CHAT", "100")))
    join_delay_min: float = field(default_factory=lambda: float(os.getenv("JOIN_DELAY_MIN", "30.0")))
    join_delay_max: float = field(default_factory=lambda: float(os.getenv("JOIN_DELAY_MAX", "60.0")))
    
    @property
    def target_chats(self) -> List[str]:
        raw = os.getenv("TARGET_CHATS", "")
        return [chat.strip() for chat in raw.split(",") if chat.strip()]


@dataclass
class ExportConfig:
    """Data export configuration."""
    export_dir: Path = field(default_factory=lambda: Path(os.getenv("EXPORT_DIR", "./data")))
    csv_filename: str = field(default_factory=lambda: os.getenv("CSV_FILENAME", "leads_export.csv"))
    
    @property
    def csv_path(self) -> Path:
        return self.export_dir / self.csv_filename


@dataclass
class LoggingConfig:
    """Logging configuration for Aura Hub integration."""
    level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "DEBUG"))
    log_file: Path = field(default_factory=lambda: Path(os.getenv("LOG_FILE", "./logs/aura_hunter.log")))


@dataclass
class Settings:
    """Main settings container."""
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    scraper: ScraperConfig = field(default_factory=ScraperConfig)
    export: ExportConfig = field(default_factory=ExportConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    def validate(self) -> bool:
        """Validate that all required settings are present."""
        errors = []
        
        if not self.telegram.api_id:
            errors.append("TELEGRAM_API_ID is required")
        if not self.telegram.api_hash:
            errors.append("TELEGRAM_API_HASH is required")
        if not self.llm.api_key:
            errors.append("OPENROUTER_API_KEY or OPENAI_API_KEY is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.export.export_dir.mkdir(parents=True, exist_ok=True)
        self.logging.log_file.parent.mkdir(parents=True, exist_ok=True)
        Path("sessions").mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
