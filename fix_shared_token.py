with open("hamro_hospital/appointments/models.py", "r") as f:
    code = f.read()

import re

# Update token generation to use a shared utility instead of separate
# The current system has an `_get_next_token` in `appointments.models`
# Let's override it to look at both Appointments and Visits
code = code.replace(
    "last_appt = Appointment.objects.filter(doctor=doctor, preferred_date=date).order_by('-token_number').first()",
    """from patients.models import Visit
        last_appt = Appointment.objects.filter(doctor=doctor, preferred_date=date).order_by('-token_number').first()
        last_visit = Visit.objects.filter(doctor=doctor, visit_date=date).order_by('-token_number').first()
        
        last_appt_token = last_appt.token_number if last_appt else 0
        last_visit_token = last_visit.token_number if last_visit else 0
        return max(last_appt_token, last_visit_token) + 1"""
)

# wait, need to check how get_next_token is implemented exactly in patients.Visit vs appointments.Appointment.
