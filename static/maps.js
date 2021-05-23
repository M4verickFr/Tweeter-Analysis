$(function() {
    var map = L.map('map').setView([40.712, -74.006], 11);
    map.setView(["46", "2"], 6);

    tweets.forEach(tweet => {
        L.marker([tweet[6], tweet[7]]).addTo(map)
            .bindPopup(`<strong>${tweet[3]} <a target='_blank' href=https://twitter.com/user/status/${tweet[1]}>Lien</a></strong>`);
    });

    var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    
    map.addLayer(layer);
});