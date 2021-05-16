$(function() {
    var map = L.map('map').setView([40.712, -74.006], 11);

    for(city_id in data) {
        city = data[city_id]
        text = "<center>" + city.tweets.length + " tweets à " + city.display_name + "<br>"

        city.tweets.forEach(tweet => {
            text += `- <a target='_blank' href=https://twitter.com/user/status/${tweet[0]}>Lien</a><br>`
        })

        text += "</center>"

        L.marker([city.lat, city.lon]).addTo(map)
            .bindPopup(text).openPopup();

        city.polygon = JSON.parse(city.polygon)

        for (i in city.polygon[0]) {
            city.polygon[0][i] = city.polygon[0][i].reverse()
        }

        L.multiPolyline(city.polygon , {color:'red', fill: true, weight:4}).addTo(map)
    };

    var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    
    map.addLayer(layer);
});