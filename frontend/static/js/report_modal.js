document.addEventListener('DOMContentLoaded', function(){
  var modalEl = document.getElementById('reportModal');
  var iframe = document.getElementById('reportFrame');
  if(!modalEl || !iframe) return;
  var modal = new bootstrap.Modal(modalEl);
  document.querySelectorAll('.js-open-report').forEach(function(btn){
    btn.addEventListener('click', function(ev){
      // Progressive enhancement: usa modal se JS estiver ativo
      ev.preventDefault();
      var url = this.getAttribute('data-url') || this.getAttribute('href');
      if(url){
        // Abre já com recent-first
        iframe.src = url + (url.indexOf('?') >= 0 ? '&' : '?') + 'order=new';
        modal.show();
      }
    });
  });
  modalEl.addEventListener('hidden.bs.modal', function(){
    iframe.src = 'about:blank';
  });
});