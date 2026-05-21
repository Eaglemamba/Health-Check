/* ====== Anatomical concept — data (full analyzer mapping) ====== */
window.ANAT = {
  organs: {
    brain: {
      num: "01",
      name: { en: "Brain · Hypothalamus", zh: "腦 · 下視丘" },
      tag: "sleep",
      color: "#5e5ce6", colorSoft: "#eae9ff",
      lede: {
        en: "Sleep architecture, sympathetic tone, thyroid axis. The upstream organ — if it isn't repaired, everything else recovers at half power.",
        zh: "睡眠結構、交感神經張力、甲狀腺軸。最上游的器官——如果不修復，其他器官只能用一半的恢復力。",
      },
      summary: [
        ["State",  { en: "Sleep Score 77 · Body Battery 49", zh: "睡眠分數 77 · 身體電量 49" }],
        ["Flag",   { en: "Wakes 02-04 · nocturia", zh: "凌晨 02-04 醒來 · 夜尿" }],
      ],
      indicators: [
        { id: "tsh",   label: "TSH",          labelZh: "甲狀腺促激素",   ref: "0.27 – 4.20 uIU/mL" },
        { id: "hscrp", label: "hsCRP",        labelZh: "超敏 C-反應蛋白", ref: "< 0.1 mg/dL low CV risk" },
      ],
    },
    eyes: {
      num: "02",
      name: { en: "Eyes", zh: "眼睛" },
      tag: "weight",
      color: "#a374e6", colorSoft: "#ede2fa",
      lede: {
        en: "Visual acuity and intraocular pressure — early window for glaucoma, metabolic & vascular damage.",
        zh: "視力與眼壓——青光眼、代謝、血管損傷的早期觀察窗。",
      },
      summary: [
        ["Check", { en: "Annual ophthalmology exam", zh: "每年眼科檢查一次" }],
      ],
      indicators: [
        { id: "va_l", label: "Visual Acuity (Left)",   labelZh: "視力（左）", ref: "≥ 1.0" },
        { id: "va_r", label: "Visual Acuity (Right)",  labelZh: "視力（右）", ref: "≥ 1.0" },
        { id: "iop_l",label: "IOP Left",                labelZh: "眼壓（左）", ref: "10 – 21 mmHg" },
        { id: "iop_r",label: "IOP Right",               labelZh: "眼壓（右）", ref: "10 – 21 mmHg" },
      ],
    },
    lungs: {
      num: "03",
      name: { en: "Lungs · Airway", zh: "肺 · 呼吸道" },
      tag: "water",
      color: "#00b8d4", colorSoft: "#d4f4fa",
      lede: {
        en: "Where SpO2 dips happen. Tongue-base collapse and rostral fluid shift drive the OSA events.",
        zh: "SpO2 desat 事件發生的地方。舌根後墜與下肢液體往上回流是 OSA 事件主因。",
      },
      summary: [
        ["Flag", { en: "T90 ≥ 10% on 3 of last 7 nights", zh: "近 7 晚有 3 晚 T90 ≥ 10%" }],
      ],
      indicators: [
        { id: "chest_xray", label: "Chest X-ray", labelZh: "胸部 X 光", ref: "Normal" },
        { id: "spo2",       label: "SpO2 (Garmin night)", labelZh: "夜間血氧", ref: "Avg ≥ 95% · no dips < 88%" },
      ],
    },
    heart: {
      num: "04",
      name: { en: "Heart & Vessels", zh: "心 · 血管" },
      tag: "heart",
      color: "#ff375f", colorSoft: "#ffe5ec",
      lede: {
        en: "ISH (Isolated Systolic Hypertension) + borderline lipids. Lifestyle stack first — diastolic 71 means avoid over-dipping.",
        zh: "單純收縮期高血壓 + 邊緣血脂。生活方式介入優先——舒張壓 71，避免過度下降。",
      },
      summary: [
        ["BP avg",  { en: "122 / 71 mmHg (W17)", zh: "122 / 71 mmHg（W17）" }],
        ["Goal",    { en: "SBP < 125 by month 6", zh: "第 6 月 SBP < 125" }],
      ],
      indicators: [
        { id: "bp_systolic",  label: "Systolic BP",        labelZh: "收縮壓",       ref: "< 120 mmHg" },
        { id: "bp_diastolic", label: "Diastolic BP",       labelZh: "舒張壓",       ref: "< 80 mmHg" },
        { id: "pulse",        label: "Pulse",              labelZh: "心率",         ref: "60 – 100 bpm" },
        { id: "ecg",          label: "ECG",                labelZh: "心電圖",       ref: "Normal sinus" },
        { id: "abi",          label: "ABI",                labelZh: "踝臂指數",     ref: "0.9 – 1.3" },
        { id: "pwv",          label: "PWV",                labelZh: "脈波速度",     ref: "< 1400 cm/s" },
        { id: "tc",           label: "Total Cholesterol",  labelZh: "總膽固醇",     ref: "< 200 mg/dL" },
        { id: "tg",           label: "Triglycerides",      labelZh: "三酸甘油酯",   ref: "< 150 mg/dL" },
        { id: "ldl",          label: "LDL",                labelZh: "低密度脂蛋白", ref: "< 130 mg/dL" },
        { id: "hdl",          label: "HDL",                labelZh: "高密度脂蛋白", ref: "> 40 (M) / > 50 (F)" },
        { id: "tc_hdl_ratio", label: "TC/HDL Ratio",       labelZh: "TC/HDL 比",   ref: "< 5.0" },
        { id: "hscrp",        label: "hsCRP",              labelZh: "超敏 CRP",     ref: "< 0.1 mg/dL low CV" },
        { id: "hb",           label: "Hemoglobin",         labelZh: "血紅素",       ref: "13 – 18 g/dL (M)" },
        { id: "rbc",          label: "RBC",                labelZh: "紅血球",       ref: "4.5 – 5.7 (M)" },
        { id: "ht",           label: "Hematocrit",         labelZh: "血容比",       ref: "40 – 54% (M)" },
        { id: "wbc",          label: "WBC",                labelZh: "白血球",       ref: "4.0 – 10.0" },
        { id: "platelets",    label: "Platelets",          labelZh: "血小板",       ref: "140 – 450" },
        { id: "mcv",          label: "MCV",                labelZh: "MCV",          ref: "80 – 98 fL" },
        { id: "mch",          label: "MCH",                labelZh: "MCH",          ref: "27 – 32 pg" },
        { id: "mchc",         label: "MCHC",               labelZh: "MCHC",         ref: "32 – 36 g/dL" },
        { id: "rdw",          label: "RDW",                labelZh: "紅血球分佈寬度", ref: "11.5 – 14.5%" },
        { id: "neutrophils",  label: "Neutrophils %",      labelZh: "嗜中性球",     ref: "40 – 75%" },
        { id: "lymphocytes",  label: "Lymphocytes %",      labelZh: "淋巴球",       ref: "20 – 40%" },
        { id: "monocytes",    label: "Monocytes %",        labelZh: "單核球",       ref: "2 – 10%" },
        { id: "eosinophils",  label: "Eosinophils %",      labelZh: "嗜酸性球",     ref: "0 – 6%" },
        { id: "basophils",    label: "Basophils %",        labelZh: "嗜鹼性球",     ref: "0 – 2%" },
      ],
    },
    liver: {
      num: "05",
      name: { en: "Liver", zh: "肝臟" },
      tag: "weight",
      color: "#ff9f0a", colorSoft: "#fff1d6",
      lede: {
        en: "Where lipids are made and where EGCG can be hepatotoxic. AST 27→38 after EGCG — capsule discontinued 4/21.",
        zh: "脂質合成處，也是 EGCG 可能造成肝毒性的地方。AST 27→38 後 4/21 停用 EGCG。",
      },
      summary: [
        ["Watch", { en: "AST 38 · recheck month 4", zh: "AST 38 · 第 4 月複檢" }],
      ],
      indicators: [
        { id: "ast",              label: "AST (SGOT)",         labelZh: "AST / GOT",    ref: "≤ 40 U/L (M)" },
        { id: "alt",              label: "ALT (SGPT)",         labelZh: "ALT / GPT",    ref: "≤ 40 U/L (M)" },
        { id: "alp",              label: "ALP",                labelZh: "鹼性磷酸酶",   ref: "40 – 129 U/L" },
        { id: "direct_bilirubin", label: "Direct Bilirubin",   labelZh: "直接膽紅素",   ref: "≤ 0.40 mg/dL" },
        { id: "total_bilirubin",  label: "Total Bilirubin",    labelZh: "總膽紅素",     ref: "≤ 1.20 mg/dL" },
        { id: "hbsag",            label: "HBsAg",              labelZh: "B肝表面抗原",  ref: "< 0.90 negative" },
        { id: "afp",              label: "AFP",                labelZh: "甲型胎兒蛋白", ref: "≤ 7.0 ng/mL" },
        { id: "ultrasound",       label: "Abdominal U/S",      labelZh: "腹部超音波",   ref: "Normal · no fatty liver" },
      ],
    },
    pancreas: {
      num: "06",
      name: { en: "Pancreas", zh: "胰臟" },
      tag: "metabolic",
      color: "#ffb84d", colorSoft: "#fff0d6",
      lede: {
        en: "Glycemic control. Fiber + the post-lunch walk are your biggest levers — both flatten the curve before the pancreas has to compensate.",
        zh: "血糖調控。纖維與餐後快走是最大的兩個槓桿——都能在胰臟代償之前把血糖曲線壓平。",
      },
      summary: [
        ["State", { en: "HbA1c 5.9 → 5.7 target", zh: "HbA1c 5.9 → 目標 5.7" }],
      ],
      indicators: [
        { id: "glucose", label: "Fasting Glucose", labelZh: "空腹血糖", ref: "70 – 100 mg/dL" },
        { id: "hba1c",   label: "HbA1c",           labelZh: "糖化血色素", ref: "< 5.7% normal · 5.7–6.4 pre-DM" },
      ],
    },
    kidneys: {
      num: "07",
      name: { en: "Kidneys & Bladder", zh: "腎臟 · 膀胱" },
      tag: "uric",
      color: "#bf5af2", colorSoft: "#f3e3fb",
      lede: {
        en: "Constitutional hyperuricemia. Lactic acid competes with urate at the tubular transporter — high-intensity exercise is off until UA normalizes.",
        zh: "體質性高尿酸。乳酸與尿酸鹽在腎小管轉運子競爭排泄——高強度運動暫停直到尿酸正常。",
      },
      summary: [
        ["State",  { en: "UA 8.9 mg/dL · neph referral", zh: "尿酸 8.9 · 腎臟科轉診中" }],
      ],
      indicators: [
        { id: "bun",        label: "BUN",            labelZh: "尿素氮",       ref: "6 – 23 mg/dL" },
        { id: "uric_acid",  label: "Uric Acid",      labelZh: "尿酸",         ref: "≤ 7.0 (M) / 6.0 (F)" },
        { id: "creatinine", label: "Creatinine",     labelZh: "肌酸酐",       ref: "0.7 – 1.2 mg/dL (M)" },
        { id: "egfr",       label: "eGFR",           labelZh: "腎絲球過濾率", ref: "≥ 90 mL/min" },
        { id: "urine_sg",       label: "Urine SG",       labelZh: "尿液比重",     ref: "1.003 – 1.030" },
        { id: "urine_ph",       label: "Urine pH",       labelZh: "尿液 pH",      ref: "5.0 – 8.0" },
        { id: "urine_protein",  label: "Urine Protein",  labelZh: "尿蛋白",       ref: "Negative" },
        { id: "urine_glucose",  label: "Urine Glucose",  labelZh: "尿糖",         ref: "Negative" },
        { id: "urine_ketones",  label: "Urine Ketones",  labelZh: "尿酮體",       ref: "Negative" },
        { id: "urine_blood",    label: "Urine Blood",    labelZh: "尿潛血",       ref: "Negative" },
        { id: "urine_urobilinogen", label: "Urobilinogen", labelZh: "尿膽素原",   ref: "≤ 1.0 mg/dL" },
        { id: "psa",        label: "PSA (male)",     labelZh: "攝護腺特異抗原", ref: "< 4.0 ng/mL" },
      ],
    },
    gut: {
      num: "08",
      name: { en: "Gut · Lower GI", zh: "腸道 · 下消化道" },
      tag: "metabolic",
      color: "#30d158", colorSoft: "#ddf7e2",
      lede: {
        en: "Where bile acids meet psyllium and where most polyphenols are absorbed. The lipid lever you can pull at every meal.",
        zh: "膽汁酸遇到洋車前子、多酚被吸收的地方。每餐都能拉動的血脂槓桿。",
      },
      summary: [
        ["Daily", { en: "Psyllium 5g × 2 · Na < 1.5g", zh: "洋車前子 5g × 2 · 鈉 < 1.5g" }],
      ],
      indicators: [
        { id: "stool_ob", label: "Fecal Occult Blood", labelZh: "糞便潛血",     ref: "< 30 ng/mL" },
        { id: "cea",      label: "CEA",                labelZh: "癌胚抗原",     ref: "< 5.0 ng/mL" },
        { id: "ca199",    label: "CA-199",             labelZh: "胰腺腫瘤標誌", ref: "≤ 39 U/mL" },
      ],
    },
  },

  // Body-composition / vital signs — float around the silhouette
  bodyComp: [
    { id: "bmi",          label: "BMI",           labelZh: "BMI",       ref: "18.5 – 24.9",       pos: "tl" },
    { id: "body_fat",     label: "Body Fat",      labelZh: "體脂率",     ref: "17 – 23% (M)",     pos: "bl" },
    { id: "visceral_fat", label: "Visceral Fat",  labelZh: "內臟脂肪",   ref: "≤ 10",              pos: "tr" },
    { id: "waist",        label: "Waist",         labelZh: "腰圍",       ref: "< 90 cm (M)",       pos: "br" },
    { id: "temperature",  label: "Temperature",   labelZh: "體溫",       ref: "36.0 – 37.5 °C",    pos: "tc" },
    { id: "bone_density", label: "Bone Density",  labelZh: "骨密度",     ref: "T-score > −1",      pos: "bc" },
  ],

  // Chips that target organs
  chips: {
    supplements: [
      { id: "omega",     name: "Omega-3 rTG",   nameZh: "魚油",       organ: "heart" },
      { id: "hibiscus",  name: "Hibiscus tea",  nameZh: "洛神花",     organ: "heart" },
      { id: "citrulline",name: "L-Citrulline",  nameZh: "瓜胺酸",     organ: "heart" },
      { id: "psyllium",  name: "Psyllium husk", nameZh: "洋車前子",   organ: "gut" },
      { id: "d3k2",      name: "D3 + K2",       nameZh: "D3 + K2",   organ: "heart" },
      { id: "mg",        name: "Mg Glycinate",  nameZh: "甘胺酸鎂",   organ: "brain" },
      { id: "cherry",    name: "Tart cherry",   nameZh: "酸櫻桃",     organ: "kidneys" },
      { id: "whey",      name: "Whey protein",  nameZh: "乳清蛋白",   organ: "gut" },
      { id: "pumpkin",   name: "Pumpkin seeds", nameZh: "南瓜籽",     organ: "brain" },
    ],
    practices: [
      { id: "wallsit",   name: "Wall sits 4×2′",      nameZh: "靠牆深蹲",         organ: "heart" },
      { id: "run",       name: "Run-walk Z2",         nameZh: "Z2 跑走",          organ: "heart" },
      { id: "walk",      name: "Post-lunch walk",     nameZh: "餐後快走",         organ: "pancreas" },
      { id: "sidesleep", name: "Side sleep + 20°",    nameZh: "側睡 + 床頭抬高",   organ: "lungs" },
      { id: "legelev",   name: "Leg elevation 20:00", nameZh: "20:00 抬腿",       organ: "lungs" },
      { id: "cutoff",    name: "Fluid cutoff 17:00",  nameZh: "17:00 停水",       organ: "kidneys" },
      { id: "lowna",     name: "Sodium < 1.5g",       nameZh: "鈉 < 1.5g",        organ: "gut" },
      { id: "478",       name: "4-7-8 breathing",     nameZh: "4-7-8 呼吸",       organ: "brain" },
      { id: "fiber",     name: "Fiber 30g/day",       nameZh: "纖維 30g/天",      organ: "pancreas" },
    ],
  },
};
