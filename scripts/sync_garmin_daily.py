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
        # 優先讀環境變數 GARMIN_MFA（給非 TTY 環境如 Claude Code 用）；無則走互動 input。
        env_code = os.getenv("GARMIN_MFA", "").strip()
        if env_code:
            print(f"使用環境變數 GARMIN_MFA：{env_code}")
            return env_code
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

    # garminconnect 0.3.x：prompt_mfa 在建構式注入，login(tokenstore) 自動處理 MFA 並寫入 token。
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
        "activities": safe_call("activities", client.get_activities_by_date, iso_date, iso_date),
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
        wake_ms_gmt = dto.get("sleepEndTimestampGMT")
        lines += [
            "## 睡眠",
            f"- 就寢：{_hhmm(bed_ms) or '—'}｜起床：{_hhmm(wake_ms) or '—'}",
            f"- 總時長：{dur_s // 3600}h {(dur_s % 3600) // 60}m",
            f"- 深眠：{deep_s // 60} 分｜REM：{rem_s // 60} 分",
            f"- Sleep Score：{score if score is not None else '—'}",
        ]

        # Prefer sleepBodyBattery (per-minute during sleep, GMT) over daily body_battery array.
        # sleepBodyBattery startGMT is directly comparable to sleepEndTimestampGMT.
        bb_wake = None
        sbb = sleep.get("sleepBodyBattery") or []
        if isinstance(sbb, list) and sbb and wake_ms_gmt:
            valid_sbb = [e for e in sbb if isinstance(e, dict) and e.get("startGMT") and e.get("value") is not None]
            if valid_sbb:
                closest = min(valid_sbb, key=lambda e: abs(e["startGMT"] - wake_ms_gmt))
                bb_wake = closest["value"]
        if bb_wake is None:
            bb_list = payload.get("body_battery") or []
            if isinstance(bb_list, list) and bb_list and wake_ms_gmt:
                arr = (bb_list[0] or {}).get("bodyBatteryValuesArray") or []
                valid = [x for x in arr if isinstance(x, list) and len(x) >= 2 and x[0] and x[1] is not None]
                if valid:
                    closest = min(valid, key=lambda x: abs(x[0] - wake_ms_gmt))
                    bb_wake = closest[1]
        if bb_wake is not None:
            lines.append(f"- Body Battery 起床值：{bb_wake}")

        # === Sleep latency 估算（HR/步數/壓力回推上床時間）===
        try:
            from estimate_sleep_latency import estimate as estimate_latency
            est = estimate_latency(d)
            if est and "error" not in est and est.get("bedtime_est_local"):
                lat = est.get("latency_min")
                lo = est.get("latency_min_lower")
                hi = est.get("latency_min_upper")
                q = est.get("quality")
                src = est.get("source")
                src_tag = "（手動）" if src == "manual_override" else ""
                if lo is not None and hi is not None and lo != hi:
                    lat_str = f"{lat} 分（範圍 {lo}–{hi} 分）"
                else:
                    lat_str = f"{lat} 分"
                q_tag = "" if q in ("ok", "manual") else f"（{q}）"
                lines.append(f"- 估算上床：{est['bedtime_est_local']}{src_tag}｜入睡 latency：{lat_str}{q_tag}")
                if est.get("note"):
                    lines.append(f"  - 備註：{est['note']}")
        except Exception as e:
            lines.append(f"- 估算上床：—（估算失敗：{e.__class__.__name__}）")

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

    # === Activities（運動 / 騎車 / 走路 等）===
    acts = payload.get("activities") or []
    if isinstance(acts, list) and acts:
        # Sort by startTimeLocal
        acts_sorted = sorted(acts, key=lambda a: a.get("startTimeLocal", ""))
        lines += ["## 活動", "| 時段 | 類型 | 距離 | 時長 | 平均 HR | 最大 HR | 主動 kcal | 含 BMR |",
                  "|------|------|------|------|---------|---------|-----------|--------|"]
        tot_dist = 0.0
        tot_dur = 0.0
        tot_kcal_active = 0.0
        tot_kcal_total = 0.0
        for a in acts_sorted:
            start = (a.get("startTimeLocal") or "")[-8:-3]  # HH:MM
            atype = (a.get("activityType") or {}).get("typeKey", "—")
            dist_m = a.get("distance") or 0
            dur_s = a.get("duration") or 0
            avg_hr = a.get("averageHR")
            max_hr = a.get("maxHR")
            cal_active = a.get("calories") or 0
            cal_bmr = a.get("bmrCalories") or 0
            cal_total = cal_active + cal_bmr
            tot_dist += dist_m
            tot_dur += dur_s
            tot_kcal_active += cal_active
            tot_kcal_total += cal_total
            lines.append(
                f"| {start} | {atype} | {dist_m/1000:.2f} km | {dur_s/60:.1f} min | "
                f"{int(avg_hr) if avg_hr else '—'} | {int(max_hr) if max_hr else '—'} | "
                f"{int(cal_active)} | {int(cal_total)} |"
            )
        if len(acts_sorted) > 1:
            lines.append(
                f"| **小計** | {len(acts_sorted)} 段 | **{tot_dist/1000:.2f} km** | "
                f"**{tot_dur/60:.1f} min** | — | — | **{int(tot_kcal_active)}** | **{int(tot_kcal_total)}** |"
            )
        lines.append("")

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
    ap.add_argument("--date", help="YYYY-MM-DD；預設今日（Garmin calendarDate 以起床日歸檔，今日 = 昨夜睡眠）")
    ap.add_argument("--days-back", type=int, default=0, help="抓幾天前（預設 0 = 今日；需昨日 day-level 總量用 1）")
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
