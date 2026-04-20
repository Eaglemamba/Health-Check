@echo off
REM ======================================================
REM Garmin 每日同步 + 儀表板更新 + git commit/push
REM 由 Windows Task Scheduler 每天 08:00 觸發
REM ======================================================

setlocal
cd /d C:\Users\david.kuo\Health-Check

REM 日誌：附加到當月檔
set LOGDIR=logs
if not exist %LOGDIR% mkdir %LOGDIR%
set LOGFILE=%LOGDIR%\garmin-sync-%date:~0,4%-%date:~5,2%.log

echo. >> %LOGFILE%
echo ===== %date% %time% ===== >> %LOGFILE%

REM 1) 下載 Garmin 昨日資料
python scripts\sync_garmin_daily.py >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo [FAIL] sync_garmin_daily.py >> %LOGFILE%
    exit /b 1
)

REM 2) 重新生成健康儀表板
python scripts\generate_dashboard.py >> %LOGFILE% 2>&1

REM 3) git add 只加「可公開」衍生物，raw JSON 已 gitignore
git add reports/daily-garmin reviews/health_dashboard.png >> %LOGFILE% 2>&1

REM 4) 只有 diff 存在才 commit
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "daily garmin sync %date%" >> %LOGFILE% 2>&1
    git push >> %LOGFILE% 2>&1
    echo [OK] committed and pushed >> %LOGFILE%
) else (
    echo [SKIP] no changes to commit >> %LOGFILE%
)

endlocal
