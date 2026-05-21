"""
頭部楔形枕 pre/post C1 SpO2 對照 — one-shot 自然實驗分析。

楔形枕啟用日：2026-05-14（user-stated）
Pre  cohort: Venu 4 nights, 2026-04-24 → 2026-05-13 (N=20)
Post cohort: Venu 4 nights, 2026-05-14 → today

Output: reviews/daily/spo2/spo2_wedge_pre_post_{today}.png
  - Panel A: C1 T90 box plot (pre vs post)
  - Panel B: C1 nadir box plot
  - Panel C: Full-night T90 box plot
  - Panel D: Per-night C1 T90 timeline (with wedge start marker)
"""
import json
from pathlib import Path
from datetime import datetime, timezone, date
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

VENU4_DEVICE_ID = 3622900919
WEDGE_START = "2026-05-14"


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
    epochs = sleep.get("wellnessEpochSPO2DataDTOList") or []
    if not epochs or epochs[0].get("deviceId") != VENU4_DEVICE_ID:
        return None

    c1_vals, all_vals = [], []
    for e in epochs:
        ts_raw = e.get("epochTimestamp")
        ts = parse_gmt(ts_raw) if isinstance(ts_raw, str) else datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc)
        if ts < sleep_start or ts > sleep_end:
            continue
        v = e.get("spo2Reading")
        if not v or v <= 0:
            continue
        em = (ts - sleep_start).total_seconds() / 60
        all_vals.append(v)
        if em < 90:
            c1_vals.append(v)
    if not c1_vals or not all_vals:
        return None

    c1 = np.array(c1_vals)
    fa = np.array(all_vals)
    return {
        "date": p.stem,
        "c1_nadir": int(c1.min()),
        "c1_t90": 100 * (c1 < 90).sum() / len(c1),
        "all_t90": 100 * (fa < 90).sum() / len(fa),
    }


def main():
    nights = []
    for p in sorted(DATA_DIR.glob("20*.json")):
        n = load_night(p)
        if n:
            nights.append(n)
    nights.sort(key=lambda n: n["date"])
    if not nights:
        print("No Venu 4 nights found.")
        return

    pre = [n for n in nights if n["date"] < WEDGE_START]
    post = [n for n in nights if n["date"] >= WEDGE_START]
    today = nights[-1]["date"]

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(
        f"Head-elevation wedge — pre/post SpO2 analysis\n"
        f"Wedge start: {WEDGE_START}  ·  Pre N={len(pre)} (4/24 – 5/13)  ·  Post N={len(post)} ({WEDGE_START} – {today})",
        fontsize=12,
    )

    # Panel A: C1 T90
    ax = axes[0, 0]
    pre_c1t = [r["c1_t90"] for r in pre]
    post_c1t = [r["c1_t90"] for r in post]
    bp = ax.boxplot([pre_c1t, post_c1t], labels=["PRE", "POST"], widths=0.5,
                    patch_artist=True, showmeans=True,
                    meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black"))
    for patch, color in zip(bp["boxes"], ["#d9534f", "#5cb85c"]):
        patch.set_facecolor(color); patch.set_alpha(0.55)
    # scatter
    for i, vals in enumerate([pre_c1t, post_c1t]):
        jitter = (np.random.RandomState(42 + i).random(len(vals)) - 0.5) * 0.15
        ax.scatter([i + 1 + j for j in jitter], vals, s=22, color="black", alpha=0.55, zorder=3)
    ax.set_ylabel("C1 T90 (%)")
    ax.set_title(f"C1 T90 (0-90 min)  ·  median {np.median(pre_c1t):.2f}% → {np.median(post_c1t):.2f}%  ({100*(np.median(post_c1t)-np.median(pre_c1t))/max(np.median(pre_c1t),0.01):+.0f}%)")
    ax.axhline(10, color="red", lw=0.6, linestyle="--", alpha=0.5, label="severe OSA threshold 10%")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    # Panel B: C1 nadir
    ax = axes[0, 1]
    pre_c1n = [r["c1_nadir"] for r in pre]
    post_c1n = [r["c1_nadir"] for r in post]
    bp = ax.boxplot([pre_c1n, post_c1n], labels=["PRE", "POST"], widths=0.5,
                    patch_artist=True, showmeans=True,
                    meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black"))
    for patch, color in zip(bp["boxes"], ["#d9534f", "#5cb85c"]):
        patch.set_facecolor(color); patch.set_alpha(0.55)
    for i, vals in enumerate([pre_c1n, post_c1n]):
        jitter = (np.random.RandomState(42 + i).random(len(vals)) - 0.5) * 0.15
        ax.scatter([i + 1 + j for j in jitter], vals, s=22, color="black", alpha=0.55, zorder=3)
    ax.set_ylabel("C1 nadir SpO2 (%)")
    ax.set_title(f"C1 nadir  ·  median {np.median(pre_c1n):.0f}% → {np.median(post_c1n):.0f}%")
    ax.axhline(88, color="red", lw=0.6, linestyle="--", alpha=0.5, label="OSA red-flag 88%")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", alpha=0.3)

    # Panel C: Full-night T90
    ax = axes[1, 0]
    pre_ft = [r["all_t90"] for r in pre]
    post_ft = [r["all_t90"] for r in post]
    bp = ax.boxplot([pre_ft, post_ft], labels=["PRE", "POST"], widths=0.5,
                    patch_artist=True, showmeans=True,
                    meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black"))
    for patch, color in zip(bp["boxes"], ["#d9534f", "#5cb85c"]):
        patch.set_facecolor(color); patch.set_alpha(0.55)
    for i, vals in enumerate([pre_ft, post_ft]):
        jitter = (np.random.RandomState(42 + i).random(len(vals)) - 0.5) * 0.15
        ax.scatter([i + 1 + j for j in jitter], vals, s=22, color="black", alpha=0.55, zorder=3)
    ax.set_ylabel("Full-night T90 (%)")
    ax.set_title(f"Full-night T90  ·  median {np.median(pre_ft):.2f}% → {np.median(post_ft):.2f}%  ({100*(np.median(post_ft)-np.median(pre_ft))/max(np.median(pre_ft),0.01):+.0f}%)")
    ax.axhline(10, color="red", lw=0.6, linestyle="--", alpha=0.5, label="severe OSA threshold 10%")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    # Panel D: timeline
    ax = axes[1, 1]
    dates = [n["date"] for n in nights]
    c1_t90 = [n["c1_t90"] for n in nights]
    all_t90 = [n["all_t90"] for n in nights]
    x = np.arange(len(dates))
    ax.plot(x, c1_t90, marker="o", lw=1.5, color="#4a90e2", label="C1 T90")
    ax.plot(x, all_t90, marker="s", lw=1.2, color="gray", alpha=0.6, label="Full T90")
    wedge_idx = next((i for i, d in enumerate(dates) if d >= WEDGE_START), len(dates))
    ax.axvline(wedge_idx - 0.5, color="red", lw=2, alpha=0.7, label=f"Wedge start {WEDGE_START}")
    ax.axhline(10, color="red", lw=0.6, linestyle="--", alpha=0.4)
    ax.set_ylabel("T90 (%)")
    ax.set_xticks(x[::3])
    ax.set_xticklabels([d[5:] for d in dates[::3]], rotation=45, fontsize=8)
    ax.set_title("Per-night timeline")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(alpha=0.3)

    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    fig.text(0.5, 0.005,
             f"Single-device cohort: Garmin Venu 4. Observational, within-subject, no control. "
             f"Co-interventions present (5/17 forced lateral travel; 5/19 nasal rinse; 5/20 matcha). "
             f"Diamond = mean.",
             ha="center", fontsize=7.5, style="italic", color="dimgray")

    out = OUT_DIR / f"spo2_wedge_pre_post_{today}.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")
    print(f"\nPre N={len(pre)} C1 T90: mean={np.mean(pre_c1t):.2f}% median={np.median(pre_c1t):.2f}%")
    print(f"Post N={len(post)} C1 T90: mean={np.mean(post_c1t):.2f}% median={np.median(post_c1t):.2f}%")
    print(f"Δ C1 T90 median: {np.median(post_c1t)-np.median(pre_c1t):+.2f}% ({100*(np.median(post_c1t)-np.median(pre_c1t))/np.median(pre_c1t):+.0f}%)")


if __name__ == "__main__":
    main()
