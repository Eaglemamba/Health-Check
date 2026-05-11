#!/usr/bin/env python3
"""
從 Garmin HR / 步數 / 壓力資料回推「上床時間」與「入睡 latency」

Garmin Connect 的 `sleepStartTimestampLocal` 是手錶偵測到的「已入睡」時點，
不是「上床時點」。Garmin 不獨立記錄上床時間。本腳本以下列訊號回推：

- HR 2-min sample（主訊號）：以入睡後 30 分 HR 中位數為 sleep baseline，
  找出 sleep_onset 前最後一個 HR > baseline + 5 bpm 的樣本
- 步數 15-min bin：找出睡眠視窗開始前最後一個 steps >= 10 的 bin
- 壓力 3-min sample：找出睡眠視窗開始前最後一個 stress >= 40 的樣本
- 上床候選 = max(三個訊號)
- Latency = sleep_onset − 上床候選

用法：
    python scripts/estimate_sleep_latency.py --date 2026-05-11
    python scripts/estimate_sleep_latency.py --date 2026-05-11 --json
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
TPE = timezone(timedelta(hours=8))

# 啟發式門檻
STEPS_ACTIVE_MIN = 10        # 15-min bin >= 10 步視為「醒著活動」
STRESS_HIGH_MIN = 40         # stress >= 40 視為明確清醒
HR_AWAKE_DELTA_BPM = 5       # HR 高於入睡後 HR 中位數 +5 bpm 視為清醒
SLEEP_BASELINE_MIN = 30      # 用入睡後前 30 分鐘 HR 樣本計算 baseline
LATENCY_MAX_MIN = 90         # latency 上限（避免被遠處離群點拉壞）
SEARCH_WINDOW_MIN = 120      # 只往睡眠視窗前 120 分鐘內找訊號
LOW_CONFIDENCE_MIN = 45      # latency > 45 分 → 標記低信心（可能是久坐而非真在床）


def _load_json(date: str) -> dict | None:
    p = DATA_DIR / f"{date}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _parse_iso_naive_as_gmt(s: str) -> datetime:
    """Garmin 在多數欄位以無時區 ISO 字串表示 GMT 時間，補上 UTC 時區。"""
    return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc)


def _gather_steps_bins(jsons: list[dict]) -> list[tuple[datetime, datetime, int]]:
    """合併多份 JSON 的 steps 陣列，去重後依時間排序。回傳 [(start_utc, end_utc, steps)]。"""
    seen = {}
    for d in jsons:
        if not d:
            continue
        for seg in d.get("steps") or []:
            s = seg.get("startGMT")
            e = seg.get("endGMT")
            v = seg.get("steps")
            if not (s and e and v is not None):
                continue
            seen[s] = (_parse_iso_naive_as_gmt(s), _parse_iso_naive_as_gmt(e), int(v))
    return sorted(seen.values(), key=lambda x: x[0])


def _gather_hr_samples(jsons: list[dict]) -> list[tuple[datetime, int]]:
    """合併 heart_rates.heartRateValues。格式 [[epoch_ms_gmt, bpm], ...]，去重排序。"""
    seen = {}
    for d in jsons:
        if not d:
            continue
        arr = (d.get("heart_rates") or {}).get("heartRateValues") or []
        for item in arr:
            if not (isinstance(item, list) and len(item) >= 2):
                continue
            ts_ms, val = item[0], item[1]
            if ts_ms is None or val is None:
                continue
            seen[ts_ms] = (datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc), int(val))
    return sorted(seen.values(), key=lambda x: x[0])


def _gather_stress_samples(jsons: list[dict]) -> list[tuple[datetime, int]]:
    """合併 stress 陣列。Garmin stress array 為 [[epoch_ms_gmt, value], ...]，value -1/-2 為無資料/活動。"""
    seen = {}
    for d in jsons:
        if not d:
            continue
        arr = (d.get("stress") or {}).get("stressValuesArray") or []
        for item in arr:
            if not (isinstance(item, list) and len(item) >= 2):
                continue
            ts_ms, val = item[0], item[1]
            if ts_ms is None or val is None:
                continue
            seen[ts_ms] = (datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc), int(val))
    return sorted(seen.values(), key=lambda x: x[0])


def estimate(date: str) -> dict:
    """回傳 dict，包含 sleep_onset / bedtime_est / latency_min / signals / quality。

    date = sleep block 所在 calendarDate（= 起床日，與 sync_garmin_daily.py 一致）。
    讀 date 與 date-1 兩份 JSON 以涵蓋睡前活動。
    """
    today = _load_json(date)
    if not today:
        return {"error": f"找不到 {date}.json"}

    yesterday_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = _load_json(yesterday_date)

    dto = ((today.get("sleep") or {}).get("dailySleepDTO")) or {}
    sleep_start_gmt_ms = dto.get("sleepStartTimestampGMT")
    sleep_start_local_ms = dto.get("sleepStartTimestampLocal")
    if not sleep_start_gmt_ms:
        return {"error": "JSON 內無 sleepStartTimestampGMT"}

    sleep_onset_utc = datetime.fromtimestamp(sleep_start_gmt_ms / 1000, tz=timezone.utc)
    sleep_onset_tpe = sleep_onset_utc.astimezone(TPE)
    search_floor = sleep_onset_utc - timedelta(minutes=SEARCH_WINDOW_MIN)

    # === 步數訊號 ===
    bins = _gather_steps_bins([today, yesterday])
    last_active_end = None  # UTC
    for start_utc, end_utc, steps in bins:
        if end_utc > sleep_onset_utc:
            continue
        if start_utc < search_floor:
            continue
        if steps >= STEPS_ACTIVE_MIN:
            if last_active_end is None or end_utc > last_active_end:
                last_active_end = end_utc

    # === 壓力訊號 ===
    samples = _gather_stress_samples([today, yesterday])
    last_high_stress = None  # UTC
    for ts_utc, val in samples:
        if ts_utc > sleep_onset_utc:
            continue
        if ts_utc < search_floor:
            continue
        if val >= STRESS_HIGH_MIN:
            if last_high_stress is None or ts_utc > last_high_stress:
                last_high_stress = ts_utc

    # === HR 訊號（主訊號）===
    hr_samples = _gather_hr_samples([today, yesterday])
    sleep_baseline_end = sleep_onset_utc + timedelta(minutes=SLEEP_BASELINE_MIN)
    baseline_vals = [v for t, v in hr_samples if sleep_onset_utc <= t <= sleep_baseline_end]
    last_high_hr = None  # UTC
    hr_baseline = None
    if len(baseline_vals) >= 5:
        baseline_vals.sort()
        hr_baseline = baseline_vals[len(baseline_vals) // 2]  # median
        hr_threshold = hr_baseline + HR_AWAKE_DELTA_BPM
        for ts_utc, val in hr_samples:
            if ts_utc > sleep_onset_utc:
                continue
            if ts_utc < search_floor:
                continue
            if val >= hr_threshold:
                if last_high_hr is None or ts_utc > last_high_hr:
                    last_high_hr = ts_utc

    # === 上床候選 = 三訊號中較晚者 ===
    candidates = [c for c in (last_active_end, last_high_stress, last_high_hr) if c is not None]
    if not candidates:
        return {
            "date": date,
            "sleep_onset_local": sleep_onset_tpe.strftime("%H:%M"),
            "bedtime_est_local": None,
            "latency_min": None,
            "quality": "no_signal",
            "note": "前 120 分鐘無步數或壓力訊號，無法回推",
        }

    bedtime_utc = max(candidates)
    latency_min = round((sleep_onset_utc - bedtime_utc).total_seconds() / 60)

    quality = "ok"
    note_parts = []
    if latency_min < 0:
        latency_min = 0
        quality = "clipped_zero"
    elif latency_min > LATENCY_MAX_MIN:
        quality = "capped"
        note_parts.append(f"原始 {latency_min} 分，超過 {LATENCY_MAX_MIN} 分上限")
        latency_min = LATENCY_MAX_MIN
    elif latency_min > LOW_CONFIDENCE_MIN:
        quality = "low_confidence"
        note_parts.append("久坐時段過長，真實 latency 可能小於估計值")

    if last_active_end is None:
        note_parts.append("步數訊號缺")
    if last_high_stress is None:
        note_parts.append("壓力訊號缺")
    if last_high_hr is None:
        note_parts.append("HR 訊號缺")

    bedtime_tpe = bedtime_utc.astimezone(TPE)

    return {
        "date": date,
        "sleep_onset_local": sleep_onset_tpe.strftime("%H:%M"),
        "sleep_onset_utc_ms": sleep_start_gmt_ms,
        "bedtime_est_local": bedtime_tpe.strftime("%H:%M"),
        "bedtime_est_utc_ms": int(bedtime_utc.timestamp() * 1000),
        "latency_min": latency_min,
        "signals": {
            "last_high_hr_local": last_high_hr.astimezone(TPE).strftime("%H:%M") if last_high_hr else None,
            "last_active_end_local": last_active_end.astimezone(TPE).strftime("%H:%M") if last_active_end else None,
            "last_high_stress_local": last_high_stress.astimezone(TPE).strftime("%H:%M") if last_high_stress else None,
            "hr_baseline_bpm": hr_baseline,
        },
        "quality": quality,
        "note": "; ".join(note_parts) if note_parts else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="Sleep block 的 calendarDate（起床日），YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="輸出 JSON 而非文字")
    args = ap.parse_args()

    result = estimate(args.date)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if "error" in result:
        print(f"[error] {result['error']}")
        sys.exit(1)

    print(f"=== 睡眠 latency 估算 — {result['date']} ===")
    print(f"  Garmin 偵測入睡：{result['sleep_onset_local']}")
    print(f"  估算上床時間：  {result['bedtime_est_local'] or '—'}")
    print(f"  入睡 latency：  {result['latency_min'] if result['latency_min'] is not None else '—'} 分")
    sig = result.get("signals") or {}
    hr_b = sig.get("hr_baseline_bpm")
    print(f"  訊號：HR>baseline+{HR_AWAKE_DELTA_BPM} {sig.get('last_high_hr_local') or '—'}（baseline {hr_b or '—'} bpm）"
          f"｜活動 bin 終止 {sig.get('last_active_end_local') or '—'}"
          f"｜高壓力 {sig.get('last_high_stress_local') or '—'}")
    print(f"  品質：{result['quality']}")
    if result.get("note"):
        print(f"  備註：{result['note']}")


if __name__ == "__main__":
    main()
