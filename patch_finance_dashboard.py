import re

with open("hamro_hospital/templates/finance/dashboard.html", "r") as f:
    code = f.read()

# Add load statement
if "{% load finance_tags %}" not in code:
    code = code.replace("{% extends 'dashboard_base.html' %}", "{% extends 'dashboard_base.html' %}\n{% load finance_tags %}")

# Replace and add onclick
replacements = [
    (r'<div class="stat-card green"><i class="bi bi-cash-coin fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ todays_total }}</h2><small>Today\'s Revenue</small></div>',
     r'<div class="stat-card green click-amount-card" onclick="showFullValue(\'Today\\\'s Revenue\', \'NPR {{ todays_total|floatformat:2 }}\')"><i class="bi bi-cash-coin fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ todays_total|short_amount }}</h2><small>Today\'s Revenue</small></div>'),
    
    (r'<div class="stat-card blue"><i class="bi bi-calendar-month fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ month_total }}</h2><small>This Month\'s Revenue</small></div>',
     r'<div class="stat-card blue click-amount-card" onclick="showFullValue(\'This Month\\\'s Revenue\', \'NPR {{ month_total|floatformat:2 }}\')"><i class="bi bi-calendar-month fs-3"></i><h2 class="fw-bold mt-2 mb-0">NPR {{ month_total|short_amount }}</h2><small>This Month\'s Revenue</small></div>'),
]

for old, new in replacements:
    code = code.replace(old, new)


with open("hamro_hospital/templates/finance/dashboard.html", "w") as f:
    f.write(code)
