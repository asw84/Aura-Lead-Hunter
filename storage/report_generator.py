"""
Aura Lead Hunter - HTML Report Generator
==========================================
Generates beautiful HTML reports from lead analysis results.
Supports EN/RU language switching.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from core.intent_analyzer import LeadAnalysis


def generate_html_report(
    leads: List[LeadAnalysis],
    output_path: str = "data/report.html",
    chats_processed: int = 0,
    discovered_links: int = 0
) -> str:
    """
    Generate a beautiful HTML report from lead analysis results.
    Includes EN/RU language toggle.
    
    Returns:
        Path to generated HTML file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Stats
    total = len(leads)
    positive = [l for l in leads if l.is_lead and l.score >= 5]
    
    # Category breakdown
    categories = {}
    for lead in leads:
        cat = lead.category
        categories[cat] = categories.get(cat, 0) + 1
    
    # Sort leads by score
    sorted_leads = sorted(leads, key=lambda x: x.score, reverse=True)
    hot_leads = [l for l in sorted_leads if l.score >= 7]
    warm_leads = [l for l in sorted_leads if 5 <= l.score < 7]
    cold_leads = [l for l in sorted_leads if l.score < 5]
    
    # Category icons
    cat_icons = {
        'traffic_buyer': '💰',
        'advertiser': '📢',
        'influencer': '⭐',
        'community_owner': '👑',
        'marketing_pro': '🎯',
        'potential': '🔮',
        'not_lead': '❌'
    }
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Aura Lead Hunter Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #e4e4e4;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .lang-toggle {{
            position: fixed;
            top: 20px;
            left: 20px;
            display: flex;
            gap: 5px;
            z-index: 1001;
        }}
        
        .lang-btn {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: #888;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .lang-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        .lang-btn.active {{
            background: linear-gradient(45deg, #7b2cbf, #00d4ff);
            color: white;
            border-color: transparent;
        }}
        
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #888;
            font-size: 1.1rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .stat-card .number {{
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stat-card .label {{
            color: #888;
            margin-top: 5px;
        }}
        
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }}
        
        .section h2 {{
            margin-bottom: 20px;
            color: #00d4ff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .lead-card {{
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid;
            transition: transform 0.2s;
        }}
        
        .lead-card:hover {{
            transform: translateX(5px);
        }}
        
        .lead-card.hot {{
            border-left-color: #ff4757;
        }}
        
        .lead-card.warm {{
            border-left-color: #ffa502;
        }}
        
        .lead-card.cold {{
            border-left-color: #747d8c;
        }}
        
        .lead-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .lead-handle {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #00d4ff;
        }}
        
        .lead-score {{
            background: linear-gradient(45deg, #7b2cbf, #00d4ff);
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}
        
        .lead-category {{
            display: inline-block;
            background: rgba(123, 44, 191, 0.3);
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.85rem;
            margin-right: 10px;
        }}
        
        .lead-summary {{
            color: #ccc;
            margin-top: 10px;
            font-style: italic;
        }}
        
        .lead-keywords {{
            margin-top: 10px;
        }}
        
        .keyword {{
            display: inline-block;
            background: rgba(0, 212, 255, 0.2);
            color: #00d4ff;
            padding: 2px 8px;
            border-radius: 5px;
            font-size: 0.8rem;
            margin-right: 5px;
            margin-top: 5px;
        }}
        
        .lead-source {{
            color: #666;
            font-size: 0.85rem;
            margin-top: 10px;
        }}
        
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .category-item {{
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .category-item .cat-count {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #00d4ff;
        }}
        
        .category-item .cat-name {{
            color: #888;
            font-size: 0.9rem;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
        }}
        
        .tg-link {{
            color: #00d4ff;
            text-decoration: none;
        }}
        
        .tg-link:hover {{
            text-decoration: underline;
        }}
        
        .pdf-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #7b2cbf, #00d4ff);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            z-index: 1000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }}
        
        .pdf-btn:hover {{
            transform: scale(1.05);
        }}
        
        /* Hide elements based on language */
        [data-lang-ru] {{ display: none; }}
        [data-lang-en] {{ display: inline; }}
        
        body.lang-ru [data-lang-ru] {{ display: inline; }}
        body.lang-ru [data-lang-en] {{ display: none; }}
        
        @media print {{
            body {{
                background: white !important;
                color: black !important;
                padding: 10px !important;
            }}
            
            .pdf-btn, .lang-toggle {{
                display: none !important;
            }}
            
            .container {{
                max-width: 100% !important;
            }}
            
            .header {{
                background: #f5f5f5 !important;
                color: black !important;
            }}
            
            .header h1 {{
                background: none !important;
                -webkit-text-fill-color: #7b2cbf !important;
            }}
            
            .stat-card {{
                background: #f5f5f5 !important;
                border: 1px solid #ddd !important;
            }}
            
            .stat-card .number {{
                background: none !important;
                -webkit-text-fill-color: #7b2cbf !important;
            }}
            
            .section {{
                background: #f5f5f5 !important;
                border: 1px solid #ddd !important;
            }}
            
            .section h2 {{
                color: #7b2cbf !important;
            }}
            
            .lead-card {{
                background: white !important;
                border: 1px solid #ddd !important;
                page-break-inside: avoid;
            }}
            
            .lead-handle {{
                color: #7b2cbf !important;
            }}
            
            .lead-summary {{
                color: #333 !important;
            }}
            
            .lead-source {{
                color: #666 !important;
            }}
            
            .category-item {{
                background: #f5f5f5 !important;
            }}
            
            .category-item .cat-count {{
                color: #7b2cbf !important;
            }}
        }}
    </style>
</head>
<body>
    <!-- Language Toggle -->
    <div class="lang-toggle">
        <button class="lang-btn active" onclick="setLang('en')" id="btn-en">EN</button>
        <button class="lang-btn" onclick="setLang('ru')" id="btn-ru">RU</button>
    </div>
    
    <button class="pdf-btn" onclick="window.print()">
        <span data-lang-en>📄 Save PDF</span>
        <span data-lang-ru>📄 Сохранить PDF</span>
    </button>
    
    <div class="container">
        <div class="header">
            <h1>🎯 AURA LEAD HUNTER</h1>
            <p class="subtitle">
                <span data-lang-en>Report generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}</span>
                <span data-lang-ru>Отчёт от {datetime.now().strftime('%d.%m.%Y %H:%M')}</span>
            </p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{chats_processed}</div>
                <div class="label">
                    <span data-lang-en>Chats Processed</span>
                    <span data-lang-ru>Чатов обработано</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="number">{total}</div>
                <div class="label">
                    <span data-lang-en>Users Analyzed</span>
                    <span data-lang-ru>Пользователей</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="number">{len(positive)}</div>
                <div class="label">
                    <span data-lang-en>Leads Found</span>
                    <span data-lang-ru>Лидов найдено</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="number">{len(hot_leads)}</div>
                <div class="label">
                    <span data-lang-en>🔥 Hot Leads</span>
                    <span data-lang-ru>🔥 Горячих</span>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>
                <span data-lang-en>📊 Categories</span>
                <span data-lang-ru>📊 Категории</span>
            </h2>
            <div class="category-grid">
"""
    
    # Category items
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        icon = cat_icons.get(cat, '📌')
        html += f"""
                <div class="category-item">
                    <div class="cat-count">{count}</div>
                    <div class="cat-name">{icon} {cat}</div>
                </div>
"""
    
    html += """
            </div>
        </div>
"""
    
    # Hot leads section
    if hot_leads:
        html += """
        <div class="section">
            <h2>
                <span data-lang-en>🔥 Hot Leads (Score 7-10)</span>
                <span data-lang-ru>🔥 Горячие лиды (Score 7-10)</span>
            </h2>
"""
        for lead in hot_leads[:20]:
            handle = f"@{lead.username}" if lead.username else f"ID:{lead.user_id}"
            tg_link = f"https://t.me/{lead.username}" if lead.username else "#"
            keywords_html = "".join([f'<span class="keyword">{k}</span>' for k in (lead.matched_keywords or [])[:5]])
            icon = cat_icons.get(lead.category, '')
            
            # Get bilingual reasons
            reason_en = getattr(lead, 'reason_en', lead.reason) or lead.reason
            reason_ru = getattr(lead, 'reason_ru', lead.reason) or lead.reason
            
            html += f"""
            <div class="lead-card hot">
                <div class="lead-header">
                    <a href="{tg_link}" target="_blank" class="lead-handle tg-link">{handle}</a>
                    <span class="lead-score">{lead.score}/10</span>
                </div>
                <span class="lead-category">{icon} {lead.category}</span>
                <span style="color:#888">{lead.display_name or ''}</span>
                <p class="lead-summary">
                    <span data-lang-en>"{reason_en}"</span>
                    <span data-lang-ru>"{reason_ru}"</span>
                </p>
                <div class="lead-keywords">{keywords_html}</div>
                <p class="lead-source">📍 {lead.source_chat}</p>
            </div>
"""
        html += "        </div>\n"
    
    # Warm leads section
    if warm_leads:
        html += """
        <div class="section">
            <h2>
                <span data-lang-en>🟡 Warm Leads (Score 5-6)</span>
                <span data-lang-ru>🟡 Тёплые лиды (Score 5-6)</span>
            </h2>
"""
        for lead in warm_leads[:30]:
            handle = f"@{lead.username}" if lead.username else f"ID:{lead.user_id}"
            tg_link = f"https://t.me/{lead.username}" if lead.username else "#"
            keywords_html = "".join([f'<span class="keyword">{k}</span>' for k in (lead.matched_keywords or [])[:3]])
            
            # Get bilingual reasons
            reason_en = getattr(lead, 'reason_en', lead.reason) or lead.reason
            reason_ru = getattr(lead, 'reason_ru', lead.reason) or lead.reason
            
            html += f"""
            <div class="lead-card warm">
                <div class="lead-header">
                    <a href="{tg_link}" target="_blank" class="lead-handle tg-link">{handle}</a>
                    <span class="lead-score">{lead.score}/10</span>
                </div>
                <span class="lead-category">{lead.category}</span>
                <p class="lead-summary">
                    <span data-lang-en>"{reason_en}"</span>
                    <span data-lang-ru>"{reason_ru}"</span>
                </p>
                <div class="lead-keywords">{keywords_html}</div>
                <p class="lead-source">📍 {lead.source_chat}</p>
            </div>
"""
        html += "        </div>\n"
    
    # Footer and JavaScript
    html += f"""
        <div class="footer">
            <p>
                <span data-lang-en>Generated by Aura Lead Hunter 2.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                <span data-lang-ru>Создано Aura Lead Hunter 2.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </p>
        </div>
    </div>
    
    <script>
        function setLang(lang) {{
            const body = document.body;
            const btnEn = document.getElementById('btn-en');
            const btnRu = document.getElementById('btn-ru');
            
            if (lang === 'ru') {{
                body.classList.add('lang-ru');
                btnRu.classList.add('active');
                btnEn.classList.remove('active');
            }} else {{
                body.classList.remove('lang-ru');
                btnEn.classList.add('active');
                btnRu.classList.remove('active');
            }}
            
            // Save preference
            localStorage.setItem('aura_lang', lang);
        }}
        
        // Load saved language preference
        document.addEventListener('DOMContentLoaded', function() {{
            const savedLang = localStorage.getItem('aura_lang') || 'en';
            setLang(savedLang);
        }});
    </script>
</body>
</html>
"""
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_path)
