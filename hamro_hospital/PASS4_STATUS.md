# Pass 4 - Print Consistency + Named Bug Sweep

**Same limitation as before: no working Django in this sandbox (no internet
to install it), so nothing here was executed against a real server.** Every
change was hand-checked against the existing code conventions, field names,
and URL names using static analysis (syntax compile, template `{% url %}` /
`{% extends %}` / `{% include %}` cross-referenced against every `urls.py`
and every file on disk). No missing views, no dangling template references,
no missing files were found anywhere in the project as of this pass.

## What I found still missing from "every printable document, one identity"

Registration/OPD, Billing, Pharmacy, Laboratory, Radiology, and Appointment
receipts already shared `static/css/print_unified.css` (logo left, barcode
upper-right, one-page A4, Print/Download PDF/Download JPG). **Admission,
Operation Theatre, and Insurance did not have a printable document at all**
- these are new in this pass:

- `operation_theatre/models.py` - added `Surgery.barcode` (was the only one
  of the three missing a barcode field entirely) + migration
  `0003_surgery_barcode.py`, following the exact same `_generate_barcode()`
  pattern already used by `Admission` and `InsuranceClaim`.
- `templates/admissions/admission_slip.html` + `admissions:admission_slip`
  URL/view - printable Admission Slip, linked from Admission Detail.
- `templates/operation_theatre/surgery_slip.html` +
  `operation_theatre:surgery_slip` URL/view - printable OT Slip, linked
  from Surgery Detail.
- `templates/insurance/claim_slip.html` + `insurance:claim_slip` URL/view -
  printable Insurance Claim Slip, linked from both the patient's claim list
  and the claim review page.

All three use the identical `tuh-print-wrapper` / header / barcode-upper-
right / footer markup as every other document, so the whole system (10/10
document types from the original list) now shares one printed identity.

## Named bugs re-checked this pass

Went through the specific list again (Hospital Services, Nursing/Vitals,
Admission, Export Excel, Back buttons, Hospital Settings, Revenue Dashboard)
line by line against the current code:

- **Hospital Services, Nursing dashboard, Vitals, Admission** - all present
  and wired correctly (these were the Checkpoint 3 additions; they exist
  now). No missing views/URLs/templates found for any of them.
- **Export Excel** - every report's `?export=excel` link works; confirmed
  `reports/excel_utils.py` streams a real `.xlsx`. Only `registration_report`
  has date filters to preserve on export, and it already does.
- **Back buttons** - already solid: `document.referrer` host-check +
  `window.history.back()`, falling back to home if there's no same-site
  referrer (e.g. arriving from an external link or a fresh tab).
- **Hospital Settings** - already fully wired: `website/context_processors.py`
  reads the live `HospitalSetting` singleton (not a hardcoded settings.py
  value) for name/logo/address/phone/etc., so saving the form actually
  changes the name/logo/contact info everywhere immediately.
- **Revenue Dashboard** - genuinely fixed this pass. It was already
  responsive (`calc(1.1rem + 1vw)` + `word-break: break-all` on every
  figure, so large numbers can't overflow their card). But the cards
  always computed and showed totals on first load ("All Time" by default)
  instead of staying blank until a filter was applied, per spec. Changed
  `reports/views.py::revenue_dashboard` to only compute figures when
  `date_filter` is actually present in the querystring, and the template
  now shows a "Select a date filter above and click Apply" placeholder
  otherwise.

## Still open (unchanged from Pass 3's list)

- Patient portal auth rework + permission scoping
- Payment system architecture (Cash default + eSewa/Khalti/PhonePe/etc.)
- Notification system polish
- AI Assistant redesign + public-website-only placement
- SQLite/MySQL/PostgreSQL env-based config
- Demo data reseed (10 connected patients) + demo account documentation
- Migrations for this pass (`operation_theatre/migrations/0003_surgery_barcode.py`)
  are unverified the same way Checkpoint 3's were - run
  `python manage.py makemigrations --check` first thing after `pip install`
  to confirm nothing else is out of sync, then `migrate`.
