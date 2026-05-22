# Health-Check

個人健康追蹤系統，使用 Markdown 檔案記錄每日健康數據並定期回顧。前端為 React 單頁 PWA（6-Month Health Reversal Plan），可加到 iPhone 桌面當原生 app 用，部署於 GitHub Pages。

## 專案結構

```
templates/                  # 模板與指令
  daily.md                  # 每日紀錄模板
  weekly.md                 # 每週回顧模板
  monthly.md                # 每月回顧模板
  annual.md                 # 年度健康評估報告模板
  daily-command.md          # 每日 check-in 流程指令
  food.md                   # 每日飲食紀錄模板
scripts/
  generate_dashboard.py     # 健康儀表板圖表生成腳本（matplotlib PNG）
  sync_data_js.py           # 從 reviews/daily/*.md 同步最新值至 data.js
  sync_garmin_daily.py      # 抓取 Garmin 昨夜睡眠 + 今晨 SpO2
  analyze_spo2_desats.py    # SpO2 全夜圖（含 hypnogram 條帶）+ 趨勢 + 7 晚 hypnogram×SpO2 疊圖
  analyze_spo2_by_cycle.py  # SpO2 cycle 統計（90-min bins，全 Venu 4 cohort）
  analyze_spo2_heatmap.py   # SpO2 全夜 heatmap（all Venu 4 nights × elapsed min × color；自 2026-05-21 取代 7 晚 overlay）
  analyze_wedge_effect.py   # 頭部楔形枕 pre/post C1 SpO2 對照（one-shot 自然實驗分析；2026-05-21 建立）
  log_hydration.py          # 將昨日飲水量回寫至 Garmin Connect
  archive_spo2.py           # 週一執行：將非當週 SpO2 PNG 移至 spo2/archive/ 並更新 daily review 連結
reviews/
  daily/                    # 每日紀錄（YYYY-MM-DD.md）
    YYYY-MM/                # 月份歸檔（非當週的 daily md，2026-05-22 起組織化）
    spo2/                   # 當週 SpO2 圖 + 永久軸圖（trend / hrv_trend / by_cycle / heatmap_all_nights）
      archive/              # 非當週 SpO2 圖；週一 daily check-in 自動歸檔（scripts/archive_spo2.py）
  weekly/                   # 每週回顧（YYYY-Wxx.md）
  monthly/                  # 每月回顧（YYYY-MM.md）
  annual/                   # 年度健康評估報告（YYYY-MM-DD.md，含子資料夾歸檔）
  food/                     # 每日飲食紀錄（YYYY-MM-DD.md）
  health_dashboard.png      # 健康趨勢儀表板圖表（自動生成）
reports/
  daily-garmin/             # Garmin 每日摘要 markdown（sync_garmin_daily.py 產生）
    YYYY-MM/                # 月份歸檔（非當週）
  archive/                  # 一次性歷史回顧（Garmin 8 年完整 + 睡眠分析及圖表，2026-04-18-20）
articles/                   # 前瞻性指南（補充品、健檢加測等）
  archive/                  # 被新版取代的歷史指南；不再修改
archive/                    # 非健康資料歸檔（過時 handover、前端原型 / template / dev scratch）

PROGRESS.md                 # 專案進度總覽（timeline、關鍵指標、目前生效策略、待辦）

# 前端 PWA — 6-Month Health Reversal Plan（React + Babel-standalone CDN）
index.html                  # HTML shell（PWA meta、SW 註冊、Babel 編譯 JSX）
data.js                     # 雙語（EN/ZH）資料層 — hero / markers / panels / tracker
styles.css                  # 主題 + 密度 + Hero variant CSS
components-core.jsx         # Hero、Marker、Tabs、Icon
components-panels.jsx       # 11 個 panel（overview/sleep/diet/exercise/running/supps/routine/timeline/safety/dashboard/tracker）
tweaks-panel.jsx            # 右下角即時調整面板
manifest.webmanifest        # PWA manifest
sw.js                       # Service Worker（cache-first，離線可用）
icons/                      # PWA icon（apple-touch / 192 / 512 / maskable）

analyzer.html               # 年度健檢數據獨立分析頁（仍為 vanilla JS）
```

## 月份歸檔慣例（2026-05-22 起）

當週（ISO week）以外的 daily-style 檔案歸檔於各資料夾的 `YYYY-MM/` 子資料夾，避免單一目錄檔案過多：
- `reviews/daily/2026-04/2026-04-19.md` …
- `reports/daily-garmin/2026-04/2026-04-19.md` …
- `data/garmin/2026-04/2026-04-19.json` …（gitignored 內容）

所有讀取這些目錄的 script 已改為 **recursive glob**（`rglob` / `glob.glob(..., recursive=True)`）+ 路徑 fallback（先試根目錄再試 `YYYY-MM/` 子資料夾）。新增的當週檔案仍寫到根目錄；週一/週日節點手動或腳本將上週批次移入 `YYYY-MM/`。

## 每日 Check-in 流程

執行 `templates/daily-command.md` 中的流程，逐項引導填寫：體重、血壓、睡眠、身體信號、今日計畫。

填寫完成後，同步將當天數據更新至對應的 weekly review 檔案。若該週檔案不存在，從 `templates/weekly.md` 建立。

### 儀表板與 data.js 同步（commit 前**必做**）

每次 daily check-in 完成並 commit 前，依序執行：

1. **`python3 scripts/generate_dashboard.py`** — 重新生成 `reviews/health_dashboard.png`（體重、體組成、血壓/心率、Sleep Score 四組趨勢圖）
2. **`python3 scripts/sync_data_js.py`** — 從 `reviews/daily/*.md` 與最近收盤 ISO 週的 BP 解析最新值，寫回 `data.js` 對應欄位：
   - `hero.currentWeight` / `currentWeightDate`（最新週六正式體重）
   - `hero.progressMeta`（Day N · X.X kg）
   - `hero.startDate`（Last sync M/D）
   - `markers[heart] / [sleep] / [weight]` 的 val + delta
   - `tracker.bp / weight / sleep / bb`（last 14 days，缺值 forward-fill）
   - **idempotent，無變化會印 `data.js: no changes`**
3. 將 daily / weekly / `health_dashboard.png` / `data.js` 一併 commit & push

PWA 部署於 `https://eaglemamba.github.io/Health-Check/`（GitHub Pages）。**Service Worker 自 v16 起對 `data.js` 採 stale-while-revalidate**：每次開 PWA 立即顯示 cache 版，背景拉新版寫回 cache，下次開啟即見最新 daily 數值。其餘靜態資源（HTML/JSX/CSS/icons）仍 cache-first。SW 邏輯本身有變動時才需 bump `sw.js` 內 `VERSION` 字串；單純 data.js 數值更新無需 bump。

## 重要規則

- **日期確認**：每次使用者輸入「daily」或「health check」啟動 check-in 時，**第一步必須**用 `date` 指令取得當前台灣時間（TZ=Asia/Taipei），確認正確日期後再建立檔案。不依賴系統提供的日期資訊，以台灣時間為準。
- 語言：所有健康紀錄與模板使用**繁體中文**
- 每次 check-in 控制在 3 分鐘內，簡潔不討論
- 體重：以**週六早晨**為正式週記錄（排尿後、進食前）— 週六是連續 5 個工作日執行後、週末大餐尚未開始前的最低真實值；其他日可選填
- 血壓：連量兩次取第二次；收縮壓 > 160 或 < 90 提醒就醫
- Sleep Score 連續三天 < 65 → 提醒檢視睡眠修復方案
- 身體信號連續三天非「清」→ 提醒關注趨勢

## 重要規則

- **日期確認**：每次使用者輸入「daily」或「health check」啟動 check-in 時，**第一步必須**用 `date` 指令取得當前台灣時間（TZ=Asia/Taipei），確認正確日期後再建立檔案。不依賴系統提供的日期資訊，以台灣時間為準。
- 語言：所有健康紀錄與模板使用**繁體中文**
- 每次 check-in 控制在 3 分鐘內，簡潔不討論
- 體重：以**週六早晨**為正式週記錄（排尿後、進食前）— 週六是連續 5 個工作日執行後、週末大餐尚未開始前的最低真實值；其他日可選填
- 血壓：連量兩次取第二次；收縮壓 > 160 或 < 90 提醒就醫
- Sleep Score 連續三天 < 65 → 提醒檢視睡眠修復方案
- 身體信號連續三天非「清」→ 提醒關注趨勢

## 檔案命名慣例

- Daily: `reviews/daily/YYYY-MM-DD.md`（當週位於根目錄；過往週於 `reviews/daily/YYYY-MM/`）
- Weekly: `reviews/weekly/YYYY-Wxx.md`
- Monthly: `reviews/monthly/YYYY-MM.md`
- Annual（單次健檢）: `reviews/annual/YYYY-MM-DD.md`（目前生效位於根目錄；過往年度已歸檔至 `reviews/annual/YYYY/` 子資料夾）
- Annual（年度彙整，歷史遺留）: `reviews/annual/YYYY/YYYY.md`
- Food: `reviews/food/YYYY-MM-DD.md`

**Annual 資料夾組織原則**（詳見 `reviews/annual/README.md`）：
- 最新健檢的所有檔案（報告 / pe.json / 補充品指南鏡射 / 因果地圖）**保留在根目錄**
- 新健檢產出時，將**前一次健檢全部檔案** `git mv` 至以年份命名的子資料夾（如 `reviews/annual/2026/`）
- 歷史檔案一經歸檔即**不再異動**

## 物理治療 & 健康管理建議規則

每日 check-in 完成後，讀取 `templates/pt-rules.md` 中的規則，自動提供簡短建議（2-3 句），以「💡 PT 建議：」開頭附在紀錄尾端。

## 新健檢報告納入規則

每次新增健檢結果（`reviews/annual/YYYY-MM-DD.md` 與 `reviews/annual/YYYY-MM-DD-pe.json`）後，**必須**完成下列調整。**支援同年多次健檢**（採健檢日期前綴命名）。

### 命名慣例（與 `reviews/annual/` 對齊）

| 文件類型 | 檔名格式 |
|---------|---------|
| 健檢報告 | `reviews/annual/YYYY-MM-DD.md` + `YYYY-MM-DD-pe.json` |
| **目前生效**補充品指南 | `articles/YYYY-MM-DD-supplement-guide.md` |
| **歷史**補充品指南（已被新版取代） | `articles/archive/YYYY-MM-DD-supplement-guide.md` |
| 補充品指南 filed 鏡射 | `reviews/annual/YYYY-MM-DD-supplement-guide.md` |
| **目前生效**健檢加測項目 | `articles/YYYY-MM-DD-mackay-checkup-addons.md` |
| **歷史**健檢加測項目 | `articles/archive/YYYY-MM-DD-mackay-checkup-addons.md` |

「YYYY-MM-DD」必須與該次健檢日期完全一致，1:1 對應。

### 「目前生效 vs 歷史」原則

`articles/` 根目錄**僅保留最新一版**指南檔案，方便讀者立即看到當前策略；前版全部移至 `articles/archive/`。建立新版時：

1. 將前版檔案 `git mv` 至 `articles/archive/`
2. 在新版 header 與 footer 用相對路徑 `archive/...` 連結到前版
3. `reviews/annual/` 下的 filed 鏡射不動（其本身即為日期化歷史快照）

### 流程

1. **歸檔前版指南（不得就地修改）**
   - `git mv articles/{舊日期}-supplement-guide.md articles/archive/{舊日期}-supplement-guide.md`
   - `git mv articles/{舊日期}-mackay-checkup-addons.md articles/archive/{舊日期}-mackay-checkup-addons.md`（若存在）
   - `reviews/annual/{舊日期}-supplement-guide.md`（filed 鏡射）保留原位不動

2. **建立新版指南（檔名以新健檢日期命名，置於 articles/ 根目錄）**
   - 複製最近一版為 `articles/{新日期}-supplement-guide.md`
   - Header 註明：基準日期、前次基準、前版連結（用 `archive/...` 相對路徑）
   - 對齊新健檢數值更新各項指標、策略表、預期效果（含趨勢比較欄）
   - Footer 加註 `*前版保存：articles/archive/{舊日期}-supplement-guide.md*`
   - 同步鏡射至 `reviews/annual/{新日期}-supplement-guide.md`

3. **更新前瞻性參考文件中的當前狀態**
   - `articles/{新日期}-mackay-checkup-addons.md`（若需新建）以新值為基準
   - **`data.js` 必須同步**（**新版 React PWA 的資料來源**，舊版單檔 `index.html` 已歸檔至 `articles/archive/`）：
     - `routineDetail.hourly.rows` 的補品時程欄位（早餐打包、午餐註記、晚餐後魚油+EGCG、睡前鎂+酸櫻桃）必須與新指南第七節 1:1 一致
     - `suppsDetail.fullStack` 的優先序、劑量、時機、月成本對齊新指南
     - `markers[]`、`overview.profile`、`hero.progressMeta` 內引用的具體數值（UA / LDL / HbA1c / 體重等）更新為最新值
     - `data.js` 注釋頭可加 `Source of truth: articles/{新日期}-supplement-guide.md`
   - 每日數據（hero.currentWeight、markers BP/Sleep/Weight、tracker 14 天）由 `scripts/sync_data_js.py` 自動從 daily reviews 拉取，不需手改
   - 歷史記錄（`reviews/annual/YYYY.md`、`reviews/annual/YYYY-causal-map.html` 等）**不得修改**

4. **commit 訊息格式**
   - 標題：`分版：保留 {舊日期} 原指南，{新日期} 改版另存新檔`
   - 列出新建與保留的檔案清單

5. **判斷原則**
   - 「前瞻性指南」（articles/、index.html 中的策略描述）→ 改版另存新檔，前版保留
   - 「歷史紀錄」（reviews/annual/ 中的當時報告與分析）→ 永不修改
   - 數值更新範圍以「指引性、決策性、未來會被遵循的文字」為準
   - **同年多次健檢**：每次都以日期建立新檔，前版皆保留為連續 baseline 軌跡
