import os
import glob

html_files = glob.glob("hamro_hospital/templates/reports/*.html")

for file in html_files:
    if file.endswith("revenue_dashboard.html"):
        continue

    with open(file, "r") as f:
        code = f.read()

    if "{% load finance_tags %}" not in code:
        code = code.replace("{% extends 'dashboard_base.html' %}", "{% extends 'dashboard_base.html' %}\n{% load finance_tags %}")

    import re
    # Match any stat-card containing NPR {{ something }}
    pattern = r'<div class="stat-card ([a-z]+)"><h6>(.*?)</h6><h[34] class="fw-bold">NPR \{\{\s*(.*?)\s*\}\}</h[34]></div>'
    
    def repl(m):
        color = m.group(1)
        label = m.group(2)
        var = m.group(3)
        return f'<div class="stat-card {color} click-amount-card" onclick="showFullValue(\'{label}\', \'NPR {{{{{var}|floatformat:2}}}}\')"><h6>{label}</h6><h3 class="fw-bold">NPR {{{{{var}|short_amount}}}}</h3></div>'

    code = re.sub(pattern, repl, code)

    with open(file, "w") as f:
        f.write(code)

