$(function() {
    var map = L.map('map').setView([40.712, -74.006], 11);

    tweet_with_coordinates.forEach(async tweet => {
        let posResponse = await axios.get(`https://nominatim.openstreetmap.org/reverse?lat=${tweet[1]}&lon=${tweet[2]}&format=json`, {headers: {'Access-Control-Allow-Origin': '*'}})
        let cityResponse = await axios.get(`https://nominatim.openstreetmap.org/search?q=${posResponse.data.address.city}&format=json&limit=1`, {headers: {'Access-Control-Allow-Origin': '*'}})
                
        cityResponse.data = cityResponse.data[0]
        let bounds = [[cityResponse.data.boundingbox[0],cityResponse.data.boundingbox[2]],[cityResponse.data.boundingbox[1],cityResponse.data.boundingbox[3]]];
        console.log("bounds : " + bounds)
        map.addLayer(L.rectangle(bounds, {color: "#ff7800", weight: 1}));

        L.marker([cityResponse.data.lat, cityResponse.data.lon]).addTo(map)
            .bindPopup(`<strong><a target='_blank' href=https://twitter.com/user/status/${tweet[0]}>Tweet</a></strong>`).openPopup();
    });

    var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    
    // Now add the layer onto the map
    map.addLayer(layer);
});