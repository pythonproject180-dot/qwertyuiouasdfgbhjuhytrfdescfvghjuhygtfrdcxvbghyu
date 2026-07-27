# Pass 5 - Dummy Data Fill + Req 4-20 Re-verify

No Django in this sandbox still (no internet). Data changes below were
written straight into `db.sqlite3` via raw sqlite3, matching the exact
schema of each model (verified column-by-column against `models.py`
before inserting) - not run through the ORM, so `python manage.py
makemigrations --check` is still the first thing to run after `pip
install`, same caveat as every prior pass.

## Correction to Pass 4 audit
Req 15 (chatbot) is NOT missing - it exists as `website.views.assistant_api`
+ the floating "CareBot" widget in `templates/base.html`. Keyword-gated to
hospital topics (OPD/emergency timings, doctor lookup, departments,
contact, insurance, booking), only queries `Doctor`/`Department`, never
touches `Patient`. Earlier grep for literal "chat" missed it since the
view/widget is named "assistant"/"CareBot", not "chatbot". One real gap:
the widget lives in `base.html`, which `dashboard_base.html` also extends,
so it shows on internal staff pages too, not just the public site -
cosmetic, not a data-safety issue since it never queries patient data.

## Dummy data - filled every table that was at 0 or under 50
Inserted directly into `db.sqlite3`, all FK'd to real existing rows
(patients, admissions, bills, medicines, users):

- `accounts_notification` 0 -> 55
- `nursing_note` 0 -> 55
- `website_contact_message` 0 -> 55
- `blood_bank_unit` 0 -> 55, `blood_bank_issue` 0 -> 55 (issued units flip to status=issued)
- `billing_discount_request` 0 -> 55, `billing_refund_request` 0 -> 55
- `pharmacy_stock_adjustment` 0 -> 55 (running resulting_stock computed per medicine)
- `accounts_audit_log` 5 -> 55
- `website_disease_info` 3 -> 48 (2 of the 50 candidate names collided with existing rows, skipped)
- `website_gallery_image` 15 -> 50
- `ot_surgery` 15 -> 50
- `departments_department` 25 -> 50 (25 new sub-specialty departments, Nepali-hospital-realistic)
- `doctors_doctor` 15 -> 50 (new doctors spread across all departments, no `user_account_id` -
  they're directory/booking entries, not login accounts; only staff who need to log in have a User row)

Not bumped to 50: `insurance_company` (7) and `admissions_ward` (7). Real
Nepali hospitals realistically deal with well under 50 insurance
companies and physical wards - forcing that number would mean inventing
fake entities with no operational meaning. Left as-is; flag if you
actually want 50 regardless.

## Req 4-20 re-verified this pass
- Req 4 (phone on every printable doc) - confirmed present on all 8:
  patient card, OPD ticket, billing/pharmacy/lab/radiology receipts,
  admission slip, insurance claim slip.
- Req 11 (appointment age + DOB, auto-calc) - confirmed:
  `appointments/forms.py` computes `date_of_birth` from `age` via
  `relativedelta` when only age is given.
- Req 19 (staff discount / auto insurance coverage calc) - **gap**.
  `billing.DiscountRequest` exists (generic reason field, e.g. "Staff
  family") but there's no dedicated 90%-staff-discount rule or automatic
  insurance-coverage-percentage calculator anywhere in `insurance/models.py`.
  Every claim currently needs the amount entered by hand.
- Req 20 (RBAC enforced per view) - `accounts/decorators.py::role_required`
  (+ per-role shortcuts like `laboratory_required`) is real and wraps
  `@login_required`, checks `request.user.effective_role`, superuser
  bypass. Applied across laboratory/radiology/billing views on spot check.
  Did not audit every single view function in every app for a missing
  decorator - that needs a full pass, not a sample.

## Still the two real gaps, unchanged from what I flagged last message
1. **Req 10, payment gateways** - only eSewa is a real signed integration
   (`appointments/esewa.py`). Khalti and FonePay are dropdown labels only;
   selecting them just writes a fake `TXN-{method}-{random}` reference and
   marks paid. No real gateway call.
2. **Req 5/6, Search Patient + Scan QR "everywhere"** - only present in
   Billing, Blood Bank, Insurance, Medical Records, Operation Theatre,
   Pharmacy, and the generic Patients app. No dedicated
   lookup/scan template or view found for: **Laboratory, Radiology,
   Admissions, Nursing, Doctors, Appointments, Reports, Cash Counter, or
   the main Dashboard.** No global search bar in `dashboard_base.html`
   either, so those 9 areas have to reach a patient through whatever
   detail-page link already exists, not a dedicated search/scan entry
   point per spec.

## Suggested next step
Item 2 above is the biggest true gap left against the spec (named
explicitly, affects 9 modules) - it's real view+template+URL work across
9 Django apps, which is too much to hand-write blind (no server to click
through) safely in one more pass without risking broken `{% url %}`
references. Recommend doing it one module at a time, laboratory first
(highest clinical traffic), each verified against its own `urls.py`
before moving to the next, rather than all 9 at once.
