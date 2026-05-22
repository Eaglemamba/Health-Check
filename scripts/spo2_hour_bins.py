#!/usr/bin/env python3
"""SpO2 × Sleep Stage 小時分箱分析（5/1-5/5）

每晚以 sleepStart 為 0h，分箱 0-1, 1-2, ..., 7-8h：
  - SpO2 avg / min / 事件數 (<90)
  - 該時段主導 sleep stage（Garmin sleepLevels: 0=deep, 1=light, 2=REM, 3=awake）

輸出：跨晚彙總表 + 系統性偏弱時段識別。
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
TPE = timezone(timedelta(hours=8))
STAGE_NAME = {0: "Deep", 1: "Light", 2: "REM", 3: "Awake"}


def parse_ts(s):
    return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc)


def load_night(date):
    p = next(iter(DATA_DIR.rglob(f"{date}.json")), DATA_DIR / f"{date}.json")
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    s = d.get("sleep") or {}
    epochs = s.get("wellnessEpochSPO2DataDTOList") or []
    levels = s.get("sleepLevels") or []
    dto = s.get("dailySleepDTO") or {}
    if not epochs or not dto.get("sleepStartTimestampGMT"):
        return None
    sleep_start = datetime.fromtimestamp(dto["sleepStartTimestampGMT"] / 1000, tz=timezone.utc)
    return {"date": date, "epochs": epochs, "levels": levels, "sleep_start": sleep_start, "dto": dto}


def stage_at(t, levels):
    for lv in levels:
        st = parse_ts(lv["startGMT"])
        en = parse_ts(lv["endGMT"])
        if st <= t < en:
            return int(lv.get("activityLevel", -1))
    return -1


def analyze(night, n_bins=8):
    sleep_start = night["sleep_start"]
    bins = [defaultdict(list) for _ in range(n_bins)]
    stage_time = [defaultdict(int) for _ in range(n_bins)]

    for e in night["epochs"]:
        ts = parse_ts(e["epochTimestamp"])
        h = (ts - sleep_start).total_seconds() / 3600
        if h < 0 or h >= n_bins:
            continue
        bi = int(h)
        v = e.get("spo2Reading")
        if v is not None:
            bins[bi]["vals"].append(v)
        stg = stage_at(ts, night["levels"])
        if stg >= 0:
            stage_time[bi][stg] += 60

    rows = []
    for i in range(n_bins):
        vals = bins[i].get("vals", [])
        if not vals:
            rows.append(None)
            continue
        below = sum(1 for v in vals if v < 90)
        below88 = sum(1 for v in vals if v < 88)
        below80 = sum(1 for v in vals if v < 80)
        st = stage_time[i]
        if st:
            top = sorted(st.items(), key=lambda x: -x[1])
            stage_str = "+".join(STAGE_NAME.get(s, "?") for s, _ in top[:2])
        else:
            stage_str = "—"
        rows.append({
            "bin": f"{i}-{i+1}h",
            "n": len(vals),
            "avg": sum(vals) / len(vals),
            "min": min(vals),
            "below90": below,
            "below88": below88,
            "below80": below80,
            "stage": stage_str,
        })
    return rows


def main():
    dates = sys.argv[1:] or ["2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05"]
    all_rows = {}
    for d in dates:
        n = load_night(d)
        if not n:
            print(f"[skip] {d}")
            continue
        all_rows[d] = analyze(n)

    print(f"\n{'='*98}")
    print("  每晚 × 每小時 SpO2 × 主導睡眠 stage")
    print(f"{'='*98}")
    print(f"{'時段':<5} {'avg':>5} {'min':>5} {'<90':>4} {'<88':>4} {'<80':>4}  {'stage':<12}")
    for d in dates:
        if d not in all_rows: continue
        print(f"\n— {d} —")
        for r in all_rows[d]:
            if r is None:
                print("  (no data)")
                continue
            print(f"{r['bin']:<5} {r['avg']:>5.1f} {r['min']:>5} "
                  f"{r['below90']:>4} {r['below88']:>4} {r['below80']:>4}  {r['stage']:<12}")

    # 跨晚彙總：哪個時段最弱
    print(f"\n{'='*98}")
    print("  跨 5 晚 — 每小時系統性偏弱程度（SpO2<90 累計分數 / 平均最低 / 平均 SpO2）")
    print(f"{'='*98}")
    print(f"{'時段':<5}  {'總<90分':>7}  {'平均最低':>7}  {'平均SpO2':>8}  {'重度晚數(<80)':>13}  {'常見stage':<14}")
    summary = []
    for i in range(8):
        bin_rows = [all_rows[d][i] for d in dates if d in all_rows and all_rows[d][i]]
        if not bin_rows:
            continue
        total_b90 = sum(r["below90"] for r in bin_rows)
        avg_min = sum(r["min"] for r in bin_rows) / len(bin_rows)
        avg_avg = sum(r["avg"] for r in bin_rows) / len(bin_rows)
        severe_nights = sum(1 for r in bin_rows if r["below80"] > 0)
        stages = defaultdict(int)
        for r in bin_rows:
            for s in r["stage"].split("+"):
                stages[s] += 1
        common_stage = "+".join(s for s, _ in sorted(stages.items(), key=lambda x: -x[1])[:2])
        print(f"{i}-{i+1}h  {total_b90:>7}  {avg_min:>6.1f}%  {avg_avg:>7.1f}%  "
              f"{severe_nights:>11}/{len(bin_rows)}   {common_stage:<14}")
        summary.append((i, total_b90, avg_min, avg_avg, severe_nights))

    if summary:
        worst = max(summary, key=lambda x: x[1])
        deepest = min(summary, key=lambda x: x[2])
        print(f"\n>> SpO2<90 總分鐘數最多：{worst[0]}-{worst[0]+1}h（{worst[1]} 分）")
        print(f">> 平均最低 SpO2 最深：{deepest[0]}-{deepest[0]+1}h（{deepest[2]:.1f}%）")


if __name__ == "__main__":
    main()
