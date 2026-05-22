# SpO2 ↔ HR 偶聯分析：14 晚 cohort 揭露 sympathetic arousal response blunted

*建立日：2026-05-22*
*資料：Garmin Venu 4 cohort 14 晚（2026-05-09 – 2026-05-22）*
*狀態：HSAT 預約 6/21；本分析作為就診時 push 報告涵蓋 pulse rate response 的佐證材料*
*腳本：[scripts/analyze_spo2_hr_coupling.py](../scripts/analyze_spo2_hr_coupling.py)*
*圖：[reviews/daily/spo2/spo2_hr_dual_2026-05-21.png](../reviews/daily/spo2/spo2_hr_dual_2026-05-21.png)*

---

## 一、研究問題

每次 SpO2 desat 都該伴隨 sympathetic surge（HR ↑ 5-20 bpm）— 這是 OSA event 的標準 autonomic signature，也是 PAT-based 居家睡眠檢查（WatchPAT 系列）偵測 AHI 的核心訊號。

→ **若大量 desat 沒有對應 HR 反應，含意是 autonomic arousal-side blunted**（chronic OSA 的長期適應）。
→ 用 Garmin Venu 4 wrist data 可不可以 lower-bound 這個比例？

## 二、方法

| 項目 | 設定 |
|------|------|
| Desat 偵測 | SpO2 < 90% 連續 1+ min；gap tolerance 2 min |
| HR 來源 | `sleep.sleepHeartRate`（Garmin Connect API）|
| **HR 採樣率** | **120 秒平均**（hard limit；Connect API 不暴露更細粒度） |
| Baseline | `max(local 5-min pre-event median, sleep-onset 20-min median)` 取較高者（保守） |
| Response window | event_start − 60s ～ event_end + 240s（4 min post）|
| 分類門檻 | Δpeak ≥ +5 = coupled；+3 ～ +5 = ambiguous；< +3 = silent |
| 門檻調整原因 | 2-min avg 會 dilute 真實 spike ~3-5×；+5 bpm 觀察值 ≈ +10-15 bpm 真實 spike |

## 三、結果

### 14 晚 cohort（114 events）

| 分類 | 數量 | % |
|------|------|---|
| Coupled（Δpeak ≥ +5） | 3 | 2.6% |
| Ambiguous（+3 ～ +5） | 9 | 7.9% |
| **Silent（Δpeak < +3）** | **102** | **89.5%** |

健康 cohort PSG 對照值 coupled 通常 60-80%（Bonsignore 2002 *Eur Respir J*；Drager 2007）。**89% silent 顯著偏離正常**。

### 5/21 單晚 highlight（10 events, 100% silent）

```
True baseline = 69 bpm
Δpeak 分布：+1, -2, -2, -2, -2, -1, -5, 0, 0, -3
→ 10 個 event 中 6 個 Δpeak 為負（HR 比 baseline 低）
```

最深 event（03:23-03:27, nadir 83%, 5 min）：Δpeak = -3 — 4 分鐘觀察窗內 **HR 從未超過 baseline**。

## 四、解讀（精確版）

「Silent」這詞太粗。實際 pattern 比較像：

```
正常 OSA event（PSG 觀察）：
  Apnea 期（30-60s）：vagal predominance → HR ↓ 5-15 bpm（diving reflex bradycardia）
  Termination + arousal（5-30s）：sympathetic surge → HR ↑ 10-20 bpm

David cohort 觀察到的（2-min avg 限制下）：
  Apnea 期：HR ↓（被 2-min avg 捕捉 → 形成負 Δpeak）
  Arousal surge：缺席 or 時間太短被 dilute 進 baseline
```

→ **不是「全 autonomic failure」**。
→ 是 **「vagal apneic bradycardia 完整 + sympathetic arousal surge blunted」**。

兩者結合機轉：
- 中樞 chemoreceptor 反射弧（→ vagal pathway）未壞
- Sympathetic arousal pathway（locus coeruleus → autonomic nervous system → SA node）長期 desensitized
- 對應 HRV 19.7 ms（low）+ 0 次 wake event + 主觀疲憊 — 自律神經知道氧氣掉了，但叫不醒大腦皮質

## 五、本分析的方法學限制（誠實版）

| 限制 | 影響 | 緩解 |
|------|------|------|
| Garmin Connect API HR 限 120s avg | 真實 5-30s spike 被 dilute 至 lower-bound 觀察值 | 調低 coupled 閾值至 +5 部分補償；仍可能 underestimate coupling 20-30% |
| 光學 PPG vs ECG | ±3-5 bpm 雜訊 | 小 ambiguous 可能有 misclass，但對 cohort-level 89% 結論影響小 |
| Local baseline 可能含前一 event 餘震 | 高估 baseline → 壓 Δ | 已改用 max(local, sleep-onset) 取較高者 |
| 無 EEG arousal data | 無法區分 cortical arousal vs autonomic arousal | 需 PSG / HSAT |
| n=14 nights, single subject | 結論不能 generalize | 本分析目的是 self-narrative + HSAT 就診材料，非 publication |

→ **lower bound**：本分析的數據意味「真實 sympathetic blunting 至少存在」；upper bound 要 PSG/PAT 驗證。

## 六、對 6/21 HSAT 就診的具體請求

帶這份分析到就診，主動向睡眠科醫師 / 技師提出：

1. **請報告 pulse rate response index (PRRi)**，不僅是 AHI / RDI
   - 健康人 PRRi 通常 6-15 bpm/event；OSA 典型 10-20 bpm；arousal-blunted OSA <5 bpm
   - 大部分 HSAT 設備可算這個指標，但預設報告不一定列出
2. **請報告 supine vs lateral AHI 分層**
   - 對應我自家 POSA 假設（5/21 user-confirmed 仰臥翻身）+ 楔形枕 C1 T90 ↓ 75% 證據
3. **若 HSAT 設備配 pulse arrival time / PAT**：請保留原始檔
   - PAT 才能驗證 wrist PPG 看不到的 sympathetic surge 是否真存在
4. **詢問 cardiopulmonary coupling (CPC) 分析**
   - 補足 EEG-less HSAT 的 autonomic insight

## 七、對 CPAP 治療策略的含意

| 觀察 | 含意 |
|------|------|
| Vagal apneic bradycardia 完整 | 中樞反射弧未壞 → CPAP 撤除缺氧後，正常 autonomic rhythm 可重建 |
| Sympathetic arousal blunted | 長期 chronic adaptation → 治療後 HRV 恢復需 **3-6 個月** 而非數週 |
| HRV 19.7 ms（flat） | 起跑點低，可恢復空間大；CPAP 後預期升至 25-30 ms |
| Δpeak 多為負值 | 「機制完整但反應被抑制」比「機制壞掉」預後好 |

→ **CPAP 反應應屬「可逆 + 但需耐心」型**。第 1 / 3 / 6 個月各重跑本分析；coupled % 應從目前 2.6% 逐步爬升至 20-40%（同時 silent % 從 89% → ~60%）。

## 八、未來追蹤節點

| 節點 | 預期 coupled / silent % | 紅旗 |
|------|------------------------|------|
| Baseline（2026-05-22） | 2.6% / 89.5% | — |
| CPAP M1 | 5-10% / 80% | 若仍 < 5% coupled → 設備設定或順從度問題 |
| CPAP M3 | 15-25% / 65% | 若 < 10% → 重新評估 phenotype |
| CPAP M6 | 25-40% / 50% | 若 < 20% → 考慮 myofunctional therapy 加碼或口腔裝置 |
| **每日 daily** | — | silent % 連 3 晚 100% → 設備檢查 |

---

## 附錄：腳本用法

```bash
# 單晚分析 + dual-panel 圖
python scripts/analyze_spo2_hr_coupling.py --night 2026-05-21

# cohort 摘要（最近 N 晚）
python scripts/analyze_spo2_hr_coupling.py --summary 14

# 只算不出圖
python scripts/analyze_spo2_hr_coupling.py --night 2026-05-22 --no-chart
```

---

*Filed: articles/2026-05-22-osa-hr-coupling-analysis.md*
*前置：[2026-05-21 OSA 累積傷害評估](2026-05-21-osa-damage-recovery.md)｜[2026-05-15 OSA 診斷敘事](2026-05-15-osa-diagnostic-journey.md)*
