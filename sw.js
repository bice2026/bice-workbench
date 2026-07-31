// Bice Workbench Service Worker v22 — Cache-First app shell for instant offline PWA
const CACHE_NAME = 'bice-wb-v22';
const SW_VERSION = '22';

self.addEventListener('install', function(event) {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll([
        './', './index.html', './manifest.json', './sw.js?v=22',
        './icon-192.png', './icon-512.png'
      ]);
attr
    })
  );
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.put('./sw.js', new Response('/* v22 */', { 'Content-Type': 'application/javascript' }));
    })
  );
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.map(function(k) { if (k !== CACHE_NAME) return caches.delete(k); })
      ).then(function() { return self.clients.claim(); });
    })
  );
});

self.addEventListener('fetch', function(event) {
  if (event.request.method !== 'GET') return;
  var url = new URL(event.request.url);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  if (url.origin === location.origin) {
    // App shell: CACHE-FIRST — offline navigation returns instantly (no connect wait)
    event.respondWith(
      caches.match(event.request).then(function(cached) {
        if (cached) return cached;
        return fetch(event.request).then(function(res) {
          if (res.ok) {
            var clone = res.clone();
            caches.open(CACHE_NAME).then(function(cache) { cache.put(event.request, clone); });
          }
          return res;
        }).catch(function() {
          if (event.request.mode === 'navigate') {
            return new Response('离线模式已就绪，请稍候加载', { status: 503, statusText: 'Service Unavailable' });
          }
          return new Response('', { status: 503 });
        });
      })
    );
  } else {
    // Cross-origin (Unsplash / GitHub API): network-first with cache fallback
    event.respondWith(
      fetch(event.request).then(function(res) { return res; }).catch(function() {
        return caches.match(event.request).then(function(c) { return c || new Response('', { status: 503 }); });
      })
    );
  }
});
