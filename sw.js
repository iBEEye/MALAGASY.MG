// MALAGASY.MG - Service Worker (Fitehirizana ho an'ny Mode Hors-ligne)
const CACHE_NAME = 'malagasy-mg-v2';

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

// VAHAOLANA MAHARITRA: Aterineto aloha (Network-First) vao Fitadidiana (Cache)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then((valinyVaovao) => {
        // Raha misy internet: avoaka avy hatrany ny vaovao farany sady havaozina mangina ny fitadidiana
        if (valinyVaovao && valinyVaovao.status === 200) {
          const dikaVaovao = valinyVaovao.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, dikaVaovao);
          });
        }
        return valinyVaovao;
      })
      .catch(() => {
        // Raha tapaka tanteraka ny internet: eo vao alaina ao amin'ny fitadidiana (Mode Hors-ligne)
        return caches.match(event.request).then((valinyVoatahiry) => {
          if (valinyVoatahiry) {
            return valinyVoatahiry;
          }
          if (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) {
            return caches.match('./index.html');
          }
        });
      })
  );
});