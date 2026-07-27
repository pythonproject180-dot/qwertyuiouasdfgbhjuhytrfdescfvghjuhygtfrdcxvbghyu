with open("hamro_hospital/patients/models.py", "r") as f:
    code = f.read()

# Make sure fields are completely strictly required
code = code.replace("first_name = models.CharField(max_length=100)", "first_name = models.CharField(max_length=100, blank=False, null=False)")
code = code.replace("last_name = models.CharField(max_length=100)", "last_name = models.CharField(max_length=100, blank=False, null=False)")
code = code.replace("phone_number = models.CharField(max_length=20)", "phone_number = models.CharField(max_length=20, blank=False, null=False)")

with open("hamro_hospital/patients/models.py", "w") as f:
    f.write(code)
