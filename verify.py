"""在主機或 CI 執行，檢查指定 Image 的實際輸出是否符合專案 CSV。"""
import csv
import math
import subprocess
import sys
from pathlib import Path

image = sys.argv[1] if len(sys.argv) > 1 else "python-report:ci"
with (Path(__file__).parent / "data/evaluation.csv").open(encoding="utf-8", newline="") as file:
    rows = list(csv.DictReader(file))
if not rows:
    raise SystemExit("驗證失敗：CSV 沒有資料")
expected = [f"{row['model']}：{row['score']} 分" for row in rows]
average = math.fsum(float(row["score"]) for row in rows) / len(rows)
expected.append(f"平均分數：{average:.1f}")
result = subprocess.run(["docker", "run", "--rm", image], capture_output=True, text=True, encoding="utf-8")
print(result.stdout, end="")
if result.returncode != 0:
    print(result.stderr, file=sys.stderr)
    raise SystemExit("驗證失敗：Container 未正常完成")
actual = result.stdout.splitlines()
if actual != expected:
    print("預期輸出：\n" + "\n".join(expected), file=sys.stderr)
    raise SystemExit("驗證失敗：報表內容或平均分數不正確")
print("驗證通過：報表列數、分數與平均值正確")
