# Health-Check

個人健康追蹤系統。以 Markdown 為主資料格式，搭配 Garmin 同步腳本與年度健檢分析，建立可長期累積、可版本控管、可回顧的健康紀錄。

## 用途

- 每日 check-in（體重、血壓、睡眠、身體信號、計畫）
- 每週 / 每月 / 年度回顧
- 年度健檢報告與補充品策略追蹤
- Garmin 數據同步、健康趨勢儀表板自動生成

## 專案結構

```
templates/        每日 / 週 / 月 / 年模板與 check-in 流程指令
scripts/          Garmin 同步腳本、健康儀表板圖表生成
reviews/
  daily/          每日紀錄（YYYY-MM-DD.md）
  weekly/         每週回顧（YYYY-Wxx.md）
  monthly/        每月回顧（YYYY-MM.md）
  annual/         年度健檢報告（最新版位於根目錄，歷年歸檔於 YYYY/ 子資料夾）
  food/           每日飲食紀錄
articles/         前瞻性指南（補充品、健檢加測等），最新版於根目錄，舊版於 archive/
index.html        健康策略總覽單頁
analyzer.html     數據分析介面
```

## 主要流程

### 每日 check-in
依 `templates/daily-command.md` 流程執行。完成後同步更新對應 weekly review，並執行 `scripts/generate_dashboard.py` 重新生成趨勢圖表，於同一個 commit 提交。

### 年度健檢納入
新健檢產出後，建立 `reviews/annual/YYYY-MM-DD.md` 與對應 `pe.json`，依「目前生效 vs 歷史」原則分版：前版指南 `git mv` 至 `articles/archive/`，新版於 `articles/` 根目錄建立並同步鏡射至 `reviews/annual/`。歷史檔案一經歸檔不再異動。

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
