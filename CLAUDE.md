# Health-Check

個人健康追蹤系統，使用 Markdown 檔案記錄每日健康數據並定期回顧。

## 專案結構

```
health-check-daily-setup/   # 模板與指令
  _template.md              # 每日紀錄模板
  _weekly-template.md       # 每週回顧模板
  daily-command.md          # 每日 check-in 流程指令
reviews/
  daily/                    # 每日紀錄（YYYY-MM-DD.md）
  weekly/                   # 每週回顧（YYYY-Wxx.md）
  monthly/                  # 每月回顧（YYYY-MM.md），模板在 _template.md
```

## 每日 Check-in 流程

執行 `daily-command.md` 中的流程，逐項引導填寫：體重、血壓、睡眠、身體信號、今日計畫。

填寫完成後，同步將當天數據更新至對應的 weekly review 檔案。若該週檔案不存在，從 `_weekly-template.md` 建立。

## 重要規則

- 語言：所有健康紀錄與模板使用**繁體中文**
- 每次 check-in 控制在 3 分鐘內，簡潔不討論
- 體重：週日早晨為正式紀錄（排尿後、進食前）
- 血壓：連量兩次取第二次；收縮壓 > 160 或 < 90 提醒就醫
- Sleep Score 連續三天 < 65 → 提醒檢視睡眠修復方案
- 身體信號連續三天非「清」→ 提醒關注趨勢

## 檔案命名慣例

- Daily: `reviews/daily/YYYY-MM-DD.md`
- Weekly: `reviews/weekly/YYYY-Wxx.md`
- Monthly: `reviews/monthly/YYYY-MM.md`
