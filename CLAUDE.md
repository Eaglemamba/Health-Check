# Health-Check

個人健康追蹤系統，使用 Markdown 檔案記錄每日健康數據並定期回顧。

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
  generate_dashboard.py     # 健康儀表板圖表生成腳本
reviews/
  daily/                    # 每日紀錄（YYYY-MM-DD.md）
  weekly/                   # 每週回顧（YYYY-Wxx.md）
  monthly/                  # 每月回顧（YYYY-MM.md）
  annual/                   # 年度健康評估報告（YYYY.md）
  food/                     # 每日飲食紀錄（YYYY-MM-DD.md）
  health_dashboard.png      # 健康趨勢儀表板圖表（自動生成）
```

## 每日 Check-in 流程

執行 `templates/daily-command.md` 中的流程，逐項引導填寫：體重、血壓、睡眠、身體信號、今日計畫。

填寫完成後，同步將當天數據更新至對應的 weekly review 檔案。若該週檔案不存在，從 `templates/weekly.md` 建立。

### 儀表板圖表更新

每次 daily check-in 完成並 commit 前，**必須**執行 `python3 scripts/generate_dashboard.py` 重新生成 `reviews/health_dashboard.png`，將更新後的圖表一併加入同一個 commit。圖表包含體重、血壓/心率、Sleep Score 三組趨勢圖（最多顯示近 14 天）。

## 重要規則

- **日期確認**：每次使用者輸入「daily」或「health check」啟動 check-in 時，**第一步必須**用 `date` 指令取得當前台灣時間（TZ=Asia/Taipei），確認正確日期後再建立檔案。不依賴系統提供的日期資訊，以台灣時間為準。
- 語言：所有健康紀錄與模板使用**繁體中文**
- 每次 check-in 控制在 3 分鐘內，簡潔不討論
- 體重：以週一至週五早晨均值為正式週記錄（排尿後、進食前），避免週末餐食干擾
- 血壓：連量兩次取第二次；收縮壓 > 160 或 < 90 提醒就醫
- Sleep Score 連續三天 < 65 → 提醒檢視睡眠修復方案
- 身體信號連續三天非「清」→ 提醒關注趨勢

## 檔案命名慣例

- Daily: `reviews/daily/YYYY-MM-DD.md`
- Weekly: `reviews/weekly/YYYY-Wxx.md`
- Monthly: `reviews/monthly/YYYY-MM.md`
- Annual: `reviews/annual/YYYY.md`
- Food: `reviews/food/YYYY-MM-DD.md`

## 物理治療 & 健康管理建議規則

每日 check-in 完成後，讀取 `templates/pt-rules.md` 中的規則，自動提供簡短建議（2-3 句），以「💡 PT 建議：」開頭附在紀錄尾端。
