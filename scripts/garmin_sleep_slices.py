#!/usr/bin/env python3
"""Deep-dive slices on Garmin sleep data.

Builds on analyze_garmin_sleep.py data loader to answer:
  1. What separates good (score>=70) from poor (<50) nights?
  2. Bedtime hour vs sleep score.
  3. Weekday vs weekend.
  4. 2025 vs 2026 YoY.

Writes a markdown appendix and 3 extra charts.
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.expanduser("~/Health-Check/scripts"))
from analyze_garmin_sleep import load_nights, mean, fmt_hm, fmt_num, CHART_DIR, REPORT_DIR


def percentile(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = max(0, min(len(xs) - 1, int(round((p / 100) * (len(xs) - 1)))))
    return xs[k]


def corr(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    x = np.array([p[0] for p in pairs], dtype=float)
    y = np.array([p[1] for p in pairs], dtype=float)
    x -= x.mean()
    y -= y.mean()
    denom = (np.sqrt((x * x).sum()) * np.sqrt((y * y).sum()))
    return float((x * y).sum() / denom) if denom else None


def bedtime_hour(n):
    """Local Taipei bedtime as a continuous number 18.0..29.99 (wraps midnight)."""
    s = n["start_local"]
    if s is None:
        return None
    h = s.hour + s.minute / 60
    return h if h >= 12 else h + 24  # treat 01:00 as 25.0 for ordering


def slice_good_vs_poor(nights):
    scored = [n for n in nights if n["overall_score"] is not None]
    good = [n for n in scored if n["overall_score"] >= 70]
    poor = [n for n in scored if n["overall_score"] < 50]

    def stats(ns):
        return {
            "n": len(ns),
            "dur": mean([n["total_sleep_s"] for n in ns]),
            "deep_pct": mean([n["deep_s"] / n["total_sleep_s"] * 100 for n in ns if n["total_sleep_s"]]),
            "rem_pct": mean([n["rem_s"] / n["total_sleep_s"] * 100 for n in ns if n["total_sleep_s"]]),
            "awake_pct": mean([n["awake_s"] / (n["total_sleep_s"] + n["awake_s"]) * 100 for n in ns if (n["total_sleep_s"] + n["awake_s"])]),
            "awakenings": mean([n["awake_count"] for n in ns if n["awake_count"] is not None]),
            "restless": mean([n["restless"] for n in ns if n["restless"] is not None]),
            "stress": mean([n["avg_stress"] for n in ns if n["avg_stress"] is not None]),
            "resp": mean([n["avg_resp"] for n in ns if n["avg_resp"] is not None]),
            "bedtime": mean([bedtime_hour(n) for n in ns]),
        }

    return stats(good), stats(poor)


def slice_bedtime_vs_score(nights):
    scored = [n for n in nights if n["overall_score"] is not None and n["start_local"] is not None]
    buckets = defaultdict(list)
    for n in scored:
        bh = bedtime_hour(n)
        # Bucket by floor hour: 20, 21, 22, 23, 0(24), 1(25), 2(26), 3+
        b = int(bh)
        buckets[b].append(n["overall_score"])
    rows = []
    for b in sorted(buckets):
        rows.append({
            "bucket": b,
            "label": f"{b % 24:02d}:00",
            "n": len(buckets[b]),
            "mean": float(np.mean(buckets[b])),
            "median": float(np.median(buckets[b])),
        })
    return rows, buckets


def slice_weekday_vs_weekend(nights):
    scored = [n for n in nights if n["overall_score"] is not None]
    wd = [n for n in scored if n["date"].weekday() < 5]
    we = [n for n in scored if n["date"].weekday() >= 5]

    def stats(ns):
        return {
            "n": len(ns),
            "dur": mean([n["total_sleep_s"] for n in ns]),
            "score": mean([n["overall_score"] for n in ns]),
            "bedtime": mean([bedtime_hour(n) for n in ns if n["start_local"] is not None]),
            "short_pct": sum(1 for n in ns if n["total_sleep_s"] < 6 * 3600) / len(ns) * 100 if ns else 0,
        }

    return stats(wd), stats(we)


def slice_yoy_2025_2026(nights):
    y25 = [n for n in nights if n["date"].year == 2025]
    y26 = [n for n in nights if n["date"].year == 2026]

    def stats(ns):
        return {
            "n": len(ns),
            "dur": mean([n["total_sleep_s"] for n in ns]),
            "score": mean([n["overall_score"] for n in ns if n["overall_score"] is not None]),
            "deep_pct": mean([n["deep_s"] / n["total_sleep_s"] * 100 for n in ns if n["total_sleep_s"]]),
            "rem_pct": mean([n["rem_s"] / n["total_sleep_s"] * 100 for n in ns if n["total_sleep_s"]]),
            "short_pct": sum(1 for n in ns if n["total_sleep_s"] < 6 * 3600) / len(ns) * 100 if ns else 0,
            "stress": mean([n["avg_stress"] for n in ns if n["avg_stress"] is not None]),
            "resp": mean([n["avg_resp"] for n in ns if n["avg_resp"] is not None]),
            "avg_spo2": mean([n["avg_spo2"] for n in ns if n["avg_spo2"] is not None]),
            "low_spo2": mean([n["low_spo2"] for n in ns if n["low_spo2"] is not None]),
        }

    return stats(y25), stats(y26)


def chart_bedtime_boxes(buckets, out):
    keys = sorted(buckets)
    data = [buckets[k] for k in keys]
    labels = [f"{k % 24:02d}" for k in keys]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    bp = ax.boxplot(data, labels=labels, patch_artist=True)
    for patch in bp["boxes"]:
        patch.set_facecolor("#4299e1")
        patch.set_alpha(0.6)
    ax.axhline(70, color="#38a169", linestyle="--", linewidth=1, label="Good (70)")
    ax.axhline(50, color="#e53e3e", linestyle="--", linewidth=1, label="Poor (50)")
    ax.set_title("Sleep Score Distribution by Bedtime Hour (Taipei)")
    ax.set_xlabel("Bedtime hour")
    ax.set_ylabel("Overall score")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def chart_duration_score_scatter(nights, out):
    scored = [n for n in nights if n["overall_score"] is not None]
    xs = [n["total_sleep_s"] / 3600 for n in scored]
    ys = [n["overall_score"] for n in scored]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(xs, ys, alpha=0.25, s=14, color="#2b6cb0")
    # Trend line
    if len(xs) > 1:
        coef = np.polyfit(xs, ys, 1)
        xx = np.linspace(min(xs), max(xs), 50)
        ax.plot(xx, np.polyval(coef, xx), color="#e53e3e", linewidth=2, label=f"slope={coef[0]:.1f} pts/hour")
    ax.axhline(70, color="#38a169", linestyle="--", linewidth=1, alpha=0.5)
    ax.axvline(7, color="#38a169", linestyle="--", linewidth=1, alpha=0.5)
    ax.set_xlabel("Sleep duration (hours)")
    ax.set_ylabel("Overall score")
    ax.set_title("Sleep Duration vs Score")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def chart_yoy_bars(y25, y26, out):
    metrics = ["dur_h", "score", "deep_pct", "rem_pct", "short_pct"]
    labels = ["Duration (h)", "Score", "Deep %", "REM %", "<6h nights %"]
    v25 = [y25["dur"] / 3600, y25["score"] or 0, y25["deep_pct"] or 0, y25["rem_pct"] or 0, y25["short_pct"]]
    v26 = [y26["dur"] / 3600, y26["score"] or 0, y26["deep_pct"] or 0, y26["rem_pct"] or 0, y26["short_pct"]]
    x = np.arange(len(metrics))
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(x - 0.2, v25, width=0.4, label="2025", color="#718096")
    ax.bar(x + 0.2, v26, width=0.4, label="2026 YTD", color="#2b6cb0")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15)
    ax.set_title("2025 vs 2026 YTD")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    # Annotate
    for i, (a, b) in enumerate(zip(v25, v26)):
        ax.text(i - 0.2, a, f"{a:.1f}", ha="center", va="bottom", fontsize=8)
        ax.text(i + 0.2, b, f"{b:.1f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def main():
    nights = load_nights()
    scored = [n for n in nights if n["overall_score"] is not None]

    good, poor = slice_good_vs_poor(nights)
    bed_rows, bed_buckets = slice_bedtime_vs_score(nights)
    wd, we = slice_weekday_vs_weekend(nights)
    y25, y26 = slice_yoy_2025_2026(nights)

    # Correlations
    dur_score_r = corr([n["total_sleep_s"] for n in scored], [n["overall_score"] for n in scored])
    bed_score_r = corr([bedtime_hour(n) for n in scored], [n["overall_score"] for n in scored])
    stress_score_r = corr([n["avg_stress"] for n in scored], [n["overall_score"] for n in scored])
    resp_score_r = corr([n["avg_resp"] for n in scored], [n["overall_score"] for n in scored])

    # Charts
    os.makedirs(CHART_DIR, exist_ok=True)
    c_bed = os.path.join(CHART_DIR, "07_bedtime_score_box.png")
    c_scatter = os.path.join(CHART_DIR, "08_duration_score_scatter.png")
    c_yoy = os.path.join(CHART_DIR, "09_yoy_2025_2026.png")
    chart_bedtime_boxes(bed_buckets, c_bed)
    chart_duration_score_scatter(nights, c_scatter)
    chart_yoy_bars(y25, y26, c_yoy)

    md = []
    md.append("\n---\n")
    md.append("# Appendix: Deep-Dive Slices")
    md.append("")
    md.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")
    md.append("")

    md.append("## A. Good vs Poor Nights")
    md.append("")
    md.append(f"_Good = score ≥ 70 ({good['n']} nights) · Poor = score < 50 ({poor['n']} nights)_")
    md.append("")
    md.append("| Metric | Good | Poor | Δ (Good − Poor) |")
    md.append("|---|---|---|---|")
    md.append(f"| Duration | {fmt_hm(good['dur'])} | {fmt_hm(poor['dur'])} | {(good['dur'] - poor['dur'])/60:+.0f} min |")
    md.append(f"| Deep % | {fmt_num(good['deep_pct'])} | {fmt_num(poor['deep_pct'])} | {(good['deep_pct'] - poor['deep_pct']):+.1f} |")
    md.append(f"| REM % | {fmt_num(good['rem_pct'])} | {fmt_num(poor['rem_pct'])} | {(good['rem_pct'] - poor['rem_pct']):+.1f} |")
    md.append(f"| Awake % (in bed) | {fmt_num(good['awake_pct'])} | {fmt_num(poor['awake_pct'])} | {(good['awake_pct'] - poor['awake_pct']):+.1f} |")
    md.append(f"| Awakenings | {fmt_num(good['awakenings'])} | {fmt_num(poor['awakenings'])} | {(good['awakenings'] - poor['awakenings']):+.1f} |")
    md.append(f"| Restless moments | {fmt_num(good['restless'])} | {fmt_num(poor['restless'])} | {(good['restless'] - poor['restless']):+.0f} |")
    md.append(f"| Avg stress | {fmt_num(good['stress'])} | {fmt_num(poor['stress'])} | {(good['stress'] - poor['stress']):+.1f} |")
    md.append(f"| Avg respiration | {fmt_num(good['resp'])} | {fmt_num(poor['resp'])} | {(good['resp'] - poor['resp']):+.1f} |")
    md.append(f"| Bedtime (local) | {good['bedtime']:.2f}h | {poor['bedtime']:.2f}h | {(good['bedtime'] - poor['bedtime']):+.2f}h |")
    md.append("")
    md.append("**Correlations with overall score** (Pearson r, n=%d):" % len(scored))
    md.append(f"- Duration: r = {dur_score_r:.3f}")
    md.append(f"- Bedtime hour: r = {bed_score_r:+.3f}")
    md.append(f"- Avg stress: r = {stress_score_r:+.3f}")
    md.append(f"- Avg respiration: r = {resp_score_r:+.3f}")
    md.append("")

    md.append("## B. Bedtime Hour vs Score")
    md.append("")
    md.append("| Bedtime hour | Nights | Mean score | Median |")
    md.append("|---|---|---|---|")
    for r in bed_rows:
        md.append(f"| {r['label']} | {r['n']} | {r['mean']:.1f} | {r['median']:.0f} |")
    md.append("")
    md.append(f"![Bedtime → Score](garmin-sleep-charts/07_bedtime_score_box.png)")
    md.append("")

    md.append("## C. Weekday vs Weekend")
    md.append("")
    md.append("| Metric | Weekday (Mon–Fri) | Weekend (Sat–Sun) |")
    md.append("|---|---|---|")
    md.append(f"| Nights | {wd['n']} | {we['n']} |")
    md.append(f"| Duration | {fmt_hm(wd['dur'])} | {fmt_hm(we['dur'])} |")
    md.append(f"| Score | {fmt_num(wd['score'])} | {fmt_num(we['score'])} |")
    md.append(f"| Bedtime | {wd['bedtime']:.2f}h | {we['bedtime']:.2f}h |")
    md.append(f"| <6h nights | {wd['short_pct']:.1f}% | {we['short_pct']:.1f}% |")
    md.append("")

    md.append("## D. 2025 vs 2026 YTD")
    md.append("")
    md.append("| Metric | 2025 | 2026 YTD | Δ |")
    md.append("|---|---|---|---|")
    md.append(f"| Nights | {y25['n']} | {y26['n']} | — |")
    md.append(f"| Duration | {fmt_hm(y25['dur'])} | {fmt_hm(y26['dur'])} | {(y26['dur'] - y25['dur'])/60:+.0f} min |")
    md.append(f"| Score | {fmt_num(y25['score'])} | {fmt_num(y26['score'])} | {(y26['score'] - y25['score']):+.1f} |")
    md.append(f"| Deep % | {fmt_num(y25['deep_pct'])} | {fmt_num(y26['deep_pct'])} | {(y26['deep_pct'] - y25['deep_pct']):+.1f} |")
    md.append(f"| REM % | {fmt_num(y25['rem_pct'])} | {fmt_num(y26['rem_pct'])} | {(y26['rem_pct'] - y25['rem_pct']):+.1f} |")
    md.append(f"| <6h nights | {y25['short_pct']:.1f}% | {y26['short_pct']:.1f}% | {(y26['short_pct'] - y25['short_pct']):+.1f} |")
    md.append(f"| Stress | {fmt_num(y25['stress'])} | {fmt_num(y26['stress'])} | {(y26['stress'] - y25['stress']):+.1f} |")
    md.append(f"| Avg respiration | {fmt_num(y25['resp'])} | {fmt_num(y26['resp'])} | {(y26['resp'] - y25['resp']):+.1f} |")
    md.append(f"| Avg SpO2 | {fmt_num(y25['avg_spo2'])} | {fmt_num(y26['avg_spo2'])} | {(y26['avg_spo2'] - y25['avg_spo2']):+.1f} |")
    md.append(f"| Low SpO2 | {fmt_num(y25['low_spo2'])} | {fmt_num(y26['low_spo2'])} | {(y26['low_spo2'] - y25['low_spo2']):+.1f} |")
    md.append("")
    md.append("![YoY 2025 vs 2026](garmin-sleep-charts/09_yoy_2025_2026.png)")
    md.append("")

    md.append("## E. Duration ↔ Score relationship")
    md.append("")
    md.append(f"![Duration vs Score](garmin-sleep-charts/08_duration_score_scatter.png)")
    md.append("")

    appendix = "\n".join(md)
    report_path = os.path.join(REPORT_DIR, "garmin-sleep-analysis.md")
    with open(report_path, "a") as f:
        f.write(appendix)
    print(f"Appended deep-dive to {report_path}")
    print(f"Charts: {c_bed}, {c_scatter}, {c_yoy}")

    # Print key findings to stdout
    print("\n=== KEY FINDINGS ===")
    print(f"Good vs Poor duration delta: +{(good['dur'] - poor['dur'])/60:.0f} min")
    print(f"Duration↔Score correlation: r = {dur_score_r:.3f}")
    print(f"Bedtime↔Score correlation: r = {bed_score_r:+.3f}")
    print(f"Stress↔Score correlation: r = {stress_score_r:+.3f}")
    best_bed = max(bed_rows, key=lambda r: r["mean"])
    print(f"Best bedtime bucket: {best_bed['label']} (mean score {best_bed['mean']:.1f}, n={best_bed['n']})")
    print(f"Weekday score: {wd['score']:.1f} | Weekend score: {we['score']:.1f}")
    print(f"YoY score: 2025={y25['score']:.1f} → 2026={y26['score']:.1f}")


if __name__ == "__main__":
    main()
