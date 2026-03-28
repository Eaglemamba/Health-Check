#!/usr/bin/env python3
"""Parse daily health records and generate health_dashboard.png."""

import re
import os
import glob
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def parse_daily_file(filepath):
    """Extract health data from a daily markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    data = {}

    # Date from filename
    basename = os.path.basename(filepath)
    date_str = basename.replace(".md", "")
    data["date"] = datetime.strptime(date_str, "%Y-%m-%d")

    # Weight
    m = re.search(r"\*\*今日：([\d.]+)\s*kg\*\*", content)
    data["weight"] = float(m.group(1)) if m else None

    # Sunday official weight — only mark if the record date is actually a Sunday
    data["weight_official"] = data["date"].weekday() == 6  # 6 = Sunday

    # Blood pressure - parse the table for 1st and 2nd readings
    bp_pattern = re.findall(
        r"\|\s*第([一二])次\s*\|\s*(\d+)?\s*\|\s*(\d+)?\s*\|\s*(\d+)?\s*\|",
        content,
    )
    data["bp1_sys"] = data["bp1_dia"] = data["bp1_hr"] = None
    data["bp2_sys"] = data["bp2_dia"] = data["bp2_hr"] = None

    for reading in bp_pattern:
        order, sys_val, dia_val, hr_val = reading
        if order == "一" and sys_val:
            data["bp1_sys"] = int(sys_val)
            data["bp1_dia"] = int(dia_val) if dia_val else None
            data["bp1_hr"] = int(hr_val) if hr_val else None
        elif order == "二" and sys_val:
            data["bp2_sys"] = int(sys_val)
            data["bp2_dia"] = int(dia_val) if dia_val else None
            data["bp2_hr"] = int(hr_val) if hr_val else None

    # Sleep Score
    m = re.search(r"Garmin Sleep Score[：:]\*?\*?\s*(\d+)\s*/\s*100", content)
    data["sleep_score"] = int(m.group(1)) if m else None

    # Body Battery
    m = re.search(r"Body Battery[^：:]*[：:]\*?\*?\s*(\d+)", content)
    data["body_battery"] = int(m.group(1)) if m else None

    return data


def generate_dashboard(data_list, output_path):
    """Generate the health dashboard PNG."""
    data_list.sort(key=lambda d: d["date"])

    # Filter to last 14 days max for readability
    if len(data_list) > 14:
        data_list = data_list[-14:]

    dates = [d["date"] for d in data_list]
    first_date = dates[0].strftime("%Y-%m-%d")
    last_date = dates[-1].strftime("%Y-%m-%d")
    n_days = (dates[-1] - dates[0]).days + 1

    # Dark theme
    plt.style.use("dark_background")
    fig, axes = plt.subplots(3, 1, figsize=(10, 11), dpi=180)
    fig.patch.set_facecolor("#0d1117")

    title = f"Health Tracking Dashboard\n{first_date} ~ {last_date} ({n_days} days)"
    fig.suptitle(title, fontsize=14, fontweight="bold", color="white", y=0.98)

    date_labels = [d.strftime("%m/%d") for d in dates]

    # --- Panel 1: Weight ---
    ax = axes[0]
    ax.set_facecolor("#0d1117")
    weights = [d["weight"] for d in data_list]
    valid_w = [(dt, w) for dt, w in zip(dates, weights) if w is not None]
    if valid_w:
        w_dates, w_vals = zip(*valid_w)
        ax.plot(w_dates, w_vals, "o-", color="#00d4ff", linewidth=2, markersize=6)
        ax.fill_between(w_dates, w_vals, alpha=0.15, color="#00d4ff")
        for dt, w, d in zip(w_dates, w_vals, [x for x in data_list if x["weight"] is not None]):
            label = f"{w}"
            offset = 8
            if d.get("weight_official"):
                label += "\n(Sun official)"
                ax.plot(dt, w, "o", color="#ffd700", markersize=8, zorder=5)
            ax.annotate(label, (dt, w), textcoords="offset points",
                        xytext=(0, offset), ha="center", fontsize=8, color="#00d4ff")
        margin = 0.5
        ax.set_ylim(min(w_vals) - margin, max(w_vals) + margin)
    ax.set_title("Weight", fontsize=12, color="white", pad=8)
    ax.set_ylabel("kg", fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.grid(axis="y", alpha=0.2)

    # --- Panel 2: Blood Pressure & Heart Rate ---
    ax = axes[1]
    ax.set_facecolor("#0d1117")

    # Use 2nd reading if available, otherwise 1st
    bp_data = []
    for d in data_list:
        sys_val = d["bp2_sys"] or d["bp1_sys"]
        dia_val = d["bp2_dia"] or d["bp1_dia"]
        hr_val = d["bp2_hr"] or d["bp1_hr"]
        bp_data.append((d["date"], sys_val, dia_val, hr_val))

    valid_bp = [(dt, s, di, h) for dt, s, di, h in bp_data if s is not None]
    if valid_bp:
        bp_dates = [x[0] for x in valid_bp]
        sbp = [x[1] for x in valid_bp]
        dbp = [x[2] for x in valid_bp]
        hr = [x[3] for x in valid_bp]

        ax.plot(bp_dates, sbp, "o-", color="#ff4757", linewidth=2, markersize=5, label="SBP")
        ax.plot(bp_dates, [d for d in dbp if d is not None] if all(d is not None for d in dbp) else dbp,
                "s--", color="#ffa502", linewidth=1.5, markersize=4, label="DBP")
        valid_hr = [(dt, h) for dt, h in zip(bp_dates, hr) if h is not None]
        if valid_hr:
            hr_dates, hr_vals = zip(*valid_hr)
            ax.plot(hr_dates, hr_vals, "^--", color="#2ed573", linewidth=1.5, markersize=4, label="HR")

        for dt, s in zip(bp_dates, sbp):
            ax.annotate(str(s), (dt, s), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=7, color="#ff4757")

        # Reference line at 140
        ax.axhline(y=140, color="#ff4757", linestyle=":", alpha=0.4, linewidth=1)

    ax.set_title("Blood Pressure & Heart Rate", fontsize=12, color="white", pad=8)
    ax.set_ylabel("mmHg / bpm", fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.2)

    # --- Panel 3: Sleep Score ---
    ax = axes[2]
    ax.set_facecolor("#0d1117")

    sleep_dates = []
    sleep_scores = []
    sleep_colors = []
    for d in data_list:
        sleep_dates.append(d["date"])
        score = d["sleep_score"]
        sleep_scores.append(score)
        if score is None:
            sleep_colors.append("#555555")
        elif score >= 70:
            sleep_colors.append("#9b59b6")
        elif score >= 65:
            sleep_colors.append("#e74c3c")
        else:
            sleep_colors.append("#e74c3c")

    bar_scores = [s if s is not None else 0 for s in sleep_scores]
    bars = ax.bar(sleep_dates, bar_scores, width=0.6, color=sleep_colors, alpha=0.85)

    for dt, score, bar in zip(sleep_dates, sleep_scores, bars):
        if score is not None:
            ax.annotate(str(score), (dt, score), textcoords="offset points",
                        xytext=(0, 5), ha="center", fontsize=8, color="white")
        else:
            ax.annotate("N/A", (dt, 0), textcoords="offset points",
                        xytext=(0, 5), ha="center", fontsize=7, color="#888888")

    # Reference line at 65
    ax.axhline(y=65, color="#e74c3c", linestyle=":", alpha=0.5, linewidth=1)
    ax.set_title("Sleep Score (Garmin)", fontsize=12, color="white", pad=8)
    ax.set_ylabel("Score", fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.set_ylim(0, 100)

    for a in axes:
        a.tick_params(colors="white", labelsize=8)
        for spine in a.spines.values():
            spine.set_color("#333333")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_path, facecolor="#0d1117", edgecolor="none", bbox_inches="tight")
    plt.close()
    print(f"Dashboard saved to {output_path}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    daily_dir = os.path.join(base_dir, "reviews", "daily")
    output_path = os.path.join(base_dir, "reviews", "health_dashboard.png")

    files = sorted(glob.glob(os.path.join(daily_dir, "*.md")))
    if not files:
        print("No daily records found.")
        return

    data_list = []
    for f in files:
        try:
            data_list.append(parse_daily_file(f))
        except Exception as e:
            print(f"Warning: failed to parse {f}: {e}")

    if data_list:
        generate_dashboard(data_list, output_path)


if __name__ == "__main__":
    main()
