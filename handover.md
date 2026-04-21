# Session Handover — 2026-04-21

**Branch:** `claude/add-roselle-tea-rct-BMzxw` (8 commits ahead of main, all pushed)
**Status:** Supplement guide fully updated; `index.html` partially synced (EN done, ZH pending)

*Replaces prior handover.md (2026-04-18 causal-map work, completed in commit 0265b46 and no longer current).*

---

## What this session accomplished

Starting from a single request ("add 洛神花茶 with RCT support to the supplement guide"), the session expanded into a comprehensive overhaul of the 2026-03-25 supplement guide, partial sync of `index.html`, and a behavioral milestone capture in the daily log.

### Commit timeline (oldest → newest)

| # | Commit | Scope |
|---|--------|-------|
| 1 | `aced978` | Added 洛神花茶 RCT discussion (Serban 2015 meta SBP −7.58, McKay 2010, Mozaffari-Khosravi 2009) |
| 2 | `eb44ca3` | Realigned matcha to single lunch latte; cancelled NOW EGCG capsule; added L-Citrulline 2g |
| 3 | `5667f87` | Added Psyllium husk 5g × 2/day as LDL primary replacement |
| 4 | `1dbed15` | Added pumpkin seeds 30g afternoon snack + daily-load accounting (§8) addressing 72% chocolate question |
| 5 | `81c3440` | Captured identity milestone in daily log (no longer wants 珍珠) |
| 6 | `b0f8ecb` | Added resistance training protocol as §9 ("missing piece" for HDL 39→45 and 65 kg body composition) |
| 7 | `a0037fc` | index.html Phase 1 — Daily Routine table synced (EN+ZH) with gram-explicit dosing |
| 8 | `a0dff12` | index.html Phase 2 (EN only) — Matcha/Hibiscus prose + supplements table + cost table |

---

## Current state of the supplement guide

**File:** `articles/2026-03-25-supplement-guide.md` (mirrored to `reviews/annual/2026-03-25-supplement-guide.md`)

10 sections now:

1. **茶飲選擇** — matcha ✅ + 枸杞 ✅ + **洛神花茶 ✅ 加選 🆕** + corn silk / burdock ☐
2. **補品組合** — 5 core (fish oil / tart cherry / D3K2 / Mg / probiotics) + **L-Citrulline 2g 🆕** + **Psyllium 5g×2 🆕** + **南瓜籽仁 30g (food) 🆕**
3. **效果全比較表** (PubMed RCT) + Hibiscus RCT summary + **L-Citrulline RCT summary 🆕** + **Psyllium RCT summary 🆕**
4. **各指標策略分析** — LDL primary lever reassigned to Psyllium; BP gets hibiscus + citrulline; HDL strategy rewritten around resistance training
5. **抹茶執行方案** — rewritten for single-lunch-latte; EGCG 48–95 mg/day (sub-RCT); ALT/AST safety rationale for capsule cancellation
6. **劑量與時機表** — all new items integrated
7. **建議每日時程** — breakfast no matcha + citrulline; hibiscus ×2 tea windows; psyllium ×2 (11:30 + 16:30); pumpkin seeds 15:00–16:00; dinner fish oil ×4 only
8. **下午零食盤點與 72% 巧克力決策 🆕** — full-day macro accounting + 3 reasons to NOT stack 72% chocolate
9. **阻力訓練（缺失拼圖）🆕** — detrained-resume protocol (week 1–2 → 9+); 6 compound movements; integration with NO stack; safety boundaries
10. **預期效果與時程** — LDL 154 → **135–145** (with psyllium); HDL 39 → **42–48** (conditional on RT ≥12 weeks); body comp 68.6 → **65 kg @ 16–18%** (requires RT for lean mass preservation)

---

## Current state of `index.html` sync

### Synced ✅
- Daily Routine & Hydration table (EN + ZH, lines ~1025–1115) — gram-explicit for every item
- Daily supplement dose summary list (EN + ZH)
- Hydration total updated 2.3–2.5 L → **2.5–2.8 L**
- All-Day Beverage Strategy table (**EN only**, ~387–402)
- Matcha card (**EN only**, ~404) — EGCG math corrected
- Breakfast Yogurt Recipe table (**EN only**, ~408–424)
- T4 Supplements master table (**EN only**, ~858–872)
- Hibiscus prose section (**EN only**, ~904–940) — split from goji, Serban/McKay/Mozaffari citations added
- Goji standalone section (**EN only**) — explains move to breakfast blend
- L-Citrulline dosing rationale (**EN only**) — 2g single-dose justified
- Creatine caveats (**EN only**) — water retention + eGFR caveats
- Cost table (**EN only**, ~975–1005) — priorities reordered

### Out of sync ❌ — PENDING
- **ZH T4 Supplements section (lines ~1009–1063)** — severely outdated, only 3 items in table (Omega-3, tart cherry, goji tea); missing D3K2, Mg, citrulline, psyllium, hibiscus, pumpkin seeds. Full rewrite needed to mirror current EN version.
- **Current Supplements 總覽** (line 111 EN, line 146 ZH) — still says "Expanding to: L-Citrulline, Creatine, D3K2, Chelated Magnesium, NAC, Whey Protein"; creatine/NAC not active.
- **ZH T2 matcha/beverage strategy** — searched, does not appear to exist as a mirror of EN T2 (ZH T2 is streamlined to DASH/macros). Likely no update needed; verify.

---

## Pending work (priority order)

### Phase 2 remainder — ZH T4 rewrite
Rewrite `index.html` lines ~1009–1063 to mirror the current EN T4 (lines ~853–1005). Specifically:
- Supplements master table: add D3K2, Mg, L-Citrulline 2g, Psyllium 5g×2, Hibiscus tea 2g×2, probiotics, pumpkin seeds, whey; mark creatine + NAC as 未啟用（灰階）
- Add ZH detailed prose for Hibiscus tea (copy RCT citations from §3 of the MD guide)
- Add ZH cost table mirroring EN priority list

### Phase 3 — New standalone `index.html` subsections (both EN + ZH)
- **Psyllium husk** detailed section (Jovanovski 2018 meta, dosing, safety)
- **Pumpkin seeds** detailed section (Zn/Mg/phytosterol/tryptophan)
- **L-Citrulline** — EN done (needs verify); add ZH mirror
- **Resistance training summary** — brief section linking back to guide §9 (full protocol stays in the MD guide)

### Phase 4 — Overview sync
- `index.html` line 111 (EN) and line 146 (ZH): rewrite "Current Supplements" one-liner to reflect active stack (fish oil, tart cherry, D3K2, Mg glycinate, probiotics-in-yogurt, L-citrulline 2g, psyllium 5g×2, hibiscus 2g×2, pumpkin seeds 30g; matcha now lunch-latte only)
- Remove "Expanding to:" language for items that are now active
- Explicitly note creatine + NAC as NOT in active stack

---

## Key decisions made this session

- **Matcha dose drastically reduced** (270–320 mg EGCG → ~48–95 mg) because user stopped morning matcha + evening capsule on their own. Guide accepts this; LDL responsibility transferred to psyllium. User's rationale stands: feels great, trend is good.
- **NOW EGCG capsule permanently discontinued** due to AST 27→38 + EFSA >338 mg single-dose hepatotoxicity signal.
- **72% dark chocolate: NOT recommended to stack** — full daily-load analysis showed +4 g sugar, +4 g sat fat, +70 mg theobromine, near-zero marginal flavanol benefit (morning cacao already saturates). If cravings: 85% 10 g > 72% on every dimension.
- **Creatine: not added yet**. User curious; recommended to defer until resistance training resumes ≥2×/week. Two caveats documented:
  - Water retention pollutes 65 kg weight trend
  - Serum creatinine rise triggers eGFR misread (critical for pending nephrology referral given UA 8.9)
- **Second bedtime L-Citrulline: No**. Chronic NO adaptation, not acute dosing window. If escalating, single 3 g morning > split 2+2 g.
- **Resistance training protocol created** because user revealed they used to train 2+/week but ate poorly; now eats well but zero RT — this is the one combination they've never experienced. Protocol is detrained-resume conservative: week 1–2 × 1/week × 15 min, ramping to 2–3×/week × 30 min by week 9.

---

## Observable health state snapshot (2026-04-21)

| Metric | Value | Note |
|--------|-------|------|
| Weight | 68.6 kg | Target 65 kg, requires RT for lean mass preservation |
| Body fat | 19.8% | From 24.9% (−3.4% over 6 months) |
| Visceral fat | 9.5 | Target <9 |
| Home BP AM | 121/75 (today), 112/70 (yesterday) | Vs. clinic 153/88 — setting-induced |
| LDL | 154 | From 177; target <130 |
| HDL | 39 | From 46 — needs RT (biochemical fingerprint of missing muscle signal) |
| hsCRP | 1.42 mg/L | From 3.02 (−53%); likely personal lifetime low |
| HbA1c | 5.9% | Prediabetes platform easing |
| Uric acid | 8.9 | Worsening; nephrology referral pending |
| Sleep SpO2 min | **84% ×2 consecutive nights** | 🔴 **OSA red flag** — pulse oximeter or sleep clinic consult recommended |
| Body Battery | 30 today, 62 yesterday | Low autonomic recovery despite decent Sleep Score 74 |

---

## Flagged items user has not yet actioned (each raised ≥3 times)

1. **Home pulse oximeter night recording** or ENT/sleep clinic consult for OSA. The SpO2 data is the one objective signal pointing somewhere concerning and cannot be fixed by supplements.
2. **Nephrology referral** for febuxostat/allopurinol evaluation — constitutional hyperuricemia (UA 7.8 at age 26, now 8.9) won't respond to supplements/tea alone.

---

## Behavioral / psychological notes

User expressed in this session:
- "feel so great" on current yogurt + tea + supplement + bed-supplement routine
- "I never ate like this before…with controlled food and beverage"
- "I even don't like to eat bubble when order beverage" — captured in daily log as identity transition milestone
- Looking forward to "65 kg 完全健康" state, potentially "healthier than when young"
- Acknowledged: used to train 2+/week but ate poorly → current opposite is the missing piece

Captured in `reviews/daily/2026-04-21.md` §心理/行為里程碑 with objective data backing.

---

## Next session suggested opening

If resuming: ask user which is priority:
- (a) Finish ZH T4 rewrite + Phase 3/4 `index.html` sync
- (b) Something has come up (new symptoms, SpO2 test results, RT started, etc.)

**Do NOT start more supplement additions without asking.** User's stack is at a good saturation point and the guide now explicitly recommends proving the current system for 4 weeks before further changes. 7 月 (July 2026) blood test will be the next decision point for statin / dose escalation.

---

*File: `handover.md` (root)*
*Branch: `claude/add-roselle-tea-rct-BMzxw`*
*Written: 2026-04-21*
