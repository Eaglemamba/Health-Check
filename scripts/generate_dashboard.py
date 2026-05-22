#!/usr/bin/env python3
"""Parse daily health records and generate health_dashboard.png."""

import re
import os
import glob
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.family'] = [
    'Noto Sans CJK TC', 'Noto Sans CJK SC',
    'Microsoft YaHei', 'SimHei', 'PingFang TC', 'Arial Unicode MS', 'sans-serif'
]
matplotlib.rcParams['axes.unicode_minus'] = False
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

    # Weight — supports both inline (｜) and separate-line formats
    m = re.search(r"\*\*今日：([\d.]+)\s*kg", content)
    data["weight"] = float(m.group(1)) if m else None

    # Body fat % — inline format: 體脂率：XX% or separate line **體脂率：XX %**
    m = re.search(r"體脂率：([\d.]+)\s*%", content)
    data["body_fat"] = float(m.group(1)) if m else None

    # Visceral fat level — inline format: 內臟脂肪：XX or separate **內臟脂肪等級：XX**
    m = re.search(r"內臟脂肪(?:等級)?[：:]\*{0,2}\s*([\d.]+)", content)
    data["visceral_fat"] = float(m.group(1)) if m else None

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

    # Show all data — no day cap
    dates = [d["date"] for d in data_list]
    first_date = dates[0].strftime("%Y-%m-%d")
    last_date = dates[-1].strftime("%Y-%m-%d")
    n_days = (dates[-1] - dates[0]).days + 1

    # Responsive figure width: wider for more data points
    fig_width = max(12, min(len(data_list) * 0.6, 32))

    # Dark theme
    plt.style.use("dark_background")
    fig, axes = plt.subplots(4, 1, figsize=(fig_width, 16), dpi=160, sharex=True)
    fig.patch.set_facecolor("#0d1117")

    title = f"Health Tracking Dashboard\n{first_date} ~ {last_date} ({n_days} days)"
    fig.suptitle(title, fontsize=14, fontweight="bold", color="white", y=0.99)

    # --- Panel 1: Weight ---
    ax = axes[0]
    ax.set_facecolor("#0d1117")
    weights = [d["weight"] for d in data_list]
    valid_w = [(dt, w) for dt, w in zip(dates, weights) if w is not None]
    if valid_w:
        w_dates, w_vals = zip(*valid_w)
        ax.plot(w_dates, w_vals, "o-", color="#00d4ff", linewidth=2, markersize=6,
                label="Daily")
        ax.fill_between(w_dates, w_vals, alpha=0.15, color="#00d4ff")
        for dt, w, d in zip(w_dates, w_vals, [x for x in data_list if x["weight"] is not None]):
            label = f"{w}"
            offset = 8
            if d.get("weight_official"):
                label += "\n(Sun)"
                ax.plot(dt, w, "o", color="#ffd700", markersize=8, zorder=5)
            ax.annotate(label, (dt, w), textcoords="offset points",
                        xytext=(0, offset), ha="center", fontsize=8, color="#00d4ff")

        # 7-day rolling mean (calendar window, not point window — handles gaps)
        rolling_dates = []
        rolling_means = []
        for dt, _ in valid_w:
            window_start = dt - timedelta(days=6)
            window_vals = [ww for dd, ww in valid_w if window_start <= dd <= dt]
            if len(window_vals) >= 2:
                rolling_dates.append(dt)
                rolling_means.append(sum(window_vals) / len(window_vals))
        if rolling_dates:
            ax.plot(rolling_dates, rolling_means, "--", color="#ffd700",
                    linewidth=2, alpha=0.9, label="7-Day Rolling Mean", zorder=4)
            # Label the latest rolling mean value
            ax.annotate(f"{rolling_means[-1]:.1f}", (rolling_dates[-1], rolling_means[-1]),
                        textcoords="offset points", xytext=(6, 0), ha="left", va="center",
                        fontsize=9, color="#ffd700", fontweight="bold")
            ax.legend(loc="upper right", fontsize=8)

        margin = 0.5
        ax.set_ylim(min(w_vals) - margin, max(w_vals) + margin)
    ax.set_title("Weight", fontsize=12, color="white", pad=8)
    ax.set_ylabel("kg", fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.grid(axis="y", alpha=0.2)

    # --- Panel 2: Body Composition ---
    # Left axis : Body Fat % + Visceral Fat Level (both unitless ratio/index)
    # Right axis: Net Fat Mass (kg) — distinct physical-mass unit
    ax2 = axes[1]
    ax2.set_facecolor("#0d1117")
    ax2r = ax2.twinx()
    ax2r.set_facecolor("#0d1117")

    valid_bf = [(d["date"], d["body_fat"]) for d in data_list if d["body_fat"] is not None]
    valid_vf = [(d["date"], d["visceral_fat"]) for d in data_list if d["visceral_fat"] is not None]
    valid_nf = [(d["date"], d["weight"] * d["body_fat"] / 100.0)
                for d in data_list
                if d["weight"] is not None and d["body_fat"] is not None]

    left_vals = []

    if valid_bf:
        bf_dates, bf_vals = zip(*valid_bf)
        ax2.plot(bf_dates, bf_vals, "o-", color="#ff6b81", linewidth=2, markersize=6, label="Body Fat %")
        ax2.fill_between(bf_dates, bf_vals, alpha=0.12, color="#ff6b81")
        for dt, v in zip(bf_dates, bf_vals):
            ax2.annotate(f"{v}%", (dt, v), textcoords="offset points",
                         xytext=(0, 8), ha="center", fontsize=8, color="#ff6b81")
        ax2.axhline(y=20, color="#ff6b81", linestyle=":", alpha=0.4, linewidth=1)
        left_vals.extend(bf_vals)

    if valid_vf:
        vf_dates, vf_vals = zip(*valid_vf)
        ax2.plot(vf_dates, vf_vals, "s--", color="#ffa502", linewidth=2, markersize=5, label="Visceral Fat")
        for dt, v in zip(vf_dates, vf_vals):
            ax2.annotate(f"{v}", (dt, v), textcoords="offset points",
                         xytext=(0, -14), ha="center", fontsize=8, color="#ffa502")
        ax2.axhline(y=10, color="#ffa502", linestyle=":", alpha=0.4, linewidth=1)
        left_vals.extend(vf_vals)

    if left_vals:
        ax2.set_ylim(min(left_vals) - 1.0, max(left_vals) + 2.0)

    if valid_nf:
        nf_dates, nf_vals = zip(*valid_nf)
        ax2r.plot(nf_dates, nf_vals, "D-.", color="#00d4ff", linewidth=1.8, markersize=5, label="Net Fat Mass")
        for dt, v in zip(nf_dates, nf_vals):
            ax2r.annotate(f"{v:.2f}", (dt, v), textcoords="offset points",
                          xytext=(8, 0), ha="left", va="center", fontsize=8, color="#00d4ff")
        nf_margin = 0.3
        ax2r.set_ylim(min(nf_vals) - nf_margin, max(nf_vals) + nf_margin + 0.5)

    ax2.set_title("Body Composition", fontsize=12, color="white", pad=8)
    ax2.set_ylabel("Body Fat % / Visceral Fat Level", fontsize=10, color="white")
    ax2r.set_ylabel("Net Fat Mass (kg)", fontsize=10, color="#00d4ff")
    ax2.tick_params(axis="y", colors="white")
    ax2r.tick_params(axis="y", colors="#00d4ff")
    ax2r.set_xlim(dates[0], dates[-1])
    ax2r.xaxis.set_visible(False)
    ax2.grid(axis="y", alpha=0.2)

    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2r.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)

    # --- Panel 3: Blood Pressure & Heart Rate ---
    ax = axes[2]
    ax.set_facecolor("#0d1117")

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
        ax.plot(bp_dates, dbp, "s--", color="#ffa502", linewidth=1.5, markersize=4, label="DBP")
        valid_hr = [(dt, h) for dt, h in zip(bp_dates, hr) if h is not None]
        if valid_hr:
            hr_dates, hr_vals = zip(*valid_hr)
            ax.plot(hr_dates, hr_vals, "^--", color="#2ed573", linewidth=1.5, markersize=4, label="HR")

        for dt, s in zip(bp_dates, sbp):
            ax.annotate(str(s), (dt, s), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=7, color="#ff4757")

        ax.axhline(y=140, color="#ff4757", linestyle=":", alpha=0.4, linewidth=1)

    ax.set_title("Blood Pressure & Heart Rate", fontsize=12, color="white", pad=8)
    ax.set_ylabel("mmHg / bpm", fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.2)

    # --- Panel 4: Sleep Score ---
    ax = axes[3]
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
        else:
            sleep_colors.append("#e74c3c")

    bar_scores = [s if s is not None else 0 for s in sleep_scores]
    bar_w = max(0.3, min(0.75, 8.0 / max(len(sleep_dates), 1)))
    ax.bar(sleep_dates, bar_scores, width=bar_w, color=sleep_colors, alpha=0.85)

    for dt, score in zip(sleep_dates, sleep_scores):
        if score is not None:
            ax.annotate(str(score), (dt, score), textcoords="offset points",
                        xytext=(0, 5), ha="center", fontsize=8, color="white")
        else:
            ax.annotate("N/A", (dt, 0), textcoords="offset points",
                        xytext=(0, 5), ha="center", fontsize=7, color="#888888")

    # --- Weekly average: one horizontal dashed line per week ---
    week_data = {}
    for dt, score in zip(sleep_dates, sleep_scores):
        if score is not None:
            wk = dt.isocalendar()[:2]  # (year, week_number)
            if wk not in week_data:
                week_data[wk] = {"scores": [], "dates": []}
            week_data[wk]["scores"].append(score)
            week_data[wk]["dates"].append(dt)

    legend_added = False
    for wk in sorted(week_data.keys()):
        scores = week_data[wk]["scores"]
        dates  = week_data[wk]["dates"]
        avg    = sum(scores) / len(scores)
        x_start = min(dates)
        x_end   = max(dates)
        label = "Weekly Avg" if not legend_added else "_nolegend_"
        ax.hlines(avg, x_start, x_end, colors="#00d4ff", linestyles="--",
                  linewidth=2.5, alpha=0.92, label=label, zorder=5)
        # Label at right end of the line
        ax.annotate(f"{avg:.0f}", (x_end, avg), textcoords="offset points",
                    xytext=(6, 0), ha="left", va="center", fontsize=9,
                    color="#00d4ff", fontweight="bold")
        legend_added = True

    if legend_added:
        ax.legend(loc="upper left", fontsize=8)

    ax.set_title("Sleep Score (Garmin)", fontsize=12, color="white", pad=8)
    ax.set_ylabel("Score", fontsize=10)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=20))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.set_ylim(30, 90)

    for a in axes:
        a.tick_params(colors="white", labelsize=8)
        for spine in a.spines.values():
            spine.set_color("#333333")
    for spine in ax2r.spines.values():
        spine.set_color("#333333")
    ax2r.tick_params(colors="white", labelsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(output_path, facecolor="#0d1117", edgecolor="none", bbox_inches="tight")
    plt.close()
    print(f"Dashboard saved to {output_path}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    daily_dir = os.path.join(base_dir, "reviews", "daily")
    output_path = os.path.join(base_dir, "reviews", "health_dashboard.png")

    # Recursive: 涵蓋月份歸檔子資料夾 (reviews/daily/YYYY-MM/*.md)
    files = sorted(glob.glob(os.path.join(daily_dir, "**", "*.md"), recursive=True))
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
