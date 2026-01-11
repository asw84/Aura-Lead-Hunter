import csv
from pathlib import Path

DATA_DIR = Path(r"d:\Aura Lead Hunter\data")
TARGET = "oleg_trafficbalance"

def search_oleg():
    csv_files = list(DATA_DIR.glob("*.csv"))
    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = str(row).lower()
                    if TARGET.lower() in text:
                        print(f"--- Found in {csv_file.name} ---")
                        for k, v in row.items():
                            print(f"{k}: {v}")
                        print("-" * 30)
        except Exception as e:
            continue

if __name__ == "__main__":
    search_oleg()
