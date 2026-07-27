import re

with open("hamro_hospital/reports/views.py", "r") as f:
    code = f.read()

# Make the Revenue Dashboard viewable by Finance roles as requested:
# "The Finance Department should have permission to view revenue generated from all departments."

code = code.replace("@super_admin_required\ndef revenue_dashboard(request):", 
                    "@role_required(Role.SUPER_ADMIN, Role.ACCOUNTS_DEPT)\ndef revenue_dashboard(request):")

with open("hamro_hospital/reports/views.py", "w") as f:
    f.write(code)
