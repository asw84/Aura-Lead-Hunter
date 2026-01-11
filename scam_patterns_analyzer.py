import csv
import re
from pathlib import Path
from collections import Counter, defaultdict

# --- CONFIGURATION ---
DATA_DIR = Path(r"d:\Aura Lead Hunter\data")
OUTPUT_FILE = DATA_DIR / "SCAM_ANALYSIS_REPORT.md"

# Patterns that scream "Too good to be true"
VOLUME_PATTERNS = [
    r"\b\d+m\+?", r"\bmillions?\b", r"\b\d+000\s*daily", 
    r"\bunlimited\b", r"\b5k\b", r"\b10k\b", r"\bbig\s*volume"
]

SUSPICIOUS_TERMS = [
    "daily", "no hold", "instant", "prepay", "pre-payment", 
    "immediately", "right now", "fast cash", "usdt daily"
]

def analyze_scam_patterns():
    user_messages = defaultdict(list)
    user_metadata = {}
    
    csv_files = list(DATA_DIR.glob("*.csv"))
    print(f"Analyzing {len(csv_files)} files for behavioral anomalies...")

    scam_candidates = []
    total_users = 0

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_users += 1
                    uid = row.get('user_id', row.get('telegram_handle', 'unknown'))
                    msg = row.get('message_preview', '').strip()
                    chat = row.get('source_chat', 'unknown')
                    score = int(row.get('score', 0))
                    
                    if not msg: continue
                    
                    user_messages[uid].append({
                        'msg': msg,
                        'chat': chat,
                        'file': csv_file.name
                    })
                    
                    user_metadata[uid] = {
                        'handle': row.get('telegram_handle', 'N/A'),
                        'score': score,
                        'summary': row.get('ai_summary_ru', row.get('ai_summary_en', ''))
                    }
        except:
            continue

    # --- CROSS-ANALYSIS LOGIC ---
    report_data = []
    
    for uid, activity in user_messages.items():
        reasons = []
        is_suspicious = False
        
        # 1. Multi-chat Spamming (Redundancy Check)
        unique_chats = set(a['chat'] for a in activity)
        if len(unique_chats) > 2:
            reasons.append(f"Spamming across {len(unique_chats)} different chats")
            is_suspicious = True
            
        # 2. Volume Inflation Check
        full_text = " ".join(a['msg'] for a in activity).lower()
        matched_volumes = [p for p in VOLUME_PATTERNS if re.search(p, full_text)]
        if matched_volumes:
            reasons.append(f"Unrealistic volume claims: {', '.join(matched_volumes)}")
            if user_metadata[uid]['score'] >= 8: # High score + high volume = high risk
                is_suspicious = True
        
        # 3. Aggressive Payout Terms
        matched_terms = [t for t in SUSPICIOUS_TERMS if t in full_text]
        if matched_terms:
            reasons.append(f"Aggressive payout pressure: {', '.join(matched_terms)}")

        if is_suspicious or len(reasons) >= 2:
            report_data.append({
                'uid': uid,
                'handle': user_metadata[uid]['handle'],
                'score': user_metadata[uid]['score'],
                'reasons': reasons,
                'summary': user_metadata[uid]['summary']
            })

    # --- SAVE REPORT ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🛡️ Aura AI: Behavioral Scant Analyzer (Anti-Scam Report)\n")
        f.write(f"Analyzed {total_users} users across {len(csv_files)} data sources.\n\n")
        
        f.write("## 🚨 High-Risk Anomalies Detected\n")
        f.write("| Score | Handle / ID | Risk Factors | Summary |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        # Sort by number of reasons (risk intensity)
        sorted_scam = sorted(report_data, key=lambda x: len(x['reasons']), reverse=True)
        
        for s in sorted_scam:
            f.write(f"| {s['score']}/10 | **{s['handle']}** | {'<br>'.join(s['reasons'])} | {s['summary']} |\n")

    print(f"Analysis complete! Found {len(report_data)} high-risk behavioral patterns.")
    print(f"Report saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_scam_patterns()
