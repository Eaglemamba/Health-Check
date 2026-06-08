# 五色植化素光譜 — RCT-first 實證 review 與 David 飲食優化（v2 定版）

**建立日期：** 2026-06-08（v2，RCT-first 改寫，取代當日初版）
**讀者錨點：** David（37 歲男性，UA 8.9、LDL 154、HDL 39、BP 待降週均、目標體重 65kg、OSA 修復、AST 38、2017 右腎鈣化點史）
**緣起：** 使用者讀《天然植物營養素》（依黑/紅/橘/綠/白分色），問能否優化現有飲食。
**方法演進（重要）：** 初版用泛用 deep-research，盲點是**被 umbrella review 帶偏、漏掉單篇 landmark RCT**（如 Curtis 2019）。v2 改用 **RCT-first pipeline**：每個「食物 × 終點」做定向原始 RCT 檢索 → confirm/refute 雙 panel → judge 判定（ROBUST/MIXED/WEAK/REFUTED）+ David 對應。9 標的 / 36 agents / 441 tool calls。
**v2 對 v1 的關鍵修正：** 初版稱「可可粉是你最大草酸源」**過度警示**——RCT 顯示可可草酸生體吸收率僅 ~1.82%，黑巧克力不顯著升尿草酸（PMID 7806135；PMID 41083049）。真正該管的是**杏仁**與**維 C megadose**。詳見 §5。

---

## 0. TL;DR

1. **顏色光譜=多樣性記憶法，不是療效保證。** 用嚴格 RCT 檢驗，沒有任何一色拿到 ROBUST。多數是 MIXED（亞族群/劑型/劑量限定）、WEAK 或 REFUTED。
2. **唯一明確的「不要做」：β-胡蘿蔔素補充劑 = REFUTED 且有害**（ATBC/CARET 提高死亡率與肺癌）。吃橘色蔬菜可以，**別吃 β-胡蘿蔔素膠囊**。
3. **對你最值得加的兩個食物層**（食物、非補充劑、UA/草酸雙安全）：
   - 🥬 **芝麻葉 arugula 75-100g/天**——高硝酸鹽但**低草酸（7-10 mg/100g，菠菜的 ~1/80）**，補你 BP 的 NO 路徑，且避開菠菜/甜菜的草酸地雷。
   - 🧅 **紅洋蔥 ~100g/天（生食佳）**——quercetin 對**尿酸**有小幅 RCT 訊號（Shi & Williamson 2016，−0.45 mg/dL），低草酸、補你白色缺口。
4. **要重新校準的兩件你現在的認知**：
   - 🍒 **酸櫻桃對你 UA 的效果其實 WEAK**——在「真正痛風/高尿酸患者」的嚴謹 RCT（Stamp 2020）是 **null**。你補品指南標的 尿酸⭐⭐⭐ 偏高估（見 §6）。
   - 🫐 **藍莓不是 LDL/HDL/BP 工具**——脂質效果在多篇獨立 RCT 為 null；只有「內皮功能 FMD」次要訊號（單一廠商試驗）。留它是為了血管/纖維/多樣性，不是 marker。

---

## 1. 五色 RCT 判定總表

| 色 | 食物 / 成分 | 主張 | 判定 | 最佳 RCT 證據 |
|----|------------|------|------|----------------|
| ⚫🔵 | 藍莓（花青素）| 改善內皮/血脂 | **MIXED** | FMD +1.45% 次要終點；血脂 null（Curtis 2019, AJCN）|
| 🔴 | 酸櫻桃（花青素）| 降尿酸/痛風發作 | **WEAK** | 痛風患者 null（Stamp 2020, Rheumatology）|
| 🔴 | 番茄 / 茄紅素 | 降 LDL/BP | **MIXED** | 最大 GRADE meta null（Zamani 2023）；BP 僅高血壓亞組 |
| 🟠 | β-胡蘿蔔素 / 類胡蘿蔔素 | 降死亡率 | **REFUTED** | 補充劑↑死亡率（Bjelakovic 2007 JAMA）|
| 🟢 | 花椰菜 / sulforaphane | 降 BP/LDL | **MIXED** | LDL −5~7% 預設主終點複製（Armah 2015）；BP null |
| 🟢 | 硝酸鹽（甜菜/葉菜）| 降 BP | **MIXED** | SBP −7.7 mmHg（Kapil 2015）；但甜菜/菠菜高草酸 |
| ⚪ | 大蒜 / allicin | 降 BP/LDL | **MIXED** | AGE −11.8 mmHg 限高血壓者（Ried 2013）；LDL null（Gardner 2007）|
| ⚪ | 洋蔥 / quercetin | 降 BP | **MIXED** | BP 僅 ≥500mg 補充劑 + 高血壓者（Serban 2016）；**UA 有食物級訊號**（Shi 2016）|
| 🧪 | 草酸分級（跨色腎安全）| 可可/杏仁/菠菜高、kale/花椰菜/南瓜低 | **MIXED** | 食物分級成立但生體吸收/結石預防 RCT 弱（Sorensen 2014）|

> 評級：ROBUST=多篇複製主終點 RCT；MIXED=有正向 RCT 但限亞族群/劑型/劑量或被大型 meta 推翻；WEAK=僅單篇小型或次要終點；REFUTED=null 或證明有害。

---

## 2. 逐色詳解（RCT 級）

### ⚫🔵 黑/藍 — 藍莓（MIXED）
- **血脂/HDL 臂 = 實質否決**：Curtis 2019 主終點 HOMA-IR null（p=0.07）；TC/LDL 全族群 null；HDL +3 mg/dL 僅為「非 statin 使用者」事後亞組。Basu 2010（~350g/天）與 Wang 2022 在等量或更高劑量仍 null。花青素降脂需 **>300 mg/天 × >12 週且 delphinidin 主導**（藍莓主為 cyanidin）。
- **內皮 FMD 臂 = 未否決但未確立**：Curtis 2019 次要終點 FMD +1.45%（p=0.003）；機制（NO/cGMP）合理；**但無任何獨立 RCT 以 FMD 為主終點複製**。
- **你的用法**：150g/天**留著**（血管+纖維+多樣性），**別當 LDL/HDL/BP 工具**。草酸 14-17 mg/100g → 150g ≈ 21-25 mg，1 杯可接受，當天別再疊菠菜/杏仁/巧克力。

### 🔴 紅 — 酸櫻桃（WEAK）
- **尿酸**：唯一正向 RCT（Hillman 2021）是**非痛風、急性 48h、n=8/組**；而在**真正痛風患者**的嚴謹試驗（Stamp 2020, n=50, 28 天, 4 劑量）**任何劑量皆 null（p=0.76）**；2024 crossover（Gonzalez）亦 null。
- **痛風發作**：**零完成 RCT**；常被引的 OR 0.65（Zhang 2012）是網路招募 case-crossover（回憶偏差/反向因果）；唯一 flare RCT 中止未發表。
- **你的用法**：你 UA 8.9 正對應 Stamp 2020 的 null 族群 → **預期效益低**。**果汁/濃縮禁用**（果糖直接升尿酸 + 不利減重）；若留，**膠囊型** 480mg。UA 8.9 真正解方是腎臟科降尿酸藥討論，非櫻桃。

### 🔴 紅 — 番茄/茄紅素（MIXED）
- **BP**：乾淨正向 RCT 僅在**已服藥未控制高血壓者**（Paran 2009, SBP −13 mmHg）；健康族群 null；最大 GRADE meta（Zamani 2023, 34 RCT）全 null。
- **LDL**：正向僅限 ≥25mg/天亞組 + 廠商利益衝突試驗；Zamani 2023 null。
- **你的用法**：**新鮮番茄 100-150g + 油脂**（提升 lycopene 吸收）當低風險配菜可以；**別吃高劑量茄紅素膠囊**；濃縮番茄製品（醬/乾）草酸較高，限量。⚠️ 觀察性訊號：番茄**可能升尿酸**——你 UA 8.9，別大量堆。

### 🟠 橘 — 類胡蘿蔔素 / β-胡蘿蔔素（REFUTED）
- **β-胡蘿蔔素補充劑有害**：ATBC（總死亡 +8%、肺癌 +18%）、CARET（死亡 RR 1.17，提早中止）、Bjelakovic 2007 JAMA（47 RCT, n=180,938, 全因死亡 RR 1.07）。
- **你的用法**：**胡蘿蔔/南瓜肉吃（低草酸、低嘌呤），β-胡蘿蔔素膠囊一顆都別碰。** 補類胡蘿蔔素**別用菠菜（高草酸）或地瓜（中高草酸）**——用南瓜肉/胡蘿蔔。

### 🟢 綠 — 花椰菜 / sulforaphane（MIXED）
- **LDL**：Armah 2015 兩個**預設主終點** RCT，高 glucoraphanin 花椰菜 −5~7% LDL（pooled p=0.031）——真複製，但效果小、與更廣 meta 的 null 並存。
- **BP**：唯一專設主終點試驗（Christiansen 2010）null；pooled −10.9 mmHg 是小樣本假象。
- **你的用法**：**新鮮/輕蒸花椰菜 ~400g/週（≈每天 1 杯）**作 LDL 輔助（約 −7~10 mg/dL，非取代飲食/藥）；**乾燥粉劑無效**（myrosinase 失活）。低嘌呤、成熟花椰菜低草酸。**別當 BP 或 HDL 工具。**

### 🟢 綠 — 硝酸鹽（MIXED）→ 你的最佳新增之一
- **BP**：Kapil 2015（4 週, n=68, 高血壓）SBP −7.7 mmHg 三法一致；但 Bondonno 2015 在已治療高血壓者 null；正向試驗多用**濃縮甜菜汁 250-500mL**，非日常葉菜。
- **草酸衝突（關鍵）**：**甜菜、菠菜=高草酸，對你禁用**作硝酸鹽來源。
- **✅ 解法 = 芝麻葉 arugula**：草酸僅 **7-10 mg/100g**（菠菜 567-970），卻是最高硝酸鹽葉菜之一。**每天 75-100g 沙拉**——補你 NO 路徑（與洛神花、citrulline 4g、生可可、鎂、魚油的 NO 堆疊加成），且不踩草酸地雷。低嘌呤、無補品重疊。

### ⚪ 白 — 大蒜 / allicin（MIXED）
- **BP**：AGE（陳年大蒜萃取）480mg/天（含 SAC ~1.2mg）在**高血壓者** SBP −11.8 mmHg（Ried 2013）；Rohner 2015 meta 複製；正常血壓者無效。
- **LDL**：最強獨立 RCT（Gardner 2007, NIH, n=192）**全 null**。
- **你的用法**：**若你確為高血壓**→ AGE 480mg/天（標 SAC）可輔助；**烹調大蒜 allicin 幾乎失活**（別期待補品效果）。每日 1-2 瓣調味：低草酸、低嘌呤、安全。⚠️ AGE 抗血小板，與 aspirin/NSAID/warfarin 併用要告知醫師。

### ⚪ 白 — 洋蔥 / quercetin（MIXED）→ 你的最佳新增之一（走 UA 不是 BP）
- **BP**：僅 quercetin **補充劑 ≥500mg/天 + 高血壓者**有效（Serban 2016）；飲食洋蔥達不到劑量（要 10-50 顆）。
- **UA（對你更相關）**：Shi & Williamson 2016（雙盲 crossover, n=22 pre-高尿酸男性）500mg/天 quercetin × 4 週 → **血漿 UA −0.45 mg/dL（p=0.008）**，機制走 xanthine oxidase 抑制，與你 UA 管理直接重疊。作者估 **500mg ≈ ~100g 紅洋蔥**。
- **你的用法**：**每天 ~100g 紅洋蔥（生食佳，加熱降解 quercetin）**——食物級補 UA + 補白色缺口，低草酸。⚠️ 若日後用 allopurinol，高劑量 quercetin 補充劑與其加成抑制 XO，需醫師審；食物量無此風險。

---

## 3. 對 David 的優化建議（可執行、份量、排序）

> 原則：補真缺口 + UA/草酸雙安全 + 食物優先、避補充劑 + 不與現有重疊。

### 🟢 加入（淨正向）
1. **芝麻葉 arugula 75-100g/天**（午餐沙拉基底）→ BP 的 NO 路徑，低草酸安全。**取代你想加的菠菜/甜菜**。
2. **紅洋蔥 ~100g/天（生）**→ quercetin 食物級降 UA + 白色缺口。落地：沙拉加生洋蔥絲 + 晚餐魚鋪蒜末（順帶大蒜）。
3. **花椰菜 ~1 杯/天（輕蒸）**→ LDL 輔助 −7~10 mg/dL（非取代主力）。
4. **胡蘿蔔/南瓜肉**輪替→ 類胡蘿蔔素（食物，非膠囊），低草酸。

### 🟡 維持（已對）
- 藍莓 150g（血管/纖維，非 marker）、kale 15-20g（低草酸綠色最佳）、菇 100-130g（UA 安全，植物嘌呤不增痛風，Choi 2004 NEJM）。

### 🔴 不要
- **β-胡蘿蔔素 / 抗氧化綜合補充劑**（REFUTED 且增死亡率）。
- 高劑量茄紅素/quercetin/花青素膠囊（CP 值低、證據弱）。
- 酸櫻桃**果汁/濃縮**（果糖升 UA + 不利減重）。

---

## 4. 與你現況的衝突與旗標

### 🍒 你的補品指南「酸櫻桃 尿酸⭐⭐⭐」需下修
RCT-first 證據：在你這種高尿酸族群，酸櫻桃降尿酸 **WEAK/null（Stamp 2020）**。它在你 stack 仍可因**睡眠/BP**理由保留，但**不該被當 UA 主力**。建議下次改版補品指南時把它從 尿酸⭐⭐⭐ 下修為 ⭐（並把 UA 主力明確放在飲水 + 減動物嘌呤/果糖 + 腎臟科藥）。

### 🧅 番茄/洋蔥的 UA 方向相反，別搞混
番茄（觀察性）**可能升** UA；洋蔥 quercetin（RCT）**小幅降** UA。要補 UA 走**洋蔥**不是番茄。

### 💊 補品交互
- 大蒜 AGE 抗血小板（aspirin/NSAID/warfarin 告知醫師）。
- quercetin 補充劑 × allopurinol 加成抑 XO（食物洋蔥無虞）。

---

## 5. 草酸：v1 警示修正（重要）

RCT 級重新校準後的優先順序（**個別食物草酸含量其實是最弱的槓桿**）：

| 項目 | 校準後結論 |
|------|-----------|
| **可可粉（v1 過度警示）** | 生體吸收率僅 ~1.82%；黑巧克力 100g **不顯著升尿草酸**（PMID 41083049）。你 5-10g/天**影響可忽略**，無需特別限制。**但勿與維 C megadose 同時。** |
| **杏仁（真正該管）** | RCT 確認顯著升尿草酸（931 µmol/24h）。**杏仁奶稀釋無妨，但整顆杏仁限 ≤15g/天**，勿與其他高草酸同餐。 |
| **維 C 高劑量（>500mg/天）** | ascorbic acid 是內源草酸前驅 →**比可可更大的草酸風險**。你補品無高劑量維 C，維持即可。 |
| 菠菜 / 甜菜葉 | 高（567-970 / ~610 mg/100g）→ **避免**；硝酸鹽改用 arugula。 |
| kale / 花椰菜 / 南瓜肉 | 低 → 安全（且鉀/鎂/citrate 反而護結石）。 |
| **南瓜籽（pepitas）** | 比南瓜肉高 → 你下午 30g 可**斟酌降到 15g**，或確保同餐有鈣。 |

**結石防護真正的槓桿排序（RCT 級）**：① 大量飲水（尿量 >2L/天，最強）② 高草酸食物**與鈣同餐**（腸道螯合）③ 限杏仁/菠菜量 ④ 不維 C megadose ⑤ 低鈉。

---

## 6. 限制與後續

- 沒有任何一色達 ROBUST；多數正向訊號限**特定亞族群/劑型/劑量**，且**食物 ≠ 補充劑劑量**。
- 多數試驗為 surrogate endpoint（FMD/血脂/BP），**無 MACE 硬終點**。
- 草酸結石「食物限制可防復發」**無主終點 RCT**（Sorensen 2014 null）。
- 後續可單獨深挖：arugula 慢性 BP RCT、紅洋蔥 UA 在「真高尿酸」族群的 RCT、你 kale+南瓜籽 每日總草酸定量。

---

## 引用（primary RCT / meta）

- Curtis PJ et al. 2019, *Am J Clin Nutr* (PMID 31136659) — 藍莓 6 月 RCT，FMD +1.45%，血脂 null
- Basu A et al. 2010 (PMID 20660279)；Wang Y et al. 2022 (PMID 35807742) — 藍莓血脂 null 複製
- Stamp LK et al. 2020, *Rheumatology* (PMID 31891407) — 痛風患者酸櫻桃降尿酸 null（主證據）
- Hillman & Uhranowsky 2021 (PMID 33506357) — 非痛風急性 UA −8%
- Zamani M et al. 2023, *Curr Pharm Des* (PMID 37496241) — 茄紅素 34 RCT GRADE，null；Paran 2009 — 高血壓亞組 SBP −13
- Bjelakovic G et al. 2007, *JAMA* (PMID 17327526) — β-胡蘿蔔素增死亡；ATBC (PMID 8127329)；CARET (PMID 8602180)
- Armah CN et al. 2015, *Mol Nutr Food Res* (PMID 25851421) — 花椰菜 LDL −5~7% 主終點；Christiansen 2010 — BP null
- Kapil V et al. 2015, *Hypertension* (PMID 25421976) — 硝酸鹽 SBP −7.7；Bondonno 2015 (PMID 26135348) — 已治療高血壓 null
- Ried K et al. 2013, *Eur J Clin Nutr* (PMID 23169470) — AGE SBP −11.8；Gardner CD et al. 2007, *Arch Intern Med* — 大蒜 LDL null
- Serban MC et al. 2016, *JAHA* (PMID 27405810) — quercetin BP ≥500mg；**Shi & Williamson 2016, *Br J Nutr* (PMID 26785820) — quercetin 降 UA −0.45 mg/dL**
- Sorensen MD et al. 2014, *AJKD* (PMID 24560157) — 低草酸 vs DASH null；可可吸收 PMID 7806135 / PMID 41083049
- 背景：Choi HK et al. 2004, *NEJM* — 植物嘌呤不增痛風（非本次驗證，確立文獻）

---

*分類：diet-nutrition｜方法：RCT-first multi-agent（定向檢索 + confirm/refute 雙 panel + judge；36 agents / 9 targets / 441 tool calls）｜2026-06-08 v2，取代初版 deep-research 版*
