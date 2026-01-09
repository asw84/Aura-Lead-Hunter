"""
Aura Lead Hunter - CSV Exporter
================================
Export leads and analysis results to CSV files using Pandas.
"""

import asyncio
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import pandas as pd

from core.intent_analyzer import LeadAnalysis
from utils.logger import AuraLogger, ThoughtType


class CSVExporter:
    """Export leads to CSV with Pandas."""
    
    def __init__(self, export_dir: Path, logger: Optional[AuraLogger] = None):
        self.export_dir = export_dir
        self.logger = logger
        self.export_dir.mkdir(parents=True, exist_ok=True)
        
        self._log(ThoughtType.SYSTEM, "CSVExporter initialized", {
            "export_dir": str(export_dir)
        })
    
    def _log(self, thought_type: ThoughtType, action: str, details: dict = None) -> None:
        if self.logger:
            self.logger.thought(thought_type, "CSVExporter", action, details)
    
    def export_leads(
        self,
        leads: List[LeadAnalysis],
        filename: Optional[str] = None,
        include_non_leads: bool = False
    ) -> Path:
        """
        Export lead analysis results to CSV.
        
        Args:
            leads: List of LeadAnalysis objects
            filename: Optional filename, defaults to timestamped name
            include_non_leads: Whether to include users who are not leads
            
        Returns:
            Path to the exported CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"leads_{timestamp}.csv"
        
        filepath = self.export_dir / filename
        
        # Filter leads if needed
        if not include_non_leads:
            leads = [l for l in leads if l.is_lead]
        
        if not leads:
            self._log(ThoughtType.WARNING, "No leads to export")
            return filepath
        
        # Convert to DataFrame (Hunter 2.0 format)
        data = []
        for lead in leads:
            data.append({
                "telegram_handle": f"@{lead.username}" if lead.username else f"ID:{lead.user_id}",
                "user_id": lead.user_id,
                "display_name": lead.display_name or "",
                "is_lead": lead.is_lead,
                "score": lead.score,
                "category": lead.category,
                "confidence": lead.confidence,
                "ai_summary": lead.reason,
                "bio": lead.bio[:200] if lead.bio else "",
                "has_keywords": lead.has_keywords,
                "matched_keywords": ", ".join(lead.matched_keywords) if lead.matched_keywords else "",
                "source_chat": lead.source_chat,
                "message_preview": lead.message_samples[0][:100] if lead.message_samples else "",
                "analyzed_at": lead.analyzed_at
            })
        
        df = pd.DataFrame(data)
        
        # Sort by score (Hunter 2.0)
        df = df.sort_values("score", ascending=False)
        
        # Export to CSV
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        self._log(ThoughtType.EXPORT, f"Exported {len(df)} leads to CSV", {
            "filepath": str(filepath),
            "leads_count": len(df)
        })
        
        return filepath
    
    def export_all_users(
        self,
        leads: List[LeadAnalysis],
        filename: Optional[str] = None
    ) -> Path:
        """Export all analyzed users including non-leads."""
        return self.export_leads(leads, filename, include_non_leads=True)
