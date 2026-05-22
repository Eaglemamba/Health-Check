"""
SpO2 × Sleep HR overlay — 驗證「desaturated 時心率上升」假說。

對 Venu 4 cohort（4/24 起，deviceId 3622900919）做兩件事：
  1. 並排 heatmap — SpO2（RdYlGn, 紅=低）與 HR（RdYlGn_r, 紅=高）
     y 軸同 rows = nights，x 軸同 minutes-from-sleep-onset。
     肉眼可看「SpO2 紅帶」對應的位置 HR 是否也是紅帶。

  2. Paired statistics — 每晚 ΔHR = mean(HR | SpO2<90) − mean(HR | SpO2≥90)
     若假說成立，ΔHR > 0 應在大多數夜出現；用 Wilcoxon signed-rank 檢定。

Per-minute aggregation:
  - SpO2: minute min（與既有 heatmap 一致 — 突顯 desat）
  - HR:   minute max（突顯 arousal-driven spike）

Output:
  reviews/daily/spo2/spo2_hr_overlay_all_nights.png
"""
import json
from pathlib import Path
from datetime import datetime, timezone
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as st

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "garmin"
OUT_DIR = ROOT / "reviews" / "daily" / "spo2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_MIN = 480
SPO2_MIN_VIS = 80
SPO2_MAX_VIS = 100
HR_MIN_VIS = 45
HR_MAX_VIS = 85
VENU4_DEVICE_ID = 3622900919


def parse_gmt(s: str) -> datetime:
    if s.endswith(".0"):
        s = s[:-2]
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def load_night(p: Path):
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
    if not epochs_raw:
        return None

    first_device = epochs_raw[0].get("deviceId")
    if first_device != VENU4_DEVICE_ID:
        return None

    spo2_min = {}
    for e in epochs_raw:
        ts_raw = e.get("epochTimestamp")
        ts = parse_gmt(ts_raw) if isinstance(ts_raw, str) else datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc)
        if ts < sleep_start or ts > sleep_end:
            continue
        em = int((ts - sleep_start).total_seconds() / 60)
        v = e.get("spo2Reading")
        if v is None or v <= 0 or em < 0 or em >= MAX_MIN:
            continue
        if em not in spo2_min or v < spo2_min[em]:
            spo2_min[em] = v

    if not spo2_min:
        return None

    hr_max = {}
    for item in (data.get("heart_rates") or {}).get("heartRateValues") or []:
        if not (isinstance(item, list) and len(item) >= 2):
            continue
        ts_ms, val = item[0], item[1]
        if ts_ms is None or val is None or val <= 0:
            continue
        ts = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
        if ts < sleep_start or ts > sleep_end:
            continue
        em = int((ts - sleep_start).total_seconds() / 60)
        if em < 0 or em >= MAX_MIN:
            continue
        if em not in hr_max or val > hr_max[em]:
            hr_max[em] = int(val)

    spo2_arr = np.full(MAX_MIN, np.nan)
    for em, v in spo2_min.items():
        spo2_arr[em] = v
    hr_arr = np.full(MAX_MIN, np.nan)
    for em, v in hr_max.items():
        hr_arr[em] = v

    return {
        "date": p.stem,
        "spo2_per_min": spo2_arr,
        "hr_per_min": hr_arr,
    }


def paired_delta_hr(spo2, hr, threshold=90):
    """ΔHR = mean(HR | SpO2<thr) − mean(HR | SpO2≥thr). 兩側都需 ≥3 分鐘樣本。"""
    mask = ~np.isnan(spo2) & ~np.isnan(hr)
    if mask.sum() < 10:
        return None, 0, 0
    s = spo2[mask]
    h = hr[mask]
    desat = h[s < threshold]
    normal = h[s >= threshold]
    if len(desat) < 3 or len(normal) < 3:
        return None, len(desat), len(normal)
    return float(desat.mean() - normal.mean()), len(desat), len(normal)


def main():
    files = sorted(DATA_DIR.rglob("20*.json"))
    nights = []
    for f in files:
        n = load_night(f)
        if n is not None:
            nights.append(n)
    if not nights:
        print("No usable Venu 4 nights.")
        return

    nights.sort(key=lambda n: n["date"])
    spo2_mat = np.array([n["spo2_per_min"] for n in nights])
    hr_mat = np.array([n["hr_per_min"] for n in nights])

    n_nights = spo2_mat.shape[0]
    dates = [n["date"][5:] for n in nights]

    # Per-night ΔHR (desat vs non-desat minutes)
    deltas = []
    n_desats = []
    per_night = []
    for i, n in enumerate(nights):
        d, nd, nn = paired_delta_hr(n["spo2_per_min"], n["hr_per_min"])
        deltas.append(d)
        n_desats.append(nd)
        per_night.append((n["date"], d, nd, nn))

    valid_deltas = np.array([d for d in deltas if d is not None])
    n_positive = int((valid_deltas > 0).sum()) if len(valid_deltas) else 0
    median_delta = float(np.median(valid_deltas)) if len(valid_deltas) else float("nan")
    mean_delta = float(np.mean(valid_deltas)) if len(valid_deltas) else float("nan")
    wilcox_p = float("nan")
    if len(valid_deltas) >= 6:
        try:
            wilcox_p = float(st.wilcoxon(valid_deltas, alternative="greater").pvalue)
        except Exception:
            pass

    # Pooled minute-level correlation (Spearman on all available paired minutes)
    flat_mask = ~np.isnan(spo2_mat) & ~np.isnan(hr_mat)
    flat_spo2 = spo2_mat[flat_mask]
    flat_hr = hr_mat[flat_mask]
    rho_total = rho_p = float("nan")
    if len(flat_spo2) > 100:
        try:
            r = st.spearmanr(flat_spo2, flat_hr)
            rho_total, rho_p = float(r.statistic), float(r.pvalue)
        except Exception:
            pass

    # Median curves
    spo2_med = np.nanmedian(spo2_mat, axis=0)
    hr_med = np.nanmedian(hr_mat, axis=0)

    # Annotate rows: date + ΔHR + n_desat
    row_labels = []
    for d, dlt, nd in zip(dates, deltas, n_desats):
        if dlt is None:
            row_labels.append(f"{d}  (no desat)")
        else:
            sign = "+" if dlt >= 0 else ""
            row_labels.append(f"{d}  ΔHR {sign}{dlt:.1f}  nd{nd}")

    fig = plt.figure(figsize=(17, max(8, 0.22 * n_nights + 4.5)))
    gs = fig.add_gridspec(
        2, 3,
        height_ratios=[max(4, 0.22 * n_nights), 2.8],
        width_ratios=[1, 1, 0.025],
        hspace=0.13, wspace=0.05,
    )
    ax_spo2 = fig.add_subplot(gs[0, 0])
    ax_hr = fig.add_subplot(gs[0, 1], sharey=ax_spo2)
    ax_cb = fig.add_subplot(gs[0, 2])
    ax_med = fig.add_subplot(gs[1, :2])

    # SpO2 heatmap (red = low = bad)
    im_s = ax_spo2.imshow(
        spo2_mat, aspect="auto", origin="upper", cmap="RdYlGn",
        vmin=SPO2_MIN_VIS, vmax=SPO2_MAX_VIS,
        extent=[0, MAX_MIN, n_nights, 0], interpolation="nearest",
    )
    ax_spo2.set_yticks(np.arange(n_nights) + 0.5)
    ax_spo2.set_yticklabels(row_labels, fontsize=7)
    ax_spo2.set_xlim(0, MAX_MIN)
    ax_spo2.set_xlabel("Minutes from sleep onset")
    ax_spo2.set_title(f"SpO2 (minute nadir)  ·  Venu 4 cohort N={n_nights}", fontsize=10)
    for x in [90, 180, 270, 360]:
        ax_spo2.axvline(x, color="black", lw=0.4, alpha=0.4, linestyle=":")
    ax_spo2.axvspan(90, 270, color="black", alpha=0.06, zorder=0)

    # HR heatmap (red = high = arousal). Reverse colormap so red = high HR.
    im_h = ax_hr.imshow(
        hr_mat, aspect="auto", origin="upper", cmap="RdYlGn_r",
        vmin=HR_MIN_VIS, vmax=HR_MAX_VIS,
        extent=[0, MAX_MIN, n_nights, 0], interpolation="nearest",
    )
    ax_hr.set_xlim(0, MAX_MIN)
    ax_hr.set_xlabel("Minutes from sleep onset")
    ax_hr.set_title("Sleep HR (minute max bpm)  ·  red = arousal-driven spike", fontsize=10)
    for x in [90, 180, 270, 360]:
        ax_hr.axvline(x, color="black", lw=0.4, alpha=0.4, linestyle=":")
    ax_hr.axvspan(90, 270, color="black", alpha=0.06, zorder=0)
    plt.setp(ax_hr.get_yticklabels(), visible=False)

    cb = fig.colorbar(im_h, cax=ax_cb)
    cb.set_label("HR (bpm)", fontsize=9)
    # SpO2 colorbar 放在左 heatmap 上方的 inset
    cax_s = ax_spo2.inset_axes([0.0, 1.04, 1.0, 0.025])
    cb_s = fig.colorbar(im_s, cax=cax_s, orientation="horizontal")
    cb_s.set_label("SpO2 %", fontsize=8)
    cb_s.ax.xaxis.set_label_position("top")
    cb_s.ax.xaxis.tick_top()

    # Median overlay panel — twin axis
    x = np.arange(MAX_MIN)
    ax_med.plot(x, spo2_med, color="steelblue", lw=1.7, label="SpO2 median")
    ax_med.axhline(90, color="orange", lw=0.7, linestyle="--", alpha=0.6)
    ax_med.set_ylabel("SpO2 %", color="steelblue", fontsize=9)
    ax_med.set_ylim(86, 100)
    ax_med.set_xlim(0, MAX_MIN)
    ax_med.tick_params(axis="y", labelcolor="steelblue")
    for xv in [90, 180, 270, 360]:
        ax_med.axvline(xv, color="black", lw=0.4, alpha=0.4, linestyle=":")
    ax_med.axvspan(90, 270, color="black", alpha=0.06, zorder=0)
    ax_med.set_xlabel("Minutes from sleep onset")

    ax_hr_twin = ax_med.twinx()
    ax_hr_twin.plot(x, hr_med, color="#d7301f", lw=1.7, label="HR median")
    ax_hr_twin.set_ylabel("HR (bpm)", color="#d7301f", fontsize=9)
    finite_hr = hr_med[np.isfinite(hr_med)]
    if finite_hr.size:
        lo = max(45, float(np.nanmin(finite_hr)) - 3)
        hi = float(np.nanmax(finite_hr)) + 3
        ax_hr_twin.set_ylim(lo, hi)
    ax_hr_twin.tick_params(axis="y", labelcolor="#d7301f")

    ax_top = ax_med.secondary_xaxis("top")
    ax_top.set_xticks([45, 135, 225, 315, 405])
    ax_top.set_xticklabels(["C1", "C2", "C3", "C4", "C5+"], fontsize=9)

    # Stat block (printed in figure footer)
    stat_lines = []
    if not np.isnan(median_delta):
        stat_lines.append(
            f"ΔHR (desat vs normal minutes): median {median_delta:+.2f} bpm, "
            f"mean {mean_delta:+.2f}, ΔHR>0 in {n_positive}/{len(valid_deltas)} nights"
        )
        if not np.isnan(wilcox_p):
            verdict = "✓ HYPOTHESIS SUPPORTED" if (wilcox_p < 0.05 and mean_delta > 0) else "✗ inconclusive"
            stat_lines.append(f"Wilcoxon signed-rank (one-sided ΔHR>0): p = {wilcox_p:.4f}  ·  {verdict}")
    if not np.isnan(rho_total):
        stat_lines.append(
            f"Pooled minute-level Spearman ρ(SpO2, HR) = {rho_total:+.3f} "
            f"(n={int(flat_mask.sum())} minutes, p = {rho_p:.2e}; expect negative if desat→HR↑)"
        )
    stat_lines.append(
        f"Single-device cohort: Garmin Venu 4 (deviceId {VENU4_DEVICE_ID}). "
        f"SpO2 = minute nadir, HR = minute max (1-2 min Garmin sampling)."
    )
    fig.text(0.5, 0.005, "  |  ".join(stat_lines[:-1]) + "\n" + stat_lines[-1],
             ha="center", fontsize=8, color="dimgray")

    out = OUT_DIR / "spo2_hr_overlay_all_nights.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")

    print(f"\n=== Venu 4 cohort: {n_nights} nights ({nights[0]['date']} → {nights[-1]['date']}) ===")
    print(f"\nHypothesis: SpO2 desaturation drives HR rise (arousal-mediated sympathetic surge).")
    print(f"\nPer-night ΔHR = mean(HR | SpO2<90%) − mean(HR | SpO2≥90%):")
    print(f"  {'Date':<12} {'ΔHR (bpm)':>10}  {'desat min':>10}  {'normal min':>11}")
    print(f"  {'-'*12} {'-'*10}  {'-'*10}  {'-'*11}")
    for d, dlt, nd, nn in per_night:
        ds = f"{dlt:+.2f}" if dlt is not None else "   —"
        print(f"  {d:<12} {ds:>10}  {nd:>10}  {nn:>11}")

    if not np.isnan(median_delta):
        print(f"\nCohort summary (N={len(valid_deltas)} nights with desat coverage):")
        print(f"  Median ΔHR = {median_delta:+.2f} bpm")
        print(f"  Mean ΔHR   = {mean_delta:+.2f} bpm")
        print(f"  ΔHR > 0    = {n_positive}/{len(valid_deltas)} nights ({100*n_positive/len(valid_deltas):.0f}%)")
        if not np.isnan(wilcox_p):
            print(f"  Wilcoxon signed-rank (H1: ΔHR > 0): p = {wilcox_p:.4f}")
    if not np.isnan(rho_total):
        print(f"\nPooled minute-level Spearman ρ(SpO2, HR) = {rho_total:+.3f}, p = {rho_p:.2e}")
        print(f"  (negative ρ ⇒ low SpO2 minutes coincide with high HR — supports hypothesis)")


if __name__ == "__main__":
    main()
