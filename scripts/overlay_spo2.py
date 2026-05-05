#!/usr/bin/env python3
"""SpO2 多晚疊圖：將指定日期的夜間 SpO2 曲線在同一時間軸疊放。

每日依輸入順序套用彩虹色（紅橙黃綠藍紫），方便逐線辨識。

用法：
    python scripts/overlay_spo2.py 2026-05-01 2026-05-02 2026-05-03 2026-05-04 2026-05-05
"""
import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
TPE = timezone(timedelta(hours=8))


def parse_ts(s):
    return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc).astimezone(TPE)


def load_epochs(date):
    p = DATA_DIR / f"{date}.json"
    if not p.exists():
        return None, None, None
    data = json.loads(p.read_text())
    sleep = data.get("sleep") or {}
    epochs = sleep.get("wellnessEpochSPO2DataDTOList") or []
    if not epochs:
        return None, None, None
    epochs.sort(key=lambda e: e["epochTimestamp"])
    dto = sleep.get("dailySleepDTO") or {}
    sleep_start_ms = dto.get("sleepStartTimestampGMT")
    sleep_start = (datetime.fromtimestamp(sleep_start_ms / 1000, tz=timezone.utc).astimezone(TPE)
                   if sleep_start_ms else None)
    return epochs, sleep.get("wellnessSpO2SleepSummaryDTO") or {}, sleep_start


RAINBOW = [
    ("#d7301f", "紅"),
    ("#f17c1f", "橙"),
    ("#d4b500", "黃"),
    ("#2ca02c", "綠"),
    ("#1f77b4", "藍"),
    ("#7b3fa6", "紫"),
]


def severity_tier(lowest):
    if lowest is None: return "—"
    if lowest < 80: return "重度"
    if lowest < 85: return "中度"
    if lowest < 88: return "紅旗"
    return "正常"


def find_events(epochs, threshold=90, gap_tolerance_min=2):
    events, cur = [], None
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
    ev["duration_min"] = int((ev["end"] - ev["start"]).total_seconds() / 60 + 1)
    ev["min"] = min(ev["vals"])
    return ev


def to_clock_dt(ts, anchor_date):
    """將 datetime 對齊到同一個基準日，僅保留時間部分（跨午夜的 22:00 → anchor_date，01:00 → anchor_date+1）。"""
    base = anchor_date
    if ts.hour < 12:
        base = anchor_date + timedelta(days=1)
    return ts.replace(year=base.year, month=base.month, day=base.day)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dates", nargs="+", help="YYYY-MM-DD 列表")
    ap.add_argument("--out", default=None, help="輸出 PNG 路徑")
    ap.add_argument("--elapsed", action="store_true",
                    help="X 軸改為睡眠經過時間（h），0 = sleepStart")
    args = ap.parse_args()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib import rcParams
    rcParams["font.sans-serif"] = ["Microsoft JhengHei", "PingFang TC", "Heiti TC",
                                    "Noto Sans CJK TC", "Arial Unicode MS", "DejaVu Sans"]
    rcParams["axes.unicode_minus"] = False

    anchor = datetime(2000, 1, 1, tzinfo=TPE)

    fig, ax = plt.subplots(figsize=(15, 6))

    summaries = []
    for i, date in enumerate(args.dates):
        epochs, summary, sleep_start = load_epochs(date)
        if not epochs:
            print(f"[skip] {date}：無 epoch 資料")
            continue
        if args.elapsed:
            if sleep_start is None:
                print(f"[skip] {date}：無 sleepStart")
                continue
            times = [(parse_ts(e["epochTimestamp"]) - sleep_start).total_seconds() / 3600
                     for e in epochs]
        else:
            times = [to_clock_dt(parse_ts(e["epochTimestamp"]), anchor) for e in epochs]
        vals = [e.get("spo2Reading") for e in epochs]
        valid = [v for v in vals if v is not None]
        lowest = min(valid) if valid else None
        avg = summary.get("averageSPO2")
        color, color_name = RAINBOW[i % len(RAINBOW)]
        tier = severity_tier(lowest)
        label = f"{color_name}  {date}  Low {lowest}%  Avg {avg}%  ({tier})"
        ax.plot(times, vals, color=color, linewidth=1.6, alpha=0.9, label=label, zorder=3)
        # 每日曲線下 < 90% 區段以該日色填滿（仿 5/1 單日圖標法）
        below = [v is not None and v < 90 for v in vals]
        ax.fill_between(times, vals, 90, where=below, interpolate=False,
                        color=color, alpha=0.30, zorder=2)
        # 標註該日 desat events（min < 88 的事件，仿單日圖 xx% N分）
        for ev in find_events(epochs):
            if ev["min"] >= 88:
                continue
            mid = ev["start"] + (ev["end"] - ev["start"]) / 2
            if args.elapsed:
                x_ev = (mid - sleep_start).total_seconds() / 3600
            else:
                x_ev = to_clock_dt(mid, anchor)
            xy = (x_ev, ev["min"])
            ax.annotate(f"{ev['min']}% {ev['duration_min']}分",
                        xy=xy, xytext=(0, -14), textcoords="offset points",
                        fontsize=7, ha="center", color=color, fontweight="bold",
                        zorder=4,
                        bbox=dict(boxstyle="round,pad=0.18", fc="white",
                                  ec=color, lw=0.6, alpha=0.85))
        summaries.append((date, lowest, avg, color_name, tier))

    ax.axhline(90, color="#cc8400", linestyle="--", linewidth=0.9, alpha=0.8, label="OSA 閾值 90%")
    ax.axhline(88, color="#cc3a1f", linestyle="--", linewidth=0.8, alpha=0.7, label="紅旗 88%")
    ax.axhline(80, color="#7a0a0a", linestyle="--", linewidth=0.8, alpha=0.7, label="重度 80%")

    ax.set_ylabel("SpO2 (%)")
    ax.set_ylim(70, 100)
    ax.grid(alpha=0.3)
    if args.elapsed:
        ax.set_xlabel("睡眠經過時間 (h)，0 = sleepStart")
        ax.set_xlim(0, 8)
        ax.set_xticks(range(0, 9))
        title_suffix = "（X 軸：睡眠經過時間 0–8h）"
    else:
        ax.set_xlabel("時間（Asia/Taipei，跨夜對齊）")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=TPE))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        title_suffix = "（每日獨立色：紅橙黃綠藍紫）"
        fig.autofmt_xdate()
    ax.set_title(f"夜間 SpO2 疊圖 — {args.dates[0]} ~ {args.dates[-1]}{title_suffix}", pad=10)
    ax.legend(loc="lower right", fontsize=8, framealpha=0.92)
    fig.tight_layout()

    suffix = "_elapsed" if args.elapsed else ""
    out = Path(args.out) if args.out else (ROOT / "reviews" / "daily" / "spo2" /
                                            f"spo2_overlay_{args.dates[0]}_to_{args.dates[-1][-5:]}{suffix}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=120)
    print(f"疊圖已存：{out}")
    print()
    print(f"{'色':<3} {'日期':<12} {'最低':>5} {'平均':>5}  分級")
    for d, low, avg, cname, tier in summaries:
        print(f"{cname:<3} {d}  {low:>4}%  {avg:>4}%  {tier}")


if __name__ == "__main__":
    main()
