# Handover: Expand Health Indicators — Health Analyzer App

**Branch:** `claude/expand-health-indicators-ThnjJ`
**Date:** 2026-04-15
**Status:** Design complete, implementation pending

---

## 1. Background & Goal

The current `index.html` is a **6-Month Health Reversal Plan** focused on 4 key markers: blood pressure (ISH), triglycerides, cholesterol, and uric acid. It includes detailed plans for sleep repair, diet, exercise (wall sits), and supplements.

However, the 2025 annual health report (`reviews/annual/2025.md`) contains **many more abnormal indicators** that are not addressed in the current plan. The user wants to **expand scope** by building a new **Health Analyzer App** (`analyzer.html`) that:

1. Accepts input for **all** PE (physical examination) test indicators
2. Auto-flags which values are abnormal (red/orange/yellow)
3. Generates **personalized, evidence-based plans** for each flagged indicator — similar in depth and quality to the plans already in `index.html`

---

## 2. What Exists Today

### `index.html` (721 lines)
- 6-month plan targeting weight loss (70 → 65 kg) and 4 marker normalization
- 9 tabs: Overview, Sleep Repair, Diet Plan, Exercise & Wall Sits, Supplements & Cost, Daily Routine, Timeline & Milestones, Safety & Medical, Health Dashboard
- Styled as a mobile-friendly single-page app with tab navigation
- CSS variables: `--bd:#1B3A5C; --bm:#2E6B9E; --bl:#E8F0F8; --gn:#2D7D46; --gl:#E8F5E9; --rd:#C62828; --rl:#FDECEA; --or:#E65100; --ol:#FFF3E0;` etc.

### `reviews/annual/2025.md` — Full Health Report
The 2025 report (exam date 2025-09-17) is the **source of truth** for all indicators. Key abnormalities:

| Indicator | Value | Reference | Priority |
|-----------|-------|-----------|----------|
| LDL Cholesterol | 177 mg/dL | <130 | High |
| Total Cholesterol | 234 mg/dL | <200 | High |
| Body Fat % | 24.9% | 17–23% | High |
| Weight / BMI | 69.9 kg / 24.2 | <69.16 / <24.0 | High |
| Myocardial Ischemia (ECG) | Persistent | — | High (cardiology follow-up) |
| Uric Acid | 8.6 mg/dL | 3.4–7.0 | Medium |
| HbA1c | 6.0% | <5.9% | Medium (pre-diabetes) |
| Fatty Liver (ultrasound) | New finding | None | Medium |
| T-Chol/HDL Ratio | 5.09 | <5 | Medium |
| hsCRP | 0.302 mg/L | ≤0.300 | Low |
| Vitamin D | 28.8 ng/mL | ≥30 | Low |

Improvements noted: PWV normalized, hsCRP down 46%, BP improved, pulse improved, LV strain resolved.

### Other Key Files
- `template.html` — older/alternative version of the plan (844 lines)
- `reviews/daily/` — 30 daily records (2026-03-17 to 2026-04-15) tracking weight, BP, sleep score, body battery, body signals
- `reviews/weekly/` — weekly reviews (W12–W16)
- `reviews/monthly/2026-03.md` — March monthly review
- `scripts/generate_dashboard.py` — auto-generates health_dashboard.png from daily records
- `templates/pt-rules.md` — physical therapy auto-advice rules

---

## 3. What Needs to Be Built

### `analyzer.html` — Health Analyzer App

A single-page HTML app (matching `index.html` visual style) with these sections:

#### A. Input Form — All PE Test Indicators

Organized into collapsible sections:

1. **Physical Measurements**
   - Height (cm), Weight (kg), BMI (auto-calculated), Body Temperature (°C)
   - Blood Pressure — Systolic/Diastolic (mmHg), Pulse (bpm)
   - Body Fat % , Visceral Fat Level, Waist (cm), Hip (cm)

2. **Blood — CBC**
   - Hemoglobin, RBC, Hematocrit, MCV, MCH, MCHC
   - WBC, Neutrophils %, Eosinophils %, Basophils %, Monocytes %, Lymphocytes %
   - Platelets, RDW

3. **Blood — Liver Function**
   - Direct Bilirubin, Total Bilirubin, ALP, AST (SGOT), ALT (SGPT)

4. **Blood — Kidney Function**
   - BUN, Uric Acid, Creatinine, eGFR

5. **Blood — Glucose Metabolism**
   - Fasting Glucose, HbA1c

6. **Blood — Lipid Panel**
   - Total Cholesterol, Triglycerides, LDL, HDL, TC/HDL Ratio (auto-calculated)

7. **Serum & Inflammation**
   - Vitamin D (25-OH), TSH, hsCRP, HBsAg

8. **Tumor Markers**
   - PSA, CEA, AFP, CA-199

9. **Cardiovascular Tests**
   - ABI, PWV (cm/s)

10. **Urinalysis**
    - Specific Gravity, pH, Protein, Glucose, Ketones, Occult Blood, Urobilinogen

11. **Stool**
    - Fecal Occult Blood (ng/mL)

12. **Imaging & Special Tests** (qualitative dropdowns)
    - ECG: Normal / Abnormal (with sub-options: arrhythmia, LVH, ischemia, etc.)
    - Chest X-ray: Normal / Abnormal
    - Abdominal Ultrasound: Normal / Fatty Liver (mild/moderate/severe) / Other
    - Bone Density: Normal / Osteopenia / Osteoporosis

13. **Eye Exam**
    - Visual Acuity L/R, Intraocular Pressure L/R (mmHg)

#### B. Analysis Engine (JavaScript)

- Gender selector (male/female) for gender-specific reference ranges
- Auto-calculations: BMI from height+weight, TC/HDL ratio from TC+HDL
- Real-time color coding as values are entered (green/yellow/red border)
- "Load Sample Data" button pre-fills with 2025 report values for demo
- "Analyze" button triggers full analysis

#### C. Results Report

1. **Summary Dashboard** — count of red/orange/yellow flags, overall risk level
2. **Flagged Indicators** — priority-ranked list (High → Medium → Low), each showing:
   - Current value vs reference range
   - What it means (brief explanation)
   - Risk level badge
3. **Detailed Plans** — expandable card for each flagged indicator containing:
   - Explanation of the indicator and why it matters
   - Specific action items organized by: Diet, Exercise, Supplements, Medical, Lifestyle
   - Expected improvement timeline
   - Related indicators to watch
4. **Cross-Indicator Analysis** — pattern detection:
   - Metabolic Syndrome (≥3 of: waist, TG, HDL, BP, glucose)
   - Cardiovascular Risk Cluster (LDL + TC/HDL + hsCRP + BP)
   - Liver-Metabolic Axis (fatty liver + ALT + body fat)
   - Kidney-Uric Acid Axis (creatinine + eGFR + uric acid)
   - Pre-Diabetes Pathway (HbA1c + glucose + body fat + waist)
5. **Recommended Follow-Up Schedule** — when to retest, which specialists to see

#### D. Plan Depth by Indicator Tier

**Tier 1 — Very Detailed Plans (10+ action items each):**
- Body composition (BMI / Weight / Body Fat / Waist)
- Blood Pressure (ISH-aware)
- LDL / Total Cholesterol
- Triglycerides
- Uric Acid
- HbA1c / Fasting Glucose (pre-diabetes)
- Fatty Liver

**Tier 2 — Moderate Plans (5–8 action items):**
- HDL (low), hsCRP, Vitamin D, AST/ALT, eGFR/Creatinine, TSH

**Tier 3 — Brief Notes (2–4 action items):**
- CBC abnormalities, Bilirubin, BUN, Urinalysis, Tumor markers, Eye findings

---

## 4. Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Separate file vs new tab in index.html | Separate `analyzer.html` | index.html is the plan (reference); analyzer is a tool (interactive). Different purposes. |
| Visual style | Reuse index.html CSS variables and component classes | Visual consistency across the project |
| Language | English with Chinese medical terms in parentheses | Matches index.html style; user is bilingual |
| Data storage | None (client-side only, no backend) | Simplicity; user can bookmark/print results |
| Gender handling | Selector at top; adjusts reference ranges for gender-specific indicators | Male/female have different ranges for hemoglobin, body fat %, etc. |
| Navigation | Cross-links between index.html ↔ analyzer.html | Easy switching between plan and analyzer |

---

## 5. Evidence Sources for Plans

The plans should reference the same evidence base as index.html:

- **Wall sits / isometric exercise:** 2023 BJSM meta-analysis (270 RCTs), 2024 RCT (−12.9 mmHg systolic)
- **DASH diet:** Combined with Omega-3 → LDL −31.7, TG −45.3, SBP −14.7, UA −1.3
- **Omega-3 (rTG):** 2g/day therapeutic dose for TG and BP
- **Tart cherry:** 2025 RCT → UA −37.4%, CRP −23%
- **Oat beta-glucan:** 3g/day → LDL −5–10%
- **Weight loss:** ~1 mmHg BP reduction per kg lost; 5–10% body weight loss reverses fatty liver
- **Sleep repair:** Hypertension risk 3.5× with <6h sleep; cortisol/TG/VLDL pathway
- **HbA1c:** Lifestyle intervention (DPP study) can reduce diabetes progression by 58%
- **Vitamin D:** D3 2000–4000 IU/day to reach ≥30 ng/mL; pair with K2

---

## 6. Sample Data for Testing

Pre-fill "Load Sample Data" with 2025 report values:

```javascript
const sampleData = {
  gender: "male",
  height: 169.8, weight: 69.9,
  bp_systolic: 129, bp_diastolic: 74, pulse: 67,
  temperature: 36.4,
  body_fat: 24.9, waist: 85.5, hip: 94.5,
  hb: 14.2, rbc: 4.93, ht: 41.2, mcv: 83.5, mch: 28.9, mchc: 34.5,
  wbc: 8.00, neutrophils: 61.4, eosinophils: 3.5, basophils: 0.5, monocytes: 5.7, lymphocytes: 28.9,
  platelets: 278, rdw: 13.4,
  direct_bilirubin: 0.29, total_bilirubin: 0.70, alp: 74, ast: 27, alt: 25,
  bun: 16, uric_acid: 8.6, creatinine: 1.0, egfr: 89.8,
  glucose: 89, hba1c: 6.0,
  total_cholesterol: 234, triglycerides: 125, ldl: 177, hdl: 46,
  vitamin_d: 28.8, tsh: 2.32, hscrp: 0.302, hbsag: 0.34,
  psa: 0.94, cea: 2.23, afp: 3.0, ca199: 2.00,
  ecg: "ischemia", chest_xray: "normal",
  ultrasound: "fatty_liver_mild", bone_density: "normal",
  visual_acuity_l: 1.5, visual_acuity_r: 1.2,
  iop_l: 15.9, iop_r: 17.4,
  urine_sg: 1.015, urine_ph: 6.0,
  urine_protein: "negative", urine_glucose: "negative",
  urine_ketones: "negative", urine_blood: "negative", urine_urobilinogen: 0.2,
  stool_ob: 7.0
};
```

---

## 7. Implementation Steps

1. **Create `analyzer.html`** with the full form, CSS, and JS analysis engine
2. **Add cross-links** between `index.html` and `analyzer.html`
3. **Test** with sample data — verify all 11 abnormal indicators from 2025 report are correctly flagged
4. **Verify** personalized plans generate correctly for each flagged indicator
5. **Test** cross-indicator patterns (metabolic syndrome detection, CV risk cluster, etc.)
6. **Commit and push** to `claude/expand-health-indicators-ThnjJ`

---

## 8. File Map After Implementation

```
Health-Check/
├── index.html              # Existing 6-month plan (unchanged, add nav link)
├── analyzer.html           # NEW — Health Analyzer App
├── handover.md             # This file
├── template.html           # Legacy template
├── CLAUDE.md               # Project instructions
├── .github/workflows/
├── templates/
├── scripts/
└── reviews/
```

---

## 9. Open Questions

- **Print/export:** Should the results be print-friendly (CSS @media print)? Likely yes.
- **History:** Should the app save previous analyses to localStorage for trend comparison? Nice-to-have for v2.
- **Bilingual toggle:** Should the app support full Chinese mode? Current plan is English + Chinese medical terms.
- **Mobile:** index.html is already mobile-optimized; analyzer.html should match (responsive form layout).
