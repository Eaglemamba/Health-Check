/* ============ Health Reversal Plan — components ============ */
const { useState, useEffect, useMemo, useRef } = React;

const D = window.HC_DATA;

const t = (obj, lang) => {
  if (!obj) return "";
  if (typeof obj === "string") return obj;
  return obj[lang] ?? obj.en ?? "";
};

/* ===== Icons ===== */
const Icon = ({ name, size = 16 }) => {
  const stroke = "currentColor";
  const sw = 1.8;
  const common = { width: size, height: size, viewBox: "0 0 24 24", fill: "none", stroke, strokeWidth: sw, strokeLinecap: "round", strokeLinejoin: "round" };
  switch (name) {
    case "heart": return <svg {...common}><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 1 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>;
    case "moon": return <svg {...common}><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>;
    case "scale": return <svg {...common}><circle cx="12" cy="12" r="9"/><path d="M12 3v3M9 12h6"/></svg>;
    case "drop": return <svg {...common}><path d="M12 2.5s6 7 6 11.5a6 6 0 0 1-12 0c0-4.5 6-11.5 6-11.5z"/></svg>;
    case "sparkle": return <svg {...common}><path d="M12 3l1.6 4.7L18 9l-4.4 1.3L12 15l-1.6-4.7L6 9l4.4-1.3z"/></svg>;
    case "leaf": return <svg {...common}><path d="M5 21c8 0 14-6 14-14V3h-4C7 3 3 9 3 17v4z"/><path d="M5 21l9-9"/></svg>;
    case "activity": return <svg {...common}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>;
    case "clock": return <svg {...common}><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/></svg>;
    case "shield": return <svg {...common}><path d="M12 2l8 4v6c0 5-4 9-8 10-4-1-8-5-8-10V6z"/></svg>;
    case "calendar": return <svg {...common}><rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/></svg>;
    case "list": return <svg {...common}><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>;
    default: return null;
  }
};

const tabIcons = {
  overview: "sparkle", sleep: "moon", diet: "leaf", exercise: "activity",
  supps: "drop", routine: "clock", timeline: "calendar", safety: "shield", tracker: "list",
};

const sysIcons = { heart: "heart", sleep: "moon", weight: "scale", uric: "sparkle", remnant: "drop", tghdl: "activity" };

/* ===== Hero ===== */
function Hero({ lang, variant }) {
  const h = D.hero;
  const titleParts = h.title[lang];
  return (
    <div className="hero">
      <OsaAlert lang={lang} />
      <div className="hero-top">
        <div>
          <div className="hero-eyebrow">{t(h.eyebrow, lang)}</div>
          {variant === "snapshot" ? (
            <h2>
              {lang === "en" ? <>Today's snapshot — <em>four systems, one root.</em></> : <>今日總覽 — <em>四系統、單一根源。</em></>}
            </h2>
          ) : variant === "today" ? (
            <h2>
              {lang === "en" ? <>What you're doing <em>today.</em></> : <>今天該做的 <em>事項</em>。</>}
            </h2>
          ) : (
            <h2>
              {titleParts[0]} <em>{titleParts[1]}</em> {titleParts[2]}
            </h2>
          )}
          <p className="hero-lede">{t(h.lede, lang)}</p>
        </div>
        <HeroProgress lang={lang} />
      </div>
      <div className="marker-grid">
        {D.markers.map((m, i) => (
          <Marker key={i} m={m} lang={lang} />
        ))}
      </div>
    </div>
  );
}

/* ===== OSA red-flag banner ===== */
function trailingStreakBelow(arr, threshold) {
  if (!Array.isArray(arr)) return 0;
  let n = 0;
  for (let i = arr.length - 1; i >= 0; i--) {
    const v = arr[i];
    if (v == null) break;
    if (v < threshold) n++;
    else break;
  }
  return n;
}

function OsaAlert({ lang }) {
  const cfg = D.osaAlert;
  const nadir = D.tracker?.spo2Nadir;
  const [psgBooked, setPsgBooked] = useState(() => {
    try { return localStorage.getItem("hc_psg_booked") === "1"; } catch { return false; }
  });
  if (!cfg || !nadir) return null;
  if (psgBooked || cfg.psgStatus === "booked" || cfg.psgStatus === "done") return null;
  const streak = trailingStreakBelow(nadir, cfg.threshold);
  if (streak < cfg.minAlert) return null;
  const urgent = streak >= cfg.minUrgent;
  const tmpl = urgent ? cfg.urgent : cfg.body;
  const text = t(tmpl, lang).replace("%N", streak);
  return (
    <div className={"osa-banner" + (urgent ? " urgent" : "")} role="alert">
      <div className="osa-icon" aria-hidden="true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 2l10 18H2L12 2z"/><line x1="12" y1="9" x2="12" y2="14"/><circle cx="12" cy="17" r="0.6" fill="currentColor"/>
        </svg>
      </div>
      <div className="osa-text">
        <div className="osa-title">{t(cfg.title, lang)} · {t(cfg.psgStatusLabel, lang)}: {cfg.psgStatus}</div>
        <div className="osa-body">{text}</div>
      </div>
      <button className="osa-cta" onClick={() => {
        try { localStorage.setItem("hc_psg_booked", "1"); } catch {}
        setPsgBooked(true);
      }}>{t(cfg.cta, lang)}</button>
    </div>
  );
}

function HeroProgress({ lang }) {
  const start = D.hero.startWeight ?? 70;
  const target = D.hero.targetWeight ?? 65;
  const current = D.hero.currentWeight ?? 68.0;
  const pct = Math.min(100, Math.max(0, ((start - current) / (start - target)) * 100));
  const lost = (start - current).toFixed(1);
  const goal = (start - target).toFixed(0);
  const [w, setW] = useState(0);
  useEffect(() => { const t = setTimeout(() => setW(pct), 200); return () => clearTimeout(t); }, [pct]);
  return (
    <div className="hero-progress">
      <div className="lbl">{t(D.hero.progressLbl, lang)}</div>
      <div className="val">
        {current.toFixed(1)}<small>/ {target} kg</small>
      </div>
      <div className="bar"><div className="bar-fill" style={{ width: `${w}%` }} /></div>
      <div className="meta">
        <span>{lang === "en" ? `−${lost} kg / ${goal} kg goal` : `已減 ${lost} / ${goal} 公斤`}</span>
        <span>{t(D.hero.progressMeta, lang)}</span>
      </div>
    </div>
  );
}

function Marker({ m, lang }) {
  return (
    <div className="marker" data-system={m.sys}>
      <div className="head">
        <div className="ico"><Icon name={sysIcons[m.sys]} size={16} /></div>
        {m.cadence && <span className="cadence">{t(m.cadence, lang)}</span>}
      </div>
      <div className="name">{t(m.name, lang)}</div>
      <div className="num">{m.val}<small>{m.unit}</small></div>
      <div className={`delta ${m.status}`}>
        <span className="dot" />
        {t(m.delta, lang)}
      </div>
    </div>
  );
}

/* ===== Tabs ===== */
function Tabs({ active, onChange, lang }) {
  return (
    <div className="tabs-wrap">
      <div className="tabs">
        {D.tabs.map(tab => (
          <button key={tab.id} className={"tab" + (active === tab.id ? " active" : "")} onClick={() => onChange(tab.id)}>
            {t(tab, lang)}
          </button>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { Icon, t, Hero, Tabs, tabIcons, sysIcons });
