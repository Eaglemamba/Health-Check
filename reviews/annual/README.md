# Annual Review — 總索引

_最後更新：2026-04-20_

此資料夾存放歷次健檢原始報告、pe.json 結構化資料、補充品指南鏡射、因果地圖與歷史影像。

**組織原則**：
- **最新一次健檢的所有檔案保留在本資料夾根目錄**（便於快速取用）
- **過往年度的檔案依年份歸檔至子資料夾**（`2025/`, `2024/`, `2017/` …）
- 所有檔案為歷史快照，**不得就地修改**；修訂請另存新檔

---

## 一、目前生效（最新健檢）

**2026-03-25（馬偕）** — 位於 `reviews/annual/` 根目錄：

| 資產 | 檔案 |
|---|---|
| 健檢報告 | [2026-03-25.md](2026-03-25.md) |
| PE 結構化資料 | [2026-03-25-pe.json](2026-03-25-pe.json) |
| 補充品指南（鏡射） | [2026-03-25-supplement-guide.md](2026-03-25-supplement-guide.md) |
| 因果地圖 | [2026-causal-map.html](2026-causal-map.html) |
| 原始影像 | — |

---

## 二、歷史歸檔

### `2025/` — 2025-09-17 馬偕健檢

| 資產 | 檔案 |
|---|---|
| 健檢報告（年度彙整，歷史遺留命名） | [2025/2025.md](2025/2025.md) |
| PE 結構化資料 | ❌ 未建立 |
| 補充品指南（鏡射） | [2025/2025-09-17-supplement-guide.md](2025/2025-09-17-supplement-guide.md) |
| 因果地圖 | [2025/2025-causal-map.html](2025/2025-causal-map.html) |

### `2017/` — 集美（Jimei）健檢

| 資產 | 檔案 |
|---|---|
| 原始影像 | [2017/images/](2017/images/) |

---

## 三、命名慣例

| 檔案類型 | 格式 | 範例 |
|---|---|---|
| 健檢報告（單次） | `YYYY-MM-DD.md` | `2026-03-25.md` |
| 健檢報告（年度彙整，歷史遺留） | `YYYY.md` | `2025/2025.md` |
| PE 結構化資料 | `YYYY-MM-DD-pe.json` | `2026-03-25-pe.json` |
| 補充品指南鏡射 | `YYYY-MM-DD-supplement-guide.md` | `2026-03-25-supplement-guide.md` |
| 因果地圖（年度） | `YYYY-causal-map.html` | `2026-causal-map.html` |
| 原始影像 | `YYYY/images/` 或 `YYYY/{院所}-images/` | `2017/images/` |
| 年份資料夾 | `YYYY/` | `2025/` |

---

## 四、新增年度健檢時的標準流程

當新一次健檢產出（例：2027-03-15）時，執行以下步驟：

1. **建立新年度的子資料夾歸檔前次內容**
   ```bash
   mkdir -p reviews/annual/2026
   git mv reviews/annual/2026-03-25.md reviews/annual/2026/
   git mv reviews/annual/2026-03-25-pe.json reviews/annual/2026/
   git mv reviews/annual/2026-03-25-supplement-guide.md reviews/annual/2026/
   git mv reviews/annual/2026-causal-map.html reviews/annual/2026/
   ```

2. **在根目錄建立新健檢檔案**
   - `reviews/annual/2027-03-15.md`
   - `reviews/annual/2027-03-15-pe.json`
   - `reviews/annual/2027-03-15-supplement-guide.md`（鏡射自 `articles/`）
   - `reviews/annual/2027-causal-map.html`

3. **更新本 README**
   - 「目前生效」區塊改為 2027-03-15
   - 「歷史歸檔」區塊新增 `2026/` 條目

4. **更新引用的外部檔案**
   - 檢查 `handover.md`、`articles/archive/*-supplement-guide.md`、前版因果地圖內的「Filed:」footer 等

5. **commit 訊息格式**
   ```
   annual/ 歸檔 2026-03-25 至 2026/，建立 2027-03-15 為最新
   ```

---

## 五、交叉引用關係

```
articles/YYYY-MM-DD-supplement-guide.md         ← 目前生效版（前瞻性指南）
       ↕ 內容 1:1 鏡射
reviews/annual/YYYY-MM-DD-supplement-guide.md   ← 最新健檢的歷史快照（根目錄）
       或 reviews/annual/YYYY/YYYY-MM-DD-supplement-guide.md   ← 舊版（已歸檔）

articles/archive/舊YYYY-MM-DD-supplement-guide.md  ← 前版前瞻性指南（已歸檔）
       ↕ 內容 1:1 鏡射
reviews/annual/舊YYYY/舊YYYY-MM-DD-supplement-guide.md  ← 歷史快照
```

- `articles/` 根目錄**只保留最新一版**前瞻性指南
- `articles/archive/` 保存所有舊版
- `reviews/annual/` 的鏡射檔案**永不異動**，用於追溯當時建議

---

## 六、已知缺件

| 項目 | 狀態 | 處理建議 |
|---|---|---|
| `2025/2025-09-17-pe.json` | ❌ 未建立 | 從 `2025/2025.md` 反向抽取；非必要 |
| `2024-12-05` 獨立報告 | ❌ 未建立 | 數據已在 `2025/2025.md` 前次欄，不建議補檔 |
| 2025-09-17 原始影像 | ❌ 無 | 若 PDF/掃描存在可建立 `2025/images/` |
| 2026-03-25 原始影像 | ❌ 無 | 若 PDF/掃描存在可建立 `images/`（根目錄） |

---

## 七、歷史變更紀錄

| 日期 | 變更 |
|---|---|
| 2026-04-20 | 重組資料夾結構：過往年度改歸檔至 `YYYY/` 子資料夾；根目錄只保留最新健檢；`source-images/2017-jimei/` 移至 `2017/images/` |
| 2026-04-20 | 建立 `2026-causal-map.html` 與首版 README |
| 2026-04-20 | 整合 Garmin 1680 夜睡眠資料進 2026 因果地圖 Layer 0 |
| 2026-04-07 | 建立 `2025.md`、`2025-09-17-supplement-guide.md`、`2025-causal-map.html` |

---

## 八、相關資料夾

- `../daily/` — 每日紀錄
- `../weekly/` — 每週回顧
- `../monthly/` — 每月回顧
- `../food/` — 飲食紀錄
- `../../articles/` — 前瞻性指南（目前生效版）
- `../../articles/archive/` — 歷史歸檔指南
- `../../reports/garmin-sleep-charts/` — Garmin 睡眠分析圖表
- `../../scripts/` — 資料處理腳本
