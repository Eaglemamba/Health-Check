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
    python scripts/analyze_spo2_desats.py --overlay 2026-05-06   # rolling 7-day overlay
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
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=TPE))
    fig.autofmt_xdate()
    fig.tight_layout()

    out = out or (ROOT / "reviews" / "daily" / "spo2" / f"spo2_desat_{date}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=110)
    print(f"圖表已存：{out}")


def cmd_trend(days: int = 9999, out: Path = None):
    """多日趨勢圖：每天一個 x 點，顯示 lowest / avg / T90 / longest event。"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib import rcParams
        rcParams["font.sans-serif"] = ["PingFang TC", "PingFang SC", "Heiti TC",
                                       "Hiragino Sans GB", "Arial Unicode MS",
                                       "Noto Sans CJK TC", "DejaVu Sans"]
        rcParams["axes.unicode_minus"] = False
    except ImportError:
        print("需先安裝 matplotlib")
        return

    files = sorted(DATA_DIR.glob("*.json"))[-days:]
    rows = []
    for f in files:
        date = f.stem
        epochs, summary = load_epochs(date)
        if not epochs or not summary:
            continue
        events = find_events(epochs)
        pct, below, total = t90(epochs)
        longest = max((e["duration_min"] for e in events), default=0)
        # TST 從 dailySleepDTO 取
        data = json.loads(f.read_text())
        dto = (data.get("sleep") or {}).get("dailySleepDTO") or {}
        tst_min = (dto.get("sleepTimeSeconds") or 0) / 60
        rows.append({
            "date": datetime.strptime(date, "%Y-%m-%d").date(),
            "lowest": summary.get("lowestSPO2"),
            "avg": summary.get("averageSPO2"),
            "t90": pct,
            "longest": longest,
            "events": len(events),
            "tst": tst_min,
        })

    if not rows:
        print("無資料")
        return

    dates = [r["date"] for r in rows]
    lowest = [r["lowest"] for r in rows]
    avg = [r["avg"] for r in rows]
    t90s = [r["t90"] for r in rows]
    longest_ev = [r["longest"] for r in rows]
    tsts = [r["tst"] / 60 for r in rows]  # 小時
    # ODI 代理（AHI proxy）= 每睡眠小時 desat events 數
    odi = [r["events"] / (r["tst"] / 60) if r["tst"] > 0 else 0 for r in rows]

    def color_t90(v):
        if v >= 15: return "#d7301f"
        if v >= 10: return "#fc8d59"
        if v >= 5:  return "#fdcc8a"
        return "#74c476"

    def color_dur(v):
        if v >= 20: return "#d7301f"
        if v >= 15: return "#fc8d59"
        if v >= 10: return "#fdcc8a"
        return "#74c476"

    def color_tst(v):
        # 反向：時數越短越紅
        if v < 6:   return "#d7301f"
        if v < 7:   return "#fc8d59"
        if v < 7.5: return "#fdcc8a"
        return "#74c476"

    def color_odi(v):
        # AASM 嚴重度切點
        if v >= 30: return "#d7301f"
        if v >= 15: return "#fc8d59"
        if v >= 5:  return "#fdcc8a"
        return "#74c476"

    width = max(16, len(dates) * 0.32)
    fig, axes = plt.subplots(5, 1, figsize=(width, 20),
                              sharex=True, gridspec_kw={"height_ratios": [3, 2, 2, 2, 2]})

    # Panel 1: SpO2 lowest + avg
    ax = axes[0]
    ax.plot(dates, avg, color="#2c7fb8", marker="o", markersize=6, linewidth=1.5,
            label="夜間平均 SpO2")
    ax.plot(dates, lowest, color="#d7301f", marker="v", markersize=7, linewidth=1.5,
            label="夜間最低 SpO2")
    # 標出每點的最低值
    for d, v in zip(dates, lowest):
        if v is not None and v < 85:
            ax.annotate(f"{v}", xy=(d, v), xytext=(0, -14),
                        textcoords="offset points", ha="center", fontsize=7,
                        color="darkred" if v < 80 else "darkorange")
    ax.axhline(90, color="orange", linestyle="--", linewidth=1.0, alpha=0.7, label="OSA 閾值 90%")
    ax.axhline(88, color="red", linestyle="--", linewidth=0.8, alpha=0.5, label="紅旗 88%")
    ax.axhline(80, color="darkred", linestyle="--", linewidth=0.8, alpha=0.5, label="重度 80%")
    ax.set_ylabel("SpO2 (%)", fontsize=11)
    ax.set_ylim(70, 100)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize=9, frameon=False)
    ax.set_title(f"夜間 SpO2 / OSA 趨勢 — {dates[0]} 至 {dates[-1]}（共 {len(dates)} 晚）",
                 fontsize=13, pad=12)

    # Panel 2: T90 bar
    ax = axes[1]
    colors = [color_t90(v) for v in t90s]
    ax.bar(dates, t90s, color=colors, edgecolor="#333", linewidth=0.6, width=0.8)
    ax.axhline(5, color="goldenrod", linestyle=":", linewidth=1.0, alpha=0.6, label="輕度 5%")
    ax.axhline(10, color="orange", linestyle=":", linewidth=1.0, alpha=0.6, label="中度 10%")
    ax.axhline(15, color="red", linestyle=":", linewidth=1.0, alpha=0.6, label="重度 15%")
    ax.set_ylabel("T90 (%)\nSpO2<90% 時間佔比", fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="upper right", fontsize=8, ncol=3)

    # Panel 3: Longest event bar
    ax = axes[2]
    colors = [color_dur(v) for v in longest_ev]
    ax.bar(dates, longest_ev, color=colors, edgecolor="#333", linewidth=0.6, width=0.8)
    ax.axhline(10, color="goldenrod", linestyle=":", linewidth=1.0, alpha=0.6, label="10 分")
    ax.axhline(15, color="orange", linestyle=":", linewidth=1.0, alpha=0.6, label="15 分")
    ax.axhline(20, color="red", linestyle=":", linewidth=1.0, alpha=0.6, label="20 分")
    ax.set_ylabel("最長 desat event\n（連續 SpO2<90% 分鐘）", fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="upper right", fontsize=8, ncol=3)

    # Panel 4: ODI (AHI proxy) = events per sleep-hour
    ax = axes[3]
    colors = [color_odi(v) for v in odi]
    ax.bar(dates, odi, color=colors, edgecolor="#333", linewidth=0.6, width=0.8)
    ax.axhline(5,  color="goldenrod", linestyle=":", linewidth=1.0, alpha=0.6, label="輕度 ≥5")
    ax.axhline(15, color="orange",    linestyle=":", linewidth=1.0, alpha=0.6, label="中度 ≥15")
    ax.axhline(30, color="red",       linestyle=":", linewidth=1.0, alpha=0.6, label="重度 ≥30")
    for d, v in zip(dates, odi):
        if v >= 5:
            ax.annotate(f"{v:.1f}", xy=(d, v), xytext=(0, 2),
                        textcoords="offset points", ha="center", fontsize=6,
                        color="darkred" if v >= 15 else "#444")
    ax.set_ylabel("ODI 代理 (events/h)\nAHI proxy (非 PSG 診斷)", fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="upper right", fontsize=8, ncol=3)
    # 警示：Garmin 60s epoch 嚴重低估事件數
    ax.text(0.01, 0.95,
            "[!] Garmin 60s 取樣會嚴重低估事件數（PSG 1 Hz）；真實 AHI 推估約 5-10× 此值",
            transform=ax.transAxes, fontsize=8, color="darkred",
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", fc="#fff3cd", ec="#d7301f", alpha=0.9))

    # Panel 5: TST (Total Sleep Time)
    ax = axes[4]
    colors = [color_tst(v) for v in tsts]
    ax.bar(dates, tsts, color=colors, edgecolor="#333", linewidth=0.6, width=0.8)
    ax.axhline(6,   color="red",       linestyle=":", linewidth=1.0, alpha=0.6, label="底線 6h")
    ax.axhline(7,   color="orange",    linestyle=":", linewidth=1.0, alpha=0.6, label="目標 7h")
    ax.axhline(7.5, color="goldenrod", linestyle=":", linewidth=1.0, alpha=0.6, label="理想 7.5h")
    # 在每根 bar 上方標出時數
    for d, v in zip(dates, tsts):
        ax.annotate(f"{v:.1f}", xy=(d, v), xytext=(0, 2),
                    textcoords="offset points", ha="center", fontsize=6,
                    color="darkred" if v < 6 else "#444")
    ax.set_ylabel("TST 總睡眠時間 (h)\nGarmin dailySleepDTO", fontsize=11)
    ax.set_ylim(0, max(10, max(tsts) + 0.5))
    ax.set_xlabel("日期（每根 bar = 一晚睡眠）", fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="upper right", fontsize=8, ncol=3)

    # Date formatting — 每天一個 tick（放在最底層 panel）
    ax.set_xticks(dates)
    ax.set_xticklabels([d.strftime("%m-%d") for d in dates], rotation=60, ha="right", fontsize=8)

    fig.tight_layout()

    out = out or (ROOT / "reviews" / "daily" / "spo2" / "spo2_desat_trend.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=110)
    print(f"趨勢圖已存：{out}")

    # 摘要統計
    avg_lowest = sum(lowest) / len(lowest)
    avg_t90 = sum(t90s) / len(t90s)
    avg_longest = sum(longest_ev) / len(longest_ev)
    nights_red_t90 = sum(1 for v in t90s if v >= 10)
    nights_red_event = sum(1 for v in longest_ev if v >= 15)
    nights_below_88 = sum(1 for v in lowest if v < 88)
    nights_below_80 = sum(1 for v in lowest if v < 80)
    print()
    print(f"=== {len(rows)} 晚統計 ===")
    print(f"平均最低 SpO2：{avg_lowest:.1f}%")
    print(f"平均 T90：{avg_t90:.1f}%")
    print(f"平均最長 event：{avg_longest:.1f} 分")
    print(f"最低 SpO2 < 88%：{nights_below_88}/{len(rows)} 晚（{nights_below_88/len(rows)*100:.0f}%）")
    print(f"最低 SpO2 < 80%：{nights_below_80}/{len(rows)} 晚（{nights_below_80/len(rows)*100:.0f}%）")
    print(f"T90 ≥ 10%（重度）：{nights_red_t90}/{len(rows)} 晚")
    print(f"最長 event ≥ 15 分（重度）：{nights_red_event}/{len(rows)} 晚")


def cmd_overlay(today_str: str, max_nights: int = 7):
    """多晚 SpO2 epoch 疊圖（x = 距入睡分鐘，y = SpO2）。

    Cycle 規則（檔名 spo2_overlay_{start}_to_{end}_elapsed.png）：
    - 無前檔：bootstrap，向前最多 max_nights 晚可用資料當 anchor
    - 前檔 < max_nights 晚：取代為 (start=old_start, end=today)
    - 前檔 = max_nights 晚：起新 cycle (start=today, end=today)，舊檔保留
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import rcParams
        rcParams["font.sans-serif"] = ["PingFang TC", "PingFang SC", "Heiti TC",
                                       "Hiragino Sans GB", "Arial Unicode MS",
                                       "Noto Sans CJK TC", "DejaVu Sans"]
        rcParams["axes.unicode_minus"] = False
    except ImportError:
        print("需先安裝 matplotlib")
        return

    from datetime import date as date_type
    spo2_dir = ROOT / "reviews" / "daily" / "spo2"
    spo2_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.strptime(today_str, "%Y-%m-%d").date()

    existing = sorted(spo2_dir.glob("spo2_overlay_*_to_*_elapsed.png"))
    new_start = None
    file_to_replace = None

    if existing:
        latest = existing[-1]
        parts = latest.stem.split("_")
        try:
            old_start = datetime.strptime(parts[2], "%Y-%m-%d").date()
            old_end = datetime.strptime(parts[4], "%Y-%m-%d").date()
        except (ValueError, IndexError):
            old_start = old_end = None

        if old_start and old_end:
            nights = (old_end - old_start).days + 1
            if old_end == today:
                new_start = old_start
                file_to_replace = latest
            elif nights < max_nights:
                new_start = old_start
                file_to_replace = latest
            else:
                new_start = today

    if new_start is None:
        new_start = today
        for back in range(max_nights - 1, -1, -1):
            cand = today - timedelta(days=back)
            if (DATA_DIR / f"{cand}.json").exists():
                new_start = cand
                break

    nights_to_plot = []
    cur = new_start
    while cur <= today:
        if (DATA_DIR / f"{cur}.json").exists():
            nights_to_plot.append(cur)
        cur += timedelta(days=1)

    if not nights_to_plot:
        print(f"[skip] {new_start} ~ {today} 無可用 epoch 資料")
        return

    fig, ax = plt.subplots(figsize=(14, 6))
    cmap = plt.get_cmap("viridis")
    n = len(nights_to_plot)

    legend_lines = []
    for i, d in enumerate(nights_to_plot):
        epochs, summary = load_epochs(str(d))
        if not epochs:
            continue
        t0 = parse_ts(epochs[0]["epochTimestamp"])
        xs = [(parse_ts(e["epochTimestamp"]) - t0).total_seconds() / 60 for e in epochs]
        ys = [e.get("spo2Reading") for e in epochs]
        is_today = (d == today)
        color = "#d7301f" if is_today else cmap(i / max(n - 1, 1) * 0.85)
        alpha = 1.0 if is_today else 0.55
        lw = 1.8 if is_today else 1.0
        nadir = summary.get("lowestSPO2") if summary else None
        avg = summary.get("averageSPO2") if summary else None
        pct, _, _ = t90(epochs)
        label = f"{d}  nadir {nadir}%  avg {avg}%  T90 {pct:.1f}%" + ("  ◀ today" if is_today else "")
        ax.plot(xs, ys, color=color, alpha=alpha, linewidth=lw, label=label)
        legend_lines.append(label)

    ax.axhline(90, color="orange", linestyle="--", linewidth=0.8, alpha=0.7, label="OSA 90%")
    ax.axhline(88, color="red", linestyle="--", linewidth=0.6, alpha=0.5, label="紅旗 88%")
    ax.axhline(80, color="darkred", linestyle="--", linewidth=0.6, alpha=0.5, label="重度 80%")

    ax.set_xlabel("距入睡時間 (分鐘)")
    ax.set_ylabel("SpO2 (%)")
    ax.set_ylim(70, 100)
    ax.grid(alpha=0.3)
    ax.set_title(f"多晚 SpO2 Overlay — {new_start} 至 {today}（{n} 晚，cycle 上限 {max_nights} 晚）")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.85)
    fig.tight_layout()

    out = spo2_dir / f"spo2_overlay_{new_start}_to_{today}_elapsed.png"
    if file_to_replace and file_to_replace != out and file_to_replace.exists():
        file_to_replace.unlink()
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print(f"Overlay 圖已存：{out}")
    print(f"涵蓋 {n} 晚（cycle 上限 {max_nights}），下一晚 {'起新 cycle' if n >= max_nights else '繼續延伸'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", type=int, metavar="N", help="近 N 晚文字摘要")
    ap.add_argument("--night", help="單晚詳細 events，YYYY-MM-DD")
    ap.add_argument("--chart", help="產生單晚 SpO2 chart，YYYY-MM-DD")
    ap.add_argument("--trend", type=int, nargs="?", const=9999, metavar="N",
                    help="多日趨勢圖（預設全部，N 限制最近幾天）")
    ap.add_argument("--overlay", help="多晚 SpO2 epoch 疊圖（rolling 7 晚），YYYY-MM-DD = 今日")
    args = ap.parse_args()

    if args.summary:
        cmd_summary(args.summary)
    if args.night:
        cmd_night(args.night)
    if args.chart:
        cmd_chart(args.chart)
    if args.trend is not None:
        cmd_trend(args.trend)
    if args.overlay:
        cmd_overlay(args.overlay)
    if not (args.summary or args.night or args.chart or args.trend is not None or args.overlay):
        ap.print_help()


if __name__ == "__main__":
    main()
