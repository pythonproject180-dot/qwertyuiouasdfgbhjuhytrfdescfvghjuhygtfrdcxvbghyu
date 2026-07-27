with open("hamro_hospital/templates/website/home.html", "r") as f:
    code = f.read()

import re

# Remove the "Already a patient here?" section entirely to keep it clean, as login button is now in hero
pattern = r'<section class="container py-5">\s*<div class="tuh-card p-4 p-md-5">\s*<div class="row align-items-center g-4">.*?</div>\s*</div>\s*</section>'
code = re.sub(pattern, '', code, flags=re.DOTALL)

with open("hamro_hospital/templates/website/home.html", "w") as f:
    f.write(code)
