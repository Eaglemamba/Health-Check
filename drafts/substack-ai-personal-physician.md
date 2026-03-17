# 我用 AI 當了三個月的私人醫師——一個軟體工程師的健康逆轉實驗

*當 81% 的醫生都在用 AI 輔助看診，為什麼你不能用 AI 來管理自己的健康？*

---

## 一封來自體檢報告的警告信

今年三月，我拿到了一份讓人不太舒服的體檢報告。

收縮壓 135 mmHg（高血壓前期）、三酸甘油酯偏高、膽固醇超標、尿酸逼近警戒線。我 70 公斤，BMI 在超標邊緣。每天實際睡眠只有 5-6 小時——Garmin 手錶冷冰冰地給我打了 63 分。

醫生說了幾句「少吃鹹、多運動、注意睡眠」，然後下一位。

門診三分鐘。

我站在診所門口想：這四項指標各看一個科，掛號四次、等待四次、被告知同樣的「生活型態調整」四次。半年後回來抽血，好了或沒好，再說。

這不是我想要的健康管理。

我是軟體工程師。我想要的是：每天追蹤、即時反饋、數據驅動的決策、一個不會因為門診爆量而只給我三分鐘的「人」。

所以我做了一件事——**我讓 AI 當我的私人健康管理師。**

---

## 不是取代醫生，是填補那 99% 的空白

讓我先把話說清楚：**AI 不是醫生，我也沒有試圖取代醫生。**

但現實是這樣的：你一年看醫生幾次？兩次？四次？每次十分鐘？

一年 8,760 個小時，你和醫生相處的時間大約 40 分鐘。剩下的 8,759 小時又 20 分鐘，你的健康完全靠自己。

這中間的空白，才是 AI 真正的戰場。

2026 年初，Anthropic 推出了 [Claude for Healthcare](https://www.anthropic.com/news/healthcare-life-sciences)，可以連接 Apple Health、Android Health Connect，讀取你的健康數據。[AMA 調查顯示](https://www.ama-assn.org/practice-management/digital-health/more-80-physicians-use-ai-professionally-ama-survey)，超過 81% 的醫師已經在工作中使用 AI。[NPR 報導](https://www.npr.org/sections/shots-health-news/2026/01/09/nx-s1-5670382/primary-care-doctor-shortage-medical-ai-diagnosis)指出，你的下一個家庭醫師可能完全是線上的、透過 AI 工具來存取。

但我做的事情更基礎、更 DIY——也可能更適合像我一樣的普通人。

我沒有用任何付費健康 AI 產品。我用的是 **Claude Code + Markdown 檔案 + Garmin 手錶 + 一個血壓計**。

---

## 系統架構：極簡但有效

身為工程師，我的第一反應是建系統。但這次我刻意走極簡路線——**沒有 App、沒有資料庫、沒有 Dashboard。只有純文字檔。**

```
templates/          → 模板（每日、每週、每月）
reviews/
  daily/            → 每天一個 .md 檔
  weekly/           → 每週一份回顧
  monthly/          → 每月一份趨勢分析
CLAUDE.md           → AI 的「臨床指引」
index.html          → 半年計畫總覽
```

核心概念很簡單：

1. **每天早上 3 分鐘**，回答五個問題：體重、血壓、睡眠、身體哪裡不舒服、今天打算做什麼
2. **AI 即時記錄**，同步更新到週報表格
3. **AI 根據規則自動給建議**——不是泛泛的「多喝水」，而是根據我當天的具體數據
4. **每週日花 10 分鐘回顧**，看趨勢、找模式
5. **每月底花 20 分鐘**，對照半年計畫的里程碑

最關鍵的部分是 `CLAUDE.md`——這是我寫給 AI 的「臨床指引手冊」。

---

## 教 AI 當你的物理治療師

CLAUDE.md 裡面不是寫「請幫我追蹤健康」這種空泛指令。我寫的是 **具體的臨床決策規則**，就像醫院裡的 clinical protocol。

舉幾個例子：

### 身體信號 → 即時 PT 建議

每天我會記錄身體哪裡不舒服。AI 不只記下來，還會根據部位和強度給物理治療建議：

> **我說：**「左前臂、手腕酸緊，強度 3/10」
>
> **AI 回：**「💡 PT 建議：前臂伸展——手掌朝上，另一手輕壓手指向下 30 秒 ×2。工作每 50 分鐘休息活動手腕。」

如果同一個部位連續出現三天，AI 會升級建議，提供完整的居家復健菜單。五天以上？它會直接建議我去預約物理治療師。

### 數據異常 → 自動警報

規則寫得很具體：

- 收縮壓比前一天上升超過 15 mmHg → 問我是不是昨晚沒睡好、壓力大、或吃太鹹
- 體重一週內掉超過 1.5 公斤 → 警告太快，有痛風發作風險
- Sleep Score < 65 且 Body Battery < 40 → 建議今天只做輕度伸展，暫停靠牆深蹲
- 飲水不到 1.5 公升 → 提醒尿酸排泄效率降低

### 運動自動調整

AI 會根據我的恢復狀態，自動把我分成四級：

| 狀態 | 條件 | 運動建議 |
|------|------|----------|
| 恢復充足 | Sleep Score ≥ 70 + 身體無痛 + 主觀 ≥ 4/5 | 按計畫執行，可嘗試進階 |
| 恢復一般 | Score 65-70 或有輕微不適 | 按計畫但不進階 |
| 恢復不足 | Score < 65 或 Battery < 40 | 降級：深蹲減量、快走改散步 |
| 有疼痛 | 任何部位強度 ≥ 5/10 | 避開該部位，提供替代動作 |

**這不是什麼黑科技。這就是把一個好的物理治療師會做的判斷，寫成 AI 可以執行的規則。**

---

## 那份改變一切的半年計畫

四項指標同時超標，表面上看是四個問題。但深入研究後我發現——**它們共享同一個代謝根源。**

我花了一整個週末，讓 Claude 幫我查文獻、做計算、設計方案。最後產出的是一份完整的半年計畫：

**目標：70 kg → 65 kg，四項指標同步回歸正常。**

這份計畫裡最反直覺的發現：

### 1. 睡眠是一切的起點，不是運動

5-6 小時的睡眠讓高血壓風險增加 3.5 倍，膽固醇代謝基因表達被抑制，尿酸排泄效率降低。**如果睡眠不修好，飲食運動做到 100 分也只能發揮 50% 效果。**

AI 幫我設計了一套「睡眠修復三步驟」：17:00 後減量飲水（解決夜尿）、睡前抬腳 15 分鐘（加速下肢水分回流）、5:30 前不離床的硬性規則。

### 2. 靠牆深蹲是降血壓最強的運動

2023 年《BJSM》統合分析（270 項 RCT、15,827 人）：靠牆深蹲在所有運動類型中降收縮壓排名第一。每週三次、每次 16 分鐘（含休息），12 週可降收縮壓 -12.9 mmHg。

我的收縮壓 135。135 - 13 = 122。**一個動作，可能就讓我從高血壓前期回到正常。**

### 3. 蛋白質的「來源」比「總量」重要

NHANES III 研究顯示總蛋白攝取量與尿酸無顯著相關。但紅肉高攝取者尿酸高 +0.48 mg/dL，乳製品反而降低 -0.21 mg/dL。**所以不是「少吃蛋白質」，而是「換來源」。**

---

## 一個典型的早晨

5:47，Garmin 震動，我醒了。

打開終端機，輸入 `/daily-checkin`。Claude 開始問：

> 「早安。體重？」

70.5。

> 「血壓第一次？」

117/70，心率 82。（等一分鐘，量第二次。）

> 「睡眠狀態？」

22:28 入睡，05:47 起床，中途醒來 1 次（夜尿）。Score 64，Battery 36。主觀恢復感 2/5。

> 「身體信號？」

左前臂酸緊 3 分、手腕酸緊 3 分、肩胛骨酸緊 4 分。

> 「今日運動計畫？」

靠牆深蹲。

三分鐘。檔案存好了。然後 AI 自動附上建議：

> 💡 PT 建議：Sleep Score 64 + Body Battery 36，恢復明顯不足。今天靠牆深蹲建議降級為 2 組 × 20 秒，不追求突破。前臂和肩胛骨酸緊提示上交叉症候群前兆——今天工作時每 50 分鐘做一次前臂伸展和肩胛骨 Y-T-W 靠牆動作。

**這就是我的「私人醫師」。不賣保健品、不推療程、不用排隊掛號。每天三分鐘，精準到我當天的具體狀況。**

---

## 這件事為什麼現在才成為可能

三年前，你沒辦法做到這件事。

不是因為沒有 AI——ChatGPT 在 2022 年底就出來了。而是因為 AI 缺乏三個關鍵能力：

**1. 持久記憶與上下文**

早期的聊天機器人每次對話都是全新的。它不記得你昨天血壓多少、上週睡眠趨勢、上個月身體哪裡不舒服。我用 CLAUDE.md 和 Markdown 檔案系統解決了這個問題——AI 每次啟動都會讀取完整的規則和歷史數據。

**2. 指令遵循能力**

你可以試試看叫早期的 AI「只回答我問的問題，不要多說廢話，控制在兩句話以內」——它做不到。現在的模型可以嚴格遵循複雜的臨床決策樹，在正確的時機觸發正確的建議。

**3. 工具使用能力**

Claude Code 可以直接讀寫檔案、建立目錄結構、執行指令。它不只是「聊天」，而是一個可以操作系統的 agent。這讓整個健康追蹤流程可以自動化——我回答問題，它即時更新所有表格。

---

## 真正的風險：你必須知道的事

我不想寫一篇「AI 拯救了我的健康」的爽文。這件事有真實的風險。

### AI 會出錯

[史丹佛和哈佛的研究](https://time.com/7382493/ai-healthcare-doctors/)發現，AI 醫療模型在高達 22.2% 的案例中產生了嚴重有害的臨床建議。我的應對方式是：**AI 只處理日常追蹤和自我照護建議，任何異常數據（收縮壓 > 160、關節突然紅腫）都直接就醫。**

### 數據不等於診斷

我追蹤的體重、血壓、Sleep Score 都是表面指標。真正的代謝狀況需要抽血才能看到。所以計畫裡有三次抽血追蹤（第 0、3、6 月），這是 AI 無法取代的。

### 自我管理有極限

慢性病管理最需要的不是數據，而是行為改變。AI 可以告訴你「今天要喝 2.5 公升水」，但它沒辦法幫你喝。[正如 TIME 的報導所說](https://time.com/7382493/ai-healthcare-doctors/)：AI 不是在縮減醫療人力的需求——而是在揭露一直存在、卻從未被滿足的巨大需求。

---

## 三個月後的數字

（以下是計畫中的預期進展，不是保證）

我的半年計畫預設的第三個月里程碑：

- **體重：** 70.0 → 67.5 kg
- **收縮壓：** 135 → 125 以下（靠牆深蹲 12 週 RCT 數據支持）
- **Sleep Score：** 63 → 70+（如果睡眠修復有執行）
- **三酸甘油酯：** 預計下降 15-30%（Omega-3 8-12 週效果 + 飲食改善）

第三個月會做完整抽血。到時候再寫一篇，用數字說話。

---

## 你也可以這樣做

你不需要會寫程式。你需要的是：

1. **一個血壓計**（隧道型上臂式，幾百塊）
2. **一支有睡眠追蹤的手錶**（Garmin、Apple Watch、甚至小米手環）
3. **一個 AI 助手**（Claude、ChatGPT 都可以）
4. **每天三分鐘的紀律**

把你的身體指標告訴 AI，請它幫你追蹤趨勢、在異常時提醒你。你不需要建立我這麼複雜的系統——甚至你只要每天跟 AI 說「今天血壓 135/75、睡了 6 小時、右肩有點痠」，它就能開始幫你建立模式、發現趨勢。

**重點不在工具。重點在你願不願意每天花三分鐘，認真看一眼自己的身體。**

---

## 寫在最後

我不是在宣稱 AI 可以取代醫生。我從第一天就預約了睡眠門診和泌尿科。計畫裡有明確的就醫時間表。

但我在宣稱的是：**醫療系統給你的三分鐘門診和半年後再來抽血之間，有一個巨大的空白。AI 可以填補這個空白。**

它不完美。它會出錯。它不能幫你動手術或開處方。

但它可以每天早上問你：「今天身體怎麼樣？」然後認真聽完你的回答。

這件事，連很多醫生都做不到。

---

*這篇文章是「半年健康逆轉計畫」系列的第一篇。我會在第三個月（抽血追蹤後）和第六個月（計畫結束時）各寫一篇更新。如果你對具體的系統設計、模板、或 CLAUDE.md 的寫法有興趣，整個專案是開源的。*

*免責聲明：本文為個人健康管理經驗分享，不構成醫療建議。所有健康決策請諮詢專業醫療人員。*

---

**Sources:**
- [AMA: More than 80% of physicians use AI professionally](https://www.ama-assn.org/practice-management/digital-health/more-80-physicians-use-ai-professionally-ama-survey)
- [AMA: Physicians' use of AI doubled from 2023 to 2026](https://www.fiercehealthcare.com/ai-and-machine-learning/ama-physicians-use-ai-doubled-2023-2026)
- [Anthropic: Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)
- [NPR: Your next primary care doctor could be online only, accessed through an AI tool](https://www.npr.org/sections/shots-health-news/2026/01/09/nx-s1-5670382/primary-care-doctor-shortage-medical-ai-diagnosis)
- [TIME: Healthcare Is AI's Hardest Test](https://time.com/7382493/ai-healthcare-doctors/)
- [BCG: How AI Agents and Tech Will Transform Health Care in 2026](https://www.bcg.com/publications/2026/how-ai-agents-will-transform-health-care)
- [Bessemer Venture Partners: State of Health AI 2026](https://www.bvp.com/atlas/state-of-health-ai-2026)
- [Medium: Claude Code for Life #1 — Managing my Health and Wellness](https://medium.com/data-science-collective/claude-code-for-life-1-managing-my-health-and-wellness-cae435c77030)
- [PMC: AI in chronic disease self-management](https://pmc.ncbi.nlm.nih.gov/articles/PMC12675485/)
- [AHA: Hospitals Advance AI-Enabled Prevention at Scale](https://www.aha.org/aha-center-health-innovation-market-scan/2025-11-18-hospitals-advance-ai-enabled-prevention-scale)
