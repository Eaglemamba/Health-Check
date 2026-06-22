# articles/ — 前瞻性指南與專題分析

依**主題**分資料夾（2026-05-28 起）。每篇文章為知識型/決策型文件，非每日流水紀錄。

## 分類規則

1. 每篇新 article **必須**歸入最相關的既有主題資料夾。
2. 若不屬於任何既有資料夾 → **新建主題資料夾**（小寫連字號命名），並更新本檔與 `CLAUDE.md` 的分類表。
3. 檔名 `YYYY-MM-DD-<slug>.md`（或無日期的常設參考）。移檔/新建後須更新所有引用路徑（`data.js`、`PROGRESS.md`、`templates/`、`reviews/`、article 間交叉連結）。

## 例外：留根目錄的「目前生效指南」

| 檔案 | 說明 |
|------|------|
| `2026-03-25-supplement-guide.md` | 目前生效補充品指南；`data.js` source-of-truth |
| `2026-09-17-mackay-checkup-addons.md` | 目前生效健檢加測清單（6M；前版 3/25 已移 archive/） |

依「新健檢報告納入規則」，這兩份隨健檢改版而更新，前版移至 `archive/`。

## 資料夾

### `osa-sleep/` — OSA / SpO2 / 睡眠
OSA 調查、姿勢療法、設備決策、診斷敘事、肌功能訓練、累積傷害修復、HR coupling、Sims 姿勢、被蓋頭 rebreathing、穿戴血氧可信度、深睡 HRV、過敏性鼻炎行動計畫。

### `diet-nutrition/` — 飲食 / 補充品 / 營養
尿酸日式 protocol、creatine/glycine 評估、晨間 smoothie、醋實證、7-11 營養參考、糖代謝、FDA/SSA health claims、**五色植化素光譜實證 review（2026-06-08，v2 RCT-first：定向原始 RCT 檢索 + confirm/refute 雙 panel）**、**早餐 smoothie 食材農藥清洗逐項實證（2026-06-22，八路平行 agent 查證；接觸/系統 × 皮吃不吃雙軸）**。

### `cardio-metabolic/` — 心血管 / 代謝 / 訓練
體重停滯診斷、Z2/RHR 分析、上坡 Z2 健走、HRV 心血管風險、AHA 心臟習慣、生理軸綜覽、**健康槓桿排序（2026-06-08，證據分層 + provenance 標註 + 2 處自我更正）**、**最小有效劑量阻力訓練（2026-06-08，每週 1 次全身 60 分；strength 第 2 篇後移 strength-resistance/）**。

### `skin-aesthetics/` — 臉部保養 / 美學
臉部保養 RCT、痘印 vs 真疤判別、A 酸/維 C/菸鹼醯胺/防曬光老化、頭髮、體態美學。

### `checkups/` — 預測健檢報告
Month 3（2026-06-17）、Month 6（2026-09-17）預測報告。

### `archive/` — 歷史歸檔（不再修改）
被新版取代的歷史指南與前端原型。

---

## 規劃中分類（rule of two）

未來主題累積到 **2 篇**時再建資料夾，**不預先建空夾**。新 article 寫作時若主題對應下表，請以下列命名建立資料夾、同步更新本檔與 `CLAUDE.md`：

### 第一階（近期會用到）

| 規劃資料夾 | 收錄主題 |
|------------|---------|
| `mind-cognition/` | 壓力管理、冥想、HRV biofeedback、認知效能、情緒/憂鬱 markers、共振呼吸 |
| `mobility-flexibility/` | 瑜珈、伸展、姿勢矯正、box/Wim Hof 呼吸 protocol、抗久坐、筋膜 |
| `strength-resistance/` | 重訓 protocol、肥大/最大肌力、肌少症預防、taper/deload、specific lifts |

### 第二階（3–6 個月內）

| 規劃資料夾 | 收錄主題 |
|------------|---------|
| `hormones-endocrine/` | testosterone、thyroid、cortisol、melatonin、DHEA、andropause |
| `longevity-biomarkers/` | 生物年齡、autophagy/fasting、mTOR/AMPK、rapamycin/metformin、NAD+、ApoB/Lp(a)/CAC |
| `oral-dental/` | 口腔微生物 ↔ 系統發炎、牙周-心血管軸、口腔器具（與 OSA mouthguard 銜接） |
| `environmental/` | 空氣品質、淨水、塑膠/BPA、黴菌、EMF、內分泌干擾物 |

### 第三階（專題化，有素材再上）

`labs-diagnostics/`、`gear-wearables/`、`vision-eyes/`、`immune-inflammation/`、`gut-microbiome/`（若 `physiological-axes-survey.md` 之後拆出獨立成系）

---

## 元層級備案

當資料夾數 > 10 時，考慮改用 **tag 系統**（一篇可同屬多主題，如「壓力 → 失眠 → OSA」）：在 frontmatter 加 `tags:`，寫 `scripts/build_articles_index.py` 自動產生 tag-based 索引。短期主題夾夠用；長期 50+ 篇時 tag 比樹狀更耐用。
