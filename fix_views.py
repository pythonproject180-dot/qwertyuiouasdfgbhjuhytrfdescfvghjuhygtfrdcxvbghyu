import re

with open("hamro_hospital/patients/views.py", "r") as f:
    code = f.read()

# Make the JSON response from qr_lookup include all necessary fields for the form
code = code.replace("return JsonResponse({", "return JsonResponse({\n        'first_name': patient.first_name,\n        'last_name': patient.last_name,\n        'phone_number': patient.phone_number,\n        'gender': patient.gender,")

with open("hamro_hospital/patients/views.py", "w") as f:
    f.write(code)

with open("hamro_hospital/patients/urls.py", "r") as f:
    urls_code = f.read()
urls_code = urls_code.replace("'api/qr-lookup/'", "'api/lookup/'")
with open("hamro_hospital/patients/urls.py", "w") as f:
    f.write(urls_code)

