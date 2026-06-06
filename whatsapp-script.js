var distributorForm = document.getElementById('distributorForm');
if (distributorForm) {
  distributorForm.addEventListener('submit', function(e) {
    e.preventDefault();
    if (!distributorForm.checkValidity()) {
      distributorForm.reportValidity();
      return;
    }
    var data = new FormData(distributorForm);
    var message = 'New contact request from liquidpowerdrink.com'
      + '%0A%0AName: ' + encodeURIComponent(data.get('nombre') || '')
      + '%0ACompany: ' + encodeURIComponent(data.get('empresa') || '')
      + '%0AContact: ' + encodeURIComponent(data.get('contacto') || '')
      + '%0A%0AComments:%0A' + encodeURIComponent(data.get('mensaje') || '');
    // Replace 34646712043 with your full WhatsApp number (no + or spaces)
    window.open('https://wa.me/34646712043?text=' + message, '_blank');
  });
}