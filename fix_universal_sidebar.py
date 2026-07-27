with open("hamro_hospital/templates/dashboard_base.html", "r") as f:
    code = f.read()

# Replace block sidebar with a universal dynamic sidebar
universal_sidebar = """
            <nav class="nav flex-column" id="universalSidebar">
                <a class="nav-link" href="{{ user_dashboard_url }}"><i class="bi bi-speedometer2"></i> <span>Main Dashboard</span></a>
                
                {% if request.user.role == 'super_admin' %}
                <!-- Super Admin Menu -->
                <div class="nav-item">
                    <a class="nav-link" data-bs-toggle="collapse" href="#menuDepartments" role="button" aria-expanded="false" aria-controls="menuDepartments">
                        <i class="bi bi-diagram-3"></i> <span>Departments</span> <i class="bi bi-chevron-down ms-auto" style="font-size: 0.8rem;"></i>
                    </a>
                    <div class="collapse" id="menuDepartments" data-bs-parent="#universalSidebar">
                        <div class="ps-4">
                            <a class="nav-link small py-1" href="{% url 'departments:department_list' %}">Manage Departments</a>
                            <a class="nav-link small py-1" href="{% url 'departments:department_create' %}">Add New</a>
                        </div>
                    </div>
                </div>
                
                <div class="nav-item">
                    <a class="nav-link" data-bs-toggle="collapse" href="#menuDoctors" role="button" aria-expanded="false" aria-controls="menuDoctors">
                        <i class="bi bi-person-badge"></i> <span>Doctors</span> <i class="bi bi-chevron-down ms-auto" style="font-size: 0.8rem;"></i>
                    </a>
                    <div class="collapse" id="menuDoctors" data-bs-parent="#universalSidebar">
                        <div class="ps-4">
                            <a class="nav-link small py-1" href="{% url 'doctors:doctor_list' %}">Manage Doctors</a>
                            <a class="nav-link small py-1" href="{% url 'doctors:doctor_create' %}">Add New</a>
                        </div>
                    </div>
                </div>
                
                <div class="nav-item">
                    <a class="nav-link" data-bs-toggle="collapse" href="#menuReports" role="button" aria-expanded="false" aria-controls="menuReports">
                        <i class="bi bi-bar-chart"></i> <span>Reports & Finance</span> <i class="bi bi-chevron-down ms-auto" style="font-size: 0.8rem;"></i>
                    </a>
                    <div class="collapse" id="menuReports" data-bs-parent="#universalSidebar">
                        <div class="ps-4">
                            <a class="nav-link small py-1" href="{% url 'reports:revenue_dashboard' %}">Revenue Dashboard</a>
                            <a class="nav-link small py-1" href="{% url 'reports:department_report' %}">Department Reports</a>
                            <a class="nav-link small py-1" href="{% url 'reports:doctor_report' %}">Doctor Reports</a>
                        </div>
                    </div>
                </div>
                
                <div class="nav-item">
                    <a class="nav-link" data-bs-toggle="collapse" href="#menuSettings" role="button" aria-expanded="false" aria-controls="menuSettings">
                        <i class="bi bi-gear"></i> <span>System Settings</span> <i class="bi bi-chevron-down ms-auto" style="font-size: 0.8rem;"></i>
                    </a>
                    <div class="collapse" id="menuSettings" data-bs-parent="#universalSidebar">
                        <div class="ps-4">
                            <a class="nav-link small py-1" href="{% url 'accounts:staff_list' %}">Staff Accounts</a>
                            <a class="nav-link small py-1" href="{% url 'accounts:hospital_settings' %}">Hospital Settings</a>
                            <a class="nav-link small py-1" href="{% url 'website:service_list' %}">Website Services</a>
                            <a class="nav-link small py-1" href="{% url 'accounts:backups_view' %}">Backups</a>
                        </div>
                    </div>
                </div>
                {% endif %}
                
                <!-- Display context-specific sidebar block appended if needed -->
                <hr class="border-secondary opacity-25 mx-3 my-2">
                {% block sidebar %}
                {% endblock %}
            </nav>
            
            <script>
            // Ensure accordion menus auto-open if the current URL is inside them
            document.addEventListener("DOMContentLoaded", function() {
                const currentPath = window.location.pathname;
                document.querySelectorAll('#universalSidebar .collapse').forEach(function(collapseEl) {
                    const links = collapseEl.querySelectorAll('a.nav-link');
                    links.forEach(function(link) {
                        if (link.getAttribute('href') && currentPath.includes(link.getAttribute('href'))) {
                            link.classList.add('fw-bold', 'text-primary');
                            new bootstrap.Collapse(collapseEl, {toggle: false}).show();
                        }
                    });
                });
            });
            </script>
"""

old_nav = """            {% block sidebar %}
            <nav class="nav flex-column">
                <a class="nav-link" href="{{ user_dashboard_url }}"><i class="bi bi-speedometer2"></i> <span>Dashboard</span></a>
            </nav>
            {% endblock %}"""

code = code.replace(old_nav, universal_sidebar)

with open("hamro_hospital/templates/dashboard_base.html", "w") as f:
    f.write(code)
