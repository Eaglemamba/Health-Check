# Annual Review — 總索引

_最後更新：2026-04-20_

此資料夾存放歷次健檢原始報告、pe.json 結構化資料、補充品指南鏡射、因果地圖與歷史影像。**所有檔案為歷史快照，不得就地修改**（修訂請另存新檔並在上層 `articles/` 建立新版）。

---

## 一、健檢時間軸

| 健檢日期 | 院所 | 健檢報告 | PE JSON | 補充品指南鏡射 | 因果地圖 | 原始影像 |
|---|---|---|---|---|---|---|
| 2017-??-?? | 集美（Jimei） | — | — | — | — | [source-images/2017-jimei/](source-images/2017-jimei/) |
| 2024-12-05 | 馬偕 | _（併入 2025.md 對照欄）_ | — | — | — | — |
| **2025-09-17** | 馬偕 | [2025.md](2025.md) | — ⚠ | [2025-09-17-supplement-guide.md](2025-09-17-supplement-guide.md) | [2025-causal-map.html](2025-causal-map.html) | — |
| **2026-03-25** | 馬偕 | [2026-03-25.md](2026-03-25.md) | [2026-03-25-pe.json](2026-03-25-pe.json) | [2026-03-25-supplement-guide.md](2026-03-25-supplement-guide.md) | [2026-causal-map.html](2026-causal-map.html) | — |

✅ = 已建立｜⚠ = 缺失或需補｜— = 不適用

---

## 二、命名慣例

| 檔案類型 | 格式 | 範例 |
|---|---|---|
| 健檢報告（單次） | `YYYY-MM-DD.md` | `2026-03-25.md` |
| 健檢報告（年度整合，歷史遺留） | `YYYY.md` | `2025.md` |
| PE 結構化資料 | `YYYY-MM-DD-pe.json` | `2026-03-25-pe.json` |
| 補充品指南鏡射 | `YYYY-MM-DD-supplement-guide.md` | `2026-03-25-supplement-guide.md` |
| 因果地圖（年度） | `YYYY-causal-map.html` | `2026-causal-map.html` |
| 原始影像 | `source-images/YYYY-院所/` | `source-images/2017-jimei/` |

> **注意**：`2025.md` 為歷史命名（整年彙整），自 2026-03-25 起改採單次健檢 `YYYY-MM-DD.md` 格式。已存在的 `2025.md` 不得改名（外部 `articles/archive/` 與 `handover.md` 有引用）。

---

## 三、缺件清單

| 項目 | 狀態 | 處理建議 |
|---|---|---|
| `2025-09-17-pe.json` | ❌ 未建立 | 回頭從 `2025.md` 結構化抽取，或等下次健檢不再補做 |
| `2024-12-05.md` 單獨檔案 | ❌ 未建立 | 其數據已於 `2025.md` 前次欄位呈現，無需補檔 |
| 2025-09-17 原始影像 | ❌ 無 | 若 PDF/掃描存在可建立 `source-images/2025-mackay/` |
| 2026-03-25 原始影像 | ❌ 無 | 若 PDF/掃描存在可建立 `source-images/2026-mackay/` |

---

## 四、交叉引用關係

```
articles/2026-03-25-supplement-guide.md         ← 目前生效版
       ↕ 內容 1:1 鏡射
reviews/annual/2026-03-25-supplement-guide.md   ← 歷史快照

articles/archive/2025-09-17-supplement-guide.md ← 已歸檔前版
       ↕ 內容 1:1 鏡射
reviews/annual/2025-09-17-supplement-guide.md   ← 歷史快照
```

- `articles/` 根目錄**只保留最新一版**前瞻性指南
- `articles/archive/` 保存所有舊版
- `reviews/annual/` 的鏡射檔案**永不異動**，用於追溯當時建議

---

## 五、檔案完整性規則（納入新健檢時）

每次新增 `YYYY-MM-DD.md` 健檢報告時，同一批次必須同步建立：

1. ✅ `YYYY-MM-DD.md` — 健檢原始紀錄
2. ✅ `YYYY-MM-DD-pe.json` — 結構化數值
3. ✅ `YYYY-MM-DD-supplement-guide.md` — 補充品指南（鏡射自 articles/）
4. 🔄 `YYYY-causal-map.html` — 該年度因果地圖（整年內可更新至同一檔案）
5. 🟡 `source-images/YYYY-院所/` — 原始掃描（如有）

違反此規則請在本 README「缺件清單」標註。

---

## 六、歷史變更紀錄

| 日期 | 變更 |
|---|---|
| 2026-04-20 | 建立 `2026-causal-map.html`；新增本索引檔 |
| 2026-04-20 | 整合 Garmin 1680 夜睡眠資料進 2026 因果地圖 Layer 0 |
| 2026-04-07 | 建立 `2025-causal-map.html`、`2025.md`、`2025-09-17-supplement-guide.md` |

---

## 七、相關資料夾

- `../daily/` — 每日紀錄
- `../weekly/` — 每週回顧
- `../monthly/` — 每月回顧
- `../food/` — 飲食紀錄
- `../../articles/` — 前瞻性指南（目前生效版）
- `../../articles/archive/` — 歷史歸檔指南
- `../../reports/garmin-sleep-charts/` — Garmin 睡眠分析圖表
- `../../scripts/` — 資料處理腳本
