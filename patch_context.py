with open("hamro_hospital/website/context_processors.py", "r") as f:
    code = f.read()

patch = """
    home_notification = HomeNotification.objects.filter(is_active=True).first()

    user_dashboard_url = ''
"""

code = code.replace("    user_dashboard_url = ''", patch)

return_patch = """
        'public_announcements': public_announcements,
        'public_announcements_count': public_announcements_count,
        'home_notification': home_notification,
"""

code = code.replace("""        'public_announcements': public_announcements,
        'public_announcements_count': public_announcements_count,""", return_patch)

with open("hamro_hospital/website/context_processors.py", "w") as f:
    f.write(code)
