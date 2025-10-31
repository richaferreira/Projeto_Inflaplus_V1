
(function(){
  const map = L.map('mapPicker');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap' }).addTo(map);
  map.setView([-22.0, -43.0], 6);

  let marker;
  function setLatLon(lat, lon){
    const latField = document.getElementById('latField');
    const lonField = document.getElementById('lonField');
    if(!latField || !lonField) return;
    latField.value = (+lat).toFixed(6);
    lonField.value = (+lon).toFixed(6);
    if (marker) { map.removeLayer(marker); }
    marker = L.marker([lat, lon]).addTo(map);
    map.setView([lat, lon], 16);
  }

  map.on('click', (e) => setLatLon(e.latlng.lat, e.latlng.lng));

  const btn = document.getElementById('btnUseLocation');
  btn && btn.addEventListener('click', () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
        setLatLon(pos.coords.latitude, pos.coords.longitude);
      }, () => alert('Não foi possível obter sua localização.'));
    } else {
      alert('Geolocalização não suportada.');
    }
  });
})();
