"""
Aura Lead Hunter - Merge Employers Results
==========================================
Объединяет все найденных работодателей в один файл с фильтрами.

Usage:
    py merge_employers.py
"""

import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


def parse_employer_file(filepath: Path) -> list:
    """Parse employer hot/warm file and extract contacts."""
    employers = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_details = False
    for line in lines:
        line = line.strip()
        
        if line.startswith("# Details:"):
            in_details = True
            continue
        
        if in_details and line.startswith("#"):
            # Parse detail line: # @username | score | category | reason
            match = re.match(r'#\s*(@\S+|ID:\d+)\s*\|\s*(\d+)/10\s*\|\s*(\S+)\s*\|\s*(.+)', line)
            if match:
                contact = match.group(1)
                score = int(match.group(2))
                category = match.group(3).strip()
                reason = match.group(4).strip()
                
                employers.append({
                    'contact': contact,
                    'score': score,
                    'category': category,
                    'reason': reason,
                    'source_file': filepath.name
                })
    
    return employers


def detect_vertical(reason: str, category: str) -> str:
    """Detect vertical from reason text."""
    reason_lower = reason.lower()
    
    if any(kw in reason_lower for kw in ['dating', 'дейтинг', 'знакомств']):
        return 'Dating'
    elif any(kw in reason_lower for kw in ['crypto', 'крипто', 'web3', 'nft', 'defi']):
        return 'Crypto'
    elif any(kw in reason_lower for kw in ['gambling', 'гемблинг', 'casino', 'казино', 'igaming']):
        return 'Gambling'
    elif any(kw in reason_lower for kw in ['nutra', 'нутра', 'health', 'здоров']):
        return 'Nutra'
    elif any(kw in reason_lower for kw in ['forex', 'trading', 'трейдинг']):
        return 'Forex'
    elif any(kw in reason_lower for kw in ['схем', 'scheme', 'обработчик']):
        return 'Scheme'
    else:
        return 'General'


def detect_language(reason: str) -> str:
    """Detect language from reason text."""
    # Simple heuristic: Ukrainian has specific letters
    ua_chars = set('іїєґ')
    if any(c in reason.lower() for c in ua_chars):
        return '🇺🇦 UA'
    else:
        return '🇷🇺 RU'


def main():
    data_dir = Path('data')
    
    # Find all employer files
    hot_files = list(data_dir.glob('employers_hot_*.txt'))
    warm_files = list(data_dir.glob('employers_warm_*.txt'))
    
    print(f"📂 Found {len(hot_files)} hot files, {len(warm_files)} warm files")
    
    # Parse all files
    all_employers = []
    
    for f in hot_files:
        employers = parse_employer_file(f)
        for emp in employers:
            emp['tier'] = '🔥 HOT'
        all_employers.extend(employers)
        print(f"  ✅ {f.name}: {len(employers)} contacts")
    
    for f in warm_files:
        employers = parse_employer_file(f)
        for emp in employers:
            emp['tier'] = '🟡 WARM'
        all_employers.extend(employers)
        print(f"  ✅ {f.name}: {len(employers)} contacts")
    
    # Remove duplicates by contact
    seen = set()
    unique_employers = []
    for emp in all_employers:
        if emp['contact'] not in seen:
            seen.add(emp['contact'])
            emp['vertical'] = detect_vertical(emp['reason'], emp['category'])
            emp['language'] = detect_language(emp['reason'])
            unique_employers.append(emp)
    
    # Sort by score descending
    unique_employers.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n📊 Total unique employers: {len(unique_employers)}")
    
    # Group by vertical
    by_vertical = defaultdict(list)
    for emp in unique_employers:
        by_vertical[emp['vertical']].append(emp)
    
    # Group by language
    by_language = defaultdict(list)
    for emp in unique_employers:
        by_language[emp['language']].append(emp)
    
    # Generate combined file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_dir / f"ALL_EMPLOYERS_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# " + "=" * 60 + "\n")
        f.write("# 🏢 AURA LEAD HUNTER — ALL EMPLOYERS COMBINED\n")
        f.write(f"# Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write(f"# Total: {len(unique_employers)} unique contacts\n")
        f.write("# " + "=" * 60 + "\n\n")
        
        # Stats
        f.write("# 📊 STATISTICS:\n")
        f.write(f"#   🔥 Hot (7+): {len([e for e in unique_employers if e['score'] >= 7])}\n")
        f.write(f"#   🟡 Warm (5-6): {len([e for e in unique_employers if 5 <= e['score'] < 7])}\n")
        f.write("#\n")
        f.write("# 🌍 By Language:\n")
        for lang, emps in sorted(by_language.items()):
            f.write(f"#   {lang}: {len(emps)}\n")
        f.write("#\n")
        f.write("# 📁 By Vertical:\n")
        for vert, emps in sorted(by_vertical.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"#   {vert}: {len(emps)}\n")
        f.write("\n")
        
        # Section: All contacts for quick copy
        f.write("# " + "─" * 60 + "\n")
        f.write("# 📋 QUICK COPY (all contacts):\n")
        f.write("# " + "─" * 60 + "\n\n")
        for emp in unique_employers:
            f.write(f"{emp['contact']}\n")
        f.write("\n")
        
        # Section: By Vertical
        f.write("# " + "=" * 60 + "\n")
        f.write("# 📁 FILTER BY VERTICAL\n")
        f.write("# " + "=" * 60 + "\n\n")
        
        for vertical in ['Dating', 'Crypto', 'Gambling', 'Nutra', 'Forex', 'Scheme', 'General']:
            emps = by_vertical.get(vertical, [])
            if emps:
                f.write(f"\n# ━━━ {vertical.upper()} ({len(emps)}) ━━━\n")
                for emp in emps:
                    f.write(f"# {emp['contact']:25} | {emp['score']}/10 | {emp['language']} | {emp['category']:18} | {emp['reason'][:50]}\n")
        
        # Section: By Language
        f.write("\n\n# " + "=" * 60 + "\n")
        f.write("# 🌍 FILTER BY LANGUAGE\n")
        f.write("# " + "=" * 60 + "\n")
        
        for lang in ['🇺🇦 UA', '🇷🇺 RU']:
            emps = by_language.get(lang, [])
            if emps:
                f.write(f"\n# ━━━ {lang} ({len(emps)}) ━━━\n")
                for emp in emps:
                    f.write(f"{emp['contact']}\n")
        
        # Full details section
        f.write("\n\n# " + "=" * 60 + "\n")
        f.write("# 📝 FULL DETAILS\n")
        f.write("# " + "=" * 60 + "\n\n")
        
        for emp in unique_employers:
            f.write(f"# {emp['contact']}\n")
            f.write(f"#   Score: {emp['score']}/10 | {emp['tier']}\n")
            f.write(f"#   Category: {emp['category']}\n")
            f.write(f"#   Vertical: {emp['vertical']} | {emp['language']}\n")
            f.write(f"#   Reason: {emp['reason']}\n")
            f.write(f"#   Source: {emp['source_file']}\n")
            f.write("#\n")
    
    print(f"\n✅ Combined file saved: {output_file}")
    print(f"\n📊 Summary:")
    print(f"   Total contacts: {len(unique_employers)}")
    print(f"   By language: {dict([(k, len(v)) for k, v in by_language.items()])}")
    print(f"   By vertical: {dict([(k, len(v)) for k, v in by_vertical.items()])}")
    
    return output_file


if __name__ == "__main__":
    main()
