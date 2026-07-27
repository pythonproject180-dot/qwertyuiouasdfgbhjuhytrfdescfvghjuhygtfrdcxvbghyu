import re

with open("hamro_hospital/templates/patients/patient_register.html", "r") as f:
    code = f.read()

# Add barcode scanner inclusion and script at the top of content
scanner_html = """
{% include 'patients/_qr_scanner.html' with target_prefix='id_' %}
<div class="tuh-card p-4 mb-4 bg-light">
    <h5 class="fw-bold mb-3 text-primary"><i class="bi bi-upc-scan"></i> Scan Barcode / QR Code</h5>
    <p class="text-muted small">Scan an existing patient's code to automatically fill their details and mark them as a Returning Patient.</p>
    <div class="d-flex gap-2 align-items-center">
        <input type="text" id="id_q" name="q" class="form-control" placeholder="Scan or type code here" style="max-width: 300px;">
        <button type="button" class="btn btn-primary" onclick="lookupPatient(document.getElementById('id_q').value)">Retrieve Patient</button>
    </div>
</div>
<script>
document.addEventListener('tuh:patient-scanned', function () { 
    lookupPatient(document.getElementById('id_q').value);
});

function lookupPatient(query) {
    if (!query) return;
    fetch(`/patients/api/lookup/?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if (data.found) {
                // Populate fields
                document.getElementById('id_first_name').value = data.first_name || '';
                document.getElementById('id_last_name').value = data.last_name || '';
                document.getElementById('id_phone_number').value = data.phone_number || '';
                if(data.gender) document.getElementById('id_gender').value = data.gender;
                
                // Set patient type to Old automatically
                const ptSelect = document.getElementById('id_patient_type');
                if(ptSelect) {
                    ptSelect.value = 'old';
                    ptSelect.dispatchEvent(new Event('change'));
                }
                
                alert('Patient details retrieved successfully. Marked as Returning Patient.');
            } else {
                alert('Patient not found.');
            }
        });
}
</script>
"""

code = code.replace("{% block dashboard_content %}", "{% block dashboard_content %}\n" + scanner_html)

# Add Payment Method to Visit form
visit_html_old = """            <div class="col-md-4">
                <label class="form-label">Patient Type *</label>
                {{ visit_form.patient_type }}
            </div>
            <div class="col-12">"""

visit_html_new = """            <div class="col-md-4">
                <label class="form-label">Patient Type *</label>
                {{ visit_form.patient_type }}
            </div>
            <div class="col-md-4">
                <label class="form-label">Payment Method *</label>
                {{ visit_form.payment_method }}
            </div>
            <div class="col-12">"""

code = code.replace(visit_html_old, visit_html_new)

with open("hamro_hospital/templates/patients/patient_register.html", "w") as f:
    f.write(code)
