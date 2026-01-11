import csv
import re
from pathlib import Path

# --- CONFIGURATION ---
DATA_DIR = Path(r"d:\Aura Lead Hunter\data")
OUTPUT_FILE = DATA_DIR / "CANDIDATES_FOR_ABHI.md"

# India + Gambling/Trading Keywords
TARGET_KEYWORDS = [
    r"india", r"\bin\b", r"pakistan", r"bangladesh",
    r"gambling", r"igaming", r"casino", r"betting",
    r"traffic", r"traff", r"lead", r"cpa", r"cpl",
    r"trading", r"binary"
]

def find_candidates_for_abhi():
    candidates = []
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
                        msg = row.get('message_preview', '').lower()
                        summary = row.get('ai_summary_ru', row.get('ai_summary_en', '')).lower()
                        
                        # 1. Real account check (< 6B ID ~ pre-2023)
                        # Abhi is a big player, he needs stable partners
                        if uid_int >= 6000000000:
                            continue
                            
                        # 2. High Score check
                        if score < 7:
                            continue
                            
                        # 3. Content check (India + Gambling/Traffic/Trading)
                        full_context = f"{msg} {summary}"
                        
                        # Check for India/GEO focus
                        is_india = any(re.search(p, full_context) for p in [r"india", r"\bin\b", r"pakistan", r"bangladesh", r"asia"])
                        
                        # Check for Vertical/Action focus
                        is_relevant_vert = any(re.search(p, full_context) for p in [r"gambling", r"casino", r"bet", r"igaming", r"traffic", r"offer", r"trading", r"binary"])
                        
                        if is_india and is_relevant_vert:
                            handle = row.get('telegram_handle', f"ID:{uid}")
                            
                            if handle not in unique_users:
                                unique_users[handle] = {
                                    'handle': handle,
                                    'score': score,
                                    'id': uid,
                                    'summary': row.get('ai_summary_en', row.get('ai_summary_ru', '')),
                                    'message': row.get('message_preview', ''),
                                    'chat': row.get('source_chat', '')
                                }
                    except Exception:
                        continue
        except Exception:
            continue

    # Save to Markdown
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# 🇮🇳 Verified Candidates for Abhi (India Gambling/Trading)\n")
        f.write(f"Criteria: ID < 6B (Real Account), Score 7+, Context: India + Gambling/Traffic/Trading\n\n")
        f.write("| Score | Account Age | Handle | Summary | Message Preview |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        # Simple ID to Age mapping
        def get_age(uid):
            u = int(uid)
            if u < 1000000000: return "Pre-2019"
            if u < 5000000000: return "2020-2021"
            return "2022-2023"

        sorted_list = sorted(unique_users.values(), key=lambda x: x['score'], reverse=True)
        for c in sorted_list:
            age = get_age(c['id'])
            # Escaping pipe in message preview for markdown table
            cleaned_msg = c['message'].replace('|', '&#124;').replace('\n', ' ')
            f.write(f"| {c['score']}/10 | {age} | **{c['handle']}** | {c['summary']} | {cleaned_msg} |\n")

    print(f"Found {len(sorted_list)} verified India-centric candidates for Abhi.")
    print(f"List saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    find_candidates_for_abhi()
