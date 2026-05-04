/* ============ Health Reversal Plan — panels ============ */
const Tt = window.t;
const DD = window.HC_DATA;

// Compute "weeks since start" — week 1 = days 1-7 from start
function weeksSince(startISO) {
  const start = new Date(startISO + "T00:00:00");
  const now = new Date();
  const days = Math.floor((now - start) / (1000 * 60 * 60 * 24));
  return Math.floor(days / 7) + 1;
}

// Wall sits: started 2026-03-17. Running: started 2026-04-26.
const WALLSIT_START = "2026-03-17";
const RUNNING_START = "2026-04-26";

/* ===== Overview ===== */
function PanelOverview({ lang }) {
  const o = DD.overview;
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Overview" : "總覽"}</div>
      <h2 className="section-title">{lang === "en" ? "Personal profile & action priority" : "個人檔案與行動優先順序"}</h2>
      <div className="grid-2">
        <div className="card">
          <div className="h3">{lang === "en" ? "Personal profile" : "個人檔案"}</div>
          <table className="t">
            <tbody>
              {o.profile[lang].map(([k, v], i) => (
                <tr key={i}><th style={{width:"38%"}}>{k}</th><td>{v}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card">
          <div className="h3">{Tt(o.priority.title, lang)}</div>
          <p className="body">{Tt(o.priority.body, lang)}</p>
          <div className="spacer-12" />
          <div className="row">
            {o.priority.order[lang].map((s, i) => (
              <span key={i} className={"tag " + (i === 0 ? "info" : "")}>{i+1}. {s}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="card">
        <div className="h3">{Tt(o.stack.title, lang)}</div>
        <p className="body" style={{marginBottom: 12}}>{Tt(o.stack.sub, lang)}</p>
        <table className="t">
          <thead><tr>{o.stack.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
          <tbody>
            {o.stack.rows.map(([id, label, delta, note], i) => (
              <tr key={i}>
                <td><strong>{Tt(label, lang)}</strong></td>
                <td className="num-cell">{delta}</td>
                <td>{Tt(note, lang)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ===== Sleep ===== */
function PanelSleep({ lang }) {
  const s = DD.sleep;
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Step zero" : "第零步"}</div>
      <h2 className="section-title">{lang === "en" ? "Sleep repair" : "睡眠修復"}</h2>
      <p className="section-sub">{Tt(s.intro, lang)}</p>

      <div className="grid-2">
        {s.pillars.map((p, i) => (
          <div key={i} className="card">
            <div className="h3">{Tt(p.ttl, lang)}</div>
            <ul className="body" style={{paddingLeft: 18, margin: 0}}>
              {p.items[lang].map((it, j) => <li key={j} style={{marginBottom: 6}}>{it}</li>)}
            </ul>
          </div>
        ))}
      </div>

      <div className="spacer-20" />
      <div className="card">
        <div className="h3">{Tt(s.cbti.ttl, lang)}</div>
        <table className="t">
          <thead><tr>{s.cbti.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
          <tbody>
            {s.cbti.rows.map(([n, name, mech, app], i) => (
              <tr key={i}>
                <td className="num-cell"><strong>{n}</strong></td>
                <td><strong>{Tt(name, lang)}</strong></td>
                <td>{Tt(mech, lang)}</td>
                <td>{Tt(app, lang)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="spacer-20" />
      <div className="card">
        <div className="h3">{Tt(s.metrics.ttl, lang)}</div>
        <div className="grid-2" style={{marginTop: 8}}>
          {s.metrics.items.map(([n, target, color], i) => (
            <div key={i} style={{display: "flex", alignItems: "center", gap: 14, padding: "10px 0"}}>
              <div style={{width: 10, height: 10, borderRadius: 99, background: color}} />
              <div style={{flex: 1}}>
                <div style={{fontWeight: 600, fontSize: 14}}>{n}</div>
                <div style={{fontSize: 12, color: "var(--ink-3)"}}>{target}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ===== Diet ===== */
function PanelDiet({ lang }) {
  const d = DD.diet;
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Modified Mediterranean-DASH" : "改良地中海-DASH"}</div>
      <h2 className="section-title">{lang === "en" ? "Diet plan" : "飲食計畫"}</h2>
      <p className="section-sub">{lang === "en" ? "Sweet-spot macros, low-sodium convenience picks, all-day beverage strategy." : "各宏量的 Sweet Spot、低鈉超商選品、全日飲料策略。"}</p>

      <div className="card">
        <div className="h3">{lang === "en" ? "Daily macros" : "每日宏量目標"}</div>
        <div className="grid-3" style={{marginTop: 10}}>
          {d.macros.map(([id, label, val, unit, note], i) => (
            <div key={i} className="combo">
              <div className="kicker">{Tt(label, lang)}</div>
              <div style={{fontFamily: "var(--font-serif)", fontSize: 32, letterSpacing: "-0.02em", lineHeight: 1}}>
                {val}<span style={{fontFamily: "var(--font-sans)", fontSize: 13, color: "var(--ink-3)", marginLeft: 4}}>{unit}</span>
              </div>
              <div style={{fontSize: 12, color: "var(--ink-3)"}}>{Tt(note, lang)}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="spacer-20" />
      <div className="card">
        <div className="h3">{lang === "en" ? "Lunch combos" : "午餐組合"}</div>
        <div className="grid-3" style={{marginTop: 10}}>
          {d.combos.map((c, i) => (
            <div key={i} className="combo">
              <div className="name">
                {Tt(c.name, lang)}
                {c.recommended && <span className="badge">{lang === "en" ? "BEST" : "推薦"}</span>}
              </div>
              <div className="desc">{Tt(c.desc, lang)}</div>
              <div className="stats">
                <span className="stat">{c.kcal} kcal</span>
                <span className="stat">Na {c.sodium}mg</span>
                <span className="stat">P {c.protein}g</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="spacer-20" />
      <div className="grid-2">
        <div className="card">
          <div className="h3" style={{color: "var(--heart)"}}>{lang === "en" ? "Strictly avoid" : "嚴格避免"}</div>
          <div className="row" style={{marginTop: 8}}>
            {d.avoid[lang].map((x, i) => <span key={i} className="tag bad">{x}</span>)}
          </div>
        </div>
        <div className="card">
          <div className="h3" style={{color: "#1a7338"}}>{lang === "en" ? "Actively increase" : "積極增加"}</div>
          <div className="row" style={{marginTop: 8}}>
            {d.increase[lang].map((x, i) => <span key={i} className="tag ok">{x}</span>)}
          </div>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="card">
        <div className="h3">{Tt(d.fructose.ttl, lang)}</div>
        <p className="body">{Tt(d.fructose.sub, lang)}</p>
        <table className="t">
          <thead><tr>
            <th>{lang === "en" ? "Sweetness" : "甜度"}</th>
            <th>{lang === "en" ? "Added sugar" : "添加糖"}</th>
            <th>{lang === "en" ? "Sugar cubes" : "方糖數"}</th>
          </tr></thead>
          <tbody>
            {d.fructose.rows.map(([name, sugar, cubes], i) => (
              <tr key={i}>
                <td><strong>{Tt(name, lang)}</strong></td>
                <td className="num-cell">{sugar}</td>
                <td className="num-cell">{cubes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ===== Exercise ===== */
function PanelExercise({ lang }) {
  const e = DD.exercise;
  const maxSec = 120;
  const wsWeek = Math.min(Math.max(weeksSince(WALLSIT_START), 1), 12);
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "BJSM 2023 — wall sits #1 for BP" : "BJSM 2023 — 靠牆深蹲降壓第一"}</div>
      <h2 className="section-title">{lang === "en" ? "Exercise & wall sits" : "運動與靠牆深蹲"}</h2>
      <p className="section-sub">{Tt(e.why, lang)}</p>

      <div className="card">
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"baseline",marginBottom:6,flexWrap:"wrap",gap:8}}>
          <div className="h3" style={{margin:0}}>{lang === "en" ? "12-week wall-sit progression" : "12 週漸進計畫"}</div>
          <div style={{fontFamily:"var(--font-mono)",fontSize:11,color:"var(--ink-3)",letterSpacing:"0.04em",textTransform:"uppercase"}}>
            {lang === "en" ? `Currently · Week ${wsWeek} of 12` : `目前 · 第 ${wsWeek} / 12 週`}
          </div>
        </div>
        <div className="wallsit" style={{marginTop: 14}}>
          {e.progression.map(([wk, ang, sec, label]) => {
            const cls = wk === wsWeek ? "now" : (wk < wsWeek ? "past" : "future");
            return (
              <div key={wk} className={"wk " + cls} title={`${Tt(label, lang)} · ${ang}° · ${sec}s`}>
                {wk === wsWeek && <div className="wk-now-pill">{lang === "en" ? "Now" : "本週"}</div>}
                <div className="wk-n">W{wk}</div>
                <div className="wk-bar">
                  <div className="wk-fill" style={{height: `${(sec / maxSec) * 100}%`}} />
                </div>
                <div className="wk-sec">{sec}s</div>
              </div>
            );
          })}
        </div>
        <div className="legend" style={{marginTop: 14}}>
          <span className="legend-item"><span className="dot" style={{background:"var(--heart)"}}/>{lang === "en" ? "Hold time (sec)" : "撐持時間（秒）"}</span>
          <span className="legend-item">{lang === "en" ? "Target: 4 sets × 2 min, 3×/week" : "目標：4 組 × 2 分鐘，每週 3 次"}</span>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="grid-2">
        <div className="card">
          <div className="h3">{Tt(e.technique.ttl, lang)}</div>
          <table className="t">
            <tbody>
              {e.technique.rows.map(([name, desc], i) => (
                <tr key={i}>
                  <td style={{width: "38%"}}><strong>{Tt(name, lang)}</strong></td>
                  <td>{Tt(desc, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card">
          <div className="h3">{lang === "en" ? "Weekly plan — Phase 1" : "每週計畫 — 階段一"}</div>
          <table className="t">
            <thead><tr>{e.weekplan.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {e.weekplan.rows.map(([day, act, dur, when], i) => (
                <tr key={i}>
                  <td><strong>{Tt(day, lang)}</strong></td>
                  <td>{Tt(act, lang)}</td>
                  <td className="num-cell">{dur}</td>
                  <td>{Tt(when, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="callout warn">
        <strong>{lang === "en" ? "Uric acid safety:" : "尿酸安全："}</strong>{" "}
        {lang === "en"
          ? "Avoid high-intensity exercise (lactic acid blocks UA excretion). Stick to RPE 4–6/10. Hydrate 500 mL pre, 200 mL/15 min during."
          : "避免高強度運動（乳酸抑制尿酸排泄）。維持 RPE 4–6/10。運動前 500 mL，運動中每 15 分鐘 200 mL。"}
      </div>
    </div>
  );
}

/* ===== Supplements ===== */
function PanelSupps({ lang }) {
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Active stack · 2026-04-21" : "現用組合 · 2026-04-21"}</div>
      <h2 className="section-title">{lang === "en" ? "Supplements & cost" : "保健品與費用"}</h2>
      <p className="section-sub">{lang === "en" ? "Each supplement targets a specific marker. Food-form nutrition (cocoa, goji, blueberries, nuts, pumpkin seeds) is in the breakfast blend." : "每項保健品針對特定指標。食物形態營養（可可、枸杞、藍莓、堅果、南瓜籽）已整合入早餐果昔。"}</p>

      <div className="grid-2">
        {DD.supps.map((s, i) => (
          <div key={i} className="card" style={{padding: 18}}>
            <div style={{display: "flex", alignItems: "flex-start", gap: 14}}>
              <div style={{width: 38, height: 38, borderRadius: 12, background: s.color, display: "grid", placeItems: "center", flexShrink: 0, color: "white"}}>
                <Icon name="drop" size={18} />
              </div>
              <div style={{flex: 1, minWidth: 0}}>
                <div style={{fontSize: 15, fontWeight: 600, letterSpacing: "-0.01em"}}>{s.name}</div>
                <div style={{fontSize: 12, color: "var(--ink-3)", marginTop: 2}}>{Tt(s.target, lang)}</div>
                <div className="row" style={{marginTop: 10}}>
                  <span className="tag info">{s.dose}</span>
                  <span className="tag">{Tt(s.time, lang)}</span>
                  <span className="tag" style={{fontFamily: "var(--font-mono)"}}>NT$ {s.cost}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="spacer-20" />
      <div className="callout">
        <strong>{lang === "en" ? "Monthly total (active stack):" : "月總費用（現用組合）："}</strong>{" "}
        NT$ 4,520–6,590. {lang === "en" ? "Creatine pending RT resumption · NAC removed · NOW EGCG discontinued (AST 27→38)." : "肌酸待重訓恢復後加入 · NAC 已移除 · NOW EGCG 已停用（AST 27→38）。"}
      </div>
    </div>
  );
}

/* ===== Daily Routine — 24h timeline ===== */
function PanelRoutine({ lang }) {
  const events = DD.routine;
  const startH = 5, endH = 22;
  const span = endH - startH;
  const pos = (h) => ((h - startH) / span) * 100;

  // stagger labels to avoid overlap
  const stems = [62, 90, 118, 146, 62, 90];

  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Front-loaded hydration · cutoff 17:00" : "前載補水 · 17:00 後停"}</div>
      <h2 className="section-title">{lang === "en" ? "Daily routine" : "每日作息"}</h2>
      <p className="section-sub">{lang === "en" ? "Hydration, BP measurement, exercise, meals and supplements integrated into a single daily flow." : "補水、量血壓、運動、餐食、保健品整合成單一每日流程。"}</p>

      <div className="card">
        <div className="day-timeline">
          <div className="day-axis" />
          {events.map((ev, i) => {
            const [h, label, cat] = ev;
            const stemH = stems[i % stems.length];
            return (
              <div key={i} className="day-event" data-cat={cat} style={{left: `${pos(h)}%`}}>
                <div className="lbl">{Tt(label, lang)}</div>
                <div className="stem" style={{height: stemH}} />
                <div className="pin" />
              </div>
            );
          })}
          {[5, 8, 11, 14, 17, 20].map(h => (
            <div key={h} className="day-tick" style={{left: `${pos(h)}%`}}>{h}:00</div>
          ))}
        </div>
        <div className="legend" style={{marginTop: 18}}>
          <span className="legend-item"><span className="dot" style={{background:"var(--sleep)"}}/>{lang === "en" ? "Sleep" : "睡眠"}</span>
          <span className="legend-item"><span className="dot" style={{background:"var(--weight)"}}/>{lang === "en" ? "Meal" : "餐食"}</span>
          <span className="legend-item"><span className="dot" style={{background:"var(--uric)"}}/>{lang === "en" ? "Supplement" : "保健品"}</span>
          <span className="legend-item"><span className="dot" style={{background:"var(--heart)"}}/>{lang === "en" ? "Exercise" : "運動"}</span>
          <span className="legend-item"><span className="dot" style={{background:"var(--ink-3)"}}/>{lang === "en" ? "Cutoff" : "停止"}</span>
        </div>
      </div>
    </div>
  );
}

/* ===== Timeline / months ===== */
function PanelTimeline({ lang }) {
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Six-month roadmap" : "6 個月路徑"}</div>
      <h2 className="section-title">{lang === "en" ? "Timeline & milestones" : "時程與里程碑"}</h2>
      <div className="months">
        {DD.months.map((m, i) => (
          <div key={i} className="month" data-num={"0" + m.num}>
            <div className="ttl">{Tt(m.ttl, lang)}</div>
            <div className="body-sm">{Tt(m.body, lang)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ===== Safety ===== */
function PanelSafety({ lang }) {
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Read before starting" : "啟動前必讀"}</div>
      <h2 className="section-title">{lang === "en" ? "Safety & medical" : "安全與就醫"}</h2>
      <div className="grid-2">
        {DD.safety.map((s, i) => (
          <div key={i} className={"callout " + (s.cls || "")} style={{padding: 18}}>
            <div style={{fontWeight: 600, fontSize: 15, marginBottom: 6, letterSpacing: "-0.01em"}}>{Tt(s.ttl, lang)}</div>
            <div style={{fontSize: 13, lineHeight: 1.55}}>{Tt(s.body, lang)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ===== Tracker ===== */
function PanelTracker({ lang }) {
  const tr = DD.tracker;
  // Sparkline helper
  const spark = (data, color, fmt = (v) => v) => {
    const min = Math.min(...data), max = Math.max(...data);
    const range = max - min || 1;
    const w = 240, h = 50;
    const pts = data.map((v, i) => `${(i / (data.length - 1)) * w},${h - ((v - min) / range) * (h - 6) - 3}`).join(" ");
    const lastY = h - ((data[data.length-1] - min) / range) * (h - 6) - 3;
    return (
      <svg viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none">
        <polyline points={pts} fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx={w} cy={lastY} r="3" fill={color} />
      </svg>
    );
  };

  // Checklist with localStorage
  const [checks, setChecks] = useState(() => {
    try {
      const raw = localStorage.getItem("hc_checks");
      if (raw) {
        const obj = JSON.parse(raw);
        if (obj.date === new Date().toDateString()) return obj.state || {};
      }
    } catch (e) {}
    return {};
  });
  useEffect(() => {
    localStorage.setItem("hc_checks", JSON.stringify({ date: new Date().toDateString(), state: checks }));
  }, [checks]);
  const toggle = (k) => setChecks(s => ({ ...s, [k]: !s[k] }));
  const items = DD.checklist[lang];
  const done = items.filter(([k]) => checks[k]).length;
  const pct = (done / items.length) * 100;

  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Live data · sample numbers" : "即時數據 · 樣本"}</div>
      <h2 className="section-title">{lang === "en" ? "Progress tracker" : "進度追蹤"}</h2>

      <div className="card">
        <div className="h3">{lang === "en" ? "14-day trends" : "14 日趨勢"}</div>
        <div className="spark-wrap" style={{marginTop: 10}}>
          <div className="spark-card">
            <div className="lbl" style={{color:"var(--heart)"}}>{lang === "en" ? "Systolic BP" : "收縮壓"}</div>
            <div className="num">{tr.bp[tr.bp.length-1][0]}<small style={{fontFamily:"var(--font-sans)",fontSize:13,color:"var(--ink-3)",marginLeft:4}}>mmHg</small></div>
            {spark(tr.bp.map(b => b[0]), "var(--heart)")}
          </div>
          <div className="spark-card">
            <div className="lbl" style={{color:"var(--weight)"}}>{lang === "en" ? "Weight" : "體重"}</div>
            <div className="num">{tr.weight[tr.weight.length-1].toFixed(1)}<small style={{fontFamily:"var(--font-sans)",fontSize:13,color:"var(--ink-3)",marginLeft:4}}>kg</small></div>
            {spark(tr.weight, "var(--weight)")}
          </div>
          <div className="spark-card">
            <div className="lbl" style={{color:"var(--sleep)"}}>{lang === "en" ? "Sleep score" : "睡眠分數"}</div>
            <div className="num">{tr.sleep[tr.sleep.length-1]}</div>
            {spark(tr.sleep, "var(--sleep)")}
          </div>
          <div className="spark-card">
            <div className="lbl" style={{color:"var(--metabolic)"}}>{lang === "en" ? "Body Battery" : "身體電量"}</div>
            <div className="num">{tr.bb[tr.bb.length-1]}</div>
            {spark(tr.bb, "var(--metabolic)")}
          </div>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="card">
        <div style={{display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 12}}>
          <div className="h3" style={{margin:0}}>{lang === "en" ? "Today's checklist" : "今日清單"}</div>
          <div style={{fontSize: 13, color: "var(--ink-3)"}}>{done} / {items.length}</div>
        </div>
        <div style={{height: 6, borderRadius: 999, background: "var(--line)", overflow: "hidden", marginBottom: 16}}>
          <div style={{height: "100%", width: `${pct}%`, background: "linear-gradient(90deg, var(--metabolic), var(--water))", transition: "width .3s"}} />
        </div>
        <div className="checklist">
          {items.map(([k, label]) => (
            <div key={k} className={"check-item" + (checks[k] ? " done" : "")} onClick={() => toggle(k)}>
              <div className="check-box" />
              <div>
                <div className="lbl">{label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ===== Running ===== */
function PanelRunning({ lang }) {
  const r = DD.running;
  const rWeek = Math.min(Math.max(weeksSince(RUNNING_START), 1), 8);
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Started 2026-04-26 · Z2 capped" : "2026-04-26 起步 · 限 Z2"}</div>
      <h2 className="section-title">{lang === "en" ? "Running — base building" : "跑步 — 建立基礎"}</h2>
      <p className="section-sub">{Tt(r.intro, lang)}</p>

      <div className="card">
        <div className="h3" style={{color: "var(--heart)"}}>{Tt(r.rules.ttl, lang)}</div>
        <ul className="body" style={{paddingLeft: 18, margin: "8px 0 0"}}>
          {r.rules.items[lang].map((it, i) => <li key={i} style={{marginBottom: 8}}>{it}</li>)}
        </ul>
      </div>

      <div className="spacer-20" />
      <div className="card">
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"baseline",marginBottom:6,flexWrap:"wrap",gap:8}}>
          <div className="h3" style={{margin:0}}>{lang === "en" ? "8-week run-walk progression" : "8 週跑走漸進計畫"}</div>
          <div style={{fontFamily:"var(--font-mono)",fontSize:11,color:"var(--ink-3)",letterSpacing:"0.04em",textTransform:"uppercase"}}>
            {lang === "en" ? `Currently · Week ${rWeek} of 8` : `目前 · 第 ${rWeek} / 8 週`}
          </div>
        </div>
        <p className="body" style={{margin:"0 0 14px",fontSize:13,color:"var(--ink-3)"}}>
          {lang === "en"
            ? "Two run-walk sessions per week (Mon, Thu). Z2 effort throughout — if you can't talk, slow down."
            : "每週兩次跑走（一、四）。全程 Zone 2 — 不能說話就放慢。"}
        </p>
        <div className="runprog">
          {r.progression.map(([wk, label, fmt, totalMin, runFrac]) => {
            const cls = wk === rWeek ? "now" : (wk < rWeek ? "past" : "future");
            return (
              <div key={wk} className={"rwk " + cls}>
                {wk === rWeek && <div className="wk-now-pill">{lang === "en" ? "Now" : "本週"}</div>}
                <div className="rwk-n">W{wk}</div>
                <div className="rwk-label">{Tt(label, lang)}</div>
                <div className="rwk-fmt">{Tt(fmt, lang)}</div>
                <div className="rwk-min">
                  {totalMin}{lang === "en" ? " min · " : " 分 · "}
                  {Math.round(runFrac * 100)}% {lang === "en" ? "run" : "跑"}
                </div>
                <div className="rwk-bar">
                  <div className="rwk-bar-fill" style={{width: `${runFrac * 100}%`}} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="spacer-20" />
      <div className="grid-2">
        <div className="card">
          <div className="h3">{Tt(r.schedule.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{r.schedule.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {r.schedule.rows.map(([day, prim, why], i) => (
                <tr key={i}>
                  <td><strong>{Tt(day, lang)}</strong></td>
                  <td>{Tt(prim, lang)}</td>
                  <td style={{color:"var(--ink-3)",fontSize:12}}>{Tt(why, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card">
          <div className="h3">{Tt(r.metrics.ttl, lang)}</div>
          <div style={{marginTop:8}}>
            {r.metrics.items.map(([n, target, color], i) => (
              <div key={i} style={{display:"flex",alignItems:"center",gap:14,padding:"10px 0",borderBottom: i < r.metrics.items.length-1 ? "1px solid var(--line)" : "none"}}>
                <div style={{width:10,height:10,borderRadius:99,background:color}} />
                <div style={{flex:1}}>
                  <div style={{fontWeight:600,fontSize:14}}>{n}</div>
                  <div style={{fontSize:12,color:"var(--ink-3)"}}>{typeof target === "string" ? target : Tt(target, lang)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="callout warn">
        <strong>{lang === "en" ? "UA 8.9 reminder:" : "尿酸 8.9 提醒："}</strong>{" "}
        {lang === "en"
          ? "Stay strictly in Z2 until UA normalizes. Lactic acid competes with urate at renal tubule transporters — push too hard and UA will spike for 24-72h."
          : "尿酸正常前嚴格守 Zone 2。乳酸與尿酸鹽在腎小管轉運子競爭排泄，硬推之後尿酸會升高 24-72 小時。"}
      </div>
    </div>
  );
}

Object.assign(window, {
  PanelOverview, PanelSleep, PanelDiet, PanelExercise, PanelRunning,
  PanelSupps, PanelRoutine, PanelTimeline, PanelSafety, PanelTracker,
});
