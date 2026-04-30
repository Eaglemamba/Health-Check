#!/usr/bin/env python3
"""
SpO2 Desaturation Event 分析（從 wellnessEpochSPO2DataDTOList 擷取）

產出：
- summary 表（最近 N 晚 T90 / 最長 event / 最深 event）
- per-night event 清單（適合插入 daily.md）
- 單晚 chart（matplotlib，標出 desat 區段）

用法：
    python scripts/analyze_spo2_desats.py --summary 14
    python scripts/analyze_spo2_desats.py --night 2026-05-01
    python scripts/analyze_spo2_desats.py --chart 2026-05-01
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
TPE = timezone(timedelta(hours=8))
THRESHOLD = 90  # SpO2 < 90% 視為 desat


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc).astimezone(TPE)


def load_epochs(date: str):
    """回傳 (epochs_sorted, summary_dict) 或 (None, None)。"""
    p = DATA_DIR / f"{date}.json"
    if not p.exists():
        return None, None
    data = json.loads(p.read_text())
    sleep = data.get("sleep") or {}
    epochs = sleep.get("wellnessEpochSPO2DataDTOList") or []
    if not epochs:
        return None, None
    epochs.sort(key=lambda e: e["epochTimestamp"])
    summary = sleep.get("wellnessSpO2SleepSummaryDTO") or {}
    return epochs, summary


def find_events(epochs, threshold=THRESHOLD, gap_tolerance_min=2):
    """回傳 desat events 列表，每筆 {start, end, duration_min, min, mean, vals}."""
    events = []
    cur = None
    for e in epochs:
        ts = parse_ts(e["epochTimestamp"])
        val = e.get("spo2Reading")
        if val is None:
            continue
        if val < threshold:
            if cur is None:
                cur = {"start": ts, "end": ts, "vals": [val]}
            else:
                gap = (ts - cur["end"]).total_seconds() / 60
                if gap > gap_tolerance_min:
                    events.append(_finalize(cur))
                    cur = {"start": ts, "end": ts, "vals": [val]}
                else:
                    cur["end"] = ts
                    cur["vals"].append(val)
        else:
            if cur is not None:
                events.append(_finalize(cur))
                cur = None
    if cur is not None:
        events.append(_finalize(cur))
    return events


def _finalize(ev):
    duration = (ev["end"] - ev["start"]).total_seconds() / 60 + 1
    ev["duration_min"] = int(duration)
    ev["min"] = min(ev["vals"])
    ev["mean"] = sum(ev["vals"]) / len(ev["vals"])
    return ev


def severity(val):
    if val is None: return "—"
    if val < 80: return "🔴 重度"
    if val < 85: return "🟠 中度"
    if val < 88: return "🟡 紅旗"
    if val < 90: return "🟢 邊緣"
    return "✅ 正常"


def t90(epochs, threshold=90):
    valid = [e for e in epochs if e.get("spo2Reading") is not None]
    if not valid:
        return 0.0, 0, 0
    below = sum(1 for e in valid if e["spo2Reading"] < threshold)
    return below / len(valid) * 100, below, len(valid)


def cmd_night(date: str):
    epochs, summary = load_epochs(date)
    if not epochs:
        print(f"[skip] {date}：無 epoch 資料")
        return
    events = find_events(epochs)
    pct, below, total = t90(epochs)
    sleep_low = summary.get("lowestSPO2")
    sleep_avg = summary.get("averageSPO2")
    print(f"### {date}")
    print(f"睡眠平均 {sleep_avg}%｜瞬間最低 {sleep_low}%（手錶秒級聚合）")
    print(f"睡眠分鐘數 ~{total}｜SpO2 < 90% 累計 {below} 分｜T90 ≈ {pct:.1f}%")
    print(f"Desat events: {len(events)} 段")
    if events:
        print()
        print(f"  {'時段':<14} {'長':>4} {'最低':>5} {'平均':>5}  分級")
        for ev in events:
            sev = severity(ev["min"])
            print(f"  {ev['start'].strftime('%H:%M')}–{ev['end'].strftime('%H:%M')}  "
                  f"{ev['duration_min']:>3}分  {ev['min']:>3}%  {ev['mean']:>4.0f}%  {sev}")


def cmd_summary(days: int):
    files = sorted(DATA_DIR.glob("*.json"))[-days:]
    print(f"{'='*82}")
    print(f"  近 {len(files)} 晚 SpO2 Desat 摘要（threshold < 90%）")
    print(f"{'='*82}\n")
    print(f"{'日期':<12} {'TST 分':>6} {'T90 %':>6} {'累計分':>6}  {'最長':>5} {'最深':>5}  events  分級")
    print("-" * 82)
    for f in files:
        date = f.stem
        epochs, summary = load_epochs(date)
        if not epochs:
            continue
        events = find_events(epochs)
        pct, below, total = t90(epochs)
        longest = max((e["duration_min"] for e in events), default=0)
        deepest = min((e["min"] for e in events), default=None)
        sev = severity(deepest)
        print(f"{date}  {total:>5}  {pct:>5.1f}  {below:>5}   {longest:>3}分  "
              f"{deepest if deepest is not None else '—':>4}%  {len(events):>5}   {sev}")


def cmd_chart(date: str, out: Path = None):
    """產生單晚 SpO2 epoch chart，標出 desat 區段。"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib import rcParams
        # macOS Chinese font fallback
        rcParams["font.sans-serif"] = ["PingFang TC", "PingFang SC", "Heiti TC",
                                       "Hiragino Sans GB", "Arial Unicode MS",
                                       "Noto Sans CJK TC", "DejaVu Sans"]
        rcParams["axes.unicode_minus"] = False
    except ImportError:
        print("需先安裝 matplotlib")
        return

    epochs, summary = load_epochs(date)
    if not epochs:
        print(f"[skip] {date}：無 epoch 資料")
        return

    times = [parse_ts(e["epochTimestamp"]) for e in epochs]
    vals = [e["spo2Reading"] for e in epochs]

    events = find_events(epochs)
    pct, below, total = t90(epochs)

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(times, vals, color="#2c7fb8", linewidth=1.0)
    ax.fill_between(times, vals, 90, where=[v is not None and v < 90 for v in vals],
                     interpolate=False, alpha=0.3, color="#fdae6b")

    # 標註 desat events
    for ev in events:
        if ev["min"] < 85:
            ax.annotate(f"{ev['min']}%\n{ev['duration_min']}分",
                        xy=(ev["start"], ev["min"]),
                        xytext=(0, -20), textcoords="offset points",
                        fontsize=8, ha="center",
                        color="darkred" if ev["min"] < 80 else "darkorange")

    ax.axhline(90, color="orange", linestyle="--", linewidth=0.8, label="OSA threshold 90%")
    ax.axhline(88, color="red", linestyle="--", linewidth=0.6, alpha=0.6, label="紅旗 88%")
    ax.axhline(80, color="darkred", linestyle="--", linewidth=0.6, alpha=0.6, label="重度 80%")

    ax.set_ylabel("SpO2 (%)")
    ax.set_xlabel("Time (Asia/Taipei)")
    sleep_low = summary.get("lowestSPO2")
    sleep_avg = summary.get("averageSPO2")
    ax.set_title(f"夜間 SpO2 — {date}  |  Avg {sleep_avg}%  Lowest {sleep_low}%  T90 {pct:.1f}%  ({len(events)} events)")
    ax.set_ylim(70, 100)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    fig.autofmt_xdate()
    fig.tight_layout()

    out = out or (ROOT / "reviews" / f"spo2_desat_{date}.png")
    fig.savefig(out, dpi=110)
    print(f"圖表已存：{out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", type=int, metavar="N", help="近 N 晚摘要")
    ap.add_argument("--night", help="單晚詳細 events，YYYY-MM-DD")
    ap.add_argument("--chart", help="產生單晚 chart，YYYY-MM-DD")
    args = ap.parse_args()

    if args.summary:
        cmd_summary(args.summary)
    if args.night:
        cmd_night(args.night)
    if args.chart:
        cmd_chart(args.chart)
    if not (args.summary or args.night or args.chart):
        ap.print_help()


if __name__ == "__main__":
    main()
