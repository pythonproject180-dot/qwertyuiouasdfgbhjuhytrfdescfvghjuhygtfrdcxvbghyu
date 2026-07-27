import re

with open("hamro_hospital/templates/reports/revenue_dashboard.html", "r") as f:
    code = f.read()

# Add load statement
if "{% load finance_tags %}" not in code:
    code = code.replace("{% extends 'dashboard_base.html' %}", "{% extends 'dashboard_base.html' %}\n{% load finance_tags %}")

# Replace full numbers with shortened ones and add click handlers
replacements = [
    (r"NPR {{ todays_revenue\|floatformat:2 }}", r"NPR {{ todays_revenue|short_amount }}"),
    (r"NPR {{ monthly_revenue\|floatformat:2 }}", r"NPR {{ monthly_revenue|short_amount }}"),
    (r"NPR {{ yearly_revenue\|floatformat:2 }}", r"NPR {{ yearly_revenue|short_amount }}"),
    (r"NPR {{ total_revenue\|floatformat:2 }}", r"NPR {{ total_revenue|short_amount }}"),
]

for old, new in replacements:
    code = re.sub(old, new, code)

# Make cards clickable
card_replacements = [
    (r'<div class="stat-card blue shadow-sm d-flex flex-column justify-content-between p-3" style="min-height: 110px;">',
     r'<div class="stat-card blue shadow-sm d-flex flex-column justify-content-between p-3 click-amount-card" style="min-height: 110px;" onclick="showFullValue(\'Today\\\'s Revenue\', \'NPR {{ todays_revenue|floatformat:2 }}\')">'),
    
    (r'<div class="stat-card green shadow-sm d-flex flex-column justify-content-between p-3" style="min-height: 110px;">',
     r'<div class="stat-card green shadow-sm d-flex flex-column justify-content-between p-3 click-amount-card" style="min-height: 110px;" onclick="showFullValue(\'Monthly Revenue\', \'NPR {{ monthly_revenue|floatformat:2 }}\')">'),
    
    (r'<div class="stat-card orange shadow-sm d-flex flex-column justify-content-between p-3" style="min-height: 110px;">',
     r'<div class="stat-card orange shadow-sm d-flex flex-column justify-content-between p-3 click-amount-card" style="min-height: 110px;" onclick="showFullValue(\'Yearly Revenue\', \'NPR {{ yearly_revenue|floatformat:2 }}\')">'),
    
    (r'<div class="stat-card gray shadow-sm d-flex flex-column justify-content-between p-3" style="min-height: 110px;">',
     r'<div class="stat-card gray shadow-sm d-flex flex-column justify-content-between p-3 click-amount-card" style="min-height: 110px;" onclick="showFullValue(\'Total Revenue (All Time)\', \'NPR {{ total_revenue|floatformat:2 }}\')">'),
]

for old, new in card_replacements:
    code = code.replace(old, new)


with open("hamro_hospital/templates/reports/revenue_dashboard.html", "w") as f:
    f.write(code)
