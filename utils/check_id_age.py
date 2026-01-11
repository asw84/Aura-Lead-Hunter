import csv
from pathlib import Path

# Static map of Telegram ID launch years (approximate)
ID_TIMELINE = {
    100000000: "2015 or earlier",
    500000000: "2017/2018",
    1000000000: "2019/2020",
    5000000000: "2021/2022",
    6000000000: "2023",
    7000000000: "Late 2024 (Risk: Newbie/Spammer)"
}

def check_id_age(user_id):
    uid = int(user_id)
    year = "Recent (2024+)"
    for limit in sorted(ID_TIMELINE.keys(), reverse=True):
        if uid >= limit:
            year = ID_TIMELINE[limit]
            break
    return year

# Test it on you and Mohit
print(f"Sergey (You) | ID: 5059160861 | Approx Age: {check_id_age(5059160861)}")
print(f"Mohit (Loh)  | ID: 7453055850 | Approx Age: {check_id_age(7453055850)}")
