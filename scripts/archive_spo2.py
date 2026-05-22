#!/usr/bin/env python3
"""
SpO2 PNG 週度歸檔：將 reviews/daily/spo2/ 中**非當週 ISO week** 的 PNG 移至 archive/。

規則：
- 檔名含 YYYY-MM-DD（單一日期或範圍）→ 若所有日期 / 範圍終止日均不在當週 → 移至 archive/
- 檔名不含日期但屬「永久軸」（spo2_desat_trend.png / hrv_trend.png / spo2_by_cycle.png）→ 永遠保留
- 其他無日期檔案 → 保守保留至 root
- 同步更新 reviews/daily/*.md 中的圖片連結（`spo2/X.png` → `spo2/archive/X.png`）

用法：
    python scripts/archive_spo2.py                  # 以今日 = 系統時間
    python scripts/archive_spo2.py --date 2026-05-19   # 指定基準日
    python scripts/archive_spo2.py --dry-run        # 預覽不動作
"""
import argparse
import re
import shutil
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
SPO2_DIR = ROOT / "reviews" / "daily" / "spo2"
DAILY_DIR = ROOT / "reviews" / "daily"
ALWAYS_ROOT = {
    "spo2_desat_trend.png",
    "hrv_trend.png",
    "spo2_by_cycle.png",
    "spo2_heatmap_all_nights.png",
}
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def iso_week_range(d: date):
    iso_year, iso_week, iso_dow = d.isocalendar()
    monday = d - timedelta(days=iso_dow - 1)
    sunday = monday + timedelta(days=6)
    return iso_year, iso_week, monday, sunday


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="基準日 YYYY-MM-DD（預設今天）")
    ap.add_argument("--dry-run", action="store_true", help="只列出，不實際移動")
    args = ap.parse_args()

    today = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
    iso_year, iso_week, monday, sunday = iso_week_range(today)
    print(f"基準週：{iso_year}-W{iso_week:02d}  ({monday} ~ {sunday})")

    archive = SPO2_DIR / "archive"
    if not args.dry_run:
        archive.mkdir(exist_ok=True)

    moved, kept = [], []
    for f in sorted(SPO2_DIR.iterdir()):
        if f.is_dir():
            continue
        name = f.name
        if name in ALWAYS_ROOT:
            kept.append(name)
            continue
        matches = DATE_RE.findall(name)
        if not matches:
            kept.append(name)
            continue
        dates = [date(int(y), int(m), int(d)) for y, m, d in matches]
        end_date = max(dates)
        if monday <= end_date <= sunday:
            kept.append(name)
        else:
            moved.append(name)
            if not args.dry_run:
                shutil.move(str(f), str(archive / name))

    print(f"\n保留 root（{len(kept)}）")
    for n in kept:
        print(f"  {n}")
    print(f"\n移至 archive/（{len(moved)}）")
    for n in moved:
        print(f"  {n}")

    if args.dry_run:
        print("\n(dry-run；未實際移動)")
        return

    # Update daily review markdown to point to archive/
    archived_names = {f.name for f in archive.iterdir() if f.is_file()}
    updated_md = 0
    for md in sorted(DAILY_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        orig = text
        for name in archived_names:
            text = re.sub(
                r"(spo2/)(?!archive/)" + re.escape(name),
                r"spo2/archive/" + name,
                text,
            )
        if text != orig:
            md.write_text(text, encoding="utf-8")
            updated_md += 1
    print(f"\n更新 daily review 連結：{updated_md} 個檔案")


if __name__ == "__main__":
    main()
