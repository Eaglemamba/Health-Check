#!/usr/bin/env python3
"""Aggregate daily health records into ISO-week means and render a weekly-level dashboard.

日線級 dashboard（generate_dashboard.py）每天一個點，受水分 / 單晚睡眠雜訊影響大。
本腳本把同一份 daily 資料按 ISO 週聚合成週均，平滑短期波動，凸顯半年逆轉趨勢。
解析邏輯直接重用 generate_dashboard.parse_daily_file，確保兩張圖資料來源 1:1 一致。
"""

import os
import glob
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC",
    "Microsoft JhengHei", "Microsoft YaHei", "SimHei", "PingFang TC",
    "Arial Unicode MS", "sans-serif",
]
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt

from generate_dashboard import parse_daily_file, CHECKUP_BASELINE


# 半年計畫體重里程碑（CLAUDE.md baseline）：第 0 月 = 健檢 2026-03-25。
# 月節點日期採健檢路徑錨點（Month 3 = 06-17、Month 6 = 09-17）線性內插。
PLAN_ANCHORS = {0: datetime(2026, 3, 25), 3: datetime(2026, 6, 17), 6: datetime(2026, 9, 17)}
PLAN_WEIGHTS = {0: 70.0, 1: 69.2, 2: 68.3, 3: 67.5, 4: 66.7, 5: 65.8, 6: 65.0}


def _plan_month_date(month):
    """月節點日期：用 0/3/6 三個錨點線性內插出中間月份。"""
    if month <= 3:
        lo, hi = 0, 3
    else:
        lo, hi = 3, 6
    span_days = (PLAN_ANCHORS[hi] - PLAN_ANCHORS[lo]).days
    frac = (month - lo) / (hi - lo)
    return PLAN_ANCHORS[lo] + timedelta(days=span_days * frac)


def _mean(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def aggregate_weekly(data_list):
    """把 daily dict list 聚合成 per-ISO-week 統計，按週起始日（週一）排序。"""
    weeks = {}
    for d in data_list:
        key = d["date"].isocalendar()[:2]  # (iso_year, iso_week)
        weeks.setdefault(key, []).append(d)

    rows = []
    for (iso_year, iso_week), days in sorted(weeks.items()):
        monday = datetime.fromisocalendar(iso_year, iso_week, 1)

        # 體重：週均（平滑）＋ 週六正式讀數（連 5 工作日後的真實低點）
        weights = [x["weight"] for x in days if x["weight"] is not None]
        saturday = next((x["weight"] for x in days
                         if x["weight"] is not None and x["date"].weekday() == 5), None)

        # 淨脂肪質量 = 體重 × 體脂% / 100，先逐日算再取週均（避免用週均相乘失真）
        net_fat = [x["weight"] * x["body_fat"] / 100.0 for x in days
                   if x["weight"] is not None and x["body_fat"] is not None]

        # 血壓：每日取第二次（缺則第一次），再求週均
        sbp = [x["bp2_sys"] or x["bp1_sys"] for x in days]
        dbp = [x["bp2_dia"] or x["bp1_dia"] for x in days]
        hr = [x["bp2_hr"] or x["bp1_hr"] for x in days]

        rows.append({
            "iso_year": iso_year, "iso_week": iso_week, "x": monday,
            "label": f"W{iso_week}\n{monday.strftime('%m/%d')}",
            "n_days": len(days),
            "weight_mean": _mean(weights),
            "weight_sat": saturday,
            "body_fat": _mean([x["body_fat"] for x in days]),
            "visceral": _mean([x["visceral_fat"] for x in days]),
            "net_fat": _mean(net_fat),
            "sbp": _mean(sbp), "dbp": _mean(dbp), "hr": _mean(hr),
            "sleep": _mean([x["sleep_score"] for x in days]),
            "bb": _mean([x["body_battery"] for x in days]),
        })
    return rows


def _annotate(ax, x, y, text, color, dy=8, ha="center", va="bottom"):
    if y is None:
        return
    ax.annotate(text, (x, y), textcoords="offset points",
                xytext=(0, dy), ha=ha, va=va, fontsize=8, color=color)


def generate_weekly_dashboard(rows, output_path):
    xs = [r["x"] for r in rows]
    first, last = rows[0]["x"].strftime("%Y-%m-%d"), rows[-1]["x"].strftime("%Y-%m-%d")

    plt.style.use("dark_background")
    fig, axes = plt.subplots(4, 1, figsize=(max(12, len(rows) * 1.1), 16), dpi=160, sharex=True)
    fig.patch.set_facecolor("#0d1117")
    fig.suptitle(f"Weekly Health Dashboard  (ISO-week means)\n{first} ~ {last}  ·  {len(rows)} weeks",
                 fontsize=14, fontweight="bold", color="white", y=0.995)

    cb = CHECKUP_BASELINE

    # --- Panel 1: Weight (weekly mean + Saturday official + plan reference) ---
    ax = axes[0]; ax.set_facecolor("#0d1117")
    wm = [(r["x"], r["weight_mean"]) for r in rows if r["weight_mean"] is not None]
    if wm:
        wx, wv = zip(*wm)
        ax.plot(wx, wv, "o-", color="#00d4ff", linewidth=2.2, markersize=7, label="Weekly Mean", zorder=4)
        ax.fill_between(wx, wv, alpha=0.12, color="#00d4ff")
        for x, v in zip(wx, wv):
            _annotate(ax, x, v, f"{v:.1f}", "#00d4ff", dy=9)
    # 週六正式讀數（真實低點）
    sat = [(r["x"], r["weight_sat"]) for r in rows if r["weight_sat"] is not None]
    if sat:
        sx, sv = zip(*sat)
        ax.plot(sx, sv, "o", color="#ffd700", markersize=7, zorder=5, label="Sat official")
    # 半年計畫里程碑參考線
    plan_x = [_plan_month_date(m) for m in sorted(PLAN_WEIGHTS)]
    plan_y = [PLAN_WEIGHTS[m] for m in sorted(PLAN_WEIGHTS)]
    ax.plot(plan_x, plan_y, ":", color="#2ed573", linewidth=1.8, alpha=0.7, label="Plan (M0->M6)", zorder=2)
    for m in sorted(PLAN_WEIGHTS):
        ax.plot(_plan_month_date(m), PLAN_WEIGHTS[m], "_", color="#2ed573", markersize=10, alpha=0.7)
    # 健檢 baseline 錨點
    ax.plot(cb["date"], cb["weight"], "*", color="#ffffff", markersize=16,
            markeredgecolor="#ff4757", markeredgewidth=1.2, zorder=6, label="Checkup (3/25)")
    # 緊湊 ylim：把 0 軸壓出畫面，避免 fill_between 形成大色塊
    _wy = [v for _, v in wm] + [v for _, v in sat] + list(PLAN_WEIGHTS.values()) + [cb["weight"]]
    if _wy:
        ax.set_ylim(min(_wy) - 0.6, max(_wy) + 0.8)
    ax.set_title("Weight — weekly mean vs plan", fontsize=12, color="white", pad=8)
    ax.set_ylabel("kg", fontsize=10)
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    ax.grid(axis="y", alpha=0.2)

    # --- Panel 2: Body Composition (weekly mean) ---
    ax2 = axes[1]; ax2.set_facecolor("#0d1117")
    ax2r = ax2.twinx(); ax2r.set_facecolor("#0d1117")
    left_vals = []
    bf = [(r["x"], r["body_fat"]) for r in rows if r["body_fat"] is not None]
    if bf:
        bx, bv = zip(*bf)
        ax2.plot(bx, bv, "o-", color="#ff6b81", linewidth=2, markersize=6, label="Body Fat %")
        ax2.fill_between(bx, bv, alpha=0.10, color="#ff6b81")
        for x, v in zip(bx, bv):
            _annotate(ax2, x, v, f"{v:.1f}%", "#ff6b81", dy=8)
        left_vals += list(bv)
    vf = [(r["x"], r["visceral"]) for r in rows if r["visceral"] is not None]
    if vf:
        vx, vv = zip(*vf)
        ax2.plot(vx, vv, "s--", color="#ffa502", linewidth=2, markersize=5, label="Visceral Fat")
        for x, v in zip(vx, vv):
            _annotate(ax2, x, v, f"{v:.1f}", "#ffa502", dy=-14, va="top")
        left_vals += list(vv)
    ax2.plot(cb["date"], cb["body_fat"], "*", color="#ffffff", markersize=16,
             markeredgecolor="#ff6b81", markeredgewidth=1.2, zorder=6, label="Checkup (3/25)")
    left_vals.append(cb["body_fat"])
    nf = [(r["x"], r["net_fat"]) for r in rows if r["net_fat"] is not None]
    if nf:
        nx, nv = zip(*nf)
        ax2r.plot(nx, nv, "D-.", color="#00d4ff", linewidth=1.8, markersize=5, label="Net Fat Mass")
        for x, v in zip(nx, nv):
            ax2r.annotate(f"{v:.2f}", (x, v), textcoords="offset points",
                          xytext=(8, 0), ha="left", va="center", fontsize=8, color="#00d4ff")
    if left_vals:
        ax2.set_ylim(min(left_vals) - 1.0, max(left_vals) + 2.0)
    ax2.set_title("Body Composition — weekly mean", fontsize=12, color="white", pad=8)
    ax2.set_ylabel("Body Fat % / Visceral", fontsize=10, color="white")
    ax2r.set_ylabel("Net Fat Mass (kg)", fontsize=10, color="#00d4ff")
    ax2.tick_params(axis="y", colors="white"); ax2r.tick_params(axis="y", colors="#00d4ff")
    ax2r.xaxis.set_visible(False)
    ax2.grid(axis="y", alpha=0.2)
    l1, lab1 = ax2.get_legend_handles_labels()
    l2, lab2 = ax2r.get_legend_handles_labels()
    ax2.legend(l1 + l2, lab1 + lab2, loc="upper right", fontsize=8)

    # --- Panel 3: Blood Pressure & Heart Rate (weekly mean) ---
    ax = axes[2]; ax.set_facecolor("#0d1117")
    bp = [(r["x"], r["sbp"], r["dbp"], r["hr"]) for r in rows if r["sbp"] is not None]
    if bp:
        px = [b[0] for b in bp]
        ax.plot(px, [b[1] for b in bp], "o-", color="#ff4757", linewidth=2, markersize=5, label="SBP")
        ax.plot(px, [b[2] for b in bp], "s--", color="#ffa502", linewidth=1.5, markersize=4, label="DBP")
        hrp = [(b[0], b[3]) for b in bp if b[3] is not None]
        if hrp:
            hx, hv = zip(*hrp)
            ax.plot(hx, hv, "^--", color="#2ed573", linewidth=1.5, markersize=4, label="HR")
        for b in bp:
            _annotate(ax, b[0], b[1], f"{b[1]:.0f}", "#ff4757", dy=8)
        ax.axhline(y=130, color="#ff4757", linestyle=":", alpha=0.4, linewidth=1)
    ax.plot(cb["date"], cb["sbp"], "*", color="#ffffff", markersize=16,
            markeredgecolor="#ff4757", markeredgewidth=1.2, zorder=6, label="Checkup (3/25)")
    ax.plot(cb["date"], cb["dbp"], "*", color="#ffffff", markersize=12,
            markeredgecolor="#ffa502", markeredgewidth=1.0, zorder=6)
    ax.set_title("Blood Pressure & Heart Rate — weekly mean", fontsize=12, color="white", pad=8)
    ax.set_ylabel("mmHg / bpm", fontsize=10)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.2)

    # --- Panel 4: Sleep Score (weekly mean bars) + Body Battery (weekly mean line) ---
    ax = axes[3]; ax.set_facecolor("#0d1117")
    axr = ax.twinx(); axr.set_facecolor("#0d1117")
    sl = [(r["x"], r["sleep"]) for r in rows if r["sleep"] is not None]
    if sl:
        slx, slv = zip(*sl)
        colors = ["#9b59b6" if v >= 70 else "#e74c3c" for v in slv]
        ax.bar(slx, slv, width=4.5, color=colors, alpha=0.85, label="Sleep Score")
        for x, v in zip(slx, slv):
            ax.annotate(f"{v:.0f}", (x, v), textcoords="offset points",
                        xytext=(0, 5), ha="center", fontsize=8, color="white")
        ax.axhline(y=70, color="#9b59b6", linestyle=":", alpha=0.4, linewidth=1)
    bb = [(r["x"], r["bb"]) for r in rows if r["bb"] is not None]
    if bb:
        bx, bv = zip(*bb)
        axr.plot(bx, bv, "o-", color="#00d4ff", linewidth=2, markersize=6, label="Body Battery")
        for x, v in zip(bx, bv):
            axr.annotate(f"{v:.0f}", (x, v), textcoords="offset points",
                         xytext=(0, -14), ha="center", va="top", fontsize=8, color="#00d4ff")
        axr.axhline(y=50, color="#00d4ff", linestyle=":", alpha=0.35, linewidth=1)
    ax.set_title("Sleep Score & Body Battery — weekly mean", fontsize=12, color="white", pad=8)
    ax.set_ylabel("Sleep Score", fontsize=10, color="white")
    axr.set_ylabel("Body Battery (wake)", fontsize=10, color="#00d4ff")
    ax.set_ylim(30, 90); axr.set_ylim(20, 90)
    ax.tick_params(axis="y", colors="white"); axr.tick_params(axis="y", colors="#00d4ff")
    l1, lab1 = ax.get_legend_handles_labels()
    l2, lab2 = axr.get_legend_handles_labels()
    ax.legend(l1 + l2, lab1 + lab2, loc="upper left", fontsize=8)

    # X 軸鎖在資料範圍（含健檢錨點），避免計畫線把全圖撐到 9 月
    x_lo = min(xs[0], cb["date"]) - timedelta(days=4)
    x_hi = xs[-1] + timedelta(days=4)
    axes[-1].set_xlim(x_lo, x_hi)
    # X 軸用週標籤（W## + 週一日期）
    axes[-1].set_xticks(xs)
    axes[-1].set_xticklabels([r["label"] for r in rows], fontsize=8)

    for a in axes:
        a.tick_params(colors="white", labelsize=8)
        for spine in a.spines.values():
            spine.set_color("#333333")
    for spine in ax2r.spines.values():
        spine.set_color("#333333")
    for spine in axr.spines.values():
        spine.set_color("#333333")
    ax2r.tick_params(colors="#00d4ff", labelsize=8)
    axr.tick_params(colors="#00d4ff", labelsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(output_path, facecolor="#0d1117", edgecolor="none", bbox_inches="tight")
    plt.close()
    print(f"Weekly dashboard saved to {output_path}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    daily_dir = os.path.join(base_dir, "reviews", "daily")
    output_path = os.path.join(base_dir, "reviews", "health_dashboard_weekly.png")

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

    rows = aggregate_weekly(data_list)
    if rows:
        generate_weekly_dashboard(rows, output_path)


if __name__ == "__main__":
    main()
