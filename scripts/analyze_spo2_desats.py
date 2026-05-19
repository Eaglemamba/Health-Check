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
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Windows cp950 → UTF-8 for unicode markers in stdout
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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
    data = json.loads(p.read_text(encoding="utf-8"))
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
    """產生單晚 SpO2 epoch chart，標出 desat 區段；若有 sleepLevels 則加上 hypnogram 條帶 + 階段背景色。"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib import rcParams
        from matplotlib.patches import Patch
        rcParams["font.sans-serif"] = ["Microsoft JhengHei", "PingFang TC", "PingFang SC",
                                       "Heiti TC", "Hiragino Sans GB", "Arial Unicode MS",
                                       "Noto Sans CJK TC", "DejaVu Sans"]
        rcParams["axes.unicode_minus"] = False
    except ImportError:
        print("需先安裝 matplotlib")
        return

    epochs, summary = load_epochs(date)
    if not epochs:
        print(f"[skip] {date}：無 epoch 資料")
        return

    # Load sleepLevels (hypnogram)
    p = DATA_DIR / f"{date}.json"
    levels = []
    if p.exists():
        try:
            sleep = json.loads(p.read_text(encoding="utf-8")).get("sleep") or {}
            levels = sleep.get("sleepLevels") or []
        except Exception:
            levels = []

    def _parse_gmt(s):
        return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc).astimezone(TPE)

    stage_color = {0.0: "#1f3a5f", 1.0: "#9ecae1", 2.0: "#d7301f", 3.0: "#777777"}
    stage_alpha_bg = {0.0: 0.08, 1.0: 0.04, 2.0: 0.15, 3.0: 0.10}
    stage_y = {0.0: 0, 1.0: 1, 2.0: 2, 3.0: 3}
    stage_name = {0.0: "Deep", 1.0: "Light", 2.0: "REM", 3.0: "Awake"}

    times = [parse_ts(e["epochTimestamp"]) for e in epochs]
    vals = [e["spo2Reading"] for e in epochs]

    events = find_events(epochs)
    pct, below, total = t90(epochs)

    if levels:
        fig, (ax_h, ax) = plt.subplots(2, 1, figsize=(14, 6.5), sharex=True,
                                         gridspec_kw={"height_ratios": [1, 3.5]})
        # Hypnogram strip
        for lv in levels:
            start = _parse_gmt(lv["startGMT"])
            end = _parse_gmt(lv["endGMT"])
            al = lv["activityLevel"]
            y = stage_y.get(al, 1)
            w_days = (end - start).total_seconds() / 86400.0
            ax_h.barh(y, w_days, left=mdates.date2num(start), height=0.85,
                      color=stage_color.get(al, "#888"), edgecolor="white", linewidth=0.5)
        ax_h.set_yticks([0, 1, 2])
        ax_h.set_yticklabels(["Deep", "Light", "REM"])
        ax_h.set_ylabel("分期")
        ax_h.grid(alpha=0.3, axis="x")
        ax_h.invert_yaxis()

        # Stage backgrounds on SpO2 panel
        for lv in levels:
            s_dt = _parse_gmt(lv["startGMT"])
            e_dt = _parse_gmt(lv["endGMT"])
            al = lv["activityLevel"]
            if al in stage_alpha_bg:
                ax.axvspan(s_dt, e_dt, color=stage_color[al], alpha=stage_alpha_bg[al], zorder=0)
    else:
        fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(times, vals, color="#222", linewidth=1.1, zorder=3)
    ax.fill_between(times, vals, 90, where=[v is not None and v < 90 for v in vals],
                     interpolate=False, alpha=0.3, color="#fdae6b", zorder=2)

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

    if levels:
        # Stage legend patches (compact, top-of-SpO2 panel)
        stage_legend = [
            Patch(facecolor=stage_color[0.0], alpha=0.35, label="Deep"),
            Patch(facecolor=stage_color[1.0], alpha=0.35, label="Light"),
            Patch(facecolor=stage_color[2.0], alpha=0.35, label="REM"),
        ]
        # Don't overwrite the main legend; add stage legend separately
        leg2 = ax.legend(handles=stage_legend, loc="upper right", fontsize=8, framealpha=0.85)
        ax.add_artist(leg2)

    # === 上床時間估算 + Sleep onset 標線 ===
    latency_text = ""
    try:
        from estimate_sleep_latency import estimate as estimate_latency
        est = estimate_latency(date)
        if est and "error" not in est:
            onset_ms = est.get("sleep_onset_utc_ms")
            bedtime_ms = est.get("bedtime_est_utc_ms")
            if onset_ms:
                t_onset = datetime.fromtimestamp(onset_ms / 1000, tz=timezone.utc).astimezone(TPE)
                ax.axvline(t_onset, color="#2c7fb8", linestyle="-", linewidth=1.2,
                           alpha=0.85, label=f"Sleep onset {t_onset.strftime('%H:%M')}")
            if bedtime_ms:
                t_bed = datetime.fromtimestamp(bedtime_ms / 1000, tz=timezone.utc).astimezone(TPE)
                ax.axvline(t_bed, color="#7b3294", linestyle=":", linewidth=1.2,
                           alpha=0.85, label=f"估算上床 {t_bed.strftime('%H:%M')}")
                if est.get("latency_min") is not None:
                    q = est.get("quality")
                    lo, hi = est.get("latency_min_lower"), est.get("latency_min_upper")
                    if lo is not None and hi is not None and lo != hi:
                        lat_disp = f"{lo}–{hi}分"
                    else:
                        lat_disp = f"{est['latency_min']}分"
                    tag = "" if q in ("ok", "manual") else f"·{q}"
                    latency_text = f"  |  Latency {lat_disp}{tag}"
    except Exception:
        pass

    ax.set_ylabel("SpO2 (%)")
    ax.set_xlabel("Time (Asia/Taipei)")
    sleep_low = summary.get("lowestSPO2")
    sleep_avg = summary.get("averageSPO2")
    title = f"夜間 SpO2 — {date}  |  Avg {sleep_avg}%  Lowest {sleep_low}%  T90 {pct:.1f}%  ({len(events)} events){latency_text}"
    if levels:
        ax_h.set_title(title)
    else:
        ax.set_title(title)
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
    try:
        from estimate_sleep_latency import estimate as estimate_latency
    except Exception:
        estimate_latency = None
    for f in files:
        date = f.stem
        epochs, summary = load_epochs(date)
        if not epochs or not summary:
            continue
        events = find_events(epochs)
        pct, below, total = t90(epochs)
        longest = max((e["duration_min"] for e in events), default=0)
        # TST 從 dailySleepDTO 取
        data = json.loads(f.read_text(encoding="utf-8"))
        dto = (data.get("sleep") or {}).get("dailySleepDTO") or {}
        tst_min = (dto.get("sleepTimeSeconds") or 0) / 60
        # Latency 估算
        latency_min = None
        latency_lo = None
        latency_hi = None
        latency_src = None
        if estimate_latency is not None:
            try:
                est = estimate_latency(date)
                if est and "error" not in est:
                    latency_min = est.get("latency_min")
                    latency_lo = est.get("latency_min_lower")
                    latency_hi = est.get("latency_min_upper")
                    latency_src = est.get("source")
            except Exception:
                pass
        rows.append({
            "date": datetime.strptime(date, "%Y-%m-%d").date(),
            "lowest": summary.get("lowestSPO2"),
            "avg": summary.get("averageSPO2"),
            "t90": pct,
            "longest": longest,
            "events": len(events),
            "tst": tst_min,
            "latency": latency_min,
            "latency_lo": latency_lo,
            "latency_hi": latency_hi,
            "latency_src": latency_src,
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
    latencies = [r["latency"] if r["latency"] is not None else 0 for r in rows]
    latencies_lo = [r["latency_lo"] if r["latency_lo"] is not None else 0 for r in rows]
    latencies_hi = [r["latency_hi"] if r["latency_hi"] is not None else 0 for r in rows]
    latency_srcs = [r["latency_src"] for r in rows]
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

    def color_lat(v):
        # 入睡 latency：> 30 分需注意；> 45 分提示 sleep onset insomnia
        if v >= 45: return "#d7301f"
        if v >= 30: return "#fc8d59"
        if v >= 20: return "#fdcc8a"
        return "#74c476"

    width = max(16, len(dates) * 0.32)
    fig, axes = plt.subplots(6, 1, figsize=(width, 23),
                              sharex=True, gridspec_kw={"height_ratios": [3, 2, 2, 2, 2, 2]})

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
    for d, v in zip(dates, tsts):
        ax.annotate(f"{v:.1f}", xy=(d, v), xytext=(0, 2),
                    textcoords="offset points", ha="center", fontsize=6,
                    color="darkred" if v < 6 else "#444")
    ax.set_ylabel("TST 總睡眠時間 (h)\nGarmin dailySleepDTO", fontsize=11)
    ax.set_ylim(0, max(10, max(tsts) + 0.5))
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="upper right", fontsize=8, ncol=3)

    # Panel 6: Sleep latency 估算（雙範圍 lower–upper）
    ax = axes[5]
    colors = [color_lat(v) for v in latencies_lo]
    ax.bar(dates, latencies_lo, color=colors, edgecolor="#333", linewidth=0.6, width=0.8,
           label="HR-based 下限")
    # Upper bound 用「半透明擴增條」疊在 lower bar 上方
    upper_extension = [max(hi - lo, 0) for lo, hi in zip(latencies_lo, latencies_hi)]
    ax.bar(dates, upper_extension, bottom=latencies_lo, color="#888", alpha=0.35,
           edgecolor="#444", linewidth=0.4, width=0.8, hatch="///",
           label="步數-based 上限（躺床清醒不確定區）")
    # 手動覆寫日期 — 加邊框與標記
    for d, src, v in zip(dates, latency_srcs, latencies):
        if src == "manual_override":
            ax.bar([d], [v], color="#1e88e5", edgecolor="#0d47a1", linewidth=1.5, width=0.8, alpha=0.85)
            ax.annotate("✎", xy=(d, v), xytext=(0, 8),
                        textcoords="offset points", ha="center", fontsize=10, color="#0d47a1")
    ax.axhline(20, color="goldenrod", linestyle=":", linewidth=1.0, alpha=0.6, label="正常上限 20 分")
    ax.axhline(30, color="orange",    linestyle=":", linewidth=1.0, alpha=0.6, label="偏長 30 分")
    ax.axhline(45, color="red",       linestyle=":", linewidth=1.0, alpha=0.6, label="疑似失眠 45 分")
    for d, lo, hi in zip(dates, latencies_lo, latencies_hi):
        if hi > 0:
            label = f"{lo}" if lo == hi else f"{lo}–{hi}"
            ax.annotate(label, xy=(d, hi), xytext=(0, 2),
                        textcoords="offset points", ha="center", fontsize=6,
                        color="darkred" if lo >= 30 else "#444")
    ax.set_ylabel("入睡 Latency (分)\nHR+步數+壓力 估算", fontsize=11)
    max_y = max(latencies_hi) if latencies_hi else 0
    ax.set_ylim(0, max(50, max_y + 5))
    ax.set_xlabel("日期（每根 bar = 一晚睡眠）", fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="upper right", fontsize=7, ncol=2)
    ax.text(0.01, 0.95,
            "[!] 估算非測量。實線下限=HR訊號（可能低估）；陰影上限=步數訊號（可能高估）；藍色=手動上床時間",
            transform=ax.transAxes, fontsize=8, color="darkred",
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", fc="#fff3cd", ec="#d7301f", alpha=0.9))

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

    Rolling window：每次都畫 today 與往前 (max_nights-1) 晚（共 max_nights 晚）。
    缺資料的日期自動跳過。檔名 spo2_overlay_{actual_start}_to_{today}_elapsed.png。
    每日 daily check-in 呼叫時會產生當日的滾動快照，舊快照保留為歷史。
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

    spo2_dir = ROOT / "reviews" / "daily" / "spo2"
    spo2_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.strptime(today_str, "%Y-%m-%d").date()

    window_start_target = today - timedelta(days=max_nights - 1)
    nights_to_plot = []
    cur = window_start_target
    while cur <= today:
        if (DATA_DIR / f"{cur}.json").exists():
            nights_to_plot.append(cur)
        cur += timedelta(days=1)

    if not nights_to_plot:
        print(f"[skip] {window_start_target} ~ {today} 無可用 epoch 資料")
        return

    new_start = nights_to_plot[0]

    fig, ax = plt.subplots(figsize=(14, 6))
    cmap = plt.get_cmap("viridis")
    n = len(nights_to_plot)

    def mins_below(epochs, thr):
        return sum(1 for e in epochs if e.get("spo2Reading") is not None and e["spo2Reading"] < thr)

    # Lazy import latency estimator
    try:
        from estimate_sleep_latency import estimate as estimate_latency
    except Exception:
        estimate_latency = None

    summary_rows = []
    line_entries = []  # (color, short_label) for in-plot stat block
    for i, d in enumerate(nights_to_plot):
        epochs, summary = load_epochs(str(d))
        if not epochs:
            continue
        t0 = parse_ts(epochs[0]["epochTimestamp"])
        xs = [(parse_ts(e["epochTimestamp"]) - t0).total_seconds() / 60 for e in epochs]
        ys_raw = [e.get("spo2Reading") for e in epochs]
        ys = [v if v is not None else float("nan") for v in ys_raw]
        is_today = (d == today)
        color = "#d7301f" if is_today else cmap(i / max(n - 1, 1) * 0.85)
        alpha = 1.0 if is_today else 0.55
        lw = 1.9 if is_today else 1.0
        nadir = summary.get("lowestSPO2") if summary else None
        avg = summary.get("averageSPO2") if summary else None
        pct, _, _ = t90(epochs)
        m90 = mins_below(epochs, 90)
        m85 = mins_below(epochs, 85)
        m80 = mins_below(epochs, 80)
        legend_label = f"{d}" + ("  ◀ today" if is_today else "")
        ax.plot(xs, ys, color=color, alpha=alpha, linewidth=lw, label=legend_label)
        # AUC shading: fill between line and 90 where line<90 (and 85, 80 stacked layers)
        fill_alpha = 0.30 if is_today else 0.10
        ax.fill_between(xs, ys, 90, where=[(v is not None and v < 90) for v in ys_raw],
                        color="#fdae6b", alpha=fill_alpha, interpolate=True, linewidth=0)
        ax.fill_between(xs, ys, 85, where=[(v is not None and v < 85) for v in ys_raw],
                        color="#fc8d59", alpha=fill_alpha + 0.05, interpolate=True, linewidth=0)
        ax.fill_between(xs, ys, 80, where=[(v is not None and v < 80) for v in ys_raw],
                        color="#d7301f", alpha=fill_alpha + 0.10, interpolate=True, linewidth=0)
        # Latency 估算
        lat_str = "—"
        if estimate_latency is not None:
            try:
                est = estimate_latency(str(d))
                if est and "error" not in est and est.get("latency_min") is not None:
                    lat_str = f"{est['latency_min']}m"
            except Exception:
                pass
        short = (f"{d.strftime('%m-%d')}  nadir {nadir}%  T90 {pct:.1f}%  "
                 f"<90:{m90}m  <85:{m85}m  <80:{m80}m  lat:{lat_str}"
                 + ("  ◀" if is_today else ""))
        line_entries.append((color, short, is_today))
        summary_rows.append((d, nadir, pct, m90, m85, m80, is_today))

    ax.axhline(90, color="orange", linestyle="--", linewidth=0.8, alpha=0.7, label="OSA 90%")
    ax.axhline(85, color="#fc8d59", linestyle=":", linewidth=0.7, alpha=0.6, label="中度 85%")
    ax.axhline(80, color="darkred", linestyle="--", linewidth=0.6, alpha=0.5, label="重度 80%")

    ax.set_xlabel("距入睡時間 (分鐘)")
    ax.set_ylabel("SpO2 (%)")
    ax.set_ylim(70, 100)
    ax.grid(alpha=0.3)
    ax.set_title(f"多晚 SpO2 Overlay（rolling {max_nights} 晚）— {new_start} 至 {today}（共 {n} 晚）")
    ax.legend(loc="upper right", fontsize=8, framealpha=0.85, ncol=2)

    # In-plot stat block (lower-left): one line per night, color-matched
    block_top = 0.32
    line_h = 0.035
    ax.text(0.005, block_top + line_h, "晚數累計（分鐘）", transform=ax.transAxes,
            fontsize=9, fontweight="bold", color="#222",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#888", alpha=0.85))
    for j, (color, short, is_today) in enumerate(line_entries):
        ax.text(0.005, block_top - j * line_h, short, transform=ax.transAxes,
                fontsize=8, color=color, family="monospace",
                fontweight="bold" if is_today else "normal",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))

    fig.tight_layout()

    out = spo2_dir / f"spo2_overlay_{new_start}_to_{today}_elapsed.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print(f"Overlay 圖已存：{out}")
    print(f"Rolling 窗：{new_start} ~ {today}（{n}/{max_nights} 晚有資料）")
    print()
    print(f"  {'日期':<12} {'nadir':>6} {'T90':>6}  {'<90':>5} {'<85':>5} {'<80':>5}")
    print("  " + "-" * 50)
    for d, nadir, pct, m90, m85, m80, is_today in summary_rows:
        marker = " ◀" if is_today else "  "
        print(f"  {str(d):<12} {nadir:>5}% {pct:>5.1f}%  {m90:>4}m {m85:>4}m {m80:>4}m{marker}")


def cmd_hypnogram7(today_str: str, max_nights: int = 7):
    """7 晚 SpO2 × 睡眠分期疊圖（每晚一列 subplot，stage 背景色 + SpO2 折線）。

    Rolling window：today 與往前 (max_nights-1) 晚共 max_nights 晚；缺資料自動跳過。
    輸出：reviews/daily/spo2/spo2_hypnogram_7night_{today}.png
    用途：OSA 表型驗證（REM/Light/Deep dominant 漂移分析）。
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import rcParams
        from matplotlib.patches import Patch
        rcParams["font.sans-serif"] = ["Microsoft JhengHei", "PingFang TC", "PingFang SC",
                                       "Heiti TC", "Hiragino Sans GB", "Arial Unicode MS",
                                       "Noto Sans CJK TC", "DejaVu Sans"]
        rcParams["axes.unicode_minus"] = False
    except ImportError:
        print("需先安裝 matplotlib")
        return

    spo2_dir = ROOT / "reviews" / "daily" / "spo2"
    spo2_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.strptime(today_str, "%Y-%m-%d").date()

    def _parse_gmt(s):
        return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc).astimezone(TPE)

    stage_color = {0.0: "#1f3a5f", 1.0: "#9ecae1", 2.0: "#d7301f"}
    stage_alpha = {0.0: 0.18, 1.0: 0.08, 2.0: 0.22}

    nights = []
    for i in range(max_nights - 1, -1, -1):
        d = today - timedelta(days=i)
        p = DATA_DIR / f"{d.isoformat()}.json"
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        sleep = data.get("sleep") or {}
        epochs = sleep.get("wellnessEpochSPO2DataDTOList") or []
        levels = sleep.get("sleepLevels") or []
        if not epochs or not levels:
            continue
        epochs.sort(key=lambda e: e["epochTimestamp"])
        nights.append((d, epochs, levels, sleep.get("wellnessSpO2SleepSummaryDTO") or {}))

    if not nights:
        print(f"[skip] {today} 往前 {max_nights} 晚無 sleepLevels + epochs 資料")
        return

    n = len(nights)
    fig, axes = plt.subplots(n, 1, figsize=(14, 2.0 * n), sharex=True)
    if n == 1:
        axes = [axes]

    table_rows = []
    for ax, (d, epochs, levels, summ) in zip(axes, nights):
        t_start = _parse_gmt(levels[0]["startGMT"])
        for lv in levels:
            s = (_parse_gmt(lv["startGMT"]) - t_start).total_seconds() / 60
            e = (_parse_gmt(lv["endGMT"]) - t_start).total_seconds() / 60
            al = lv["activityLevel"]
            if al in stage_color:
                ax.axvspan(s, e, color=stage_color[al], alpha=stage_alpha[al], zorder=0)
        xs = [(parse_ts(e["epochTimestamp"]) - t_start).total_seconds() / 60 for e in epochs]
        ys = [e.get("spo2Reading") if e.get("spo2Reading") is not None else float("nan") for e in epochs]
        ax.plot(xs, ys, color="#222", linewidth=1.2, zorder=3)
        ax.fill_between(xs, ys, 88, where=[(v is not None and not (v != v) and v < 88) for v in ys],
                         color="#fc8d59", alpha=0.5, interpolate=True, zorder=2)
        ax.fill_between(xs, ys, 85, where=[(v is not None and not (v != v) and v < 85) for v in ys],
                         color="#d7301f", alpha=0.6, interpolate=True, zorder=2)
        ax.axhline(88, color="orange", linestyle="--", linewidth=0.6, alpha=0.6)
        ax.axhline(85, color="darkred", linestyle=":", linewidth=0.5, alpha=0.5)
        ax.set_ylim(75, 100)
        ax.set_yticks([80, 90, 100])
        ax.grid(alpha=0.25)

        nadir = summ.get("lowestSPO2")
        avg = summ.get("averageSPO2")
        is_today = (d == today)
        label = f"{d.strftime('%m-%d %a')}  nadir {nadir}%  avg {avg}%"
        if is_today:
            label += "  < today"
        ax.set_ylabel(label, rotation=0, ha="right", va="center", fontsize=9,
                      fontweight="bold" if is_today else "normal",
                      color="#d7301f" if is_today else "#222")

        # Stage-stratified stats
        def stage_at(ts, lvs=levels):
            for lv in lvs:
                s_ = _parse_gmt(lv["startGMT"])
                e_ = _parse_gmt(lv["endGMT"])
                if s_ <= ts < e_:
                    return lv["activityLevel"]
            return None
        from collections import defaultdict
        sp = defaultdict(list)
        for ep in epochs:
            v = ep.get("spo2Reading")
            if v is None: continue
            st = stage_at(parse_ts(ep["epochTimestamp"]))
            if st is not None:
                sp[st].append(v)
        row = [d.isoformat()]
        for st_val in [0.0, 1.0, 2.0]:
            vals = sp.get(st_val, [])
            if vals:
                lo = min(vals)
                p90 = sum(1 for v in vals if v < 90) / len(vals) * 100
                row.append(f"{lo}/{p90:.0f}%")
            else:
                row.append("—")
        table_rows.append(row)

    axes[-1].set_xlabel("距入睡時間（分鐘）")
    legend_elems = [
        Patch(facecolor="#1f3a5f", alpha=0.18, label="Deep（深眠）"),
        Patch(facecolor="#9ecae1", alpha=0.4, label="Light（淺眠）"),
        Patch(facecolor="#d7301f", alpha=0.22, label="REM"),
        Patch(facecolor="#fc8d59", alpha=0.5, label="SpO2 < 88%"),
        Patch(facecolor="#d7301f", alpha=0.6, label="SpO2 < 85%"),
    ]
    axes[0].legend(handles=legend_elems, loc="lower right", fontsize=8, framealpha=0.9, ncol=5)
    axes[0].set_title(f"7 晚 SpO2 × 睡眠分期對應分析（{nights[0][0]} 至 {today}）— OSA 表型驗證")

    fig.tight_layout()
    out = spo2_dir / f"spo2_hypnogram_7night_{today}.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print(f"7 晚 hypnogram 圖已存：{out}")
    print(f"  Stage-stratified nadir / <90% 比例")
    print(f"  {'Date':<12} {'Deep':>12} {'Light':>12} {'REM':>12}")
    for row in table_rows:
        print(f"  {row[0]:<12} {row[1]:>12} {row[2]:>12} {row[3]:>12}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", type=int, metavar="N", help="近 N 晚文字摘要")
    ap.add_argument("--night", help="單晚詳細 events，YYYY-MM-DD")
    ap.add_argument("--chart", help="產生單晚 SpO2 chart，YYYY-MM-DD")
    ap.add_argument("--trend", type=int, nargs="?", const=9999, metavar="N",
                    help="多日趨勢圖（預設全部，N 限制最近幾天）")
    ap.add_argument("--overlay", help="多晚 SpO2 epoch 疊圖（rolling 7 晚），YYYY-MM-DD = 今日")
    ap.add_argument("--hypnogram7", help="7 晚 SpO2 × 睡眠分期疊圖（rolling），YYYY-MM-DD = 今日")
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
    if args.hypnogram7:
        cmd_hypnogram7(args.hypnogram7)
    if not (args.summary or args.night or args.chart or args.trend is not None or args.overlay or args.hypnogram7):
        ap.print_help()


if __name__ == "__main__":
    main()
