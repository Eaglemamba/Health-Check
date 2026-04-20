#!/usr/bin/env python3
"""Plot yearly SpO2 trend with device-change annotation.

Device history (confirmed 2026-04-20):
- 2018 → ~2024: Vivoactive 3 — NO Pulse Ox sensor
- 2024 Q4 / 2025 onwards: Vivoactive 5 — Pulse Ox, all-night sleep sampling

Therefore the 2024→2025 "drop" of 12.6 points is NOT a physiology change
and NOT a firmware rule change. It is the first year SpO2 was actually
measurable. 2025 is the true baseline year. 2025→2026 (-1.7 Low) is the
first valid year-over-year comparison.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.expanduser("~/Health-Check/reports/garmin-sleep-charts")
os.makedirs(OUT_DIR, exist_ok=True)

years   = [2024,  2025,  2026]
nights  = [87,    294,   104]
avg_sp  = [97.0,  96.1,  95.8]
low_sp  = [97.0,  84.4,  82.8]

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(11, 7.5), sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
)

x = np.arange(len(years))

# Device-change shaded zones
ax1.axvspan(-0.5, 0.5, color="#e2e8f0", alpha=0.6)
ax1.axvspan(0.5, 2.5, color="#c6f6d5", alpha=0.35)
ax1.text(0, 68, "Vivoactive 3\n(no Pulse Ox sensor)",
         ha="center", va="bottom", fontsize=10, color="#4a5568",
         bbox=dict(boxstyle="round,pad=0.35", fc="#f7fafc", ec="#a0aec0"))
ax1.text(1.5, 68, "Vivoactive 5 — true baseline",
         ha="center", va="bottom", fontsize=10, color="#22543d",
         bbox=dict(boxstyle="round,pad=0.35", fc="#c6f6d5", ec="#38a169"))

# Device boundary
ax1.axvline(0.5, color="#805ad5", linestyle="--", linewidth=2, alpha=0.8)
ax1.text(0.52, 99.3, "watch swap\n(Vivoactive 3 → 5)",
         fontsize=9, color="#44337a", va="top")

# Data series
ax1.plot(x, avg_sp, "o-", color="#2b6cb0", linewidth=2, markersize=10, label="Average SpO2")
ax1.plot(x, low_sp, "s-", color="#e53e3e", linewidth=2, markersize=10, label="Lowest SpO2")

for xi, a, l in zip(x, avg_sp, low_sp):
    ax1.annotate(f"{a:.1f}", (xi, a), textcoords="offset points",
                 xytext=(0, 10), ha="center", fontsize=9, color="#2b6cb0")
    ax1.annotate(f"{l:.1f}", (xi, l), textcoords="offset points",
                 xytext=(0, -18), ha="center", fontsize=9, color="#e53e3e")

# Grey-out 2024 data as "pseudo"
ax1.plot([0], [97.0], "o", color="#a0aec0", markersize=14, markerfacecolor="none",
         markeredgewidth=2, zorder=5)

ax1.axhline(90, color="#718096", linestyle=":", linewidth=1, alpha=0.7,
            label="90% clinical hypoxia threshold")
ax1.axhspan(0, 90, color="#fed7d7", alpha=0.2)

# Annotate real finding
ax1.annotate(
    "2024 values NOT a true measurement\n— Vivoactive 3 has no Pulse Ox.\nThe apparent drop is a device artifact.",
    xy=(0, 97.0), xytext=(0.15, 84),
    arrowprops=dict(arrowstyle="->", color="#a0aec0"),
    fontsize=9, color="#2d3748",
    bbox=dict(boxstyle="round,pad=0.4", fc="#edf2f7", ec="#a0aec0")
)

ax1.annotate(
    "2025 → 2026: Low −1.7, Avg −0.3\nSame device, same sampling →\nreal physiological drift.",
    xy=(2, 82.8), xytext=(1.0, 73),
    arrowprops=dict(arrowstyle="->", color="#38a169"),
    fontsize=9, color="#22543d",
    bbox=dict(boxstyle="round,pad=0.4", fc="#c6f6d5", ec="#38a169")
)

ax1.set_title(
    "Yearly SpO2 Trend — device-aware reading\n"
    "Vivoactive 3 → 5 swap explains 2024→2025; 2025→2026 is the first valid YoY",
    fontsize=12,
)
ax1.set_ylabel("SpO2 (%)")
ax1.set_ylim(65, 101)
ax1.legend(loc="lower left", fontsize=9)
ax1.grid(alpha=0.3)

# Nights bar
ax2.bar(x, nights, color="#4299e1", alpha=0.7)
ax2.bar([0], [87], color="#a0aec0", alpha=0.6)
for xi, n in zip(x, nights):
    ax2.text(xi, n + 10, f"n={n}", ha="center", fontsize=9)
ax2.set_ylabel("Nights measured")
ax2.set_xticks(x)
ax2.set_xticklabels(years, fontsize=11)
ax2.grid(alpha=0.3, axis="y")
ax2.set_ylim(0, max(nights) * 1.25)

fig.tight_layout()
out = os.path.join(OUT_DIR, "10_spo2_yearly_trend.png")
fig.savefig(out, dpi=120, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out}")
