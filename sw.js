// Bice Workbench Service Worker v10
const CACHE_NAME = 'bice-wb-v10';
const SW_VERSION = '10';
const ASSETS = [
  './',
  './index.html',
  './osta.js',
  './manifest.json',
  './version.json',
  './icon-192.png',
  './icon-512.png'
];

// ============ INSTALL: cache core assets, skip waiting ============
self.addEventListener('install', function(event) {
  console.log('[SW v10] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(ASSETS).catch(function(err) {
        console.warn('[SW v10] Some assets failed to pre-cache:', err);
      });
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

// ============ ACTIVATE: purge ALL old caches, claim clients ============
self.addEventListener('activate', function(event) {
  console.log('[SW v10] Activating — purging all old caches...');
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.map(function(k) {
          if (k !== CACHE_NAME) {
            console.log('[SW v10] Deleting cache:', k);
            return caches.delete(k);
          }
        })
      );
    }).then(function() {
      return self.clients.claim();
    }).then(function() {
      return self.clients.matchAll().then(function(clients) {
        clients.forEach(function(client) {
          client.postMessage({ type: 'sw-updated', version: 'v10' });
        });
      });
    })
  );
});

// ============ FETCH: network-first for ALL requests ============
// This guarantees users always see the latest deployed content.
// Cache is used as offline fallback only.
self.addEventListener('fetch', function(event) {
  if (event.request.method !== 'GET') return;

  // sw.js itself: NEVER cache, always fetch from network
  if (event.request.url.indexOf('sw.js') !== -1) {
    event.respondWith(fetch(event.request));
    return;
  }

  // version.json: NEVER cache, always fetch from network
  if (event.request.url.indexOf('version.json') !== -1) {
    event.respondWith(fetch(event.request));
    return;
  }

  // Everything else: network-first, cache as fallback
  event.respondWith(
    fetch(event.request).then(function(response) {
      // Cache successful responses
      if (response.status === 200 && response.type === 'basic') {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(event.request, clone);
        });
      }
      return response;
    }).catch(function() {
      // Network failed — serve from cache if available
      return caches.match(event.request);
    })
  );
});

// ============ MESSAGE: version responses ============
self.addEventListener('message', function(event) {
  if (event.data && event.data.type === 'get-version') {
    if (event.source) {
      event.source.postMessage({
        type: 'version-response',
        version: SW_VERSION
      });
    }
  }
  if (event.data && event.data.type === 'skip-waiting') {
    self.skipWaiting();
  }
});
