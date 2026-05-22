#!/usr/bin/env python3
"""
從 Garmin HR / 步數 / 壓力資料回推「上床時間」與「入睡 latency」

Garmin Connect 的 `sleepStartTimestampLocal` 是手錶偵測到的「已入睡」時點，
不是「上床時點」。Garmin 不獨立記錄上床時間。本腳本以下列訊號回推範圍：

- 步數 15-min bin：最後 steps >= 10 的 bin 終止時間（最可靠的「醒著」訊號）
- HR 2-min sample：以入睡後 30 分 HR 中位數為 baseline，
  找出 sleep_onset 前最後一個 HR > baseline + 5 bpm 的樣本
- 壓力 3-min sample：最後 stress >= 40 的樣本

雙估算：
- bedtime_lower（樂觀，短 latency）= max(三個訊號) — 假設 HR 一低就快睡了
- bedtime_upper（悲觀，長 latency）= 步數訊號 — 假設最後動作後就上床
- 兩者差 > 30 分 → quality=wide_range（無法區分「躺床清醒」與「已睡」）

手動覆寫：若 `reviews/daily/{date}.md` 含 `**實際上床：** HH:MM`，以使用者
回答為準（覆寫演算法估算）。

用法：
    python scripts/estimate_sleep_latency.py --date 2026-05-11
    python scripts/estimate_sleep_latency.py --date 2026-05-11 --json
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
DAILY_DIR = ROOT / "reviews" / "daily"
TPE = timezone(timedelta(hours=8))

# 啟發式門檻
STEPS_ACTIVE_MIN = 10        # 15-min bin >= 10 步視為「醒著活動」
STRESS_HIGH_MIN = 40         # stress >= 40 視為明確清醒
HR_AWAKE_DELTA_BPM = 5       # HR 高於入睡後 HR 中位數 +5 bpm 視為清醒
SLEEP_BASELINE_MIN = 30      # 用入睡後前 30 分鐘 HR 樣本計算 baseline
LATENCY_MAX_MIN = 120        # latency 上限（避免被遠處離群點拉壞）
SEARCH_WINDOW_MIN = 180      # 只往睡眠視窗前 180 分鐘內找訊號
WIDE_RANGE_MIN = 30          # upper-lower > 30 分 → wide_range 品質

OVERRIDE_RE = re.compile(r"\*\*實際上床：\*\*\s*(\d{1,2}):(\d{2})")


def _load_json(date: str) -> dict | None:
    p = next(iter(DATA_DIR.rglob(f"{date}.json")), DATA_DIR / f"{date}.json")
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _parse_iso_naive_as_gmt(s: str) -> datetime:
    return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc)


def _gather_steps_bins(jsons):
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


def _gather_hr_samples(jsons):
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


def _gather_stress_samples(jsons):
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


def _read_manual_override(date: str, sleep_onset_tpe: datetime) -> datetime | None:
    """讀取 reviews/daily/{date}.md 內 `**實際上床：** HH:MM`，回傳 UTC datetime 或 None。

    使用者輸入的是當地時間 HH:MM。上床時間通常在 sleep_onset 之前 0-3 小時，
    可能跨日（21:30 上床但 calendar 屬於 5/11；23:50 上床屬於 5/10）。
    取 sleep_onset 前最接近的 HH:MM 為上床時間。
    """
    # 先試根目錄（當週），再試 YYYY-MM/ 月份歸檔子資料夾
    p = DAILY_DIR / f"{date}.md"
    if not p.exists():
        p = DAILY_DIR / date[:7] / f"{date}.md"
        if not p.exists():
            return None
    m = OVERRIDE_RE.search(p.read_text(encoding="utf-8"))
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2))
    # 上床時刻可能在 sleep_onset 同日（晚上 21:30 → 凌晨 02:00 入睡屬同日 calendarDate）
    # 也可能在 sleep_onset 前一日（晚上 23:50 上床屬於 5/10，calendarDate=5/11）
    # 取 sleep_onset 前 24 小時內最接近的 HH:MM
    candidates = []
    for delta_days in (0, -1):
        d_local = (sleep_onset_tpe + timedelta(days=delta_days)).replace(hour=h, minute=mi, second=0, microsecond=0)
        if d_local <= sleep_onset_tpe and (sleep_onset_tpe - d_local) <= timedelta(hours=24):
            candidates.append(d_local)
    if not candidates:
        return None
    bedtime_tpe = max(candidates)  # 最接近 sleep_onset 的
    return bedtime_tpe.astimezone(timezone.utc)


def estimate(date: str) -> dict:
    today = _load_json(date)
    if not today:
        return {"error": f"找不到 {date}.json"}

    yesterday_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = _load_json(yesterday_date)

    dto = ((today.get("sleep") or {}).get("dailySleepDTO")) or {}
    sleep_start_gmt_ms = dto.get("sleepStartTimestampGMT")
    if not sleep_start_gmt_ms:
        return {"error": "JSON 內無 sleepStartTimestampGMT"}

    sleep_onset_utc = datetime.fromtimestamp(sleep_start_gmt_ms / 1000, tz=timezone.utc)
    sleep_onset_tpe = sleep_onset_utc.astimezone(TPE)
    search_floor = sleep_onset_utc - timedelta(minutes=SEARCH_WINDOW_MIN)

    # === 步數訊號 ===
    bins = _gather_steps_bins([today, yesterday])
    last_active_end = None
    for start_utc, end_utc, steps in bins:
        if end_utc > sleep_onset_utc or start_utc < search_floor:
            continue
        if steps >= STEPS_ACTIVE_MIN:
            if last_active_end is None or end_utc > last_active_end:
                last_active_end = end_utc

    # === 壓力訊號 ===
    samples = _gather_stress_samples([today, yesterday])
    last_high_stress = None
    for ts_utc, val in samples:
        if ts_utc > sleep_onset_utc or ts_utc < search_floor:
            continue
        if val >= STRESS_HIGH_MIN:
            if last_high_stress is None or ts_utc > last_high_stress:
                last_high_stress = ts_utc

    # === HR 訊號 ===
    hr_samples = _gather_hr_samples([today, yesterday])
    sleep_baseline_end = sleep_onset_utc + timedelta(minutes=SLEEP_BASELINE_MIN)
    baseline_vals = [v for t, v in hr_samples if sleep_onset_utc <= t <= sleep_baseline_end]
    last_high_hr = None
    hr_baseline = None
    if len(baseline_vals) >= 5:
        baseline_vals.sort()
        hr_baseline = baseline_vals[len(baseline_vals) // 2]
        hr_threshold = hr_baseline + HR_AWAKE_DELTA_BPM
        for ts_utc, val in hr_samples:
            if ts_utc > sleep_onset_utc or ts_utc < search_floor:
                continue
            if val >= hr_threshold:
                if last_high_hr is None or ts_utc > last_high_hr:
                    last_high_hr = ts_utc

    # === 手動覆寫（最高優先）===
    override_utc = _read_manual_override(date, sleep_onset_tpe)

    candidates = [c for c in (last_active_end, last_high_stress, last_high_hr) if c is not None]

    if not candidates and not override_utc:
        return {
            "date": date,
            "sleep_onset_local": sleep_onset_tpe.strftime("%H:%M"),
            "sleep_onset_utc_ms": sleep_start_gmt_ms,
            "bedtime_est_local": None,
            "latency_min": None,
            "latency_min_lower": None,
            "latency_min_upper": None,
            "quality": "no_signal",
            "note": "前 180 分鐘無步數/壓力/HR 訊號，無法回推",
        }

    # 雙估算
    bedtime_lower_utc = max(candidates) if candidates else None  # 樂觀：取最晚清醒訊號
    bedtime_upper_utc = last_active_end if last_active_end else (
        max(candidates) if candidates else None
    )  # 悲觀：以步數為準（最可靠的「肯定醒著」訊號）

    def _to_lat(bt):
        if bt is None:
            return None
        v = round((sleep_onset_utc - bt).total_seconds() / 60)
        return max(0, min(v, LATENCY_MAX_MIN))

    lat_lower = _to_lat(bedtime_lower_utc)
    lat_upper = _to_lat(bedtime_upper_utc)

    # 確保 upper >= lower（極少情況：HR 訊號比 steps 還早，那 upper 用 lower）
    if lat_upper is not None and lat_lower is not None and lat_upper < lat_lower:
        lat_upper = lat_lower
        bedtime_upper_utc = bedtime_lower_utc

    # 手動覆寫：優先以使用者輸入為準
    source = "estimated"
    if override_utc:
        bedtime_utc = override_utc
        latency_min = _to_lat(override_utc)
        source = "manual_override"
        quality = "manual"
        note_parts = []
    else:
        # 預設展示 = mid-point（lower 與 upper 平均）若有 wide range；否則 lower
        if lat_lower is not None and lat_upper is not None and (lat_upper - lat_lower) > WIDE_RANGE_MIN:
            latency_min = lat_lower  # 顯示樂觀值但標 wide_range
            bedtime_utc = bedtime_lower_utc
            quality = "wide_range"
        else:
            latency_min = lat_lower if lat_lower is not None else lat_upper
            bedtime_utc = bedtime_lower_utc if bedtime_lower_utc else bedtime_upper_utc
            quality = "ok"
        note_parts = []
        if lat_lower is not None and lat_upper is not None and (lat_upper - lat_lower) > WIDE_RANGE_MIN:
            note_parts.append(f"HR/步數估算差 {lat_upper - lat_lower} 分，無法區分躺床清醒")
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
        "latency_min_lower": lat_lower,
        "latency_min_upper": lat_upper,
        "source": source,
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
    print(f"  上床時間：       {result['bedtime_est_local'] or '—'}  ({result.get('source')})")
    lo, hi = result.get("latency_min_lower"), result.get("latency_min_upper")
    if lo is not None and hi is not None and lo != hi:
        print(f"  入睡 latency：   {result['latency_min']} 分（範圍 {lo}–{hi} 分）")
    else:
        print(f"  入睡 latency：   {result['latency_min'] if result['latency_min'] is not None else '—'} 分")
    sig = result.get("signals") or {}
    hr_b = sig.get("hr_baseline_bpm")
    print(f"  訊號：HR {sig.get('last_high_hr_local') or '—'}（baseline {hr_b or '—'} bpm）"
          f"｜活動 bin 終止 {sig.get('last_active_end_local') or '—'}"
          f"｜高壓力 {sig.get('last_high_stress_local') or '—'}")
    print(f"  品質：{result['quality']}")
    if result.get("note"):
        print(f"  備註：{result['note']}")


if __name__ == "__main__":
    main()
