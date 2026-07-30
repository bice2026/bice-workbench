// Bice Workbench Service Worker v17
// Strategy: NO CACHING — always network-first, cache only as fallback
// Old caches (v8-v16) deleted on activate
const CACHE_NAME = 'bice-wb-v17';
const SW_VERSION = '17';

// Skip waiting: new SW takes control immediately
self.addEventListener('install', function(event) {
  console.log('[SW v17] Installing — skipWaiting enabled');
  self.skipWaiting();
});

// Activate: DELETE ALL OLD CACHES unconditionally
self.addEventListener('activate', function(event) {
  console.log('[SW v17] Activating — clearing all legacy caches');
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.map(function(k) {
          console.log('[SW v17] Deleting old cache:', k);
          return caches.delete(k);
        })
      );
    }).then(function() {
      // Take control of all clients immediately
      return self.clients.claim();
    }).then(function() {
      // Notify all clients
      return self.clients.matchAll().then(function(clients) {
        clients.forEach(function(client) {
          client.postMessage({ type: 'sw-updated', version: 'v17' });
        });
      });
    })
  );
});

// Runtime: network-first for everything, cache as fallback only
self.addEventListener('fetch', function(event) {
  // Only handle GET
  if (event.request.method !== 'GET') return;

  // Skip non-HTTP(S)
  var url = new URL(event.request.url);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  event.respondWith(
    fetch(event.request, { cache: 'no-store' }).then(function(response) {
      // Cache successful responses for offline fallback
      if (response.ok) {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(event.request, clone);
        });
      }
      return response;
    }).catch(function() {
      // Network failed — try cache fallback
      return caches.match(event.request).then(function(cached) {
        return cached || new Response('Offline — please connect to the internet.', {
          status: 503,
          statusText: 'Service Unavailable'
        });
      });
    })
  );
});
