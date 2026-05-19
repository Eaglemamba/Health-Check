const VERSION = 'v18-2026-05-19-csp-fix';
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

// data.js 採 stale-while-revalidate：先回 cache 立即顯示，背景刷新；下次開啟即見最新值
// 其餘資源仍 cache-first（純靜態 / CDN）
const SWR_PATHS = [/\/data\.js(\?.*)?$/];

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isCDN = /unpkg\.com|fonts\.googleapis\.com|fonts\.gstatic\.com/.test(url.host);
  const isSameOrigin = url.origin === self.location.origin;
  if (!isCDN && !isSameOrigin) return;

  const isSWR = isSameOrigin && SWR_PATHS.some((re) => re.test(url.pathname));

  if (isSWR) {
    e.respondWith(
      caches.match(req).then((hit) => {
        const fresh = fetch(req).then((res) => {
          if (res && res.status === 200) {
            const clone = res.clone();
            caches.open('hc-runtime-' + VERSION).then((c) => c.put(req, clone));
          }
          return res;
        }).catch(() => hit);
        return hit || fresh;
      })
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
