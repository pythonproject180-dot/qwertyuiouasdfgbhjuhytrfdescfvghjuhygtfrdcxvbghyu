import re

with open("hamro_hospital/templates/patient_portal/dashboard.html", "r") as f:
    code = f.read()

# Make the Patient Portal dashboard mirror the requirements:
# "Profile, OPD Visits, Prescriptions, Laboratory Reports, Medical Records, Bills, Appointments"
links_grid = """
<div class="row g-3 mb-4">
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:my_visits' %}" class="btn btn-outline-primary w-100 py-3"><i class="bi bi-clipboard2-pulse d-block fs-3 mb-2"></i>OPD Visits</a></div>
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:my_prescriptions' %}" class="btn btn-outline-primary w-100 py-3"><i class="bi bi-capsule d-block fs-3 mb-2"></i>Prescriptions</a></div>
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:my_lab_reports' %}" class="btn btn-outline-primary w-100 py-3"><i class="bi bi-flask d-block fs-3 mb-2"></i>Lab Reports</a></div>
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:my_radiology_reports' %}" class="btn btn-outline-primary w-100 py-3"><i class="bi bi-file-earmark-medical d-block fs-3 mb-2"></i>Radiology</a></div>
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:my_bills' %}" class="btn btn-outline-primary w-100 py-3"><i class="bi bi-receipt d-block fs-3 mb-2"></i>Bills</a></div>
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:my_admissions' %}" class="btn btn-outline-primary w-100 py-3"><i class="bi bi-hospital d-block fs-3 mb-2"></i>Admissions</a></div>
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:my_documents' %}" class="btn btn-outline-primary w-100 py-3"><i class="bi bi-folder2-open d-block fs-3 mb-2"></i>Medical Records</a></div>
    <div class="col-6 col-md-3"><a href="{% url 'patient_portal:book_visit' %}" class="btn btn-primary w-100 py-3"><i class="bi bi-calendar-plus d-block fs-3 mb-2 text-white"></i>Book Appointment</a></div>
</div>
"""

code = code.replace('<div class="row g-4 mb-4">', links_grid + '\n<div class="row g-4 mb-4">')

with open("hamro_hospital/templates/patient_portal/dashboard.html", "w") as f:
    f.write(code)
