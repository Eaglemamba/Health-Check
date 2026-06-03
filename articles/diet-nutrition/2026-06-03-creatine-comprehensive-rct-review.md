# Creatine 全面 RCT 證據回顧（七領域 meta-analysis 彙整）

**日期**：2026-06-03
**對象**：David Kuo（37 歲男性，170 cm，~68 kg，體脂 19.6%）
**方法**：七個獨立研究 agent 平行檢索 PubMed/PMC、Cochrane、JISSN、Frontiers、Nature SR、MDPI，各領域以 RCT / systematic review / meta-analysis 為優先，並對關鍵爭議主張做 adversarial verification
**前一篇**：[2026-05-19 Creatine + Glycine 補充品評估](2026-05-19-creatine-glycine-supplement-evaluation.md)（本篇為其全面證據升級版；同時修正前篇「mid-40s / 抗老化」框架 — 依 CLAUDE.md baseline，David 為 **37 歲**，屬介入複利期，非中年退化框架）
**模式**：Copilot Mode — 以下為working paper，臨床決策須經醫師審核

---

## 一、執行摘要（七領域裁決）

| 領域 | 對 David 的淨裁決 | 證據強度（GRADE） |
|------|------------------|------------------|
| **認知 / 睡眠剝奪** | 🟢 唯一以「急性單劑」最有證據；慢性 5g 在健康年輕人為 null | 記憶 moderate；睡眠剝奪急性效益 low-moderate（單一團隊未獨立複現） |
| **肌力 / 瘦肉量** | 🟢 證據最強且穩健；<50 歲男性 + 阻力訓練效益明確 | 肌力 moderate-high；瘦肉量 moderate |
| **骨密度（BMD）** | 🔴 一致 null，勿期待 | low（2 年 RCT n=237 確定無效） |
| **腎功能 / 血清 creatinine** | 🟡 真實 GFR 不變，但血清 creatinine 生理性升高 → 干擾解讀（David 的關鍵點） | 真實 GFR 安全 moderate-high |
| **尿酸 / 普林** | 🟡 機制上不走普林路徑（不應升尿酸）；但唯一測 resting UA 的小 RCT 報 +2.77，且 David baseline 8.9 緩衝為零 | very low（直接證據稀少且 confounded） |
| **心血管代謝（BP/血脂/血糖/HRV）** | 🟡 中性偏正；不升 BP、不降 LDL/HDL；唯一較強訊號是「+運動」改善血糖 | BP moderate；血糖 moderate；HRV very low |
| **有氧 / 跑步 / 體重** | 🔴 對 Zone-2 無效、不升 VO2max；+0.9–1.7 kg 水重直接抵觸減重訊號 | VO2max high（null/微負）；水重 high |

**一句話總結**：Creatine 在「肌力 + 認知韌性」是低風險、有 RCT 證據的增益層，與你 OSA/HRV/血壓核心問題**正交**；但對你個人的兩個進行中議題 —— **腎臟科轉診未完成（baseline UA 8.9 + creatinine 1.05）** 與 **減重靠每日體重訊號** —— creatine 會在這兩處製造干擾。**結論不變且更穩固：腎臟科 baseline 取得前不啟動；啟動採無 loading 3–5g。**

---

## 二、認知 / 睡眠剝奪（你 TST ~5h，高度相關）

### 關鍵 RCT

| 研究 | 設計 | n | 劑量 | 結果 | 品質 |
|------|------|---|------|------|------|
| Gordji-Nejad 2024, *Sci Rep* | 雙盲 crossover RCT | 15 | 單劑 **0.35 g/kg**（~24g/70kg），睡眠剝奪 21h | 處理速度 +16–29%；字詞記憶 +10.3%（p=0.005）；腦 PCr/Pi 維持、pH 不降 | 機制嚴謹但 n 小、單一團隊未獨立複現 |
| Gordji-Nejad 2025, *Nutrients* | 雙盲 crossover RCT | 29 | 單劑 **0.2 g/kg** | 整體認知 ~+12% | 同團隊；無 MRS |
| Xu 2024 meta（16 RCT）, *Front Nutr* | meta-analysis | 492 | 3–20 g/d | 記憶 SMD 0.31（p<0.00001）；處理速度顯著；executive function 與整體認知 **不顯著** | PROSPERO 註冊；記憶 GRADE moderate |
| **Fazio 2023**（最嚴謹 crossover RCT） | 雙盲 crossover | 123 | **5 g/d × 6 週** | backward digit span d=0.17（p=0.064，NS）；RAPM NS；8 項任務全 NS | 迄今最大、power 充足 → **健康成人 5g/d 慢性劑量為 null** |
| Moriarty 2023, *Brain Sci* | 3-arm RCT | 30 | 10 或 20 g/d × 6 週 | 全領域 NS | null |

### 重點解讀

- **腦攝取受限**：腦 creatine 攝取速率僅約肌肉一半（SLC6A8 在 astrocyte 缺乏）。20 g/d × 4 週才升腦 total creatine ~8.7%（Dechent 1999），**5 g/d 慢性對腦幾乎無感** → 這解釋了 Fazio 2023 的 null。
- **唯一有力的是「急性單劑救援」**：0.2–0.35 g/kg 單劑在睡眠剝奪情境保護處理速度，與你工作日 5h TST + 晨間高負荷決策的型態最吻合。但 GI 風險在 24g 單劑明顯（Fazio：5g 即 GI 風險 ×4.25），須從 0.1–0.2 g/kg 試耐受。
- **EFSA 2024 健康宣稱評估**：駁回 creatine 認知宣稱，理由是申請劑量（3 g/d）遠低於有效劑量。
- **OSA 警示**：OSA 認知損害源自間歇缺氧 + 睡眠片段化，非單純睡眠縮短。Creatine **不能取代** OSA 診斷與治療。

---

## 三、肌力 / 瘦肉量 / 骨密度（搭配你阻力訓練 protocol）

### 關鍵 meta-analysis

| 研究 | n | 結果（effect size） | 備註 |
|------|---|--------------------|------|
| **Wang 2024**（<50 歲，23 RCT）, *Nutrients* | 509 | 男性上肢 1RM **+4.95 kg**（CI 3.65–6.25）；下肢 **+11.68 kg**（CI 8.79–14.57），p<0.001 | **女性不顯著**；你正落在最佳反應族群 |
| Ashtary-Larky 2025（61 RCT）, *JISSN* | 1457 | FFM **+1.39 kg**（CI 1.07–1.70），GRADE **high** | 60.7% 業界資助（利益衝突，已揭露） |
| Desai 2024（<50 歲，獨立資助） | — | 瘦體重 +1.14 kg；體脂 −0.73 kg | 政府/獨立資助，結果仍成立 |
| **Backx 2017**（固定不動模型 RCT） | 27 | 無訓練刺激 → 肌量/肌力**無保留**（−5.5% vs −5.6%） | **creatine 必須搭配訓練才有用** |
| **Chilibeck 2023**（2 年 RCT） | 237 | 股骨頸 / 全髖 **BMD 無差異**（p=0.84 / 0.69） | 最長最有力 → **BMD null 確定** |

### 重點解讀

- 肌力/瘦肉量效益**真實、可複現、且不依賴業界資助**（政府資助 trial 仍成立）。
- **無訓練 = 無效**：creatine 是放大訓練適應，不是基礎合成代謝。啟動時機應對齊你的阻力訓練 protocol 已穩定執行。
- **骨密度別期待**：5 個 meta + 2 年 RCT 一致 null。37 歲 peak bone mass 已大致定型，骨幾何（section modulus）的次級訊號為 hypothesis-generating，不可行動。
- 「瘦肉量 +1.4 kg」含初期水分；影像法 meta（Burke 2023）SMD 僅 +0.11，真實肌纖維增量小於體重秤數字。

---

## 四、腎功能 / 血清 creatinine（你的安全核心）

### 關鍵 RCT（直接測真實 GFR）

| 研究 | 設計 | 腎臟終點 | 結果 |
|------|------|----------|------|
| **Lugaresi 2013** | RCT n=26，高蛋白飲食 + 12 週 | **51Cr-EDTA 實測 GFR** | 組間交互作用 p=0.64 → 真實 GFR 不變 |
| Gualano 2008 | RCT n=18，12 週 | **cystatin C** | cystatin C 不升反降（p=0.0001 time），證實無腎損 |
| Gualano 2011（T2D） | RCT n=25，12 週 | 51Cr-EDTA GFR | p=0.58，無差異 |
| Gualano 2010（單腎） | 實測 GFR | 單腎 + 輕度腎功能不全 | mGFR 81.6 → 82.0（不變） |
| Kreider 2003 | cohort n=98，**21 個月** | 69 項臨床 panel | creatinine、BUN、UA、電解質**皆無顯著變化** |
| BMC Nephrology 2025 meta | RCT meta | 血清 creatinine | +0.07 µmol/L（統計顯著、臨床可忽略）；eGFR 無臨床意義變化 |

### 核心區分：血清 creatinine ≠ 真實腎損傷

- Creatine 以 ~1.7–2%/天非酵素降解為 creatinine。補充 → creatinine **生成增加** → 血清 creatinine 升 **0.1–0.3 mg/dL**（loading 期更明顯）。**這是化學訊號，不是腎臟訊號。**
- **eGFR artifact**：creatinine-based eGFR 會把升高的 creatinine 誤判為 GFR 下降。對 baseline 1.05 的人，+0.2 mg/dL 可使 eGFR 估值掉 **8–12 mL/min/1.73m²**，足以跨越臨床分級門檻 → 易被誤判為 CKD。
- **解法**：(1) 用 **cystatin C-based eGFR**（不受 creatine 影響）；(2) 抽血前 washout。

### Washout protocol（取得乾淨 baseline）

| 項目 | 時程 |
|------|------|
| 血清 creatinine 回 baseline | 停用 **3–4 週**（保險 6 週） |
| 抽血前避免劇烈運動 | 48–72 小時 |
| 抽血前避免高蛋白（紅肉） | 24 小時 |
| 若無法等待 | 同時加驗 cystatin C-based eGFR |

> 前篇（2026-05-19）寫「抽血前 5–7 天停用」 —— **本篇修正**：5–7 天足以消除肌肉 creatine pool 的多數影響，但要取得**腎臟科正式 baseline**（首次定義你腎功能基準），建議拉到 **≥4 週、最好 6 週**，避免把 baseline 本身污染。

### 誰不該用 / 警示

- 應避免（除非腎臟科核可）：eGFR <45（CKD 3b–5）、活動性腎病症候群、移植服用 cyclosporine/tacrolimus、孕期。
- 相對警示：單腎、輕度 CKD、**baseline creatinine 升高但病因未明（= David 目前狀態，轉診待完成）**、規律 NSAID 使用、hyperuricemia。

---

## 五、尿酸 / 普林代謝（你 UA 8.9，緩衝為零）

### 證據

| 研究 | 設計 | 對尿酸的發現 | 品質 |
|------|------|------------|------|
| **Percário 2012** | RCT，每組 n=9 | creatine 組 UA +2.77（p=0.025）；**但 placebo 組也 +2.26**（NS 僅因變異大） | 嚴重 confounded（全組同做阻力訓練、UA 為次要終點、青少年運動員） |
| **Bellinger 2000** | 雙盲 crossover RCT n=20 | hypoxanthine **顯著下降**（p<0.01）→ creatine **保留**腺核苷酸，非加速分解 | 直接反駁 ATP 分解假說 |
| Li 2024 Mendelian Randomization | MR | creatine 與血清 UA **無顯著關聯**（IVW p>0.05） | 以設計排除 confounding，支持 null |
| Kreider 2003（21 個月 cohort） | cohort n=98 | UA **無變化** | 長期 |

### 機制裁決

Creatine 分子式 C₄H₉N₃O₂，**無嘌呤環**，由 arginine + glycine 合成，代謝終點是 creatinine（經腎排出），**不進入 xanthine oxidase 路徑** → 機制上不產生尿酸。唯一理論交點（運動時 ATP 周轉 → 腺核苷酸分解 → urate）被 Bellinger 2000 反向證據駁回。

### 對 David 的關鍵 caveat

- 機制與多數證據說「不升尿酸」 —— 但 **唯一測 resting UA 的人體 RCT（Percário）報 +2.77**，雖極可能是運動 confounding，而你 baseline **8.9 已遠超 6.8 mg/dL 結晶飽和閾值，任何來源的 +2~3 都臨床上不可接受**。
- **所有 trial 受試者 baseline UA 在 4–6**，無一人是 hyperuricemic → 外推到你身上有根本不確定性。
- **無任何 creatine 引發 gout flare 的證據**（也無法量化風險）。

---

## 六、心血管代謝（BP / 血脂 / 血糖 / HRV）

| 終點 | 裁決 | 關鍵證據 |
|------|------|----------|
| **血壓** | 不升（loading 水重疑慮被駁回）；運動後 SBP 反應或微降 | 2 年停經女性 RCT BP 無差異；Sanchez-Gonzalez 2011 運動後 SBP 升幅 placebo +14 vs creatine +5.6 |
| **LDL** | **不降**（別當降脂工具） | 唯一報 LDL 升的 de Moraes 2014 為 open-label/無運動對照/7 天 loading；其餘盲性 RCT 皆 null |
| **HDL（你 39）** | 無效 | 全 trial null → 升 HDL 靠有氧運動，非 creatine |
| **血糖 / HbA1c** | **最強心代謝訊號**：+運動可降 | Gualano 2011 T2D RCT：HbA1c **−1.1%**（CI −1.9~−0.4，p=0.004），機制為 GLUT-4 translocation |
| **HRV（你用 Garmin 追）** | 證據極弱，勿期待靜息 HRV 改變 | 僅 2 個 acute 小 trial，效果限於運動後副交感再活化 |

**淨評估**：creatine 對你心代謝**安全、中性偏正**。真正槓桿是它支撐訓練量 → 間接惠及 BP/LDL/HDL/血糖。別期待它直接做藥理效果。

---

## 七、有氧 / 跑步表現 / 水分與體重（你 C25K + 減重）

| 項目 | 裁決 | 數據 |
|------|------|------|
| **VO2max** | **無效，微負** | Gras 2021 meta（19 RCT）ES −0.32（p=0.002）；Deng 2025 NS |
| **Zone-2 跑步** | 無 creatine 反應機制（PCr 在 >80% VO2max 才相關） | 無證據 |
| **體重** | loading **+0.9–1.7 kg 水重**（5–7 天內），maintenance +0.5–1.0 kg | Kutz 2003 +1.7 kg；Beis 2011 +0.90 kg；體脂%與脂肪量**不變** |
| **跑速代價** | +1 kg → 同努力配速約慢 5–6 sec/km（5K 約 +25–30 秒） | 真實但輕微 |
| **抽筋 / 熱調節** | **迷思**：不增加抽筋或脫水風險，甚至可能更佳 | Lopez 2009 meta（PEDro 7–10）；NCAA cohort creatine 組抽筋**更少**（p=0.021） |

**對減重目標的衝突**：你以**每日體重秤數字**為回饋迴路，creatine 的 +1–1.5 kg 水重即使體組成在改善，仍是**直接反訊號**。理性做法：減重 + Zone-2 base 建立後，再於導入 HIIT/重訓時加入（屆時 PCr 機制才真正運作），且以**體脂%/內臟脂肪**而非體重秤追蹤。

---

## 八、劑量 / 形式 / 時機 / 品質

### 形式

| 形式 | vs monohydrate 的 head-to-head | 裁決 |
|------|------------------------------|------|
| **Monohydrate** | 參考標準（500+ RCT） | **黃金標準** |
| Kre-Alkalyn（buffered） | Jagim 2012 RCT n=36：肌肉 creatine 無差異 | 無優勢 |
| Ethyl ester（CEE） | Spillane 2009 RCT n=30：血清 creatine 更低、creatinine 更高（已水解） | 劣於 monohydrate |
| HCl / nitrate / 液態 | 無人體 head-to-head RCT | 未證實 |

> ISSN 2017 Position Statement 5：monohydrate 是攝取與效能上最有證據的形式，**無其他形式被證明更優**。

### Loading vs 無 loading

- Loading（20 g/d × 5–7 天）：7 天飽和，但 +1–2 kg 水重、GI 風險高（Ostojić 2008：單劑 10g 腹瀉 55.6% vs 2×5g 28.6%）。
- 無 loading（3 g/d × 28 天）：**相同終點飽和**，水重與 GI 風險極小。
- **對你（weight-conscious）：無 loading 是正解。**

### 時機 / 共服

- 與**碳水 + 蛋白**同服增加肌肉攝取（ISSN PS6，胰島素介導）。
- 運動後 vs 前：Antonio 2013（n=19）運動後略佳，但未達顯著 → **一致每日服用比時機重要**。
- 休息日照常服（維持飽和）。

### 品質（台灣取得）

- 首選 **Creapure（德國 AlzChem，pharmaceutical GMP，HPLC 每批驗）** + **NSF Certified for Sport / Informed Sport** 批次認證。
- 雜質風險：DCD、DHT、creatinine；廉價來源抽驗約 42% 純度不達 USP。
- iHerb 可寄台：Thorne、Momentous、BulkSupplements（Creapure）、Optimum Nutrition（Informed Choice）。

---

## 九、對 David 的整合決策

### 9.1 啟動前置條件（順序不變、證據更穩固）

- [ ] **腎臟科轉診完成** —— 取得**乾淨 baseline**（停 creatine ≥4 週後）：serum creatinine、**cystatin C-based eGFR**、UACR、UA。這是最關鍵一步：你 UA 8.9 + creatinine 1.05 病因未明，轉診正是為釐清此事，**不應在未定性的腎臟圖像中加入新變數**。
- [ ] 若腎臟科啟動 urate-lowering therapy（allopurinol/febuxostat）使 UA <6.0 且確認腎功能正常 → creatine 不再是禁忌。
- [ ] PSG 預約敲定（避免混淆 OSA 判讀）。
- [ ] 阻力訓練 protocol 已穩定執行（無訓練 = 無肌肉效益）。

### 9.2 啟動 protocol（條件滿足後）

| 參數 | 規格 |
|------|------|
| 形式 | Creatine monohydrate，Creapure + NSF/Informed Sport |
| 劑量 | **3–5 g/d，不做 loading** |
| 時機 | 早餐後或運動後，隨碳水+蛋白 |
| 體重追蹤 | 前 6 週改看**體脂%/VFL**，非體重秤 |
| Washout（腎臟科/健檢前） | **≥4 週（保險 6 週）**；務必告知醫師正在/曾用 creatine，要求加驗 cystatin C |
| 試行 | 8 週 → 評估 |

### 9.3 認知用法（選配，與肌肉劑量分開）

- 慢性 3–5 g/d 對腦效益微弱（Fazio 2023 null）。
- **急性救援**（重大睡眠剝奪日）：0.2–0.35 g/kg 單劑，須先低劑量試 GI 耐受。**非每日**。

### 9.4 8 週評估指標

| 指標 | 預期 | 判讀 |
|------|------|------|
| 阻力訓練 1RM | +5–15% | 主要效益 |
| 體脂% / VFL | 持平或微降 | 真實體組成（非體重秤） |
| 跑步配速（同 HR） | 前 2 週微慢、4 週適應 | 已知 trade-off |
| 血清 creatinine（停 4 週後） | 回 baseline | 確認非腎損 |
| cystatin C-eGFR | 不變 | 真實腎功能 |
| 血清 UA | 不變（理想 <6） | 確認非新增風險 |

### 9.5 停止條件

任一發生 → 停用 + 醫療評估：停藥 4 週後 creatinine 仍 >1.3；UA 較 baseline 明顯上升；新增 NSAID/ACE inhibitor 前重新評估。

---

## 十、底線結論

1. **證據總量上，creatine 是低風險、肌力與認知韌性有 RCT 支撐的增益層**，與你 OSA/HRV/血壓核心議題正交。
2. **對你個人，兩個進行中議題使「先緩啟動」的結論更穩固**：(a) 腎臟科 baseline 未取得 + UA 8.9 緩衝為零；(b) 減重靠每日體重訊號，水重會反訊號。
3. **真實 GFR 安全已被實測 GFR 的 RCT 充分建立**；威脅只是「血清 creatinine 解讀干擾」 → 用 cystatin C + washout ≥4 週解決。
4. **啟動採無 loading 3–5g monohydrate（Creapure/NSF）**；骨密度與 Zone-2 跑步別期待效益。
5. **前篇（2026-05-19）兩處修正**：年齡框架 mid-40s → **37 歲**（移除中年/抗老化框架）；washout 5–7 天 → 取腎臟科 baseline 用 **≥4 週**。

---

## 參考文獻（依領域）

### 認知 / 睡眠剝奪
1. Gordji-Nejad A et al. (2024) *Sci Rep* 14:4937. https://pmc.ncbi.nlm.nih.gov/articles/PMC10902318/
2. Gordji-Nejad A et al. (2025) *Nutrients* 18(8):1192. https://www.mdpi.com/2072-6643/18/8/1192
3. Xu C et al. (2024) *Front Nutr* 11:1424972. https://pmc.ncbi.nlm.nih.gov/articles/PMC11275561/
4. Prokopidis K et al. (2023) *Nutr Rev*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9999677/
5. Fazio L et al. (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10647179/
6. Moriarty TA et al. (2023) *Brain Sci* 13(9):1276. https://pmc.ncbi.nlm.nih.gov/articles/PMC10526554/
7. Dechent P et al. (1999) *Am J Physiol* 277:R698. https://pubmed.ncbi.nlm.nih.gov/10484486/
8. EFSA Panel (2024). https://pmc.ncbi.nlm.nih.gov/articles/PMC11574456/

### 肌力 / 瘦肉量 / 骨密度
9. Wang CC et al. (2024) *Nutrients* 16(21):3665. https://pmc.ncbi.nlm.nih.gov/articles/PMC11547435/
10. Ashtary-Larky D et al. (2025) *JISSN*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12777911/
11. Desai I et al. (2024) *J Strength Cond Res*. https://pubmed.ncbi.nlm.nih.gov/39074168/
12. Backx EMP et al. (2017) *Sports Med*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5507980/
13. Forbes SC, Chilibeck PD, Candow DG (2018) *Front Nutr* 5:27. https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00027/full
14. Chilibeck PD et al. (2023) *Med Sci Sports Exerc*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10487398/
15. Liu X et al. (2025) *Eur Rev Aging Phys Act*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12752335/
16. Burke R et al. (2023) *Nutrients*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10180745/

### 腎功能 / 安全
17. Lugaresi R et al. (2013) *JISSN*. https://pmc.ncbi.nlm.nih.gov/articles/PMC3661339/
18. Gualano B et al. (2008) *Eur J Appl Physiol*. https://pubmed.ncbi.nlm.nih.gov/18188581/
19. Gualano B et al. (2010) *Am J Kidney Dis* (單腎). https://www.ajkd.org/article/S0272-6386(09)01459-0/abstract
20. Kreider RB et al. (2003) *Mol Cell Biochem* 244:95. https://link.springer.com/article/10.1023/A:1022469320296
21. Pinto CL et al. (2023) *Nutrients* 15(6):1466. https://pmc.ncbi.nlm.nih.gov/articles/PMC10054094/
22. BMC Nephrology meta (2025). https://link.springer.com/article/10.1186/s12882-025-04558-6
23. Kreider RB et al. (2017) ISSN Position Stand, *JISSN* 14:18. https://pmc.ncbi.nlm.nih.gov/articles/PMC5469049/

### 尿酸
24. Percário S et al. (2012) *JISSN* 9:56. https://pmc.ncbi.nlm.nih.gov/articles/PMC3543170/
25. Bellinger BM et al. (2000) *Acta Physiol Scand* 170(4):217. https://pubmed.ncbi.nlm.nih.gov/11167307/
26. Li X et al. (2024) *Front Nutr* (Mendelian Randomization). https://pmc.ncbi.nlm.nih.gov/articles/PMC11232645/

### 心血管代謝
27. Gualano B et al. (2011) *Med Sci Sports Exerc* 43(5):770 (T2D). https://pubmed.ncbi.nlm.nih.gov/20881878/
28. Solis MY et al. (2021) *Nutrients* 13(2):570. https://pmc.ncbi.nlm.nih.gov/articles/PMC7915263/
29. Sanchez-Gonzalez MA et al. (2011) *Eur J Appl Physiol*. https://pubmed.ncbi.nlm.nih.gov/21249385/
30. de Moraes R et al. (2014) *Nutr J*. https://pubmed.ncbi.nlm.nih.gov/25511659/
31. Antonio J et al. (2024) Part II misconceptions, *JISSN*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11703406/

### 有氧 / 體重 / 水分
32. Gras D et al. (2021/2023) *Crit Rev Food Sci Nutr* (VO2max meta). https://pubmed.ncbi.nlm.nih.gov/34859731/
33. Forbes SC, Candow DG et al. (2023) *JISSN* (endurance). https://pmc.ncbi.nlm.nih.gov/articles/PMC10132248/
34. Beis LY et al. (2011) *JISSN* (running economy). https://pmc.ncbi.nlm.nih.gov/articles/PMC3283512/
35. Kutz MR, Gunter MJ (2003) *J Strength Cond Res*. https://pubmed.ncbi.nlm.nih.gov/14636103/
36. Lopez RM et al. (2009) *J Athl Train* (熱調節 meta). https://pmc.ncbi.nlm.nih.gov/articles/PMC2657025/
37. Antonio J et al. (2021) misconceptions, *JISSN*. https://pmc.ncbi.nlm.nih.gov/articles/PMC7871530/

### 劑量 / 形式
38. Jagim AR et al. (2012) *JISSN* 9:46 (Kre-Alkalyn). https://pmc.ncbi.nlm.nih.gov/articles/PMC3500725/
39. Spillane M et al. (2009) *JISSN* 6:6 (CEE). https://link.springer.com/article/10.1186/1550-2783-6-6
40. Antonio J, Ciccone V (2013) *JISSN* 10:36 (timing). https://pmc.ncbi.nlm.nih.gov/articles/PMC3750511/
41. Ostojić SM, Ahmetović Z (2008) *Res Sports Med* 16(1):15 (GI). https://pubmed.ncbi.nlm.nih.gov/18373286/
42. Longobardi I et al. (2025) *Front Nutr* 12:1682746 (safety review). https://pmc.ncbi.nlm.nih.gov/articles/PMC12702719/

---

*Filed: articles/diet-nutrition/2026-06-03-creatine-comprehensive-rct-review.md*
*方法：七個平行研究 agent（PubMed/PMC/Cochrane/JISSN/Frontiers/Nature SR/MDPI）+ adversarial verification。Author drafted in Claude Code Copilot Mode; 臨床決策（尤其腎臟科 baseline 與 urate 管理）須經醫師審核。*
*前篇保存：[2026-05-19-creatine-glycine-supplement-evaluation.md](2026-05-19-creatine-glycine-supplement-evaluation.md)*
