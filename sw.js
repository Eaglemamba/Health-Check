const VERSION = 'v27-2026-06-08-weekly-dashboard-panel';
const CORE = './';
const CORE_FILES = [
  './',
  './index.html',
  './data.js',
  './styles.css',
  './components-core.jsx',
  './components-panels.jsx',
  './tweaks-panel.jsx',
  './manifest.webmanifest',
  './icons/apple-touch-icon.svg',
  './icons/icon-192.svg',
  './icons/icon-512.svg',
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('hc-core-' + VERSION).then((c) => c.addAll(CORE_FILES)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => !k.endsWith(VERSION)).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// data.js 採 network-first：線上先抓最新版立即顯示今天的數值，離線才退回 cache。
// 解決 stale-while-revalidate 造成「畫面永遠慢最新一天」的問題（v22 行為）。
// v26：reviews/ 下每日重生成的 PNG（health_dashboard / SpO2 圖）同樣 network-first，
//   解決「健康儀表板永遠顯示前一天」的 cache-first stale 問題。
// 其餘資源仍 cache-first（純靜態 / CDN）
const NETWORK_FIRST_PATHS = [
  /\/data\.js(\?.*)?$/,
  /\/reviews\/.*\.png(\?.*)?$/,
];

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isCDN = /unpkg\.com|fonts\.googleapis\.com|fonts\.gstatic\.com/.test(url.host);
  const isSameOrigin = url.origin === self.location.origin;
  if (!isCDN && !isSameOrigin) return;

  const isNetworkFirst = isSameOrigin && NETWORK_FIRST_PATHS.some((re) => re.test(url.pathname));

  if (isNetworkFirst) {
    e.respondWith(
      fetch(req).then((res) => {
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open('hc-runtime-' + VERSION).then((c) => c.put(req, clone));
        }
        return res;
      }).catch(() => caches.match(req))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then((hit) => {
      if (hit) return hit;
      return fetch(req).then((res) => {
        if (!res || res.status !== 200) return res;
        const clone = res.clone();
        caches.open('hc-runtime-' + VERSION).then((c) => c.put(req, clone));
        return res;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
