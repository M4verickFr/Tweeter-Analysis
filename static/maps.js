$(function() {
    var map = L.map('map').setView([40.712, -74.006], 11);

    tweets.forEach(tweet => {
        L.marker([tweet[1], tweet[2]]).addTo(map)
            .bindPopup(`<strong>${tweet[3]} <a target='_blank' href=https://twitter.com/user/status/${tweet[0]}>Lien</a></strong>`).openPopup();
    });

    var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    
    map.addLayer(layer);
});