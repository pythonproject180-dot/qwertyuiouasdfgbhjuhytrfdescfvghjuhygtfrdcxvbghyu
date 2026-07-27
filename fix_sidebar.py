import os
import glob

# Ensure sidebar current section stays expanded/accessible 
# Instead of replacing the sidebar block completely on every page, we can 
# improve it so it's always accessible and clean.
# However, the user asked for: 
# "Clicking Department should display its submenu immediately."
# We'll build a Javascript that prevents accordion collapse on active elements.

# Wait, the prompt states: 
# "The dashboard navigation is currently confusing. When navigating between modules: 
# - The sidebar should remain visible.
# - The current section should stay expanded.
# - Related submenu items should remain accessible.
# - Users should not have to return to the main dashboard repeatedly."

# The current structure overrides `{% block sidebar %}` per app.
# That means if you click "Departments", you see the Departments sidebar, but you LOSE the links to 
# "Doctors", "Patients", "Lab", etc., forcing you to go back to the Main Dashboard.

# The ideal solution is a universal sidebar based on Role.
