document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map
    var map = L.map('map').setView([49.505, -120], 13);

    // Add a tile layer (in this case, OpenStreetMap)
    var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    });

    var satelliteLayer = L.tileLayer("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", {
        maxZoom: 19,
    }).addTo(map);

    var railLayer = L.tileLayer("http://a.tiles.openrailwaymap.org/maxspeed/{z}/{x}/{y}.png", {
        maxZoom: 19,
    }).addTo(map);

    var railLayer = L.tileLayer("http://a.tiles.openrailwaymap.org/maxspeed/{z}/{x}/{y}.png", {
        maxZoom: 19,
    }).addTo(map);

    var railLayer = L.tileLayer("http://a.tiles.openrailwaymap.org/maxspeed/{z}/{x}/{y}.png", {
        maxZoom: 19,
    }).addTo(map);

    var railLayer = L.tileLayer("http://a.tiles.openrailwaymap.org/maxspeed/{z}/{x}/{y}.png", {
        maxZoom: 19,
    }).addTo(map);
    // Add a marker
    var marker = L.marker([49.505, -120]).addTo(map);
    marker.bindPopup("<b>Hello World!</b><br>I am a popup.").openPopup();

    // Function to toggle rail layer
    function toggleRailLayer() {
        if (map.hasLayer(railLayer)) {
            map.removeLayer(railLayer);
        } else {
            map.addLayer(railLayer);
        }
    }

    function toggleSatelliteLayer() {
        if (map.hasLayer(satelliteLayer)){
            map.addLayer(osmLayer);
            map.removeLayer(satelliteLayer);
        } else {
            map.addLayer(satelliteLayer);
            map.removeLayer(osmLayer);
        }
        if (map.hasLayer(railLayer)) {
            map.removeLayer(railLayer);
            map.addLayer(railLayer)
        }
    }
    // Event listener for button click
    document.getElementById('toggleSatelliteLayer').addEventListener("click", toggleSatelliteLayer)
    document.getElementById('toggleRailLayer').addEventListener('click', toggleRailLayer);
    

});
