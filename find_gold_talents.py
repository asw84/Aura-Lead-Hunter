import csv
from pathlib import Path

DATA_DIR = Path(r"d:\Aura Lead Hunter\data")
OUTPUT_FILE = DATA_DIR / "GOLDEN_RECRUIT_LIST.md"

def find_real_talent():
    talents = []
    csv_files = list(DATA_DIR.glob("*.csv"))
    
    unique_users = {}

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uid = row.get('user_id', '')
                    if not uid: continue
                    
                    try:
                        score = int(row.get('score', 0))
                        uid_int = int(uid)
                        category = row.get('category', '').lower()
                        
                        # FILTERS:
                        # 1. High Score
                        # 2. Real Account (Under 6B ID)
                        # 3. Proper category
                        if score >= 8 and uid_int < 6000000000 and category in ['traffic_buyer', 'marketing_pro']:
                            
                            summary = row.get('ai_summary_ru', row.get('ai_summary_en', ''))
                            handle = row.get('telegram_handle', f"ID:{uid}")
                            
                            # Anti-Scam filter (no "millions" in summary)
                            if "million" in summary.lower() or "unlimited" in summary.lower():
                                continue

                            unique_users[handle] = {
                                'handle': handle,
                                'score': score,
                                'summary': summary,
                                'id': uid,
                                'chat': row.get('source_chat', '')
                            }
                    except: continue
        except: continue

    # Save to Markdown
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🏆 Aura AI: Golden Talent List (Verified Media Buyers)\n")
        f.write("Only users with High Score + High Account Age (Verified via ID Series).\n\n")
        f.write("| Score | Contact | Experience Summary | Source Chat |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        sorted_talents = sorted(unique_users.values(), key=lambda x: x['score'], reverse=True)
        for t in sorted_talents:
            f.write(f"| {t['score']}/10 | **{t['handle']}** | {t['summary']} | {t['chat']} |\n")

    print(f"Done! Found {len(sorted_talents)} high-quality, low-risk candidates.")
    print(f"List saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    find_real_talent()
