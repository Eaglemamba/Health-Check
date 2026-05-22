#!/usr/bin/env python3
"""
SpO2 ↔ HR 偶聯分析（dual-panel: 上 SpO2 + 下 HR）

每個 desat event 與 sleepHeartRate 同步軸對齊，分類為：
  - Coupled  : ΔHR_max ≥ 8 bpm（≤ event_end + 90s 內）— autonomic 仍有反應
  - Ambiguous: 5–8 bpm
  - Silent   : < 5 bpm — chronic autonomic blunting 訊號（壞消息）

用法：
    python scripts/analyze_spo2_hr_coupling.py --night 2026-05-21
    python scripts/analyze_spo2_hr_coupling.py --summary 14
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from statistics import median

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
OUT_DIR = ROOT / "reviews" / "daily" / "spo2"
TPE = timezone(timedelta(hours=8))

DESAT_THRESHOLD = 90
# Garmin sleep HR 為 120s averaged → spike 被 dilute；對應放寬閾值
HR_COUPLED = 5      # 2-min 平均下，+5 bpm 已暗示真實 +10-15 bpm spike
HR_AMBIG = 3
HR_WINDOW_PRE_SEC = 60      # 含 event 內 HR 上升段
HR_WINDOW_POST_SEC = 240    # 4 min — 保證捕捉 2 個 HR samples 含 spike + recovery
SLEEP_ONSET_BASELINE_MIN = 20  # 用睡眠開始後 20 min median 作 true baseline


def parse_iso_local(s: str) -> datetime:
    return datetime.fromisoformat(s.rstrip("Z").replace(".0", "")).replace(tzinfo=timezone.utc).astimezone(TPE)


def ms_to_tpe(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone(TPE)


def load_night(date: str):
    p = DATA_DIR / f"{date}.json"
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    sleep = data.get("sleep") or {}
    epochs = sleep.get("wellnessEpochSPO2DataDTOList") or []
    hr = sleep.get("sleepHeartRate") or []
    levels = sleep.get("sleepLevels") or []
    if not epochs or not hr:
        return None
    epochs.sort(key=lambda e: e["epochTimestamp"])
    hr.sort(key=lambda r: r["startGMT"])
    dto = sleep.get("dailySleepDTO") or {}
    sleep_start = ms_to_tpe(dto["sleepStartTimestampGMT"]) if dto.get("sleepStartTimestampGMT") else None
    return {
        "spo2": [(parse_iso_local(e["epochTimestamp"]), e["spo2Reading"]) for e in epochs if e.get("spo2Reading") is not None],
        "hr": [(ms_to_tpe(r["startGMT"]), r["value"]) for r in hr if r.get("value")],
        "levels": levels,
        "sleep_start": sleep_start,
    }


def find_desat_events(spo2_series, threshold=DESAT_THRESHOLD, gap_min=2):
    events = []
    cur = None
    for t, v in spo2_series:
        if v < threshold:
            if cur is None:
                cur = {"start": t, "end": t, "vals": [v]}
            elif (t - cur["end"]).total_seconds() / 60 > gap_min:
                events.append(_finalize(cur))
                cur = {"start": t, "end": t, "vals": [v]}
            else:
                cur["end"] = t
                cur["vals"].append(v)
        elif cur is not None:
            events.append(_finalize(cur))
            cur = None
    if cur is not None:
        events.append(_finalize(cur))
    return events


def _finalize(ev):
    ev["duration_min"] = int((ev["end"] - ev["start"]).total_seconds() / 60 + 1)
    ev["min"] = min(ev["vals"])
    return ev


def hr_in_window(hr_series, start_dt, end_dt):
    return [(t, v) for t, v in hr_series if start_dt <= t <= end_dt]


def sleep_onset_baseline(hr_series, sleep_start_dt):
    """睡眠開始後前 N 分鐘 median 作 unstressed baseline。"""
    if not hr_series or sleep_start_dt is None:
        return None
    window_end = sleep_start_dt + timedelta(minutes=SLEEP_ONSET_BASELINE_MIN)
    vals = [v for t, v in hr_series if sleep_start_dt <= t <= window_end]
    return median(vals) if vals else None


def classify_coupling(event, hr_series, true_baseline=None):
    """Return dict with delta_hr_peak, delta_hr_sustained, baselines, classification.

    true_baseline = sleep-onset-derived（unstressed reference）
    local_baseline = event 前 5 min median（local context）
    classification 用較保守的（兩者取較高的 baseline 計 Δ — 避免高估反應）。
    """
    # Local baseline (event 前 5 min)
    pre = event["start"] - timedelta(minutes=5)
    base_window = [v for t, v in hr_series if pre <= t < event["start"]]
    local_baseline = median(base_window) if base_window else None

    # Response window — wider, 4 min post end
    response_end = event["end"] + timedelta(seconds=HR_WINDOW_POST_SEC)
    response_start = event["start"] - timedelta(seconds=HR_WINDOW_PRE_SEC)
    resp_hr = [v for t, v in hr_series if response_start <= t <= response_end]

    if not resp_hr:
        return {"delta_peak": None, "delta_sustained": None,
                "local_baseline": local_baseline, "true_baseline": true_baseline,
                "class": "no_hr"}

    # 用兩個 baseline 較高者（更保守）作 Δ 計算
    baselines = [b for b in (local_baseline, true_baseline) if b is not None]
    baseline_used = max(baselines) if baselines else None
    if baseline_used is None:
        return {"delta_peak": None, "delta_sustained": None,
                "local_baseline": local_baseline, "true_baseline": true_baseline,
                "class": "no_hr"}

    delta_peak = max(resp_hr) - baseline_used
    delta_sustained = median(resp_hr) - baseline_used

    if delta_peak >= HR_COUPLED:
        cls = "coupled"
    elif delta_peak >= HR_AMBIG:
        cls = "ambiguous"
    else:
        cls = "silent"
    return {"delta_peak": delta_peak, "delta_sustained": delta_sustained,
            "local_baseline": local_baseline, "true_baseline": true_baseline,
            "baseline_used": baseline_used, "n_samples": len(resp_hr),
            "class": cls}


def analyze_night(date: str, verbose=True):
    night = load_night(date)
    if not night:
        if verbose:
            print(f"[skip] {date}：缺 spo2 / hr 資料")
        return None
    events = find_desat_events(night["spo2"])
    if not events:
        if verbose:
            print(f"{date}：無 <90% event")
        return {"date": date, "events": [], "coupled": 0, "silent": 0, "ambiguous": 0, "no_hr": 0}

    true_base = sleep_onset_baseline(night["hr"], night.get("sleep_start"))
    classified = []
    for ev in events:
        result = classify_coupling(ev, night["hr"], true_baseline=true_base)
        classified.append({**ev, **result})

    # Per-cycle T90 stats (90-min cycles from sleep onset)
    cycles = []
    sleep_start = night.get("sleep_start")
    if sleep_start and night["spo2"]:
        total_min = (night["spo2"][-1][0] - sleep_start).total_seconds() / 60
        n_cycles = int(total_min // 90) + 1
        for ci in range(n_cycles):
            cs = sleep_start + timedelta(minutes=90 * ci)
            ce = sleep_start + timedelta(minutes=90 * (ci + 1))
            cycle_spo2 = [v for t, v in night["spo2"] if cs <= t < ce]
            if not cycle_spo2:
                continue
            below = sum(1 for v in cycle_spo2 if v < 90)
            t90_c = below / len(cycle_spo2) * 100
            n_ev = sum(1 for c in classified if cs <= c["start"] < ce)
            cycles.append({"cycle": ci + 1, "start": cs, "end": ce, "t90": t90_c, "n_events": n_ev})

    counts = {"coupled": 0, "silent": 0, "ambiguous": 0, "no_hr": 0}
    for c in classified:
        counts[c["class"]] += 1

    if verbose:
        print(f"### {date}（true baseline = {true_base:.0f} bpm｜HR 採樣 120s avg）" if true_base else f"### {date}")
        if cycles:
            print(f"Cycle T90（90-min cycles from sleep onset {sleep_start.strftime('%H:%M')}）：")
            for c in cycles:
                flag = " 🔴" if c["t90"] >= 5 else ""
                print(f"  C{c['cycle']} ({c['start'].strftime('%H:%M')}-{c['end'].strftime('%H:%M')}): T90={c['t90']:.1f}%, n_events={c['n_events']}{flag}")
            print()
        n = len(classified)
        print(f"Desat events: {n}（coupled {counts['coupled']} / ambiguous {counts['ambiguous']} / silent {counts['silent']} / no_hr {counts['no_hr']}）")
        silent_pct = counts["silent"] / n * 100 if n else 0
        if silent_pct >= 50:
            print(f"⚠️  Silent desat 占比 {silent_pct:.0f}% — autonomic blunting 訊號")
            print(f"   (註：2-min avg 會 dilute spike ~3-5×；真實 PSG 比例可能略低，但 pattern 應一致)")
        print()
        print(f"  {'時段':<14} {'長':>4} {'nadir':>6} {'Δpeak':>6} {'Δsust':>6} {'base':>5} {'n':>3}  分類")
        for c in classified:
            dp = f"+{c['delta_peak']:.0f}" if c.get("delta_peak") is not None else "—"
            ds = f"+{c['delta_sustained']:.0f}" if c.get("delta_sustained") is not None else "—"
            b = f"{c['baseline_used']:.0f}" if c.get("baseline_used") is not None else "—"
            nsam = str(c.get("n_samples", "—"))
            tag = {"coupled": "[+] coupled", "ambiguous": "[?] ambig", "silent": "[-] silent", "no_hr": "[ ] no HR"}[c["class"]]
            print(f"  {c['start'].strftime('%H:%M')}-{c['end'].strftime('%H:%M')}  "
                  f"{c['duration_min']:>3}m  {c['min']:>4}%  {dp:>5}  {ds:>5}  {b:>4}  {nsam:>2}  {tag}")
    return {"date": date, "events": classified, **counts}


def plot_night(date: str, out_path: Path = None):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import rcParams
        rcParams["font.sans-serif"] = ["Microsoft JhengHei", "PingFang TC", "Heiti TC",
                                        "Noto Sans CJK TC", "DejaVu Sans"]
        rcParams["axes.unicode_minus"] = False
    except ImportError:
        print("需先安裝 matplotlib")
        return

    night = load_night(date)
    if not night:
        print(f"[skip] {date}")
        return

    events = find_desat_events(night["spo2"])
    true_base = sleep_onset_baseline(night["hr"], night.get("sleep_start"))
    classified = []
    for ev in events:
        result = classify_coupling(ev, night["hr"], true_baseline=true_base)
        classified.append({**ev, **result})

    spo2_t = [t for t, _ in night["spo2"]]
    spo2_v = [v for _, v in night["spo2"]]
    hr_t = [t for t, _ in night["hr"]]
    hr_v = [v for _, v in night["hr"]]
    sleep_start = night.get("sleep_start")

    # Cycle 分隔（每 90 min，自 sleep onset）+ 各 cycle T90 計算
    cycles = []  # list of (cycle_no, start_dt, end_dt, t90_pct, n_events)
    if sleep_start and spo2_t:
        total_min = (spo2_t[-1] - sleep_start).total_seconds() / 60
        n_cycles = int(total_min // 90) + 1
        for ci in range(n_cycles):
            cs = sleep_start + timedelta(minutes=90 * ci)
            ce = sleep_start + timedelta(minutes=90 * (ci + 1))
            cycle_spo2 = [v for t, v in night["spo2"] if cs <= t < ce]
            if not cycle_spo2:
                continue
            below = sum(1 for v in cycle_spo2 if v < 90)
            t90_c = below / len(cycle_spo2) * 100
            n_ev = sum(1 for c in classified if cs <= c["start"] < ce)
            cycles.append((ci + 1, cs, ce, t90_c, n_ev))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True,
                                    gridspec_kw={"height_ratios": [1, 1]})

    ax1.plot(spo2_t, spo2_v, color="#1f77b4", lw=1.2, label="SpO2")
    ax1.axhline(90, color="orange", ls="--", lw=0.8, alpha=0.7)
    ax1.axhline(88, color="red", ls="--", lw=0.8, alpha=0.7)

    # Cycle 分隔線 + 標籤（兩 panel 都加）
    for ci, cs, ce, t90_c, n_ev in cycles:
        for ax in (ax1, ax2):
            ax.axvline(cs, color="#999", ls=":", lw=0.6, alpha=0.5)
        # cycle label + T90 在 ax1 上方
        mid = cs + (ce - cs) / 2
        clip_end = min(ce, spo2_t[-1])
        if mid > spo2_t[-1]:
            mid = cs + (clip_end - cs) / 2
        flag = " *" if t90_c >= 5 else ""
        ax1.text(mid, 99.5, f"C{ci}\nT90={t90_c:.0f}%{flag}\nn={n_ev}",
                 fontsize=7, ha="center", va="top",
                 color="#d62728" if t90_c >= 5 else "#444",
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#ccc", alpha=0.8, lw=0.5))

    color_map = {"coupled": "#2ca02c", "silent": "#d62728", "ambiguous": "#ff7f0e", "no_hr": "#888888"}
    for c in classified:
        ax1.axvspan(c["start"], c["end"], color=color_map[c["class"]], alpha=0.25)
        ax1.annotate(f"{c['min']}%", xy=(c["start"], c["min"]), fontsize=7, color=color_map[c["class"]])
    ax1.set_ylabel("SpO2 (%)")
    ax1.set_ylim(75, 102)
    cycle_summary = ""
    if cycles:
        red_cycles = [f"C{c[0]}({c[3]:.0f}%)" for c in cycles if c[3] >= 5]
        cycle_summary = f"｜🔴 cycle: {' '.join(red_cycles)}" if red_cycles else "｜all cycles T90<5%"
    ax1.set_title(f"{date} — SpO2 ↔ HR coupling（綠=coupled, 紅=silent, 橘=ambiguous）{cycle_summary}")
    ax1.grid(alpha=0.3)

    ax2.plot(hr_t, hr_v, color="#d62728", lw=1.0, label="HR")
    if true_base is not None:
        ax2.axhline(true_base, color="gray", ls=":", lw=0.7, alpha=0.6, label=f"sleep-onset baseline {true_base:.0f}")
        ax2.legend(loc="upper right", fontsize=8)
    for c in classified:
        ax2.axvspan(c["start"], c["end"], color=color_map[c["class"]], alpha=0.15)
    ax2.set_ylabel("HR (bpm)")
    ax2.set_xlabel("Time (Asia/Taipei)")
    ax2.grid(alpha=0.3)

    n = len(classified)
    counts = {"coupled": 0, "ambiguous": 0, "silent": 0, "no_hr": 0}
    for c in classified:
        counts[c["class"]] += 1
    summary = (f"events={n}  ✅ coupled={counts['coupled']}  "
               f"🟡 ambig={counts['ambiguous']}  🔴 silent={counts['silent']}  "
               f"— no HR={counts['no_hr']}")
    fig.suptitle(summary, fontsize=10, y=0.995)

    fig.autofmt_xdate(rotation=0)
    plt.tight_layout()
    out = out_path or OUT_DIR / f"spo2_hr_dual_{date}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"✓ {out.relative_to(ROOT)}")


def cmd_summary(days: int):
    files = sorted(DATA_DIR.glob("*.json"))[-days:]
    print(f"近 {len(files)} 晚 SpO2↔HR 偶聯摘要")
    print("-" * 78)
    print(f"{'日期':<12} {'events':>7} {'coupled':>8} {'ambig':>6} {'silent':>7} {'silent%':>8}")
    print("-" * 78)
    totals = {"events": 0, "coupled": 0, "ambiguous": 0, "silent": 0, "no_hr": 0}
    for f in files:
        r = analyze_night(f.stem, verbose=False)
        if not r:
            continue
        n = len(r["events"])
        sp = r["silent"] / n * 100 if n else 0
        totals["events"] += n
        for k in ("coupled", "ambiguous", "silent", "no_hr"):
            totals[k] += r[k]
        flag = " ⚠️" if sp >= 50 else ""
        print(f"{r['date']}  {n:>6}  {r['coupled']:>7}  {r['ambiguous']:>5}  {r['silent']:>6}  {sp:>6.0f}%{flag}")
    print("-" * 78)
    n = totals["events"]
    sp = totals["silent"] / n * 100 if n else 0
    print(f"{'cohort':<12}  {n:>6}  {totals['coupled']:>7}  {totals['ambiguous']:>5}  {totals['silent']:>6}  {sp:>6.0f}%")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--night", type=str, help="日期 YYYY-MM-DD：列印分析 + 出圖")
    g.add_argument("--summary", type=int, help="cohort 摘要（最近 N 晚）")
    ap.add_argument("--no-chart", action="store_true", help="--night 時不出圖")
    args = ap.parse_args()
    if args.night:
        analyze_night(args.night)
        if not args.no_chart:
            plot_night(args.night)
    else:
        cmd_summary(args.summary)


if __name__ == "__main__":
    main()
