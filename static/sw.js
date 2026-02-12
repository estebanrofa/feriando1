const CACHE_NAME = 'feriando-v1';
const STATIC_CACHE = 'feriando-static-v1';
const DYNAMIC_CACHE = 'feriando-dynamic-v1';

// Archivos esenciales para cache inicial
const STATIC_ASSETS = [
    '/',
    '/static/lobby.css',
    '/static/style.css',
    '/static/registro.css',
    '/static/favicon.png',
    '/static/fondo-boton.png',
    '/static/fundador.png',
    '/static/manifest.json'
];

// Instalacion: cachear archivos estaticos
self.addEventListener('install', event => {
    console.log('[SW] Instalando...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('[SW] Cacheando archivos estaticos');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => self.skipWaiting())
    );
});

// Activacion: limpiar caches viejos
self.addEventListener('activate', event => {
    console.log('[SW] Activando...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(name => name !== STATIC_CACHE && name !== DYNAMIC_CACHE)
                    .map(name => {
                        console.log('[SW] Eliminando cache viejo:', name);
                        return caches.delete(name);
                    })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch: estrategia Network First con fallback a cache
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // Solo cachear requests del mismo origen
    if (url.origin !== location.origin) {
        return;
    }

    // Para navegacion (HTML): Network First
    if (request.mode === 'navigate') {
        event.respondWith(
            fetch(request)
                .then(response => {
                    // Cachear respuesta exitosa
                    const responseClone = response.clone();
                    caches.open(DYNAMIC_CACHE).then(cache => {
                        cache.put(request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    // Offline: buscar en cache
                    return caches.match(request)
                        .then(cachedResponse => {
                            if (cachedResponse) {
                                return cachedResponse;
                            }
                            // Fallback a pagina principal
                            return caches.match('/');
                        });
                })
        );
        return;
    }

    // Para assets estaticos: Cache First
    if (request.destination === 'style' ||
        request.destination === 'script' ||
        request.destination === 'image') {
        event.respondWith(
            caches.match(request)
                .then(cachedResponse => {
                    if (cachedResponse) {
                        // Actualizar cache en background
                        fetch(request).then(response => {
                            caches.open(STATIC_CACHE).then(cache => {
                                cache.put(request, response);
                            });
                        });
                        return cachedResponse;
                    }
                    // No en cache: fetch y guardar
                    return fetch(request).then(response => {
                        const responseClone = response.clone();
                        caches.open(STATIC_CACHE).then(cache => {
                            cache.put(request, responseClone);
                        });
                        return response;
                    });
                })
        );
        return;
    }

    // Default: Network with cache fallback
    event.respondWith(
        fetch(request)
            .then(response => {
                const responseClone = response.clone();
                caches.open(DYNAMIC_CACHE).then(cache => {
                    cache.put(request, responseClone);
                });
                return response;
            })
            .catch(() => caches.match(request))
    );
});

// Mensaje para actualizar cache manualmente
self.addEventListener('message', event => {
    if (event.data.action === 'skipWaiting') {
        self.skipWaiting();
    }
});
