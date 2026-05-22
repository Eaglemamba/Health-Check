# Health-Check

個人健康追蹤系統。以 Markdown 為主資料格式，搭配 Garmin 同步腳本與年度健檢分析；前端為 React 單頁 PWA，可加到 iPhone / Android 桌面當原生 app 用。

## 用途

- 每日 check-in（體重、血壓、睡眠、身體信號、計畫）
- 每週 / 每月 / 年度回顧
- 年度健檢報告與補充品策略追蹤
- Garmin 數據同步、健康趨勢儀表板自動生成
- 6 個月健康逆轉計畫前端（11 個 panel：總覽 / 睡眠 / 飲食 / 靠牆深蹲 / 跑步 / 保健品 / 每日作息 / 時程 / 安全 / 儀表板 / 追蹤）

## 專案結構

```
templates/            每日 / 週 / 月 / 年模板與 check-in 流程指令
scripts/
  sync_garmin_daily.py    抓取 Garmin 昨夜睡眠 + 今晨 SpO2
  analyze_spo2_desats.py  SpO2 全夜圖（含 hypnogram 條帶）+ 趨勢 + 7 晚 hypnogram×SpO2 疊圖
  analyze_spo2_by_cycle.py  SpO2 cycle 統計（90-min bins，Venu 4 cohort）
  analyze_spo2_heatmap.py SpO2 全夜 heatmap（all Venu 4 nights × elapsed min × color；2026-05-21 取代 7 晚 overlay）
  analyze_wedge_effect.py 頭部楔形枕 pre/post C1 SpO2 對照（one-shot 自然實驗）
  analyze_hrv_trend.py    HRV 趨勢圖 + markdown snippet（週日 daily 額外執行）
  generate_dashboard.py   健康儀表板圖表
  sync_data_js.py         從 daily reviews 同步最新值至 data.js
  log_hydration.py        將昨日飲水量回寫 Garmin Connect
  archive_spo2.py         週一 daily check-in 執行：將非當週 SpO2 PNG 移至 archive/
  archive_to_monthly.py   每天 daily check-in 執行（idempotent）：將非當週 daily-style 檔案移至 YYYY-MM/ 子資料夾
reviews/
  daily/              每日紀錄（YYYY-MM-DD.md）
    spo2/             當週 SpO2 圖 + 永久軸圖（trend / hrv_trend / by_cycle / heatmap_all_nights）
      archive/        非當週 SpO2 圖；週一自動歸檔
  weekly/             每週回顧（YYYY-Wxx.md）
  monthly/            每月回顧（YYYY-MM.md）
  annual/             年度健檢報告（最新版位於根目錄，歷年歸檔於 YYYY/ 子資料夾）
  food/               每日飲食紀錄
  health_dashboard.png  健康趨勢儀表板（自動生成）
articles/             前瞻性指南（補充品、健檢加測等），最新版於根目錄，舊版於 archive/
  archive/            被新版取代的歷史指南；不再修改
reports/
  daily-garmin/       Garmin 每日摘要 markdown（由 sync_garmin_daily.py 產生）
  archive/            一次性歷史回顧（2026-04-18-20 Garmin 8 年完整 + 睡眠分析及對應圖表）
archive/              非健康資料歸檔（過時的 handover、預測前端原型、template、dev scratch 等）

PROGRESS.md           專案進度總覽（timeline、關鍵指標、目前生效策略、待辦）

# 前端（React 單頁 PWA — 6-Month Health Reversal Plan）
index.html            HTML shell（React 18 + Babel-standalone CDN；含 CSP meta 允許 unsafe-eval）
data.js               雙語（EN/ZH）資料層 — hero、markers、panels、tracker
styles.css            主題（Cool / Warm / Dark）+ 密度（Comfortable / Compact）
components-core.jsx   Hero、Marker、Tabs、Icon
components-panels.jsx 11 個 panel
tweaks-panel.jsx      右下角即時調整面板（theme / lang / hero / density）
manifest.webmanifest  PWA manifest（standalone display、theme-color）
sw.js                 Service Worker（自 v16 起：data.js stale-while-revalidate；其餘 cache-first）
icons/                PWA icon（apple-touch / 192 / 512 / maskable）

analyzer.html         年度健檢數據獨立分析頁（仍為 vanilla JS）
```

## 主要流程

### 每日 check-in
依 `templates/daily-command.md` 流程執行。完成後依序：
1. 同步更新對應 weekly review
2. `python3 scripts/generate_dashboard.py` 重新生成 `reviews/health_dashboard.png`
3. `python3 scripts/sync_data_js.py` 將最新 daily / weekly 數據寫回 `data.js`（hero.currentWeight、markers BP/Sleep/Weight、tracker 14 天陣列）— **idempotent，無變化會印 `data.js: no changes`**
4. 一個 commit 同時 push：daily / weekly / dashboard PNG / data.js

### 年度健檢納入
新健檢產出後，建立 `reviews/annual/YYYY-MM-DD.md` 與對應 `pe.json`，依「目前生效 vs 歷史」原則分版：前版指南 `git mv` 至 `articles/archive/`，新版於 `articles/` 根目錄建立並同步鏡射至 `reviews/annual/`。歷史檔案一經歸檔不再異動。

## PWA 部署（iPhone / Android 加到主畫面）

1. 確認 `git push` 後在 `https://github.com/Eaglemamba/Health-Check/settings/pages` 啟用 GitHub Pages（Branch: `main` / Folder: `/ (root)`）
2. URL：`https://eaglemamba.github.io/Health-Check/`（**大小寫敏感**）
3. iPhone Safari 開該網址 → 分享 → 加入主畫面 → 點 icon = 全螢幕 standalone 啟動
4. Service Worker 第一次載入後快取 React / Babel / Google Fonts，**離線可用**
5. data.js 更新時，每天 daily check-in 流程自動 push；下次開 PWA 會抓到新版（SW 重新註冊）

如改動到 SW 邏輯（非 data.js 數值）需強制清快取，bump `sw.js` 內 `VERSION` 字串，user 端：刪除桌面 icon → Safari 重新打開網址 → 加回主畫面。data.js 數值變動則 SW 自動拉新（stale-while-revalidate），下次開啟即見最新。

## 設定

- 複製 `.env.example` 為 `.env`，填入 Garmin 帳號與其他憑證
- Python 依套件依 `scripts/` 內各腳本需求安裝
- 時區以台灣時間（`TZ=Asia/Taipei`）為準

## 規則重點

- 體重以**週六早晨**為正式週記錄（排尿後、進食前）
- 血壓連量兩次取第二次；收縮壓 > 160 或 < 90 提醒就醫
- Sleep Score 連續三天 < 65 → 檢視睡眠修復
- 身體信號連續三天非「清」→ 關注趨勢
- 所有紀錄使用繁體中文

## 注意

本 repo 含個人健康資料，僅供本人使用，未對外開放使用授權。
