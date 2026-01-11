import csv
import os
from pathlib import Path

# --- CONFIGURATION ---
DATA_DIR = Path(r"d:\Aura Lead Hunter\data")
WHALES_FILE = DATA_DIR / "GAMBLING_KEWAL_WHALES.txt"
OUTPUT_FILE = DATA_DIR / "WHALES_WITH_USERNAMES.md"

def match_usernames():
    # 1. Read the IDs we found
    whale_ids = {}
    if not WHALES_FILE.exists():
        print("Whales file not found.")
        return

    with open(WHALES_FILE, 'r', encoding='utf-8') as f:
        current_id = None
        for line in f:
            if line.startswith("["):
                # Extract ID from [Score/10] ID:12345
                parts = line.split("ID:")
                if len(parts) > 1:
                    current_id = parts[1].strip()
                    whale_ids[current_id] = {"id": current_id, "score": line.split("]")[0][1:]}
            elif current_id and "Summary:" in line:
                whale_ids[current_id]["summary"] = line.split("Summary:")[1].strip()

    # 2. Scan CSVs for usernames
    csv_files = list(DATA_DIR.glob("*.csv"))
    found_contacts = {}

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uid = row.get('user_id', '')
                    if uid in whale_ids:
                        handle = row.get('telegram_handle', '')
                        display_name = row.get('display_name', '')
                        if handle and handle.startswith('@'):
                            found_contacts[uid] = {
                                'handle': handle,
                                'name': display_name,
                                'score': whale_ids[uid]['score'],
                                'summary': whale_ids[uid]['summary']
                            }
        except:
            continue

    # 3. Generate Markdown Report
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🐳 High-Priority Gambling & India Whales (with Usernames)\n\n")
        f.write("| Score | Contact | Name | Summary |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        # Sort by score
        sorted_contacts = sorted(found_contacts.values(), key=lambda x: int(x['score'].split('/')[0]), reverse=True)
        
        for c in sorted_contacts:
            f.write(f"| {c['score']} | **{c['handle']}** | {c['name']} | {c['summary']} |\n")

    print(f"Done! Matched {len(found_contacts)} contacts with usernames.")
    print(f"Final list saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    match_usernames()
