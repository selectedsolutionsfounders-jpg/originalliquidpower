var distributorForm = document.getElementById('distributorForm');
var successMessage = document.getElementById('successMessage');
if (distributorForm) {
  distributorForm.addEventListener('submit', function(e) {
    e.preventDefault();
    if (!distributorForm.checkValidity()) {
      distributorForm.reportValidity();
      return;
    }
    var data = new FormData(distributorForm);
    fetch(distributorForm.action, {
      method: 'POST',
      body: data,
      headers: { 'Accept': 'application/json' }
    }).then(function(response) {
      if (response.ok) {
        if (successMessage) successMessage.style.display = 'block';
        distributorForm.reset();
      } else {
        alert('There was an error. Please try again or contact us directly.');
      }
    }).catch(function() {
      alert('Connection error. Please try again later.');
    });
  });
}