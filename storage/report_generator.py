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
    Includes interactive charts and EN/RU language toggle.
    
    Returns:
        Path to generated HTML file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Stats
    total = len(leads)
    positive = [l for l in leads if l.is_lead and l.score >= 5]
    
    # Analytics data
    category_counts = {}
    score_counts = {i: 0 for i in range(1, 11)}
    source_counts = {}
    
    for lead in leads:
        # Category
        cat = lead.category or "potential"
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Score
        if 1 <= lead.score <= 10:
            score_counts[lead.score] += 1
            
        # Source
        src = lead.source_chat or "Unknown"
        source_counts[src] = source_counts.get(src, 0) + 1
    
    # Sort source counts for top 10
    top_sources = dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    # Sort leads by score
    sorted_leads = sorted(leads, key=lambda x: x.score, reverse=True)
    hot_leads = [l for l in sorted_leads if l.score >= 7]
    warm_leads = [l for l in sorted_leads if 5 <= l.score < 7]
    
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
    
    # Chart colors
    chart_colors = [
        '#00d4ff', '#7b2cbf', '#ff00c8', '#00ff88', '#ff8c00', 
        '#ff4757', '#ffa502', '#2ed573', '#1e90ff', '#ffffff'
    ]
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Aura Lead Hunter Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        
        body {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #0f172a; /* Solid dark background for web */
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            color: #f1f5f9;
            padding: 20px;
            scroll-behavior: smooth;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        
        /* Language Toggle */
        .lang-toggle {{
            position: fixed;
            top: 20px;
            left: 20px;
            display: flex;
            gap: 5px;
            z-index: 1001;
        }}
        
        .lang-btn {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #aaa;
            padding: 10px 18px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 800;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}
        
        .lang-btn.active {{
            background: linear-gradient(45deg, #7b2cbf, #00d4ff);
            color: white;
            border-color: transparent;
        }}
        
        /* Action Buttons */
        .pdf-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: bold;
            z-index: 1000;
            box-shadow: 0 8px 25px rgba(0, 212, 255, 0.2);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .pdf-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
        }}

        /* Header */
        .header {{
            text-align: center;
            padding: 50px 20px;
            background: rgba(255,255,255,0.03);
            border-radius: 24px;
            margin-bottom: 30px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(to right, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #94a3b8;
            font-size: 1.1rem;
            font-weight: 500;
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.04);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        
        .stat-card .number {{
            font-size: 2.5rem;
            font-weight: 800;
            color: #00d4ff;
            line-height: 1.2;
        }}
        
        .stat-card .label {{
            color: #94a3b8;
            margin-top: 5px;
            text-transform: uppercase;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 1px;
        }}
        
        /* Analytics */
        .analytics-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .chart-box {{
            background: rgba(255,255,255,0.03);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.05);
            height: 320px;
        }}
        
        .chart-box h3 {{
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* Section */
        .section {{
            background: rgba(255,255,255,0.02);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.04);
        }}
        
        .section h2 {{
            margin-bottom: 20px;
            color: #00d4ff;
            font-size: 1.5rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        /* Lead Cards */
        .lead-card {{
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.02);
            border-left: 4px solid #444;
            break-inside: avoid;
        }}
        
        .lead-card.hot {{ border-left-color: #ff4757; }}
        .lead-card.warm {{ border-left-color: #ffa502; }}
        
        .lead-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .lead-handle {{
            font-size: 1.1rem;
            font-weight: 800;
            color: #00d4ff;
            text-decoration: none;
        }}
        
        .lead-score {{
            background: #7b2cbf;
            color: white;
            padding: 4px 12px;
            border-radius: 50px;
            font-weight: 800;
            font-size: 0.8rem;
        }}
        
        .lead-badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
        }}
        
        .badge {{
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        
        .badge-cat {{ background: rgba(123, 44, 191, 0.2); color: #c084fc; }}
        .badge-source {{ background: rgba(255,255,255,0.05); color: #94a3b8; }}
        
        .lead-summary {{
            color: #cbd5e1;
            margin: 12px 0;
            font-size: 0.95rem;
            line-height: 1.5;
            font-style: italic;
        }}
        
        .keyword {{
            display: inline-block;
            background: rgba(0, 212, 255, 0.1);
            color: #00d4ff;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            margin-right: 6px;
            margin-top: 6px;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #64748b;
            font-size: 0.85rem;
        }}
        
        /* Multilingual */
        [data-lang-ru] {{ display: none; }}
        [data-lang-en] {{ display: inline; }}
        body.lang-ru [data-lang-ru] {{ display: inline; }}
        body.lang-ru [data-lang-en] {{ display: none; }}
        
        /* PRINT FIXES - PURE PDF MAGIC */
        @media print {{
            @page {{
                margin: 1.5cm 1cm;
                size: A4;
            }}
            
            body {{
                background: white !important;
                color: #1e293b !important;
                padding: 0 !important;
            }}
            
            .container {{
                max-width: 100% !important;
                margin: 0 !important;
            }}
            
            .pdf-btn, .lang-toggle {{
                display: none !important;
            }}
            
            .header {{
                background: #f1f5f9 !important;
                border: 1px solid #e2e8f0 !important;
                padding: 30px !important;
                border-radius: 12px !important;
                margin-bottom: 20px !important;
            }}
            
            .header h1 {{
                background: none !important;
                -webkit-text-fill-color: #0f172a !important;
                color: #0f172a !important;
                font-size: 2.5rem !important;
            }}
            
            .stats-grid {{
                display: flex !important;
                justify-content: space-between !important;
                gap: 10px !important;
                grid-template-columns: none !important;
                margin-bottom: 20px !important;
            }}
            
            .stat-card {{
                flex: 1 !important;
                background: #f8fafc !important;
                border: 1px solid #e2e8f0 !important;
                padding: 15px !important;
            }}
            
            .stat-card .number {{
                color: #7b2cbf !important;
                font-size: 2rem !important;
            }}
            
            .stat-card .label {{
                color: #64748b !important;
            }}
            
            .analytics-grid {{
                display: grid !important;
                grid-template-columns: 1fr 1fr !important;
                gap: 15px !important;
                margin-bottom: 20px !important;
            }}
            
            .chart-box {{
                background: white !important;
                border: 1px solid #e2e8f0 !important;
                height: 280px !important;
                break-inside: avoid;
            }}
            
            .section {{
                padding: 0 !important;
                background: transparent !important;
                border: none !important;
            }}
            
            .section h2 {{
                color: #0f172a !important;
                border-bottom: 2px solid #e2e8f0 !important;
                padding-bottom: 8px !important;
                margin-top: 20px !important;
            }}
            
            .lead-card {{
                border: 1px solid #e2e8f0 !important;
                border-left-width: 6px !important;
                background: white !important;
                margin-bottom: 12px !important;
                padding: 15px !important;
            }}
            
            .lead-handle {{ color: #0f172a !important; }}
            .lead-summary {{ color: #334155 !important; }}
            
            .badge-source {{ background: #f1f5f9 !important; color: #475569 !important; }}
            .keyword {{ background: #f8fafc !important; color: #475569 !important; border: 1px solid #e2e8f0 !important; }}
            
            .footer {{ color: #94a3b8 !important; padding: 20px !important; }}
        }}
    </style>
</head>
<body>
    <div class="lang-toggle">
        <button class="lang-btn active" onclick="setLang('en')" id="btn-en">EN</button>
        <button class="lang-btn" onclick="setLang('ru')" id="btn-ru">RU</button>
    </div>
    
    <button class="pdf-btn" onclick="window.print()">
        <span>📄</span>
        <span data-lang-en>Save PDF Report</span>
        <span data-lang-ru>Сохранить PDF</span>
    </button>
    
    <div class="container">
        <div class="header">
            <h1>🎯 AURA LEAD HUNTER</h1>
            <p class="subtitle">
                <span data-lang-en>Deep Market Intelligence & Lead Discovery</span>
                <span data-lang-ru>Глубокая аналитика рынка и поиск лидов</span>
            </p>
            <p style="margin-top: 10px; opacity: 0.7; font-size: 0.85rem;">
                <span data-lang-en>Environment: Aura AI Hub | Pro Report</span>
                <span data-lang-ru>Окружение: Aura AI Hub | Pro Отчёт</span>
            </p>
            <p style="margin-top: 5px; opacity: 0.5; font-size: 0.8rem;">
                <span data-lang-en>Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}</span>
                <span data-lang-ru>Сформирован: {datetime.now().strftime('%d.%m.%Y %H:%M')}</span>
            </p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{chats_processed}</div>
                <div class="label">
                    <span data-lang-en>Channels</span>
                    <span data-lang-ru>Каналов</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="number">{total}</div>
                <div class="label">
                    <span data-lang-en>Analyzed</span>
                    <span data-lang-ru>Проверено</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="number">{len(positive)}</div>
                <div class="label">
                    <span data-lang-en>Leads Found</span>
                    <span data-lang-ru>Лидов</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="number">{len(hot_leads)}</div>
                <div class="label">
                    <span data-lang-en>Hot (7+)</span>
                    <span data-lang-ru>Горячих (7+)</span>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="analytics-grid">
            <div class="chart-box">
                <h3>📊 
                    <span data-lang-en>Categories</span>
                    <span data-lang-ru>Категории</span>
                </h3>
                <div style="height: 220px; position: relative;">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
            <div class="chart-box">
                <h3>📈 
                    <span data-lang-en>Score Distribution</span>
                    <span data-lang-ru>Распределение баллов</span>
                </h3>
                <div style="height: 220px; position: relative;">
                    <canvas id="scoreChart"></canvas>
                </div>
            </div>
            <div class="chart-box" style="grid-column: 1 / -1; height: 300px;">
                <h3>📍 
                    <span data-lang-en>Top Sources</span>
                    <span data-lang-ru>Топ источников</span>
                </h3>
                <div style="height: 230px; position: relative;">
                    <canvas id="sourceChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Hot Leads -->
        <div class="section">
            <h2>
                <span>🔥</span>
                <span data-lang-en>Priority Leads (Score 7-10)</span>
                <span data-lang-ru>Приоритетные лиды (Score 7-10)</span>
            </h2>
            <div class="leads-list">
"""
    
    for lead in hot_leads:
        handle = f"@{lead.username}" if lead.username else f"ID:{lead.user_id}"
        tg_link = f"https://t.me/{lead.username}" if lead.username else "#"
        keywords_html = "".join([f'<span class="keyword">{k}</span>' for k in (lead.matched_keywords or [])[:5]])
        icon = cat_icons.get(lead.category, '📌')
        
        reason_en = getattr(lead, 'reason_en', lead.reason) or lead.reason
        reason_ru = getattr(lead, 'reason_ru', lead.reason) or lead.reason
        
        html += f"""
                <div class="lead-card hot">
                    <div class="lead-header">
                        <a href="{tg_link}" target="_blank" class="lead-handle">{handle}</a>
                        <span class="lead-score">{lead.score}/10</span>
                    </div>
                    <div class="lead-badges">
                        <span class="badge badge-cat">{icon} {lead.category}</span>
                        <span class="badge badge-source">📍 {lead.source_chat}</span>
                    </div>
                    <p class="lead-summary">
                        <span data-lang-en>{reason_en}</span>
                        <span data-lang-ru>{reason_ru}</span>
                    </p>
                    <div class="lead-keywords">{keywords_html}</div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <!-- Warm Leads -->
        <div class="section">
            <h2>
                <span>🟡</span>
                <span data-lang-en>Interesting Leads (Score 5-6)</span>
                <span data-lang-ru>Заслуживают внимания (Score 5-6)</span>
            </h2>
            <div class="leads-list">
"""
    
    for lead in warm_leads:
        handle = f"@{lead.username}" if lead.username else f"ID:{lead.user_id}"
        tg_link = f"https://t.me/{lead.username}" if lead.username else "#"
        keywords_html = "".join([f'<span class="keyword">{k}</span>' for k in (lead.matched_keywords or [])[:3]])
        
        reason_en = getattr(lead, 'reason_en', lead.reason) or lead.reason
        reason_ru = getattr(lead, 'reason_ru', lead.reason) or lead.reason
        
        html += f"""
                <div class="lead-card warm">
                    <div class="lead-header">
                        <a href="{tg_link}" target="_blank" class="lead-handle">{handle}</a>
                        <span class="lead-score">{lead.score}/10</span>
                    </div>
                    <div class="lead-badges">
                        <span class="badge badge-cat">{icon} {lead.category}</span>
                        <span class="badge badge-source">📍 {lead.source_chat}</span>
                    </div>
                    <p class="lead-summary">
                        <span data-lang-en>{reason_en}</span>
                        <span data-lang-ru>{reason_ru}</span>
                    </p>
                    <div class="lead-keywords">{keywords_html}</div>
                </div>
"""
    
    # Passing data to JavaScript
    import json
    category_data_json = json.dumps(category_counts)
    score_data_json = json.dumps(score_counts)
    source_data_json = json.dumps(top_sources)
    
    html += f"""
            </div>
        </div>
        
        <div class="footer">
            <p>© {datetime.now().year} Aura Lead Hunter Pro | Confidential Affiliate Intelligence</p>
            <p style="margin-top: 5px; opacity: 0.5;">
                <span data-lang-en>Internal use only. Data processed by AURA AI Engine.</span>
                <span data-lang-ru>Только для внутреннего использования. Обработка Aura AI Engine.</span>
            </p>
        </div>
    </div>
    
    <script>
        // Data from Python
        const categoryData = {category_data_json};
        const scoreData = {score_data_json};
        const sourceData = {source_data_json};
        const colors = {json.dumps(chart_colors)};

        const legendColor = window.matchMedia('(prefers-color-scheme: dark)').matches ? '#94a3b8' : '#64748b';

        // Helper for Chart.js options
        const chartOptions = {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    position: 'bottom',
                    labels: {{ color: '#94a3b8', font: {{ weight: 'bold', size: 10 }} }}
                }},
                tooltip: {{
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    padding: 10,
                    cornerRadius: 8
                }}
            }},
            scales: {{
                y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#64748b', font: {{ size: 10 }} }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#64748b', font: {{ size: 10 }} }} }}
            }}
        }};

        // Category Chart
        new Chart(document.getElementById('categoryChart'), {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(categoryData),
                datasets: [{{
                    data: Object.values(categoryData),
                    backgroundColor: colors,
                    borderWidth: 0
                }}]
            }},
            options: {{
                ...chartOptions,
                cutout: '65%',
                plugins: {{ ...chartOptions.plugins, legend: {{ position: 'right' }} }}
            }}
        }});

        // Score Chart
        new Chart(document.getElementById('scoreChart'), {{
            type: 'bar',
            data: {{
                labels: Object.keys(scoreData),
                datasets: [{{
                    label: 'Leads',
                    data: Object.values(scoreData),
                    backgroundColor: 'rgba(0, 212, 255, 0.6)',
                    borderColor: '#00d4ff',
                    borderWidth: 1,
                    borderRadius: 4
                }}]
            }},
            options: chartOptions
        }});

        // Source Chart
        new Chart(document.getElementById('sourceChart'), {{
            type: 'bar',
            data: {{
                labels: Object.keys(sourceData),
                datasets: [{{
                    label: 'Leads',
                    data: Object.values(sourceData),
                    backgroundColor: 'rgba(123, 44, 191, 0.6)',
                    borderColor: '#7b2cbf',
                    borderWidth: 1,
                    borderRadius: 4
                }}]
            }},
            options: {{
                ...chartOptions,
                indexAxis: 'y',
                plugins: {{ ...chartOptions.plugins, legend: {{ display: false }} }}
            }}
        }});

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
            localStorage.setItem('aura_report_lang', lang);
        }}
        
        document.addEventListener('DOMContentLoaded', () => {{
            const saved = localStorage.getItem('aura_report_lang') || 'en';
            setLang(saved);
        }});
    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_path)
