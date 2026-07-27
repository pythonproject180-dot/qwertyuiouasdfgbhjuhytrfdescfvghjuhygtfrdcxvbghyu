with open("hamro_hospital/templates/website/home.html", "r") as f:
    code = f.read()

code = code.replace('<section class="container py-5">\n    <h2 class="text-center mb-4 fw-bold">External Hospital Services (EHS)</h2>', '<section id="ehs" class="container py-5">\n    <h2 class="text-center mb-4 fw-bold">External Hospital Services (EHS)</h2>')

with open("hamro_hospital/templates/website/home.html", "w") as f:
    f.write(code)
