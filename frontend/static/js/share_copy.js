
(function(){
  const btn = document.getElementById('btnCopy');
  if (btn){
    btn.addEventListener('click', ()=>{
      navigator.clipboard.writeText(window.location.href).then(()=> alert('Link copiado!'));
    });
  }
})();
