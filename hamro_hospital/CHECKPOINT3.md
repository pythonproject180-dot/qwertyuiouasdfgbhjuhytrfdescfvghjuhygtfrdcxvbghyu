# Checkpoint 3 - Handoff Notes

This checkpoint adds the 6 missing departments, a unified PDF/document system used
by every department, IPD/surgery billing with a refund workflow, Excel export on
reports, and backup/restore tooling, on top of the existing Checkpoint 2 system.

**Important: this code was written without a working Django install** (the build
sandbox has no internet access, so Django/pip could not be installed to run
`manage.py` or execute tests). Every file was hand-written against the existing
codebase's conventions and cross-checked line-by-line against the real model
field names, but it has **not been executed**. Follow the setup steps below
carefully and expect to fix a small mistake or two on first run.

## Setup (run in order)

```bash
pip install -r requirements.txt          # now includes openpyxl for Excel export
python manage.py makemigrations          # generates migrations for documents,
                                          # nursing, operation_theatre, blood_bank,
                                          # finance, medical_records, plus the
                                          # accounts/billing field & choice changes
python manage.py migrate
python manage.py createsuperuser         # if you don't already have one
python manage.py seed_checkpoint3_data   # one-shot demo data (see below)
python manage.py runserver
```

`seed_checkpoint3_data` automatically runs `seed_nepal_address` and
`seed_demo_data` first if they haven't been run yet, then creates:
- ~25 Nepali patients (reuses existing ones if you already have some)
- 3 staff accounts per new role (`nurse1`/`nurse2`/`nurse3`, `ot1`-`ot3`,
  `bloodbank1`-`3`, `accounts1`-`3`, `medrecords1`-`3`, `ward1`-`3`),
  password `sashi` for all of them
- 25 visits/consultations with prescriptions, ~12 lab requests, ~8 radiology requests
- 20 admissions with nursing notes, 20 surgery records, 25 blood units (8 issued)
- 25 bills (OPD/IPD/lab/surgery mixed), 20 pharmacy sales
- 20 patient documents (placeholder PDFs) spread across every document category

## What's new

**Roles** - 6 added to `accounts.Role`: Ward/Admission, Nursing, Operation
Theatre, Blood Bank, Accounts, Medical Records. Each has its own decorator in
`accounts/decorators.py` and dashboard routing in `User.dashboard_url_name()`.

**`documents` app** - the unified PDF system from spec section 3. Every
department uploads/views/downloads/replaces through `PatientDocument`
(category-tagged, versioned - replacing a file keeps the old version for
audit history instead of deleting it). Any authenticated staff role can use
it (`accounts_dept_required` style decorator: `any_staff_required`). Files
download through an authenticated view (`documents:document_download`), not
a raw `/media/` link.

**`nursing` app** - vitals + notes per admission, ward-round dashboard.

**`operation_theatre` app** - `Surgery` records (scheduling, surgeon,
anesthesia, pre/operative/post-op notes, status, charge amount), OT rooms,
patient lookup to schedule a new surgery.

**`blood_bank` app** - `BloodUnit` inventory (blood group/component/expiry),
issuing units against a patient with an audit trail (`BloodIssue`).

**`finance` app** - the Accounts department's dashboard: revenue by bill
type, pending refund count, links into the refund approval queue and the
existing Reports module.

**`medical_records` app** - patient search + a single aggregated "complete
digital file" view (OPD history, admissions, operations, lab, radiology,
prescriptions, billing, documents) matching spec section 2 exactly.

**Billing** - `Bill` now has `bill_type` (OPD/IPD/Lab/Pharmacy/Surgery/Other)
and optional `admission`/`surgery` links, so IPD and surgery charges use the
same billing flow with the right classification. `RefundRequest` model:
Cash Counter requests, Accounts approves/rejects, approving marks the bill
`REFUNDED` without ever editing/deleting the original (audit-safe, matching
the existing reprint-log pattern). PDF invoice download via reportlab.

**Reports** - `?export=excel` on every report (registration, department,
doctor, counter, pharmacy, laboratory, plus new nursing/OT/blood-bank
reports) streams an `.xlsx` via a shared `reports/excel_utils.py` helper.

**Security (section 11)** - `backup_data`/`restore_data` management commands
(JSON dumpdata/loaddata) plus a Super Admin "Backups" dashboard page to
trigger one. `AuditLog.Action` extended to cover documents, nursing,
surgery, blood bank, refunds, and backups.

## Known gaps / what to check first

1. **Migrations are unverified.** This is the biggest risk. If
   `makemigrations` produces something unexpected (e.g. a field default
   prompt for a non-nullable field added to an existing table), resolve it
   there rather than editing model files blindly - the model code was
   written carefully against the existing schema, but real migration
   dependency graphs can only be confirmed by actually running Django.
2. **Media security is only fixed for the new `documents` app.** Older
   `FileField`s (lab `result_file`, radiology `report_file`/`image_file`,
   pharmacy `manual_prescription_copy`, patient `photo`/`qr_code`) still
   serve via the plain `/media/` URL in `DEBUG` mode, same as Checkpoint 2 -
   they were not touched to avoid breaking working views/templates I
   couldn't test. For production, put a reverse proxy in front that
   requires auth for `/media/`, or migrate those fields into
   `PatientDocument` over time.
3. **"20 records per module" is approximate**, not exact for every single
   module (e.g. exactly 3 staff accounts per new role, not 20 - 20 login
   accounts per department isn't a realistic demo dataset). Patients,
   admissions, surgeries, blood units, bills, and documents each hit the
   ≥20 bar; nursing notes end up well over 20 (2 per admission).
4. **OPD Counter / Billing Counter** from the spec's role list weren't added
   as separate roles - they map to the existing `Registration Counter` and
   `Cash Counter` roles, which already cover that functionality per the
   Checkpoint 1/2 design. Flag if you want them split out as distinct
   logins.
5. I did not re-verify existing Checkpoint 1/2 code beyond the files I
   directly edited (`patients/views.py`, `admissions/views.py`,
   `billing/models.py` & `views.py`, `reports/views.py`, `accounts/*`,
   several templates) - the rest of the codebase is untouched from your
   upload.

## Login quick reference (after seeding)

| Role | Username | Password |
|---|---|---|
| Ward/Admission | `ward1` | `sashi` |
| Nursing | `nurse1` | `sashi` |
| Operation Theatre | `ot1` | `sashi` |
| Blood Bank | `bloodbank1` | `sashi` |
| Accounts | `accounts1` | `sashi` |
| Medical Records | `medrecords1` | `sashi` |
