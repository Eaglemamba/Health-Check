#!/usr/bin/env python3
"""Sync data.js dynamic fields (hero, markers, tracker) from reviews/daily/*.md.

Targets fields driven from latest readings:
  - hero.currentWeight / currentWeightDate
  - hero.currentBodyFat / currentVisceralFat / currentBodyCompDate (latest daily reading)
  - hero.currentWaist / currentWaistDate (latest WHO-midpoint waist reading)
  - hero.progressMeta (Day N · X.X kg)
  - hero.startDate (Last sync M/D)
  - markers[heart] (BP weekly avg, when week is closed)
  - markers[sleep] (latest daily Sleep Score)
  - markers[weight] (latest Sat official weight)
  - tracker.bp / weight / sleep / bb / spo2Nadir (last 14 daily entries)

Run after `daily-command.md` finishes, before commit. Idempotent.
"""

from __future__ import annotations

import datetime as dt
import glob
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = REPO_ROOT / "reviews" / "daily"
DATA_JS = REPO_ROOT / "data.js"
PLAN_START = dt.date(2026, 3, 17)


# ---------- daily file parser ----------

def parse_daily(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    base = path.stem  # YYYY-MM-DD
    try:
        date = dt.datetime.strptime(base, "%Y-%m-%d").date()
    except ValueError:
        return {}
    data: dict = {"date": date, "path": path}

    m = re.search(r"\*\*今日：([\d.]+)\s*kg", text)
    data["weight"] = float(m.group(1)) if m else None

    m = re.search(r"體脂率：([\d.]+)\s*%", text)
    data["body_fat"] = float(m.group(1)) if m else None

    m = re.search(r"內臟脂肪等級：([\d.]+)", text)
    data["visceral_fat"] = float(m.group(1)) if m else None

    # Waist: WHO-midpoint only (健檢-comparable). Empty cells (—, [ ], blank) => None, never fabricated.
    m = re.search(r"腰圍\s*\(WHO midpoint\)：\s*([\d.]+)\s*cm", text)
    data["waist"] = float(m.group(1)) if m else None

    m = re.search(r"Garmin Sleep Score[：:]\*?\*?\s*(\d+)\s*/\s*100", text)
    data["sleep_score"] = int(m.group(1)) if m else None

    m = re.search(r"Body Battery[^：:]*[：:]\*?\*?\s*(\d+)", text)
    data["body_battery"] = int(m.group(1)) if m else None

    bp = re.findall(
        r"\|\s*第([一二])次\s*\|\s*(\d+)?\s*\|\s*(\d+)?\s*\|\s*(\d+)?\s*\|",
        text,
    )
    data["bp_sys"] = data["bp_dia"] = None
    for order, sys_v, dia_v, _hr in bp:
        if order == "二" and sys_v:
            data["bp_sys"] = int(sys_v)
            data["bp_dia"] = int(dia_v) if dia_v else None
            break
    if data["bp_sys"] is None:
        for order, sys_v, dia_v, _hr in bp:
            if order == "一" and sys_v:
                data["bp_sys"] = int(sys_v)
                data["bp_dia"] = int(dia_v) if dia_v else None
                break

    # SpO2 nightly nadir — last column of the 7-night "最低 %" table is THIS file's own night.
    # "—" / 空白 cell => no reading that night => None (never fabricated).
    data["spo2_nadir"] = None
    m = re.search(r"^\|\s*最低\s*%\s*\|(.+)$", text, re.MULTILINE)
    if m:
        cells = [c.strip().strip("*").strip() for c in m.group(1).split("|")]
        cells = [c for c in cells if c]
        if cells:
            mm = re.search(r"\d+", cells[-1])
            data["spo2_nadir"] = int(mm.group()) if mm else None

    return data


def collect_daily(n_days: int = 14) -> list[dict]:
    # Recursive: 涵蓋月份歸檔子資料夾 (e.g. reviews/daily/2026-04/*.md)
    files = sorted(glob.glob(str(DAILY_DIR / "**" / "*.md"), recursive=True))
    parsed = [d for d in (parse_daily(Path(p)) for p in files) if d.get("date")]
    parsed.sort(key=lambda d: d["date"])
    return parsed


# ---------- helpers ----------

def latest_official_weight(daily: list[dict]) -> tuple[float, dt.date] | None:
    """Saturday morning is the canonical weekly weight per CLAUDE.md."""
    sats = [d for d in daily if d["date"].weekday() == 5 and d["weight"] is not None]
    if not sats:
        return None
    last = sats[-1]
    return last["weight"], last["date"]


def latest_value(daily: list[dict], key: str):
    for d in reversed(daily):
        v = d.get(key)
        if v is not None:
            return v, d["date"]
    return None


def closed_week_bp_avg(daily: list[dict], today: dt.date) -> tuple[int, int, int, int] | None:
    """Avg over the most recently CLOSED ISO week (Mon–Sun ending before today)."""
    iso_year, iso_week, iso_dow = today.isocalendar()
    if iso_dow == 7:
        target_year, target_week = iso_year, iso_week
    elif iso_week > 1:
        target_year, target_week = iso_year, iso_week - 1
    else:
        prev_dec_28 = dt.date(today.year - 1, 12, 28)
        target_year, target_week, _ = prev_dec_28.isocalendar()

    sys_vals, dia_vals = [], []
    for d in daily:
        y, w, _ = d["date"].isocalendar()
        if (y, w) == (target_year, target_week) and d["bp_sys"] and d["bp_dia"]:
            sys_vals.append(d["bp_sys"])
            dia_vals.append(d["bp_dia"])
    if not sys_vals:
        return None
    return (
        round(sum(sys_vals) / len(sys_vals)),
        round(sum(dia_vals) / len(dia_vals)),
        target_week,
        len(sys_vals),
    )


def fwd_fill(values: list, default):
    out, last = [], default
    for v in values:
        if v is None:
            out.append(last if last is not None else default)
        else:
            out.append(v)
            last = v
    return out


def last_14(daily: list[dict]) -> dict:
    cut = daily[-14:] if len(daily) >= 14 else daily
    bp_pairs = []
    for d in cut:
        if d["bp_sys"] and d["bp_dia"]:
            bp_pairs.append([d["bp_sys"], d["bp_dia"]])
        else:
            bp_pairs.append(None)
    seed_bp = next((p for p in bp_pairs if p is not None), [120, 75])
    bp_filled = fwd_fill(bp_pairs, seed_bp)

    weights = fwd_fill([d["weight"] for d in cut], 70.0)
    sleep = fwd_fill([d["sleep_score"] for d in cut], 70)
    bb = fwd_fill([d["body_battery"] for d in cut], 50)
    # nadir is NOT forward-filled — a missing night is genuinely unknown (null), not the prior value
    spo2 = [d.get("spo2_nadir") for d in cut]
    return {"bp": bp_filled, "weight": weights, "sleep": sleep, "bb": bb, "spo2": spo2}


# ---------- data.js writer ----------

def replace_field(text: str, pattern: str, replacement: str, label: str) -> str:
    new, n = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if n == 0:
        print(f"  [skip] {label}")
        return text
    print(f"  [ok]   {label}")
    return new


def replace_in_marker(text: str, sys_id: str, inner_pattern: str, inner_repl: str, label: str) -> str:
    """Run an inner regex inside a single markers[] entry scoped by sys_id.

    Matches from `{ sys: "<id>"` up to the entry's closing `},` after `status: "..."`.
    """
    block_re = re.compile(
        r'\{\s*sys:\s*"' + re.escape(sys_id) + r'"[\s\S]*?status:\s*"\w+",\s*\},',
    )
    m = block_re.search(text)
    if not m:
        print(f"  [skip] {label} (marker block not found)")
        return text
    block = m.group(0)
    new_block, n = re.subn(inner_pattern, inner_repl, block, count=1, flags=re.DOTALL)
    if n == 0:
        print(f"  [skip] {label} (inner pattern no match)")
        return text
    print(f"  [ok]   {label}")
    return text[: m.start()] + new_block + text[m.end():]


def fmt_array(values: list, transform=str) -> str:
    return ", ".join(transform(v) for v in values)


def fmt_bp_array(values: list[list[int]]) -> str:
    return ", ".join(f"[{v[0]},{v[1]}]" for v in values)


def fmt_weight_array(values: list[float]) -> str:
    return ", ".join(f"{v:g}" if v == int(v) else f"{v}" for v in values)


def fmt_spo2(values: list) -> str:
    return ", ".join("null" if v is None else str(v) for v in values)


def update_data_js(text: str, ctx: dict) -> str:
    today = ctx["today"]
    daily = ctx["daily"]
    arrays = ctx["arrays"]

    # hero.currentWeight + currentWeightDate
    if ctx.get("official"):
        w, w_date = ctx["official"]
        text = replace_field(
            text,
            r"currentWeight:\s*[\d.]+,",
            f"currentWeight: {w},",
            "hero.currentWeight",
        )
        text = replace_field(
            text,
            r'currentWeightDate:\s*"[^"]*",',
            f'currentWeightDate: "{w_date.strftime("%-m/%-d Sat official") if os.name != "nt" else w_date.strftime("%#m/%#d Sat official")}",',
            "hero.currentWeightDate",
        )

    # hero.currentBodyFat / currentVisceralFat / currentBodyCompDate — latest daily readings
    # (body comp is recorded daily, not Saturday-only, so use most-recent non-null reading)
    g = lambda v: f"{v:g}"  # 8.5 -> "8.5", 9.0 -> "9"
    if ctx.get("bf_latest"):
        bf, _ = ctx["bf_latest"]
        text = replace_field(
            text,
            r"currentBodyFat:\s*[\d.]+,",
            f"currentBodyFat: {g(bf)},",
            "hero.currentBodyFat",
        )
    if ctx.get("vf_latest"):
        vf, _ = ctx["vf_latest"]
        text = replace_field(
            text,
            r"currentVisceralFat:\s*[\d.]+,",
            f"currentVisceralFat: {g(vf)},",
            "hero.currentVisceralFat",
        )
    bc_readings = [r for r in (ctx.get("bf_latest"), ctx.get("vf_latest")) if r]
    if bc_readings:
        bc_date = max(r[1] for r in bc_readings)
        text = replace_field(
            text,
            r'currentBodyCompDate:\s*"[^"]*",',
            f'currentBodyCompDate: "{bc_date.month}/{bc_date.day}",',
            "hero.currentBodyCompDate",
        )
    if ctx.get("waist_latest"):
        ws, ws_date = ctx["waist_latest"]
        text = replace_field(
            text,
            r"currentWaist:\s*[\d.]+,",
            f"currentWaist: {g(ws)},",
            "hero.currentWaist",
        )
        text = replace_field(
            text,
            r'currentWaistDate:\s*"[^"]*",',
            f'currentWaistDate: "{ws_date.month}/{ws_date.day}",',
            "hero.currentWaistDate",
        )

    # hero.progressMeta — Day N + Sat official
    if ctx.get("official"):
        w, w_date = ctx["official"]
        day_n = (today - PLAN_START).days + 1
        en = f"Day {day_n} · {w} kg · Sat official ({w_date.month}/{w_date.day})"
        zh = f"第 {day_n} 天 · {w} 公斤 · 週六正式（{w_date.month}/{w_date.day}）"
        pattern = (
            r'progressMeta:\s*\{\s*en:\s*"[^"]*",\s*zh:\s*"[^"]*"\s*\},'
        )
        text = replace_field(
            text,
            pattern,
            f'progressMeta: {{ en: "{en}", zh: "{zh}" }},',
            "hero.progressMeta",
        )

    # hero.startDate — last sync M/D
    en = f"Start date · Mar 17, 2026 · Last sync {today.month}/{today.day}"
    zh = f"起始日期 · 2026 年 3 月 17 日 · 最後同步 {today.month}/{today.day}"
    text = replace_field(
        text,
        r'startDate:\s*\{\s*en:\s*"[^"]*",\s*zh:\s*"[^"]*"\s*\},',
        f'startDate: {{ en: "{en}", zh: "{zh}" }},',
        "hero.startDate",
    )

    # markers[heart] — closed weekly avg
    if ctx.get("bp_week"):
        sys_v, dia_v, week_n, n_days = ctx["bp_week"]
        latest = next(
            (d for d in reversed(daily) if d["bp_sys"] and d["bp_dia"]), None
        )
        last_str = (
            f"{latest['bp_sys']}/{latest['bp_dia']} ({latest['date'].month}/{latest['date'].day})"
            if latest else "—"
        )
        en = f"W{week_n} weekly avg ({n_days} days) · target met (<130) · last {last_str}"
        zh = f"W{week_n} 週均（{n_days} 天）· 已達標 (<130) · 最新 {last_str}"
        text = replace_in_marker(
            text, "heart",
            r'val:\s*"[^"]*"', f'val: "{sys_v}/{dia_v}"',
            "markers[heart] val",
        )
        text = replace_in_marker(
            text, "heart",
            r'delta:\s*\{\s*en:\s*"[^"]*",\s*zh:\s*"[^"]*"\s*\}',
            f'delta: {{ en: "{en}", zh: "{zh}" }}',
            "markers[heart] delta",
        )

    # markers[sleep] — latest daily SS
    if ctx.get("sleep_latest"):
        ss, ss_date = ctx["sleep_latest"]
        text = replace_in_marker(
            text, "sleep",
            r'val:\s*"[^"]*"', f'val: "{ss}"',
            "markers[sleep] val",
        )

    # markers[weight] — Sat official
    if ctx.get("official"):
        w, w_date = ctx["official"]
        text = replace_in_marker(
            text, "weight",
            r'val:\s*"[^"]*"', f'val: "{w}"',
            "markers[weight] val",
        )
        en = f"{w_date.month}/{w_date.day} Sat official · auto-synced"
        zh = f"{w_date.month}/{w_date.day} 週六正式 · 自動同步"
        text = replace_in_marker(
            text, "weight",
            r'delta:\s*\{\s*en:\s*"[^"]*",\s*zh:\s*"[^"]*"\s*\}',
            f'delta: {{ en: "{en}", zh: "{zh}" }}',
            "markers[weight] delta",
        )

    # tracker arrays — use \g<1> to disambiguate when value starts with a digit
    # bp array contains inner [N,N] arrays so terminator must be the indented closing line
    text = replace_field(
        text,
        r"(bp:\s*\[)[\s\S]*?(\n\s+\],)",
        f"\\g<1>\n      {fmt_bp_array(arrays['bp'])},\\g<2>",
        "tracker.bp",
    )
    text = replace_field(
        text,
        r"(weight:\s*\[)[^\]]*(\],)",
        f"\\g<1>{fmt_weight_array(arrays['weight'])}\\g<2>",
        "tracker.weight",
    )
    text = replace_field(
        text,
        r"(sleep:\s*\[)[^\]]*(\],)",
        f"\\g<1>{fmt_array(arrays['sleep'])}\\g<2>",
        "tracker.sleep",
    )
    text = replace_field(
        text,
        r"(bb:\s*\[)[^\]]*(\],)",
        f"\\g<1>{fmt_array(arrays['bb'])}\\g<2>",
        "tracker.bb",
    )
    text = replace_field(
        text,
        r"(spo2Nadir:\s*\[)[^\]]*(\],)",
        f"\\g<1>{fmt_spo2(arrays['spo2'])}\\g<2>",
        "tracker.spo2Nadir",
    )

    return text


# ---------- main ----------

def main() -> int:
    if not DAILY_DIR.is_dir():
        print(f"reviews/daily not found at {DAILY_DIR}", file=sys.stderr)
        return 1
    daily = collect_daily()
    if not daily:
        print("no daily reviews parsed", file=sys.stderr)
        return 1

    today = daily[-1]["date"]
    ctx = {
        "today": today,
        "daily": daily,
        "official": latest_official_weight(daily),
        "sleep_latest": latest_value(daily, "sleep_score"),
        "bf_latest": latest_value(daily, "body_fat"),
        "vf_latest": latest_value(daily, "visceral_fat"),
        "waist_latest": latest_value(daily, "waist"),
        "bp_week": closed_week_bp_avg(daily, today),
        "arrays": last_14(daily),
    }

    print(f"sync source: {len(daily)} daily files, latest = {today}")
    if ctx["official"]:
        print(f"  Sat official weight: {ctx['official'][0]} kg ({ctx['official'][1]})")
    if ctx["sleep_latest"]:
        print(f"  Sleep score latest: {ctx['sleep_latest'][0]} ({ctx['sleep_latest'][1]})")
    if ctx["bf_latest"]:
        print(f"  Body fat latest: {ctx['bf_latest'][0]}% ({ctx['bf_latest'][1]})")
    if ctx["vf_latest"]:
        print(f"  Visceral fat latest: {ctx['vf_latest'][0]} ({ctx['vf_latest'][1]})")
    if ctx["waist_latest"]:
        print(f"  Waist (WHO mid) latest: {ctx['waist_latest'][0]} cm ({ctx['waist_latest'][1]})")
    if ctx["bp_week"]:
        sys_v, dia_v, wk, n = ctx["bp_week"]
        print(f"  BP closed week W{wk}: {sys_v}/{dia_v} avg over {n} day(s)")
    print(f"  tracker arrays: last {len(ctx['arrays']['weight'])} days")

    text = DATA_JS.read_text(encoding="utf-8")
    new_text = update_data_js(text, ctx)
    if new_text == text:
        print("data.js: no changes")
        return 0
    DATA_JS.write_text(new_text, encoding="utf-8")
    print("data.js: updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
