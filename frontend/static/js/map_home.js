
(function(){
  const markers = window.__MARKERS || [];
  const map = L.map('mapHome');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap' }).addTo(map);
  if (markers.length){
    const group = L.featureGroup(markers.map(m => L.marker([m.lat, m.lon]).bindPopup(`#${m.id} - ${m.title}<br><small>${m.category} • ${m.status}</small>`)));
    group.addTo(map);
    map.fitBounds(group.getBounds().pad(0.2));
  } else {
    map.setView([-22.0, -43.0], 6);
  }
})();
