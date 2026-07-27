import re

with open("hamro_hospital/templates/patient_portal/book_visit.html", "r") as f:
    code = f.read()

# Add Payment Method exactly like Registration Counter
old_html = """            <div class="col-md-4">
                <label class="form-label">Visit Type *</label>
                {{ form.patient_type }}
            </div>
            <div class="col-12">"""

new_html = """            <div class="col-md-4">
                <label class="form-label">Visit Type *</label>
                {{ form.patient_type }}
            </div>
            <div class="col-md-4">
                <label class="form-label">Payment Method *</label>
                <select name="payment_method" class="form-select" id="id_payment_method" required>
                    <option value="cash" selected>Cash (Payment Pending)</option>
                    <option value="esewa">eSewa (Online Payment)</option>
                </select>
            </div>
            <div class="col-md-4">
                <label class="form-label">Use Insurance?</label>
                <select name="use_insurance" class="form-select">
                    <option value="no" selected>No</option>
                    <option value="yes">Yes (Will verify at counter)</option>
                </select>
            </div>
            <div class="col-12">"""

code = code.replace(old_html, new_html)

with open("hamro_hospital/templates/patient_portal/book_visit.html", "w") as f:
    f.write(code)
