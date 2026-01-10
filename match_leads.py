"""
Aura Lead Hunter - AI Matching Engine
======================================
Сопоставляет работодателей и байеров по:
- Вертикаль (Dating, Crypto, Gambling, Nutra)
- ГЕО (Tier 1, Tier 2, Asian, EU)
- Опыт и специфика трафика

Генерирует персонализированные сообщения для обеих сторон.

Usage:
    py match_leads.py
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Employer:
    """Работодатель/Тимлид."""
    contact: str
    score: int
    category: str
    reason: str
    language: str  # 🇷🇺 RU / 🇺🇦 UA
    vertical: str  # Dating, Crypto, Gambling, General
    geo: List[str] = field(default_factory=list)
    conditions: str = ""  # 70%, фикс, ставка


@dataclass 
class Buyer:
    """Байер/Трафик покупатель."""
    contact: str
    user_id: int
    display_name: str
    score: int
    category: str
    reason_en: str
    reason_ru: str
    bio: str
    source_chat: str
    vertical: str = "General"
    geo: List[str] = field(default_factory=list)
    traffic_type: str = ""  # FB, TT, Google
    volume: str = ""  # 2M daily, etc.


@dataclass
class Match:
    """Мэтч между работодателем и байером."""
    employer: Employer
    buyer: Buyer
    match_score: int  # 1-100
    match_reason: str
    message_to_employer: str
    message_to_buyer: str


def detect_vertical(text: str) -> str:
    """Определить вертикаль по тексту."""
    text_lower = text.lower()
    
    if any(kw in text_lower for kw in ['dating', 'дейтинг', 'знакомств', 'date']):
        return 'Dating'
    elif any(kw in text_lower for kw in ['crypto', 'крипто', 'web3', 'nft', 'defi', 'ton', 'bitcoin']):
        return 'Crypto'
    elif any(kw in text_lower for kw in ['gambling', 'гембл', 'casino', 'казино', 'igaming', 'betting', 'ggbet', 'slots']):
        return 'Gambling'
    elif any(kw in text_lower for kw in ['nutra', 'нутра', 'health', 'здоров', 'weight', 'diet']):
        return 'Nutra'
    elif any(kw in text_lower for kw in ['forex', 'trading', 'трейдинг', 'cfd']):
        return 'Forex'
    elif any(kw in text_lower for kw in ['gaming', 'game', 'cpi', 'mobile']):
        return 'Gaming'
    else:
        return 'General'


def detect_geo(text: str) -> List[str]:
    """Определить GEO по тексту."""
    text_lower = text.lower()
    geos = []
    
    # Tier 1
    if any(kw in text_lower for kw in ['tier 1', 'tier1', 'usa', 'uk', 'canada', 'australia', 'германия', 'germany', 'france']):
        geos.append('Tier1')
    
    # Tier 2
    if any(kw in text_lower for kw in ['tier 2', 'tier2', 'brazil', 'brasil', 'mexico', 'poland', 'spain', 'italy']):
        geos.append('Tier2')
    
    # Asian
    if any(kw in text_lower for kw in ['asian', 'asia', 'india', 'indian', 'indonesia', 'vietnam', 'thailand', 'азия', 'индия', 'индонезия']):
        geos.append('Asia')
    
    # CIS/RU
    if any(kw in text_lower for kw in ['cis', 'russia', 'russian', 'снг', 'россия', 'ukraine', 'ua', 'казахстан', 'belarus']):
        geos.append('CIS')
    
    # Latam
    if any(kw in text_lower for kw in ['latam', 'latin', 'brazil', 'argentina', 'chile', 'peru', 'colombia']):
        geos.append('Latam')
    
    return geos if geos else ['Worldwide']


def detect_traffic_type(text: str) -> str:
    """Определить тип трафика."""
    text_lower = text.lower()
    types = []
    
    if any(kw in text_lower for kw in ['fb', 'facebook', 'meta']):
        types.append('FB')
    if any(kw in text_lower for kw in ['tt', 'tiktok', 'tik tok']):
        types.append('TT')
    if any(kw in text_lower for kw in ['google', 'uac', 'adwords']):
        types.append('Google')
    if any(kw in text_lower for kw in ['push', 'native', 'pop']):
        types.append('Push/Pop')
    if any(kw in text_lower for kw in ['seo', 'organic']):
        types.append('SEO')
    if any(kw in text_lower for kw in ['email', 'smtp']):
        types.append('Email')
    
    return '/'.join(types) if types else 'Mixed'


def detect_volume(text: str) -> str:
    """Определить объём трафика."""
    # Ищем паттерны типа 2M, 50k, 30-50 FD
    patterns = [
        r'(\d+[MmKk]+)\s*(daily|в день|traffic|трафик)?',
        r'(\d+-\d+)\s*(fd|фд|депозит|leads|лидов)',
        r'(\d+)\s*(leads|лидов|конверт|conversions)\s*(daily|в день)?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return ""


def detect_conditions(text: str) -> str:
    """Определить условия работодателя."""
    conditions = []
    
    # Процент
    pct_match = re.search(r'(\d+)\s*%', text)
    if pct_match:
        conditions.append(f"{pct_match.group(1)}%")
    
    # Фикс/ставка
    if any(kw in text.lower() for kw in ['фикс', 'fix', 'ставка', 'rate', 'salary']):
        conditions.append("Фикс")
    
    # Бонусы
    if any(kw in text.lower() for kw in ['бонус', 'bonus', 'премия', 'prize']):
        conditions.append("Бонусы")
    
    # Отпуск
    if any(kw in text.lower() for kw in ['отпуск', 'vacation', 'відпустка']):
        conditions.append("Отпуск")
    
    return ", ".join(conditions) if conditions else "Стандартные"


def parse_employers(filepath: Path) -> List[Employer]:
    """Парсинг файла работодателей."""
    employers = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Новый формат: # @contact | 9/10 | 🇺🇦 UA | category | reason
    pattern = r'#\s*(@\S+|ID:\d+)\s*\|\s*(\d+)/10\s*\|\s*(🇺🇦 UA|🇷🇺 RU)\s*\|\s*(\S+)\s*\|\s*(.+)'
    matches = re.findall(pattern, content)
    
    # Fallback: старый формат без языка
    if not matches:
        pattern = r'#\s*(@\S+|ID:\d+)\s*\|\s*(\d+)/10\s*\|\s*(\S+)\s*\|\s*(.+)'
        old_matches = re.findall(pattern, content)
        for match in old_matches:
            contact, score, category, reason = match
            # Определяем язык по символам
            ua_chars = set('іїєґ')
            language = '🇺🇦 UA' if any(c in reason.lower() for c in ua_chars) else '🇷🇺 RU'
            
            employer = Employer(
                contact=contact.strip(),
                score=int(score),
                category=category.strip(),
                reason=reason.strip(),
                language=language,
                vertical=detect_vertical(reason),
                geo=detect_geo(reason),
                conditions=detect_conditions(reason)
            )
            employers.append(employer)
        return employers
    
    for match in matches:
        contact, score, language, category, reason = match
        
        employer = Employer(
            contact=contact.strip(),
            score=int(score),
            category=category.strip(),
            reason=reason.strip(),
            language=language.strip(),
            vertical=detect_vertical(reason),
            geo=detect_geo(reason),
            conditions=detect_conditions(reason)
        )
        employers.append(employer)
    
    return employers


def parse_buyers(filepath: Path) -> List[Buyer]:
    """Парсинг CSV с байерами."""
    buyers = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                score = int(row.get('score', 0))
                if score < 6:  # Только score 6+
                    continue
                
                category = row.get('category', '')
                if category not in ['traffic_buyer', 'marketing_pro', 'influencer']:
                    continue  # Только реальные байеры
                
                full_text = f"{row.get('ai_summary_en', '')} {row.get('ai_summary_ru', '')} {row.get('message_preview', '')} {row.get('bio', '')}"
                
                buyer = Buyer(
                    contact=row.get('telegram_handle', f"ID:{row.get('user_id', '')}"),
                    user_id=int(row.get('user_id', 0)),
                    display_name=row.get('display_name', ''),
                    score=score,
                    category=category,
                    reason_en=row.get('ai_summary_en', ''),
                    reason_ru=row.get('ai_summary_ru', ''),
                    bio=row.get('bio', ''),
                    source_chat=row.get('source_chat', ''),
                    vertical=detect_vertical(full_text),
                    geo=detect_geo(full_text),
                    traffic_type=detect_traffic_type(full_text),
                    volume=detect_volume(full_text)
                )
                buyers.append(buyer)
                
            except Exception as e:
                continue
    
    return buyers


def calculate_match_score(employer: Employer, buyer: Buyer) -> int:
    """Рассчитать score совпадения."""
    score = 0
    
    # Совпадение вертикали (40 баллов)
    if employer.vertical == buyer.vertical:
        score += 40
    elif employer.vertical == 'General' or buyer.vertical == 'General':
        score += 20  # Частичное совпадение
    
    # Совпадение GEO (30 баллов)
    geo_overlap = set(employer.geo) & set(buyer.geo)
    if geo_overlap:
        score += 30
    elif 'Worldwide' in employer.geo or 'Worldwide' in buyer.geo:
        score += 15
    
    # Языковое совпадение (20 баллов)
    if employer.language == '🇺🇦 UA' and any(kw in buyer.reason_ru.lower() for kw in ['укр', 'ua', 'шукає']):
        score += 20
    elif employer.language == '🇷🇺 RU':
        score += 20  # RU универсальный
    else:
        score += 10
    
    # Score байера (10 баллов)
    score += min(10, buyer.score)
    
    return min(100, score)


def generate_match_messages(employer: Employer, buyer: Buyer) -> tuple:
    """Генерировать сообщения для мэтча."""
    
    # Сообщение для работодателя
    buyer_info = []
    if buyer.traffic_type:
        buyer_info.append(f"льёт {buyer.traffic_type}")
    if buyer.volume:
        buyer_info.append(f"объём {buyer.volume}")
    if buyer.vertical != 'General':
        buyer_info.append(f"опыт в {buyer.vertical}")
    if buyer.geo and buyer.geo[0] != 'Worldwide':
        buyer_info.append(f"GEO: {', '.join(buyer.geo)}")
    
    buyer_desc = ", ".join(buyer_info) if buyer_info else "активный байер с опытом"
    
    msg_employer = f"""Привет! 👋

Увидел, что ищете байера. У меня есть кандидат под ваш запрос:

📌 {buyer.display_name or buyer.contact}
• {buyer_desc}
• Score: {buyer.score}/10
• Описание: {buyer.reason_ru[:100]}

Контакт: {buyer.contact}

Могу организовать связь, если интересно. 🤝"""

    # Сообщение для байера
    conditions_text = employer.conditions if employer.conditions != "Стандартные" else "хорошие условия"
    
    msg_buyer = f"""Привет! 👋

Нашёл тимлида под твой профиль:

📌 {employer.contact}
• Категория: {employer.category}
• Условия: {conditions_text}
• {employer.language}

Описание: {employer.reason[:100]}

Если интересно — могу дать контакт. 🚀"""

    return msg_employer, msg_buyer


def find_matches(employers: List[Employer], buyers: List[Buyer], min_score: int = 50) -> List[Match]:
    """Найти все совпадения."""
    matches = []
    
    for employer in employers:
        employer_matches = []
        
        for buyer in buyers:
            match_score = calculate_match_score(employer, buyer)
            
            if match_score >= min_score:
                msg_emp, msg_buy = generate_match_messages(employer, buyer)
                
                match = Match(
                    employer=employer,
                    buyer=buyer,
                    match_score=match_score,
                    match_reason=f"Vertical: {employer.vertical}↔{buyer.vertical}, GEO overlap",
                    message_to_employer=msg_emp,
                    message_to_buyer=msg_buy
                )
                employer_matches.append(match)
        
        # Сортируем по score и берём топ-3 для каждого работодателя
        employer_matches.sort(key=lambda x: x.match_score, reverse=True)
        matches.extend(employer_matches[:3])
    
    return matches


def main():
    print("🔄 Aura Lead Hunter - AI Matching Engine")
    print("=" * 50)
    
    data_dir = Path('data')
    
    # Ищем файлы
    employer_files = list(data_dir.glob('ALL_EMPLOYERS_*.txt'))
    buyer_files = [f for f in data_dir.glob('leads_*.csv') if 'export' not in f.name]
    
    if not employer_files:
        print("❌ No employer files found!")
        return
    
    if not buyer_files:
        # Fallback to leads_export
        buyer_files = list(data_dir.glob('leads_export.csv'))
        if not buyer_files:
            print("❌ No buyer CSV files found!")
            return
    
    # Берём последние файлы
    employer_file = sorted(employer_files)[-1]
    buyer_file = sorted(buyer_files)[-1]
    
    print(f"📂 Employers: {employer_file.name}")
    print(f"📂 Buyers: {buyer_file.name}")
    
    # Парсим данные
    employers = parse_employers(employer_file)
    buyers = parse_buyers(buyer_file)
    
    print(f"\n📊 Loaded: {len(employers)} employers, {len(buyers)} buyers")
    
    # Находим мэтчи
    matches = find_matches(employers, buyers, min_score=40)
    
    print(f"🎯 Found {len(matches)} matches")
    
    # Генерируем отчёт
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_dir / f"MATCHES_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# " + "=" * 60 + "\n")
        f.write("# 🎯 AURA LEAD HUNTER - AI MATCHING REPORT\n")
        f.write(f"# Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write(f"# Total matches: {len(matches)}\n")
        f.write("# " + "=" * 60 + "\n\n")
        
        # Уникальные работодатели с мэтчами
        unique_employers = {}
        for m in matches:
            if m.employer.contact not in unique_employers:
                unique_employers[m.employer.contact] = []
            unique_employers[m.employer.contact].append(m)
        
        f.write(f"# 📋 Summary: {len(unique_employers)} employers matched with buyers\n\n")
        
        # Детальные мэтчи по работодателям
        for emp_contact, emp_matches in unique_employers.items():
            f.write("\n" + "─" * 60 + "\n")
            emp = emp_matches[0].employer
            f.write(f"# 🏢 EMPLOYER: {emp_contact}\n")
            f.write(f"# Category: {emp.category} | {emp.language}\n")
            f.write(f"# Looking for: {emp.reason[:80]}\n")
            f.write(f"# Conditions: {emp.conditions}\n")
            f.write(f"# Matched buyers: {len(emp_matches)}\n")
            f.write("─" * 60 + "\n\n")
            
            for i, m in enumerate(emp_matches, 1):
                f.write(f"## Match #{i} — Score: {m.match_score}/100\n")
                f.write(f"## Buyer: {m.buyer.contact} ({m.buyer.display_name})\n")
                f.write(f"## Vertical: {m.buyer.vertical} | Traffic: {m.buyer.traffic_type}\n")
                f.write(f"## {m.buyer.reason_ru[:100]}\n\n")
                
                f.write("### 📤 MESSAGE TO EMPLOYER:\n")
                f.write("```\n")
                f.write(m.message_to_employer)
                f.write("\n```\n\n")
                
                f.write("### 📤 MESSAGE TO BUYER:\n")
                f.write("```\n")
                f.write(m.message_to_buyer)
                f.write("\n```\n\n")
        
        # Quick contacts section
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("# 📋 QUICK CONTACT PAIRS\n")
        f.write("=" * 60 + "\n\n")
        
        for emp_contact, emp_matches in unique_employers.items():
            f.write(f"🏢 {emp_contact} → ")
            buyer_contacts = [m.buyer.contact for m in emp_matches]
            f.write(", ".join(buyer_contacts) + "\n")
    
    print(f"\n✅ Report saved: {output_file}")
    
    # Показываем превью
    print("\n" + "=" * 50)
    print("📋 TOP MATCHES:")
    print("=" * 50)
    
    for i, (emp_contact, emp_matches) in enumerate(list(unique_employers.items())[:5], 1):
        emp = emp_matches[0].employer
        print(f"\n{i}. {emp_contact} ({emp.category})")
        print(f"   Looking for: {emp.reason[:50]}...")
        for m in emp_matches[:2]:
            print(f"   → {m.buyer.contact} (Score: {m.match_score}) - {m.buyer.vertical}")


if __name__ == "__main__":
    main()
