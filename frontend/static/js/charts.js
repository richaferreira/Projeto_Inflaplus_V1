
(function(){
  const days = window.__DAYS || [];
  const series7 = window.__SERIES7 || [];
  const byCategory = window.__BY_CATEGORY || {};
  if (typeof Chart === 'undefined') return;
  new Chart(document.getElementById('chart7d'), {type:'line',data:{labels:days.map(d=>d.substring(5).split('-').reverse().join('/')),datasets:[{data:series7,label:'Denúncias',fill:true,borderColor:'rgba(13,110,253,.9)',backgroundColor:'rgba(13,110,253,.15)',tension:.3}]},options:{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,precision:0}}}});
  const catLabels = Object.keys(byCategory);
  const catValues = Object.values(byCategory);
  const palette = ['#0d6efd','#6f42c1','#198754','#fd7e14','#dc3545','#20c997'];
  new Chart(document.getElementById('chartCategory'), {type:'doughnut',data:{labels:catLabels,datasets:[{data:catValues,backgroundColor:palette.slice(0,catValues.length)}]},options:{plugins:{legend:{position:'bottom'}}}});
})();
