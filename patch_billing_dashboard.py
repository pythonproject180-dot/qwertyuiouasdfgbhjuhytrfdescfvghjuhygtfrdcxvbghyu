import re

with open("hamro_hospital/templates/billing/dashboard.html", "r") as f:
    code = f.read()

# Add load statement
if "{% load finance_tags %}" not in code:
    code = code.replace("{% extends 'dashboard_base.html' %}", "{% extends 'dashboard_base.html' %}\n{% load finance_tags %}")

# Replace and add onclick
replacements = [
    (r'<div class="stat-card green"><i class="bi bi-cash-stack fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ todays_total }}</h2><small>Total Collected</small></div>',
     r'<div class="stat-card green click-amount-card" onclick="showFullValue(\'Total Collected (Today)\', \'NPR {{ todays_total|floatformat:2 }}\')"><i class="bi bi-cash-stack fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ todays_total|short_amount }}</h2><small>Total Collected</small></div>'),
    
    (r'<div class="stat-card orange"><i class="bi bi-credit-card fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ totals_by_method.esewa }}</h2><small>eSewa</small></div>',
     r'<div class="stat-card orange click-amount-card" onclick="showFullValue(\'eSewa Collected\', \'NPR {{ totals_by_method.esewa|floatformat:2 }}\')"><i class="bi bi-credit-card fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ totals_by_method.esewa|short_amount }}</h2><small>eSewa</small></div>'),
     
    (r'<div class="stat-card gray"><i class="bi bi-shield-check fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ totals_by_method.insurance }}</h2><small>Insurance</small></div>',
     r'<div class="stat-card gray click-amount-card" onclick="showFullValue(\'Insurance Billed\', \'NPR {{ totals_by_method.insurance|floatformat:2 }}\')"><i class="bi bi-shield-check fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ totals_by_method.insurance|short_amount }}</h2><small>Insurance</small></div>'),
     
    (r'<div class="stat-card green"><i class="bi bi-graph-up fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ monthly_total }}</h2><small>Revenue This Month</small></div>',
     r'<div class="stat-card green click-amount-card" onclick="showFullValue(\'Revenue This Month\', \'NPR {{ monthly_total|floatformat:2 }}\')"><i class="bi bi-graph-up fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ monthly_total|short_amount }}</h2><small>Revenue This Month</small></div>'),
     
    (r'<div class="stat-card green"><i class="bi bi-bar-chart fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ yearly_total }}</h2><small>Revenue This Year</small></div>',
     r'<div class="stat-card green click-amount-card" onclick="showFullValue(\'Revenue This Year\', \'NPR {{ yearly_total|floatformat:2 }}\')"><i class="bi bi-bar-chart fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ yearly_total|short_amount }}</h2><small>Revenue This Year</small></div>'),
]

for old, new in replacements:
    code = code.replace(old, new)


with open("hamro_hospital/templates/billing/dashboard.html", "w") as f:
    f.write(code)
