document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    var alertList = document.querySelectorAll('.alert')
    alertList.forEach(function (alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    var coverImageInput = document.querySelector('input[type="file"]');
    if (coverImageInput) {
        coverImageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                var reader = new FileReader();

                reader.onload = function(e) {
                    var preview = document.querySelector('.img-thumbnail');
                    if (preview) {
                        preview.src = e.target.result;
                    }
                }

                reader.readAsDataURL(this.files[0]);
            }
        });
    }
});