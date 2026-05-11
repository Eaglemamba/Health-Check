#!/usr/bin/env python3
"""
從 reviews/food/{date}.md 抓取每日 Na / K / 熱量 / 蛋白質 等小計，
計算 Na/K 比值與 7-日 trend。

用途：
- daily check-in 時自動校準鈉/鉀預算
- 評估 INTERSALT (Na/K) 風險：< 0.5 理想 / 0.5-0.6 良好 / 0.6-0.8 邊緣 / > 0.8 警示

用法：
    python scripts/analyze_nutrition.py --date 2026-05-11
    python scripts/analyze_nutrition.py --trend 7
    python scripts/analyze_nutrition.py --date 2026-05-11 --json
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Windows cp950 → UTF-8 for emoji/CJK
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
FOOD_DIR = ROOT / "reviews" / "food"

# 目標值（依 templates/food.md 與你健檢狀況校準）
TARGETS = {
    "kcal": 1800,
    "protein_g": 95,
    "fat_g_low": 50,
    "fat_g_high": 65,
    "carb_g_low": 225,
    "carb_g_high": 250,
    "fiber_g": 25,
    "sodium_mg": 1500,
    "potassium_mg": 3500,
    "na_k_ratio_max": 0.6,
}

# 「**小計**」row 的 column mapping
# 舊格式 8 col: 品項 / 份量 / 熱量 / 蛋白 / 脂肪 / 碳水 / 纖維 / 鈉
# 新格式 9 col: 品項 / 份量 / 熱量 / 蛋白 / 脂肪 / 碳水 / 纖維 / 鈉 / 鉀
COL_ORDER = ["item", "portion", "kcal", "protein_g", "fat_g", "carb_g",
             "fiber_g", "sodium_mg", "potassium_mg"]

# Markdown table row pattern, capture cells between |
ROW_RE = re.compile(r"\|\s*\*\*小計\*\*\s*\|(.+)$")
# 全日合計 row（在「每日總計」表）
TOTAL_RE = re.compile(r"\|\s*\*\*合計\*\*\s*\|(.+)$")


def _parse_num(s: str):
    """從 cell 字串擷取第一個數字（移除粗體、單位、emoji、千分號）。"""
    if not s:
        return None
    cleaned = re.sub(r"[*,_]|⚠️|✓|✅|🟢|🟡|🟠|🔴|⭐", "", s)
    m = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(m.group()) if m else None


def parse_food_md(date: str) -> dict | None:
    """讀 reviews/food/{date}.md，聚合所有「**小計**」row 數值（每餐表）。

    回傳 dict: {kcal, protein_g, fat_g, carb_g, fiber_g, sodium_mg, potassium_mg, na_k_ratio, source_rows}
    或 None（找不到檔）
    """
    p = FOOD_DIR / f"{date}.md"
    if not p.exists():
        return None

    text = p.read_text(encoding="utf-8")
    totals = {k: 0.0 for k in ["kcal", "protein_g", "fat_g", "carb_g",
                                "fiber_g", "sodium_mg", "potassium_mg"]}
    source_rows = 0
    # 僅在「食物區塊」（早餐/午餐/晚餐/點心/早餐前/宵夜/加餐 等）統計 subtotals；
    # 排除「活動」「全日總計 / 合計」「補充品」等非食物表。
    FOOD_SECTIONS = ("早餐", "午餐", "晚餐", "點心", "宵夜", "加餐", "早午餐")
    in_food_section = False
    for line in text.splitlines():
        stripped = line.strip()
        # H2 section header
        if stripped.startswith("## "):
            header = stripped[3:].strip()
            in_food_section = any(s in header for s in FOOD_SECTIONS)
            continue
        if not in_food_section:
            continue
        m = ROW_RE.match(stripped)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        # cells[0]=portion, cells[1]=kcal, cells[2]=protein, ...
        for i, key in enumerate(COL_ORDER[1:], start=0):
            if i >= len(cells):
                break
            if key == "portion":
                continue
            v = _parse_num(cells[i])
            if v is not None:
                totals[key] += v
        source_rows += 1

    if source_rows == 0:
        return None

    na = totals["sodium_mg"]
    k = totals["potassium_mg"]
    na_k = na / k if k > 0 else None

    return {
        "date": date,
        "source_rows": source_rows,
        "kcal": totals["kcal"],
        "protein_g": totals["protein_g"],
        "fat_g": totals["fat_g"],
        "carb_g": totals["carb_g"],
        "fiber_g": totals["fiber_g"],
        "sodium_mg": totals["sodium_mg"],
        "potassium_mg": totals["potassium_mg"],
        "na_k_ratio": round(na_k, 3) if na_k is not None else None,
    }


def _na_k_severity(ratio: float | None) -> str:
    if ratio is None:
        return "—"
    if ratio < 0.5:
        return "✅ 理想"
    if ratio < 0.6:
        return "🟢 良好"
    if ratio < 0.8:
        return "🟡 邊緣"
    return "🟠 警示"


def _kcal_severity(kcal: float, target: float) -> str:
    pct = kcal / target * 100
    if pct < 80:
        return "🟡 偏低"
    if pct < 110:
        return "🟢 達標"
    return "🟠 偏高"


def cmd_day(date: str, as_json: bool = False):
    result = parse_food_md(date)
    if not result:
        msg = f"找不到 reviews/food/{date}.md 或內容為空"
        if as_json:
            print(json.dumps({"error": msg, "date": date}, ensure_ascii=False))
        else:
            print(f"[skip] {msg}")
        sys.exit(1)

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    r = result
    print(f"=== 飲食營養分析 — {date} ===")
    print(f"  熱量：       {r['kcal']:>6.0f} kcal     (目標 {TARGETS['kcal']}, {r['kcal']/TARGETS['kcal']*100:.0f}%)  {_kcal_severity(r['kcal'], TARGETS['kcal'])}")
    print(f"  蛋白質：     {r['protein_g']:>6.1f} g       (目標 {TARGETS['protein_g']}, {r['protein_g']/TARGETS['protein_g']*100:.0f}%)")
    print(f"  脂肪：       {r['fat_g']:>6.1f} g       (目標 {TARGETS['fat_g_low']}-{TARGETS['fat_g_high']})")
    print(f"  碳水：       {r['carb_g']:>6.1f} g       (目標 {TARGETS['carb_g_low']}-{TARGETS['carb_g_high']})")
    print(f"  纖維：       {r['fiber_g']:>6.1f} g       (目標 ≥{TARGETS['fiber_g']})")
    print(f"  鈉：         {r['sodium_mg']:>6.0f} mg      (目標 <{TARGETS['sodium_mg']}, {r['sodium_mg']/TARGETS['sodium_mg']*100:.0f}%)")
    print(f"  鉀：         {r['potassium_mg']:>6.0f} mg      (目標 ≥{TARGETS['potassium_mg']}, {r['potassium_mg']/TARGETS['potassium_mg']*100:.0f}%)")
    print(f"  Na/K 比值：  {r['na_k_ratio'] if r['na_k_ratio'] is not None else '—':>6}        (目標 <{TARGETS['na_k_ratio_max']})  {_na_k_severity(r['na_k_ratio'])}")
    print(f"  資料 row 數：{r['source_rows']}")


def cmd_trend(days: int):
    today = datetime.now().date()
    rows = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        date_str = d.isoformat()
        r = parse_food_md(date_str)
        if r:
            rows.append(r)

    if not rows:
        print(f"近 {days} 天皆無 food log 資料")
        return

    print(f"=== Na / K Trend — 近 {days} 天有資料：{len(rows)} 天 ===")
    print()
    print(f"  {'日期':<12} {'熱量':>5} {'鈉(mg)':>7} {'鉀(mg)':>7} {'Na/K':>5}  判讀")
    print("  " + "-" * 60)
    for r in rows:
        sev = _na_k_severity(r["na_k_ratio"])
        nakr = f"{r['na_k_ratio']:.2f}" if r["na_k_ratio"] else "—"
        print(f"  {r['date']:<12} {int(r['kcal']):>5} {int(r['sodium_mg']):>7} {int(r['potassium_mg']):>7} {nakr:>5}  {sev}")

    print("  " + "-" * 60)
    avg_na = sum(r["sodium_mg"] for r in rows) / len(rows)
    avg_k = sum(r["potassium_mg"] for r in rows) / len(rows)
    avg_ratio = avg_na / avg_k if avg_k > 0 else None
    print(f"  {'平均':<12} {'':>5} {int(avg_na):>7} {int(avg_k):>7} "
          f"{avg_ratio:.2f}".ljust(70) + f"  {_na_k_severity(avg_ratio)}")
    print()

    # 警示
    high_na = sum(1 for r in rows if r["sodium_mg"] > TARGETS["sodium_mg"])
    low_k = sum(1 for r in rows if r["potassium_mg"] < TARGETS["potassium_mg"])
    high_ratio = sum(1 for r in rows if r["na_k_ratio"] and r["na_k_ratio"] >= 0.8)
    if high_na:
        print(f"  ⚠️  Na > {TARGETS['sodium_mg']} mg：{high_na}/{len(rows)} 天")
    if low_k:
        print(f"  ⚠️  K < {TARGETS['potassium_mg']} mg：{low_k}/{len(rows)} 天")
    if high_ratio:
        print(f"  🟠 Na/K ≥ 0.8（警示）：{high_ratio}/{len(rows)} 天")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="單日分析（YYYY-MM-DD）")
    ap.add_argument("--trend", type=int, help="近 N 天 trend（含今日往回）")
    ap.add_argument("--json", action="store_true", help="輸出 JSON")
    args = ap.parse_args()

    if not args.date and not args.trend:
        ap.print_help()
        sys.exit(0)

    if args.date:
        cmd_day(args.date, as_json=args.json)
    if args.trend:
        cmd_trend(args.trend)


if __name__ == "__main__":
    main()
