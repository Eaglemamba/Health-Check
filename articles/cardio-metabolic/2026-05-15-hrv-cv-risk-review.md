# 夜間 HRV 偏低作為獨立心血管風險指標：19.7 ms 代表什麼，以及如何應對

*建檔：2026-05-15*
*前置：[Z2 訓練量與 RHR 降階分析（2026-05-13）](2026-05-13-weight-stall-z2-rhr-analysis.md) ｜ [OSA 深度調查（2026-04-30）](../osa-sleep/2026-04-30-osa-investigation-deep-dive.md)*

---

## 一、為何這對你特別重要

這份文章的起點不是「HRV 低在人群中代表什麼」，而是一個更具體的問題：**19.7 ms 的 avgOvernightHrv，在你的 ECG 已顯示 LVH + biatrial enlargement + 疑似重度 OSA 的背景下，是同一個病理基底的反映，還是獨立的訊號？**

**你的當前臨床輪廓（2026-05-15 基準）：**

| 指標 | 數值 | 意義 |
|------|------|------|
| avgOvernightHrv | **19.7 ms**（27 晚均值，範圍 17–22 ms，CV 7.5%） | 長期穩定偏低，無急性波動 |
| LVH | ECG 確認，病程 11 年（自 2015 年） | 慢性心肌重塑 |
| Biatrial enlargement | 2026-03-25 ECG 新增 | 新增的電氣重塑訊號 |
| Anterior ST elevation | 2026-03-25 ECG 新增 | 待 echo 排除結構性因素 |
| Suspected OSA | SpO2 nadir < 88%（27/27 晚），最差單晚 T90 12.1% | 重度夜間缺氧 |
| BP | W19 週均 < 130，最近 122/69 | 目前控制中 |
| 尿酸 | 8.9 mg/dL（果糖性，約 2026-04 起介入） | 缺氧代謝副產品 |
| BMI / 體脂 | 22 / 19.5% | 非肥胖型 |

**核心論點：**

LVH + biatrial enlargement + 夜間低 HRV，三者共享一個自主神經基底——**長期交感神經主導 + 迷走神經退縮**。這不是三個獨立問題，而是同一個 autonomic substrate 的三個面向。OSA 是這個過程最大的可治療驅動因子。

低 HRV 在此不只是「壓力指標」，而是你已知心臟重塑綜合徵的電生理伴隨訊號，同時本身也是獨立的心血管事件預測因子。

---

## 二、19.7 ms 在人群分布中的位置

### 2.1 RMSSD 參考值：Nunan 2010 系統性回顧

Nunan et al. 對 44 項研究（共 21,438 名健康成人）進行 meta-analysis，建立短時 HRV 常模 **(Nunan 2010, Pacing Clin Electrophysiol)**：

| 統計量 | RMSSD（ms）|
|--------|----------:|
| 均值 | **42** |
| 標準差 | 15 |
| 範圍（約 5th–95th pct）| **19 – 75** |

健康成人 35–40 歲男性的 5 分鐘短時 RMSSD 大致落在 **35–50 ms** 區間（中位數約 38–42 ms）；夜間長時窗口的 RMSSD 通常略高於日間短時測量，因為夜間副交感張力較高。

**你的 19.7 ms 落在哪裡：**

以健康成人均值 42 ms、SD 15 ms 計算：

```
Z-score = (19.7 - 42) / 15 = -1.49
對應約第 7 百分位
```

意即：**同年齡層約 93% 的健康成人 RMSSD 高於你目前的水準。**

> **重要限制**：Nunan 2010 是短時（5 分鐘）日間測量的常模，不是直接可比的夜間 Garmin avgOvernightHrv。夜間 RMSSD 通常較高，但對應的年齡常模資料庫較少。方向性判斷不變：19.7 ms 在任何參考框架下都屬於偏低端。

### 2.2 Garmin avgOvernightHrv 的測量方法與限制

Garmin Vivoactive 5 使用 **PPG（光體積描記法）+ Enhanced BBI 演算法**，計算睡眠中穩定期的 5 分鐘 RMSSD 窗口，取多個窗口平均後輸出 avgOvernightHrv。

| 特性 | 說明 |
|------|------|
| 物理量測原理 | 腕部 PPG 感測光反射變化 → 推算 Pulse Rate Variability（PRV） |
| HRV 指標 | **RMSSD 近似值**（非直接 R-R interval，而是 pulse-to-pulse interval） |
| 系統性偏差 | Enhanced BBI 驗證研究顯示：vs 胸帶 ECG，均值偏差約 **+8 ms**（PPG 天然略高於 ECG-derived HRV）**(Labfront/Garmin Enhanced BBI 驗證報告)** |
| 夜間移動干擾 | 演算法排除高移動期，僅取高信心片段 |
| 偽低值風險 | 睡眠翻身頻繁、手腕彎曲、感測器壓迫均可造成偽低 |

**研究可比性判斷：**

若考量 +8 ms 偏差，你的「真實 ECG-equivalent RMSSD」估計約為 **19.7 − 8 = 11.7 ms**（保守）至 **19.7 ms**（名目值）。

無論哪個方向，19.7 ms 在 Garmin 用戶群中代表顯著偏低。更重要的是：**27 晚 CV 7.5% 的極低夜間變異性，本身就是慢性生理壓制的訊號**——健康人的 HRV 應有較大的日間波動，反映自律神經對環境/睡眠的動態調節；你的 HRV 幾乎是一條水平線（17–22 ms），表示調節能力已受長期損耗。

---

## 三、低 HRV 作為獨立心血管風險指標：關鍵文獻

### 3.1 Hillebrand 2013 — 無已知 CVD 人群的首發心血管事件

**(Hillebrand et al., Europace 2013;15(5):742-749)**

- 8 項研究，21,988 名無已知 CVD 的人群
- 主要指標：SDNN（24 小時）
- **最低 vs 最高 SDNN 分位：pooled RR = 1.35（95% CI 1.10–1.67）**
- LF 成分：RR = 1.45（1.12–1.87）
- HF 成分：RR = 1.32（0.96–1.81，接近顯著）
- 劑量反應 meta-regression：SDNN 第 10 百分位 vs 第 50 百分位 → RR = 1.50（1.22–1.83）
- **結論：SDNN 偏低（最低分位）與首發心血管事件風險增加 32–45% 相關**

> **注意**：此研究使用 SDNN，非直接 RMSSD。兩者相關但代表不同面向（SDNN 反映整體 HRV；RMSSD 主要反映副交感/迷走活性）。低 SDNN 通常伴隨低 RMSSD，但不是完全等價。

### 3.2 Tsuji 1994 — Framingham 長者族群全因死亡率

**(Tsuji et al., Circulation 1994;90(2):878-883)**

- 736 名 Framingham Heart Study 老年受試者（平均年齡 72 ± 6 歲）
- 4 年追蹤期，74 例死亡
- **LF 功率每下降 1 SD → 全因死亡風險 HR 1.70（95% CI 1.37–2.09）**
- SDNN 下降同樣顯著預測死亡率（P = .0019）
- HRV 提供的預後資訊**獨立於傳統風險因子之外**

### 3.3 Tsuji 1996 — Framingham 心臟事件

**(Tsuji et al., Circulation 1996;94(11):2850-2855)**

- 2,501 名無冠心病或心衰的 Framingham 受試者（平均年齡 53 歲）
- 平均追蹤 3.5 年，58 例心臟事件
- 低 HRV（多個頻域及時域指標）獨立預測心臟事件發生

### 3.4 La Rovere 1998 ATRAMI — 心肌梗塞後心臟死亡率

**(La Rovere et al., Lancet 1998;351(9101):478-484)**

- 1,284 名近期 MI（< 28 天）患者，前瞻性多中心研究
- **SDNN < 70 ms → 心臟死亡多變量 RR 3.2（95% CI 1.42–7.36）**
- 兩者同低時（SDNN < 70 ms + BRS < 3.0 ms/mmHg）：2 年死亡率 **17%** vs 兩者正常時 **2%**
- 合併低 LVEF（< 35%）：RR 升至 **6.7（3.1–14.6）**

### 3.5 Bigger 1992 — 心肌梗塞後頻域 HRV 與總死亡率

**(Bigger et al., Circulation 1992;85(1):164-171)**

- 時域指標截斷值：SDNN < 70 ms，RMSSD < 17.5 ms，NN50+ < 200/24h
- 低 HRV 可識別高總死亡風險患者，各指標獨立預測力：NN50+ RR 3.5，SDNN RR 3.0，**RMSSD RR 2.8**
- **RMSSD < 17.5 ms 是本研究中預測死亡的切斷點**

> **你的 19.7 ms 與 Bigger 1992 的 RMSSD 切斷點 17.5 ms 僅差 2.2 ms**。雖然這是 post-MI 高危族群的截斷值，不直接適用於你的情境，但其接近程度值得注意。

### 3.6 量化風險含義

基於現有文獻的整合性推算（需謹慎詮釋，非個體預測）：

| 比較 | 估計風險增幅 | 來源 |
|------|------------|------|
| SDNN 最低 vs 最高分位（一般人群，首發 CV 事件）| +32–45% | Hillebrand 2013 |
| LF 功率每↓1 SD（老年族群，全因死亡）| +70% | Tsuji 1994 |
| SDNN < 70 ms（post-MI，心臟死亡）| RR 3.2 | La Rovere 1998 |
| RMSSD < 17.5 ms（post-MI，總死亡）| RR 2.8 | Bigger 1992 |

> **重要caveat**：這些風險估計來自不同族群（部分為老年或 post-MI），且是 SDNN（24h），非直接的 Garmin RMSSD。你的情境（37 歲，非 post-MI）的絕對風險遠低於上述數字。低 HRV 是**風險指標**，不是確定性預測。

---

## 四、LVH + Biatrial Enlargement + 低 HRV：共享的自主神經基底

### 4.1 共同機轉圖

```
長期慢性壓力源（高血壓、OSA、代謝負荷）
          ↓
    交感神經持續高張
    迷走神經撤退（vagal withdrawal）
          ↓
    ┌──────────────────────────────────┐
    │           三重並行表現            │
    │                                  │
    │  LVH                HRV 降低      │
    │  心肌細胞肥大        RMSSD ↓       │
    │  心室壁增厚          副交感張力 ↓  │
    │                                  │
    │  Biatrial enlargement             │
    │  心房容積增加                     │
    │  心房機械性重塑                   │
    └──────────────────────────────────┘
```

### 4.2 LVH 與低 HRV 的直接關聯

Mandawat et al. 的研究確認，LVH 患者（高血壓性及瓣膜性）HRV 顯著低於對照組（P < 0.001），且呈**連續性反比關係**：LV mass index 越高，HRV 越低（r = −0.478）**(Mandawat et al., Br Heart J 1995;73(2):139-144)**。

機轉：
- 心肌肥厚 → 心臟機械受器（mechanoreceptor）反應性下降 → 迷走傳入訊號減弱
- 高血壓狀態下壓力感受器反射（baroreflex）長期敏感性下降
- 腎素-血管緊張素-醛固酮系統活化 → 交感神經增益

### 4.3 Biatrial Enlargement 的形成與自主神經

Biatrial enlargement 的根因是**心房機械性負荷長期增加**（高血壓、LVH 導致的左室順應性下降、OSA 反覆增加右心後負荷）。在自主神經層面：

- 慢性交感過度活化 → 心房肌細胞直接腎上腺素受器刺激 → 心房重塑、纖維化、電傳導改變
- 交感神經過度支配（sympathetic hyperinnervation）是心房擴大後的典型伴隨現象
- 這個過程同時抑制副交感傳入 → 進一步降低 HRV（尤其是 HF 成分）

> **不過度解讀因果**：目前無法確定是 LVH「導致」低 HRV，或是兩者都是同一慢性壓力源的並行下游結果。更合理的框架是：**它們共享一個 autonomic substrate，相互強化，而非線性因果鏈。**

### 4.4 OSA 在這個圖像中的位置

OSA 是可能的**主要可治療驅動因子**，同時上游影響 LVH、biatrial enlargement、低 HRV 三者：

- 每次呼吸中斷 → 大腦偵測高 CO₂/低 O₂ → 強制交感激增（sympathetic surge）
- 反覆夜間缺氧 → 慢性交感神經系統激活 → 血壓升高、心肌肥厚加速
- 間歇性缺氧 → 系統性氧化壓力 → 心房肌細胞直接損傷
- 夜間反覆微清醒 → 完全抑制副交感 rebound → 夜間 RMSSD 無法恢復

你的 27 晚 avgOvernightHrv 之所以如此穩定偏低（17–22 ms，CV 7.5%），部分原因可能正是每晚重複的 OSA 事件抑制了夜間副交感恢復。

---

## 五、OSA × HRV 交互作用

### 5.1 OSA 如何急性降低夜間 HRV

每次阻塞性呼吸暫停事件的自主神經反應序列：

1. 氣道塌陷 → SpO₂ 下降 → 化學受器激活
2. 交感神經爆發 → 心率上升 3–5 bpm
3. 微清醒（arousal）恢復氣道張力
4. 過度換氣（rebound hyperpnea）→ 心率 + 心率變異短暫出現
5. 迷走張力尚未完全回復即進入下一個事件循環

結果：**夜間 RMSSD 被反覆抑制，無法在睡眠中自然回升到健康基線。**

Narkiewicz & Somers 的研究顯示，OSA 患者即使在清醒靜息狀態下肌肉交感神經活性（MSNA）也顯著高於對照組，且 baroreflex 控制受損 **(Narkiewicz, Somers et al., Hypertension 1998;32(6):1039-1043)**。

### 5.2 CPAP 治療後的 HRV 恢復

Jiang et al. 的 meta-analysis（11 項 cohort 研究）顯示，CPAP 治療可改善自主神經活性的交感-副交感平衡：off-CPAP 測量的 HF 功率顯著上升（SMD 0.31，95% CI 0.02–0.60，P = .034），LF 在 CPAP 使用中下降，代表交感張力減低 **(Jiang et al., Heart Lung 2018;47(5):516-524)**。

**重要含義：**
- HRV 改善可能**不需要**任何 CV 藥物，僅靠 OSA 治療即可出現
- CPAP 啟動後 1–3 個月是第一個可靠的 HRV 再評估時間點
- 即使 HRV 未完全正常化，方向性改善也代表自主神經功能在恢復

### 5.3 HRV 是 OSA 治療效果的客觀生物標記

如果 CPAP（或 MAD）啟動後：
- avgOvernightHrv **上升 ≥ 3 ms** → 有意義的治療反應
- avgOvernightHrv 無變化 → 考慮 CPAP 壓力設定不足或仍有殘餘 OSA（AHI > 5）
- **19.7 ms 是你目前的 CPAP 前基準，3 個月後的數值直接反映治療效果**

---

## 六、可移動 HRV 的介入：以證據等級排序

以下效應量來自近期 meta-analysis，以 RMSSD 毫秒或 SMD 表示。請注意：在你目前 OSA + 睡眠剝奪的狀態下，單項介入效果會被 OSA 部分抵消。

### 6.1 強效據（多項 RCT 或 meta-analysis 支持）

| 介入 | 預期 RMSSD 增量 | 時程 | 關鍵文獻 |
|------|----------------|------|---------|
| **有氧訓練（Zone 2，≥ 150 min/週）** | SMD 0.84（約 +7–12 ms 估計） | 12–16 週 | Amekran & El Hangouche, Cureus 2024（16 RCTs，623 受試者）；HRV 引導式訓練見 Manresa-Rocamora, IJERPH 2021（SMD 0.50）|
| **OSA 治療（CPAP/MAD）** | HF 顯著上升（SMD 0.31 off-CPAP） | 4–12 週 | Jiang et al., Heart Lung 2018 |
| **睡眠總時長 ≥ 7h（TST 延長）** | 間接機轉：降低夜間交感負荷 | 立即 | 睡眠剝奪文獻共識 |
| **戒酒 / 限酒** | 夜間 HRV 急性上升明顯 | 立即–1 週 | 多項觀察性研究 |

> 有氧訓練的 SMD 0.84 屬中到大效應；絕對 ms 數值因基線而異，起點越低通常增量空間越大。

### 6.2 中等證據（小型 RCT 或觀察性研究支持）

| 介入 | 預期效果 | 時程 | 關鍵文獻 |
|------|---------|------|---------|
| **慢速呼吸 5–6 次/分鐘，每天 2×5 min** | 急性 RMSSD 上升；慢性 HF 功率改善 | 急性立即；慢性 4–8 週 | Russo et al., Breathe 2017;13:298-309 |
| **體重減輕（> 5%）** | 代謝負荷下降 → 自主神經改善 | 2–3 個月 | 間接路徑 |
| **避免深夜進食（< 睡前 2h）** | 減少夜間消化代謝負荷 | 立即 |  |

**慢速呼吸機轉**：6 次/分鐘呼吸使吸氣-呼氣週期與 baroreflex 自然頻率（Mayer wave，~0.1 Hz）共振，最大化呼吸竇性心律不整（RSA），是 HF 功率的直接上調機制。效果可在第一次練習後就測量到，但要轉化為靜息 HRV 基線改善需要數週規律執行。

### 6.3 混合/弱證據（不建議單獨依賴）

| 介入 | 現有證據 | 說明 |
|------|---------|------|
| 冥想 / 正念 | 小效應，研究異質性高 | 不反對，但不是主力 |
| Magnesium 補充 | 部分研究顯示 HF 功率改善，效應小 | 可作為支持性補充，非主力 |
| Omega-3 補充 | 一些訊號但效應小且不一致 | 同上 |
| **單純 HRV biofeedback app（無慢速呼吸）** | 幾乎無效 | 需要搭配實際呼吸節律訓練，單純看 app 數字無益 |

---

## 七、監測實務

### 7.1 你的數字雜訊有多大

27 晚的 avgOvernightHrv：

| 統計量 | 數值 |
|--------|------|
| 均值 | 19.7 ms |
| 範圍 | 17–22 ms |
| CV | 7.5% |
| 日間標準差估計 | ~1.5 ms |

CV 7.5% 在一般人群是**非常低的**——健康人通常 CV 15–30%，代表自律神經有更多動態調節。你的數字呈現慢性「鎖死」，反映持續壓制狀態，同時也意味著**日間波動本身就是一個有用的介入反應指標**（如果 CV 從 7.5% 上升到 12–15%，代表自律神經的動態調節能力在恢復）。

### 7.2 避免單晚解讀，用 7 天或 28 天 rolling mean

| 時間窗口 | 適用判斷 |
|---------|---------|
| 單晚 | 僅供參考，雜訊高（飲食、壓力、睡前活動） |
| **7 天 rolling mean** | **日常趨勢監測，最實用** |
| **28 天 rolling mean** | 介入效果評估（每 4 週比較一次） |

### 7.3 主要干擾因子（需同步記錄）

| 干擾因子 | 對 HRV 的影響 | 記錄建議 |
|---------|-------------|---------|
| 酒精（≥ 1 標準杯，< 睡前 4h）| 急性 RMSSD -5 至 -10 ms | daily.md 記錄 |
| 晚餐 > 20:30 | HRV 輕度下降（消化代謝） | food.md 時間戳 |
| 急性疾病/發燒 | 顯著下降，數天持續 | 症狀記錄 |
| 高強度訓練前一日 | 隔夜 HRV 通常下降 | exercise log |
| 長途飛行 / 時差 | 數天恢復期 | 旅遊記錄 |

### 7.4 里程碑目標

| 時間點 | 目標 avgOvernightHrv（7 天均） | 條件 |
|--------|-------------------------------|------|
| 現在（基準） | 19.7 ms | 27 晚確立 |
| **2026-08（+3 個月）** | **23–25 ms** | CPAP 啟動 + Z2 訓練啟動 |
| **2026-11（+6 個月）** | **27–32 ms** | CPAP + 150 min/週 Z2 + TST ≥ 7h |
| 長期目標（12 個月）| 32–38 ms | 多項介入協同效果 |

> **19.7 → 35 ms** 需要多項介入同時見效，時程 9–12 個月，不是 3 個月可以期望的。**短期目標是先破 25 ms**，這在 CPAP + 規律 Z2 組合下有合理文獻支持。

---

## 八、行動決策樹

### 8.1 立即可做（無需 PSG 結果）

**[A] Z2 有氧訓練**
- 超慢跑 180 spm 或 Karvonen Z2（133–146 bpm）
- Phase 1：3×20 min/週
- Phase 2（2 週後）：4×30 min/週 = **120 min/週**
- Phase 3（CPAP 啟動後）：5×30 min/週 = **150 min/週**
- *HRV 效果期望：12 週後 +5–10 ms；依 OSA 治療是否啟動而異*

**[B] 慢速呼吸 5–6 次/分鐘**
- 每天 2 次 × 5 分鐘，建議晨起 + 睡前
- 工具：Garmin 內建呼吸訓練，或 Breathwrk / Prana Breath app
- 吸氣 5 秒 / 呼氣 5 秒（4 次/分鐘也可；5–6 最接近 resonance frequency）
- *急性效果立即可見；慢性 HF 基線改善需 4–8 週*

**[C] 睡眠時長硬目標**
- TST ≥ 7h（21:30 上床、22:00 熄燈）
- 睡眠剝奪是 HRV 的即時抑制因子，延長 TST 是成本最低的介入

### 8.2 PSG 後（若確認 OSA）

| 結果 | 行動 | HRV 監測節點 |
|------|------|------------|
| AHI 5–15（輕度）| MAD（SomnoDent / Narval CC）首選 | 啟動後 1 個月、3 個月 |
| AHI 15–30（中度）| CPAP 優先，不耐受者 MAD | 同上 |
| AHI > 30（重度）| CPAP 直接啟動 | 啟動後 1 個月、3 個月 |

**評估指標：CPAP 啟動後 4 週，avgOvernightHrv 7 天均值是否上升 ≥ 2 ms。**

### 8.3 Echo + 24h Holter 結果後

| 結果 | 含義 | 行動調整 |
|------|------|---------|
| Echo 確認 LVH，LVEF 正常（> 55%） | 結構性重塑已建立，但功能保留；Z2 訓練安全 | 維持現行計畫，心臟科追蹤 |
| LVEF 下降（< 50%） | 心臟功能受損，Z2 強度需醫師評估 | 停 Z2 等心臟科意見 |
| Holter：頻繁 VPB 或 SVT | 心律失常風險 | 心臟科評估再啟動運動計畫 |
| ST elevation 原因確認（心包炎 / vasospasm / 早期復極） | 良性 vs 需治療 | 依診斷調整 |

### 8.4 3 個月回顧（2026-08 節點）

| 指標 | 目標 | 若未達目標 |
|------|------|----------|
| avgOvernightHrv 7天均 | ≥ 23 ms | 確認 CPAP 依從性、Z2 實際執行量 |
| HRV CV | > 10%（動態調節恢復訊號）| 同上 |
| RHR | ≤ 53 bpm | 若 CPAP 已啟動但未降：確認 AHI residual |
| SpO2 夜間最低值（CPAP 使用中）| ≥ 90% | CPAP 壓力設定複診 |

---

## 九、本文核心結論

1. **19.7 ms 屬於健康成人分布的第 7 百分位（約），並且在 27 晚中幾乎沒有波動（CV 7.5%）——這是慢性自主神經壓制的特徵，不是正常低值。**

2. 你的 LVH + biatrial enlargement + 低 HRV 三者呈現一個共同的 autonomic substrate：長期交感主導 + 迷走退縮。不要將它們當作三個獨立問題分別處理。

3. 低 HRV 是獨立的心血管事件預測因子（Hillebrand 2013），獨立於已知 CV 風險因子之外。結合你既有的 LVH，理由充分支持積極介入。

4. **OSA 治療是最大的單一可逆驅動因子。** CPAP 啟動後的 HRV 軌跡會直接告訴你自主神經系統的恢復狀況——這是 CPAP 依從性的生物指標，比主觀感受更客觀。

5. 在 PSG 結果出來之前，Z2 訓練 + 慢速呼吸 + TST ≥ 7h 三者可以同步啟動，無安全疑慮（除非 Echo/Holter 有特殊發現）。

6. 目標設定：**19.7 ms → 25 ms（3 個月）→ 30+ ms（6–9 個月）**，這個軌跡需要 CPAP + 運動 + 睡眠三箭並發，缺任何一個都會減緩進度。

---

## 引用來源

1. Hillebrand S, et al. Heart rate variability and first cardiovascular event in populations without known cardiovascular disease: meta-analysis and dose-response meta-regression. *Europace* 2013;15(5):742-749. PMID: 23370966.

2. Tsuji H, Venditti FJ Jr, Manders ES, et al. Reduced heart rate variability and mortality risk in an elderly cohort: the Framingham Heart Study. *Circulation* 1994;90(2):878-883. PMID: 8044959.

3. Tsuji H, Larson MG, Venditti FJ Jr, et al. Impact of reduced heart rate variability on risk for cardiac events: the Framingham Heart Study. *Circulation* 1996;94(11):2850-2855. PMID: 8941112.

4. La Rovere MT, Bigger JT Jr, Marcus FI, Mortara A, Schwartz PJ; ATRAMI (Autonomic Tone and Reflexes After Myocardial Infarction) Investigators. Baroreflex sensitivity and heart-rate variability in prediction of total cardiac mortality after myocardial infarction. *Lancet* 1998;351(9101):478-484. PMID: 9482439.

5. Bigger JT, Fleiss JL, Steinman RC, Rolnitzky LM, Kleiger RE, Rottman JN. Frequency domain measures of heart period variability and mortality after myocardial infarction. *Circulation* 1992;85(1):164-171.

6. Nunan D, Sandercock GRH, Brodie DA. A quantitative systematic review of normal values for short-term heart rate variability in healthy adults. *Pacing Clin Electrophysiol* 2010;33(11):1407-1417. PMID: 20663071.

7. Mandawat MK, Wallbridge DR, Pringle SD, et al. Heart rate variability in left ventricular hypertrophy. *Br Heart J* 1995;73(2):139-144. PMID: 7696023.

8. Narkiewicz K, Somers VK. Baroreflex control of sympathetic nerve activity in obstructive sleep apnea. *Hypertension* 1998;32(6):1039-1043.

9. Jiang J, Zhao P, Deng H. The impact of continuous positive airway pressure on heart rate variability in obstructive sleep apnea patients during sleep: a meta-analysis. *Heart Lung* 2018;47(5):516-524. PMID: 30031552.

10. Amekran Y, El Hangouche AJ. Effects of exercise training on heart rate variability in healthy adults: a systematic review and meta-analysis of randomized controlled trials. *Cureus* 2024;16(6):e62465. PMID: 39015867.

11. Manresa-Rocamora A, Sarabia JM, Javaloyes A, Flatt AA, Moya-Ramón M. Heart rate variability-guided training for enhancing cardiac-vagal modulation, aerobic fitness, and endurance performance: a methodological systematic review with meta-analysis. *Int J Environ Res Public Health* 2021;18(19):10299. PMID: 34639599.

12. Russo MA, Santarelli DM, O'Rourke D. The physiological effects of slow breathing in the healthy human. *Breathe (Sheff)* 2017;13(4):298-309. PMID: 29209423.

13. Labfront. Garmin Enhanced BBI: HRV accuracy validation. Technical report, 2023. Available at: https://www.labfront.com/article/garmin-enhanced-bbi-hrv-accuracy-validation

---
**附注（引用#11 Manresa-Rocamora vs #10 Amekran 的區別）：**
Manresa-Rocamora 2021 研究的是「以 HRV 數值動態排程訓練」是否優於固定計畫，而非「有氧訓練是否提升 HRV」。兩者均引用；第六節 6.1 的 RMSSD 效應量來自 Amekran 2024 meta-analysis（直接量測有氧訓練 → HRV 提升）；Manresa-Rocamora 2021 支持 HRV 引導式訓練在提升副交感 HRV 指標方面優於固定計畫（SMD 0.50）。

---

*Filed: articles/cardio-metabolic/2026-05-15-hrv-cv-risk-review.md*
*作者：David Kuo + Claude Sonnet 4.6（協作分析）*
*基準資料：Garmin avgOvernightHrv 27 晚（2026-04-18 ~ 2026-05-14）、ECG 2026-03-25、articles/osa-sleep/2026-04-30-osa-investigation-deep-dive.md*
