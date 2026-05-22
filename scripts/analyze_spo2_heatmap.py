"""
SpO2 全夜 heatmap — 33+ 晚疊圖。

每一晚一橫列，x 軸入睡後分鐘，色階 SpO2 75-100%。
下方副圖：每分鐘中位數 + IQR（25-75 百分位）。

用途：
  - 視覺化「C2-C3 (90-270 min) 塌陷帶」是 robust 還是少數夜驅動
  - 揪 outlier 夜 → 對照當天介入 / 體位 / 晚餐 → 找可控變因

Output:
  reviews/daily/spo2/spo2_heatmap_all_nights.png
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

MAX_MIN = 480  # 8 小時
SPO2_MIN_VIS = 80  # color scale lower bound
SPO2_MAX_VIS = 100

# Device filter — Venu 4 only. Earlier device (3471541259, used 4/19-4/23) had
# different SpO2 sensor characteristics and is excluded for cross-night consistency.
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

    # Device filter — skip nights from non-Venu 4 devices
    first_device = epochs_raw[0].get("deviceId") if epochs_raw else None
    if first_device != VENU4_DEVICE_ID:
        return None

    minute_min = {}  # minute_int -> min SpO2 in that minute
    for e in epochs_raw:
        ts_raw = e.get("epochTimestamp")
        if isinstance(ts_raw, str):
            ts = parse_gmt(ts_raw)
        else:
            ts = datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc)
        if ts < sleep_start or ts > sleep_end:
            continue
        em = int((ts - sleep_start).total_seconds() / 60)
        val = e.get("spo2Reading")
        if val is None or val <= 0:
            continue
        if em < 0 or em >= MAX_MIN:
            continue
        if em not in minute_min or val < minute_min[em]:
            minute_min[em] = val

    if not minute_min:
        return None

    arr = np.full(MAX_MIN, np.nan)
    for em, v in minute_min.items():
        arr[em] = v

    return {
        "date": p.stem,
        "tst_min": (sleep_end - sleep_start).total_seconds() / 60,
        "spo2_per_min": arr,
    }


def main():
    files = sorted(DATA_DIR.rglob("20*.json"))
    nights = []
    for f in files:
        n = load_night(f)
        if n is not None:
            nights.append(n)
    if not nights:
        print("No usable nights.")
        return

    nights.sort(key=lambda n: n["date"])
    matrix = np.array([n["spo2_per_min"] for n in nights])

    n_nights = matrix.shape[0]
    dates = [n["date"][5:] for n in nights]  # MM-DD
    nadirs = [int(np.nanmin(n["spo2_per_min"])) if not np.all(np.isnan(n["spo2_per_min"])) else None for n in nights]
    t90s = []
    for n in nights:
        v = n["spo2_per_min"]
        v = v[~np.isnan(v)]
        t90s.append(100 * (v < 90).sum() / len(v) if len(v) else None)

    # Median + IQR per minute across nights
    med = np.nanmedian(matrix, axis=0)
    q25 = np.nanpercentile(matrix, 25, axis=0)
    q75 = np.nanpercentile(matrix, 75, axis=0)
    cov = (~np.isnan(matrix)).sum(axis=0)

    fig = plt.figure(figsize=(14, max(8, 0.22 * n_nights + 4)))
    gs = fig.add_gridspec(
        2, 2,
        height_ratios=[max(4, 0.22 * n_nights), 2.5],
        width_ratios=[1, 0.025],
        hspace=0.12, wspace=0.02,
    )
    ax_hm = fig.add_subplot(gs[0, 0])
    ax_cb = fig.add_subplot(gs[0, 1])
    ax_med = fig.add_subplot(gs[1, 0], sharex=ax_hm)

    # Heatmap
    cmap = plt.get_cmap("RdYlGn")
    im = ax_hm.imshow(
        matrix,
        aspect="auto",
        origin="upper",
        cmap=cmap,
        vmin=SPO2_MIN_VIS, vmax=SPO2_MAX_VIS,
        extent=[0, MAX_MIN, n_nights, 0],
        interpolation="nearest",
    )
    ax_hm.set_yticks(np.arange(n_nights) + 0.5)
    annotated = []
    for i, (d, nad, t90) in enumerate(zip(dates, nadirs, t90s)):
        if nad is None or t90 is None:
            annotated.append(d)
        else:
            annotated.append(f"{d}  n{nad}  T{t90:.1f}%")
    ax_hm.set_yticklabels(annotated, fontsize=7)
    ax_hm.set_xlim(0, MAX_MIN)
    ax_hm.set_xlabel("Minutes from sleep onset")
    ax_hm.set_title(
        f"SpO2 heatmap — {n_nights} nights ({nights[0]['date']} → {nights[-1]['date']})\n"
        f"Each row = 1 night (nadir per minute); annotation = date  nadir  T90",
        fontsize=10,
    )
    # Cycle band markers
    for x in [90, 180, 270, 360]:
        ax_hm.axvline(x, color="black", lw=0.4, alpha=0.4, linestyle=":")
    # Highlight C2-C3 worst band
    ax_hm.axvspan(90, 270, color="black", alpha=0.06, zorder=0)

    cb = fig.colorbar(im, cax=ax_cb)
    cb.set_label("SpO2 %", fontsize=9)

    # Median + IQR panel
    x = np.arange(MAX_MIN)
    ax_med.fill_between(x, q25, q75, alpha=0.25, color="steelblue", label="IQR (25-75)")
    ax_med.plot(x, med, color="steelblue", lw=1.6, label="Median")
    ax_med.axhline(90, color="orange", lw=0.7, linestyle="--", alpha=0.6, label="90% threshold")
    ax_med.axhline(88, color="red", lw=0.7, linestyle="--", alpha=0.6, label="88% OSA red-flag")
    for xv in [90, 180, 270, 360]:
        ax_med.axvline(xv, color="black", lw=0.4, alpha=0.4, linestyle=":")
    ax_med.axvspan(90, 270, color="black", alpha=0.06, zorder=0)
    ax_med.set_xlabel("Minutes from sleep onset")
    ax_med.set_ylabel("SpO2 %")
    ax_med.set_ylim(82, 100)
    ax_med.set_xlim(0, MAX_MIN)
    ax_med.legend(loc="lower right", fontsize=8, ncol=4)

    # Annotate cycle bins on top axis
    ax_top = ax_med.secondary_xaxis("top")
    ax_top.set_xticks([45, 135, 225, 315, 405])
    ax_top.set_xticklabels(["C1", "C2", "C3", "C4", "C5+"], fontsize=9)

    # Device-consistency caption
    fig.text(
        0.5, 0.005,
        f"Single-device cohort: Garmin Venu 4 (deviceId {VENU4_DEVICE_ID}). "
        f"Earlier device (4/19-4/23, 5 nights) excluded for SpO2 sensor consistency.",
        ha="center", fontsize=7.5, style="italic", color="dimgray",
    )

    out = OUT_DIR / "spo2_heatmap_all_nights.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")
    print(f"Nights: {n_nights}, range {nights[0]['date']} → {nights[-1]['date']}")

    # Quick outlier console table — bottom 5 by T90
    pairs = [(d, t) for d, t in zip(dates, t90s) if t is not None]
    pairs.sort(key=lambda x: -x[1])
    print("\nTop 5 worst nights (T90 %):")
    for d, t in pairs[:5]:
        print(f"  {d}  T90 = {t:.1f}%")
    print("\nTop 5 best nights (T90 %):")
    for d, t in sorted(pairs, key=lambda x: x[1])[:5]:
        print(f"  {d}  T90 = {t:.1f}%")


if __name__ == "__main__":
    main()
