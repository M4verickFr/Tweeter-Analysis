$(async function() {
    var map = L.map('map').setView([40.712, -74.006], 11);

    map.addLayer(L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }));

    $( "#reload-btn" ).click(function() {
        alert( "Reoload tweet and Add point" );
        // let response = await axios.get(`http://localhost:5000/streaming_tweets`)
        // console.log(response.data.map(e => {return e.coordinates}))
    });
});