#!/usr/bin/env python3
"""
回寫飲水量至 Garmin Connect（支援指定日期）

用法：
    python scripts/log_hydration.py --ml 2500             # 回寫至昨日
    python scripts/log_hydration.py --ml 2500 --date 2026-04-19
    python scripts/log_hydration.py --ml -250             # 從目前值扣除 250 mL

注意：add_hydration_data 是「累加」而非「覆寫」。若當天已有紀錄，會加上去。
"""
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_garmin_daily import get_client  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ml", type=float, required=True, help="飲水量 mL（正=加，負=扣）")
    ap.add_argument("--date", default=None, help="YYYY-MM-DD，預設昨日")
    ap.add_argument("--replace", action="store_true", help="覆寫模式：先讀當日值，計算 delta")
    args = ap.parse_args()

    target = args.date or (
        datetime.date.today() - datetime.timedelta(days=1)
    ).isoformat()

    client = get_client()

    if args.replace:
        current = client.get_hydration_data(target) or {}
        existing = current.get("valueInML") or 0
        delta = args.ml - existing
        if abs(delta) < 1:
            print(f"{target} 目前已有 {existing} mL，與目標 {args.ml} 相同，不需回寫")
            return
        print(f"{target} 目前 {existing} mL → 目標 {args.ml} mL，推送 delta {delta:+.0f} mL")
        client.add_hydration_data(value_in_ml=delta, cdate=target)
    else:
        print(f"推送 {args.ml:+.0f} mL 至 Garmin {target}")
        client.add_hydration_data(value_in_ml=args.ml, cdate=target)

    final = client.get_hydration_data(target) or {}
    print(f"完成。{target} 目前飲水量：{final.get('valueInML')} mL / 目標 {final.get('goalInML')} mL")


if __name__ == "__main__":
    main()
