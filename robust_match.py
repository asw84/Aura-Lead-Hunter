import csv
import re
from pathlib import Path

DATA_DIR = Path(r"d:\Aura Lead Hunter\data")
WHALES_FILE = DATA_DIR / "GAMBLING_KEWAL_WHALES.txt"
OUTPUT_FILE = DATA_DIR / "WHALES_WITH_USERNAMES.md"

def robust_match():
    # 1. Сначала вытянем всё, что нашли в GAMBLING_KEWAL_WHALES.txt
    whales_data = []
    if not WHALES_FILE.exists():
        print("Файл с китами не найден.")
        return

    with open(WHALES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Ищем блоки данных, разделенные пунктиром
    entries = re.split(r'-{30,}', content)
    
    for entry in entries:
        lines = [l.strip() for l in entry.strip().split("\n") if l.strip()]
        if not lines: continue
        
        # Ищем строку с скором: [9/10] ID:... или [9/10] @...
        header = None
        for line in lines:
            if re.match(r'\[\d+/10\]', line):
                header = line
                break
        
        if not header: continue
        
        try:
            score_part = header.split("]")[0][1:]
            contact = header.split("]")[1].strip()
            
            summary = ""
            for l in lines:
                if l.startswith("Summary:"):
                    summary = l.replace("Summary:", "").strip()
            
            whales_data.append({
                "contact": contact,
                "score": score_part,
                "summary": summary,
                "handle": contact if contact.startswith("@") else None,
                "id": contact.replace("ID:", "") if contact.startswith("ID:") else None
            })
        except Exception as e:
            print(f"Ошибка при парсинге строки '{header}': {e}")
            continue

    if not whales_data:
        print("Не удалось распарсить данные из файла.")
        return

    # 2. Ищем ники для тех, у кого только ID
    csv_files = list(DATA_DIR.glob("*.csv"))
    
    for whale in whales_data:
        if not whale["handle"] and whale["id"]:
            # Пытаемся найти ник во всех CSV
            for csv_file in csv_files:
                try:
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Проверяем и user_id и telegram_handle (на случай если ID записан там)
                            if row.get('user_id') == whale["id"] or row.get('telegram_handle') == f"ID:{whale['id']}":
                                handle = row.get('telegram_handle')
                                if handle and handle.startswith("@"):
                                    whale["handle"] = handle
                                    break
                except: continue
                if whale["handle"]: break

    # 3. Генерируем красивый отчет
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🐳 Gambling & India Whales: Actionable Contacts\n")
        f.write("Бот Aura отфильтровал прямых рекламодателей и владельцев сеток.\n\n")
        f.write("| Score | Username | Summary | Original ID |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        # Сортируем: сначала те, у кого есть @handle, потом по скору
        # Конвертируем скор в число для правильной сортировки (9/10 -> 9)
        def get_score_val(w):
            try:
                return int(w["score"].split("/")[0])
            except:
                return 0

        sorted_whales = sorted(whales_data, key=lambda x: (x["handle"] is None, -get_score_val(x)))
        
        for w in sorted_whales:
            handle_display = f"**{w['handle']}**" if w['handle'] else "_Unknown_"
            f.write(f"| {w['score']} | {handle_display} | {w['summary']} | {w['id'] if w['id'] else 'N/A'} |\n")

    print(f"Success! Processed {len(whales_data)} whales.")
    print(f"Report: {OUTPUT_FILE}")

if __name__ == "__main__":
    robust_match()
