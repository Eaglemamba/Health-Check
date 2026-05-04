/* ====== Health Reversal Plan — bilingual data ====== */
window.HC_DATA = {
  // Hero
  hero: {
    eyebrow: { en: "6-Month Health Reversal Plan · March 2026 Edition", zh: "6 個月健康逆轉計畫 · 2026 年 3 月個人化版" },
    title:   { en: ["Normalize four markers,", "from the ", "ground up."],
               zh: ["從根基修復", "同步正常化", "四項關鍵指標"] },
    titleEm: { en: "without medication first", zh: "先以生活方式介入" },
    lede:    { en: "Sleep, BP, lipids, uric acid — one shared metabolic root. Lifestyle stacks first; medication only after lifestyle plateaus.",
               zh: "睡眠、血壓、血脂、尿酸——共享同一個代謝根源。生活方式介入優先，等到效果平台期再考慮藥物。" },
    progressLbl: { en: "Weight progress · 70 → 65 kg", zh: "體重進度 · 70 → 65 公斤" },
    progressMeta: { en: "Day 49 · 67.8 kg · Month-2 target met early", zh: "第 49 天 · 67.8 公斤 · 提前達第 2 月目標" },
    startDate: { en: "Start date · Mar 17, 2026 · Last sync May 4", zh: "起始日期 · 2026 年 3 月 17 日 · 最後同步 5/4" },
  },

  markers: [
    {
      sys: "heart", name: { en: "Blood Pressure", zh: "血壓" },
      val: "122/71", unit: "mmHg",
      delta: { en: "W17 weekly avg · target met (<130)", zh: "W17 週均 · 已達標 (<130)" },
      cadence: { en: "Daily · 7-day avg", zh: "每日 · 7 日均" },
      status: "ok",
    },
    {
      sys: "sleep", name: { en: "Sleep Score", zh: "睡眠分數" },
      val: "77", unit: "Garmin",
      delta: { en: "5/4 · OSA flag: T90 18.4% (severe)", zh: "5/4 · OSA 紅旗：T90 18.4%（重度）" },
      cadence: { en: "Daily · Garmin", zh: "每日 · Garmin" },
      status: "warn",
    },
    {
      sys: "weight", name: { en: "Weight", zh: "體重" },
      val: "67.8", unit: "kg",
      delta: { en: "5/2 official · Month-2 target met early", zh: "5/2 週六正式 · 提前達第 2 月目標" },
      cadence: { en: "Daily · Sat official", zh: "每日 · 週六正式" },
      status: "ok",
    },
    {
      sys: "uric", name: { en: "Uric Acid", zh: "尿酸" },
      val: "8.9", unit: "mg/dL",
      delta: { en: "Constitutional · neph. referral", zh: "體質性偏高 · 已轉診腎臟科" },
      cadence: { en: "Lab only · last Mar 25", zh: "僅實驗室 · 上次 3/25" },
      status: "bad",
    },
  ],

  tabs: [
    { id: "overview", en: "Overview", zh: "總覽" },
    { id: "sleep",    en: "Sleep",    zh: "睡眠" },
    { id: "diet",     en: "Diet",     zh: "飲食" },
    { id: "exercise", en: "Wall sits", zh: "靠牆深蹲" },
    { id: "running",  en: "Running",  zh: "跑步" },
    { id: "supps",    en: "Supplements", zh: "保健品" },
    { id: "routine",  en: "Daily Routine", zh: "每日作息" },
    { id: "timeline", en: "Timeline", zh: "時程" },
    { id: "safety",   en: "Safety",   zh: "安全" },
    { id: "tracker",  en: "Tracker",  zh: "追蹤" },
  ],

  // ===== Overview =====
  overview: {
    profile: {
      en: [
        ["Bedtime", "22:00–22:40 (target 22:30)"],
        ["Actual sleep", "6.0–7.2 h · W17 avg Sleep Score 71.4"],
        ["Garmin (W17)", "Body Battery 56.7 · RHR 56–61"],
        ["BP (W17 avg)", "122/71 mmHg · ✓ <130 target"],
        ["Weight (5/2 Sat)", "67.8 kg · 20.2% BF · VFL 9.5"],
        ["OSA flag", "T90 18.4% on 5/4 · POSA trial 5/5–5/8"],
        ["Running", "Started 4/26 — building base"],
        ["Current supps", "Omega-3 4g, hibiscus, D3K2, cherry, Mg, citrulline, psyllium 10g"],
        ["Discontinued", "NOW EGCG (AST 27→38, stopped 4/21)"],
      ],
      zh: [
        ["就寢時間", "22:00–22:40（目標 22:30）"],
        ["實際睡眠", "6.0–7.2 小時 · W17 平均 Sleep Score 71.4"],
        ["Garmin（W17）", "身體電量 56.7 · RHR 56–61"],
        ["血壓（W17 週均）", "122/71 mmHg · ✓ 已達 <130 目標"],
        ["體重（5/2 週六）", "67.8 公斤 · 體脂 20.2% · 內臟 9.5"],
        ["OSA 紅旗", "5/4 T90 18.4% · 體位治療試驗 5/5–5/8"],
        ["跑步", "4/26 開始，建立基礎中"],
        ["目前保健品", "Omega-3 4g、洛神花、D3K2、酸櫻桃、鎂、瓜胺酸、洋車前子 10g"],
        ["已停用", "NOW EGCG（AST 27→38，4/21 停用）"],
      ],
    },
    priority: {
      title: { en: "Top priority — fix sleep first", zh: "最高優先 — 先修復睡眠" },
      body: {
        en: "5–6 h of actual sleep + Body Battery 40–50 means sleep deprivation is undermining metabolic repair from the ground up. Without sleep, even a perfect diet and exercise regimen delivers only 50% of its potential.",
        zh: "實際睡眠 5–6 小時 + 身體電量 40–50，代表睡眠不足正在從根基破壞所有代謝修復。如果不先修好睡眠，即使完美的飲食和運動計畫也只能發揮 50% 的效果。",
      },
      order: {
        en: ["Sleep repair + OSA screening", "Shift hydration earlier", "Wall sits", "Diet adjustments", "Supplements"],
        zh: ["睡眠修復 + OSA 篩檢", "提前補水時間", "靠牆深蹲", "飲食調整", "保健品"],
      },
    },
    stack: {
      title: { en: "BP-lowering combination — interventions stack", zh: "降壓組合 — 介入效果疊加" },
      sub:   { en: "Each row layers on top of the others. Diastolic is already 75 — lifestyle first prevents over-dipping.",
               zh: "以下每項介入效果可以疊加。舒張壓已經 75，生活方式優先以避免過度下降。" },
      head:  { en: ["Intervention", "SBP reduction", "Notes"],
               zh: ["介入措施", "收縮壓降幅", "備註"] },
      rows: [
        ["wallsit", { en: "Wall sits 3×/week", zh: "靠牆深蹲 3次/週" }, "−10 to −13 mmHg",
          { en: "Visible at 12 weeks; equivalent to one BP medication", zh: "12 週可見效；等同一種降壓藥" }],
        ["sodium",  { en: "Sodium < 1,500 mg/day", zh: "鈉攝取 < 1,500 mg/天" }, "−5 to −8 mmHg",
          { en: "Sodium impacts systolic more than diastolic", zh: "鈉對收縮壓影響大於舒張壓" }],
        ["omega",   { en: "Omega-3 ~2 g/day", zh: "Omega-3 ~2 g/天" }, "−4 to −5 mmHg",
          { en: "Preferentially lowers systolic", zh: "優先降低收縮壓" }],
        ["sleep",   { en: "Sleep repair to 7+ hours", zh: "睡眠修復至 7+ 小時" }, "−3 to −5 mmHg",
          { en: "Reduces sympathetic overactivation", zh: "降低交感神經過度活化" }],
        ["weight",  { en: "Weight loss of 5 kg", zh: "減重 5 公斤" }, "−3 to −5 mmHg",
          { en: "~1 mmHg per kg lost", zh: "每減 1 kg 約降 1 mmHg" }],
        ["combo",   { en: "Combined potential", zh: "合併效果" }, "−25 to −36 mmHg",
          { en: "135 → 99–110 range", zh: "135 → 99–110 範圍" }],
      ],
    },
  },

  // ===== Sleep =====
  sleep: {
    intro: {
      en: "Lies down 20:30 → wakes 2–4 AM for nocturia → alert after bathroom → starts working → actual sleep 5–6 h. Goal: delay nocturia to 5:00–5:30, achieve 8.5–9 h.",
      zh: "20:30 躺下 → 凌晨 2–4 點夜尿醒來 → 上完廁所精神清醒 → 起床工作 → 實際睡眠 5–6 小時。目標：將夜尿延後至 5:00–5:30，達成 8.5–9 小時睡眠。",
    },
    pillars: [
      {
        ttl: { en: "A. Solve nocturia (upstream)", zh: "A. 解決夜尿（上游問題）" },
        items: {
          en: [
            "Reduce fluids after 17:00; minimal soup at dinner.",
            "Pre-bed leg elevation 15–20 min at 20:00 — fluid returns to circulation, kidneys process before sleep.",
            "Always urinate at 20:00 even without urge.",
            "After 18:30, lip-moistening sips only.",
          ],
          zh: [
            "17:00 後減少液體攝取，晚餐少喝湯。",
            "20:00 睡前抬腿 15–20 分鐘 — 下肢液體回流，腎臟入睡前處理。",
            "20:00 一定要上廁所，即使沒有尿意。",
            "18:30 後僅「潤唇式」小啜。",
          ],
        },
      },
      {
        ttl: { en: "B. If you wake, force return to sleep", zh: "B. 半夜醒來，強迫回去睡" },
        items: {
          en: [
            "Lights off; dim warm nightlight only. No phone, no clock.",
            "Return to bed immediately. 4-7-8 breathing × 2–3 cycles.",
            "Hard rule: do not leave bed before 5:30 AM.",
            "Quiet rest still gives ~50% of deep sleep recovery.",
          ],
          zh: [
            "全程不開燈，僅暖色低亮夜燈。不碰手機、不看時鐘。",
            "立即回床。4-7-8 呼吸法 × 2–3 個循環。",
            "硬規則：5:30 之前不離床。",
            "安靜休息仍可提供深度睡眠約 50% 的恢復效果。",
          ],
        },
      },
      {
        ttl: { en: "C. OSA screening", zh: "C. OSA 篩檢" },
        items: {
          en: [
            "Enable Garmin Pulse Ox tonight — observe 5–7 nights for SpO2 < 90%.",
            "Phone audio recording overnight for snoring / apnea.",
            "Book sleep clinic (pulmonology / ENT) + urology for nocturia.",
            "Bring Sleep Score, Body Battery, Pulse Ox data to doctor.",
          ],
          zh: [
            "今晚開啟 Garmin Pulse Ox — 觀察 5–7 晚 SpO2 是否 < 90%。",
            "手機錄音 app 整夜錄音檢查打鼾／呼吸暫停。",
            "預約睡眠門診（胸腔／耳鼻喉）+ 泌尿科夜尿評估。",
            "帶 Sleep Score、Body Battery、Pulse Ox 數據給醫師。",
          ],
        },
      },
      {
        ttl: { en: "D. Sleep position", zh: "D. 睡姿" },
        items: {
          en: [
            "Side sleep (left preferred) — supine collapses tongue base, ~50% more apnea.",
            "Pillow behind back to prevent rolling supine.",
            "Elevate head 15–20° — reduces airway pressure & reflux.",
          ],
          zh: [
            "側睡（左側為佳）— 仰睡使舌根後墜，呼吸暫停多 ~50%。",
            "背後放枕頭防止翻回仰躺。",
            "墊高床頭 15–20° — 減少呼吸道壓力與胃食道逆流。",
          ],
        },
      },
    ],
    cbti: {
      ttl: { en: "CBT-I — first-line, ranked by impact", zh: "CBT-I — 第一線療法，依證據強度排序" },
      head: { en: ["#", "Intervention", "Mechanism", "Your application"],
              zh: ["#", "介入", "機轉", "你的應用"] },
      rows: [
        ["1", { en: "Sleep restriction", zh: "睡眠限制" },
               { en: "Build adenosine pressure by limiting time in bed", zh: "限制躺床時間以建立腺苷壓力" },
               { en: "No bed before 20:00; no bed past 5:30", zh: "20:00 前不躺床；5:30 後不躺床" }],
        ["2", { en: "Stimulus control", zh: "刺激控制" },
               { en: "Bed = sleep only", zh: "床 = 只用來睡覺" },
               { en: "If awake >20 min, get up — no screens", zh: "醒著 >20 分鐘就起床，不碰螢幕" }],
        ["3", { en: "Sleep hygiene", zh: "睡眠衛生" },
               { en: "Environment & behavior", zh: "環境與行為" },
               { en: "Blackout, 18–20°C, no caffeine after 14:00", zh: "全黑、18–20°C、14:00 後無咖啡因" }],
        ["4", { en: "Relaxation", zh: "放鬆技巧" },
               { en: "Reduce pre-sleep arousal", zh: "降低入睡前覺醒" },
               { en: "4-7-8 breathing, leg elevation", zh: "4-7-8 呼吸法、抬腿" }],
        ["5", { en: "Cognitive restructuring", zh: "認知重建" },
               { en: "Reduce performance anxiety", zh: "降低對睡眠的焦慮" },
               { en: "“Quiet rest is 50% of deep sleep”", zh: "「安靜休息有深度睡眠 50% 效果」" }],
      ],
    },
    metrics: {
      ttl: { en: "Tracking metrics", zh: "追蹤指標" },
      items: [
        ["Sleep Score", "≥ 70 → 80", "var(--sleep)"],
        ["Body Battery (waking)", "≥ 65 → 75", "var(--metabolic)"],
        ["Deep sleep %", "> 15%", "var(--uric)"],
        ["Pulse Ox SpO2", "stable, no dips < 90%", "var(--water)"],
      ],
    },
  },

  // ===== Diet =====
  diet: {
    macros: [
      ["calories",  { en: "Calories", zh: "熱量" }, "1,950–2,050", "kcal", { en: "Base · +150 on training days", zh: "基礎 · 運動日 +150" }],
      ["protein",   { en: "Protein", zh: "蛋白質" }, "95", "g", { en: "Range 85–115 · ~30 g/meal", zh: "區間 85–115 · 每餐 ~30g" }],
      ["fat",       { en: "Fat", zh: "脂肪" }, "55–60", "g", { en: "Hard floor 50 · MUFA-led", zh: "硬下限 50 · 以單元不飽和為主" }],
      ["carbs",     { en: "Carbs", zh: "碳水" }, "170–200", "g", { en: "Complex, low-GI", zh: "複合、低 GI" }],
      ["sodium",    { en: "Sodium", zh: "鈉" }, "< 1,500", "mg", { en: "Hard cap 2,000", zh: "硬上限 2,000" }],
      ["fiber",     { en: "Fiber", zh: "纖維" }, "28–32", "g", { en: "β-glucan 3 g/day", zh: "β-glucan 3 g/天" }],
      ["water",     { en: "Water", zh: "飲水" }, "2.5–3.0", "L", { en: "Done by 17:00", zh: "17:00 前完成" }],
    ],
    combos: [
      { name: { en: "DIY Assembly", zh: "DIY 組裝" }, recommended: true,
        desc: { en: "Steamed sweet potato + ready-to-eat chicken breast + black soy milk. Add a tea egg.",
                zh: "蒸地瓜 + 即食雞胸肉 + 黑豆漿 + 茶葉蛋。" },
        kcal: 450, sodium: 410, protein: 32 },
      { name: { en: "Grilled Chicken Box", zh: "香烤雞胸便當" },
        desc: { en: "7-11 Simple Fit. Purple rice, broccoli, carrot, king oyster mushroom.",
                zh: "7-11 Simple Fit 香烤雞胸鮮蔬餐。紫米、花椰菜、紅蘿蔔、杏鮑菇。" },
        kcal: 374, sodium: 577, protein: 18 },
      { name: { en: "Cauliflower Low-Carb", zh: "減醣花椰菜飯" },
        desc: { en: "Chicken breast cauliflower rice. Triglyceride-friendly.",
                zh: "雞胸花椰菜飯減醣餐。對三酸甘油酯友善。" },
        kcal: 319, sodium: 600, protein: 20 },
      { name: { en: "Sweet Potato Premium", zh: "地瓜經典升級" },
        desc: { en: "Sweet potato + sous vide chicken + edamame + black soy milk.",
                zh: "蒸地瓜 + 舒肥雞胸 + 鹽味毛豆 + 黑豆漿。" },
        kcal: 470, sodium: 725, protein: 35 },
      { name: { en: "Oatmeal + Chicken", zh: "燕麥 + 雞胸" },
        desc: { en: "50–60 g oats brewed with milk + chicken breast + tea egg. β-glucan 3 g hits LDL target.",
                zh: "50–60 g 燕麥沖牛奶 + 雞胸 + 茶葉蛋。β-glucan 3 g 達到降 LDL 目標。" },
        kcal: 470, sodium: 500, protein: 28 },
      { name: { en: "Sweet Potato + Egg Salad", zh: "地瓜 + 蛋沙拉" },
        desc: { en: "Sweet potato + 2 tea eggs + Simple-Fit salad (½ dressing) + grain soy milk.",
                zh: "地瓜 + 茶葉蛋 ×2 + 繽紛蔬菜沙拉（醬料一半）+ 健康穀物豆漿。" },
        kcal: 530, sodium: 700, protein: 26 },
    ],
    avoid: {
      en: ["Sugary drinks", "Beer", "Organ meats", "Processed meats", "Fried foods", "Instant noodles", "Shellfish", "Excessive white rice", "Bubble tea", "Pig blood cake"],
      zh: ["含糖飲料", "啤酒", "內臟", "加工肉品", "油炸食品", "泡麵", "蝦蟹貝類", "過量白飯", "珍珠奶茶", "豬血糕"],
    },
    increase: {
      en: ["Low-fat dairy", "Oats", "Edamame / tofu", "Unsalted nuts 15g", "Cherries / blueberries", "Sweet potato", "Black fungus", "Green / oolong tea", "Guava", "Kiwi"],
      zh: ["低脂乳製品", "燕麥", "毛豆 / 豆腐", "無調味堅果 15g", "櫻桃 / 藍莓", "地瓜", "黑木耳", "綠茶 / 烏龍茶", "芭樂", "奇異果"],
    },
    fructose: {
      ttl: { en: "Bubble tea — sugar reality check", zh: "珍珠奶茶 — 含糖真相" },
      sub: { en: "Fructose → KHK (no feedback inhibition) → ATP depletion → AMP → IMP → uric acid. One full-sugar bubble tea hits UA harder than a plate of shrimp.",
             zh: "果糖 → KHK（無回饋抑制）→ ATP 耗竭 → AMP → IMP → 尿酸。一杯全糖珍奶對尿酸的衝擊大於一盤蝦。" },
      rows: [
        [{ en: "Minimal (一分糖)", zh: "一分糖" }, "10g", "2"],
        [{ en: "Less sweet (微糖)", zh: "微糖" }, "15–25g", "3–5"],
        [{ en: "Half sweet (半糖)", zh: "半糖" }, "30–35g", "6–7"],
        [{ en: "Full sweet (全糖)", zh: "全糖" }, "50–52.5g", "10 — full WHO daily limit"],
      ],
    },
  },

  // ===== Exercise =====
  exercise: {
    why: {
      en: "Isometric exercise — wall sits — is the #1 most effective exercise for lowering BP per the 2023 BJSM meta-analysis (270 RCTs, 15,827 participants). 4 sets × 2 min, 3×/week → systolic BP −12.9 mmHg over 12 weeks. Specially effective for ISH: improves vascular endothelial function and arterial compliance.",
      zh: "等長運動 — 靠牆深蹲 — 在 2023 BJSM 統合分析（270 項 RCT、15,827 名參與者）中是最有效的降壓運動。4 組 × 2 分鐘、每週 3 次，12 週收縮壓 −12.9 mmHg。特別適合 ISH：改善血管內皮功能與動脈順應性。",
    },
    technique: {
      ttl: { en: "Six key points", zh: "六大要點" },
      rows: [
        [{ en: "Back fully against wall", zh: "背部完全貼牆" }, { en: "Head, shoulders, upper & lower back. Engage core.", zh: "頭、肩、上下背全貼牆，核心收緊。" }],
        [{ en: "Foot position", zh: "腳的位置" }, { en: "Shoulder-width, ~60 cm out from wall.", zh: "與肩同寬，離牆 ~60 cm。" }],
        [{ en: "Knees don't pass toes", zh: "膝蓋不超過腳尖" }, { en: "Shins vertical; knees above ankles.", zh: "小腿垂直，膝在踝正上。" }],
        [{ en: "Knee angle", zh: "膝蓋角度" }, { en: "Start 120° (very shallow); deepen weekly to 90°.", zh: "從 120°（非常淺）開始，逐週加深至 90°。" }],
        [{ en: "Breathing", zh: "呼吸" }, { en: "Steady nose-in / mouth-out. Never hold breath.", zh: "鼻吸口呼，絕不憋氣。" }],
        [{ en: "Center of gravity", zh: "重心" }, { en: "Weight on heels, not toes.", zh: "重心在腳跟，不是腳尖。" }],
      ],
    },
    progression: [
      // [week, angle, sec, label{en,zh}]
      [1, 120, 15,  { en: "Adaptation", zh: "適應" }],
      [2, 120, 22,  { en: "Increase duration", zh: "增加時間" }],
      [3, 105, 28,  { en: "Deepen angle", zh: "加深角度" }],
      [4, 100, 30,  { en: "Build intensity", zh: "建立強度" }],
      [5, 100, 38,  { en: "Build", zh: "進展" }],
      [6, 100, 45,  { en: "Build", zh: "進展" }],
      [7, 100, 52,  { en: "Build", zh: "進展" }],
      [8, 100, 60,  { en: "Build", zh: "進展" }],
      [9, 95, 75,   { en: "Push", zh: "推進" }],
      [10, 92, 90,  { en: "Push", zh: "推進" }],
      [11, 90, 105, { en: "Target zone", zh: "達標區" }],
      [12, 90, 120, { en: "Target — 2 min", zh: "達標 — 2 分鐘" }],
    ],
    weekplan: {
      head: { en: ["Day", "Activity", "Duration", "When"], zh: ["日", "活動", "時長", "時間"] },
      rows: [
        [{ en: "Mon", zh: "一" }, { en: "Brisk walk + wall sits", zh: "快走 + 靠牆深蹲" }, "20 + 14 min", { en: "Evening 19:00", zh: "晚間 19:00" }],
        [{ en: "Tue", zh: "二" }, { en: "Exercise snacks ×3", zh: "運動零食 ×3" }, "5 min × 3", { en: "Throughout day", zh: "分散全天" }],
        [{ en: "Wed", zh: "三" }, { en: "Brisk walk", zh: "快走" }, "20 min", { en: "Commute / evening", zh: "通勤或晚間" }],
        [{ en: "Thu", zh: "四" }, { en: "Wall sits + bodyweight", zh: "靠牆深蹲 + 徒手" }, "14 + 10 min", { en: "Evening, home", zh: "晚間在家" }],
        [{ en: "Fri", zh: "五" }, { en: "Brisk walk + snacks ×2", zh: "快走 + 零食 ×2" }, "20 + 10 min", { en: "Spread", zh: "分散" }],
        [{ en: "Sat", zh: "六" }, { en: "Family activity day", zh: "家庭活動日" }, "30 min", { en: "With family", zh: "全家一起" }],
        [{ en: "Sun", zh: "日" }, { en: "Light stretching", zh: "輕度伸展" }, "10 min", { en: "Any time", zh: "任何時間" }],
      ],
    },
  },

  // ===== Supplements =====
  supps: [
    { name: "Omega-3 Fish Oil rTG", target: { en: "TG ↓ / SBP ↓ / anti-inflammatory", zh: "三酸甘油酯 ↓ / 收縮壓 ↓ / 抗發炎" },
      dose: "4 caps · ~2g EPA+DHA", time: { en: "All 4 after dinner", zh: "晚餐後 4 顆" }, cost: "2,000–2,250", color: "var(--heart)" },
    { name: "Psyllium Husk", target: { en: "LDL −9.69 mg/dL · bile acid binding", zh: "LDL −9.69 mg/dL · 膽汁酸結合" },
      dose: "5g × 2 (10g)", time: { en: "11:30 + 16:30", zh: "11:30 + 16:30" }, cost: "150–300", color: "var(--metabolic)" },
    { name: "D3 + K2", target: { en: "Vit D / hsCRP / BP / Ca-routing", zh: "維他命 D / hsCRP / 血壓 / 鈣質導向" },
      dose: "D3 2000 IU + K2 100 mcg", time: { en: "Breakfast blend", zh: "早餐果昔" }, cost: "200–400", color: "var(--weight)" },
    { name: "Hibiscus Calyces", target: { en: "SBP −7.58 / DBP −3.53 · LDL −12% · UA (XO)", zh: "SBP −7.58 / DBP −3.53 · LDL −12% · 尿酸 (XO)" },
      dose: "2g × 2 cups", time: { en: "9:30 + 14:00", zh: "9:30 + 14:00" }, cost: "100–200", color: "var(--heart)" },
    { name: "L-Citrulline", target: { en: "NO precursor · vasodilation · renal perfusion", zh: "一氧化氮前體 · 血管舒張 · 腎臟灌流" },
      dose: "2 g", time: { en: "Breakfast blend", zh: "早餐果昔" }, cost: "200–350", color: "var(--sleep)" },
    { name: "Mg Glycinate", target: { en: "Sleep · BP · HbA1c adjunct", zh: "睡眠 · 血壓 · HbA1c 輔助" },
      dose: "200–400 mg", time: { en: "Bedtime", zh: "睡前" }, cost: "300–500", color: "var(--uric)" },
    { name: "Tart Cherry (CherryPURE)", target: { en: "UA −37% (4-week RCT) · CRP ↓ · sleep", zh: "尿酸 −37%（4 週 RCT）· CRP ↓ · 助眠" },
      dose: "1000–2000 mg", time: { en: "Bedtime", zh: "睡前" }, cost: "370–740", color: "var(--uric)" },
    { name: "Whey Protein", target: { en: "MPS · satiety · lean mass on cut", zh: "肌肉合成 · 飽足感 · 減重保肌" },
      dose: "30 g (25–30 g protein)", time: { en: "Breakfast blend", zh: "早餐果昔" }, cost: "800–1,200", color: "var(--metabolic)" },
    { name: "Pumpkin Seeds (food)", target: { en: "Zn + Mg + phytosterol + tryptophan", zh: "鋅 + 鎂 + 植物固醇 + 色胺酸" },
      dose: "30 g", time: { en: "Afternoon 15:00", zh: "下午 15:00" }, cost: "300–500", color: "var(--weight)" },
  ],

  // ===== Daily Routine — 24h timeline events =====
  routine: [
    // hour, label{en,zh}, cat
    [5.5,  { en: "Wake", zh: "起床" }, "sleep"],
    [7,    { en: "Breakfast blend", zh: "早餐果昔" }, "meal"],
    [9.5,  { en: "Hibiscus #1", zh: "洛神花 ①" }, "supp"],
    [11.5, { en: "Psyllium #1", zh: "洋車前子 ①" }, "supp"],
    [12,   { en: "Lunch", zh: "午餐" }, "meal"],
    [12.7, { en: "Post-lunch walk", zh: "餐後快走" }, "exer"],
    [14,   { en: "Hibiscus #2", zh: "洛神花 ②" }, "supp"],
    [15.5, { en: "Pumpkin seeds", zh: "南瓜籽" }, "supp"],
    [16.5, { en: "Psyllium #2", zh: "洋車前子 ②" }, "supp"],
    [17,   { en: "Fluid cutoff", zh: "停止補水" }, "cutoff"],
    [18.5, { en: "Dinner + Omega-3", zh: "晚餐 + 魚油" }, "meal"],
    [19,   { en: "Wall sits", zh: "靠牆深蹲" }, "exer"],
    [20,   { en: "Leg elevation", zh: "抬腿" }, "exer"],
    [20.5, { en: "Bed · Mg + Cherry", zh: "就寢 · 鎂 + 酸櫻桃" }, "sleep"],
  ],

  // ===== Daily checklist =====
  checklist: {
    en: [
      ["water_pre17", "Hydration completed before 17:00 (2.5–3.0 L)"],
      ["sodium",      "Stayed under 1,500 mg sodium today"],
      ["walk",        "30-min post-lunch walk"],
      ["wallsit",     "Wall sits — 4 sets × current target"],
      ["psyllium",    "Psyllium husk × 2 (11:30 & 16:30)"],
      ["hibiscus",    "Hibiscus × 2 cups (9:30 & 14:00)"],
      ["omega",       "Omega-3 × 4 capsules with dinner"],
      ["mg_cherry",   "Magnesium + tart cherry at bedtime"],
      ["leg_elev",    "Leg elevation 15 min before bed"],
      ["bed_530",     "Did not leave bed before 5:30"],
      ["bp_log",      "BP measured & logged"],
      ["weight_log",  "Weight measured & logged"],
    ],
    zh: [
      ["water_pre17", "17:00 前完成補水（2.5–3.0 L）"],
      ["sodium",      "今日鈉攝取 < 1,500 mg"],
      ["walk",        "午餐後快走 30 分鐘"],
      ["wallsit",     "靠牆深蹲 — 4 組 × 當週目標"],
      ["psyllium",    "洋車前子 × 2（11:30 & 16:30）"],
      ["hibiscus",    "洛神花 × 2 杯（9:30 & 14:00）"],
      ["omega",       "晚餐 Omega-3 × 4 顆"],
      ["mg_cherry",   "睡前鎂 + 酸櫻桃"],
      ["leg_elev",    "睡前抬腿 15 分鐘"],
      ["bed_530",     "5:30 前未離床"],
      ["bp_log",      "已量測並記錄血壓"],
      ["weight_log",  "已量測並記錄體重"],
    ],
  },

  // ===== Timeline / months =====
  months: [
    { num: 1, ttl: { en: "Sleep first", zh: "先修睡眠" },
              body: { en: "OSA screen, fluid timing, leg elevation, 5:30 rule.", zh: "OSA 篩檢、補水時機、抬腿、5:30 規則。" } },
    { num: 2, ttl: { en: "Foundation", zh: "打基礎" },
              body: { en: "Brisk walk routine, sodium audit, supplement stack settled.", zh: "快走、鈉審視、保健品穩定。" } },
    { num: 3, ttl: { en: "Wall sit ramp", zh: "靠牆深蹲進展" },
              body: { en: "Hold time 60 s, sodium < 1,500 mg, Body Battery ≥ 65.", zh: "撐 60 秒、鈉 < 1,500 mg、身體電量 ≥ 65。" } },
    { num: 4, ttl: { en: "First labs", zh: "首次回診" },
              body: { en: "BP, lipids, UA recheck. Adjust fish oil if LDL ↑.", zh: "血壓、血脂、尿酸複檢。LDL 上升則調魚油。" } },
    { num: 5, ttl: { en: "Optimize", zh: "優化" },
              body: { en: "Hold 90–120 s, intervals in walks, weight ~66 kg.", zh: "撐 90–120 秒、走路間歇、體重 ~66 kg。" } },
    { num: 6, ttl: { en: "Goal check", zh: "目標檢視" },
              body: { en: "65 kg target, BP 120/75, all four markers in range.", zh: "65 kg、血壓 120/75、四項指標達標。" } },
  ],

  // ===== Safety =====
  safety: [
    { ttl: { en: "Diastolic floor", zh: "舒張壓下限" },
      cls: "warn",
      body: { en: "Diastolic already 75. Some BP drugs lower both systolic and diastolic, risking diastolic < 60. Lifestyle interventions first.",
              zh: "舒張壓已 75。部分降壓藥同時降收縮與舒張壓，可能使舒張壓 < 60。生活方式介入優先。" } },
    { ttl: { en: "Uric acid 8.9 — referral pending", zh: "尿酸 8.9 — 轉診中" },
      cls: "bad",
      body: { en: "Constitutional. Avoid high-intensity exercise (lactic acid blocks UA excretion). Hydrate 500 mL pre-exercise + 200 mL/15 min during.",
              zh: "體質性。避免高強度運動（乳酸抑制尿酸排泄）。運動前 500 mL，運動中每 15 分 200 mL。" } },
    { ttl: { en: "Iron + polyphenol spacing", zh: "鐵與多酚間隔" },
      cls: "info",
      body: { en: "Hibiscus / tea polyphenols inhibit non-heme iron. Space ≥ 1 hr from red meat / iron supplements.",
              zh: "洛神花／茶的多酚抑制非血基質鐵吸收。與紅肉／鐵劑間隔 ≥ 1 小時。" } },
    { ttl: { en: "Drug interactions", zh: "藥物交互作用" },
      cls: "info",
      body: { en: "Hibiscus accelerates acetaminophen elimination; PK interactions with HCTZ, chloroquine, diclofenac.",
              zh: "洛神花加速 acetaminophen 代謝；與 HCTZ、chloroquine、diclofenac 有藥動學交互。" } },
    { ttl: { en: "Hypotension watch", zh: "低血壓警戒" },
      cls: "warn",
      body: { en: "If home BP < 110/70, drop to 1 cup hibiscus and pause citrulline.",
              zh: "若家中血壓 < 110/70，洛神花減為 1 杯，瓜胺酸暫停。" } },
    { ttl: { en: "EGCG / liver", zh: "EGCG / 肝臟" },
      cls: "bad",
      body: { en: "NOW EGCG capsule discontinued 2026-04-21 after AST 27→38; EFSA flags hepatotoxicity > 338 mg single dose.",
              zh: "2026-04-21 停用 NOW EGCG（AST 27→38）；EFSA 警示單次劑量 > 338 mg 肝毒性風險。" } },
  ],

  // ===== Tracker — last 14 days (4/21–5/4, real Garmin / cuff data) =====
  tracker: {
    // [SBP, DBP] — gaps filled with prior reading
    bp: [
      [121,75], [125,71], [126,68], [121,72], [128,74], [128,74], [122,70],
      [129,75], [127,75], [127,72], [127,72], [127,72], [127,72], [113,68],
    ],
    // 4/21–5/4 daily weight (kg)
    weight: [68.6, 68.5, 68.0, 67.9, 68.4, 68.6, 68.9, 68.4, 68.2, 67.8, 67.9, 67.8, 68.7, 69.1],
    // Garmin Sleep Score
    sleep:  [74, 69, 73, 71, 75, 64, 64, 69, 64, 71, 52, 69, 77, 77],
    // Body Battery waking
    bb:     [56, 60, 59, 34, 66, 60, 57, 57, 58, 51, 47, 41, 54, 49],
  },

  // ===== Running — started 2026-04-26 =====
  running: {
    intro: {
      en: "First run logged 2026-04-26 (DOMS appeared 4/27 at intensity 3/10). Running adds aerobic stress on top of wall sits and walks — but with UA 8.9 it must be paced carefully: lactic acid blocks uric-acid excretion, so high-intensity efforts are off the table for now.",
      zh: "首次跑步紀錄為 4/26（4/27 出現大腿 DOMS 強度 3/10）。跑步在靠牆深蹲與快走之上加入有氧負荷——但尿酸 8.9 必須謹慎控速：乳酸會抑制尿酸排泄，目前不做高強度。",
    },
    rules: {
      ttl: { en: "Three hard rules (UA 8.9 + ISH context)", zh: "三條硬規則（尿酸 8.9 + 單純收縮期高血壓背景）" },
      items: {
        en: [
          "Hydrate: 500 mL 30 min pre-run · 200 mL every 15 min during · 500 mL post — UA excretion priority.",
          "Heart-rate ceiling: Zone 2 only — talk-test pace, ≤ 70% HRmax (~135 bpm). Above this lactic acid spikes UA.",
          "DOMS rule: if soreness ≥ 4/10, switch to walk + stretch. No back-to-back run days for first 4 weeks.",
        ],
        zh: [
          "補水：跑前 30 分 500 mL · 跑中每 15 分 200 mL · 跑後 500 mL — 尿酸排泄優先。",
          "心率上限：僅 Zone 2 — 可對話配速、≤ 70% HRmax（~135 bpm）。超過則乳酸飆升、尿酸難排。",
          "DOMS 規則：肌肉痠 ≥ 4/10 改為走路 + 伸展。前 4 週不做連續兩天跑步。",
        ],
      },
    },
    // 8-week run-walk progression (Couch-to-5K adapted, Z2-capped)
    progression: [
      // [week, label{en,zh}, format{en,zh}, totalMin, runFrac]
      [1, { en: "Foundation", zh: "打底" },
          { en: "Run 1' / Walk 2' × 8", zh: "跑 1 分 / 走 2 分 × 8" }, 24, 0.33],
      [2, { en: "Foundation", zh: "打底" },
          { en: "Run 1.5' / Walk 2' × 8", zh: "跑 1.5 分 / 走 2 分 × 8" }, 28, 0.43],
      [3, { en: "Build", zh: "進展" },
          { en: "Run 2' / Walk 2' × 7", zh: "跑 2 分 / 走 2 分 × 7" }, 28, 0.50],
      [4, { en: "Deload", zh: "減量" },
          { en: "Run 2' / Walk 1.5' × 7", zh: "跑 2 分 / 走 1.5 分 × 7" }, 24.5, 0.57],
      [5, { en: "Build", zh: "進展" },
          { en: "Run 3' / Walk 2' × 6", zh: "跑 3 分 / 走 2 分 × 6" }, 30, 0.60],
      [6, { en: "Build", zh: "進展" },
          { en: "Run 5' / Walk 2' × 4", zh: "跑 5 分 / 走 2 分 × 4" }, 28, 0.71],
      [7, { en: "Push", zh: "推進" },
          { en: "Run 8' / Walk 2' × 3", zh: "跑 8 分 / 走 2 分 × 3" }, 30, 0.80],
      [8, { en: "Continuous", zh: "連續" },
          { en: "Run 20' continuous", zh: "連續跑 20 分" }, 25, 1.00],
    ],
    schedule: {
      ttl: { en: "Weekly placement — running fits between wall sits, doesn't replace them", zh: "每週安排 — 跑步插在靠牆深蹲之間，不取代深蹲" },
      head: { en: ["Day", "Primary", "Why"], zh: ["日", "主項", "原因"] },
      rows: [
        [{ en: "Mon", zh: "一" }, { en: "Run-walk Z2", zh: "跑走 Z2" },
          { en: "Fresh legs from weekend", zh: "週末恢復後雙腿狀態好" }],
        [{ en: "Tue", zh: "二" }, { en: "Wall sits + stretch", zh: "靠牆深蹲 + 伸展" },
          { en: "BP-lowering isometric — different stimulus", zh: "等長運動降壓，不同刺激" }],
        [{ en: "Wed", zh: "三" }, { en: "Brisk walk 25 min", zh: "快走 25 分" },
          { en: "Active recovery, NEAT", zh: "主動恢復、提升非運動消耗" }],
        [{ en: "Thu", zh: "四" }, { en: "Run-walk Z2", zh: "跑走 Z2" },
          { en: "≥48 h since Mon run", zh: "距週一跑步 ≥48 小時" }],
        [{ en: "Fri", zh: "五" }, { en: "Wall sits", zh: "靠牆深蹲" },
          { en: "Maintain BP protocol", zh: "維持降壓主軸" }],
        [{ en: "Sat", zh: "六" }, { en: "Long walk / family", zh: "長距離走路 / 家庭日" },
          { en: "Volume without joint stress", zh: "累積量但不傷關節" }],
        [{ en: "Sun", zh: "日" }, { en: "Stretch + leg elevation", zh: "伸展 + 抬腿" },
          { en: "Recovery for the week", zh: "全週恢復" }],
      ],
    },
    metrics: {
      ttl: { en: "Watch these on your runs", zh: "跑步時觀察這些" },
      items: [
        ["HR avg", "≤ 135 bpm (Z2)", "var(--heart)"],
        ["Cadence", "170–180 spm", "var(--metabolic)"],
        ["Pace", { en: "comfortable, can talk", zh: "舒服、能說話" }, "var(--sleep)"],
        ["Post-run UA signs", { en: "no toe pain at 24-48 h", zh: "24-48h 無拇趾痛" }, "var(--uric)"],
      ],
    },
  },

  // ===== OSA POSA Trial (5/5–5/8) =====
  osa: {
    intro: {
      en: "SpO2 desaturation events have been escalating: T90 ≥ 10% on 4/29, 4/30, and 5/4 (peak 18.4% — severe). 5/4 attributed to dual stack: high-sodium meal 36–40 h prior + 2-night REM debt rebound. Positional therapy (POSA) trial runs 5/5–5/8 in parallel with PSG booking.",
      zh: "SpO2 desat 事件持續升級：4/29、4/30、5/4 T90 ≥ 10%（高峰 18.4% — 重度）。5/4 歸因於雙因子疊加：36–40h 前高鈉餐 + 連兩晚 REM 負債反彈。體位治療試驗（POSA）5/5–5/8 與 PSG 預約並行。",
    },
    intervention: {
      ttl: { en: "Level-1 intervention", zh: "Level 1 介入" },
      items: {
        en: [
          "Head of bed elevated 20–30° (pillow / towel roll).",
          "Body pillow in front, firm pillow behind back to block supine.",
          "If supine return < 5 min → upgrade to tennis-ball shirt.",
        ],
        zh: [
          "床頭抬高 20–30°（疊枕 / 毛巾捲）。",
          "身前抱長抱枕，背後放扎實小枕頭擋翻仰。",
          "若 5 分鐘內翻仰 → 升級網球療法。",
        ],
      },
    },
    readout: {
      ttl: { en: "Decision criteria — averaged over 4 nights", zh: "判讀準則 — 4 晚平均" },
      rows: [
        ["≤ 5%", { en: "Strong POSA — upgrade to SPT vibration device", zh: "強烈 POSA 反應 — 升級 SPT 震動裝置" }, "ok"],
        ["5–10%", { en: "Moderate — reinforce elevation / tennis-ball", zh: "中度 — 加強床頭抬高 / 網球" }, "warn"],
        ["> 10%", { en: "Not POSA-driven — PSG → CPAP/MAD", zh: "非 POSA 主導 — PSG → CPAP/MAD" }, "bad"],
      ],
    },
  },
};
