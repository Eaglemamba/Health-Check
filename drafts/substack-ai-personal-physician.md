# I Used AI as My Personal Physician for Three Months — A Software Engineer's Health Reversal Experiment

*If 81% of doctors are already using AI in their practice, why aren't you using it to manage your own health?*

---

## A Warning Letter from My Lab Results

This March, I got a physical exam report that made me uncomfortable.

Systolic blood pressure 135 mmHg (pre-hypertension). Elevated triglycerides. High cholesterol. Uric acid creeping toward the danger zone. I weighed 70 kg, BMI hovering at the edge of overweight. Actual sleep? Five to six hours — my Garmin watch gave me a cold, hard score of 63 out of 100.

The doctor said a few words: "Eat less salt, exercise more, watch your sleep." Next patient.

Three minutes. That was my appointment.

Standing outside the clinic, I did the math: four abnormal markers means four different specialists, four separate appointments, four rounds of waiting, four doctors telling me the same thing — "lifestyle adjustment." Come back in six months for blood work. Better or not, we'll see then.

That's not health management. That's a coin toss with extra steps.

I'm a software engineer. What I wanted was: daily tracking, real-time feedback, data-driven decisions, and someone — or *something* — that wouldn't rush me out the door in three minutes because twenty patients were waiting behind me.

So I did something unconventional: **I made AI my personal health manager.**

---

## Not Replacing Doctors — Filling the 99% Gap

Let me be absolutely clear: **AI is not a doctor, and I'm not trying to replace mine.**

But here's the reality: how often do you see your doctor? Twice a year? Four times? Ten minutes each?

A year has 8,760 hours. You spend roughly 40 minutes with your doctor. The remaining 8,759 hours and 20 minutes? Your health is entirely in your own hands.

That gap is where AI belongs.

In early 2026, Anthropic launched [Claude for Healthcare](https://www.anthropic.com/news/healthcare-life-sciences), allowing users to connect Apple Health and Android Health Connect data directly. An [AMA survey](https://www.ama-assn.org/practice-management/digital-health/more-80-physicians-use-ai-professionally-ama-survey) found over 81% of physicians now use AI professionally. [NPR reported](https://www.npr.org/sections/shots-health-news/2026/01/09/nx-s1-5670382/primary-care-doctor-shortage-medical-ai-diagnosis) that your next primary care doctor might be entirely online, accessed through an AI tool.

But what I did is more basic, more DIY — and possibly more accessible for regular people.

I didn't use any paid health AI product. My stack: **Claude Code + Markdown files + a Garmin watch + a blood pressure monitor.**

---

## System Architecture: Minimal but Effective

As an engineer, my first instinct was to build something elaborate. But this time I went deliberately minimal — **no app, no database, no dashboard. Just plain text files.**

```
templates/          → Templates (daily, weekly, monthly)
reviews/
  daily/            → One .md file per day
  weekly/           → Weekly review
  monthly/          → Monthly trend analysis
CLAUDE.md           → AI's "clinical guidelines"
index.html          → Six-month plan overview
```

The core concept is simple:

1. **Every morning, 3 minutes**: Answer five questions — weight, blood pressure, sleep, body discomfort, today's plan
2. **AI records immediately**, syncing data into the weekly review spreadsheet
3. **AI gives rule-based suggestions** — not generic "drink more water," but advice tailored to *my specific numbers that day*
4. **Every Sunday, 10 minutes**: Review trends, find patterns
5. **End of each month, 20 minutes**: Compare against six-month milestone targets

The most critical piece is `CLAUDE.md` — the "clinical guidelines manual" I wrote for the AI.

---

## Teaching AI to Be Your Physical Therapist

CLAUDE.md doesn't contain vague instructions like "please help me track my health." It contains **specific clinical decision rules**, like the protocols you'd find in a hospital.

Here's what I mean:

### Body Signals → Instant PT Advice

Every day, I log where my body hurts. AI doesn't just record it — it responds with targeted physical therapy recommendations based on the body part and severity:

> **Me:** "Left forearm and wrist — tight, aching. Intensity 3/10. Scapula — tight, 4/10."
>
> **AI:** "💡 PT Advice: Forearm stretch — palm facing up, use other hand to gently press fingers downward, 30 seconds ×2. Take a break every 50 minutes at work to mobilize wrists. Scapular retraction (Y-T-W against wall, 8 reps ×2 sets). Check if screen height is below eye level."

If the same body part shows up three days in a row, AI escalates — providing a complete home rehab routine (3-4 exercises). Five consecutive days? It firmly recommends booking a physical therapist.

### Data Anomalies → Automatic Alerts

The rules are specific:

- Systolic BP jumps >15 mmHg from yesterday → Ask if I slept poorly, was stressed, or ate high-sodium food
- Weight drops >1.5 kg in one week → Warning: too fast, risk of gout flare and gallstones
- Sleep Score <65 AND Body Battery <40 → Skip wall squats today, do gentle stretching only
- Water intake <1.5L → Remind that uric acid excretion efficiency drops

### Auto-Adjusting Exercise

AI classifies my recovery status into four tiers and adjusts accordingly:

| Status | Criteria | Exercise Recommendation |
|--------|----------|------------------------|
| Well Recovered | Sleep Score ≥70 + no pain + subjective ≥4/5 | Follow the plan, try to progress |
| Moderately Recovered | Score 65-70 or mild discomfort | Follow the plan, don't progress |
| Under-Recovered | Score <65 or Battery <40 or subjective ≤2 | Downgrade: fewer squat sets, walk instead of brisk walk |
| Pain Signal | Any body part ≥5/10 | Avoid that body part, provide alternatives |

**This isn't rocket science. It's encoding what a good physical therapist would do into rules an AI can execute.**

---

## The Six-Month Plan That Changed Everything

Four abnormal markers look like four problems. But after digging into the research, I discovered — **they share the same metabolic root cause.**

I spent a weekend with Claude, searching literature, running calculations, designing protocols. The result was a comprehensive six-month plan:

**Goal: 70 kg → 65 kg. All four markers back to normal.**

The most counterintuitive findings:

### 1. Sleep First, Not Exercise

5-6 hours of sleep increases hypertension risk by 3.5x. Cholesterol metabolism gene expression gets suppressed. Uric acid excretion efficiency drops. **If you don't fix sleep first, diet and exercise at 100% effort will only deliver 50% results.**

AI helped me design a three-step sleep repair protocol: cut water intake after 17:00 (to fix nighttime urination), elevate legs against the wall for 15 minutes before bed (to accelerate lower-limb fluid return), and a hard rule — do not leave bed before 5:30, period.

### 2. Wall Squats Are the Most Powerful Blood Pressure Exercise

A 2023 *British Journal of Sports Medicine* meta-analysis (270 RCTs, 15,827 participants): wall squats ranked #1 among all exercise types for lowering systolic blood pressure. Three times per week, 16 minutes per session (including rest), 12 weeks → systolic BP reduction of -12.9 mmHg.

My systolic is 135. 135 - 13 = 122. **One exercise could take me from pre-hypertension to normal.**

### 3. Protein Source Matters More Than Protein Amount

NHANES III showed total protein intake has no significant correlation with uric acid. But high red meat consumers had uric acid +0.48 mg/dL higher, while dairy consumers were -0.21 mg/dL *lower*. **So it's not "eat less protein" — it's "switch the source."**

---

## A Typical Morning

5:47 AM. Garmin vibrates. I'm awake.

Open the terminal. Type `/daily-checkin`. Claude starts asking:

> "Good morning. Weight?"

70.5.

> "Blood pressure, first reading?"

117/70, heart rate 82. (Wait one minute. Take the second reading.)

> "Sleep status?"

Fell asleep 22:28, woke up 05:47, woke once during the night (bathroom). Score 64, Battery 36. Subjective recovery 2/5.

> "Body signals?"

Left forearm tight 3/10, wrist tight 3/10, scapula tight 4/10.

> "Today's exercise plan?"

Wall squats.

Three minutes. File saved. Then AI automatically appends its advice:

> 💡 PT Advice: Sleep Score 64 + Body Battery 36, recovery clearly insufficient. Today's wall squats — downgrade to 2 sets × 20 seconds, don't push for a breakthrough. Forearm and scapular tightness suggests early upper cross syndrome pattern — do forearm stretches and scapular Y-T-W wall exercises every 50 minutes during work today.

**That's my "personal physician." No supplement upsells, no treatment packages, no waiting rooms. Three minutes a day, precisely tailored to my exact condition that morning.**

---

## Why This Only Became Possible Now

Three years ago, you couldn't do this.

Not because AI didn't exist — ChatGPT launched in late 2022. It was because AI lacked three critical capabilities:

**1. Persistent Memory and Context**

Early chatbots started fresh every conversation. They didn't remember yesterday's blood pressure, last week's sleep trend, or last month's body signals. I solved this with CLAUDE.md and a Markdown file system — every time AI starts, it reads the complete ruleset and historical data.

**2. Instruction Following**

Try telling early AI: "Only answer what I ask, no fluff, keep it to two sentences." It couldn't do it. Today's models can strictly follow complex clinical decision trees, triggering the right advice at the right moment.

**3. Tool Use**

Claude Code can directly read and write files, create directory structures, execute commands. It's not just "chatting" — it's an agent that can operate a system. This lets the entire health tracking workflow happen automatically — I answer questions, it updates all the spreadsheets in real time.

---

## The Real Risks: What You Must Know

I don't want to write a "AI saved my health" puff piece. There are real risks here.

### AI Makes Mistakes

A [Stanford and Harvard study](https://time.com/7382493/ai-healthcare-doctors/) found that AI medical models produced severely harmful clinical recommendations in up to 22.2% of cases. My mitigation: **AI only handles daily tracking and self-care advice. Any abnormal data (systolic >160, sudden joint swelling) goes straight to a real doctor.**

### Data Is Not Diagnosis

Weight, blood pressure, and Sleep Score are surface metrics. True metabolic status requires blood work. That's why the plan includes three blood draws (months 0, 3, and 6). AI can't replace that.

### Self-Management Has Limits

Chronic disease management isn't really about data — it's about behavior change. AI can tell you "drink 2.5 liters of water today," but it can't drink it for you. [As TIME reported](https://time.com/7382493/ai-healthcare-doctors/): AI isn't shrinking the demand for medical professionals — it's revealing how much unmet need was always there.

---

## The Numbers at Three Months

(These are the plan's projected milestones, not guarantees.)

My six-month plan's month-three targets:

- **Weight:** 70.0 → 67.5 kg
- **Systolic BP:** 135 → below 125 (supported by wall squat 12-week RCT data)
- **Sleep Score:** 63 → 70+ (if sleep repair protocol is followed)
- **Triglycerides:** Expected 15-30% reduction (Omega-3 8-12 week effect + dietary changes)

Full blood work at month three. I'll write the next article then — with real numbers.

---

## You Can Do This Too

You don't need to know how to code. You need:

1. **A blood pressure monitor** (upper-arm cuff type, under $30)
2. **A watch with sleep tracking** (Garmin, Apple Watch, even a Xiaomi band)
3. **An AI assistant** (Claude, ChatGPT, or similar)
4. **Three minutes of daily discipline**

Tell the AI your body metrics. Ask it to track trends and alert you on anomalies. You don't need to build a system as elaborate as mine — even just saying "today BP was 135/75, slept 6 hours, right shoulder a bit sore" daily will let AI start finding patterns and spotting trends.

**The tool doesn't matter. What matters is whether you're willing to spend three minutes a day actually paying attention to your body.**

---

## Final Thoughts

I'm not claiming AI can replace doctors. I booked a sleep clinic and a urologist on day one. The plan has a clear medical appointment schedule.

But I am claiming this: **Between your doctor's three-minute appointment and the "come back in six months for blood work," there is an enormous void. AI can fill that void.**

It's not perfect. It makes mistakes. It can't perform surgery or write prescriptions.

But it can ask you every morning: "How's your body today?" And actually listen to your answer.

That's something even many doctors can't do.

---

*This is the first article in the "Six-Month Health Reversal Plan" series. I'll write updates at month three (after blood work follow-up) and month six (plan completion). If you're interested in the specific system design, templates, or how to write a CLAUDE.md for health management, the entire project is open-source.*

*Disclaimer: This article shares a personal health management experience and does not constitute medical advice. All health decisions should be made in consultation with qualified medical professionals.*

---

**Sources:**
- [AMA: More than 80% of physicians use AI professionally](https://www.ama-assn.org/practice-management/digital-health/more-80-physicians-use-ai-professionally-ama-survey)
- [AMA: Physicians' use of AI doubled from 2023 to 2026](https://www.fiercehealthcare.com/ai-and-machine-learning/ama-physicians-use-ai-doubled-2023-2026)
- [Anthropic: Advancing Claude in Healthcare and the Life Sciences](https://www.anthropic.com/news/healthcare-life-sciences)
- [NPR: Your next primary care doctor could be online only, accessed through an AI tool](https://www.npr.org/sections/shots-health-news/2026/01/09/nx-s1-5670382/primary-care-doctor-shortage-medical-ai-diagnosis)
- [TIME: Healthcare Is AI's Hardest Test](https://time.com/7382493/ai-healthcare-doctors/)
- [BCG: How AI Agents and Tech Will Transform Health Care in 2026](https://www.bcg.com/publications/2026/how-ai-agents-will-transform-health-care)
- [Bessemer Venture Partners: State of Health AI 2026](https://www.bvp.com/atlas/state-of-health-ai-2026)
- [Medium: Claude Code for Life #1 — Managing my Health and Wellness](https://medium.com/data-science-collective/claude-code-for-life-1-managing-my-health-and-wellness-cae435c77030)
- [PMC: AI in Chronic Disease Self-Management](https://pmc.ncbi.nlm.nih.gov/articles/PMC12675485/)
- [AHA: Hospitals Advance AI-Enabled Prevention at Scale](https://www.aha.org/aha-center-health-innovation-market-scan/2025-11-18-hospitals-advance-ai-enabled-prevention-scale)
