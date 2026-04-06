self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('hangarin-cache-v1').then(function(cache) {
            return cache.addAll([
                '/static/css/hangarin.css',
                '/static/img/icon-192.png',
                '/static/img/icon-512.png'
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});