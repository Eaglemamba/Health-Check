#!/usr/bin/env python3
"""Comprehensive 8-year Garmin analysis.

Loads:
  - UDS daily summaries (steps, RHR, stress, body battery, SpO2, intensity)
  - VO2max / MaxMet metrics
  - FitnessAge data (bioAge vs chronological)
  - BioMetrics (weight, height)
  - AbnormalHrEvents (5+ years)
  - Activities (exercise sessions)
  - HealthStatus (LHA daily with baselines, 2025-09+)
  - Sleep (already loaded via analyze_garmin_sleep)

Outputs a unified markdown report + charts to
~/Health-Check/reports/garmin-full-analysis.md.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.expanduser("~/Health-Check/scripts"))
from analyze_garmin_sleep import load_nights  # reuse sleep loader

BASE = os.path.expanduser(
    "~/Downloads/eefa96d4-19bc-4be1-930c-f10a197cd658_1/DI_CONNECT"
)
AGG = f"{BASE}/DI-Connect-Aggregator"
WELLNESS = f"{BASE}/DI-Connect-Wellness"
METRICS = f"{BASE}/DI-Connect-Metrics"
FITNESS = f"{BASE}/DI-Connect-Fitness"

REPORT_DIR = os.path.expanduser("~/Health-Check/reports")
CHART_DIR = os.path.join(REPORT_DIR, "garmin-full-charts")
TAIPEI = timezone(timedelta(hours=8))


def load_json_files(pattern):
    """Load and concatenate list records from files matching the glob pattern."""
    records = []
    for p in sorted(glob.glob(pattern)):
        try:
            with open(p) as f:
                d = json.load(f)
            if isinstance(d, list):
                records.extend(d)
        except Exception as e:
            print(f"  WARN: failed to load {p}: {e}")
    return records


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pct(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def load_uds():
    """Daily summaries. Deduplicate by calendarDate, keep most complete record."""
    records = load_json_files(f"{AGG}/UDSFile_*.json")
    by_date = {}
    for r in records:
        cal = r.get("calendarDate")
        if not cal:
            continue
        if cal not in by_date:
            by_date[cal] = r
        else:
            # Merge: prefer the record with more non-null fields
            cur = by_date[cal]
            if sum(1 for v in r.values() if v not in (None, 0, 0.0)) > sum(
                1 for v in cur.values() if v not in (None, 0, 0.0)
            ):
                by_date[cal] = r
    def unwrap_stress(v):
        if not isinstance(v, dict):
            return v if isinstance(v, (int, float)) else None
        for agg in v.get("aggregatorList") or []:
            if agg.get("type") == "TOTAL":
                return agg.get("averageStressLevel")
        return None

    def unwrap_bb(v):
        if not isinstance(v, dict):
            return v if isinstance(v, (int, float)) else None
        for stat in v.get("bodyBatteryStatList") or []:
            if stat.get("bodyBatteryStatType") == "HIGHEST":
                return stat.get("statsValue")
        return v.get("chargedValue")

    def unwrap_resp(v):
        if isinstance(v, dict):
            return v.get("avgWakingRespirationValue") or v.get("avgValue")
        return v if isinstance(v, (int, float)) else None

    rows = []
    for cal, r in sorted(by_date.items()):
        try:
            date = datetime.strptime(cal, "%Y-%m-%d").date()
        except ValueError:
            continue
        rows.append({
            "date": date,
            "steps": r.get("totalSteps"),
            "step_goal": r.get("dailyStepGoal"),
            "total_kcal": r.get("totalKilocalories"),
            "active_kcal": r.get("activeKilocalories"),
            "bmr_kcal": r.get("bmrKilocalories"),
            "moderate_min": r.get("moderateIntensityMinutes"),
            "vigorous_min": r.get("vigorousIntensityMinutes"),
            "is_vigorous_day": r.get("isVigorousDay"),
            "min_hr": r.get("minHeartRate"),
            "max_hr": r.get("maxHeartRate"),
            "rhr": r.get("restingHeartRate") or r.get("currentDayRestingHeartRate"),
            "all_day_stress": unwrap_stress(r.get("allDayStress")),
            "body_battery": unwrap_bb(r.get("bodyBattery")),
            "avg_spo2": r.get("averageSpo2Value"),
            "low_spo2": r.get("lowestSpo2Value"),
            "respiration": unwrap_resp(r.get("respiration")),
        })
    return rows


def load_vo2max():
    records = load_json_files(f"{METRICS}/MetricsMaxMetData_*.json")
    rows = []
    for r in records:
        cal = r.get("calendarDate")
        if not cal:
            continue
        try:
            date = datetime.strptime(cal, "%Y-%m-%d").date()
        except ValueError:
            continue
        rows.append({
            "date": date,
            "vo2max": r.get("vo2MaxValue"),
            "fitness_age": int(r.get("fitnessAge")) if r.get("fitnessAge") else None,
            "category": r.get("maxMetCategory"),
        })
    rows.sort(key=lambda x: x["date"])
    return rows


def load_fitness_age():
    with open(f"{WELLNESS}/72396565_fitnessAgeData.json") as f:
        data = json.load(f)
    rows = []
    for r in data:
        ts = r.get("asOfDateGmt")
        if not ts:
            continue
        try:
            date = datetime.fromisoformat(ts.replace(".0", "")).date()
        except Exception:
            continue
        rows.append({
            "date": date,
            "chrono_age": r.get("chronologicalAge"),
            "bmi": r.get("bmi"),
            "rhr": r.get("rhr"),
            "vigorous_days": r.get("totalVigorousDays"),
            "vigorous_ims": r.get("totalVigorousIMs"),
            "bio_vo2max": r.get("biometricVo2Max"),
            "current_bio_age": r.get("currentBioAge"),
            "healthy_bio_age": r.get("healthyAllBioAge"),
            "healthy_rhr_age": r.get("healthyRhrBioAge"),
            "healthy_active_age": r.get("healthyActiveBioAge"),
            "healthy_bmi_fat_age": r.get("healthyBmiFatBioAge"),
        })
    rows.sort(key=lambda x: x["date"])
    return rows


def load_biometrics():
    with open(f"{WELLNESS}/72396565_userBioMetrics.json") as f:
        data = json.load(f)
    rows = []
    for r in data:
        md = r.get("metaData") or {}
        cal = md.get("calendarDate")
        if not cal:
            continue
        try:
            date = datetime.fromisoformat(cal.replace(".0", "")).date()
        except Exception:
            continue
        wt = r.get("weight")
        # Garmin wraps weight as {"weight": grams, "sourceType": "..."}
        if isinstance(wt, dict):
            wt = wt.get("weight")
        rows.append({
            "date": date,
            "height": r.get("height"),
            "weight": wt,
            "activity_class": r.get("activityClass"),
            "vo2max_running": r.get("vo2MaxRunning"),
            "vo2max_cycling": r.get("vo2MaxCycling"),
            "lactate_hr": r.get("lactateThresholdHR"),
        })
    rows.sort(key=lambda x: x["date"])
    return rows


def load_abnormal_hr():
    records = load_json_files(f"{WELLNESS}/*AbnormalHrEvents.json")
    rows = []
    for r in records:
        cal = r.get("calendarDate")
        if not cal:
            continue
        try:
            date = datetime.strptime(cal, "%Y-%m-%d").date()
        except ValueError:
            continue
        rows.append({
            "date": date,
            "hr_value": r.get("abnormalHrValue"),
            "threshold": r.get("abnormalHrThresholdValue"),
        })
    rows.sort(key=lambda x: x["date"])
    return rows


def load_activities():
    path = f"{FITNESS}/eaglemamba@gmail.com_0_summarizedActivities.json"
    with open(path) as f:
        wrapper = json.load(f)
    items = wrapper[0].get("summarizedActivitiesExport") if wrapper else []
    rows = []
    for a in items or []:
        ts = a.get("startTimeLocal")
        if not ts:
            continue
        try:
            date = datetime.fromtimestamp(ts / 1000, tz=TAIPEI).date()
        except Exception:
            continue
        rows.append({
            "date": date,
            "type": a.get("activityType"),
            "sport_type": a.get("sportType"),
            "duration_s": (a.get("duration") or 0) / 1000,
            "distance_m": a.get("distance"),
            "elevation_gain": a.get("elevationGain"),
            "avg_hr": a.get("avgHr"),
            "max_hr": a.get("maxHr"),
            "avg_speed": a.get("avgSpeed"),
            "calories": a.get("calories"),
            "moderate_min": a.get("moderateIntensityMinutes"),
            "vigorous_min": a.get("vigorousIntensityMinutes"),
            "aerobic_te": a.get("aerobicTrainingEffect"),
            "anaerobic_te": a.get("anaerobicTrainingEffect"),
            "name": a.get("activityName") or a.get("name"),
        })
    rows.sort(key=lambda x: x["date"])
    return rows


def load_health_status():
    records = load_json_files(f"{WELLNESS}/*healthStatusData.json")
    rows = []
    for r in records:
        cal = r.get("calendarDate")
        if not cal:
            continue
        try:
            date = datetime.strptime(cal, "%Y-%m-%d").date()
        except ValueError:
            continue
        by_type = {m.get("type"): m for m in r.get("metrics") or []}
        rows.append({
            "date": date,
            "outliers": r.get("outliersCount"),
            "hrv": (by_type.get("HRV") or {}).get("value"),
            "hrv_status": (by_type.get("HRV") or {}).get("status"),
            "hr": (by_type.get("HR") or {}).get("value"),
            "hr_status": (by_type.get("HR") or {}).get("status"),
            "spo2": (by_type.get("SPO2") or {}).get("value"),
            "spo2_status": (by_type.get("SPO2") or {}).get("status"),
            "respiration": (by_type.get("RESPIRATION") or {}).get("value"),
            "stress": (by_type.get("STRESS") or {}).get("value"),
            "body_battery": (by_type.get("BODY_BATTERY") or {}).get("value"),
        })
    rows.sort(key=lambda x: x["date"])
    return rows


def group_by_month(rows, key):
    g = defaultdict(list)
    for r in rows:
        v = r.get(key)
        if v is not None:
            g[r["date"].strftime("%Y-%m")].append(v)
    return g


def group_by_year(rows, key):
    g = defaultdict(list)
    for r in rows:
        v = r.get(key)
        if v is not None:
            g[r["date"].year].append(v)
    return g


def fmt_num(x, digits=1):
    return f"{x:.{digits}f}" if x is not None else "—"


def chart_vo2max_trend(vo2_rows, chart_path):
    """VO2max over time with category bands."""
    dates = [r["date"] for r in vo2_rows]
    vals = [r["vo2max"] for r in vo2_rows]
    # monthly smoothing
    by_m = defaultdict(list)
    for r in vo2_rows:
        by_m[r["date"].strftime("%Y-%m")].append(r["vo2max"])
    months = sorted(by_m)
    m_vals = [mean(by_m[m]) for m in months]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(dates, vals, alpha=0.15, s=8, color="#2b6cb0", label="Daily")
    ax.plot(
        [datetime.strptime(m, "%Y-%m").date() for m in months],
        m_vals, color="#1a365d", linewidth=2, label="Monthly avg",
    )
    # Age-group category bands for men 30-40
    for y, label, color in [
        (55, "Superior", "#38a169"), (50, "Excellent", "#68d391"),
        (45, "Good", "#d69e2e"), (41, "Fair", "#ed8936"), (35, "Poor", "#e53e3e"),
    ]:
        ax.axhline(y, color=color, linestyle="--", linewidth=0.8, alpha=0.4)
        ax.text(dates[0], y + 0.2, label, fontsize=8, color=color, alpha=0.7)
    ax.set_title("VO2max (8-Year Trend) — Age-bracketed category lines (male 30-40)")
    ax.set_ylabel("VO2max (ml/kg/min)")
    ax.legend(loc="lower left")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)


def chart_fitness_age_gap(fa_rows, chart_path):
    """Bio age vs chronological age gap."""
    dates = [r["date"] for r in fa_rows if r["current_bio_age"] and r["chrono_age"]]
    gap = [r["current_bio_age"] - r["chrono_age"] for r in fa_rows if r["current_bio_age"] and r["chrono_age"]]
    healthy_gap = [
        r["healthy_bio_age"] - r["chrono_age"]
        for r in fa_rows
        if r["healthy_bio_age"] and r["chrono_age"]
    ]
    h_dates = [r["date"] for r in fa_rows if r["healthy_bio_age"] and r["chrono_age"]]
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.plot(dates, gap, color="#2b6cb0", linewidth=1.5, label="Current bio age − chrono age")
    ax.plot(h_dates, healthy_gap, color="#38a169", linewidth=1.5, linestyle="--", label="Healthy bio age − chrono age")
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.5)
    ax.fill_between(dates, gap, 0, where=np.array(gap) > 0, alpha=0.2, color="#e53e3e", label="Older than age")
    ax.fill_between(dates, gap, 0, where=np.array(gap) < 0, alpha=0.2, color="#38a169", label="Younger than age")
    ax.set_title("Fitness Age Gap (years younger/older than chronological age)")
    ax.set_ylabel("Years (+/-)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)


def chart_rhr_trend(uds_rows, chart_path):
    by_m = defaultdict(list)
    for r in uds_rows:
        if r["rhr"] and 35 <= r["rhr"] <= 100:  # filter outliers
            by_m[r["date"].strftime("%Y-%m")].append(r["rhr"])
    months = sorted(by_m)
    vals = [mean(by_m[m]) for m in months]
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(months, vals, color="#805ad5", linewidth=1.5)
    ax.axhline(60, color="#38a169", linestyle="--", linewidth=1, label="Good (<60)")
    ax.axhline(70, color="#d69e2e", linestyle="--", linewidth=1, label="Average (60-70)")
    ax.axhline(80, color="#e53e3e", linestyle="--", linewidth=1, label="Elevated (>80)")
    ax.set_title("Resting Heart Rate — Monthly Average")
    ax.set_ylabel("bpm")
    step = max(1, len(months) // 14)
    ax.set_xticks(range(0, len(months), step))
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
    ax.legend(loc="lower left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)


def chart_weight_trend(bio_rows, chart_path):
    # Weight is in grams in Garmin data; convert to kg
    pairs = [(r["date"], r["weight"] / 1000) for r in bio_rows if r["weight"] and 40 < r["weight"] / 1000 < 120]
    if not pairs:
        return False
    dates, kgs = zip(*pairs)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.scatter(dates, kgs, alpha=0.4, s=14, color="#2b6cb0", label="Measurements")
    # 30-day rolling mean
    if len(pairs) > 30:
        dates_s = sorted(pairs, key=lambda x: x[0])
        rolling = []
        for i, (d, _) in enumerate(dates_s):
            window = [v for x, v in dates_s if (d - x).days <= 30 and (d - x).days >= 0]
            rolling.append(mean(window))
        ax.plot([d for d, _ in dates_s], rolling, color="#1a365d", linewidth=2, label="30-day rolling avg")
    ax.axhline(69.16, color="#38a169", linestyle="--", linewidth=1, label="Target (69.16 kg BMI 24)")
    ax.axhline(72.06, color="#d69e2e", linestyle="--", linewidth=1, label="BMI 25")
    ax.set_title("Weight Trend (kg)")
    ax.set_ylabel("kg")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)
    return True


def chart_steps_activity(uds_rows, chart_path):
    """Monthly avg steps + intensity minutes."""
    by_m_steps = defaultdict(list)
    by_m_mod = defaultdict(list)
    by_m_vig = defaultdict(list)
    for r in uds_rows:
        m = r["date"].strftime("%Y-%m")
        if r["steps"]:
            by_m_steps[m].append(r["steps"])
        if r["moderate_min"] is not None:
            by_m_mod[m].append(r["moderate_min"])
        if r["vigorous_min"] is not None:
            by_m_vig[m].append(r["vigorous_min"])
    months = sorted(set(by_m_steps) | set(by_m_mod) | set(by_m_vig))
    steps = [mean(by_m_steps.get(m, [])) for m in months]
    mod = [mean(by_m_mod.get(m, [])) for m in months]
    vig = [mean(by_m_vig.get(m, [])) for m in months]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    ax1.plot(months, steps, color="#2b6cb0", linewidth=1.5)
    ax1.axhline(10000, color="#38a169", linestyle="--", linewidth=1, label="10k target")
    ax1.axhline(7500, color="#d69e2e", linestyle="--", linewidth=1, label="7.5k min")
    ax1.set_ylabel("Steps (daily avg)")
    ax1.set_title("Steps & Intensity Minutes (monthly)")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)
    ax2.plot(months, mod, color="#d69e2e", linewidth=1.5, label="Moderate IMs/day")
    ax2.plot(months, vig, color="#e53e3e", linewidth=1.5, label="Vigorous IMs/day")
    ax2.axhline(150 / 7, color="#38a169", linestyle="--", linewidth=1, label="WHO 150min/wk (21/day)")
    ax2.set_ylabel("Intensity minutes / day")
    step = max(1, len(months) // 12)
    ax2.set_xticks(range(0, len(months), step))
    ax2.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)


def chart_stress_body_battery(uds_rows, chart_path):
    by_m_stress = defaultdict(list)
    by_m_bb = defaultdict(list)
    for r in uds_rows:
        m = r["date"].strftime("%Y-%m")
        if r["all_day_stress"] is not None and 0 < r["all_day_stress"] < 100:
            by_m_stress[m].append(r["all_day_stress"])
        if r["body_battery"] is not None and 0 < r["body_battery"] < 100:
            by_m_bb[m].append(r["body_battery"])
    months = sorted(set(by_m_stress) | set(by_m_bb))
    stress = [mean(by_m_stress.get(m, [])) for m in months]
    bb = [mean(by_m_bb.get(m, [])) for m in months]
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(months, stress, color="#e53e3e", linewidth=1.5, label="All-day stress")
    ax.plot(months, bb, color="#38a169", linewidth=1.5, label="Body Battery")
    ax.set_title("Stress & Body Battery (monthly avg)")
    ax.set_ylabel("Score 0-100")
    step = max(1, len(months) // 14)
    ax.set_xticks(range(0, len(months), step))
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)


def chart_abnormal_hr(abnormal_rows, chart_path):
    by_ym = defaultdict(int)
    for r in abnormal_rows:
        by_ym[r["date"].strftime("%Y-%m")] += 1
    if not by_ym:
        return False
    months = sorted(by_ym)
    counts = [by_ym[m] for m in months]
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(months, counts, color="#e53e3e", alpha=0.7)
    ax.set_title("Abnormal Heart-Rate Events (monthly count)")
    ax.set_ylabel("Events")
    step = max(1, len(months) // 14)
    ax.set_xticks(range(0, len(months), step))
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)
    return True


def chart_activities_yearly(act_rows, chart_path):
    by_year = defaultdict(lambda: defaultdict(int))
    for r in act_rows:
        y = r["date"].year
        t = (r.get("type") or "other").lower()
        by_year[y][t] += 1
    years = sorted(by_year)
    all_types = sorted({t for y in by_year.values() for t in y})
    # Keep top 8 types by total count
    total_by_type = defaultdict(int)
    for y in by_year.values():
        for t, c in y.items():
            total_by_type[t] += c
    top_types = [t for t, _ in sorted(total_by_type.items(), key=lambda x: -x[1])[:8]]
    fig, ax = plt.subplots(figsize=(12, 5))
    bottom = np.zeros(len(years))
    colors = plt.cm.tab10(np.linspace(0, 1, len(top_types)))
    for i, t in enumerate(top_types):
        vals = [by_year[y].get(t, 0) for y in years]
        ax.bar(years, vals, bottom=bottom, label=t, color=colors[i])
        bottom += np.array(vals)
    ax.set_title("Recorded Activities per Year (by type, top 8)")
    ax.set_ylabel("Activity count")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)


def compute_yearly_summary(uds_rows, vo2_rows, fa_rows, bio_rows, abnormal_rows, act_rows):
    years = sorted({r["date"].year for r in uds_rows} | {r["date"].year for r in vo2_rows})
    rows = []
    for y in years:
        u = [r for r in uds_rows if r["date"].year == y]
        # Skip years with very sparse UDS (<30 days)
        uds_days = sum(1 for r in u if r["steps"] is not None)
        if uds_days < 30 and y < 2018:
            continue
        v = [r for r in vo2_rows if r["date"].year == y]
        f = [r for r in fa_rows if r["date"].year == y]
        b = [r for r in bio_rows if r["date"].year == y and r["weight"] and 40 < r["weight"] / 1000 < 120]
        ah = [r for r in abnormal_rows if r["date"].year == y]
        # Activities: filter out step-counter "walking" logs with multi-day durations
        a = [r for r in act_rows if r["date"].year == y and (r["duration_s"] or 0) < 86400 * 2]
        rows.append({
            "year": y,
            "uds_days": uds_days,
            "avg_steps": mean([r["steps"] for r in u]),
            "avg_rhr": mean([r["rhr"] for r in u if r["rhr"] and 35 <= r["rhr"] <= 100]),
            "avg_stress": mean([r["all_day_stress"] for r in u if r["all_day_stress"] and 0 < r["all_day_stress"] < 100]),
            "avg_bb": mean([r["body_battery"] for r in u if r["body_battery"] and 0 < r["body_battery"] < 100]),
            "avg_moderate": mean([r["moderate_min"] for r in u]),
            "avg_vigorous": mean([r["vigorous_min"] for r in u]),
            "weekly_intensity": (mean([r["moderate_min"] or 0 for r in u]) or 0) * 7 + (mean([r["vigorous_min"] or 0 for r in u]) or 0) * 14,
            "avg_vo2max": mean([r["vo2max"] for r in v]),
            "min_vo2max": min([r["vo2max"] for r in v], default=None),
            "max_vo2max": max([r["vo2max"] for r in v], default=None),
            "bio_age_gap": mean([r["current_bio_age"] - r["chrono_age"] for r in f if r["current_bio_age"] and r["chrono_age"]]),
            "weight_avg": mean([r["weight"] / 1000 for r in b]) if b else None,
            "weight_min": min([r["weight"] / 1000 for r in b]) if b else None,
            "weight_max": max([r["weight"] / 1000 for r in b]) if b else None,
            "abnormal_hr_events": len(ah),
            "activities": len(a),
        })
    return rows


def write_report(uds_rows, vo2_rows, fa_rows, bio_rows, abnormal_rows, act_rows, hs_rows, nights, yearly, chart_paths):
    md = []
    now = datetime.now(TAIPEI).strftime("%Y-%m-%d %H:%M")
    md.append("# Garmin 8-Year Comprehensive Health Analysis")
    md.append("")
    md.append(f"_Generated: {now} (Taipei)_  ")
    md.append(f"_Source: Garmin GDPR export, user 72396565_")
    md.append("")
    md.append("## 1. Data Inventory")
    md.append("")
    md.append("| Data source | Records | Earliest | Latest |")
    md.append("|---|---|---|---|")
    for label, rows in [
        ("Daily summary (UDS)", uds_rows),
        ("VO2max / MaxMet", vo2_rows),
        ("Fitness Age", fa_rows),
        ("BioMetrics (weight)", [r for r in bio_rows if r["weight"]]),
        ("Abnormal HR events", abnormal_rows),
        ("Recorded activities", act_rows),
        ("Health Status (LHA)", hs_rows),
        ("Sleep nights", nights),
    ]:
        if rows:
            md.append(f"| {label} | {len(rows)} | {rows[0]['date']} | {rows[-1]['date']} |")
        else:
            md.append(f"| {label} | 0 | — | — |")
    md.append("")

    md.append("## 2. Yearly Summary")
    md.append("")
    md.append(
        "| Year | UDS days | Steps | RHR | Stress | BB | Mod/day | Vig/day | Wkly IMs | VO2max (min→max) | Bio-age gap | AbnHR | Activities |"
    )
    md.append(
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|"
    )
    for r in yearly:
        vo2_str = "—"
        if r["avg_vo2max"] is not None:
            vo2_str = f"{r['avg_vo2max']:.1f} ({r['min_vo2max']:.0f}→{r['max_vo2max']:.0f})"
        md.append(
            f"| {r['year']} | {r['uds_days']} | {fmt_num(r['avg_steps'], 0)} | "
            f"{fmt_num(r['avg_rhr'])} | {fmt_num(r['avg_stress'])} | "
            f"{fmt_num(r['avg_bb'])} | {fmt_num(r['avg_moderate'])} | {fmt_num(r['avg_vigorous'])} | "
            f"{fmt_num(r['weekly_intensity'], 0)} | {vo2_str} | "
            f"{fmt_num(r['bio_age_gap'])} | {r['abnormal_hr_events']} | "
            f"{r['activities']} |"
        )
    md.append("")
    md.append("_Wkly IMs = weekly intensity minutes (moderate×7 + vigorous×14, WHO formula). Bio-age gap: negative = fitness age younger than chronological. Weight omitted from this table — only 4 entries in 8 years of BioMetrics; see Notes._")
    md.append("")

    # Correlations with PE findings
    md.append("## 3. Cross-Reference to PE Findings")
    md.append("")
    md.append("### 3.1 Cardiovascular (ECG ischemia 2025 new finding)")
    md.append("")
    # Find RHR 12-month trend before 2025-09 exam
    exam_2025 = datetime(2025, 9, 17).date()
    exam_2026 = datetime(2026, 3, 25).date()
    pre_exam_12m = [r for r in uds_rows if r["rhr"] and exam_2025 - timedelta(days=365) <= r["date"] < exam_2025]
    pre_exam_12m_rhr = mean([r["rhr"] for r in pre_exam_12m if 35 <= r["rhr"] <= 100])
    pre_exam_24_13m = [r for r in uds_rows if r["rhr"] and exam_2025 - timedelta(days=730) <= r["date"] < exam_2025 - timedelta(days=365)]
    pre_exam_24_13m_rhr = mean([r["rhr"] for r in pre_exam_24_13m if 35 <= r["rhr"] <= 100])
    abnormal_12m_pre = [r for r in abnormal_rows if exam_2025 - timedelta(days=365) <= r["date"] < exam_2025]
    abnormal_total = len(abnormal_rows)
    md.append(f"- **RHR 12 months before 2025-09 exam**: {fmt_num(pre_exam_12m_rhr)} bpm (n={len(pre_exam_12m)} days)")
    md.append(f"- **RHR 13-24 months before**: {fmt_num(pre_exam_24_13m_rhr)} bpm (n={len(pre_exam_24_13m)} days)")
    if pre_exam_12m_rhr and pre_exam_24_13m_rhr:
        md.append(f"- **RHR change**: {(pre_exam_12m_rhr - pre_exam_24_13m_rhr):+.1f} bpm in the year before the ischemia finding")
    md.append(f"- **Abnormal HR events 12 months pre-exam**: {len(abnormal_12m_pre)} (of {abnormal_total} total recorded)")
    md.append("")

    # VO2max trend
    vo2_12m_pre = mean([r["vo2max"] for r in vo2_rows if exam_2025 - timedelta(days=365) <= r["date"] < exam_2025])
    vo2_24_13m = mean([r["vo2max"] for r in vo2_rows if exam_2025 - timedelta(days=730) <= r["date"] < exam_2025 - timedelta(days=365)])
    vo2_after_2025 = mean([r["vo2max"] for r in vo2_rows if r["date"] >= exam_2025])
    md.append("### 3.2 VO2max / Cardiorespiratory fitness")
    md.append("")
    md.append(f"- **VO2max 12 months before 2025-09 exam**: {fmt_num(vo2_12m_pre)} — data gap (watch not worn 2024-08 → 2025-02)")
    md.append(f"- **VO2max 13-24 months before**: {fmt_num(vo2_24_13m)}")
    md.append(f"- **VO2max since 2025-09**: {fmt_num(vo2_after_2025)}")
    if vo2_rows:
        peak = max(r['vo2max'] for r in vo2_rows)
        peak_date = next(r['date'] for r in vo2_rows if r['vo2max'] == peak)
        low = min(r['vo2max'] for r in vo2_rows)
        low_date = next(r['date'] for r in vo2_rows if r['vo2max'] == low)
        md.append(f"- **All-time peak**: {peak:.1f} on {peak_date}")
        md.append(f"- **All-time low**: {low:.1f} on {low_date}")
        md.append(f"- **Net change from peak**: {low - peak:.1f} ml/kg/min ({(low - peak)/peak*100:+.1f}%)")
    md.append("")

    # Period comparison: between 2025-09 and 2026-03 PE exams — did Garmin show activity increase?
    md.append("### 3.3 Period 2025-09 → 2026-03 (between the two PE exams)")
    md.append("")
    md.append("_2026-03 PE improvements: LDL 177→154, TC 234→191, body fat 24.9→21.5%, HbA1c 6.0→5.9%_")
    md.append("")
    between = [r for r in uds_rows if exam_2025 <= r["date"] <= exam_2026]
    before = [r for r in uds_rows if exam_2025 - timedelta(days=190) <= r["date"] < exam_2025]
    def slab(ns, key, valid=lambda v: v is not None):
        xs = [r[key] for r in ns if valid(r[key])]
        return mean(xs)
    md.append("| Metric | 6 mo before 2025-09 exam | Between exams (2025-09→2026-03) |")
    md.append("|---|---|---|")
    md.append(f"| Daily steps | {fmt_num(slab(before, 'steps'), 0)} | {fmt_num(slab(between, 'steps'), 0)} |")
    md.append(f"| RHR | {fmt_num(slab(before, 'rhr', lambda v: v and 35<=v<=100))} | {fmt_num(slab(between, 'rhr', lambda v: v and 35<=v<=100))} |")
    md.append(f"| Stress | {fmt_num(slab(before, 'all_day_stress', lambda v: v and 0<v<100))} | {fmt_num(slab(between, 'all_day_stress', lambda v: v and 0<v<100))} |")
    md.append(f"| Body Battery | {fmt_num(slab(before, 'body_battery', lambda v: v and 0<v<100))} | {fmt_num(slab(between, 'body_battery', lambda v: v and 0<v<100))} |")
    md.append(f"| Moderate IMs/day | {fmt_num(slab(before, 'moderate_min'))} | {fmt_num(slab(between, 'moderate_min'))} |")
    md.append(f"| Vigorous IMs/day | {fmt_num(slab(before, 'vigorous_min'))} | {fmt_num(slab(between, 'vigorous_min'))} |")
    md.append("")

    # Activity
    md.append("### 3.4 Activity volume (for HDL, BP, BG control)")
    md.append("")
    r_latest = yearly[-1] if yearly else None
    if r_latest:
        md.append(
            f"- **2026 YTD weekly intensity minutes**: {fmt_num(r_latest['weekly_intensity'], 0)} (WHO target: 150 moderate or 75 vigorous)"
        )
    # Find best year
    best_year = max(yearly, key=lambda r: r["weekly_intensity"] or 0, default=None)
    if best_year:
        md.append(f"- **Best-activity year**: {best_year['year']} with {fmt_num(best_year['weekly_intensity'], 0)} weekly IMs, VO2max {fmt_num(best_year['avg_vo2max'])}")
    worst_year = min(yearly, key=lambda r: r["weekly_intensity"] or float("inf"), default=None)
    if worst_year:
        md.append(f"- **Lowest-activity year**: {worst_year['year']} with {fmt_num(worst_year['weekly_intensity'], 0)} weekly IMs")
    md.append("")

    # Health Status recent (LHA)
    if hs_rows:
        md.append("## 4. Recent Health Status (LHA baseline comparison, 2025-09 onward)")
        md.append("")
        out_counts = defaultdict(lambda: defaultdict(int))
        for r in hs_rows:
            for k in ["hrv_status", "hr_status", "spo2_status"]:
                v = r.get(k)
                if v:
                    out_counts[k][v] += 1
        md.append("| Metric | Status distribution |")
        md.append("|---|---|")
        for metric, label in [("hrv_status", "HRV"), ("hr_status", "HR"), ("spo2_status", "SpO2")]:
            dist = out_counts[metric]
            total = sum(dist.values())
            parts = [f"{k}: {v} ({v/total*100:.0f}%)" for k, v in sorted(dist.items(), key=lambda x: -x[1])]
            md.append(f"| {label} | {' · '.join(parts)} |")
        md.append("")
        avg_hrv = mean([r["hrv"] for r in hs_rows])
        avg_hr = mean([r["hr"] for r in hs_rows])
        avg_spo2 = mean([r["spo2"] for r in hs_rows])
        avg_resp = mean([r["respiration"] for r in hs_rows])
        md.append(f"- Avg HRV: {fmt_num(avg_hrv)} ms · Avg HR: {fmt_num(avg_hr)} bpm · Avg SpO2: {fmt_num(avg_spo2)}% · Avg Respiration: {fmt_num(avg_resp)} bpm")
        md.append(f"- _(Stress / Body Battery not in LHA metrics — see UDS yearly table above for those.)_")
        md.append("")

    # Charts
    md.append("## 5. Charts")
    md.append("")
    for title, path in chart_paths:
        if path is None:
            continue
        rel = os.path.relpath(path, REPORT_DIR)
        md.append(f"### {title}")
        md.append("")
        md.append(f"![{title}]({rel})")
        md.append("")

    # Data-quality notes
    md.append("## 6. Data Quality Notes")
    md.append("")
    md.append("- **UDS coverage gaps** reflect periods when the watch was not worn or not synced.")
    md.append("- **Weight** is stored in grams in Garmin's export; values outside 40–120 kg filtered as entry errors.")
    md.append("- **VO2max** is device-algorithm-derived; newer devices (Fenix/Forerunner) tend to read higher than older models — treat large jumps across device changes with caution.")
    md.append("- **`nutritionLogs.json`** only contains MyFitnessPal **calorie goal** (not actual intake), so nutrition trends cannot be derived from Garmin.")
    md.append("- **`AbnormalHrEvents`** threshold is user-configured (usually ~100 bpm while inactive); counts are sensitive to this setting.")
    md.append("- **`healthStatusData` (LHA)** only populated from 2025-09 onward (feature launched then); baseline comparisons are recent-only.")
    md.append("")

    out = os.path.join(REPORT_DIR, "garmin-full-analysis.md")
    with open(out, "w") as f:
        f.write("\n".join(md))
    return out


def main():
    os.makedirs(CHART_DIR, exist_ok=True)
    print("Loading data sources...")
    print("  UDS..."); uds = load_uds()
    print(f"    {len(uds)} daily summaries")
    print("  VO2max..."); vo2 = load_vo2max()
    print(f"    {len(vo2)} daily VO2max records")
    print("  FitnessAge..."); fa = load_fitness_age()
    print(f"    {len(fa)} fitness-age samples")
    print("  BioMetrics..."); bio = load_biometrics()
    print(f"    {len(bio)} biometric entries")
    print("  Abnormal HR..."); abn = load_abnormal_hr()
    print(f"    {len(abn)} events")
    print("  Activities..."); acts = load_activities()
    print(f"    {len(acts)} activities")
    print("  Health Status..."); hs = load_health_status()
    print(f"    {len(hs)} daily LHA records")
    print("  Sleep..."); nights = load_nights()
    print(f"    {len(nights)} nights")

    yearly = compute_yearly_summary(uds, vo2, fa, bio, abn, acts)

    print("\nGenerating charts...")
    charts = []
    p = os.path.join(CHART_DIR, "01_vo2max.png"); chart_vo2max_trend(vo2, p); charts.append(("VO2max 8-Year Trend", p))
    p = os.path.join(CHART_DIR, "02_fitness_age.png"); chart_fitness_age_gap(fa, p); charts.append(("Fitness Age Gap", p))
    p = os.path.join(CHART_DIR, "03_rhr.png"); chart_rhr_trend(uds, p); charts.append(("Resting Heart Rate", p))
    p = os.path.join(CHART_DIR, "04_weight.png"); chart_weight_trend(bio, p); charts.append(("Weight Trend", p))
    p = os.path.join(CHART_DIR, "05_steps_intensity.png"); chart_steps_activity(uds, p); charts.append(("Steps & Intensity Minutes", p))
    p = os.path.join(CHART_DIR, "06_stress_bb.png"); chart_stress_body_battery(uds, p); charts.append(("Stress & Body Battery", p))
    if abn:
        p = os.path.join(CHART_DIR, "07_abnormal_hr.png"); chart_abnormal_hr(abn, p); charts.append(("Abnormal HR Events", p))
    p = os.path.join(CHART_DIR, "08_activities.png"); chart_activities_yearly(acts, p); charts.append(("Activities by Year/Type", p))
    for title, path in charts:
        print(f"  {title} → {path}")

    report = write_report(uds, vo2, fa, bio, abn, acts, hs, nights, yearly, charts)
    print(f"\nReport: {report}")


if __name__ == "__main__":
    main()
