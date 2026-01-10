"""Export outreach contacts from existing leads CSV"""
import pandas as pd
from datetime import datetime
from pathlib import Path

# Find latest leads file
data_dir = Path('data')
leads_files = sorted(data_dir.glob('leads_2026*.csv'), reverse=True)

if not leads_files:
    print("No leads files found!")
    exit()

latest = leads_files[0]
print(f"Loading: {latest.name}")

df = pd.read_csv(latest)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Filter leads
hot = df[df['score'] >= 7].sort_values('score', ascending=False)
warm = df[(df['score'] >= 5) & (df['score'] < 7)].sort_values('score', ascending=False)
all_leads = df[df['score'] >= 5].sort_values('score', ascending=False)

# Export HOT
hot_file = data_dir / f'outreach_hot_{timestamp}.txt'
with open(hot_file, 'w', encoding='utf-8') as f:
    f.write(f"# 🔥 HOT LEADS (Score >= 7)\n")
    f.write(f"# Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    f.write(f"# Total: {len(hot)} contacts\n")
    f.write("# " + "─" * 50 + "\n\n")
    for handle in hot['telegram_handle']:
        f.write(f"{handle}\n")
    f.write("\n# " + "─" * 50 + "\n")
    f.write("# Details:\n")
    for _, row in hot.iterrows():
        handle = str(row['telegram_handle'])
        score = row['score']
        cat = str(row['category'])
        f.write(f"# {handle:25} | {score}/10 | {cat}\n")

# Export WARM
warm_file = data_dir / f'outreach_warm_{timestamp}.txt'
with open(warm_file, 'w', encoding='utf-8') as f:
    f.write(f"# 🟡 WARM LEADS (Score 5-6)\n")
    f.write(f"# Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    f.write(f"# Total: {len(warm)} contacts\n")
    f.write("# " + "─" * 50 + "\n\n")
    for handle in warm['telegram_handle']:
        f.write(f"{handle}\n")

# Export ALL
all_file = data_dir / f'outreach_all_{timestamp}.txt'
with open(all_file, 'w', encoding='utf-8') as f:
    f.write(f"# 🎯 ALL LEADS (Score >= 5)\n")
    f.write(f"# Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    f.write(f"# Total: {len(all_leads)} | 🔥 Hot: {len(hot)} | 🟡 Warm: {len(warm)}\n")
    f.write("# " + "─" * 50 + "\n\n")
    for handle in all_leads['telegram_handle']:
        f.write(f"{handle}\n")

print()
print("=" * 60)
print("📤 OUTREACH FILES CREATED")
print("=" * 60)
print(f"🔥 Hot leads:  {hot_file.name} ({len(hot)} contacts)")
print(f"🟡 Warm leads: {warm_file.name} ({len(warm)} contacts)")
print(f"🎯 All leads:  {all_file.name} ({len(all_leads)} contacts)")
print("=" * 60)
