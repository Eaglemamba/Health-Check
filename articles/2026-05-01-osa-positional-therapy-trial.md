# OSA 體位治療（Positional Therapy）試驗設計與預期效益

*建立日期：2026-05-01*
*前置文件：[2026-04-30-osa-investigation-deep-dive.md](./2026-04-30-osa-investigation-deep-dive.md)*
*資料源：58 晚 Garmin SpO2 epoch-level data（`reviews/spo2_desat_trend.png`）*

---

## 一、為什麼要做這個試驗

### 個人現況（截至 2026-05-01）

| 指標 | 58 晚平均 | 紅旗夜佔比 |
|---|---|---|
| 最低 SpO2 | 82.3% | < 88% 佔 86% 夜晚 |
| T90（SpO2<90% 時間佔比） | 15.7% | ≥ 10% 重度佔 60% 夜晚 |
| 最長單一 desat event | 19.8 分 | ≥ 15 分佔 59% 夜晚 |
| 4/29-5/1 連 3 晚最低 SpO2 | 79% / 79% / 79% | OSA 強紅旗 cluster |

### 表現型推論：lean POSA

符合「亞洲非肥胖型 + 姿勢相關 OSA（POSA）」的所有特徵：

1. **BMI 24.5** — 排除典型肥胖型 OSA
2. **最深 desat 出現在補眠夜（TST ≥ 7h）** — REM rebound 暴露效應，而 REM 期間咽喉肌張力最低
3. **Fexofenadine 180mg 改善鼻塞主觀感受但 SpO2 未改善** — 排除上呼吸道單純鼻腔阻塞，主因是咽喉/舌根塌陷
4. **連續 3 晚 79% cluster** — 通常代表近期睡姿偏向 supine（仰睡）

POSA 在亞洲非肥胖 OSA 族群盛行率 ~50-60%（vs 西方肥胖型 ~25%）。

---

## 二、體位治療文獻基線改善幅度

### 一般 POSA 族群（混合 BMI）

| 指標 | 仰睡 → 側睡平均改善 | 主要文獻 |
|---|---|---|
| AHI | **下降 50-60%** | Joosten 2014 (Sleep Med Rev) |
| 最低 SpO2 | **回升 3-5 點**（如 79% → 83-84%） | Oksenberg 系列 |
| T90 | **下降 40-70%** | Cartwright 1984 + 後續驗證 |
| 最長 event | **縮短 30-50%** | Ravesloot 2013 |

### 床頭抬高（Souza 2017）

| 抬高角度 | AHI 下降 | 備註 |
|---|---|---|
| 7.5 度 | ~30% | 容易執行 |
| 15 度 | ~50% | 接近側睡效益 |
| 30 度 | ~60%（半坐臥） | 影響睡眠品質 |

### 個人預期改善（lean POSA + REM-dominant + 中-重度推估）

| 指標 | 目前 58 晚平均 | 純側睡推估 | 改善幅度 |
|---|---|---|---|
| 最低 SpO2 | 82.3% | **86-88%** | +4-6 點 |
| T90 | 15.7% | **6-9%** | -50% |
| 最長 event | 19.8 分 | **9-12 分** | -40% |
| 紅旗夜（最低 < 80%） | 22% | **5-10%** | -60% |

---

## 三、放大 vs 縮小改善的個人因素

**會放大改善（順風）：**
1. 非肥胖 → 軟組織塌陷主要靠重力，側睡解除得乾淨
2. REM rebound 主導 desat → 側睡對 REM-OSA 效益最大
3. 4/29-5/1 連 3 晚 < 80% cluster → 近期睡姿可能偏 supine，調整空間大

**會縮小改善（逆風）：**
1. 鼻塞 / 鼻中隔彎曲 → 側睡讓單側鼻腔更塞，可能殘留 5-10% desat
2. 退化性後縮頷骨 → 側睡改善有限（需做頭部側位 X 光確認）
3. 中樞性（非阻塞性）成分 → 不受睡姿影響

---

## 四、試驗設計

### 階段 A：3 晚側睡 vs 3 晚自由睡姿對照（最低成本）

**工具（任一）：**
- 在睡衣後背縫網球 / 厚襪子捲起塞口袋（強迫側翻時不舒服）
- Bumper belt（市售姿勢治療帶，~$30）
- 抱枕貼緊腹部 + 背部靠墊（被動式）

**操作：**
1. Day 1-3：自由睡姿（baseline，照常）
2. Day 4-6：強制側睡（睡衣縫網球或穿 bumper belt）
3. 期間其他變數固定：相同就寢時間、無酒精、無 Fexofenadine、相同房間溫度

**判讀（看 `reviews/spo2_desat_*.png` 與 `--summary 7`）：**
| 結果 | 推論 | 後續行動 |
|---|---|---|
| 最低 SpO2 上升 ≥ 3 點 | POSA 確認 | 體位治療為一線方案 |
| 最低 SpO2 改善 < 2 點 | 非 POSA 或 sampling 漏偵 | PSG 後考慮 CPAP / 口內裝置 |
| T90 下降 ≥ 40% | 強烈 POSA | bumper belt 長期配戴 |
| 最長 event 縮短 ≥ 30% | 中度 POSA | 結合床頭抬高 |

### 階段 B：床頭抬高 15 度（更友善，可長期）

**工具：**
- 床頭腳墊高 15-20 cm（書本、瑜珈磚、床頭抬高器）
- 注意：**整張床抬，不是只墊枕頭**（後者會折頸椎反而更糟）

**操作：**
- 連續 7 晚，與 baseline（5/1 之前 58 晚）對比

### 階段 C：側睡 + 床頭抬高合併（最強組合）

若 A、B 各自有效但仍未到正常區，可疊加。文獻顯示效益部分加成（不是 1+1）。

---

## 五、Garmin 監測限制

**重要警告：Garmin SpO2 採樣 = 60 秒一筆，PSG = 1 秒一筆**

- Garmin ODI 顯示 1.2 events/h（看似正常），實際 AHI 推估 5-10× 倍率
- 「最低 SpO2 / T90 / 最長 event」相對變化可信，**絕對 ODI 數值不可信**
- 試驗判讀以「最低 SpO2 上升幾點」「T90 下降百分比」為主，不看 ODI

---

## 六、與 PSG 預約的關係

**體位治療試驗不取代 PSG，而是強化 PSG 的價值：**

1. PSG 排隊期間（通常 2-8 週）先做 A 階段試驗
2. PSG 報告出爐時，已有「自然睡姿 vs 側睡」對照數據
3. 可直接告訴醫師「側睡讓我最低 SpO2 從 82% 升到 87%，建議優先評估體位治療而非直接 CPAP」
4. 影響後續治療路徑：POSA 確認 → bumper belt + 口內裝置 first-line；非 POSA → CPAP first-line

---

## 七、執行檢查清單

- [ ] 5/1 晚：第一晚側睡測試（後背塞物 + 床頭抬 15 cm）
- [ ] 5/2 早晨：讀 `reviews/spo2_desat_2026-05-02.png`，與 5/1（最低 79%）對比
- [ ] 5/2-5/4：連 3 晚側睡 + 抬高，每日 daily check-in 記錄
- [ ] 5/4 晚：執行 `python scripts/analyze_spo2_desats.py --summary 4` 看 4 晚對照
- [ ] 5/5：依結果決定：（a）正式預約 PSG；（b）長期採用體位治療；（c）兩者並行
- [ ] PSG 預約進度（已標記為本週首要任務，不論試驗結果如何）

---

## 八、參考文獻

1. Joosten SA, et al. *Supine position related obstructive sleep apnea in adults: pathogenesis and treatment.* Sleep Med Rev. 2014;18(1):7-17.
2. Oksenberg A, Silverberg DS. *The effect of body posture on sleep-related breathing disorders: facts and therapeutic implications.* Sleep Med Rev. 1998;2(3):139-62.
3. Cartwright RD. *Effect of sleep position on sleep apnea severity.* Sleep. 1984;7(2):110-4.
4. Ravesloot MJL, et al. *The undervalued potential of positional therapy in position-dependent snoring and obstructive sleep apnea.* Sleep Breath. 2013;17(1):39-49.
5. Souza FJF, et al. *The influence of head-of-bed elevation in patients with obstructive sleep apnea.* Sleep Breath. 2017;21(4):815-820.
6. Mador MJ, et al. *Prevalence of positional sleep apnea in patients undergoing polysomnography.* Chest. 2005;128(4):2130-7.

---

*Filed: articles/2026-05-01-osa-positional-therapy-trial.md*
