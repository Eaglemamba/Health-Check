開始今天的晨間健康紀錄。

1. **確認日期**：執行 `TZ=Asia/Taipei date '+%Y-%m-%d %A %H:%M'` 取得系統時間，**自動 +8 小時**（此環境系統時鐘長期慢 8 小時，TZ flag 無效）後即為當前台灣時間。校正後若與使用者口頭告知或 context `currentDate` 一致則直接採用，無需再向使用者確認；不一致時才追問
2. **抓取昨夜 Garmin 資料**：Garmin `calendarDate` 以「起床日」歸檔，故昨夜睡眠 → calendarDate = 今日。
   - 先執行 `python scripts/sync_garmin_daily.py`（預設抓今日，即昨夜睡眠 + 今晨 SpO2）
   - 再執行 `python scripts/sync_garmin_daily.py --days-back 1`（抓昨日，取得昨日全日飲水、步數等 day-level 總量供「昨日回顧」區塊）
   - 完成後讀取 `reports/daily-garmin/{今日日期}.md`（睡眠與 SpO2 數據源）並在對話中顯示給使用者確認
   - 「昨日回顧/飲水」請讀 `reports/daily-garmin/{昨日日期}.md`
   - **SpO2 夜間趨勢**：讀取過去 7 晚 `reports/daily-garmin/*.md` 的「最低 SpO2」與「日均 SpO2」（缺檔以 `—` 表示），於對話中顯示連 3 晚 / 7 晚 < 88% 的計數，並在寫檔時填入 daily 檔案的「SpO2 夜間最低 7 晚趨勢」表格
   - **SpO2 全夜圖表（含 hypnogram 條帶）**：執行 `python scripts/analyze_spo2_desats.py --chart {今日日期}` 產生當晚 epoch-level 圖表（自動存於 `reviews/daily/spo2/spo2_desat_{今日日期}.png`）；**自 2026-05-19 起**，當 Garmin sleepLevels 可用時，圖表會自動內建 2-panel 排版（上：hypnogram 條帶 Deep/Light/REM；下：SpO2 折線 + 階段背景色），用於 OSA 表型即時判讀。並執行 `python scripts/analyze_spo2_desats.py --trend` 更新整體趨勢圖（`reviews/daily/spo2/spo2_desat_trend.png`）；在 daily 檔案的 SpO2 區塊嵌入相對連結
   - **SpO2 全夜 Heatmap（28+ 晚全紀錄；自 2026-05-21 起取代 `--overlay`）**：執行 `python scripts/analyze_spo2_heatmap.py` 產生 `reviews/daily/spo2/spo2_heatmap_all_nights.png`（永久軸圖；每日重生成、不歸檔）。每一橫列 = 1 晚，x 軸入睡後分鐘，色階 SpO2 80-100%，下方副圖為每分鐘 median + IQR + 90% / 88% 紅旗線 + C1-C5 cycle bin 標記。**用途**：(1) 確認今晚在全 cohort 中的相對分位；(2) 揪 outlier 夜對照當天介入；(3) HSAT 帶診核心圖。**裝置一致性**：僅納入 Garmin Venu 4 (deviceId 3622900919)；前一台裝置（4/19-4/23 共 5 晚）自動剔除。在 daily 檔案的 SpO2 區塊嵌入該圖相對連結
   - **SpO2 × 睡眠分期 7 晚疊圖**：執行 `python scripts/analyze_spo2_desats.py --hypnogram7 {今日日期}` 產生 rolling 7 晚 hypnogram × SpO2 疊圖（檔名 `reviews/daily/spo2/spo2_hypnogram_7night_{今日日期}.png`）。每晚一列 subplot，REM/Light/Deep 背景色 + SpO2 折線。**主要用途**：判讀 OSA 主導階段是否漂移（REM-dominant vs Light-dominant vs Deep-dominant），單晚結論需用 7 晚趨勢驗證再下表型。在 daily 檔案的 SpO2 區塊嵌入該圖相對連結。同時 console 輸出 stage-stratified nadir / <90% 表，可在判讀區引用。
   - 若 sync 失敗（429 / 網路 / token 過期），改採手動輸入模式，在睡眠步驟向使用者詢問 Sleep Score、Body Battery、就寢/起床時間
3. **逐項引導使用者填寫，一次一個問題**（此階段**不寫任何檔案**，僅在對話中收集回答，避免 stop hook 中途觸發導致重複提問）：
   - 體重（可選填，**週六**為正式紀錄日）
   - 血壓：收縮壓 / 舒張壓 / 心率（兩次測量）— Garmin 無晨間 BP，需使用者輸入
   - 睡眠：**以 Garmin 摘要為準**（就寢、起床、總時長、深眠、REM、Sleep Score、Body Battery 起床值）；只需向使用者追問：
     - 中途醒來（次數+原因）
     - 主觀恢復感：1-5 分（1=極度疲憊, 5=精力充沛）
     - **實際上床時間（可選填）**：若 daily-garmin 摘要的 latency 估算品質為 `wide_range`（HR 訊號與步數訊號差 > 30 分，代表演算法無法區分「躺床清醒」與「已睡」），向使用者追問「昨晚實際幾點上床？」；若回答則填入 `**實際上床：** HH:MM` 一行，演算法會以此覆寫 latency 估算
   - **昨日實際飲水量**（L）：優先讀取 Garmin summary 的「飲水 - 實際」欄；若為「—」（代表 Garmin Connect 未紀錄），才向使用者追問；使用者回覆後，執行 `python scripts/log_hydration.py --ml <mL值> --date <昨日日期> --replace` 自動回寫至 Garmin Connect（`--replace` 會先讀當日值算 delta，避免重複累加）；對照 ≥ 2.5L 目標
   - **昨日活動消耗**（kcal）：讀取昨日 `reports/daily-garmin/{昨日日期}.md` 的「活動」區塊小計（主動 + BMR），在「昨日回顧」中列出；用於熱量平衡校準（若 > 300 kcal → 提醒今日可彈性增加 200-300 kcal 攝取；若 < 100 kcal → 提醒今日加強運動）
   - **昨日 Na / K / Na-K ratio**：若 `reviews/food/{昨日日期}.md` 存在，執行 `python scripts/analyze_nutrition.py --date {昨日日期}` 取得每日鈉鉀總計與比值，在「昨日回顧」中列出。判讀：Na/K < 0.5 ✅ / 0.5-0.6 🟢 / 0.6-0.8 🟡 / > 0.8 🟠（INTERSALT 1988 與 BP 最低相關）。若連 3 天 ≥ 0.8 → 提醒減鈉（首選：自煮白煮蛋取代茶葉蛋，省 440 mg/天）或加 K（首選：早餐 +1 整根香蕉 +422 mg）
   - 身體信號：部位、性質、強度 (0-10)，或回答「清」
   - 今日計畫：飲水目標、補充品、運動安排、活動度/伸展安排
4. **所有問題回答完畢後**，才一次性執行以下寫檔動作：
   - 在 `reviews/daily/` 建立今日檔案：`YYYY-MM-DD.md`
   - 複製 `templates/daily.md` 的內容，將 `[DATE]` 替換為確認後的日期
   - 睡眠區塊填入 Garmin 讀到的值（就寢、起床、Sleep Score、Body Battery）+ 使用者追答（中途醒來、主觀恢復感）
   - 昨日回顧區塊填入昨日實際飲水量
   - 其餘區塊填入使用者輸入
5. 同步更新 `reviews/weekly/` 對應週次檔案（如 `2026-W12.md`）：
   - 將今日體重填入體重表格對應欄位
   - 將第二次血壓讀數填入血壓表格對應日期列
   - 將睡眠數據（Sleep Score / Body Battery / 總時長 / 主觀恢復感）填入睡眠表格對應日期列
   - 將身體信號（部位+性質+強度）更新至「身體信號模式」區塊（新增或累加出現天數、計算平均強度）
   - 將運動內容（含組數/時間）填入「本週運動紀錄」表格
   - 如果該週的 weekly 檔案不存在，先從 `templates/weekly.md` 建立，替換日期佔位符
6. **更新 Dashboard**：執行 `python3 scripts/generate_dashboard.py` 重新生成 `reviews/health_dashboard.png`
   - **週日 daily 額外執行**：`python scripts/analyze_hrv_trend.py` 產生 HRV 趨勢圖 + markdown snippet（貼至當週 weekly review 「HRV 趨勢」段）。若 Verdict 為 CONFIRMED 且 slope < −0.05 ms/night → 提醒下週訓練 deload + 熱量補回
7. **同步 data.js（index.html PWA 用）**：執行 `python3 scripts/sync_data_js.py` 將最新 daily / weekly 數據寫回 `data.js`（hero.currentWeight、markers BP/Sleep/Weight、tracker 14 天陣列）。若有變更會印出 `[ok] ...` 清單；無變更則印 `data.js: no changes`
8. **歸檔上週 SpO2 圖**（**只在週一 daily check-in 執行**）：執行 `python scripts/archive_spo2.py` — 將 `reviews/daily/spo2/` 中**非當週 ISO week** 的 PNG 移至 `archive/`，並同步更新 daily review markdown 內的圖片連結。當週 PNG（含今日新生成的 hypnogram / hrv / overlay）+ 永久軸圖（trend / hrv_trend / by_cycle）保留於 root。非週一不執行此步驟。
9. **Commit & Push**：將 daily 檔案、weekly 檔案、dashboard PNG、data.js、（若週一）archive 移動結果一併 commit 並 push（在這一步完成後才結束對話，避免 stop hook 抱怨 untracked files）
10. **開啟 Dashboard 檢查**：執行 `open reviews/health_dashboard.png` 讓使用者確認圖表數據正確
11. 控制在 3 分鐘內完成 — 簡潔，不討論

注意事項：
- 如果血壓收縮壓 > 160 或 < 90，提醒就醫
- 如果 Sleep Score 連續三天 < 65，提醒檢視睡眠修復方案
- 如果身體信號連續三天非「清」，提醒關注趨勢
- 如果身體信號同一部位強度持續 ≥ 5，建議物理治療評估
- **SpO2 最低 < 88%** → OSA 風險紅旗；連續 3 晚 < 88% 強烈建議 PSG 多項睡眠檢查
- **昨日飲水 < 2.0L** → 警示 UA 排泄效率降低；連續 2 天 < 2.0L 本週重點關注
- **RHR 3 天內上升 ≥ 5 bpm** 或 > 67 連續 3 天 → 發炎 / 感染前兆
- **步數 < 5,000 連續 3 天** → UA / HbA1c 控制風險
- Garmin raw JSON 位於 `data/garmin/YYYY-MM-DD.json`（已 gitignored）；詳細規則見 `templates/pt-rules.md`
