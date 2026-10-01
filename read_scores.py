import csv
from pathlib import Path

data_path = Path("data/evaluation.csv")

with data_path.open(encoding="utf-8", newline="") as file:
    rows = list(csv.DictReader(file))

for row in rows:
    print(f"{row['model']}：{row['score']} 分")

average = sum(int(row["score"]) for row in rows) / len(rows)
print(f"平均分數：{average:.1f}")
