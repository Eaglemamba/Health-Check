#!/usr/bin/env python3
"""
Daily Garmin Connect sync — 抓取昨日睡眠/HR/壓力/步數/SpO2 資料

第一次執行會要 MFA code（email 或 Authenticator）；之後 token 快取在 .garth/
可自動維持約 1 年。

用法：
    python scripts/sync_garmin_daily.py
    python scripts/sync_garmin_daily.py --date 2026-04-19
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
except ImportError:
    print("需先安裝套件：pip install garminconnect python-dotenv")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
TOKEN_DIR = ROOT / ".garth"
OUT_DIR = ROOT / "data" / "garmin"
SUMMARY_DIR = ROOT / "reports" / "daily-garmin"


def get_client() -> Garmin:
    """登入 Garmin Connect，優先用快取 token。"""
    load_dotenv(ROOT / ".env")

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    def prompt_mfa() -> str:
        return input("輸入 Garmin MFA 驗證碼：").strip()

    TOKEN_DIR.mkdir(parents=True, exist_ok=True)

    if TOKEN_DIR.exists() and any(TOKEN_DIR.iterdir()):
        try:
            client = Garmin()
            client.login(str(TOKEN_DIR))
            return client
        except (GarminConnectAuthenticationError, FileNotFoundError):
            print("快取 token 失效，改用帳密重新登入")

    if not email or not password:
        print("錯誤：請在 .env 設定 GARMIN_EMAIL 與 GARMIN_PASSWORD")
        sys.exit(1)

    client = Garmin(email=email, password=password, prompt_mfa=prompt_mfa)
    client.login(str(TOKEN_DIR))
    print(f"Token 已存入 {TOKEN_DIR}")
    return client


def safe_call(label: str, fn, *args):
    try:
        return fn(*args)
    except Exception as e:
        print(f"  [skip] {label}: {e.__class__.__name__}")
        return None


def fetch_day(client: Garmin, iso_date: str) -> dict:
    """抓取一天的所有可用指標。"""
    print(f"抓取 {iso_date}")
    return {
        "date": iso_date,
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "sleep": safe_call("sleep", client.get_sleep_data, iso_date),
        "heart_rates": safe_call("heart_rates", client.get_heart_rates, iso_date),
        "rhr": safe_call("rhr", client.get_rhr_day, iso_date),
        "stress": safe_call("stress", client.get_stress_data, iso_date),
        "body_battery": safe_call("body_battery", client.get_body_battery, iso_date),
        "steps": safe_call("steps", client.get_steps_data, iso_date),
        "spo2": safe_call("spo2", client.get_spo2_data, iso_date),
        "respiration": safe_call("respiration", client.get_respiration_data, iso_date),
        "hydration": safe_call("hydration", client.get_hydration_data, iso_date),
        "training_readiness": safe_call(
            "training_readiness", client.get_training_readiness, iso_date
        ),
    }


def summarize(payload: dict) -> str:
    """生成 markdown 摘要，不含 raw JSON。"""
    d = payload["date"]
    lines = [f"# Garmin 每日摘要 — {d}", ""]

    from datetime import timezone
    def _hhmm(ms):
        if not ms:
            return None
        return datetime.datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%H:%M")

    sleep = payload.get("sleep") or {}
    dto = sleep.get("dailySleepDTO") or {}
    wake_ms = None
    if dto:
        dur_s = dto.get("sleepTimeSeconds") or 0
        deep_s = dto.get("deepSleepSeconds") or 0
        rem_s = dto.get("remSleepSeconds") or 0
        score = (dto.get("sleepScores") or {}).get("overall", {}).get("value")
        bed_ms = dto.get("sleepStartTimestampLocal")
        wake_ms = dto.get("sleepEndTimestampLocal")
        lines += [
            "## 睡眠",
            f"- 就寢：{_hhmm(bed_ms) or '—'}｜起床：{_hhmm(wake_ms) or '—'}",
            f"- 總時長：{dur_s // 3600}h {(dur_s % 3600) // 60}m",
            f"- 深眠：{deep_s // 60} 分｜REM：{rem_s // 60} 分",
            f"- Sleep Score：{score if score is not None else '—'}",
        ]

        bb_list = payload.get("body_battery") or []
        if isinstance(bb_list, list) and bb_list and wake_ms:
            arr = (bb_list[0] or {}).get("bodyBatteryValuesArray") or []
            valid = [x for x in arr if isinstance(x, list) and len(x) >= 2 and x[0] and x[1] is not None]
            if valid:
                closest = min(valid, key=lambda x: abs(x[0] - wake_ms))
                lines.append(f"- Body Battery 起床值：{closest[1]}")
        lines.append("")

    rhr = payload.get("rhr") or {}
    if rhr:
        stats = (rhr.get("allMetrics") or {}).get("metricsMap") or {}
        rhr_list = stats.get("WELLNESS_RESTING_HEART_RATE") or []
        if rhr_list:
            v = rhr_list[0].get("value")
            lines += ["## 靜息心率", f"- RHR：{v} bpm", ""]

    stress = payload.get("stress") or {}
    avg_stress = stress.get("avgStressLevel")
    if avg_stress is not None:
        lines += ["## 壓力", f"- 日均：{avg_stress}", ""]

    steps = payload.get("steps") or []
    if isinstance(steps, list) and steps:
        total = sum(x.get("steps", 0) or 0 for x in steps)
        lines += ["## 步數", f"- 總計：{total:,}", ""]

    spo2 = payload.get("spo2") or {}
    if spo2:
        avg_sp = spo2.get("averageSpO2")
        low_sp = spo2.get("lowestSpO2")
        lines += [
            "## SpO2",
            f"- 日均：{avg_sp if avg_sp else '—'}%",
            f"- 最低：{low_sp if low_sp else '—'}%",
            "",
        ]

    hyd = payload.get("hydration") or {}
    if hyd:
        val_ml = hyd.get("valueInML")
        goal_ml = hyd.get("goalInML")
        sweat_ml = hyd.get("sweatLossInML")
        if val_ml is not None:
            lines += [
                "## 飲水",
                f"- 實際：{val_ml/1000:.2f} L",
                f"- 目標：{goal_ml/1000:.2f} L" if goal_ml else "- 目標：—",
            ]
            if sweat_ml:
                lines.append(f"- 運動流汗耗水：{sweat_ml/1000:.2f} L")
            lines.append("")
        else:
            lines += [
                "## 飲水",
                "- 實際：— （Garmin Connect 未紀錄，請於 check-in 手動輸入）",
                f"- 目標：{goal_ml/1000:.2f} L" if goal_ml else "- 目標：—",
                "",
            ]

    lines.append(f"_Source: data/garmin/{d}.json (gitignored)_")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD；預設昨天")
    ap.add_argument("--days-back", type=int, default=1, help="抓幾天前（預設 1）")
    args = ap.parse_args()

    target = args.date or (
        datetime.date.today() - datetime.timedelta(days=args.days_back)
    ).isoformat()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    try:
        client = get_client()
    except (GarminConnectConnectionError, GarminConnectTooManyRequestsError) as e:
        print(f"連線問題：{e}")
        sys.exit(2)

    payload = fetch_day(client, target)

    raw_path = OUT_DIR / f"{target}.json"
    raw_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"Raw 已存：{raw_path}")

    summary_path = SUMMARY_DIR / f"{target}.md"
    summary_path.write_text(summarize(payload), encoding="utf-8")
    print(f"摘要已存：{summary_path}")


if __name__ == "__main__":
    main()
