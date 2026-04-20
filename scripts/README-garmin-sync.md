# Garmin 每日自動同步 — 安裝說明

每日 08:00 自動下載前一日 Garmin 資料，更新儀表板並 push 至 GitHub。

## 一、前置

```powershell
pip install garminconnect python-dotenv matplotlib pandas
```

## 二、設定憑證（只做一次）

1. 複製 `.env.example` 為 `.env`
   ```powershell
   copy .env.example .env
   ```
2. 編輯 `.env`，填入實際 Garmin Connect 帳密
3. 確認 `.gitignore` 有列 `.env` 與 `.garth/`（已預設）

## 三、首次登入（取得 OAuth token）

```powershell
python scripts\sync_garmin_daily.py
```

- 第一次會要 **MFA code**（email 或 Authenticator）
- 成功後 token 存在 `.garth/`，**有效約 1 年**
- 之後每日執行都不用再輸入密碼

## 四、設定 Windows Task Scheduler

1. `Win + R` → `taskschd.msc`
2. **Create Basic Task** → 名稱 `Garmin Daily Sync`
3. **Trigger**：Daily → Start 08:00
4. **Action**：Start a program
   - Program: `C:\Users\david.kuo\Health-Check\scripts\sync_and_commit.bat`
   - Start in: `C:\Users\david.kuo\Health-Check`
5. **Properties** 勾選：
   - ✅ Run only when user is logged on（避免 MFA 卡住）
   - ✅ Run task as soon as possible after a scheduled start is missed
   - ✅ If task fails, restart every 1 hour, up to 3 times

## 五、驗證

手動右鍵 Task → **Run**，檢查：

```powershell
type logs\garmin-sync-2026-04.log
dir reports\daily-garmin
git log --oneline -5
```

預期看到：
- `logs/garmin-sync-YYYY-MM.log` 出現 `[OK] committed and pushed`
- `reports/daily-garmin/YYYY-MM-DD.md` 新增
- GitHub commit log 出現 `daily garmin sync ...`

## 六、常見問題

| 問題 | 原因 | 解法 |
|---|---|---|
| `garminconnect.GarminConnectAuthenticationError` | Token 過期或密碼變更 | 刪除 `.garth/` 資料夾，重跑一次互動登入 |
| `GarminConnectTooManyRequestsError` | 短時間重複呼叫 | 等 15 分鐘；正常一天一次不會觸發 |
| 抓不到當日資料 | 錶還沒上傳到雲 | 改抓 2 天前：`python scripts\sync_garmin_daily.py --days-back 2` |
| MFA code 一直要 | Task Scheduler 在背景跑沒法互動 | 確保「Run only when user is logged on」；首次一定要手動跑一次 |
| `git push` 失敗 | 無權限或衝突 | 手動 `cd` 過去測試；確認 credential helper 已設定 |

## 七、資料結構

```
data/garmin/YYYY-MM-DD.json        ← 原始 raw（gitignored，隱私）
reports/daily-garmin/YYYY-MM-DD.md ← 公開摘要（commit 到 GitHub）
reviews/health_dashboard.png       ← 儀表板（每日更新）
logs/garmin-sync-YYYY-MM.log       ← 執行日誌（gitignored）
.garth/                            ← OAuth token（gitignored）
.env                               ← 帳密（gitignored）
```

## 八、關閉自動 commit（只下載不推）

編輯 `.env`：

```
GARMIN_AUTO_COMMIT=false
```

或改用 `python scripts\sync_garmin_daily.py`（直接跑 script，不用 .bat）。

## 九、加 LINE / Telegram 通知（選配）

在 `sync_and_commit.bat` 最後加：

```batch
REM 抓取今日 sleep score 並推播
python scripts\notify_sleep.py >> %LOGFILE% 2>&1
```

另寫 `notify_sleep.py` 讀 raw JSON 擷取 Sleep Score，呼叫 LINE Notify / Telegram Bot API。
