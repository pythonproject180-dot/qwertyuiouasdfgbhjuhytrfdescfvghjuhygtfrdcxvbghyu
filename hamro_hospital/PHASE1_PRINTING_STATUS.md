# Phase 1 — Printing & Document Design: Status

## What I verified was already in good shape
The uploaded project already had a polished, on-brand implementation of:
- `templates/patients/opd_ticket.html`
- `templates/patients/patient_card.html`
- `templates/billing/receipt.html`
- The new hospital logo (`static/images/hospital_logo.png`) was already applied everywhere via `HOSPITAL_LOGO_URL`.

These closely matched the reference images you attached (they appear to be
screenshots taken directly from this system).

## What was genuinely broken / inconsistent, and what I fixed

1. **Pharmacy, Laboratory, Radiology, and Appointment receipts** were plain,
   unbranded stub templates with no logo, no shared header/footer, and no
   barcode grouping. Rewrote all four to match the OPD ticket / invoice
   design language:
   - `templates/pharmacy/receipt.html`
   - `templates/laboratory/report_print.html`
   - `templates/radiology/report_print.html`
   - `templates/appointments/receipt.html`

2. **New shared stylesheet** — `static/css/print_unified.css` — holds the
   common header (logo + name + address), barcode/QR-in-header-right block,
   title banner, metadata rows, results table, and footer used by the four
   documents above, so the whole system shares one visual identity as
   requested. All print rules force a single A4 page
   (`page-break-inside: avoid`, no forced second page).

3. **Print vs. Download PDF vs. Download JPG mismatch** — previously the
   billing invoice's "Download PDF" button called a hand-coded ReportLab
   canvas that looked nothing like the styled HTML receipt (no barcode
   placement, no table styling, no logo layout) — this was the literal bug
   you described ("PDF downloaded and printed version must look identical").
   Fixed by adding:
   - `static/js/print_tools.js` — captures the on-screen document at 3x
     resolution and exports it as either a PDF sized exactly to the content
     (always one page, no blank space) or a high-resolution JPG.
   - `templates/includes/print_actions.html` — a shared Back / Print /
     Download PDF / Download JPG action bar.
   - Wired into: OPD ticket, patient ID card, billing invoice, and all four
     newly redesigned receipts. Every printable document now offers all
     three actions, and print/PDF/JPG are guaranteed identical because
     they all render from the same DOM.
   - The old ReportLab `billing:invoice_pdf` view is left in place as a
     lightweight fallback URL, but is no longer the primary download path.

4. **Patient ID Card — Sticker version.** Added a "PVC Card / Sticker"
   toggle on the card page. Both share the exact same layout/data as
   requested; the sticker variant uses square-cut corners (typical for
   die-cut label stock) instead of the rounded PVC-card corners.

5. **Navbar logo** — increased from 50px to 64px and added breathing room
   (`templates/base.html`, `static/css/style.css`) since it was reported
   as too small.

## Not yet touched (still open from your original instructions)
Everything outside "Printing & Document Design" is untouched in this pass:
- Patient portal authentication rework (self-service signup/password, forgot
  password, permission scoping)
- Appointment workflow routing rules
- Registration Counter dashboard features/search
- Department-based patient search permissions
- Payment system (Cash default + eSewa/Khalti/PhonePe/etc. architecture)
- Notification system
- AI Assistant redesign + public-website-only placement
- The specific named bugs (Hospital Services page error, Nursing Dashboard
  404s, Vitals page, Admission page, Export Excel, Back buttons, Hospital
  Settings, Revenue Dashboard responsiveness/date-filter behavior)
- SQLite/MySQL/PostgreSQL env-based config
- Demo data reseed (10 connected patients) + demo account documentation

## Suggested next step
Given the size of the remaining scope, the sane order (roughly matching
your own priority list) is:
1. Fix the named broken pages/bugs (quick, high-value, unblocks testing)
2. Patient portal auth + permissions
3. Payment system architecture
4. Notifications + AI Assistant
5. Demo data + accounts + DB config, as a final pass once everything above
   is stable enough to seed data against

Tell me which of these you want next and I'll pick up from there.
