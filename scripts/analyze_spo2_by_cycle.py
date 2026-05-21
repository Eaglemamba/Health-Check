"""
SpO2 by sleep cycle — multi-night aggregated probability analysis.

For each night with Garmin sleep stages + SpO2 epoch data:
  1. Detect NREM-REM cycles. A "cycle" = block from sleep onset (or prior REM end)
     to the END of the next REM block. Trailing time after the last REM end is
     the "post-final-REM tail" (i.e. just-before-waking cycle).
  2. Per cycle, compute: duration, nadir SpO2, T90 / T88 / T85 / T80 (% time < threshold),
     mean SpO2, longest continuous desat event.
  3. Aggregate across all nights: cycle-indexed probability P(any desat < threshold)
     and pooled nadir distribution.
  4. Time-normalized stacking: P(SpO2 < threshold | elapsed minutes from sleep onset)
     across all nights, with N(t) coverage.

Output:
  - Console table summary
  - reviews/daily/spo2/spo2_by_cycle.png (3 panels)

Mapping confirmed from dailySleepDTO totals:
  activityLevel 0=deep, 1=light, 2=REM, 3=awake
"""
import json
from pathlib import Path
from datetime import datetime, timezone
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
OUT_DIR = ROOT / "reviews" / "daily" / "spo2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STAGE = {0.0: "deep", 1.0: "light", 2.0: "REM", 3.0: "awake"}
THRESHOLDS = [90, 85, 80]

# Device filter — Venu 4 only. Earlier device (3471541259, used 4/19-4/23) had
# different SpO2 sensor characteristics and is excluded for cross-night consistency.
VENU4_DEVICE_ID = 3622900919


def parse_gmt(s: str) -> datetime:
    """Garmin GMT timestamps end '.0'. Treat as UTC."""
    if s.endswith(".0"):
        s = s[:-2]
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def load_night(p: Path):
    """Return dict with sleep_start, sleep_end, stages [(start_min, end_min, stage)],
    spo2 [(elapsed_min, value)], or None if unusable."""
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    sleep = data.get("sleep") or {}
    dto = sleep.get("dailySleepDTO") or {}
    start_ts = dto.get("sleepStartTimestampGMT")
    end_ts = dto.get("sleepEndTimestampGMT")
    if not start_ts or not end_ts:
        return None
    sleep_start = datetime.fromtimestamp(start_ts / 1000, tz=timezone.utc)
    sleep_end = datetime.fromtimestamp(end_ts / 1000, tz=timezone.utc)
    epochs_raw = sleep.get("wellnessEpochSPO2DataDTOList") or []
    levels = sleep.get("sleepLevels") or []
    if not epochs_raw or not levels:
        return None

    # Device filter — skip nights from non-Venu 4 devices
    first_device = epochs_raw[0].get("deviceId") if epochs_raw else None
    if first_device != VENU4_DEVICE_ID:
        return None

    stages = []
    for s in levels:
        t0 = parse_gmt(s["startGMT"])
        t1 = parse_gmt(s["endGMT"])
        if t1 <= sleep_start or t0 >= sleep_end:
            continue
        t0 = max(t0, sleep_start)
        t1 = min(t1, sleep_end)
        em0 = (t0 - sleep_start).total_seconds() / 60
        em1 = (t1 - sleep_start).total_seconds() / 60
        stages.append((em0, em1, STAGE.get(s["activityLevel"], "?")))
    stages.sort()

    spo2 = []
    for e in epochs_raw:
        ts_raw = e.get("epochTimestamp")
        if isinstance(ts_raw, str):
            ts = parse_gmt(ts_raw)
        else:
            ts = datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc)
        if ts < sleep_start or ts > sleep_end:
            continue
        em = (ts - sleep_start).total_seconds() / 60
        val = e.get("spo2Reading")
        if val is None or val <= 0:
            continue
        spo2.append((em, val))
    spo2.sort()
    if not spo2:
        return None

    return {
        "date": p.stem,
        "sleep_start": sleep_start,
        "sleep_end": sleep_end,
        "tst_min": (sleep_end - sleep_start).total_seconds() / 60,
        "stages": stages,
        "spo2": spo2,
    }


def detect_cycles(stages):
    """A cycle ends at the END of each REM block (after at least one REM observation).
    Returns list of (cycle_start_min, cycle_end_min) for completed cycles, plus
    a 'tail' (post-final-REM block) if it exists with non-zero length.

    Edge case: if a night has 0 REM blocks, return one pseudo-cycle = entire night,
    no tail."""
    if not stages:
        return [], None
    cycle_start = stages[0][0]
    last_end = stages[-1][1]

    cycles = []
    in_rem = False
    for (em0, em1, st) in stages:
        if st == "REM":
            in_rem = True
            rem_end = em1
        else:
            if in_rem:
                cycles.append((cycle_start, rem_end))
                cycle_start = rem_end
                in_rem = False

    if in_rem:
        cycles.append((cycle_start, rem_end))
        cycle_start = rem_end

    tail = None
    if cycle_start < last_end - 1:
        tail = (cycle_start, last_end)
    return cycles, tail


def cycle_metrics(spo2, t0, t1):
    """Return dict of metrics for SpO2 readings in window [t0, t1)."""
    pts = [v for (em, v) in spo2 if t0 <= em < t1]
    if not pts:
        return {"n": 0, "nadir": None, "mean": None}
    arr = np.array(pts)
    return {
        "n": len(pts),
        "duration_min": t1 - t0,
        "nadir": int(arr.min()),
        "mean": float(arr.mean()),
        "t90_pct": float((arr < 90).mean() * 100),
        "t88_pct": float((arr < 88).mean() * 100),
        "t85_pct": float((arr < 85).mean() * 100),
        "t80_pct": float((arr < 80).mean() * 100),
    }


def main():
    nights = []
    for p in sorted(DATA_DIR.glob("*.json")):
        n = load_night(p)
        if n:
            nights.append(n)
    if not nights:
        print("No usable nights found")
        return

    # ---- Method D: fixed 90-min bins (not REM-anchored) ----
    # Rationale: Garmin HRV-based REM detection has high false-negative rate,
    # especially when HRV baseline is low (user's case: 19.7 ms mean). Using
    # fixed 90-min bins decouples desat analysis from REM-staging reliability.
    BIN_EDGES = [0, 90, 180, 270, 360, 480]  # minutes from sleep onset; final bin open-ended
    BIN_LABELS = ["0-90", "90-180", "180-270", "270-360", "360+"]

    bin_records = {lbl: [] for lbl in BIN_LABELS}
    for n in nights:
        tst = n["tst_min"]
        for i, lbl in enumerate(BIN_LABELS):
            t0 = BIN_EDGES[i]
            t1 = BIN_EDGES[i + 1] if i + 1 < len(BIN_EDGES) else 10**6
            if t0 >= tst:
                continue
            t1 = min(t1, tst)
            m = cycle_metrics(n["spo2"], t0, t1)
            if m["nadir"] is not None:
                bin_records[lbl].append(m)

    # ---- Console table: per-bin aggregate ----
    print(f"\n=== SpO2 by Fixed 90-min Bins — {len(nights)} nights ({nights[0]['date']} → {nights[-1]['date']}) ===")
    print(f"HRV baseline: 19.7 ms (low; flat) — REM-anchored cycles unreliable, using time-from-onset bins instead.\n")

    headers = ["Bin (min)", "N nights", "Mean dur", "P(nadir<90)", "P(nadir<88)", "P(nadir<85)", "Median nadir", "Mean T90%"]
    rows = []
    for lbl in BIN_LABELS:
        ms = bin_records[lbl]
        if not ms:
            continue
        nadirs = np.array([m["nadir"] for m in ms])
        t90s = np.array([m["t90_pct"] for m in ms])
        durs = np.array([m["duration_min"] for m in ms])
        rows.append([
            lbl,
            len(ms),
            f"{durs.mean():.0f}",
            f"{(nadirs < 90).mean()*100:.0f}%",
            f"{(nadirs < 88).mean()*100:.0f}%",
            f"{(nadirs < 85).mean()*100:.0f}%",
            int(np.median(nadirs)),
            f"{t90s.mean():.1f}%",
        ])

    col_w = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in col_w)
    print(fmt.format(*headers))
    print("  " + "  ".join("-" * w for w in col_w))
    for r in rows:
        print(fmt.format(*[str(x) for x in r]))

    # ---- For plotting, build a wrapper similar to old structure ----
    by_cycle = {lbl: bin_records[lbl] for lbl in BIN_LABELS if bin_records[lbl]}
    cycle_order = [lbl for lbl in BIN_LABELS if lbl in by_cycle]
    box_labels = [f"{lbl}\nmin" for lbl in cycle_order]

    # ---- Time-normalized empirical probability across nights ----
    bin_min = 1
    max_min = int(max(n["tst_min"] for n in nights)) + 1
    grid = np.arange(0, max_min, bin_min)
    n_below = {th: np.zeros_like(grid, dtype=float) for th in THRESHOLDS}
    n_obs = np.zeros_like(grid, dtype=float)
    for n in nights:
        marks_below = {th: np.zeros_like(grid, dtype=bool) for th in THRESHOLDS}
        marks_obs = np.zeros_like(grid, dtype=bool)
        for (em, v) in n["spo2"]:
            i = int(em // bin_min)
            if i >= len(grid):
                continue
            marks_obs[i] = True
            for th in THRESHOLDS:
                if v < th:
                    marks_below[th][i] = True
        n_obs += marks_obs
        for th in THRESHOLDS:
            n_below[th] += marks_below[th]

    with np.errstate(divide="ignore", invalid="ignore"):
        prob = {th: np.where(n_obs > 0, n_below[th] / n_obs, np.nan) for th in THRESHOLDS}

    # ---- Plot ----
    fig, axes = plt.subplots(3, 1, figsize=(11, 12), gridspec_kw={"height_ratios": [2.2, 1.6, 1.6]})

    ax = axes[0]
    colors = {90: "#ff9500", 85: "#ff375f", 80: "#8b0028"}
    for th in THRESHOLDS:
        ax.plot(grid, prob[th] * 100, color=colors[th], lw=2, label=f"SpO2 < {th}%")
    ax.fill_between(grid, 0, n_obs / n_obs.max() * 5, color="#cccccc", alpha=0.4, label=f"Coverage (n_obs / {int(n_obs.max())})")
    ax.set_xlabel("Elapsed minutes from sleep onset")
    ax.set_ylabel("P(SpO2 < threshold) [%]")
    ax.set_title(f"Per-minute desaturation probability — pooled across {len(nights)} nights")
    ax.set_xlim(0, max_min)
    ax.set_ylim(0, max(60, np.nanmax(prob[90] * 100) * 1.1))
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)

    ax = axes[1]
    box_data = []
    for idx in cycle_order:
        nadirs = [m["nadir"] for m in by_cycle[idx]]
        box_data.append(nadirs)
    bp = ax.boxplot(box_data, tick_labels=box_labels, patch_artist=True, widths=0.55)
    # color: progressively cooler from early to late
    palette = ["#ffb3bf", "#ffd0a8", "#ffe9a8", "#c8e8b8", "#b8d8f0"]
    for patch, color in zip(bp["boxes"], palette[:len(cycle_order)]):
        patch.set_facecolor(color)
        patch.set_edgecolor("#666")
    ax.axhline(88, color="#ff375f", ls="--", lw=1, alpha=0.6, label="88% (OSA flag)")
    ax.axhline(85, color="#8b0028", ls="--", lw=1, alpha=0.5)
    ax.set_ylabel("Nadir SpO2 (%)")
    ax.set_title("Fixed 90-min bins from sleep onset — nadir distribution (no REM-staging dependency)")
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="lower right", fontsize=9)

    ax = axes[2]
    bar_x = np.arange(len(cycle_order))
    p_lt90 = []
    p_lt85 = []
    p_lt80 = []
    for idx in cycle_order:
        nadirs = np.array([m["nadir"] for m in by_cycle[idx]])
        p_lt90.append((nadirs < 90).mean() * 100)
        p_lt85.append((nadirs < 85).mean() * 100)
        p_lt80.append((nadirs < 80).mean() * 100)
    w = 0.27
    ax.bar(bar_x - w, p_lt90, w, color=colors[90], label="P(nadir<90)")
    ax.bar(bar_x, p_lt85, w, color=colors[85], label="P(nadir<85)")
    ax.bar(bar_x + w, p_lt80, w, color=colors[80], label="P(nadir<80)")
    ax.set_xticks(bar_x)
    ax.set_xticklabels(box_labels)
    ax.set_ylabel("% of nights")
    ax.set_title("Probability of nadir below threshold, by 90-min bin from sleep onset")
    ax.grid(alpha=0.3, axis="y")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(0, 105)

    plt.tight_layout()
    out_path = OUT_DIR / "spo2_by_cycle.png"
    plt.savefig(out_path, dpi=140, bbox_inches="tight")
    print(f"\nSaved: {out_path}")

    # ---- Hypothesis test: late bin vs first bin ----
    print(f"\n=== Hypothesis test: late bin vs first 90-min ===")
    first_lbl = cycle_order[0]
    late_lbls = cycle_order[-2:] if len(cycle_order) >= 4 else cycle_order[-1:]
    first = np.array([m["nadir"] for m in by_cycle[first_lbl]])
    late = []
    for lbl in late_lbls:
        late.extend([m["nadir"] for m in by_cycle[lbl]])
    late = np.array(late)
    print(f"  First {first_lbl} min  N={len(first)}: median nadir = {int(np.median(first))}, P(nadir<88) = {(first < 88).mean()*100:.0f}%")
    print(f"  Late {'+'.join(late_lbls)} min N={len(late)}: median nadir = {int(np.median(late))}, P(nadir<88) = {(late < 88).mean()*100:.0f}%")
    try:
        from scipy import stats
        u, pval = stats.mannwhitneyu(late, first, alternative="greater")
        print(f"  Mann-Whitney U (late nadir > first nadir, one-sided): U={u:.0f}, p={pval:.4f}")
        if pval < 0.05:
            print("  → Significant: late bins have higher (cleaner) nadirs than first 90 min.")
        else:
            print("  → Not statistically significant at α=0.05.")
    except Exception as e:
        print(f"  (scipy unavailable: {e})")


if __name__ == "__main__":
    main()
