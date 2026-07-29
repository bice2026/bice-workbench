// Bice Workbench Service Worker v11
const CACHE_NAME = 'bice-wb-v11';
const SW_VERSION = '11';
const ASSETS = [
  './',
  './index.html',
  './osta.js',
  './manifest.json',
  './version.json',
  './icon-192.png',
  './icon-512.png'
];

// ============ INSTALL: pre-cache assets, skip waiting ============
self.addEventListener('install', function(event) {
  console.log('[SW v11] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(ASSETS).catch(function(err) {
        console.warn('[SW v11] Some assets failed to pre-cache:', err);
      });
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

// ============ ACTIVATE: purge ALL old caches, claim all clients ============
self.addEventListener('activate', function(event) {
  console.log('[SW v11] Activating — removing all non-v11 caches...');
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.map(function(k) {
          console.log('[SW v11] Deleting old cache:', k);
          return caches.delete(k);
        })
      );
    }).then(function() {
      return self.clients.claim();
    }).then(function() {
      return self.clients.matchAll().then(function(clients) {
        clients.forEach(function(client) {
          client.postMessage({ type: 'sw-updated', version: 'v11' });
        });
      });
    })
  );
});

// ============ FETCH: network-first for ALL, cache as fallback ============
self.addEventListener('fetch', function(event) {
  if (event.request.method !== 'GET') return;

  var url = event.request.url;

  // Core files NEVER served from cache — force network always
  if (url.indexOf('sw.js') !== -1 || url.indexOf('version.json') !== -1) {
    event.respondWith(fetch(event.request));
    return;
  }

  // Everything else: network-first, cache fallback
  event.respondWith(
    fetch(event.request).then(function(response) {
      if (response.status === 200 && response.type === 'basic') {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(event.request, clone);
        });
      }
      return response;
    }).catch(function() {
      return caches.match(event.request);
    })
  );
});

// ============ MESSAGE handlers ============
self.addEventListener('message', function(event) {
  if (event.data && event.data.type === 'get-version') {
    if (event.source) {
      event.source.postMessage({ type: 'version-response', version: SW_VERSION });
    }
  }
  if (event.data && event.data.type === 'skip-waiting') {
    self.skipWaiting();
  }
  if (event.data && event.data.type === 'clear-all') {
    event.waitUntil(
      caches.keys().then(function(keys) {
        return Promise.all(keys.map(function(k) { return caches.delete(k); }));
      }).then(function() {
        if (event.source) {
          event.source.postMessage({ type: 'cleared' });
        }
      })
    );
  }
});
