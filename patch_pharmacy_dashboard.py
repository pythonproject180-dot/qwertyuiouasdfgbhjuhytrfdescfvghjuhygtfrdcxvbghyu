import re

with open("hamro_hospital/templates/pharmacy/dashboard.html", "r") as f:
    code = f.read()

if "{% load finance_tags %}" not in code:
    code = code.replace("{% extends 'dashboard_base.html' %}", "{% extends 'dashboard_base.html' %}\n{% load finance_tags %}")

replacements = [
    (r'<div class="stat-card green"><i class="bi bi-cash-stack fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ todays_total }}</h2><small>Total Today</small></div>',
     r'<div class="stat-card green click-amount-card" onclick="showFullValue(\'Total Today\', \'NPR {{ todays_total|floatformat:2 }}\')"><i class="bi bi-cash-stack fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ todays_total|short_amount }}</h2><small>Total Today</small></div>'),
    
    (r'<div class="stat-card green"><i class="bi bi-graph-up fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ monthly_total }}</h2><small>Revenue This Month</small></div>',
     r'<div class="stat-card green click-amount-card" onclick="showFullValue(\'Revenue This Month\', \'NPR {{ monthly_total|floatformat:2 }}\')"><i class="bi bi-graph-up fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ monthly_total|short_amount }}</h2><small>Revenue This Month</small></div>'),
     
    (r'<div class="stat-card green"><i class="bi bi-bar-chart fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ yearly_total }}</h2><small>Revenue This Year</small></div>',
     r'<div class="stat-card green click-amount-card" onclick="showFullValue(\'Revenue This Year\', \'NPR {{ yearly_total|floatformat:2 }}\')"><i class="bi bi-bar-chart fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ yearly_total|short_amount }}</h2><small>Revenue This Year</small></div>'),
]

for old, new in replacements:
    code = code.replace(old, new)


with open("hamro_hospital/templates/pharmacy/dashboard.html", "w") as f:
    f.write(code)
