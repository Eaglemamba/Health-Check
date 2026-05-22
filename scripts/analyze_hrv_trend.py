"""
HRV trend analysis — detect statistically-significant drift in avgOvernightHrv.

Garmin's avgOvernightHrv is a per-night RMSSD approximation. This script:
  1. Loads all available data/garmin/*.json
  2. Extracts (date, avgOvernightHrv) pairs
  3. Runs 3 independent trend tests: linear regression, first-vs-second-half
     Mann-Whitney, Mann-Kendall
  4. Saves a trend chart with regression line + 14-day rolling mean
  5. Prints a markdown-ready summary for embedding into weekly reviews

Usage:
  python scripts/analyze_hrv_trend.py            # all available nights
  python scripts/analyze_hrv_trend.py --days 28  # last 28 nights only
  python scripts/analyze_hrv_trend.py --md       # markdown snippet only
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats as st

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
OUT_DIR = ROOT / "reviews" / "daily" / "spo2"  # reuse same folder for trend images
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_hrv(days=None):
    rows = []
    for p in sorted(DATA_DIR.rglob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        sleep = d.get("sleep") or {}
        h = sleep.get("avgOvernightHrv")
        if h is not None:
            rows.append((p.stem, float(h)))
    if days:
        rows = rows[-days:]
    return rows


def mann_kendall(arr):
    """Non-parametric monotonic trend test (S, Z, p)."""
    n = len(arr)
    s = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            s += np.sign(arr[j] - arr[i])
    var = n * (n - 1) * (2 * n + 5) / 18
    if s > 0:
        z = (s - 1) / np.sqrt(var)
    elif s < 0:
        z = (s + 1) / np.sqrt(var)
    else:
        z = 0
    p = 2 * (1 - st.norm.cdf(abs(z)))
    return int(s), float(z), float(p)


def analyze(rows, md_only=False):
    if len(rows) < 7:
        print(f"Need >= 7 nights, got {len(rows)}")
        return

    dates = [r[0] for r in rows]
    hrvs = np.array([r[1] for r in rows], dtype=float)
    n = len(rows)

    # 1. Linear regression
    x = np.arange(n)
    slope, intercept, r, pval, se = st.linregress(x, hrvs)
    total_drift = slope * (n - 1)

    # 2. First vs second half
    half = n // 2
    fh, sh = hrvs[:half], hrvs[half:]
    u_two, p_two = st.mannwhitneyu(fh, sh, alternative="two-sided")
    direction = "decreasing" if sh.mean() < fh.mean() else "increasing"

    # 3. Mann-Kendall
    s, z, pmk = mann_kendall(hrvs)

    # 14-day rolling mean
    if n >= 14:
        roll = np.convolve(hrvs, np.ones(14) / 14, mode="valid")
        roll_x = np.arange(13, n)
    else:
        roll, roll_x = None, None

    # Significance count
    sig = sum([pval < 0.05, p_two < 0.05, pmk < 0.05])
    verdict_en = {
        3: "CONFIRMED (3/3 tests significant)",
        2: "LIKELY (2/3 tests significant)",
        1: "WEAK (1/3 test significant)",
        0: "NO TREND (all p > 0.05)",
    }[sig]

    md = []
    md.append(f"### HRV trend — {dates[0]} → {dates[-1]} (N={n} nights)\n")
    md.append(f"**Mean = {hrvs.mean():.2f} ms · Median = {np.median(hrvs):.0f} · Range {hrvs.min():.0f}–{hrvs.max():.0f} · Verdict: {verdict_en}**\n")
    md.append("")
    md.append("| Test | Result | p | Significant? |")
    md.append("|---|---|---|---|")
    md.append(f"| Linear regression | slope = {slope:+.4f} ms/night · drift {total_drift:+.2f} ms | {pval:.4f} | {'✓' if pval < 0.05 else '✗'} |")
    md.append(f"| First vs second half ({direction}) | {fh.mean():.2f} → {sh.mean():.2f} ms | {p_two:.4f} | {'✓' if p_two < 0.05 else '✗'} |")
    md.append(f"| Mann-Kendall | S = {s}, Z = {z:+.2f} | {pmk:.4f} | {'✓' if pmk < 0.05 else '✗'} |")
    md.append("")
    md.append(f"![HRV trend](daily/spo2/hrv_trend.png)")
    md_text = "\n".join(md)

    if md_only:
        print(md_text)
        return

    print(f"\n=== HRV trend analysis — {n} nights ({dates[0]} → {dates[-1]}) ===\n")
    print(f"Mean = {hrvs.mean():.2f} ms, median = {np.median(hrvs):.1f}, std = {hrvs.std():.2f}")
    print(f"Range = {hrvs.min():.0f}–{hrvs.max():.0f} ms\n")
    print(f"[1] Linear regression: slope = {slope:+.4f} ms/night, r = {r:+.3f}, p = {pval:.4f}")
    print(f"    Total drift over {n} nights: {total_drift:+.2f} ms")
    print(f"[2] First half (N={len(fh)}) mean = {fh.mean():.2f} vs second (N={len(sh)}) mean = {sh.mean():.2f}")
    print(f"    Mann-Whitney two-sided p = {p_two:.4f} ({direction})")
    print(f"[3] Mann-Kendall: S = {s}, Z = {z:+.2f}, p = {pmk:.4f}")
    print(f"\nVerdict: {verdict_en}")

    # Plot
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(x, hrvs, "o-", color="#3a76d8", lw=1.4, ms=5, label="Nightly HRV")
    ax.plot(x, intercept + slope * x, "--", color="#ff375f", lw=1.5,
            label=f"Linear fit (slope {slope:+.3f} ms/night, p={pval:.3f})")
    if roll is not None:
        ax.plot(roll_x, roll, "-", color="#2a9d8f", lw=2.5, label="14-day rolling mean")
    ax.axhline(hrvs.mean(), color="#888", ls=":", lw=1, alpha=0.6, label=f"Period mean {hrvs.mean():.1f}")

    # Mark deload-worthy zone
    ax.axhspan(0, 18, color="#ffd0d8", alpha=0.25, zorder=0)

    show_every = max(1, n // 14)
    ax.set_xticks(x[::show_every])
    ax.set_xticklabels([dates[i][5:] for i in x[::show_every]], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("avgOvernightHrv (ms)")
    ax.set_title(f"HRV trend — {dates[0]} → {dates[-1]} ({n} nights) · Verdict: {verdict_en}")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left", fontsize=9)
    ax.set_ylim(max(0, hrvs.min() - 3), hrvs.max() + 3)
    plt.tight_layout()
    out = OUT_DIR / "hrv_trend.png"
    plt.savefig(out, dpi=140, bbox_inches="tight")
    print(f"\nSaved: {out}")
    print(f"\n--- Markdown snippet for weekly review (copy block below) ---\n")
    print(md_text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=None, help="Limit to last N nights")
    ap.add_argument("--md", action="store_true", help="Markdown snippet only (no PNG)")
    args = ap.parse_args()

    rows = load_hrv(days=args.days)
    if not rows:
        print("No HRV data found in data/garmin/*.json")
        return
    analyze(rows, md_only=args.md)


if __name__ == "__main__":
    main()
