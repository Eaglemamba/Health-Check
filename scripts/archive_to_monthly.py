#!/usr/bin/env python3
"""
月份歸檔：將 daily-style 檔案中**非當週 ISO week** 的檔案移至 YYYY-MM/ 子資料夾。

涵蓋三個資料夾：
  - reviews/daily/          *.md
  - reports/daily-garmin/   *.md
  - data/garmin/            *.json  (gitignored 內容)

設計：
  - 當週 = 今日所在 ISO week (Asia/Taipei)
  - 非當週的 YYYY-MM-DD.* 檔案 → 移至同資料夾下 YYYY-MM/ 子資料夾
  - Idempotent：已歸檔的檔案不再動
  - --dry-run：列出將移動的檔案但不實際執行
  - 純 stdlib，無第三方依賴

用法：
  python scripts/archive_to_monthly.py             # 實際執行
  python scripts/archive_to_monthly.py --dry-run   # 預演

整合：建議掛在 daily check-in 流程末段（sync_data_js 之後、git add 之前）。
週日跑一次即可，但天天跑也無妨（不會誤動當週檔案）。
"""
import argparse
import re
import shutil
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
TPE = timezone(timedelta(hours=8))
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

# (folder, extension) pairs to manage
TARGETS = [
    (ROOT / "reviews" / "daily",        "md"),
    (ROOT / "reports" / "daily-garmin", "md"),
    (ROOT / "data"    / "garmin",       "json"),
]


def current_iso_week_range(today_local: date) -> tuple[date, date]:
    """回傳今日所在 ISO week 的 Mon-Sun (date, date)。"""
    weekday = today_local.weekday()  # Mon=0, Sun=6
    monday = today_local - timedelta(days=weekday)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def archive_folder(folder: Path, ext: str, week_start: date, week_end: date, dry_run: bool) -> dict:
    """掃描 folder 內 YYYY-MM-DD.{ext} 檔案；非當週者移到 folder/YYYY-MM/。"""
    if not folder.is_dir():
        return {"folder": str(folder), "skipped": True, "moved": 0, "kept": 0}

    moved = []
    kept = []
    errors = []

    for f in sorted(folder.glob(f"*.{ext}")):
        m = DATE_RE.match(f.stem)
        if not m:
            continue
        yyyy, mm, dd = m.group(1), m.group(2), m.group(3)
        try:
            file_date = date(int(yyyy), int(mm), int(dd))
        except ValueError:
            continue
        if week_start <= file_date <= week_end:
            kept.append(f.name)
            continue
        target_dir = folder / f"{yyyy}-{mm}"
        target_path = target_dir / f.name
        if target_path.exists():
            errors.append(f"target exists: {target_path.relative_to(ROOT)}")
            continue
        if dry_run:
            moved.append((f.name, f"{yyyy}-{mm}/{f.name}"))
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(target_path))
            moved.append((f.name, f"{yyyy}-{mm}/{f.name}"))

    return {
        "folder": str(folder.relative_to(ROOT)),
        "moved": len(moved),
        "kept": len(kept),
        "moved_list": moved,
        "kept_list": kept,
        "errors": errors,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="預演，不實際移動")
    ap.add_argument("--verbose", "-v", action="store_true", help="列出每個檔案")
    args = ap.parse_args()

    today_local = datetime.now(TPE).date()
    week_start, week_end = current_iso_week_range(today_local)

    print(f"今日 (TPE): {today_local}")
    print(f"當週 ISO week: {week_start} ~ {week_end}（保留於根目錄）")
    print(f"{'[DRY-RUN]' if args.dry_run else '[執行]'}")
    print()

    total_moved = 0
    for folder, ext in TARGETS:
        result = archive_folder(folder, ext, week_start, week_end, args.dry_run)
        if result.get("skipped"):
            print(f"[skip] {result['folder']} (資料夾不存在)")
            continue
        print(f"[{result['folder']}]  moved: {result['moved']}  kept: {result['kept']}")
        if result["errors"]:
            for e in result["errors"]:
                print(f"  ! {e}")
        if args.verbose:
            for src, dst in result["moved_list"]:
                print(f"  → {dst}")
            for k in result["kept_list"]:
                print(f"  · {k} (kept)")
        total_moved += result["moved"]

    print()
    if total_moved == 0:
        print("無需歸檔（所有檔案皆在當週或已歸檔）")
    else:
        verb = "將移動" if args.dry_run else "已移動"
        print(f"{verb} {total_moved} 個檔案")


if __name__ == "__main__":
    main()
