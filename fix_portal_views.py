with open("hamro_hospital/patient_portal/views.py", "r") as f:
    code = f.read()

# Make the backend capture the new Payment Method correctly
old_visit_save = """            visit = form.save(commit=False)
            visit.patient = patient
            visit.registration_fee = form.cleaned_data['registration_fee']
            visit.created_by = None  # self-booked, not staff-created
            visit.save()"""

new_visit_save = """            visit = form.save(commit=False)
            visit.patient = patient
            visit.registration_fee = form.cleaned_data['registration_fee']
            
            # Handle payment method
            payment_method = request.POST.get('payment_method', 'cash')
            use_insurance = request.POST.get('use_insurance', 'no')
            
            if use_insurance == 'yes':
                visit.payment_method = 'insurance'
            else:
                visit.payment_method = payment_method

            if visit.payment_method == 'esewa':
                visit.payment_status = 'pending_esewa'
            else:
                visit.payment_status = 'unpaid'
            
            visit.created_by = None  # self-booked, not staff-created
            visit.save()"""

code = code.replace(old_visit_save, new_visit_save)

with open("hamro_hospital/patient_portal/views.py", "w") as f:
    f.write(code)
