<div align="center">

# 🎯 Aura Lead Hunter 2.0

### High-Velocity Telegram Lead Generation Engine for Crypto Affiliate Networks

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Telethon](https://img.shields.io/badge/Telethon-1.36+-green.svg)](https://docs.telethon.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Automated lead discovery from Telegram chats with AI-powered intent analysis, bio fetching, and smart keyword pre-filtering.*

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Configuration](#%EF%B8%8F-configuration) • [Usage](#-usage) • [API Reference](#-api-reference)

</div>

---

## 🚀 Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **🔍 Deep Scraping** | Scrape up to 1000+ messages per chat with rate-limit-aware delays |
| **👤 Bio Fetching** | Automatically fetch user bios for enhanced profiling |
| **🔑 Keyword Pre-filter** | 40+ industry keywords filter users BEFORE expensive AI calls |
| **🤖 AI Intent Analysis** | LLM-powered lead scoring (1-10) with category classification |
| **🔗 Discovery Mode** | Automatically discovers new Telegram chats from messages |
| **📊 HTML Reports** | Beautiful dark-themed reports with PDF export |
| **💾 History Preservation** | Timestamped exports — never overwrite previous hunts |

### Lead Categories

```
traffic_buyer   → Active traffic buyers/arbitrageurs
advertiser      → Ad placement buyers  
influencer      → Channel owners with audience
community_owner → Group/channel admins
marketing_pro   → Marketing managers, CMOs
potential       → Promising leads for follow-up
```

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AURA LEAD HUNTER 2.0                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Telegram   │───▶│   Scraper    │───▶│  AI Analyzer │      │
│  │    Client    │    │   Engine     │    │  (OpenRouter)│      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                    │              │
│         ▼                   ▼                    ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Rate Limiter │    │  Discovery   │    │    CSV +     │      │
│  │  (FloodWait) │    │    Mode      │    │ HTML Export  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tech Stack

- **Telethon** — MTProto Telegram client
- **OpenRouter** — Multi-model LLM gateway (DeepSeek, GPT-4, Claude)
- **Pandas** — Data processing & CSV export
- **Rich** — Beautiful console output
- **asyncio** — High-performance async I/O

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Telegram API credentials ([my.telegram.org](https://my.telegram.org))
- OpenRouter API key ([openrouter.ai](https://openrouter.ai))

### Installation

```bash
# Clone repository
git clone https://github.com/asw84/Aura-Lead-Hunter.git
cd Aura-Lead-Hunter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### First Run

```bash
# Authorize with Telegram (QR code or phone)
python qr_login.py

# Start hunting
python main.py
```

---

## ⚙️ Configuration

### Environment Variables

```env
# Telegram API (from my.telegram.org)
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+1234567890

# LLM Configuration
OPENROUTER_API_KEY=sk-or-v1-xxx
LLM_MODEL=deepseek/deepseek-chat

# Scraper Settings
MESSAGES_PER_CHAT=1000
SCRAPE_DELAY_MIN=3.0
SCRAPE_DELAY_MAX=7.0
JOIN_DELAY_MIN=90.0
JOIN_DELAY_MAX=180.0

# Target Chats (comma-separated)
TARGET_CHATS=chat1,chat2,chat3
```

### Rate Limiting Strategy

| Action | Delay | Rationale |
|--------|-------|-----------|
| Message fetch | 3-7s | Avoid FloodWait |
| Chat join | 90-180s | Prevent account ban |
| AI request | 4s | API rate limit |
| Bio fetch | Per-user cache | Minimize API calls |

---

## 📖 Usage

### Basic Hunt

```bash
python main.py
```

### Custom Chats

```bash
python main.py --chats chat1,chat2,chat3
```

### Keywords-Only Mode (Faster)

```bash
python main.py --keywords-only
```

### Output Files

```
data/
├── leads_YYYYMMDD_HHMMSS.csv      # High-score leads (score ≥ 5)
├── all_users_YYYYMMDD_HHMMSS.csv  # All analyzed users
├── report_YYYYMMDD_HHMMSS.html    # Visual HTML report
└── potential_chats.txt             # Discovered chat links
```

---

## 📚 API Reference

### ScraperEngine

```python
from core.scraper import ScraperEngine

scraper = ScraperEngine(
    client=telegram_client,
    rate_limiter=rate_limiter,
    logger=aura_logger,
    messages_per_chat=1000
)

# Scrape multiple chats
results = await scraper.scrape_multiple_chats(
    chat_handles=["chat1", "chat2"],
    min_message_length=15,
    min_messages_per_user=1,
    fetch_bios=True
)

# Get discovered links (Discovery Mode)
new_links = scraper.get_discovered_links()
```

### IntentAnalyzer

```python
from core.intent_analyzer import IntentAnalyzer

analyzer = IntentAnalyzer(llm_config, logger)

# Analyze single user
lead = await analyzer.analyze_user(
    user_id=123456,
    username="johndoe",
    display_name="John",
    messages=["I'm looking for traffic offers..."],
    source_chat="arbitrage_chat",
    bio="Traffic buyer | FB/TikTok",
    has_keywords=True,
    matched_keywords=["traffic", "offers"]
)

# Lead result
print(f"Score: {lead.score}/10")
print(f"Category: {lead.category}")
print(f"Reason: {lead.reason}")
```

---

## 🛡 Security

### Protected Data

| Data | Protection |
|------|------------|
| `.env` | Gitignored, never committed |
| `*.session` | Telegram auth tokens — NEVER share |
| `data/*.csv` | Contains PII — gitignored |
| `data/*.html` | May contain usernames — gitignored |

### Best Practices

1. **Never commit `.env`** — Contains API keys
2. **Protect `.session` files** — Full Telegram account access
3. **Use dedicated account** — Avoid ban on main account
4. **Respect rate limits** — Configure conservative delays
5. **Review before contact** — AI isn't perfect

---

## 📈 Performance

### Benchmarks (1000 msgs/chat, 10 chats)

| Metric | Value |
|--------|-------|
| Total scrape time | ~15-20 min |
| AI analysis (100 users) | ~7 min |
| Leads found | 60-85% |
| API cost | ~$0.05-0.10 |

### Optimization Tips

- Use `--keywords-only` for 3x faster analysis
- Increase `MESSAGES_PER_CHAT` for deeper insights
- Run during off-peak hours (less FloodWait)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with 🔥 by the Aura Team**

*Finding leads so you don't have to.*

</div>
