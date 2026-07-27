with open("hamro_hospital/templates/website/home.html", "r") as f:
    code = f.read()

# Add scrolling banner at the top
banner = """{% block content %}
{% if home_notification %}
<div style="background-color: var(--accent); color: white; padding: 10px 0; overflow: hidden; white-space: nowrap; font-size: 1.1rem; font-weight: 600;">
    <div style="display: inline-block; padding-left: 100%; animation: marquee 20s linear infinite;">
        {{ home_notification.message }}
    </div>
</div>
<style>
@keyframes marquee {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
}
</style>
{% endif %}
"""
code = code.replace("{% block content %}", banner)

# Update Hero section
hero_old = """<section class="tuh-hero text-center">
    <div class="container">
        <h1 class="display-4 fw-bold mb-3">हाम्रो अस्पताल — स्वास्थ्य नै सबैभन्दा ठूलो धन हो।</h1>
        <p class="lead mb-4">{{ HOSPITAL_NAME }} brings together expert doctors and modern facilities for the people of Nepal.</p>
        <div class="d-flex justify-content-center gap-3 flex-wrap">
            <a href="tel:{{ HOSPITAL_EMERGENCY_PHONE }}" class="btn btn-danger btn-lg text-white">
                <i class="bi bi-telephone-fill"></i> Emergency: {{ HOSPITAL_EMERGENCY_PHONE }}
            </a>
        </div>
    </div>
</section>"""

hero_new = """<section class="tuh-hero text-center">
    <div class="container">
        <h1 class="display-4 fw-bold mb-3">हाम्रो अस्पताल — स्वास्थ्य नै सबैभन्दा ठूलो धन हो।</h1>
        <p class="lead mb-4">हाम्रो अस्पतालले दक्ष चिकित्सक र अत्याधुनिक प्रविधि मार्फत नेपालका नागरिकहरूलाई उत्कृष्ट, भरपर्दो र सुलभ स्वास्थ्य सेवा प्रदान गर्दै आइरहेको छ।</p>
        <div class="d-flex justify-content-center gap-3 flex-wrap">
            <a href="{% url 'patient_portal:login' %}" class="btn btn-danger btn-lg text-white">
                <i class="bi bi-person-circle"></i> Patient Login
            </a>
        </div>
    </div>
</section>"""
code = code.replace(hero_old, hero_new)

# Rename Departments to EHS
code = code.replace('<h2 class="text-center mb-4 fw-bold">Our Departments</h2>', '<h2 class="text-center mb-4 fw-bold">External Hospital Services (EHS)</h2>')

code = code.replace('<section class="container py-5">\\n    <h2 class="text-center mb-4 fw-bold">External Hospital Services (EHS)</h2>', '<section id="ehs" class="container py-5">\\n    <h2 class="text-center mb-4 fw-bold">External Hospital Services (EHS)</h2>')


with open("hamro_hospital/templates/website/home.html", "w") as f:
    f.write(code)
