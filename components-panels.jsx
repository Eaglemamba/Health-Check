/* ============ Health Reversal Plan — panels ============ */
const Tt = window.t;
const DD = window.HC_DATA;
const Icon = window.Icon;

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

      {o.threeLeverages && (<>
        <div className="spacer-20" />
        <div className="card" style={{borderTop: "3px solid var(--heart)"}}>
          <div className="h3" style={{color: "var(--heart)"}}>{Tt(o.threeLeverages.ttl, lang)}</div>
          <p className="body" style={{marginBottom: 12}}>{Tt(o.threeLeverages.intro, lang)}</p>
          <table className="t">
            <thead><tr>{o.threeLeverages.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {o.threeLeverages.rows.map(([marker, diet, ex, sleep], i) => (
                <tr key={i}>
                  <td><strong>{Tt(marker, lang)}</strong></td>
                  <td style={{fontSize: 12}}>{typeof diet === "string" ? diet : Tt(diet, lang)}</td>
                  <td style={{fontSize: 12}}>{typeof ex === "string" ? ex : Tt(ex, lang)}</td>
                  <td style={{fontSize: 12, fontWeight: 500}}>{typeof sleep === "string" ? sleep : Tt(sleep, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {o.threeLeverages.reframe && (
            <div style={{marginTop: 16}}>
              <div className="h4" style={{fontSize: 14, marginBottom: 10}}>{Tt(o.threeLeverages.reframe.ttl, lang)}</div>
              <div className="grid-2">
                <div className="callout warn" style={{padding: 14}}>
                  <div style={{fontWeight: 600, fontSize: 12, marginBottom: 4, opacity: 0.7}}>{lang === "en" ? "Old (past 11 yr)" : "舊（過去 11 年）"}</div>
                  <div style={{fontSize: 13, lineHeight: 1.55}}>{Tt(o.threeLeverages.reframe.old, lang)}</div>
                </div>
                <div className="callout" style={{padding: 14, borderLeft: "3px solid var(--heart)"}}>
                  <div style={{fontWeight: 600, fontSize: 12, marginBottom: 4, opacity: 0.7}}>{lang === "en" ? "New (next 6 mo)" : "新（接下來 6 個月）"}</div>
                  <div style={{fontSize: 13, lineHeight: 1.55}}>{Tt(o.threeLeverages.reframe.new, lang)}</div>
                </div>
              </div>
              <div className="callout" style={{marginTop: 10, padding: 14}}>
                <strong>{lang === "en" ? "Takeaway: " : "結論："}</strong>{Tt(o.threeLeverages.reframe.takeaway, lang)}
              </div>
            </div>
          )}
        </div>
      </>)}
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

      {d.breakfast && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.breakfast.ttl, lang)}</div>
          <p className="body">{Tt(d.breakfast.sub, lang)}</p>
          <table className="t">
            <thead><tr>{d.breakfast.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.breakfast.rows.map(([name, items, kcal, hi], i) => (
                <tr key={i}>
                  <td><strong>{Tt(name, lang)}</strong></td>
                  <td>{Tt(items, lang)}</td>
                  <td className="num-cell">{kcal}</td>
                  <td>{Tt(hi, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="spacer-12" />
          <div className="h3" style={{fontSize: 14}}>{Tt(d.breakfast.oatTips.ttl, lang)}</div>
          <ul className="body" style={{paddingLeft: 18, margin: "4px 0 0"}}>
            {d.breakfast.oatTips.items[lang].map((it, i) => <li key={i} style={{marginBottom: 4}}>{it}</li>)}
          </ul>
        </div>
      </>)}

      {d.yogurtBlend && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.yogurtBlend.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{d.yogurtBlend.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.yogurtBlend.rows.map(([name, amt, prov], i) => (
                <tr key={i}>
                  <td><strong>{Tt(name, lang)}</strong></td>
                  <td>{typeof amt === "string" ? amt : Tt(amt, lang)}</td>
                  <td>{Tt(prov, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="body" style={{marginTop: 8}}><em>{Tt(d.yogurtBlend.note, lang)}</em></p>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Blending vs juicing: " : "果汁機 vs 榨汁："}</strong>
            {Tt(d.yogurtBlend.blending, lang)}
          </div>
        </div>
      </>)}

      {d.boxes711 && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.boxes711.ttl, lang)}</div>
          <p className="body">{Tt(d.boxes711.sub, lang)}</p>
          <table className="t">
            <thead><tr>{d.boxes711.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.boxes711.rows.map(([name, kcal, na, prot, note, best], i) => (
                <tr key={i}>
                  <td>
                    <strong>{Tt(name, lang)}</strong>
                    {best && <span className="badge" style={{marginLeft: 6}}>{lang === "en" ? "BEST" : "首選"}</span>}
                  </td>
                  <td className="num-cell">{kcal}</td>
                  <td className="num-cell">{na}</td>
                  <td className="num-cell">{prot}</td>
                  <td>{Tt(note, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout warn" style={{marginTop: 8}}>
            <strong>{Tt(d.boxes711.avoid.ttl, lang)}：</strong> {Tt(d.boxes711.avoid.body, lang)}
          </div>
        </div>
      </>)}

      {d.proteinSides && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.proteinSides.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{d.proteinSides.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.proteinSides.rows.map(([name, kcal, na, prot, rating, cls], i) => (
                <tr key={i}>
                  <td><strong>{Tt(name, lang)}</strong></td>
                  <td className="num-cell">{kcal}</td>
                  <td className="num-cell">{typeof na === "string" ? na : Tt(na, lang)}</td>
                  <td className="num-cell">{prot}</td>
                  <td><span className={"tag " + (cls === "ok" ? "ok" : cls === "bad" ? "bad" : "")}>{Tt(rating, lang)}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}

      {d.tofu && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.tofu.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{d.tofu.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.tofu.rows.map(([name, na, cls, note], i) => (
                <tr key={i}>
                  <td><strong>{Tt(name, lang)}</strong></td>
                  <td className="num-cell">{typeof na === "string" ? na : Tt(na, lang)}</td>
                  <td><span className={"tag " + (cls === "ok" ? "ok" : cls === "bad" ? "bad" : "")}>
                    {cls === "ok" ? (lang === "en" ? "Excellent" : "極佳") : cls === "bad" ? (lang === "en" ? "Avoid" : "避免") : (lang === "en" ? "Limit" : "限量")}
                  </span></td>
                  <td>{Tt(note, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}

      {d.drinks && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.drinks.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{d.drinks.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.drinks.rows.map(([name, kcal, na, prot, note], i) => (
                <tr key={i}>
                  <td><strong>{Tt(name, lang)}</strong></td>
                  <td className="num-cell">{kcal}</td>
                  <td className="num-cell">{na}</td>
                  <td className="num-cell">{prot}</td>
                  <td>{Tt(note, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}

      {d.beverage && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.beverage.ttl, lang)}</div>
          <p className="body">{Tt(d.beverage.sub, lang)}</p>
          <table className="t">
            <thead><tr>{d.beverage.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.beverage.rows.map(([time, drink, target], i) => (
                <tr key={i}>
                  <td><strong>{Tt(time, lang)}</strong></td>
                  <td>{Tt(drink, lang)}</td>
                  <td>{Tt(target, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{Tt(d.beverage.note.ttl, lang)}：</strong> {Tt(d.beverage.note.body, lang)}
          </div>
        </div>
      </>)}

      {d.dinnerBrands && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.dinnerBrands.ttl, lang)}</div>
          <p className="body">{Tt(d.dinnerBrands.familyNote, lang)}</p>
          <table className="t">
            <thead><tr>{d.dinnerBrands.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.dinnerBrands.rows.map(([brand, feat, rec, price], i) => (
                <tr key={i}>
                  <td><strong>{Tt(brand, lang)}</strong></td>
                  <td>{Tt(feat, lang)}</td>
                  <td>{Tt(rec, lang)}</td>
                  <td className="num-cell">{price}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="body" style={{marginTop: 8}}><strong>{Tt(d.dinnerBrands.mantra, lang)}</strong></p>
        </div>
      </>)}

      {d.principles && (<>
        <div className="spacer-20" />
        <div className="callout">
          <div style={{fontWeight: 600, marginBottom: 8}}>{Tt(d.principles.ttl, lang)}</div>
          <ol style={{paddingLeft: 20, margin: 0}}>
            {d.principles.items[lang].map((it, i) => <li key={i} style={{marginBottom: 4}}>{it}</li>)}
          </ol>
        </div>
      </>)}

      {d.fructoseHidden && (<>
        <div className="spacer-20" />
        <div className="card" style={{borderTop: "3px solid var(--uric)"}}>
          <div className="h3" style={{color: "var(--uric)"}}>{Tt(d.fructoseHidden.ttl, lang)}</div>
          <p className="body">{Tt(d.fructoseHidden.sub, lang)}</p>
          <table className="t">
            <thead><tr>{d.fructoseHidden.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.fructoseHidden.rows.map(([src, load, action, cls], i) => (
                <tr key={i}>
                  <td><strong>{Tt(src, lang)}</strong></td>
                  <td style={{fontSize: 12}}>{Tt(load, lang)}</td>
                  <td style={{fontSize: 12}}>{Tt(action, lang)}</td>
                  <td><span className={"tag " + (cls === "ok" ? "ok" : cls === "bad" ? "bad" : "")}>
                    {cls === "ok" ? (lang === "en" ? "OK" : "可") : cls === "bad" ? (lang === "en" ? "Avoid" : "避免") : (lang === "en" ? "Limit" : "限量")}
                  </span></td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{Tt(d.fructoseHidden.audit.ttl, lang)}：</strong> {Tt(d.fructoseHidden.audit.body, lang)}
          </div>
        </div>
      </>)}

      {d.fruits && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(d.fruits.ttl, lang)}</div>
          <p className="body">{Tt(d.fruits.sub, lang)}</p>
          <table className="t">
            <thead><tr>{d.fruits.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {d.fruits.rows.map(([name, frc, suit, cls], i) => (
                <tr key={i}>
                  <td><strong>{Tt(name, lang)}</strong></td>
                  <td className="num-cell">{frc}</td>
                  <td><span className={"tag " + (cls === "ok" ? "ok" : cls === "bad" ? "bad" : "")}>{Tt(suit, lang)}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}
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

      {e.selfCheck && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(e.selfCheck.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{e.selfCheck.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {e.selfCheck.rows.map(([chk, ok, warn, fix], i) => (
                <tr key={i}>
                  <td><strong>{Tt(chk, lang)}</strong></td>
                  <td>{Tt(ok, lang)}</td>
                  <td>{Tt(warn, lang)}</td>
                  <td>{Tt(fix, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}

      {e.phases && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(e.phases.ttl, lang)}</div>
          <div className="grid-3" style={{marginTop: 10}}>
            {e.phases.items.map((p, i) => (
              <div key={i} className="combo">
                <div className="kicker">{Tt(p.range, lang)} · {p.vol}</div>
                <div style={{fontFamily: "var(--font-serif)", fontSize: 28, letterSpacing: "-0.02em", lineHeight: 1, marginTop: 4}}>
                  {lang === "en" ? `Phase ${p.ph}` : `階段 ${p.ph}`}
                </div>
                <div style={{fontSize: 13, color: "var(--ink-3)", marginTop: 8, lineHeight: 1.5}}>{Tt(p.body, lang)}</div>
              </div>
            ))}
          </div>
        </div>
      </>)}
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
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2.5s6 7 6 11.5a6 6 0 0 1-12 0c0-4.5 6-11.5 6-11.5z"/>
                </svg>
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

      {DD.suppsDetail && DD.suppsDetail.fullStack && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.suppsDetail.fullStack.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{DD.suppsDetail.fullStack.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {DD.suppsDetail.fullStack.rows.map(([pri, item, dose, time, cost], i) => (
                <tr key={i}>
                  <td className="num-cell"><strong>{pri}</strong></td>
                  <td>{item}</td>
                  <td>{dose}</td>
                  <td>{Tt(time, lang)}</td>
                  <td className="num-cell" style={{fontFamily: "var(--font-mono)"}}>{cost}</td>
                </tr>
              ))}
              <tr style={{background: "var(--bg-soft)"}}>
                <td colSpan="4"><strong>{Tt(DD.suppsDetail.fullStack.total, lang)}</strong></td>
                <td></td>
              </tr>
              {DD.suppsDetail.fullStack.pending.map((p, i) => (
                <tr key={"pend-" + i} style={{opacity: 0.55}}>
                  <td>—</td>
                  <td>{p.item}</td>
                  <td>{p.dose}</td>
                  <td>{Tt(p.reason, lang)}</td>
                  <td className="num-cell" style={{fontFamily: "var(--font-mono)"}}>{p.cost}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{Tt(DD.suppsDetail.fullStack.foodForm.ttl, lang)}：</strong>{" "}
            {Tt(DD.suppsDetail.fullStack.foodForm.body, lang)}
          </div>
        </div>
      </>)}

      {DD.suppsDetail && DD.suppsDetail.rtg && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.suppsDetail.rtg.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{DD.suppsDetail.rtg.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {DD.suppsDetail.rtg.rows.map(([form, fname, conc, abs, note], i) => (
                <tr key={i}>
                  <td><strong>{form}</strong></td>
                  <td>{Tt(fname, lang)}</td>
                  <td className="num-cell">{conc}</td>
                  <td className="num-cell">{abs}</td>
                  <td>{Tt(note, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="body" style={{marginTop: 8}}>{Tt(DD.suppsDetail.rtg.note, lang)}</p>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Taiwan regulation: " : "台灣法規："}</strong>{Tt(DD.suppsDetail.rtg.taiwan, lang)}
          </div>
        </div>
      </>)}

      {DD.suppsDetail && DD.suppsDetail.citrulline && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.suppsDetail.citrulline.ttl, lang)}</div>
          <p className="body">{Tt(DD.suppsDetail.citrulline.intro, lang)}</p>
          <ol style={{paddingLeft: 20, margin: "8px 0"}}>
            {DD.suppsDetail.citrulline.points[lang].map((it, i) => <li key={i} style={{marginBottom: 6, fontSize: 13, lineHeight: 1.5}}>{it}</li>)}
          </ol>
          <p className="body" style={{marginTop: 8}}><strong>{lang === "en" ? "BP data: " : "血壓數據："}</strong>{Tt(DD.suppsDetail.citrulline.bp, lang)}</p>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Current dosing (2026-04-21): " : "現行劑量（2026-04-21）："}</strong>{Tt(DD.suppsDetail.citrulline.dose, lang)}
          </div>
          {DD.suppsDetail.citrulline.regression && (
            <div className="callout warn" style={{marginTop: 8}}>
              <div style={{fontWeight: 600, marginBottom: 6}}>{Tt(DD.suppsDetail.citrulline.regression.ttl, lang)}</div>
              <div style={{fontSize: 13, lineHeight: 1.55}}>{Tt(DD.suppsDetail.citrulline.regression.body, lang)}</div>
            </div>
          )}
        </div>
      </>)}

      {DD.suppsDetail && DD.suppsDetail.hibiscus && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.suppsDetail.hibiscus.ttl, lang)}</div>
          <ul className="body" style={{paddingLeft: 18, margin: "4px 0"}}>
            {DD.suppsDetail.hibiscus.points[lang].map((it, i) => <li key={i} style={{marginBottom: 6, fontSize: 13, lineHeight: 1.5}}>{it}</li>)}
          </ul>
          <div className="callout warn" style={{marginTop: 8}}>
            <div style={{fontWeight: 600, marginBottom: 6}}>{Tt(DD.suppsDetail.hibiscus.safety.ttl, lang)}</div>
            <ul style={{paddingLeft: 18, margin: 0}}>
              {DD.suppsDetail.hibiscus.safety.items[lang].map((it, i) => <li key={i} style={{marginBottom: 4}}>{it}</li>)}
            </ul>
          </div>
        </div>
      </>)}

      {DD.suppsDetail && DD.suppsDetail.creatine && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.suppsDetail.creatine.ttl, lang)}</div>
          <p className="body"><strong>{lang === "en" ? "Benefits: " : "好處："}</strong>{Tt(DD.suppsDetail.creatine.benefits, lang)}</p>
          <div style={{fontWeight: 600, marginTop: 10, fontSize: 13}}>{lang === "en" ? "Two caveats before adding:" : "加入前兩項警示："}</div>
          <ol style={{paddingLeft: 20, margin: "4px 0"}}>
            {DD.suppsDetail.creatine.caveats[lang].map((it, i) => <li key={i} style={{marginBottom: 4, fontSize: 13, lineHeight: 1.5}}>{it}</li>)}
          </ol>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Decision trigger: " : "加入時機："}</strong>{Tt(DD.suppsDetail.creatine.trigger, lang)}
          </div>
        </div>
      </>)}

      {DD.suppsDetail && DD.suppsDetail.plans && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.suppsDetail.plans.ttl, lang)}</div>
          <div className="grid-2" style={{marginTop: 10}}>
            {[DD.suppsDetail.plans.planA, DD.suppsDetail.plans.planB].map((plan, idx) => (
              <div key={idx} style={{padding: 14, border: "1px solid var(--line)", borderRadius: "var(--radius-sm)"}}>
                <div className="h3" style={{margin: 0, fontSize: 14}}>{Tt(plan.ttl, lang)}</div>
                <table className="t" style={{marginTop: 8}}>
                  <tbody>
                    {plan.rows.map(([item, spec, use, cost], i) => (
                      <tr key={i}>
                        <td><strong>{Tt(item, lang)}</strong></td>
                        <td style={{fontSize: 12}}>{typeof spec === "string" ? spec : Tt(spec, lang)}</td>
                        <td style={{fontSize: 12}}>{typeof use === "string" ? use : Tt(use, lang)}</td>
                        <td className="num-cell" style={{fontFamily: "var(--font-mono)", fontSize: 12}}>{cost}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <div style={{marginTop: 8, fontWeight: 700, fontFamily: "var(--font-mono)"}}>
                  {idx === 0 ? (lang === "en" ? "Total: " : "月總：") : (lang === "en" ? "Total: " : "月總：")}{plan.total}
                </div>
              </div>
            ))}
          </div>
          <div className="callout" style={{marginTop: 12}}>
            <strong>{lang === "en" ? "Where does the savings go? " : "省下的錢去哪？"}</strong>{Tt(DD.suppsDetail.plans.savings, lang)}
          </div>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Bottom line: " : "結論："}</strong>{Tt(DD.suppsDetail.plans.bottom, lang)}
          </div>
        </div>
      </>)}
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

      {DD.routineDetail && DD.routineDetail.hourly && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.routineDetail.hourly.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{DD.routineDetail.hourly.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {DD.routineDetail.hourly.rows.map(([time, act, hyd, note], i) => (
                <tr key={i}>
                  <td><strong style={{fontFamily: "var(--font-mono)"}}>{time}</strong></td>
                  <td>{Tt(act, lang)}</td>
                  <td>{typeof hyd === "string" ? hyd : Tt(hyd, lang)}</td>
                  <td style={{fontSize: 12, lineHeight: 1.5}}>{Tt(note, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Daily hydration: " : "每日補水："}</strong>{Tt(DD.routineDetail.hourly.hydrationTotal, lang)}
          </div>
        </div>
      </>)}

      {DD.routineDetail && DD.routineDetail.summary && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(DD.routineDetail.summary.ttl, lang)}</div>
          <ul className="body" style={{paddingLeft: 18, margin: "8px 0 0"}}>
            {DD.routineDetail.summary.items[lang].map((it, i) => <li key={i} style={{marginBottom: 6, fontSize: 13, lineHeight: 1.5}}>{it}</li>)}
          </ul>
          <div className="spacer-12" />
          <div className="h3" style={{fontSize: 14}}>{lang === "en" ? "Daily extras (added 2026-04-22)" : "每日附加（2026-04-22 新增）"}</div>
          <ul className="body" style={{paddingLeft: 18, margin: "4px 0 0"}}>
            {DD.routineDetail.summary.extras[lang].map((it, i) => <li key={i} style={{marginBottom: 4, fontSize: 13, lineHeight: 1.5}}>{it}</li>)}
          </ul>
        </div>
      </>)}

      {DD.routineDetail && DD.routineDetail.bpTips && (<>
        <div className="spacer-20" />
        <div className="callout">
          <div style={{fontWeight: 600, marginBottom: 6}}>{Tt(DD.routineDetail.bpTips.ttl, lang)}</div>
          <div style={{fontSize: 13, lineHeight: 1.55}}>{Tt(DD.routineDetail.bpTips.body, lang)}</div>
        </div>
      </>)}
    </div>
  );
}

/* ===== Timeline / months ===== */
function PanelTimeline({ lang }) {
  const baseline = DD.milestoneStart;
  const currentWeight = DD.hero.currentWeight;
  const startDate = new Date(baseline.fullDate + "T00:00:00");
  const today = new Date();
  const daysSince = Math.max(0, Math.floor((today - startDate) / 86400000));
  // Each month phase = 30.44 days (avg). Current month index (0=in M1 phase, 1=in M2 phase, ...).
  const monthsElapsed = daysSince / 30.44;
  const currentMonthIdx = Math.min(6, Math.floor(monthsElapsed) + 1); // which month phase we're IN
  // Find most recent past milestone (target weight already due) for comparison
  const lastDueMonth = DD.months.filter(m => m.num < currentMonthIdx).pop() || null;
  const lastDueTarget = lastDueMonth ? lastDueMonth.weight : baseline.weight;
  const lastDueDelta = +(currentWeight - lastDueTarget).toFixed(1);
  const onTrack = lastDueDelta <= 0.3; // within +0.3 kg of target considered on track
  const ahead = lastDueDelta <= -0.2;

  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Six-month roadmap" : "6 個月路徑"}</div>
      <h2 className="section-title">{lang === "en" ? "Timeline & milestones" : "時程與里程碑"}</h2>

      {/* Progress summary */}
      <div className="milestone-summary">
        <div className="ms-row">
          <div className="ms-col">
            <div className="ms-lbl">{lang === "en" ? "Day" : "第幾天"}</div>
            <div className="ms-val">{daysSince}</div>
            <div className="ms-sub">/ 183 ({lang === "en" ? "6 mo" : "6 個月"})</div>
          </div>
          <div className="ms-col">
            <div className="ms-lbl">{lang === "en" ? "Current phase" : "目前階段"}</div>
            <div className="ms-val">M{currentMonthIdx}</div>
            <div className="ms-sub">{lang === "en" ? `${(monthsElapsed).toFixed(1)} mo elapsed` : `已過 ${(monthsElapsed).toFixed(1)} 個月`}</div>
          </div>
          <div className="ms-col">
            <div className="ms-lbl">{lang === "en" ? "Current weight" : "目前體重"}</div>
            <div className="ms-val">{currentWeight}<span className="ms-unit">kg</span></div>
            <div className="ms-sub">{DD.hero.currentWeightDate}</div>
          </div>
          <div className="ms-col">
            <div className="ms-lbl">{lang === "en" ? `vs M${lastDueMonth ? lastDueMonth.num : 0} target` : `vs M${lastDueMonth ? lastDueMonth.num : 0} 目標`}</div>
            <div className={"ms-val " + (ahead ? "ms-ahead" : onTrack ? "ms-ok" : "ms-behind")}>
              {lastDueDelta > 0 ? "+" : ""}{lastDueDelta}<span className="ms-unit">kg</span>
            </div>
            <div className="ms-sub">
              {lang === "en"
                ? (ahead ? "Ahead of plan" : onTrack ? "On track" : "Behind target")
                : (ahead ? "超前進度" : onTrack ? "達標" : "落後目標")}
              {" · "}{lang === "en" ? "target" : "目標"} {lastDueTarget} kg
            </div>
          </div>
        </div>
      </div>

      <div className="spacer-12" />

      {/* Baseline (M0) + 6 month cards */}
      <div className="months months-7">
        <div className="month baseline" data-num="M0">
          <div className="ttl">{Tt(baseline.label, lang)}</div>
          <div className="m-meta">
            <span className="m-date">{baseline.date}</span>
            <span className="m-weight">{baseline.weight} kg</span>
          </div>
          {baseline.bodyFat != null && (
            <div className="m-bf">{lang === "en" ? "BF" : "體脂"} {baseline.bodyFat}%</div>
          )}
          <div className="body-sm">{lang === "en" ? "Starting point" : "起始點"}</div>
        </div>
        {DD.months.map((m, i) => {
          const isCurrent = (currentMonthIdx === m.num);
          const isPast = currentMonthIdx > m.num;
          const isFuture = currentMonthIdx < m.num;
          const delta = (isPast || isCurrent) ? +(currentWeight - m.weight).toFixed(1) : null;
          const status = delta === null ? "" : (delta <= -0.2 ? "ahead" : delta <= 0.3 ? "ok" : "behind");
          return (
            <div key={i} className={"month m-" + (isCurrent ? "current" : isPast ? "past" : "future")} data-num={"M" + m.num}>
              <div className="ttl">{Tt(m.ttl, lang)}</div>
              <div className="m-meta">
                <span className="m-date">{m.date}</span>
                <span className="m-weight">{m.weight} kg</span>
              </div>
              {m.bodyFat != null && (
                <div className="m-bf">{lang === "en" ? "BF target" : "體脂目標"} ≤ {m.bodyFat}%</div>
              )}
              {delta !== null && (
                <div className={"m-delta m-" + status}>
                  {delta > 0 ? "+" : ""}{delta} kg {lang === "en" ? "vs target" : "vs 目標"}
                </div>
              )}
              <div className="body-sm">{Tt(m.body, lang)}</div>
            </div>
          );
        })}
      </div>

      <div className="spacer-12" />
      <div className="callout" style={{fontSize: 12, lineHeight: 1.55}}>
        <strong>{lang === "en" ? "Weight trajectory: " : "體重路徑："}</strong>
        {lang === "en"
          ? "Linear plan loses ~0.83 kg/month (~0.2 kg/wk) — gentle deficit. Saturday morning reading is the official weekly value."
          : "計畫每月平均降 0.83 kg（約 0.2 kg/週）— 緩和熱量赤字。每週六晨間排尿後為正式體重讀數。"}
      </div>
    </div>
  );
}

/* ===== Safety ===== */
function PanelSafety({ lang }) {
  const sd = DD.safetyDetail;
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

      {sd && sd.triadPriority && (<>
        <div className="spacer-20" />
        <div className="card" style={{borderTop: "3px solid var(--heart)"}}>
          <div className="h3" style={{color: "var(--heart)"}}>{Tt(sd.triadPriority.ttl, lang)}</div>
          <p className="body">{Tt(sd.triadPriority.intro, lang)}</p>
          <table className="t">
            <thead><tr>{sd.triadPriority.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {sd.triadPriority.rows.map(([pri, action, why], i) => (
                <tr key={i}>
                  <td className="num-cell"><strong>{pri}</strong></td>
                  <td><strong>{Tt(action, lang)}</strong></td>
                  <td style={{fontSize: 12, lineHeight: 1.5}}>{Tt(why, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}

      {sd && sd.osaCardiacMap && (<>
        <div className="spacer-20" />
        <div className="card" style={{borderTop: "3px solid var(--heart)"}}>
          <div className="h3" style={{color: "var(--heart)"}}>{Tt(sd.osaCardiacMap.ttl, lang)}</div>
          <p className="body">{Tt(sd.osaCardiacMap.intro, lang)}</p>
          <table className="t">
            <thead><tr>{sd.osaCardiacMap.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {sd.osaCardiacMap.rows.map(([finding, mech, lit, share], i) => (
                <tr key={i}>
                  <td><strong>{Tt(finding, lang)}</strong></td>
                  <td style={{fontSize: 12, lineHeight: 1.5}}>{Tt(mech, lang)}</td>
                  <td style={{fontSize: 11, color: "var(--tl)"}}>{lit}</td>
                  <td style={{fontSize: 12}}>{Tt(share, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Implication: " : "意義："}</strong>{Tt(sd.osaCardiacMap.implication, lang)}
          </div>
        </div>
      </>)}

      {sd && sd.osaReversibility && (<>
        <div className="spacer-20" />
        <div className="card" style={{borderTop: "3px solid var(--heart)"}}>
          <div className="h3" style={{color: "var(--heart)"}}>{Tt(sd.osaReversibility.ttl, lang)}</div>
          <p className="body">{Tt(sd.osaReversibility.intro, lang)}</p>
          <table className="t">
            <thead><tr>{sd.osaReversibility.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {sd.osaReversibility.rows.map(([marker, change, time, lit], i) => (
                <tr key={i}>
                  <td><strong>{Tt(marker, lang)}</strong></td>
                  <td>{Tt(change, lang)}</td>
                  <td style={{fontSize: 12}}>{Tt(time, lang)}</td>
                  <td style={{fontSize: 11, color: "var(--tl)"}}>{lit}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {sd.osaReversibility.irreversible && (
            <div style={{marginTop: 16}}>
              <div className="h4" style={{fontSize: 14, marginBottom: 8}}>{Tt(sd.osaReversibility.irreversible.ttl, lang)}</div>
              <div className="grid-2">
                {sd.osaReversibility.irreversible.items.map((item, i) => (
                  <div key={i} className="callout warn" style={{padding: 14}}>
                    <div style={{fontWeight: 600, fontSize: 13, marginBottom: 4}}>{Tt(item.head, lang)}</div>
                    <div style={{fontSize: 12, lineHeight: 1.55}}>{Tt(item.body, lang)}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {sd.osaReversibility.riskComparison && (
            <div style={{marginTop: 16}}>
              <div className="h4" style={{fontSize: 14, marginBottom: 8}}>{Tt(sd.osaReversibility.riskComparison.ttl, lang)}</div>
              <table className="t">
                <thead><tr>{sd.osaReversibility.riskComparison.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
                <tbody>
                  {sd.osaReversibility.riskComparison.rows.map(([scenario, risk], i) => (
                    <tr key={i}>
                      <td><strong>{Tt(scenario, lang)}</strong></td>
                      <td className="num-cell">{risk}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="callout" style={{marginTop: 8}}>
                <strong>{lang === "en" ? "Takeaway: " : "結論："}</strong>{Tt(sd.osaReversibility.riskComparison.takeaway, lang)}
              </div>
            </div>
          )}
        </div>
      </>)}

      {sd && sd.uricAcidEtiology && (<>
        <div className="spacer-20" />
        <div className="card" style={{borderTop: "3px solid var(--uric)"}}>
          <div className="h3" style={{color: "var(--uric)"}}>{Tt(sd.uricAcidEtiology.ttl, lang)}</div>
          <p className="body">{Tt(sd.uricAcidEtiology.intro, lang)}</p>
          <table className="t">
            <thead><tr>{sd.uricAcidEtiology.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {sd.uricAcidEtiology.rows.map(([phase, age, exp, eff], i) => (
                <tr key={i}>
                  <td><strong>{Tt(phase, lang)}</strong></td>
                  <td className="num-cell">{age}</td>
                  <td style={{fontSize: 12}}>{Tt(exp, lang)}</td>
                  <td style={{fontSize: 12}}>{Tt(eff, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Reframed implication: " : "重新框架後的意義："}</strong>{Tt(sd.uricAcidEtiology.implication, lang)}
          </div>
        </div>
      </>)}

      {sd && sd.uricAcidProtocol && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(sd.uricAcidProtocol.ttl, lang)}</div>
          <p className="body">{Tt(sd.uricAcidProtocol.intro, lang)}</p>
          <table className="t">
            <thead><tr>{sd.uricAcidProtocol.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {sd.uricAcidProtocol.rows.map(([action, ev, eff, note], i) => (
                <tr key={i}>
                  <td><strong>{Tt(action, lang)}</strong></td>
                  <td style={{fontSize: 12}}>{typeof ev === "string" ? ev : Tt(ev, lang)}</td>
                  <td style={{fontSize: 12}}>{Tt(eff, lang)}</td>
                  <td style={{fontSize: 12}}>{Tt(note, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="callout warn" style={{marginTop: 8}}>
            <strong>{lang === "en" ? "Ceiling note: " : "天花板提醒："}</strong>{Tt(sd.uricAcidProtocol.ceiling, lang)}
          </div>
        </div>
      </>)}

      {sd && sd.liver && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(sd.liver.ttl, lang)}</div>
          <p className="body">{Tt(sd.liver.body, lang)}</p>
          <table className="t">
            <thead><tr>{sd.liver.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {sd.liver.rows.map(([m, m0, m3, m6], i) => (
                <tr key={i}>
                  <td><strong>{typeof m === "string" ? m : Tt(m, lang)}</strong></td>
                  <td>{typeof m0 === "string" ? m0 : Tt(m0, lang)}</td>
                  <td>{typeof m3 === "string" ? m3 : Tt(m3, lang)}</td>
                  <td className="num-cell">{typeof m6 === "string" ? m6 : Tt(m6, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}

      {sd && sd.medicalVisits && (<>
        <div className="spacer-20" />
        <div className="card">
          <div className="h3">{Tt(sd.medicalVisits.ttl, lang)}</div>
          <table className="t">
            <thead><tr>{sd.medicalVisits.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>
              {sd.medicalVisits.rows.map(([p, w, when], i) => (
                <tr key={i}>
                  <td><strong>{Tt(p, lang)}</strong></td>
                  <td>{Tt(w, lang)}</td>
                  <td>{typeof when === "string" ? when : Tt(when, lang)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>)}

      {sd && sd.warningSigns && (<>
        <div className="spacer-20" />
        <div className="grid-2">
          <div className="callout bad" style={{padding: 18}}>
            <div style={{fontWeight: 600, fontSize: 15, marginBottom: 6}}>{Tt(sd.warningSigns.immediate.ttl, lang)}</div>
            <ul style={{paddingLeft: 18, margin: 0, fontSize: 13, lineHeight: 1.55}}>
              {sd.warningSigns.immediate.items[lang].map((it, i) => <li key={i} style={{marginBottom: 4}}>{it}</li>)}
            </ul>
          </div>
          <div className="callout warn" style={{padding: 18}}>
            <div style={{fontWeight: 600, fontSize: 15, marginBottom: 6}}>{Tt(sd.warningSigns.soon.ttl, lang)}</div>
            <ul style={{paddingLeft: 18, margin: 0, fontSize: 13, lineHeight: 1.55}}>
              {sd.warningSigns.soon.items[lang].map((it, i) => <li key={i} style={{marginBottom: 4}}>{it}</li>)}
            </ul>
          </div>
        </div>
      </>)}

      {sd && sd.exerciseSafety && (<>
        <div className="spacer-20" />
        <div className="grid-2">
          <div className="callout bad" style={{padding: 18}}>
            <div style={{fontWeight: 600, fontSize: 15, marginBottom: 6}}>{Tt(sd.exerciseSafety.wallSit.ttl, lang)}</div>
            <div style={{fontSize: 13, lineHeight: 1.55}}>{Tt(sd.exerciseSafety.wallSit.body, lang)}</div>
          </div>
          <div className="callout warn" style={{padding: 18}}>
            <div style={{fontWeight: 600, fontSize: 15, marginBottom: 6}}>{Tt(sd.exerciseSafety.ua.ttl, lang)}</div>
            <div style={{fontSize: 13, lineHeight: 1.55}}>{Tt(sd.exerciseSafety.ua.body, lang)}</div>
          </div>
        </div>
      </>)}
    </div>
  );
}

/* ===== Dashboard ===== */
function PanelDashboard({ lang }) {
  const d = DD.dashboard;
  return (
    <div className="section">
      <div className="kicker">{lang === "en" ? "Auto-generated · matplotlib" : "自動生成 · matplotlib"}</div>
      <h2 className="section-title">{Tt(d.ttl, lang)}</h2>
      <p className="section-sub">{Tt(d.sub, lang)}</p>

      <div className="card" style={{padding: 12}}>
        <img
          src={d.src}
          alt={lang === "en" ? "Health Dashboard" : "健康儀表板"}
          style={{width: "100%", height: "auto", borderRadius: "var(--radius-sm)", display: "block"}}
          onError={(e) => { if (e.target.src !== d.fallback) e.target.src = d.fallback; }}
        />
        <div style={{fontSize: 11, color: "var(--ink-3)", marginTop: 8, fontFamily: "var(--font-mono)", textAlign: "right"}}>
          {lang === "en" ? "Source: " : "來源："}<code>{d.src}</code>
        </div>
      </div>

      <div className="spacer-20" />
      <div className="card" style={{padding: 12}}>
        <div className="h3" style={{marginBottom: 8}}>{lang === "en" ? "SpO2 nightly trend" : "SpO2 每晚趨勢"}</div>
        <img
          src={d.spo2Src}
          alt={lang === "en" ? "SpO2 desat trend" : "SpO2 desat 趨勢"}
          style={{width: "100%", height: "auto", borderRadius: "var(--radius-sm)", display: "block"}}
          onError={(e) => { if (e.target.src !== d.spo2Fallback) e.target.src = d.spo2Fallback; }}
        />
        <div style={{fontSize: 11, color: "var(--ink-3)", marginTop: 8, fontFamily: "var(--font-mono)", textAlign: "right"}}>
          {lang === "en" ? "Source: " : "來源："}<code>{d.spo2Src}</code>
        </div>
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

      {r.uphillWalk && (
        <>
          <div className="spacer-20" />
          <div className="card">
            <div className="kicker" style={{marginBottom: 4}}>{lang === "en" ? "Filed 2026-05-22 · Z2 toolkit add-on" : "2026-05-22 新增 · Z2 工具補完"}</div>
            <div className="h3">{Tt(r.uphillWalk.ttl, lang)}</div>
            <p className="body" style={{margin:"6px 0 14px", fontSize: 13, color: "var(--ink-3)"}}>
              {Tt(r.uphillWalk.intro, lang)}
            </p>

            <div className="h3" style={{fontSize: 14, marginTop: 6}}>{Tt(r.uphillWalk.prescription.ttl, lang)}</div>
            <table className="t" style={{marginTop: 6}}>
              <thead><tr>{r.uphillWalk.prescription.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.uphillWalk.prescription.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{row[0]}</strong></td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td style={{fontFamily:"var(--font-mono)"}}>{row[3]}</td>
                    <td style={{color:"var(--ink-3)", fontSize: 12}}>{Tt(row[4], lang)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="body" style={{margin:"10px 0 0", fontSize: 12, color: "var(--ink-3)", fontStyle: "italic"}}>
              {Tt(r.uphillWalk.prescription.anchor, lang)}
            </p>

            <div className="h3" style={{fontSize: 14, marginTop: 18}}>{Tt(r.uphillWalk.tools.ttl, lang)}</div>
            <table className="t" style={{marginTop: 6}}>
              <thead><tr>{r.uphillWalk.tools.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.uphillWalk.tools.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{Tt(row[0], lang)}</strong></td>
                    <td>{Tt(row[1], lang)}</td>
                    <td>{Tt(row[2], lang)}</td>
                    <td style={{color:"var(--ink-3)", fontSize: 12}}>{Tt(row[3], lang)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="h3" style={{fontSize: 14, marginTop: 18}}>{Tt(r.uphillWalk.weekly.ttl, lang)}</div>
            <table className="t" style={{marginTop: 6}}>
              <thead><tr>{r.uphillWalk.weekly.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.uphillWalk.weekly.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{Tt(row[0], lang)}</strong></td>
                    <td>{Tt(row[1], lang)}</td>
                    <td style={{fontFamily:"var(--font-mono)", color: "var(--heart)"}}>{row[2]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="body" style={{margin:"10px 0 0", fontSize: 12, color: "var(--ink-3)", fontStyle: "italic"}}>
              {Tt(r.uphillWalk.weekly.note, lang)}
            </p>

            <div className="h3" style={{fontSize: 14, marginTop: 18}}>{Tt(r.uphillWalk.ramp.ttl, lang)}</div>
            <table className="t" style={{marginTop: 6}}>
              <thead><tr>{r.uphillWalk.ramp.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.uphillWalk.ramp.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{Tt(row[0], lang)}</strong></td>
                    <td>{Tt(row[1], lang)}</td>
                    <td style={{fontFamily:"var(--font-mono)"}}>{row[2]}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="h3" style={{fontSize: 14, marginTop: 18, color: "var(--heart)"}}>{Tt(r.uphillWalk.safety.ttl, lang)}</div>
            <ul className="body" style={{paddingLeft: 18, margin: "8px 0 0"}}>
              {r.uphillWalk.safety.items[lang].map((it, i) => <li key={i} style={{marginBottom: 6, fontSize: 13}}>{it}</li>)}
            </ul>

            <p className="body" style={{margin:"14px 0 0", fontSize: 11, color: "var(--ink-3)", fontFamily: "var(--font-mono)"}}>
              {Tt(r.uphillWalk.ref, lang)}
            </p>
          </div>
        </>
      )}

      {r.hipDrive && (
        <>
          <div className="spacer-20" />
          <div className="card">
            <div className="h3">{Tt(r.hipDrive.ttl, lang)}</div>
            <p className="body" style={{margin:"6px 0 14px", fontSize: 13, color: "var(--ink-3)"}}>
              {Tt(r.hipDrive.intro, lang)}
            </p>

            <div className="h3" style={{fontSize: 14, marginTop: 6}}>{Tt(r.hipDrive.threeSteps.ttl, lang)}</div>
            <table className="t" style={{marginTop: 6}}>
              <thead><tr>{r.hipDrive.threeSteps.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.hipDrive.threeSteps.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{Tt(row[0], lang)}</strong></td>
                    <td>{Tt(row[1], lang)}</td>
                    <td style={{color:"var(--ink-3)", fontSize: 12}}>{Tt(row[2], lang)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="h3" style={{fontSize: 14, marginTop: 18}}>{Tt(r.hipDrive.drills.ttl, lang)}</div>
            <table className="t" style={{marginTop: 6}}>
              <thead><tr>{r.hipDrive.drills.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.hipDrive.drills.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{Tt(row[0], lang)}</strong></td>
                    <td>{Tt(row[1], lang)}</td>
                    <td>{Tt(row[2], lang)}</td>
                    <td style={{color:"var(--ink-3)", fontSize: 12}}>{Tt(row[3], lang)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="body" style={{margin:"10px 0 0", fontSize: 12, color: "var(--ink-3)", fontStyle: "italic"}}>
              {Tt(r.hipDrive.drills.note, lang)}
            </p>

            <div className="h3" style={{fontSize: 14, marginTop: 18}}>{Tt(r.hipDrive.diagnose.ttl, lang)}</div>
            <table className="t" style={{marginTop: 6}}>
              <thead><tr>{r.hipDrive.diagnose.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.hipDrive.diagnose.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{Tt(row[0], lang)}</strong></td>
                    <td>{Tt(row[1], lang)}</td>
                    <td style={{color:"var(--ink-3)", fontSize: 12}}>{Tt(row[2], lang)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="h3" style={{fontSize: 14, marginTop: 18}}>{Tt(r.hipDrive.shoes.ttl, lang)}</div>
            <p className="body" style={{margin:"6px 0 10px", fontSize: 13}}>
              {Tt(r.hipDrive.shoes.body, lang)}
            </p>
            <table className="t">
              <thead><tr>{r.hipDrive.shoes.fit.head[lang].map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>
                {r.hipDrive.shoes.fit.rows.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{Tt(row[0], lang)}</strong></td>
                    <td>{Tt(row[1], lang)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="body" style={{margin:"10px 0 0", fontSize: 12, color: "var(--ink-3)", fontStyle: "italic"}}>
              {Tt(r.hipDrive.shoes.pair, lang)}
            </p>
          </div>
        </>
      )}
    </div>
  );
}

Object.assign(window, {
  PanelOverview, PanelSleep, PanelDiet, PanelExercise, PanelRunning,
  PanelSupps, PanelRoutine, PanelTimeline, PanelSafety, PanelDashboard, PanelTracker,
});
