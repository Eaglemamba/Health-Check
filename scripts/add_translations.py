#!/usr/bin/env python3
"""Insert textZh translations into all PLANS and MERGED_ACTIONS items in analyzer.html."""
import re, sys

FILE = '/Users/kuoli-hung/Health-Check/analyzer.html'

# Map: exact English text → Chinese translation
TRANSLATIONS = {
    # ── body_comp ──
    'Create 500 kcal/day deficit (target ~0.5 kg/week loss) — 5-10% body weight loss reverses fatty liver and significantly improves all metabolic markers':
        '每日減少 500 大卡（目標每週減重約 0.5 kg）— 體重減少 5-10% 可逆轉脂肪肝，顯著改善所有代謝指標',
    'DASH diet pattern: vegetables 5+ servings, fruits 2-3, whole grains, lean protein, low-fat dairy — proven to reduce BP, LDL, and body fat simultaneously':
        'DASH 飲食模式：蔬菜 5+ 份、水果 2-3 份、全穀類、瘦蛋白、低脂乳品 — 已證實可同步降低血壓、LDL 及體脂',
    'Protein 1.2-1.6 g/kg/day to preserve lean mass during caloric deficit — distribute across 3 meals':
        '每日蛋白質 1.2-1.6 g/kg，以維持熱量限制期間的肌肉量 — 分配於三餐攝取',
    'Eliminate sugar-sweetened beverages and limit added sugars to < 25g/day — reduces visceral fat, TG, and hepatic fat':
        '戒除含糖飲料，每日添加糖控制在 25g 以下 — 降低內臟脂肪、三酸甘油酯及肝臟脂肪',
    'Front-load calories: larger breakfast/lunch, lighter dinner — improves insulin sensitivity and reduces overnight fat storage':
        '熱量前置：早午餐多、晚餐少 — 改善胰島素敏感性，減少夜間脂肪囤積',
    'Mindful eating: eat slowly, stop at 80% full, use smaller plates — reduces caloric intake 10-15% without counting':
        '正念飲食：細嚼慢嚥、八分飽停止、使用小盤子 — 無需計算卡路里即可減少攝取 10-15%',
    '150 min/week moderate aerobic exercise (brisk walking, cycling) — start at current fitness level and increase 10% per week':
        '每週中等強度有氧運動 150 分鐘（快走、騎車）— 從目前體能水平開始，每週增加 10%',
    'Resistance training 2x/week — preserves muscle during weight loss, increases resting metabolic rate':
        '每週阻力訓練 2 次 — 減重期間保留肌肉，提升基礎代謝率',
    'Daily step goal: 8,000-10,000 steps — each 1,000 steps above 4,000 reduces mortality risk':
        '每日目標步數：8,000-10,000 步 — 超過 4,000 步後，每增加 1,000 步均可降低死亡風險',
    'NEAT (Non-Exercise Activity Thermogenesis): standing desk, stairs, walking meetings — adds 200-500 kcal/day expenditure':
        '非運動活動熱量消耗（NEAT）：站立辦公、走樓梯、邊走邊開會 — 每日額外消耗 200-500 大卡',
    'Sleep 7-8 hours — sleep deprivation increases ghrelin (hunger hormone), cortisol, and insulin resistance; 3.5x hypertension risk with < 6h':
        '睡眠 7-8 小時 — 睡眠不足會增加飢餓素、皮質醇及胰島素阻抗；不足 6 小時高血壓風險上升 3.5 倍',
    'Stress management: chronic cortisol elevation promotes visceral fat storage and insulin resistance':
        '壓力管理：長期皮質醇升高會促進內臟脂肪囤積及胰島素阻抗',
    'Weekly official weigh-in (Saturday AM, post-void, fasted) — track trend, not daily fluctuations':
        '每週正式量體重（週六早晨、排尿後、進食前；週末大餐前）— 追蹤趨勢，不糾結單日波動',
    'Body composition analysis every 3 months — track fat mass vs lean mass, not just weight':
        '每 3 個月進行一次體組成分析 — 追蹤體脂量與肌肉量，而非僅看體重',
    'If BMI > 27 with comorbidities or > 30: discuss pharmacotherapy (GLP-1 agonists) with physician':
        '若 BMI > 27 合併共病症，或 BMI > 30：與醫師討論藥物治療（GLP-1 受體促效劑）',

    # ── bp ──
    'Wall sits (isometric exercise): 4 x 2-min holds, 2-min rest between, 3x/week — 2023 BJSM meta-analysis (270 RCTs): most effective exercise type for BP reduction':
        '靠牆深蹲（等長收縮運動）：每次 4 組 × 2 分鐘，組間休息 2 分鐘，每週 3 次 — 2023 年 BJSM 統合分析（270 項 RCT）：降血壓效果最佳的運動類型',
    '2024 RCT confirmed wall sits reduce SBP by 12.9 mmHg in 8 weeks — superior to aerobic, resistance, and combined training for ISH':
        '2024 年 RCT 確認靠牆深蹲 8 週可降低收縮壓 12.9 mmHg — 優於有氧、阻力及複合訓練（針對單純收縮期高血壓）',
    '30 min brisk walking daily — aerobic exercise reduces SBP 5-8 mmHg independently':
        '每日快走 30 分鐘 — 有氧運動可單獨降低收縮壓 5-8 mmHg',
    'Form critical: back flat against wall, thighs at target angle (start shallow, progress), breathe continuously — never hold breath':
        '動作要領：背部貼牆、大腿保持目標角度（初期較淺再漸進），全程持續呼吸 — 切勿憋氣',
    'DASH diet: high potassium (bananas, sweet potatoes, spinach), low sodium < 2,300 mg/day — reduces SBP 8-14 mmHg':
        'DASH 飲食：高鉀（香蕉、地瓜、菠菜），低鈉每日 < 2,300 mg — 可降低收縮壓 8-14 mmHg',
    'Omega-3 rTG 2g/day — combined with DASH: SBP -14.7 mmHg (combined effect)':
        'Omega-3 再酯化三酸甘油酯型每日 2g — 與 DASH 合併使用：收縮壓下降 14.7 mmHg（聯合效果）',
    'Limit caffeine to < 400mg/day and avoid 2 hours before BP measurement':
        '每日咖啡因控制在 400mg 以下，量血壓前 2 小時避免攝取',
    'Weight loss: each 1 kg lost reduces SBP ~1 mmHg':
        '體重控制：每減少 1 kg 可降低收縮壓約 1 mmHg',
    'Omega-3 Fish Oil (rTG form) 4 capsules/day — EPA+DHA 1,920mg for BP + lipid support':
        'Omega-3 魚油（rTG 型）每日 4 粒 — EPA+DHA 1,920mg，用於血壓及血脂管理',
    'Magnesium glycinate 200-400mg at bedtime — mild BP reduction + sleep quality improvement':
        '甘胺酸鎂 200-400mg 睡前服用 — 輕度降血壓 + 改善睡眠品質',
    'Sleep repair priority: hypertension risk 3.5x with < 6 hours sleep — cortisol/sympathetic activation pathway':
        '睡眠修復優先：睡不足 6 小時高血壓風險增加 3.5 倍 — 皮質醇／交感神經激活路徑',
    'Home BP monitoring 2x/week (seated, after 5 min rest, use 2nd reading) — establishes true baseline vs white coat effect':
        '每週在家量血壓 2 次（坐姿、休息 5 分鐘後、取第二次讀數）— 建立真實基線，排除白袍效應',
    '4-7-8 breathing technique: inhale 4s, hold 7s, exhale 8s — acute parasympathetic activation reduces BP':
        '4-7-8 呼吸法：吸氣 4 秒、憋氣 7 秒、吐氣 8 秒 — 急性副交感神經激活，即時降低血壓',
    'If SBP persistently > 140 despite 3 months lifestyle: discuss antihypertensive medication with physician':
        '若生活介入 3 個月後收縮壓仍持續 > 140：與醫師討論降壓藥物',
    'Annual kidney function check (eGFR, creatinine) — hypertension damages kidneys silently':
        '每年檢查腎功能（eGFR、肌酸酐）— 高血壓會無聲地損傷腎臟',

    # ── ldl ──
    'Oat beta-glucan 3g/day (40-50g dry oats or oat bran) — clinically proven LDL reduction 5-10%':
        '每日燕麥 β-葡聚糖 3g（40-50g 乾燕麥片或燕麥麩）— 臨床實證可降低 LDL 5-10%',
    'Replace saturated fats (butter, red meat fat, palm oil) with unsaturated fats (olive oil, avocado, nuts) — shifts LDL production':
        '以不飽和脂肪（橄欖油、酪梨、堅果）取代飽和脂肪（奶油、紅肉脂肪、棕櫚油）— 改變 LDL 合成路徑',
    'Plant sterols/stanols 2g/day (fortified margarine or supplement) — blocks cholesterol absorption in gut, LDL -6-10%':
        '每日植物固醇／甾烷醇 2g（強化人造奶油或補充劑）— 阻斷腸道膽固醇吸收，LDL 下降 6-10%',
    'Increase soluble fiber: psyllium 5-10g, beans, apples, citrus — each gram of soluble fiber lowers LDL ~1-2 mg/dL':
        '增加可溶性膳食纖維：車前子 5-10g、豆類、蘋果、柑橘 — 每克可溶性纖維可降低 LDL 約 1-2 mg/dL',
    'Soy protein 25g/day (tofu, edamame, soy milk) — modest LDL reduction 3-5%':
        '每日大豆蛋白 25g（豆腐、毛豆、豆漿）— 可輕度降低 LDL 3-5%',
    'Eliminate trans fats entirely — check labels for "partially hydrogenated oils"':
        '完全戒除反式脂肪 — 查看標籤，避免「部分氫化油脂」',
    '150 min/week moderate aerobic exercise — increases LDL receptor expression, LDL -5-8%':
        '每週中等強度有氧運動 150 分鐘 — 增加 LDL 受體表達，降低 LDL 5-8%',
    'Resistance training 2x/week — improves overall lipid profile independent of weight loss':
        '每週阻力訓練 2 次 — 不依賴減重，獨立改善整體血脂',
    'Omega-3 rTG form 4 caps/day (EPA+DHA 1,920mg) — primarily lowers TG but supports overall lipid metabolism':
        'Omega-3 再酯化三酸甘油酯型每日 4 粒（EPA+DHA 1,920mg）— 主要降低三酸甘油酯，同時支持整體血脂代謝',
    'Consider bergamot extract 500mg/day — shown to lower LDL 20-30% in some RCTs (consult physician)':
        '考慮佛手柑萃取物每日 500mg — 部分 RCT 顯示可降低 LDL 20-30%（請先諮詢醫師）',
    'Recheck lipid panel in 3 months — establish whether lifestyle intervention is sufficient':
        '3 個月後複查血脂四項 — 評估生活介入是否足夠',
    'At LDL > 160 with additional risk factors (elevated TC/HDL ratio, hsCRP): calculate 10-year CV risk score; discuss statin with physician':
        'LDL > 160 且合併其他風險因子（TC/HDL 比偏高、hsCRP 升高）：計算 10 年心血管風險，與醫師討論他汀類藥物',
    'If LDL > 190 mg/dL: strong indication for statin regardless of other risk factors (ACC/AHA guidelines)':
        '若 LDL > 190 mg/dL：不論其他風險因子，強烈建議使用他汀類藥物（ACC/AHA 指引）',

    # ── tg ──
    'Reduce refined carbohydrates and added sugars — fructose and sucrose are directly converted to TG in the liver':
        '減少精製碳水化合物及添加糖 — 果糖與蔗糖在肝臟直接轉化為三酸甘油酯',
    'Increase omega-3 rich fish (salmon, mackerel, sardines) 2-3x/week — EPA/DHA suppress hepatic TG synthesis':
        '每週增加富含 Omega-3 的魚類（鮭魚、鯖魚、沙丁魚）2-3 次 — EPA/DHA 抑制肝臟三酸甘油酯合成',
    'Limit alcohol — even moderate intake raises TG via hepatic lipogenesis':
        '限制飲酒 — 即使適量飲酒也會透過肝臟脂質合成升高三酸甘油酯',
    'Mediterranean diet pattern: olive oil, nuts, vegetables, whole grains, legumes — TG reduction 10-15%':
        '地中海飲食模式：橄欖油、堅果、蔬菜、全穀類、豆類 — 三酸甘油酯下降 10-15%',
    'Avoid large carbohydrate-heavy meals — spread intake across meals to prevent postprandial TG spikes':
        '避免大量高碳水化合物餐食 — 分次攝取，防止餐後三酸甘油酯急升',
    'Omega-3 rTG 2g/day therapeutic dose — TG reduction 25-30% at this dose (REDUCE-IT trial context)':
        'Omega-3 rTG 型每日 2g 治療劑量 — 此劑量可降低三酸甘油酯 25-30%（REDUCE-IT 試驗背景）',
    'Combined DASH + Omega-3 protocol: LDL -31.7, TG -45.3, SBP -14.7 (combined evidence from index.html plan)':
        'DASH + Omega-3 聯合方案：LDL -31.7、TG -45.3、收縮壓 -14.7（聯合實證數據）',
    'Regular aerobic exercise 150 min/week — TG reduction 15-20% via increased lipoprotein lipase activity':
        '每週規律有氧運動 150 分鐘 — 透過提升脂蛋白脂酶活性，降低三酸甘油酯 15-20%',
    'Post-meal walking 15-20 min — reduces postprandial TG surge':
        '餐後步行 15-20 分鐘 — 降低餐後三酸甘油酯急升',
    'If TG > 500 mg/dL: risk of pancreatitis — requires medical intervention (fibrates or prescription omega-3)':
        '若三酸甘油酯 > 500 mg/dL：有胰臟炎風險 — 需要醫療介入（貝特類藥物或處方 Omega-3）',
    'Recheck fasting lipid panel in 2-3 months — TG responds faster than LDL to lifestyle changes':
        '2-3 個月後複查空腹血脂 — 三酸甘油酯對生活改變的反應快於 LDL',

    # ── uric_acid ──
    'Limit high-purine foods: organ meats, shellfish, red meat, anchovies — reduce to < 2 servings/week':
        '限制高嘌呤食物：內臟類、甲殼海鮮、紅肉、鯷魚 — 每週控制在 2 份以下',
    'Avoid fructose-sweetened beverages — fructose metabolism directly generates uric acid via purine degradation':
        '避免含果糖飲料 — 果糖代謝透過嘌呤降解直接生成尿酸',
    'Increase low-fat dairy — casein and lactalbumin promote uric acid excretion':
        '增加低脂乳製品 — 酪蛋白與乳白蛋白可促進尿酸排泄',
    'Cherries and dark berries — anthocyanins inhibit xanthine oxidase (same target as allopurinol)':
        '櫻桃及深色漿果 — 花青素可抑制黃嘌呤氧化酶（與別嘌醇作用靶點相同）',
    'Limit alcohol, especially beer (contains purines + inhibits renal uric acid excretion)':
        '限制飲酒，尤其是啤酒（含嘌呤 + 抑制腎臟尿酸排泄）',
    'Coffee 2-3 cups/day — associated with lower uric acid levels (epidemiological data)':
        '每日咖啡 2-3 杯 — 與尿酸水平降低相關（流行病學數據）',
    'Hydration 2.5L/day minimum — increases renal uric acid clearance; complete main volume before 17:00':
        '每日至少喝水 2.5 公升 — 提升腎臟尿酸清除率；主要飲水量於 17:00 前完成',
    'Alkalinize urine with citrus water (lemon/lime) — uric acid is more soluble in alkaline urine':
        '以柑橘水（檸檬、萊姆）鹼化尿液 — 尿酸在鹼性尿液中溶解度更高',
    'Tart cherry extract — 2025 RCT: uric acid -37.4%, CRP -23% with daily supplementation':
        '酸櫻桃萃取物 — 2025 年 RCT：每日補充可降低尿酸 37.4%、CRP 23%',
    'Vitamin C 500mg/day — promotes renal uric acid excretion; modest reduction ~0.5 mg/dL':
        '維生素 C 每日 500mg — 促進腎臟尿酸排泄；輕度降低約 0.5 mg/dL',
    'Goji berry tea 20g/day — traditional use for kidney support; anti-inflammatory properties':
        '枸杞茶每日 20g — 傳統用於腎臟保健；具抗發炎特性',
    'If uric acid > 9.0 mg/dL or recurrent gout: discuss allopurinol or febuxostat with physician — pharmacotherapy indicated':
        '若尿酸 > 9.0 mg/dL 或反覆發作痛風：與醫師討論別嘌醇或非布索坦 — 需藥物治療',
    'Monitor kidney function (eGFR, creatinine) — chronic hyperuricemia can cause urate nephropathy':
        '監測腎功能（eGFR、肌酸酐）— 長期高尿酸血症可導致尿酸鹽腎病',
    'Recheck uric acid in 3 months — gradual reduction preferred (rapid drops can paradoxically trigger gout)':
        '3 個月後複查尿酸 — 建議緩慢下降（驟降反而可能誘發痛風）',
    'Avoid rapid weight loss (> 1.5 kg/week) — increases uric acid via purine release from tissue breakdown + gout flare risk':
        '避免快速減重（每週 > 1.5 kg）— 組織分解釋放嘌呤會升高尿酸，增加痛風發作風險',

    # ── hba1c ──
    'Low glycemic index (GI) diet — replace white rice/bread with brown rice, whole grain, sweet potatoes; reduces postprandial glucose spikes':
        '低升糖指數（GI）飲食 — 以糙米、全穀、地瓜取代白飯白麵包；降低餐後血糖急升',
    'Fiber 25-30g/day — slows glucose absorption; each 10g fiber increase reduces HbA1c ~0.2%':
        '每日膳食纖維 25-30g — 減緩葡萄糖吸收；每增加 10g 纖維可降低 HbA1c 約 0.2%',
    'Chromium-rich foods (broccoli, barley, oats) — chromium picolinate improves insulin sensitivity':
        '富含鉻的食物（花椰菜、大麥、燕麥）— 吡啶甲酸鉻可改善胰島素敏感性',
    'Reduce refined carbohydrates and added sugars — direct drivers of glucose excursion and insulin demand':
        '減少精製碳水化合物及添加糖 — 這是血糖波動及胰島素需求的直接驅動因素',
    'Apple cider vinegar 1-2 tbsp before meals — may reduce postprandial glucose by 20-30% (small studies)':
        '餐前蘋果醋 1-2 湯匙 — 可能降低餐後血糖 20-30%（小型研究）',
    '150 min/week moderate exercise — DPP study protocol; improves insulin sensitivity within 1 week of starting':
        '每週中等強度運動 150 分鐘 — DPP 研究方案；開始後 1 週內即可改善胰島素敏感性',
    'Resistance training 2-3x/week — increases glucose uptake by muscles independent of insulin (GLUT-4 translocation)':
        '每週阻力訓練 2-3 次 — 透過 GLUT-4 轉位增加肌肉葡萄糖攝取，不依賴胰島素',
    'Post-meal walking 15-20 min — reduces 2-hour postprandial glucose by 15-25%':
        '餐後步行 15-20 分鐘 — 降低餐後 2 小時血糖 15-25%',
    '5-7% body weight loss — the most impactful single intervention; DPP goal; reverses insulin resistance':
        '減重 5-7% — 最有效的單一介入；DPP 目標；可逆轉胰島素阻抗',
    'Sleep 7-8 hours — sleep deprivation directly impairs glucose tolerance and insulin sensitivity':
        '睡眠 7-8 小時 — 睡眠不足直接損害葡萄糖耐受性及胰島素敏感性',
    'Stress reduction — cortisol raises blood glucose via hepatic gluconeogenesis':
        '壓力管理 — 皮質醇透過肝糖異生升高血糖',
    'Annual HbA1c monitoring — track trajectory; if rising toward 6.5%, intensify intervention or discuss metformin':
        '每年監測 HbA1c — 追蹤趨勢；若接近 6.5%，加強介入或與醫師討論二甲雙胍',
    'Consider OGTT (Oral Glucose Tolerance Test) if HbA1c borderline — may reveal impaired glucose tolerance not visible in fasting glucose':
        '若 HbA1c 臨界，考慮口服葡萄糖耐受試驗（OGTT）— 可揭示空腹血糖未見的葡萄糖耐受障礙',
    'Screen for metabolic syndrome criteria — pre-diabetes rarely exists in isolation':
        '篩查代謝症候群標準 — 前期糖尿病鮮少單獨存在',

    # ── fatty_liver ──
    'Mediterranean diet — strongest evidence for NAFLD reversal: olive oil, fish, nuts, vegetables, whole grains':
        '地中海飲食 — 逆轉非酒精性脂肪肝（NAFLD）的最強實證：橄欖油、魚類、堅果、蔬菜、全穀類',
    'Eliminate fructose from beverages and minimize added sugars — fructose is preferentially metabolized in the liver and directly drives de novo lipogenesis':
        '戒除飲料中的果糖，最小化添加糖 — 果糖優先在肝臟代謝，直接驅動脂肪新生',
    'Reduce saturated fat intake — replaces liver fat stores; shift to mono/polyunsaturated fats':
        '減少飽和脂肪攝取 — 減少肝臟脂肪儲存；轉向單元及多元不飽和脂肪',
    'Coffee 2-3 cups/day (unsweetened) — multiple studies show hepatoprotective effect, reduces liver fibrosis risk':
        '每日無糖咖啡 2-3 杯 — 多項研究顯示具護肝效果，降低肝臟纖維化風險',
    'Increase dietary fiber — supports gut microbiome health which modulates liver fat metabolism':
        '增加膳食纖維 — 支持腸道菌群健康，調節肝臟脂肪代謝',
    'Both aerobic and resistance exercise reduce liver fat independently of weight loss — aim for 150+ min/week combined':
        '有氧與阻力運動均可獨立於減重之外降低肝臟脂肪 — 目標每週合計 150 分鐘以上',
    'High-intensity interval training (HIIT) may be more time-efficient for liver fat reduction than steady-state cardio':
        '高強度間歇訓練（HIIT）在減少肝臟脂肪方面可能比穩態有氧更有時間效益',
    '5-10% body weight loss — the single most effective intervention; resolves steatosis in 50%+ of cases':
        '減重 5-10% — 最有效的單一介入；超過 50% 的案例可逆轉脂肪變性',
    'Avoid rapid weight loss (> 1.5 kg/week) — can paradoxically worsen liver inflammation':
        '避免快速減重（每週 > 1.5 kg）— 可能反而加重肝臟發炎',
    'Eliminate or minimize alcohol — even moderate intake accelerates NAFLD progression':
        '完全戒酒或將飲酒降至最低 — 即使適量飲酒也會加速 NAFLD 進展',
    'Monitor ALT/AST every 3-6 months — rising transaminases suggest progression to NASH (Non-Alcoholic Steatohepatitis)':
        '每 3-6 個月監測 ALT/AST — 轉氨酶上升提示可能進展至非酒精性脂肪性肝炎（NASH）',
    'Repeat abdominal ultrasound in 6 months to assess liver fat regression':
        '6 個月後複查腹部超音波，評估肝臟脂肪消退情況',
    'If ALT persistently elevated > 2x ULN: consider FibroScan or liver biopsy to assess fibrosis stage':
        '若 ALT 持續 > 正常上限 2 倍：考慮 FibroScan 或肝臟切片，評估纖維化程度',
    'Vitamin E 800 IU/day — shown to improve NASH histology in non-diabetic patients (PIVENS trial); discuss with physician due to long-term safety concerns':
        '維生素 E 每日 800 IU — 已顯示可改善非糖尿病患者 NASH 的組織學表現（PIVENS 試驗）；因長期安全性疑慮，需與醫師討論',

    # ── hdl ──
    'Regular aerobic exercise is the most effective HDL-raising intervention — 30+ min, 5x/week; HDL increases 5-10%':
        '規律有氧運動是最有效的提升 HDL 介入 — 每次 30 分鐘以上、每週 5 次；HDL 提升 5-10%',
    'Resistance training also raises HDL — combine with aerobic for best effect':
        '阻力訓練也能提升 HDL — 與有氧運動結合效果最佳',
    'Replace refined carbs with healthy fats (olive oil, nuts, avocado) — low-fat diets paradoxically lower HDL':
        '以健康脂肪（橄欖油、堅果、酪梨）取代精製碳水化合物 — 低脂飲食反而會降低 HDL',
    'Moderate alcohol (1 drink/day) raises HDL — but weigh against TG elevation and liver effects':
        '適量飲酒（每日 1 杯）可提升 HDL — 但需權衡三酸甘油酯升高及肝臟影響',
    'Omega-3 fatty acids support HDL function and particle quality':
        'Omega-3 脂肪酸支持 HDL 功能及微粒品質',
    'Smoking cessation raises HDL 5-10% within weeks':
        '戒菸可在數週內提升 HDL 5-10%',
    'Weight loss — each 3 kg lost raises HDL ~1 mg/dL':
        '減重 — 每減少 3 kg 可提升 HDL 約 1 mg/dL',

    # ── hscrp ──
    'Anti-inflammatory diet: omega-3 rich fish, colorful vegetables, turmeric, ginger, green tea — reduces CRP 20-30%':
        '抗發炎飲食：富含 Omega-3 的魚類、多彩蔬菜、薑黃、薑、綠茶 — 降低 CRP 20-30%',
    'Reduce ultra-processed foods, refined sugars, and seed oils — all promote systemic inflammation':
        '減少超加工食品、精製糖及種子油 — 這些均會促進全身性發炎',
    'Omega-3 EPA+DHA — anti-inflammatory via resolution mediator pathways':
        'Omega-3 EPA+DHA — 透過促消退介質路徑發揮抗發炎作用',
    'Tart cherry — CRP reduction 23% (2025 RCT, also targets uric acid)':
        '酸櫻桃 — CRP 降低 23%（2025 年 RCT，同時作用於尿酸）',
    'Curcumin 500mg/day with piperine — evidence for CRP reduction in multiple meta-analyses':
        '薑黃素每日 500mg 搭配胡椒鹼 — 多項統合分析顯示有 CRP 降低效果',
    'Regular moderate exercise reduces CRP — acute anti-inflammatory effect via IL-6/IL-10 cascade':
        '規律中等強度運動可降低 CRP — 透過 IL-6/IL-10 級聯產生急性抗發炎效果',
    'Rule out acute infection or injury if hsCRP > 3.0 mg/L — values > 10 suggest acute inflammation, not cardiovascular risk':
        '若 hsCRP > 3.0 mg/L，需先排除急性感染或外傷 — 數值 > 10 提示急性發炎，而非心血管風險',

    # ── vitamin_d ──
    'Vitamin D3 2,000-4,000 IU/day to reach >= 30 ng/mL — D3 (cholecalciferol) is more effective than D2':
        '每日維生素 D3 2,000-4,000 IU，目標達到 ≥ 30 ng/mL — D3（膽鈣化醇）比 D2 更有效',
    'Pair with Vitamin K2 (MK-7) 100-200 mcg — directs calcium to bones rather than arteries':
        '搭配維生素 K2（MK-7）100-200 mcg — 將鈣引導至骨骼而非動脈',
    'Take with fat-containing meal for optimal absorption — vitamin D is fat-soluble':
        '與含脂肪餐食同服以最佳化吸收 — 維生素 D 為脂溶性維生素',
    'Sun exposure 15-20 min/day on arms/face — limited effectiveness at latitudes > 35 degrees; supplement is more reliable':
        '每日手臂及臉部日曬 15-20 分鐘 — 北緯 35 度以上效果有限；補充劑更可靠',
    'Recheck 25-OH Vitamin D in 3 months — adjust dose to maintain 30-50 ng/mL; avoid exceeding 100 ng/mL':
        '3 個月後複查 25-OH 維生素 D — 調整劑量維持 30-50 ng/mL；避免超過 100 ng/mL',

    # ── ast_alt ──
    'Reduce alcohol — primary cause of transaminase elevation outside of NAFLD':
        '減少飲酒 — 非 NAFLD 情況下轉氨酶升高的主要原因',
    'Mediterranean diet for liver health — reduces hepatic fat and inflammation':
        '地中海飲食護肝 — 減少肝臟脂肪及發炎',
    'Coffee 2-3 cups/day — hepatoprotective, reduces fibrosis risk':
        '每日咖啡 2-3 杯 — 具護肝效果，降低纖維化風險',
    'Review medications for hepatotoxicity — acetaminophen, statins, NSAIDs, herbal supplements':
        '審查藥物的肝毒性 — 乙醯胺酚、他汀類、非類固醇消炎藥、中草藥補充品',
    'If ALT > 2x ULN: check hepatitis panel (HBsAg, anti-HCV), consider liver ultrasound':
        '若 ALT > 正常上限 2 倍：檢查肝炎套組（HBsAg、anti-HCV），考慮肝臟超音波',
    'Recheck in 4-6 weeks — persistent elevation requires further workup':
        '4-6 週後複查 — 持續升高需進一步檢查',

    # ── egfr_kidney ──
    'Adequate hydration 2-2.5L/day — supports renal clearance':
        '每日足量補水 2-2.5 公升 — 維持腎臟清除功能',
    'Moderate protein intake (0.8-1.0 g/kg/day) — excessive protein increases renal workload':
        '適度蛋白質攝取（每日 0.8-1.0 g/kg）— 過量蛋白質會增加腎臟負擔',
    'Reduce sodium — lessens glomerular hyperfiltration pressure':
        '減少鈉攝取 — 降低腎小球過度過濾壓力',
    'Control blood pressure — hypertension is the #1 modifiable cause of CKD progression':
        '控制血壓 — 高血壓是慢性腎臟病進展最重要的可控因素',
    'Avoid nephrotoxic drugs: NSAIDs, high-dose contrast dye, certain antibiotics':
        '避免腎毒性藥物：非類固醇消炎藥、高劑量顯影劑、某些抗生素',
    'Annual eGFR + urine albumin-to-creatinine ratio (UACR) — detect microalbuminuria early':
        '每年檢測 eGFR + 尿液白蛋白肌酸酐比值（UACR）— 早期偵測微量白蛋白尿',

    # ── tsh_plan ──
    'Check Free T4 and Free T3 — TSH alone is insufficient for diagnosis':
        '檢查游離 T4 及游離 T3 — 單憑 TSH 不足以診斷',
    'Check thyroid antibodies (anti-TPO, anti-Tg) to rule out Hashimoto or Graves disease':
        '檢查甲狀腺抗體（anti-TPO、anti-Tg）以排除橋本氏甲狀腺炎或葛瑞夫茲病',
    'If subclinical (TSH 4.2-10, normal FT4): observe and recheck in 6-8 weeks before starting medication':
        '若為亞臨床型（TSH 4.2-10，FT4 正常）：觀察並在 6-8 週後複查，再決定是否用藥',
    'Ensure adequate iodine and selenium intake — both essential for thyroid hormone synthesis':
        '確保足夠的碘及硒攝取 — 兩者均為甲狀腺激素合成所必需',
    'Limit raw cruciferous vegetables if hypothyroid — goitrogens can interfere with iodine uptake (cooking neutralizes)':
        '若有甲狀腺低下，限制生食十字花科蔬菜 — 致甲狀腺腫物質可干擾碘的吸收（加熱可中和）',

    # ── ecg_plan ──
    'Myocardial ischemia on ECG: schedule cardiology consultation — may need stress test, echocardiogram, or coronary angiography':
        '心電圖出現心肌缺血：安排心臟科會診 — 可能需要運動壓力測試、心臟超音波或冠狀動脈攝影',
    'If persistent ischemia pattern: do NOT ignore — even without symptoms, silent ischemia carries significant risk':
        '若缺血型態持續：切勿輕忽 — 即使無症狀，無聲心肌缺血仍有顯著風險',
    'LVH (Left Ventricular Hypertrophy): often related to chronic hypertension — optimize BP control':
        '左心室肥大（LVH）：常與慢性高血壓相關 — 優化血壓控制',

    # ── bone_plan ──
    'Calcium 1000-1200 mg/day (diet + supplement) + Vitamin D3 2000 IU + Vitamin K2':
        '每日鈣 1000-1200 mg（飲食 + 補充劑）+ 維生素 D3 2000 IU + 維生素 K2',
    'Weight-bearing and resistance exercise — stimulates osteoblast activity':
        '負重及阻力運動 — 刺激成骨細胞活性',
    'If osteoporosis: discuss bisphosphonate or denosumab with physician':
        '若有骨質疏鬆：與醫師討論雙磷酸鹽或保骨針（denosumab）',
    'DEXA scan every 1-2 years to monitor':
        '每 1-2 年進行 DEXA 骨密度掃描監測',

    # ── cbc_plan ──
    'Low hemoglobin/RBC: check iron, ferritin, B12, folate — identify anemia type before supplementing':
        '血紅素/紅血球偏低：檢查鐵質、鐵蛋白、維生素 B12、葉酸 — 補充前先確認貧血類型',
    'Elevated WBC: rule out active infection; if persistent, consider hematology referral':
        '白血球升高：排除活動性感染；若持續升高，考慮血液科轉介',
    'Low platelets (< 100): avoid NSAIDs and assess bleeding risk; hematology referral if < 50':
        '血小板偏低（< 100）：避免非類固醇消炎藥並評估出血風險；若 < 50 需轉介血液科',

    # ── urine_plan ──
    'Proteinuria: check spot urine albumin/creatinine ratio — persistent proteinuria indicates kidney damage':
        '蛋白尿：檢查單次尿液白蛋白/肌酸酐比值 — 持續蛋白尿提示腎臟損傷',
    'Glucosuria with normal blood glucose: consider renal tubular dysfunction':
        '血糖正常卻有尿糖：考慮腎小管功能異常',
    'Hematuria: urology referral to rule out stones, infection, or malignancy':
        '血尿：轉介泌尿科排除結石、感染或惡性腫瘤',

    # ── tumor_plan ──
    'Single elevated tumor marker: repeat in 4-6 weeks to confirm — transient elevations are common with inflammation or benign conditions':
        '單一腫瘤標記升高：4-6 週後複查確認 — 發炎或良性疾病常見暫時性升高',
    'PSA elevated: urology referral for DRE and consideration of MRI/biopsy':
        'PSA 升高：轉介泌尿科進行直腸指診，並考慮 MRI 或切片',
    'CEA/AFP/CA-199: correlate with imaging (CT/MRI) if persistently elevated':
        'CEA/AFP/CA-199：若持續升高，需搭配影像檢查（CT/MRI）',

    # ── eye_plan ──
    'IOP > 21: ophthalmology referral for visual field test and optic nerve evaluation — early glaucoma is asymptomatic':
        '眼壓 > 21：轉介眼科進行視野測試及視神經評估 — 早期青光眼無症狀',
    'Annual comprehensive eye exam including fundoscopy — especially important with metabolic conditions':
        '每年包含眼底檢查的全面眼科檢查 — 代謝異常者尤為重要',

    # ── MERGED_ACTIONS ──
    'DASH/Mediterranean diet: vegetables 5+/day, whole grains, lean protein, olive oil, nuts, low-fat dairy — proven to reduce BP, LDL, TG, and body fat simultaneously':
        'DASH／地中海飲食：每日蔬菜 5+ 份、全穀類、瘦蛋白、橄欖油、堅果、低脂乳品 — 已證實可同步降低血壓、LDL、三酸甘油酯及體脂',
    'Create 500 kcal/day deficit (target ~0.5 kg/week). 5-10% body weight loss reverses fatty liver, improves insulin resistance, and reduces all metabolic markers':
        '每日減少 500 大卡（目標每週減重約 0.5 kg）。體重減少 5-10% 可逆轉脂肪肝、改善胰島素阻抗並降低所有代謝指標',
    'Protein 1.2-1.6 g/kg/day to preserve lean mass during weight loss — distribute across 3 meals':
        '每日蛋白質 1.2-1.6 g/kg，以維持減重期間的肌肉量 — 分配於三餐攝取',
    'Oat beta-glucan 3g/day (40-50g oats) + soluble fiber (psyllium, beans) — LDL reduction 5-10%':
        '每日燕麥 β-葡聚糖 3g（40-50g 燕麥）+ 可溶性纖維（車前子、豆類）— LDL 降低 5-10%',
    'Plant sterols/stanols 2g/day — blocks cholesterol absorption, LDL -6-10%':
        '每日植物固醇／甾烷醇 2g — 阻斷膽固醇吸收，LDL 下降 6-10%',
    'Omega-3 rich fish (salmon, mackerel) 2-3x/week + eliminate added sugars and sugar-sweetened beverages — reduces TG, hepatic fat, and fructose-driven uric acid production':
        '每週富含 Omega-3 魚類（鮭魚、鯖魚）2-3 次 + 戒除添加糖及含糖飲料 — 降低三酸甘油酯、肝臟脂肪及果糖驅動的尿酸生成',
    'Reduce refined carbohydrates; low glycemic index foods (brown rice, sweet potatoes); fiber 25-30g/day — improves HbA1c and postprandial glucose':
        '減少精製碳水化合物；選擇低升糖指數食物（糙米、地瓜）；每日膳食纖維 25-30g — 改善 HbA1c 及餐後血糖',
    'Sodium < 2,300 mg/day; increase potassium-rich foods (bananas, sweet potatoes, spinach) — BP reduction 8-14 mmHg':
        '每日鈉攝取 < 2,300 mg；增加富含鉀的食物（香蕉、地瓜、菠菜）— 血壓降低 8-14 mmHg',
    'Limit high-purine foods (organ meats, shellfish, red meat < 2x/week); increase low-fat dairy — promotes uric acid excretion':
        '限制高嘌呤食物（內臟、甲殼海鮮、紅肉每週 < 2 次）；增加低脂乳品 — 促進尿酸排泄',
    'Replace saturated fats with unsaturated fats (olive oil, avocado, nuts) — shifts LDL production and supports HDL':
        '以不飽和脂肪（橄欖油、酪梨、堅果）取代飽和脂肪 — 改變 LDL 合成並支持 HDL',
    'Anti-inflammatory foods: turmeric, ginger, green tea, colorful vegetables — reduces hsCRP 20-30%':
        '抗發炎食物：薑黃、薑、綠茶、多彩蔬菜 — 降低 hsCRP 20-30%',
    'Aerobic exercise 150+ min/week (brisk walking, cycling) — improves LDL, TG, HDL, HbA1c, BP, and body composition; start at current fitness and increase 10%/week':
        '每週有氧運動 150 分鐘以上（快走、騎車）— 改善 LDL、三酸甘油酯、HDL、HbA1c、血壓及體組成；從目前體能開始，每週增加 10%',
    'Resistance training 2-3x/week — preserves muscle during weight loss, increases resting metabolic rate, improves glucose uptake via GLUT-4 translocation':
        '每週阻力訓練 2-3 次 — 減重期間保留肌肉、提升基礎代謝率、透過 GLUT-4 轉位改善葡萄糖攝取',
    'Wall sits (isometric): 4x2min holds, 2min rest, 3x/week — most effective exercise for BP reduction (2023 BJSM meta-analysis: SBP -12.9 mmHg in 8 weeks)':
        '靠牆深蹲（等長收縮）：每組 2 分鐘 × 4 組，組間休息 2 分鐘，每週 3 次 — 降血壓效果最佳的運動（2023 年 BJSM 統合分析：8 週收縮壓 -12.9 mmHg）',
    'Post-meal walking 15-20 min — reduces postprandial glucose by 15-25% and TG surge':
        '餐後步行 15-20 分鐘 — 降低餐後血糖 15-25% 及三酸甘油酯急升',
    'Daily step goal 8,000-10,000 — each 1,000 steps above 4,000 reduces mortality risk':
        '每日目標步數 8,000-10,000 — 超過 4,000 步後，每增加 1,000 步均可降低死亡風險',
    'Omega-3 Fish Oil rTG form 4 caps/day (EPA+DHA ~1,920mg) — supports BP (-14.7 combined with DASH), TG (-25-30%), and inflammation':
        'Omega-3 魚油 rTG 型每日 4 粒（EPA+DHA 約 1,920mg）— 支持血壓（與 DASH 合用 -14.7 mmHg）、三酸甘油酯（-25-30%）及發炎管理',
    'Vitamin D3 2,000-4,000 IU/day + K2 (MK-7) 100-200mcg — take with fat-containing meal; target ≥30 ng/mL':
        '維生素 D3 每日 2,000-4,000 IU + K2（MK-7）100-200 mcg — 與含脂肪餐食同服；目標 ≥30 ng/mL',
    'Tart cherry extract daily — uric acid -37.4%, CRP -23% (2025 RCT); also targets inflammation':
        '每日酸櫻桃萃取物 — 尿酸 -37.4%、CRP -23%（2025 年 RCT）；同時作用於發炎指標',
    'Magnesium glycinate 200-400mg at bedtime — mild BP reduction + sleep quality improvement':
        '甘胺酸鎂 200-400mg 睡前服用 — 輕度降血壓 + 改善睡眠品質',
    'Vitamin C 500mg/day — promotes renal uric acid excretion; modest reduction ~0.5 mg/dL':
        '維生素 C 每日 500mg — 促進腎臟尿酸排泄；輕度降低約 0.5 mg/dL',
    'Sleep 7-8 hours — sleep deprivation increases ghrelin, cortisol, insulin resistance; hypertension risk 3.5x with < 6h; directly impairs glucose tolerance':
        '睡眠 7-8 小時 — 睡眠不足增加飢餓素、皮質醇、胰島素阻抗；不足 6 小時高血壓風險 3.5 倍；直接損害葡萄糖耐受性',
    'Hydration 2.5L/day minimum (complete main volume before 17:00) + citrus water for alkaline urine — increases renal uric acid clearance':
        '每日至少喝水 2.5 公升（主要飲水量於 17:00 前完成）+ 柑橘水鹼化尿液 — 提升腎臟尿酸清除率',
    'Stress management: chronic cortisol promotes visceral fat storage, raises blood glucose, and drives inflammation':
        '壓力管理：長期皮質醇升高促進內臟脂肪囤積、升高血糖並驅動發炎',
    'Weekly weigh-in (Saturday AM, post-void, fasted) — track trend, not daily fluctuations':
        '每週量體重（週六早晨、排尿後、進食前；週末大餐前）— 追蹤趨勢，不糾結單日波動',
    'Home BP monitoring 2x/week (seated, 5min rest, use 2nd reading) — establishes true baseline':
        '每週在家量血壓 2 次（坐姿、休息 5 分鐘後、取第二次讀數）— 建立真實基線',
    'Cardiology consultation for persistent ECG myocardial ischemia — within 1 month':
        '心電圖持續性心肌缺血：1 個月內安排心臟科會診',
    'Recheck fasting lipid panel in 3 months. If LDL >160 with additional risk factors: discuss statin with physician':
        '3 個月後複查空腹血脂。若 LDL > 160 且合併其他風險因子：與醫師討論他汀類藥物',
    'Annual HbA1c + fasting glucose monitoring; if rising toward 6.5%, discuss metformin. Consider OGTT for borderline cases':
        '每年監測 HbA1c + 空腹血糖；若趨近 6.5%，討論二甲雙胍。臨界個案考慮口服葡萄糖耐受試驗',
    'Monitor kidney function (eGFR, creatinine) annually. If uric acid >9.0 or recurrent gout: discuss allopurinol/febuxostat':
        '每年監測腎功能（eGFR、肌酸酐）。若尿酸 > 9.0 或反覆痛風：討論別嘌醇／非布索坦',
    'Repeat abdominal ultrasound in 6 months; monitor ALT/AST every 3-6 months — track fatty liver regression':
        '6 個月後重複腹部超音波；每 3-6 個月監測 ALT/AST — 追蹤脂肪肝消退情況',
    'Body composition analysis every 3 months — track fat mass vs lean mass, not just weight':
        '每 3 個月進行體組成分析 — 追蹤體脂量與肌肉量，而非僅看體重',
    'Recheck 25-OH Vitamin D in 3 months — adjust dose to maintain 30-50 ng/mL':
        '3 個月後複查 25-OH 維生素 D — 調整劑量維持 30-50 ng/mL',
}

def escape_for_js_string(s):
    """Escape special characters for JS single-quoted string."""
    return s.replace('\\', '\\\\').replace("'", "\\'")

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

count = 0
not_found = []

for en, zh in TRANSLATIONS.items():
    # Match: text: 'ENGLISH'  (not already having textZh right after)
    # We search for the exact text property and add textZh after it
    en_escaped = re.escape(en)
    zh_js = escape_for_js_string(zh)

    # Pattern: text: 'ENGLISH' followed by something that is NOT already textZh
    pattern = r"(text: '" + en_escaped + r"')(?!\s*,\s*textZh)"
    replacement = r"\1, textZh: '" + zh_js + r"'"

    new_content, n = re.subn(pattern, replacement, content)
    if n > 0:
        content = new_content
        count += n
    else:
        not_found.append(en[:60])

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done. Inserted textZh for {count} items.")
if not_found:
    print(f"\nNOT FOUND ({len(not_found)}):")
    for t in not_found:
        print(f"  - {t}")
