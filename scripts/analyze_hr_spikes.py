"""
Sleep HR spike density — proxy for sympathetic arousal frequency.

Garmin sleepHeartRate is sampled at ~2 min/epoch, which AVERAGES OUT individual
10-30 sec event-termination spikes. A single sympathetic surge of 10 bpm × 20 sec
contributes only ~1.7 bpm to a 2-min average, near the Garmin HR noise floor (±2 bpm).

What we CAN measure:
  - epoch-to-epoch HR delta >= 3 bpm and >= 5 bpm (count + density per hour)
  - HR jumps temporally co-occurring with SpO2 desats (within 4 min window)
  - Overnight HR baseline drift

What this is NOT:
  - Per-event AHI proxy (resolution too coarse)
  - Replacement for HSAT/PSG ODI

Usage:
  python scripts/analyze_hr_spikes.py
  python scripts/analyze_hr_spikes.py --night 2026-05-15  # detailed single night
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
OUT_DIR = ROOT / "reviews" / "daily" / "spo2"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_gmt(s):
    if isinstance(s, (int, float)):
        return datetime.fromtimestamp(s / 1000, tz=timezone.utc)
    if s.endswith(".0"):
        s = s[:-2]
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def load_night(p):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    sleep = d.get("sleep") or {}
    dto = sleep.get("dailySleepDTO") or {}
    start_ts = dto.get("sleepStartTimestampGMT")
    end_ts = dto.get("sleepEndTimestampGMT")
    if not start_ts or not end_ts:
        return None
    sleep_start = datetime.fromtimestamp(start_ts / 1000, tz=timezone.utc)
    sleep_end = datetime.fromtimestamp(end_ts / 1000, tz=timezone.utc)
    hr_raw = sleep.get("sleepHeartRate") or []
    spo2_raw = sleep.get("wellnessEpochSPO2DataDTOList") or []
    if not hr_raw or not spo2_raw:
        return None

    hr = []
    for e in hr_raw:
        ts = parse_gmt(e["startGMT"])
        if ts < sleep_start or ts > sleep_end:
            continue
        em = (ts - sleep_start).total_seconds() / 60
        v = e.get("value")
        if v and v > 0:
            hr.append((em, int(v)))
    hr.sort()
    if len(hr) < 10:
        return None

    spo2 = []
    for e in spo2_raw:
        ts = parse_gmt(e["epochTimestamp"])
        if ts < sleep_start or ts > sleep_end:
            continue
        em = (ts - sleep_start).total_seconds() / 60
        v = e.get("spo2Reading")
        if v and v > 0:
            spo2.append((em, int(v)))
    spo2.sort()

    return {
        "date": p.stem,
        "tst_min": (sleep_end - sleep_start).total_seconds() / 60,
        "hr": hr,
        "spo2": spo2,
    }


def hr_spike_stats(hr):
    """epoch-to-epoch HR deltas, count jumps >= 3 / 5 bpm (both directions)."""
    arr = np.array([v for _, v in hr])
    deltas = np.diff(arr)
    n_3up = int(((deltas >= 3) & (deltas < 5)).sum())
    n_5up = int((deltas >= 5).sum())
    n_3dn = int(((deltas <= -3) & (deltas > -5)).sum())
    n_5dn = int((deltas <= -5).sum())
    n_epochs = len(arr)
    interval_min = 2.0  # 2-min Garmin epoch (verified)
    hours = n_epochs * interval_min / 60
    return {
        "n_epochs": n_epochs,
        "hours": hours,
        "hr_mean": float(arr.mean()),
        "hr_min": int(arr.min()),
        "hr_max": int(arr.max()),
        "hr_std": float(arr.std()),
        "n_3up": n_3up,
        "n_5up": n_5up,
        "n_3dn": n_3dn,
        "n_5dn": n_5dn,
        "spike3_per_hr": (n_3up + n_5up) / hours,
        "spike5_per_hr": n_5up / hours,
        "deltas": deltas,
    }


def hr_spo2_coupling(hr, spo2, window_min=4, spo2_drop=4):
    """Count HR spikes (>=5 bpm) that occur within ±window_min of a SpO2 drop >= spo2_drop."""
    if not spo2:
        return 0, 0
    spo2_em = np.array([e for e, _ in spo2])
    spo2_v = np.array([v for _, v in spo2])
    # find SpO2 drop events (epoch-to-epoch fall >= spo2_drop)
    spo2_d = np.diff(spo2_v)
    drop_idx = np.where(spo2_d <= -spo2_drop)[0]
    drop_times = spo2_em[drop_idx + 1]

    n_coupled = 0
    n_total_spikes = 0
    hr_em = np.array([e for e, _ in hr])
    hr_v = np.array([v for _, v in hr])
    hr_d = np.diff(hr_v)
    spike_idx = np.where(hr_d >= 5)[0]
    for i in spike_idx:
        n_total_spikes += 1
        spike_t = hr_em[i + 1]
        if len(drop_times) and np.min(np.abs(drop_times - spike_t)) <= window_min:
            n_coupled += 1
    return n_coupled, n_total_spikes


def analyze_all():
    nights = []
    for p in sorted(DATA_DIR.rglob("*.json")):
        n = load_night(p)
        if n:
            nights.append(n)
    if not nights:
        print("No usable nights")
        return

    print(f"\n=== HR spike density — {len(nights)} nights ({nights[0]['date']} → {nights[-1]['date']}) ===")
    print(f"Garmin sleep HR epoch = 2 min. Jumps reflect SUSTAINED shifts, not individual events.\n")
    print(f"  {'Date':<12} {'mean':>5} {'min':>5} {'max':>5} {'Δ3+':>5} {'Δ5+':>5} {'5/hr':>6} {'coup':>5}")
    print("  " + "-" * 70)

    totals = {"n_3up": 0, "n_5up": 0, "hours": 0, "coupled": 0, "total_spikes": 0, "hr_means": [], "spike5_per_hr": []}
    for n in nights:
        s = hr_spike_stats(n["hr"])
        coupled, total = hr_spo2_coupling(n["hr"], n["spo2"])
        totals["n_3up"] += s["n_3up"] + s["n_5up"]
        totals["n_5up"] += s["n_5up"]
        totals["hours"] += s["hours"]
        totals["coupled"] += coupled
        totals["total_spikes"] += total
        totals["hr_means"].append(s["hr_mean"])
        totals["spike5_per_hr"].append(s["spike5_per_hr"])
        coup_pct = (coupled / total * 100) if total else 0
        print(f"  {n['date']:<12} {s['hr_mean']:>5.1f} {s['hr_min']:>5} {s['hr_max']:>5} {s['n_3up']+s['n_5up']:>5} {s['n_5up']:>5} {s['spike5_per_hr']:>6.2f} {coupled:>2}/{total:<2}")

    avg_spike5 = totals["n_5up"] / totals["hours"]
    avg_hr = np.mean(totals["hr_means"])
    coup_overall = (totals["coupled"] / totals["total_spikes"] * 100) if totals["total_spikes"] else 0
    print("\n=== Aggregate ===")
    print(f"  Mean sleep HR: {avg_hr:.1f} bpm (range {min(totals['hr_means']):.1f}–{max(totals['hr_means']):.1f})")
    print(f"  Mean spike ≥5 bpm density: {avg_spike5:.2f}/hr (range {min(totals['spike5_per_hr']):.2f}–{max(totals['spike5_per_hr']):.2f})")
    print(f"  HR↑5 spikes coupled to SpO2 drop ≥4% (within ±4 min): {totals['coupled']}/{totals['total_spikes']} = {coup_overall:.0f}%")
    print(f"\nReference (literature, PSG-based ECG sampling, not Garmin):")
    print(f"  Healthy adult: ~5–10 HR arousals/hr · Mild OSA: 5–15/hr · Moderate: 15–30/hr · Severe: >30/hr")
    print(f"  Garmin 2-min epoch UNDER-COUNTS true arousal frequency by ~5–10×")


def analyze_single(date):
    p = next(iter(DATA_DIR.rglob(f"{date}.json")), DATA_DIR / f"{date}.json")
    n = load_night(p)
    if not n:
        print(f"No data for {date}")
        return
    s = hr_spike_stats(n["hr"])
    coupled, total = hr_spo2_coupling(n["hr"], n["spo2"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 7), sharex=True, gridspec_kw={"height_ratios": [1.5, 1]})

    hr_em = np.array([e for e, _ in n["hr"]])
    hr_v = np.array([v for _, v in n["hr"]])
    spo2_em = np.array([e for e, _ in n["spo2"]])
    spo2_v = np.array([v for _, v in n["spo2"]])

    ax1.plot(hr_em, hr_v, "-", color="#ff375f", lw=1.4, label="HR (2-min epoch)")
    # mark spikes >= 5
    deltas = np.diff(hr_v)
    spike_idx = np.where(deltas >= 5)[0]
    if len(spike_idx) > 0:
        ax1.scatter(hr_em[spike_idx + 1], hr_v[spike_idx + 1], color="#ff375f", s=60, zorder=5, marker="^", label=f"Δ≥5 bpm spike (n={len(spike_idx)})")
    ax1.axhline(hr_v.mean(), color="#888", ls=":", lw=1, label=f"Mean {hr_v.mean():.1f} bpm")
    ax1.set_ylabel("HR (bpm)")
    ax1.set_title(f"Sleep HR + SpO2 — {date} · HR spikes Δ≥5: {s['n_5up']} ({s['spike5_per_hr']:.1f}/hr) · coupled to SpO2 drop: {coupled}/{total}")
    ax1.grid(alpha=0.3)
    ax1.legend(loc="upper right", fontsize=9)

    ax2.plot(spo2_em, spo2_v, "-", color="#3a76d8", lw=1.2, label="SpO2 (1-min epoch)")
    ax2.axhline(88, color="#ff375f", ls="--", lw=1, alpha=0.6, label="88% OSA flag")
    ax2.fill_between(spo2_em, 0, 88, where=(spo2_v < 88), color="#ffd0d8", alpha=0.4)
    ax2.set_ylim(spo2_v.min() - 2, 100)
    ax2.set_xlabel("Elapsed minutes from sleep onset")
    ax2.set_ylabel("SpO2 (%)")
    ax2.grid(alpha=0.3)
    ax2.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    out = OUT_DIR / f"hr_spo2_{date}.png"
    plt.savefig(out, dpi=140, bbox_inches="tight")
    print(f"Saved: {out}")
    print(f"\n{date}: HR mean {s['hr_mean']:.1f} (min {s['hr_min']}, max {s['hr_max']}), "
          f"Δ≥3 spikes {s['n_3up']+s['n_5up']}, Δ≥5 spikes {s['n_5up']} ({s['spike5_per_hr']:.2f}/hr), "
          f"coupled to SpO2 drop {coupled}/{total}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--night", help="Single night detailed plot (YYYY-MM-DD)")
    args = ap.parse_args()
    if args.night:
        analyze_single(args.night)
    else:
        analyze_all()


if __name__ == "__main__":
    main()
