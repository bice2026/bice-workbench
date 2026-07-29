// Bice Workbench Service Worker v9
const CACHE_NAME = 'bice-wb-v9';
const DATA_CACHE = 'bice-wb-data-v9';
const ASSETS = [
  './',
  './index.html',
  './osta.js',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

// ============ INSTALL ============
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(ASSETS);
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

// ============ ACTIVATE: clean old caches + notify clients ============
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) {
          return k !== CACHE_NAME && k !== DATA_CACHE;
        }).map(function(k) {
          return caches.delete(k);
        })
      );
    }).then(function() {
      return self.clients.claim();
    }).then(function() {
      // Notify all clients that a new version is available
      return self.clients.matchAll().then(function(clients) {
        clients.forEach(function(client) {
          client.postMessage({ type: 'sw-updated', version: 'v9' });
        });
      });
    })
  );
});

// ============ FETCH: network-first HTML, cache-first assets ============
self.addEventListener('fetch', function(event) {
  if (event.request.method !== 'GET') return;

  // Never cache sw.js itself — always fetch from network
  if (event.request.url.indexOf('sw.js') !== -1) {
    event.respondWith(fetch(event.request));
    return;
  }

  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).then(function(response) {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(event.request, clone);
        });
        return response;
      }).catch(function() {
        return caches.match(event.request);
      })
    );
  } else {
    event.respondWith(
      caches.match(event.request).then(function(cached) {
        return cached || fetch(event.request).then(function(response) {
          // Only cache same-origin assets
          if (response.status === 200) {
            var clone = response.clone();
            caches.open(CACHE_NAME).then(function(cache) {
              cache.put(event.request, clone);
            });
          }
          return response;
        });
      })
    );
  }
});

// ============ MESSAGE: cross-client data sync ============
self.addEventListener('message', function(event) {
  var data = event.data;

  if (data.type === 'sync-data') {
    // Store data snapshot in Data Cache (shared between Safari & PWA on iOS)
    event.waitUntil(
      caches.open(DATA_CACHE).then(function(cache) {
        return cache.put(
          new Request('/__data__/snapshot.json'),
          new Response(JSON.stringify({
            timestamp: Date.now(),
            source: data.source || 'unknown',
            payload: data.payload
          }), {
            headers: { 'Content-Type': 'application/json' }
          })
        );
      }).then(function() {
        // Broadcast to all other clients
        return self.clients.matchAll().then(function(clients) {
          clients.forEach(function(client) {
            if (client.id !== (event.source ? event.source.id : null)) {
              client.postMessage({
                type: 'data-changed',
                timestamp: Date.now()
              });
            }
          });
        });
      })
    );
  }

  if (data.type === 'fetch-data') {
    event.waitUntil(
      caches.open(DATA_CACHE).then(function(cache) {
        return cache.match('/__data__/snapshot.json');
      }).then(function(response) {
        if (response) {
          return response.json().then(function(snapshot) {
            if (event.source) {
              event.source.postMessage({
                type: 'data-response',
                snapshot: snapshot
              });
            }
          });
        } else if (event.source) {
          event.source.postMessage({ type: 'data-response', snapshot: null });
        }
      })
    );
  }

  if (data.type === 'skip-waiting') {
    self.skipWaiting();
  }
});
