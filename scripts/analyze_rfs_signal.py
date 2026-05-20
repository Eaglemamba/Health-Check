#!/usr/bin/env python3
"""
RFS (Rostral Fluid Shift) signal analysis from Garmin daily data.

Tests whether days with more sitting (sedentary minutes / fewer steps) are
followed by worse sleep / OSA markers — a within-subject empirical test of
the RFS hypothesis (Redolfi 2009 AJRCCM, Yumino 2010 Circulation,
Redolfi 2011 RCT AJRCCM).

Pairing logic:
    exposure  = daytime sedentary minutes / steps during day D (Taipei)
    outcome   = sleep score / SpO2 nadir / T90 / TST of night D->D+1
                (extracted from JSON file of date D+1, sleep section)

Inputs:
    data/garmin/YYYY-MM-DD.json  (one per day, gitignored)

Outputs:
    reviews/rfs_signal_analysis.md   (numeric report + interpretation)
    reviews/rfs_signal_analysis.png  (4-panel visualization)

Usage:
    python scripts/analyze_rfs_signal.py
    python scripts/analyze_rfs_signal.py --window 30      # last N days only
    python scripts/analyze_rfs_signal.py --threshold 480  # custom sedentary cutoff
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, median, pstdev

# Windows cp950 -> UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
OUT_MD = ROOT / "reviews" / "rfs_signal_analysis.md"
OUT_PNG = ROOT / "reviews" / "rfs_signal_analysis.png"

TPE_OFFSET = timedelta(hours=8)
DAY_START_H = 6     # 06:00 Taipei — start of "daytime sitting" window
DAY_END_H = 22      # 22:00 Taipei — end of daytime
AFT_START_H = 13    # 13:00 — afternoon sub-window (most relevant for evening RFS)
AFT_END_H = 19      # 19:00


def parse_gmt(ts: str) -> datetime:
    """Parse Garmin GMT timestamp like '2026-05-18T16:00:00.0' (assumed UTC)."""
    s = ts[:-1] if ts.endswith("Z") else ts
    if "." in s:
        s = s.split(".", 1)[0]
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def local_hour(ts_str: str) -> int:
    """Return Taipei local hour for a Garmin UTC timestamp string."""
    return (parse_gmt(ts_str) + TPE_OFFSET).hour


def local_date(ts_str: str) -> str:
    return (parse_gmt(ts_str) + TPE_OFFSET).strftime("%Y-%m-%d")


def load_day(date: str) -> dict | None:
    p = DATA_DIR / f"{date}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def extract_exposure(day_json: dict, date: str) -> dict:
    """Compute exposure metrics for one Taipei day."""
    out = {
        "total_steps": 0,
        "daytime_sedentary_min": 0,
        "daytime_active_min": 0,
        "afternoon_sedentary_min": 0,
        "n_blocks": 0,
    }
    steps = day_json.get("steps") or []
    if not isinstance(steps, list):
        return out
    for blk in steps:
        ts = blk.get("startGMT")
        if not ts:
            continue
        # Filter to this Taipei date only
        if local_date(ts) != date:
            continue
        hour = local_hour(ts)
        level = blk.get("primaryActivityLevel", "")
        step_count = blk.get("steps", 0) or 0
        out["total_steps"] += step_count
        out["n_blocks"] += 1
        is_daytime = DAY_START_H <= hour < DAY_END_H
        is_afternoon = AFT_START_H <= hour < AFT_END_H
        if not is_daytime:
            continue
        if level == "sedentary":
            out["daytime_sedentary_min"] += 15
            if is_afternoon:
                out["afternoon_sedentary_min"] += 15
        elif level in ("active", "highlyActive"):
            out["daytime_active_min"] += 15
    return out


def extract_outcome(day_json: dict) -> dict:
    """Sleep/SpO2 outcome metrics from one JSON file (= sleep ending that morning)."""
    out = {
        "sleep_score": None,
        "deep_min": None,
        "rem_min": None,
        "tst_min": None,
        "spo2_avg": None,
        "spo2_low": None,
        "t90_pct": None,
        "rhr": None,
        "stress_avg": None,
    }
    sleep = day_json.get("sleep") or {}
    ds = sleep.get("dailySleepDTO") or {}
    scores = ds.get("sleepScores") or {}
    if isinstance(scores, dict):
        overall = scores.get("overall") or {}
        if isinstance(overall, dict):
            out["sleep_score"] = overall.get("value")
    out["deep_min"] = (ds.get("deepSleepSeconds") or 0) // 60 or None
    out["rem_min"] = (ds.get("remSleepSeconds") or 0) // 60 or None
    tst_sec = (ds.get("sleepTimeSeconds") or 0)
    out["tst_min"] = (tst_sec // 60) if tst_sec else None

    spo2_sum = sleep.get("wellnessSpO2SleepSummaryDTO") or {}
    out["spo2_avg"] = spo2_sum.get("averageSPO2")
    out["spo2_low"] = spo2_sum.get("lowestSPO2")

    epochs = sleep.get("wellnessEpochSPO2DataDTOList") or []
    if epochs and tst_sec:
        below = sum((e.get("epochDuration") or 60) for e in epochs
                    if (e.get("spo2Reading") or 100) < 90)
        out["t90_pct"] = round(100.0 * below / tst_sec, 2)

    rhr = day_json.get("rhr") or {}
    if isinstance(rhr, dict):
        out["rhr"] = rhr.get("restingHeartRate")
    stress = day_json.get("stress") or {}
    if isinstance(stress, dict):
        out["stress_avg"] = stress.get("avgStressLevel") or stress.get("overallStressLevel")
    return out


def build_dataset(window: int | None = None) -> list[dict]:
    """Pair exposure(day D) with outcome(sleep night D->D+1, stored in JSON D+1)."""
    files = sorted(DATA_DIR.glob("*.json"))
    if not files:
        return []

    # Filter window
    if window:
        files = files[-(window + 1):]   # +1 because we need pair shift

    # Build per-date dicts
    expo_by_date: dict[str, dict] = {}
    outc_by_date: dict[str, dict] = {}
    for f in files:
        date = f.stem
        if len(date) != 10 or date[4] != "-":
            continue
        d = load_day(date)
        if not d:
            continue
        expo_by_date[date] = extract_exposure(d, date)
        outc_by_date[date] = extract_outcome(d)

    # Pair: exposure(D) + outcome from JSON(D+1)
    rows = []
    excluded = []
    for date_str in sorted(expo_by_date.keys()):
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        next_date = (dt + timedelta(days=1)).strftime("%Y-%m-%d")
        if next_date not in outc_by_date:
            continue
        expo = expo_by_date[date_str]
        # Exclude device-off days (no steps + no activity blocks classified)
        if (expo.get("total_steps", 0) or 0) < 1000:
            excluded.append((date_str, expo.get("total_steps", 0)))
            continue
        row = {"exposure_date": date_str, "sleep_date": next_date}
        row.update(expo)
        row.update(outc_by_date[next_date])
        rows.append(row)
    if excluded:
        print(f"Excluded {len(excluded)} device-off days: " + ", ".join(f"{d}(steps={s})" for d, s in excluded), file=sys.stderr)
    return rows


# ---------- Statistics ----------

def spearman_rho(xs: list[float], ys: list[float]) -> tuple[float, int]:
    """Spearman rank correlation. Returns (rho, n)."""
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pairs)
    if n < 4:
        return float("nan"), n
    xs_, ys_ = zip(*pairs)
    rx = rank(xs_); ry = rank(ys_)
    mx = sum(rx) / n; my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den_x = sum((a - mx) ** 2 for a in rx) ** 0.5
    den_y = sum((b - my) ** 2 for b in ry) ** 0.5
    if den_x == 0 or den_y == 0:
        return float("nan"), n
    return num / (den_x * den_y), n


def rank(xs):
    indexed = sorted((v, i) for i, v in enumerate(xs))
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][0] == indexed[i][0]:
            j += 1
        avg_rank = (i + j + 2) / 2.0   # 1-based avg rank for ties
        for k in range(i, j + 1):
            ranks[indexed[k][1]] = avg_rank
        i = j + 1
    return ranks


def group_split(rows: list[dict], expo_key: str, threshold: float | None = None):
    """Split rows by exposure median (or given threshold). Returns (high_group, low_group)."""
    vals = [r[expo_key] for r in rows if r.get(expo_key) is not None]
    if not vals:
        return [], []
    cut = threshold if threshold is not None else median(vals)
    high = [r for r in rows if (r.get(expo_key) or 0) >= cut]
    low = [r for r in rows if (r.get(expo_key) or 0) < cut]
    return high, low, cut


def group_means(rows: list[dict], keys: list[str]) -> dict:
    out = {}
    for k in keys:
        vals = [r[k] for r in rows if r.get(k) is not None]
        out[k] = round(mean(vals), 2) if vals else None
        out[f"{k}_n"] = len(vals)
    return out


# ---------- Output ----------

def write_markdown(rows: list[dict], high, low, cut, rho_table: list[tuple]) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    n_rows = len(rows)
    outcomes = ["sleep_score", "deep_min", "rem_min", "tst_min",
                "spo2_avg", "spo2_low", "t90_pct", "rhr", "stress_avg"]

    hm = group_means(high, outcomes)
    lm = group_means(low, outcomes)

    # Verdict
    sc_high = hm.get("sleep_score"); sc_low = lm.get("sleep_score")
    spo2_high = hm.get("spo2_low"); spo2_low = lm.get("spo2_low")
    t90_high = hm.get("t90_pct"); t90_low = lm.get("t90_pct")

    score_delta = (sc_low - sc_high) if (sc_high is not None and sc_low is not None) else None
    spo2_delta = (spo2_low - spo2_high) if (spo2_high is not None and spo2_low is not None) else None
    t90_delta = (t90_high - t90_low) if (t90_high is not None and t90_low is not None) else None

    verdict = "⭐ 訊號弱（RFS 非主要 OSA 機制）"
    if score_delta and score_delta >= 5 and (t90_delta and t90_delta >= 1):
        verdict = "⭐⭐⭐ RFS 主導訊號明確（建議壓力襪 trial）"
    elif (score_delta and score_delta >= 2) or (t90_delta and t90_delta >= 0.5):
        verdict = "⭐⭐ RFS 中度貢獻（值得進一步驗證）"

    lines = []
    lines.append(f"# RFS (Rostral Fluid Shift) 訊號分析\n")
    lines.append(f"**生成時間：** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**配對天數：** {n_rows} 對（exposure: day D → outcome: sleep D→D+1）")
    lines.append(f"**Sedentary 閾值（中位數分組）：** {cut:.0f} 分鐘/日\n")

    lines.append(f"## 判讀：{verdict}\n")
    if score_delta is not None:
        lines.append(f"- Low-sit 夜 Sleep Score 比 High-sit 夜高 **{score_delta:+.1f}** 分")
    if t90_delta is not None:
        lines.append(f"- High-sit 夜 T90 比 Low-sit 夜高 **{t90_delta:+.2f}** %")
    if spo2_delta is not None:
        lines.append(f"- Low-sit 夜 SpO2 nadir 比 High-sit 夜高 **{spo2_delta:+.1f}** %")
    lines.append("")

    lines.append("## 分組均值對比\n")
    lines.append("| 指標 | High-sit (≥ 閾值) n=" + str(len(high)) + " | Low-sit (< 閾值) n=" + str(len(low)) + " | Δ |")
    lines.append("|---|---|---|---|")
    for k in outcomes:
        hv = hm.get(k); lv = lm.get(k)
        d = (lv - hv) if (hv is not None and lv is not None) else None
        d_str = f"{d:+.2f}" if d is not None else "—"
        lines.append(f"| {k} | {hv if hv is not None else '—'} | {lv if lv is not None else '—'} | {d_str} |")
    lines.append("")

    lines.append("## Spearman 相關（連續變數，無分組）\n")
    lines.append("| 暴露 → 結果 | rho | n | 解讀 |")
    lines.append("|---|---|---|---|")
    for label, rho, n in rho_table:
        strength = "中-強" if abs(rho) >= 0.4 else "弱-中" if abs(rho) >= 0.2 else "無"
        direction = "正" if rho > 0 else "負"
        lines.append(f"| {label} | {rho:+.3f} | {n} | {direction}向 {strength} |")
    lines.append("")

    lines.append("## 配對原始資料\n")
    lines.append("| exposure_date | sed_min | aft_sed_min | steps | sleep_date | score | t90% | SpO2_low | TST_min |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append(
            f"| {r['exposure_date']} | {r.get('daytime_sedentary_min','—')} | "
            f"{r.get('afternoon_sedentary_min','—')} | {r.get('total_steps','—')} | "
            f"{r['sleep_date']} | {r.get('sleep_score','—')} | "
            f"{r.get('t90_pct','—')} | {r.get('spo2_low','—')} | {r.get('tst_min','—')} |"
        )
    lines.append("")

    lines.append("## 機制與下一步\n")
    lines.append("- 機制：日間久坐 → 下肢間質液堆積 → 平躺後 redistribute 至頸/胸 → 咽周組織壓 ↑ → Pcrit ↑ → AHI ↑（Redolfi 2009 AJRCCM, Yumino 2010 Circulation）")
    lines.append("- 若判讀為 ⭐⭐⭐：建議下一步 **日間壓力襪 20-30 mmHg × 7 天 trial**（Redolfi 2011 RCT AHI −36%）")
    lines.append("- 若判讀為 ⭐⭐：增加每小時起身 2 分 + 17:00 抬腿 15 分（零成本介入）")
    lines.append("- 若判讀為 ⭐：你的 OSA 主因不在 RFS，續做 POSA + PSG 為主軸\n")

    lines.append("## 統計限制\n")
    lines.append(f"- 樣本 n={n_rows} 對，statistical power 有限（多數效應需 n ≥ 30 才穩定）")
    lines.append("- 觀察性、無 randomization；可能存在 confounder（如：高鈉日 + 久坐日同時發生）")
    lines.append("- 中位數分組可能不對等；可改試 quartile 或 fixed threshold（--threshold 參數）")
    lines.append("- Garmin sedentary 判定為 15-min block，邊界粒度可能偏差 ±15 分\n")

    lines.append(f"*Source: scripts/analyze_rfs_signal.py · Data: data/garmin/*.json (gitignored)*")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def plot_results(rows: list[dict], cut: float) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping PNG output", file=sys.stderr)
        return

    sed = [r["daytime_sedentary_min"] for r in rows]
    score = [r["sleep_score"] for r in rows]
    t90 = [r["t90_pct"] for r in rows]
    spo2_low = [r["spo2_low"] for r in rows]
    steps = [r["total_steps"] for r in rows]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("RFS Signal Analysis — daytime sedentary vs next-night sleep/OSA markers",
                 fontsize=14, fontweight="bold")

    # 1. Sedentary vs Sleep Score
    ax = axes[0, 0]
    pairs = [(s, sc) for s, sc in zip(sed, score) if s is not None and sc is not None]
    if pairs:
        x, y = zip(*pairs)
        ax.scatter(x, y, alpha=0.7)
        ax.axvline(cut, color="red", linestyle="--", alpha=0.5, label=f"median cut {cut:.0f}")
        ax.set_xlabel("Daytime sedentary minutes (06:00-22:00)")
        ax.set_ylabel("Next-night Sleep Score")
        ax.set_title("Sedentary vs Sleep Score")
        ax.legend()
        ax.grid(alpha=0.3)

    # 2. Sedentary vs T90
    ax = axes[0, 1]
    pairs = [(s, t) for s, t in zip(sed, t90) if s is not None and t is not None]
    if pairs:
        x, y = zip(*pairs)
        ax.scatter(x, y, alpha=0.7, color="orange")
        ax.axvline(cut, color="red", linestyle="--", alpha=0.5)
        ax.set_xlabel("Daytime sedentary minutes")
        ax.set_ylabel("Next-night T90 (%)")
        ax.set_title("Sedentary vs T90 (SpO2 < 90% time)")
        ax.grid(alpha=0.3)

    # 3. Boxplot Sleep Score by group
    ax = axes[1, 0]
    high_score = [r["sleep_score"] for r in rows if r["sleep_score"] is not None and (r["daytime_sedentary_min"] or 0) >= cut]
    low_score = [r["sleep_score"] for r in rows if r["sleep_score"] is not None and (r["daytime_sedentary_min"] or 0) < cut]
    if high_score or low_score:
        ax.boxplot([low_score, high_score], tick_labels=[f"Low-sit\nn={len(low_score)}", f"High-sit\nn={len(high_score)}"])
        ax.set_ylabel("Sleep Score")
        ax.set_title("Sleep Score by sitting group")
        ax.grid(alpha=0.3, axis="y")

    # 4. Boxplot T90 by group
    ax = axes[1, 1]
    high_t = [r["t90_pct"] for r in rows if r["t90_pct"] is not None and (r["daytime_sedentary_min"] or 0) >= cut]
    low_t = [r["t90_pct"] for r in rows if r["t90_pct"] is not None and (r["daytime_sedentary_min"] or 0) < cut]
    if high_t or low_t:
        ax.boxplot([low_t, high_t], tick_labels=[f"Low-sit\nn={len(low_t)}", f"High-sit\nn={len(high_t)}"])
        ax.set_ylabel("T90 (%)")
        ax.set_title("T90 by sitting group")
        ax.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(description="RFS signal analysis")
    ap.add_argument("--window", type=int, default=None, help="Limit to last N days")
    ap.add_argument("--threshold", type=float, default=None, help="Fixed sedentary cutoff (minutes); default = median")
    args = ap.parse_args()

    rows = build_dataset(window=args.window)
    if not rows:
        print("No paired data found. Check data/garmin/*.json exists.", file=sys.stderr)
        sys.exit(1)

    # Group split
    high, low, cut = group_split(rows, "daytime_sedentary_min", threshold=args.threshold)

    # Spearman correlations
    sed = [r["daytime_sedentary_min"] for r in rows]
    aft = [r["afternoon_sedentary_min"] for r in rows]
    steps = [r["total_steps"] for r in rows]
    score = [r["sleep_score"] for r in rows]
    t90 = [r["t90_pct"] for r in rows]
    spo2_low = [r["spo2_low"] for r in rows]

    rho_table = []
    for label, x, y in [
        ("Daytime sedentary → Sleep Score", sed, score),
        ("Daytime sedentary → T90",         sed, t90),
        ("Daytime sedentary → SpO2 nadir",  sed, spo2_low),
        ("Afternoon sedentary → Sleep Score", aft, score),
        ("Afternoon sedentary → T90",        aft, t90),
        ("Total steps → Sleep Score",        steps, score),
        ("Total steps → T90 (expect negative)", steps, t90),
    ]:
        rho, n = spearman_rho(x, y)
        rho_table.append((label, rho if rho == rho else 0.0, n))

    write_markdown(rows, high, low, cut, rho_table)
    plot_results(rows, cut)

    print(f"Wrote: {OUT_MD}")
    print(f"Wrote: {OUT_PNG}")
    print(f"\nPaired days: {len(rows)} | High-sit: {len(high)} | Low-sit: {len(low)} | cut: {cut:.0f} min")


if __name__ == "__main__":
    main()
