import csv
import os
from pathlib import Path

# --- CONFIGURATION ---
DATA_DIR = Path(r"d:\Aura Lead Hunter\data")
OUTPUT_FILE = DATA_DIR / "GAMBLING_KEWAL_WHALES.txt"
SCORE_THRESHOLD = 8

# Keywords to hunt for
KEYWORDS = [
    "gambling", "гемблинг", "betting", "беттинг", "казино", "casino",
    "india", "индия", "asia", "азия", "pakistan", "пакистан",
    "daily", "ежедневно", "payout", "выплаты", "usdt",
    "mostbet", "1win", "pin-up", "pinup", "parimatch",
    "advertiser", "network", "owner", "ceo", "founder"
]

def find_whales():
    whales = []
    
    # Get all CSV files in data directory
    csv_files = list(DATA_DIR.glob("*.csv"))
    
    if not csv_files:
        print("No CSV files found in data directory.")
        return

    print(f"Scanning {len(csv_files)} files...")

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        score = int(row.get('score', 0))
                        if score < SCORE_THRESHOLD:
                            continue
                            
                        # Combine all searchable text
                        source_text = " ".join([
                            row.get('display_name', ''),
                            row.get('telegram_handle', ''),
                            row.get('ai_summary_en', ''),
                            row.get('ai_summary_ru', ''),
                            row.get('bio', ''),
                            row.get('message_preview', '')
                        ]).lower()
                        
                        # Check if any keyword matches
                        found_keywords = [kw for kw in KEYWORDS if kw in source_text]
                        
                        if found_keywords:
                            whales.append({
                                'contact': row.get('telegram_handle', f"ID:{row.get('user_id', '')}"),
                                'score': score,
                                'keywords': found_keywords,
                                'summary': row.get('ai_summary_ru', row.get('ai_summary_en', 'No summary')),
                                'source': csv_file.name
                            })
                    except:
                        continue
        except Exception as e:
            print(f"Error reading {csv_file.name}: {e}")

    # Remove duplicates by contact
    unique_whales = {w['contact']: w for w in whales}.values()
    sorted_whales = sorted(unique_whales, key=lambda x: x['score'], reverse=True)

    # Save report
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("🐳 AURA WHALE HUNTER: GAMBLING & INDIA SPECIALISTS\n")
        f.write("====================================================\n\n")
        
        for w in sorted_whales:
            f.write(f"[{w['score']}/10] {w['contact']}\n")
            f.write(f"Keywords: {', '.join(w['keywords'])}\n")
            f.write(f"Summary: {w['summary']}\n")
            f.write(f"Source: {w['source']}\n")
            f.write("-" * 50 + "\n")

    print(f"Done! Found {len(sorted_whales)} potential whale partners.")
    print(f"Report saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    find_whales()
