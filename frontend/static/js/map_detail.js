
(function(){
  const lat = window.__LAT;
  const lon = window.__LON;
  const map = L.map('mapDetail');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: '&copy; OpenStreetMap'}).addTo(map);
  if (lat !== null && lon !== null){
    map.setView([lat, lon], 15);
    L.marker([lat, lon]).addTo(map);
  } else {
    map.setView([-22.0, -43.0], 6);
  }
})();
