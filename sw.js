// MALAGASY.MG - Service Worker (Fitehirizana ho an'ny Mode Hors-ligne)
const CACHE_NAME = 'malagasy-mg-v1';

// Ireo rakitra fototra tehirizina ao anaty finday
const RAKITRA_HOTEHIRIZINA = [
  './',
  './index.html',
  './profil.html',
  './ampitahao.html',
  './fanabeazana.html',
  './manifest.json',
  './data_taloha.js',
  './data_vaovao.js',
  './data_bennytanana.js',
  './data_solombavambahoaka.js'
];

// Fametrahana sy fitehirizana voalohany (Install)
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('✅ Voatahiry ao anaty fitadidian\'ny finday ny pejy rehetra!');
      return cache.addAll(RAKITRA_HOTEHIRIZINA);
    })
  );
  self.skipWaiting();
});

// Fanavaozana ny cache (Activate)
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Famakiana ny pejy na dia tapaka aza ny aterineto (Fetch)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((valinyVoatahiry) => {
      // Raha efa voatahiry ao anaty finday dia iny no avoaka avy hatrany
      if (valinyVoatahiry) {
        return valinyVoatahiry;
      }
      // Raha tsy ao dia alaina amin'ny aterineto
      return fetch(event.request).catch(() => {
        // Raha sendra tapaka ny aterineto ka pejy html no tadiavina
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('./index.html');
        }
      });
    })
  );
});