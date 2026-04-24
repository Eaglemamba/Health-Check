開始今天的晨間健康紀錄。

1. **確認日期**：執行 `TZ=Asia/Taipei date '+%Y-%m-%d %A %H:%M'` 取得當前台灣時間，向使用者確認日期與星期是否正確，確認後再進行下一步
2. **抓取昨夜 Garmin 資料**：Garmin `calendarDate` 以「起床日」歸檔，故昨夜睡眠 → calendarDate = 今日。
   - 先執行 `python scripts/sync_garmin_daily.py`（預設抓今日，即昨夜睡眠 + 今晨 SpO2）
   - 再執行 `python scripts/sync_garmin_daily.py --days-back 1`（抓昨日，取得昨日全日飲水、步數等 day-level 總量供「昨日回顧」區塊）
   - 完成後讀取 `reports/daily-garmin/{今日日期}.md`（睡眠與 SpO2 數據源）並在對話中顯示給使用者確認
   - 「昨日回顧/飲水」請讀 `reports/daily-garmin/{昨日日期}.md`
   - 若 sync 失敗（429 / 網路 / token 過期），改採手動輸入模式，在睡眠步驟向使用者詢問 Sleep Score、Body Battery、就寢/起床時間
3. **逐項引導使用者填寫，一次一個問題**（此階段**不寫任何檔案**，僅在對話中收集回答，避免 stop hook 中途觸發導致重複提問）：
   - 體重（可選填，**週六**為正式紀錄日）
   - 血壓：收縮壓 / 舒張壓 / 心率（兩次測量）— Garmin 無晨間 BP，需使用者輸入
   - 睡眠：**以 Garmin 摘要為準**（就寢、起床、總時長、深眠、REM、Sleep Score、Body Battery 起床值）；只需向使用者追問：
     - 中途醒來（次數+原因）
     - 主觀恢復感：1-5 分（1=極度疲憊, 5=精力充沛）
   - **昨日實際飲水量**（L）：優先讀取 Garmin summary 的「飲水 - 實際」欄；若為「—」（代表 Garmin Connect 未紀錄），才向使用者追問；使用者回覆後，執行 `python scripts/log_hydration.py --ml <mL值> --date <昨日日期> --replace` 自動回寫至 Garmin Connect（`--replace` 會先讀當日值算 delta，避免重複累加）；對照 ≥ 2.5L 目標
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
7. **Commit & Push**：將 daily 檔案、weekly 檔案、dashboard PNG 一併 commit 並 push（在這一步完成後才結束對話，避免 stop hook 抱怨 untracked files）
8. **開啟 Dashboard 檢查**：執行 `open reviews/health_dashboard.png` 讓使用者確認圖表數據正確
9. 控制在 3 分鐘內完成 — 簡潔，不討論

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
