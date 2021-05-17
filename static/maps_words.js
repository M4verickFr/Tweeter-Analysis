$(function() {
    var map = L.map('map').setView([40.712, -74.006], 11);
    map.setView(["46", "2"], 6);

    for(city_id in data) {
        city = data[city_id]
        text = "<center>" + city.display_name + "<br><strong>"

        city.words.forEach(word => {
            text += `${word[0]} - `
        })

        text = text.slice(0, -3);
        text += "</strong></center>"

        L.marker([city.lat, city.lon]).addTo(map)
            .bindPopup(text);

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