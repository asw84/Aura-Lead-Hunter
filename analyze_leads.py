"""Quick lead analysis script"""
import pandas as pd
from pathlib import Path

# Find latest leads file
data_dir = Path('data')
leads_files = sorted(data_dir.glob('leads_*.csv'), reverse=True)

if not leads_files:
    print("No leads files found!")
    exit()

latest = leads_files[0]
print(f"Analyzing: {latest.name}")

df = pd.read_csv(latest)

print('=' * 70)
print('📊 СТАТИСТИКА ЛИДОВ')
print('=' * 70)

print(f'\n🎯 Всего лидов: {len(df)}')
hot = df[df['score'] >= 7]
warm = df[(df['score'] >= 5) & (df['score'] < 7)]
print(f'🔥 Горячих (score >= 7): {len(hot)}')
print(f'🟡 Тёплых (score 5-6): {len(warm)}')

print('\n📈 По категориям:')
print(df['category'].value_counts().to_string())

print('\n📍 По источникам (чатам):')
print(df['source_chat'].value_counts().to_string())

print('\n' + '=' * 70)
print('🔥 ТОП-20 ГОРЯЧИХ ЛИДОВ (score >= 7):')
print('=' * 70)

hot_sorted = hot.sort_values('score', ascending=False).head(20)
for idx, (i, row) in enumerate(hot_sorted.iterrows(), 1):
    handle = str(row['telegram_handle'])[:22]
    score = row['score']
    cat = str(row['category'])[:12]
    reason = str(row['ai_summary'])[:60]
    if len(str(row['ai_summary'])) > 60:
        reason += '...'
    print(f'{idx:2}. [{score}/10] {handle:22} | {cat:12} | {reason}')

print('\n' + '=' * 70)
print('📋 Экспорт контактов для outreach:')
print('=' * 70)

# Show handles for easy copy
print('\nГорячие лиды (@username):')
for handle in hot_sorted['telegram_handle'].tolist():
    print(f'  {handle}')
