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

## 新健檢報告納入規則

每次新增健檢結果（`reviews/annual/YYYY-MM-DD.md` 與 `reviews/annual/YYYY-MM-DD-pe.json`）後，**必須**完成下列調整。**支援同年多次健檢**（採健檢日期前綴命名）。

### 命名慣例（與 `reviews/annual/` 對齊）

| 文件類型 | 檔名格式 |
|---------|---------|
| 健檢報告 | `reviews/annual/YYYY-MM-DD.md` + `YYYY-MM-DD-pe.json` |
| 補充品指南 | `articles/YYYY-MM-DD-supplement-guide.md` |
| 補充品指南 filed 鏡射 | `reviews/annual/YYYY-MM-DD-supplement-guide.md` |
| 健檢加測項目 | `articles/YYYY-MM-DD-mackay-checkup-addons.md` |

「YYYY-MM-DD」必須與該次健檢日期完全一致，1:1 對應。

### 流程

1. **保留前版指南為歷史快照**
   - 既有的 `articles/{舊日期}-supplement-guide.md`、`articles/{舊日期}-mackay-checkup-addons.md` **不得就地修改**，作為當時策略的 baseline 留存
   - `reviews/annual/{舊日期}-supplement-guide.md`（filed 鏡射）一併保留

2. **建立新版指南（檔名以新健檢日期命名）**
   - 複製最近一版為 `articles/{新日期}-supplement-guide.md`
   - Header 註明：基準日期、前次基準、前版連結（用相對路徑）
   - 對齊新健檢數值更新各項指標、策略表、預期效果（含趨勢比較欄）
   - Footer 加註 `*前版保存：articles/{舊日期}-supplement-guide.md*`
   - 同步鏡射至 `reviews/annual/{新日期}-supplement-guide.md`

3. **更新前瞻性參考文件中的當前狀態**
   - `articles/{新日期}-mackay-checkup-addons.md`（若需新建）以新值為基準
   - `index.html` 等公開頁面中引用具體數值的描述（如 UA、LDL 等）更新為最新值
   - 歷史記錄（`reviews/annual/YYYY.md`、`reviews/annual/YYYY-causal-map.html` 等）**不得修改**

4. **commit 訊息格式**
   - 標題：`分版：保留 {舊日期} 原指南，{新日期} 改版另存新檔`
   - 列出新建與保留的檔案清單

5. **判斷原則**
   - 「前瞻性指南」（articles/、index.html 中的策略描述）→ 改版另存新檔，前版保留
   - 「歷史紀錄」（reviews/annual/ 中的當時報告與分析）→ 永不修改
   - 數值更新範圍以「指引性、決策性、未來會被遵循的文字」為準
   - **同年多次健檢**：每次都以日期建立新檔，前版皆保留為連續 baseline 軌跡
