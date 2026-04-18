#!/usr/bin/env python3
"""Analyze Garmin Connect sleep history.

Reads all *_sleepData.json files from the Garmin GDPR export, aggregates
metrics into yearly/monthly summaries, renders charts, and writes a
markdown report.
"""
from __future__ import annotations

import glob
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GARMIN_DIR = os.path.expanduser(
    "~/Downloads/eefa96d4-19bc-4be1-930c-f10a197cd658_1/DI_CONNECT/DI-Connect-Wellness"
)
REPORT_DIR = os.path.expanduser("~/Health-Check/reports")
CHART_DIR = os.path.join(REPORT_DIR, "garmin-sleep-charts")
TAIPEI = timezone(timedelta(hours=8))


def parse_gmt(ts: str | None):
    if not ts:
        return None
    # Garmin format: 2026-01-09T15:03:10.0
    return datetime.fromisoformat(ts.replace(".0", "")).replace(tzinfo=timezone.utc)


def load_nights():
    nights = []
    seen = set()
    for path in sorted(glob.glob(os.path.join(GARMIN_DIR, "*sleepData.json"))):
        with open(path) as f:
            data = json.load(f)
        for r in data:
            cal = r.get("calendarDate")
            if not cal or cal in seen:
                continue
            seen.add(cal)
            start = parse_gmt(r.get("sleepStartTimestampGMT"))
            end = parse_gmt(r.get("sleepEndTimestampGMT"))
            duration_s = (
                (r.get("deepSleepSeconds") or 0)
                + (r.get("lightSleepSeconds") or 0)
                + (r.get("remSleepSeconds") or 0)
            )
            if duration_s == 0:
                continue
            scores = r.get("sleepScores") or {}
            spo2 = r.get("spo2SleepSummary") or {}
            nights.append(
                {
                    "date": datetime.strptime(cal, "%Y-%m-%d").date(),
                    "start_local": start.astimezone(TAIPEI) if start else None,
                    "end_local": end.astimezone(TAIPEI) if end else None,
                    "deep_s": r.get("deepSleepSeconds") or 0,
                    "light_s": r.get("lightSleepSeconds") or 0,
                    "rem_s": r.get("remSleepSeconds") or 0,
                    "awake_s": r.get("awakeSleepSeconds") or 0,
                    "total_sleep_s": duration_s,
                    "awake_count": r.get("awakeCount"),
                    "restless": r.get("restlessMomentCount"),
                    "avg_stress": r.get("avgSleepStress"),
                    "avg_resp": r.get("averageRespiration"),
                    "low_resp": r.get("lowestRespiration"),
                    "high_resp": r.get("highestRespiration"),
                    "overall_score": scores.get("overallScore"),
                    "quality_score": scores.get("qualityScore"),
                    "duration_score": scores.get("durationScore"),
                    "recovery_score": scores.get("recoveryScore"),
                    "feedback": scores.get("feedback"),
                    "avg_spo2": spo2.get("averageSPO2"),
                    "low_spo2": spo2.get("lowestSPO2"),
                    "avg_hr": spo2.get("averageHR"),
                    "breathing_disruption": r.get("breathingDisruptionSeverity"),
                }
            )
    nights.sort(key=lambda n: n["date"])
    return nights


def group_by(nights, key_fn):
    g = defaultdict(list)
    for n in nights:
        g[key_fn(n)].append(n)
    return g


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def fmt_hours(seconds):
    if seconds is None:
        return "—"
    h = seconds / 3600
    return f"{h:.2f}h"


def fmt_hm(seconds):
    if seconds is None:
        return "—"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    return f"{h}h{m:02d}m"


def fmt_num(x, digits=1):
    return f"{x:.{digits}f}" if x is not None else "—"


def chart_monthly_duration(nights):
    by_month = group_by(nights, lambda n: n["date"].strftime("%Y-%m"))
    months = sorted(by_month)
    vals = [mean([n["total_sleep_s"] / 3600 for n in by_month[m]]) for m in months]
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(months, vals, color="#2b6cb0", linewidth=1.5)
    ax.axhline(7, color="#38a169", linestyle="--", linewidth=1, label="7h target")
    ax.axhline(6, color="#e53e3e", linestyle="--", linewidth=1, label="6h floor")
    ax.set_title("Monthly Average Sleep Duration")
    ax.set_ylabel("Hours")
    ax.set_xticks(range(0, len(months), max(1, len(months) // 12)))
    ax.set_xticklabels(
        [months[i] for i in range(0, len(months), max(1, len(months) // 12))],
        rotation=45, ha="right",
    )
    ax.legend(loc="lower left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(CHART_DIR, "01_monthly_duration.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def chart_yearly_stages(nights):
    by_year = group_by(nights, lambda n: n["date"].year)
    years = sorted(by_year)
    deep = [mean([n["deep_s"] / 60 for n in by_year[y]]) for y in years]
    light = [mean([n["light_s"] / 60 for n in by_year[y]]) for y in years]
    rem = [mean([n["rem_s"] / 60 for n in by_year[y]]) for y in years]
    awake = [mean([n["awake_s"] / 60 for n in by_year[y]]) for y in years]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(years))
    ax.bar(x, deep, label="Deep", color="#1a365d")
    ax.bar(x, light, bottom=deep, label="Light", color="#4299e1")
    ax.bar(x, rem, bottom=np.array(deep) + np.array(light), label="REM", color="#9f7aea")
    ax.bar(
        x, awake,
        bottom=np.array(deep) + np.array(light) + np.array(rem),
        label="Awake", color="#f56565",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_title("Yearly Average Sleep Stage Composition (minutes)")
    ax.set_ylabel("Minutes")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    out = os.path.join(CHART_DIR, "02_yearly_stages.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def chart_score_trend(nights):
    nights_with = [n for n in nights if n["overall_score"] is not None]
    if not nights_with:
        return None
    by_month = group_by(nights_with, lambda n: n["date"].strftime("%Y-%m"))
    months = sorted(by_month)
    vals = [mean([n["overall_score"] for n in by_month[m]]) for m in months]
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(months, vals, color="#805ad5", linewidth=1.5)
    ax.fill_between(months, vals, alpha=0.2, color="#805ad5")
    for cutoff, label, color in [(80, "Good", "#38a169"), (60, "Fair", "#d69e2e"), (50, "Poor", "#e53e3e")]:
        ax.axhline(cutoff, color=color, linestyle="--", linewidth=1, alpha=0.6, label=f"{label} ({cutoff})")
    ax.set_title("Monthly Average Sleep Score")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 100)
    step = max(1, len(months) // 12)
    ax.set_xticks(range(0, len(months), step))
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
    ax.legend(loc="lower left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(CHART_DIR, "03_score_trend.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def chart_spo2_distribution(nights):
    lows = [n["low_spo2"] for n in nights if n["low_spo2"] is not None]
    if not lows:
        return None
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(lows, bins=range(70, 101), color="#319795", edgecolor="white")
    ax.axvline(90, color="#e53e3e", linestyle="--", label="90% clinical threshold")
    ax.axvline(np.mean(lows), color="#2b6cb0", linestyle="-", label=f"Mean {np.mean(lows):.1f}%")
    ax.set_title("Distribution of Lowest SpO2 per Night")
    ax.set_xlabel("Lowest SpO2 (%)")
    ax.set_ylabel("Nights")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    out = os.path.join(CHART_DIR, "04_spo2_distribution.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def chart_dow_pattern(nights):
    dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    by_dow = group_by(nights, lambda n: n["date"].weekday())
    durations = [mean([n["total_sleep_s"] / 3600 for n in by_dow.get(i, [])]) for i in range(7)]
    scores = [mean([n["overall_score"] for n in by_dow.get(i, []) if n["overall_score"] is not None]) for i in range(7)]
    fig, ax1 = plt.subplots(figsize=(10, 4))
    x = np.arange(7)
    bars = ax1.bar(x - 0.2, durations, width=0.4, color="#2b6cb0", label="Duration (h)")
    ax1.set_ylabel("Hours", color="#2b6cb0")
    ax1.set_xticks(x)
    ax1.set_xticklabels(dow_labels)
    ax1.set_ylim(0, max(durations) * 1.15 if durations else 10)
    ax2 = ax1.twinx()
    ax2.bar(x + 0.2, scores, width=0.4, color="#805ad5", label="Score")
    ax2.set_ylabel("Score", color="#805ad5")
    ax2.set_ylim(0, 100)
    ax1.set_title("Day-of-Week Pattern (calendar date)")
    ax1.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    out = os.path.join(CHART_DIR, "05_dow_pattern.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def chart_bedtime_heatmap(nights):
    local = [n for n in nights if n["start_local"] is not None]
    if not local:
        return None
    months = sorted({n["date"].strftime("%Y-%m") for n in local})
    month_idx = {m: i for i, m in enumerate(months)}
    # Bedtime: hour of start_local, 18-29 range (6pm - 5am)
    grid = np.full((12, len(months)), np.nan)
    counts = np.zeros((12, len(months)))
    for n in local:
        h = n["start_local"].hour
        # Normalize: 18..23 → 0..5, 0..5 → 6..11
        bucket = h - 18 if h >= 18 else h + 6
        if 0 <= bucket < 12:
            m = month_idx[n["date"].strftime("%Y-%m")]
            if np.isnan(grid[bucket, m]):
                grid[bucket, m] = 0
            grid[bucket, m] += 1
            counts[bucket, m] += 1
    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(grid, aspect="auto", cmap="viridis", interpolation="nearest")
    bedtime_labels = ["18", "19", "20", "21", "22", "23", "00", "01", "02", "03", "04", "05"]
    ax.set_yticks(range(12))
    ax.set_yticklabels(bedtime_labels)
    step = max(1, len(months) // 16)
    ax.set_xticks(range(0, len(months), step))
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
    ax.set_title("Bedtime Frequency by Month (Taipei time, hour sleep started)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Bedtime hour")
    fig.colorbar(im, ax=ax, label="Nights")
    fig.tight_layout()
    out = os.path.join(CHART_DIR, "06_bedtime_heatmap.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def build_yearly_table(nights):
    by_year = group_by(nights, lambda n: n["date"].year)
    rows = []
    for y in sorted(by_year):
        ns = by_year[y]
        rows.append({
            "year": y,
            "nights": len(ns),
            "duration": mean([n["total_sleep_s"] for n in ns]),
            "deep": mean([n["deep_s"] for n in ns]),
            "light": mean([n["light_s"] for n in ns]),
            "rem": mean([n["rem_s"] for n in ns]),
            "awake": mean([n["awake_s"] for n in ns]),
            "score": mean([n["overall_score"] for n in ns if n["overall_score"] is not None]),
            "resp": mean([n["avg_resp"] for n in ns]),
            "avg_spo2": mean([n["avg_spo2"] for n in ns]),
            "low_spo2": mean([n["low_spo2"] for n in ns]),
            "stress": mean([n["avg_stress"] for n in ns]),
            "awakenings": mean([n["awake_count"] for n in ns if n["awake_count"] is not None]),
        })
    return rows


def detect_gaps(nights):
    """Return list of (start, end, days) for gaps > 14 days between consecutive nights."""
    gaps = []
    for a, b in zip(nights, nights[1:]):
        delta = (b["date"] - a["date"]).days
        if delta > 14:
            gaps.append((a["date"], b["date"], delta - 1))
    return gaps


def write_report(nights, charts):
    total = len(nights)
    span_start = nights[0]["date"]
    span_end = nights[-1]["date"]
    total_days = (span_end - span_start).days + 1
    coverage = total / total_days * 100

    overall_duration = mean([n["total_sleep_s"] for n in nights])
    overall_score = mean([n["overall_score"] for n in nights if n["overall_score"] is not None])
    overall_deep = mean([n["deep_s"] for n in nights])
    overall_light = mean([n["light_s"] for n in nights])
    overall_rem = mean([n["rem_s"] for n in nights])
    overall_awake = mean([n["awake_s"] for n in nights])

    yearly = build_yearly_table(nights)
    gaps = detect_gaps(nights)

    # Low quality / SpO2 / short sleep counts
    low_score = [n for n in nights if (n["overall_score"] or 100) < 50]
    short_sleep = [n for n in nights if n["total_sleep_s"] < 6 * 3600]
    hypoxic = [n for n in nights if n["low_spo2"] is not None and n["low_spo2"] < 90]

    # Feedback distribution
    fb = defaultdict(int)
    for n in nights:
        if n["feedback"]:
            fb[n["feedback"]] += 1

    # Breathing disruption
    bd = defaultdict(int)
    for n in nights:
        if n["breathing_disruption"]:
            bd[n["breathing_disruption"]] += 1

    # Recent vs historic (last 90 days vs rest)
    from datetime import date as _date
    cutoff = span_end - timedelta(days=90)
    recent = [n for n in nights if n["date"] > cutoff]
    historic = [n for n in nights if n["date"] <= cutoff]

    def bucket_stats(ns):
        return {
            "n": len(ns),
            "dur": mean([n["total_sleep_s"] for n in ns]),
            "score": mean([n["overall_score"] for n in ns if n["overall_score"] is not None]),
            "deep_pct": (
                mean([n["deep_s"] / n["total_sleep_s"] * 100 for n in ns if n["total_sleep_s"]]) or 0
            ),
            "rem_pct": (
                mean([n["rem_s"] / n["total_sleep_s"] * 100 for n in ns if n["total_sleep_s"]]) or 0
            ),
        }

    r_stat = bucket_stats(recent)
    h_stat = bucket_stats(historic)

    md = []
    md.append("# Garmin Sleep History Analysis")
    md.append("")
    md.append(f"_Generated: {datetime.now(TAIPEI).strftime('%Y-%m-%d %H:%M')} (Taipei)_  ")
    md.append(f"_Source: Garmin GDPR export, user 72396565_")
    md.append("")
    md.append("## 1. Coverage")
    md.append("")
    md.append(f"- **Date range**: {span_start} → {span_end} ({total_days} calendar days)")
    md.append(f"- **Nights with valid sleep data**: {total} ({coverage:.1f}% coverage)")
    md.append(f"- **Data gaps (>14 consecutive days missing)**: {len(gaps)}")
    if gaps:
        md.append("")
        md.append("  | Gap start | Gap end | Days missing |")
        md.append("  |---|---|---|")
        for s, e, d in gaps[:10]:
            md.append(f"  | {s} | {e} | {d} |")
        if len(gaps) > 10:
            md.append(f"  | ...{len(gaps) - 10} more... | | |")
    md.append("")

    md.append("## 2. Overall Averages (full history)")
    md.append("")
    md.append(f"- **Sleep duration**: {fmt_hm(overall_duration)} per night")
    md.append(f"- **Sleep score**: {fmt_num(overall_score)}")
    md.append(f"- **Deep sleep**: {fmt_hm(overall_deep)} ({overall_deep/overall_duration*100:.1f}% of total sleep)")
    md.append(f"- **Light sleep**: {fmt_hm(overall_light)} ({overall_light/overall_duration*100:.1f}%)")
    md.append(f"- **REM sleep**: {fmt_hm(overall_rem)} ({overall_rem/overall_duration*100:.1f}%)")
    md.append(f"- **Awake in bed**: {fmt_hm(overall_awake)}")
    md.append("")

    md.append("## 3. Yearly Breakdown")
    md.append("")
    md.append("| Year | Nights | Duration | Deep | REM | Awake | Score | Resp (bpm) | Avg SpO2 | Low SpO2 | Stress |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in yearly:
        md.append(
            f"| {r['year']} | {r['nights']} | {fmt_hm(r['duration'])} | "
            f"{fmt_hm(r['deep'])} | {fmt_hm(r['rem'])} | {fmt_hm(r['awake'])} | "
            f"{fmt_num(r['score'])} | {fmt_num(r['resp'])} | "
            f"{fmt_num(r['avg_spo2'])} | {fmt_num(r['low_spo2'])} | {fmt_num(r['stress'])} |"
        )
    md.append("")

    md.append("## 4. Recent vs Historical")
    md.append("")
    md.append(f"- **Last 90 days** ({r_stat['n']} nights): {fmt_hm(r_stat['dur'])} avg, score {fmt_num(r_stat['score'])}, deep {fmt_num(r_stat['deep_pct'])}%, REM {fmt_num(r_stat['rem_pct'])}%")
    md.append(f"- **Prior history** ({h_stat['n']} nights): {fmt_hm(h_stat['dur'])} avg, score {fmt_num(h_stat['score'])}, deep {fmt_num(h_stat['deep_pct'])}%, REM {fmt_num(h_stat['rem_pct'])}%")
    if r_stat["dur"] and h_stat["dur"]:
        diff_min = (r_stat["dur"] - h_stat["dur"]) / 60
        md.append(f"- **Δ Duration**: {diff_min:+.0f} min vs historic")
    if r_stat["score"] and h_stat["score"]:
        md.append(f"- **Δ Score**: {r_stat['score'] - h_stat['score']:+.1f}")
    md.append("")

    md.append("## 5. Flags & Outliers")
    md.append("")
    md.append(f"- **Poor nights (score < 50)**: {len(low_score)} ({len(low_score)/total*100:.1f}%)")
    md.append(f"- **Short sleep (<6h)**: {len(short_sleep)} ({len(short_sleep)/total*100:.1f}%)")
    md.append(f"- **Hypoxic nights (lowest SpO2 < 90%)**: {len(hypoxic)} ({len(hypoxic)/sum(1 for n in nights if n['low_spo2'] is not None)*100:.1f}% of measured)")
    md.append("")
    if fb:
        md.append("### Garmin feedback distribution")
        md.append("")
        md.append("| Feedback tag | Nights | % |")
        md.append("|---|---|---|")
        total_fb = sum(fb.values())
        for tag, cnt in sorted(fb.items(), key=lambda x: -x[1]):
            md.append(f"| {tag} | {cnt} | {cnt/total_fb*100:.1f}% |")
        md.append("")
    if bd:
        md.append("### Breathing disruption severity")
        md.append("")
        md.append("| Severity | Nights |")
        md.append("|---|---|")
        for tag, cnt in sorted(bd.items(), key=lambda x: -x[1]):
            md.append(f"| {tag} | {cnt} |")
        md.append("")

    md.append("## 6. Charts")
    md.append("")
    for title, path in charts:
        if path is None:
            continue
        rel = os.path.relpath(path, REPORT_DIR)
        md.append(f"### {title}")
        md.append("")
        md.append(f"![{title}]({rel})")
        md.append("")

    md.append("## 7. Notes on Data Quality")
    md.append("")
    md.append("- All timestamps converted from GMT to Taipei (UTC+8) for bedtime analysis.")
    md.append("- Nights where all four stage counters were zero were treated as no-data and excluded from averages.")
    md.append("- `sleepScores` only populated from mid-2019 onward; earlier years show score as — in tables.")
    md.append("- SpO2 data only available when a compatible device (watch with Pulse Ox) was worn.")
    md.append("")

    out = os.path.join(REPORT_DIR, "garmin-sleep-analysis.md")
    with open(out, "w") as f:
        f.write("\n".join(md))
    return out


def main():
    print(f"Loading from: {GARMIN_DIR}")
    nights = load_nights()
    print(f"Parsed {len(nights)} nights with valid sleep data")
    print(f"Range: {nights[0]['date']} → {nights[-1]['date']}")

    os.makedirs(CHART_DIR, exist_ok=True)
    charts = [
        ("Monthly Average Sleep Duration", chart_monthly_duration(nights)),
        ("Yearly Sleep Stage Composition", chart_yearly_stages(nights)),
        ("Monthly Sleep Score Trend", chart_score_trend(nights)),
        ("Lowest SpO2 Distribution", chart_spo2_distribution(nights)),
        ("Day-of-Week Pattern", chart_dow_pattern(nights)),
        ("Bedtime Frequency Heatmap", chart_bedtime_heatmap(nights)),
    ]
    for title, path in charts:
        print(f"  chart: {title} → {path}")

    report = write_report(nights, charts)
    print(f"\nReport written: {report}")


if __name__ == "__main__":
    main()
