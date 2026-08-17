'use strict';

const VERSION = 'brother-apeh-planner-v3.5.0';
const APP_CACHE = `${VERSION}-app`;
const RUNTIME_CACHE = `${VERSION}-runtime`;
const PRECACHE = [
  './',
  './index.html',
  './offline.html',
  './manifest.webmanifest',
  './assets/icons/icon-32.png',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png',
  './assets/icons/icon-maskable-192.png',
  './assets/icons/icon-maskable-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(APP_CACHE)
      .then(cache => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => ![APP_CACHE, RUNTIME_CACHE].includes(key)).map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', event => {
  if (event.data?.type === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // Navigation: fresh page when online, cached app/offline page otherwise.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          const copy = response.clone();
          caches.open(APP_CACHE).then(cache => cache.put('./index.html', copy));
          return response;
        })
        .catch(async () => (await caches.match('./index.html')) || caches.match('./offline.html'))
    );
    return;
  }

  // Same-origin static assets: cache first, refresh in background.
  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(request).then(cached => {
        const network = fetch(request)
          .then(response => {
            if (response.ok) caches.open(RUNTIME_CACHE).then(cache => cache.put(request, response.clone()));
            return response;
          })
          .catch(() => cached);
        return cached || network;
      })
    );
    return;
  }

  // Approved CDN assets: cache successful/opaque responses for offline reuse.
  if (['cdn.jsdelivr.net', 'cdnjs.cloudflare.com'].includes(url.hostname)) {
    event.respondWith(
      caches.match(request).then(cached => cached || fetch(request).then(response => {
        if (response.ok || response.type === 'opaque') {
          caches.open(RUNTIME_CACHE).then(cache => cache.put(request, response.clone()));
        }
        return response;
      }))
    );
  }
});
