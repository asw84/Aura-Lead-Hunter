"""Regenerate HTML report with language toggle"""
import pandas as pd
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class LeadAnalysis:
    user_id: int
    username: Optional[str]
    display_name: Optional[str]
    is_lead: bool
    score: int
    category: str
    confidence: float
    reason: str
    bio: Optional[str] = None
    has_keywords: bool = False
    matched_keywords: List[str] = None
    source_chat: str = ""
    message_samples: List[str] = None
    analyzed_at: str = ""

# Import the updated generator
from storage.report_generator import generate_html_report

# Load leads from CSV
df = pd.read_csv('data/leads_20260110_112118.csv')

# Convert to LeadAnalysis objects
leads = []
for _, row in df.iterrows():
    username = None
    user_id = 0
    handle = str(row['telegram_handle'])
    if handle.startswith('@'):
        username = handle[1:]
    elif handle.startswith('ID:'):
        user_id = int(handle[3:])
    
    lead = LeadAnalysis(
        user_id=user_id or hash(handle),
        username=username,
        display_name=str(row.get('display_name', '')),
        is_lead=row['is_lead'],
        score=int(row['score']),
        category=str(row['category']),
        confidence=float(row['confidence']),
        reason=str(row['ai_summary']),
        bio=str(row.get('bio', '')) if pd.notna(row.get('bio')) else None,
        has_keywords=bool(row.get('has_keywords', False)),
        matched_keywords=str(row.get('matched_keywords', '')).split(', ') if pd.notna(row.get('matched_keywords')) else [],
        source_chat=str(row['source_chat']),
        message_samples=[str(row.get('message_preview', ''))] if pd.notna(row.get('message_preview')) else [],
        analyzed_at=str(row.get('analyzed_at', ''))
    )
    leads.append(lead)

# Generate report
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
report_path = generate_html_report(
    leads,
    f"data/report_{timestamp}.html",
    chats_processed=9,
    discovered_links=8
)

print(f"✅ New report with EN/RU toggle created: {report_path}")
print(f"🌐 Open in browser to test language switching!")
