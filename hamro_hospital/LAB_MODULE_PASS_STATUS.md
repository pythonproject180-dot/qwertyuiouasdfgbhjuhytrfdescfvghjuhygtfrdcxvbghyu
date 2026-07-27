# Laboratory Module Rebuild - Batch 1 (Part 2, section 5)

Same limitation as prior passes: no internet in this sandbox, so Django
itself can't be installed/run here. Everything below was hand-checked
(syntax-compiled, every {% url %}/field/import cross-referenced against
disk) but not executed against a live server. Run
`python manage.py makemigrations --check` right after install.

## What changed, step by step

1. `consultations/models.py` - `RequestStatus` expanded from 3 to 5 stages
   (Pending -> Accepted -> Sample Collected -> Testing In Progress ->
   Completed), matching spec 5's dashboard queues exactly.
2. `LabTestRequest.consultation` made nullable; added `patient` (direct FK),
   `is_manual`, `referred_by`, `department_name`, `clinical_note`,
   `referral_letter`, `accepted_at`, `accepted_by` - so a walk-in patient
   with a physical referral can get a record with no doctor-side request.
3. Added `patient_obj` / `doctor_display` / `department_display`
   properties so every template/view works identically whether the
   record came from a doctor's electronic request or was opened manually.
4. `consultations/migrations/0006_labtestrequest_walkin_fields.py` - hand-
   written migration for all of the above (unverified, same caveat as
   every migration in this project so far).
5. `laboratory/forms.py` - `ManualLabRequestForm` (new walk-in form) added
   alongside the existing `LabResultForm`.
6. `laboratory/views.py` - added `search_patient` (large search box: ID/
   QR/phone/name), `manual_create` (opens a walk-in record, auto-Accepted),
   `accept_request` (Accept Request button - acknowledgement only, no
   billing/clinical-note access). `update_result` now accepts multiple
   files (`request.FILES.getlist('report_files')`) and pushes each one
   into `documents.PatientDocument` (category=Laboratory Report), which is
   what already fans out to Medical History / Doctor Dashboard / Patient
   Portal / Super Admin - so no separate sync code was needed there.
7. `laboratory/urls.py` - added `search/`, `patient/<id>/new/`,
   `<pk>/accept/`.
8. Templates rebuilt: `dashboard.html` (search box + QR scanner + all 5
   queue counts + Recent Uploaded Reports panel), `queue.html` (Accept
   button + collapsible referral/clinical-note review row), new
   `search_patient.html` + `manual_create.html`, `update_result.html`
   (shows referral letter + doctor + multi-file input),
   `report_print.html` fixed to use `patient_obj`/`department_display` so
   walk-in reports print correctly.
9. `medical_records/views.py` and `patient_portal/views.py` - the lab
   query in each was `consultation__visit__patient=patient`, which would
   have silently hidden every walk-in record from the EMR timeline and
   the Patient Portal. Both now also match on the direct `patient` FK.
10. `static/css/style.css` - added the `badge-blue-soft` / `-orange-soft`
    / `-green-soft` / `-secondary-soft` pill variants the new status
    badges use (only danger/success/warning existed before).

## Still not done (next batches, in order)

- Laboratory permissions lock-down (no print history / no billing access -
  currently relies on `@laboratory_required` only, needs an explicit
  view-level check against the "CANNOT" list in spec 5).
- Laboratory Counter payment (separate from Cashier, lab-only billing).
- Radiology module - same rebuild as Laboratory (spec 6), not started.
- Cashier central payment authority + unified payment methods (spec 7).
- Nursing, Admission/IPD, OT, Blood Bank, Insurance, Accounts (spec 9-14).
- Patient ID Card download restriction to Registration + Super Admin only
  (spec 20) - not touched yet.
- Full role-based access matrix pass (spec 21).

Tell me to keep going and I'll do Radiology next (it mirrors Laboratory
closely, so it'll go faster), then Cashier + EMR permissions.

---

# Batch 2 - Radiology Module (Part 2, section 6)

Radiology rebuilt as a mirror of Laboratory batch 1, same 8-step pattern:

1. `RadiologyRequest.consultation` made nullable, added `patient` (direct
   FK), `is_manual`, `referred_by`, `department_name`, `clinical_note`,
   `referral_letter`, `accepted_at`, `accepted_by`, plus `patient_obj` /
   `doctor_display` / `department_display` properties - identical shape to
   `LabTestRequest`.
2. `consultations/migrations/0007_radiologyrequest_walkin_fields.py` -
   hand-written, same caveats as migration 0006.
3. `radiology/forms.py` - added `ManualRadiologyRequestForm`; the existing
   `RadiologyReportForm` no longer takes `report_file`/`image_file`
   directly (those fields stay on the model for backward compatibility,
   but new uploads go through the same multi-file path as Laboratory).
4. `radiology/views.py` - added `search_patient`, `manual_create`,
   `accept_request`; `update_report` now takes multiple files via
   `request.FILES.getlist('report_files')` and pushes each into
   `documents.PatientDocument` (category=Radiology Report), which is what
   already fans out to every module that needs to see it.
5. `radiology/urls.py` - added `search/`, `patient/<id>/new/`,
   `<pk>/accept/`, matching Laboratory's URL shape exactly.
6. Templates rebuilt: `dashboard.html` (search box + QR scanner + Pending/
   Accepted/Imaging Queue/Completed counts + Recent Uploaded Reports),
   `queue.html` (Accept button + referral review row), new
   `search_patient.html` + `manual_create.html`, `update_report.html`
   (referral + doctor + multi-file input), `report_print.html` fixed to
   use `patient_obj`/`department_display`.
7. Found and fixed the same "walk-in records go missing" bug in **four**
   places this time (Laboratory batch 1 only needed two): `patients/views.py`
   `patient_section` (powers the Laboratory/Radiology tabs on a patient's
   profile page), `medical_records/views.py`, `patient_portal/views.py`,
   and `reports/views.py::laboratory_report`'s Excel export (this one
   would have hard-crashed on `AttributeError: 'NoneType' object has no
   attribute 'visit'` the first time a Super Admin exported the Laboratory
   report after any walk-in record existed - caught it by grep, not by
   running it, since nothing here can actually run Django yet).
8. `billing/views.py`'s pending-lab/pending-radiology queries were left
   untouched on purpose: those feed the OPD billing queue for
   doctor-raised requests specifically, and walk-in records are billed
   through the Laboratory/Radiology Counter (spec 5/7), not OPD billing.

## Still open (updated)

- Laboratory/Radiology permissions lock-down (the "CANNOT" list - no
  print history, no billing access) - still relies on the role decorator
  alone.
- Laboratory Counter / Radiology billing split from Cashier.
- Cashier module (spec 7) - not started.
- Nursing, Admission/IPD, OT, Blood Bank, Insurance, Accounts (spec 9-14).
- Patient ID Card download lock to Registration + Super Admin only
  (spec 20).
- Full role-based access matrix pass (spec 21).

Next batch: Cashier (spec 7) - central payment authority, unified receipt
layout, and the Laboratory Counter / Radiology Counter split that both
modules above now assume exists.

---

# Batch 3 - Cashier Module (Part 2, section 7)

Unlike Laboratory/Radiology, the Cashier module (`billing` app) was already
substantially built in earlier passes - central `Bill`/`BillItem` model,
10 payment methods, refund/discount approval workflow, barcode+QR receipt.
This batch closed the specific gaps against spec section 7 rather than
rebuilding it.

1. `billing/models.py` - `PaymentMethod.OTHER` added (spec 7 lists Cash/
   eSewa/Card/Insurance/Bank Transfer/Other explicitly; only "Other" was
   missing). Added `BillType.RADIOLOGY` (previously Radiology bills had no
   distinct type). Added `Bill.counter_name` and
   `Bill.insurance_coverage_amount` fields, plus `discount_total` /
   `final_amount_paid` properties - computed from the existing
   `DiscountRequest` approval trail, never touching `total_amount` itself
   (keeps the audit-safe pattern already in place for refunds/discounts).
2. `billing/migrations/0005_bill_counter_insurance_coverage.py` - hand-
   written, same caveats as every migration so far.
3. `billing/forms.py` - `BillPaymentForm` gained `counter_name` and
   `insurance_coverage_amount` (both optional, so existing bill-creation
   flows can't silently break if a template isn't updated).
4. `templates/billing/receipt.html` - added the fields spec 7's Receipt
   Format list required that weren't there at all before: **Phone Number**
   (now shown, compulsory per spec), **Counter Name**, Discount line,
   Insurance Coverage line, **Final Amount Paid**. "Prepared By" is now
   paired with Counter so the receipt reads "Counter - Staff Name" in one
   place instead of two disconnected labels. Amount-in-words now reflects
   `final_amount_paid`, not the pre-discount total.
5. **Laboratory Counter / Radiology Counter** (spec 5 & 6 both call for
   this, spec 7 confirms it): added `accounts.decorators.billing_counter_
   required`, and `billing.views.create_bill` now detects when a
   Laboratory or Radiology staff member (not Cashier/Super Admin) is
   billing, and force-restricts them to only their own department's
   pending items - `services`, `pending_visits`, `pending_surgeries` (and
   the other department's pending list) are all emptied server-side, not
   just hidden in the template, and `counter_name`/`bill_type` are forced
   rather than trusted from the POST body. `create_bill.html` now shows a
   clear "You are billing as the Laboratory/Radiology Counter" banner
   instead of the full service catalogue when restricted. Added "Collect
   Payment" buttons to both modules' `search_patient.html`.
6. Fixed a **workflow conflict** the Laboratory/Radiology batches
   introduced: `create_bill` used to jump a paid request straight to
   `IN_PROGRESS`, skipping the new `ACCEPTED` stage entirely (so a request
   paid via Cashier would never show as "Accepted" even though someone at
   the counter had clearly processed it). Payment now sets `ACCEPTED` +
   `accepted_at`/`accepted_by` if not already set, keeping the Pending ->
   Accepted -> Sample Collection -> In Progress -> Completed pipeline
   intact regardless of which door (Accept button vs. payment) it came in
   through.
7. Also fixed the walk-in Q()-filter bug in `create_bill`'s pending-lab/
   pending-radiology queries (same class of bug as batch 2, item 7) -
   doesn't currently change behavior since walk-in records skip straight
   to Accepted and never hit this REQUESTED-only query, but keeps the
   query correct if that ever changes.

## Still open (updated)

- Blood Bank Bill / Blood Bank billing integration (spec 12) - `BillType`
  has no Blood Bank option yet; will add when Blood Bank module is built.
- Nursing, Admission/IPD, OT, Blood Bank, Insurance, Accounts (spec 9-14) -
  none started except what Admission/OT/Insurance already had from prior
  passes (see PASS4_STATUS.md for that history).
- Patient ID Card download lock to Registration + Super Admin only
  (spec 20).
- Full role-based access matrix pass (spec 21).
- `billing/views.py::edit_bill` (bill correction before payment settles)
  wasn't touched this batch - not reviewed against spec 7 in detail yet.

Next batch: Medical Records / EMR central hub pass (spec 8) - the
walk-in-record sync work in batches 1-2 already covers most of the "every
upload becomes part of the permanent record" requirement, so this will
focus on the expandable-timeline UI and the permission matrix
(Doctor/Nursing/OT/Blood Bank/Patient upload-vs-view-vs-delete rules).

---

# Batch 4 - Medical Records / EMR Central Hub (Part 2, section 8)

1. `documents/models.py` - added soft-delete (`is_deleted`, `deleted_by`,
   `deleted_at` + `soft_delete()`). Reuses the existing `is_active` flag
   as the single "visible" switch, so every current `is_active=True`
   query across the whole project (document lists, EMR, patient portal)
   automatically hides a deleted document without those views needing to
   change - only the deletion path itself is new.
2. `documents/migrations/0002_patientdocument_soft_delete.py`.
3. **Permission split that didn't exist before**: `documents/views.py` had
   one `document_download` view open to `@any_staff_required` - i.e.
   every department could silently download every file, which is the
   opposite of spec 8's "Only Patients and Super Admin may download
   files. Other authorized users may view only." Split into:
   - `document_view` (any authorized staff, inline `Content-Disposition`
     so it opens in-browser instead of prompting Save As - the "built-in
     viewer" spec 8 asks for)
   - `document_download` (now `Role.SUPER_ADMIN` only)
   - `document_delete` (new - `Role.SUPER_ADMIN` only, soft delete,
     confirmation page, audited)
4. Added `AuditLog.Action.DOCUMENT_DELETED` (was going to reuse
   `DOCUMENT_REPLACED` for the log line, decided that would misreport
   what happened in the audit trail - added a proper action instead).
   Migration `accounts/migrations/0004_auditlog_document_deleted_action.py`.
5. `templates/documents/document_list.html` - View button for everyone,
   Download/Delete buttons only rendered for Super Admin.
   `templates/medical_records/patient_full_record.html` - its documents
   section was still linking to the now-locked-down `document_download`,
   which would have 403'd for the Medical Records role the moment this
   batch shipped (Medical Records isn't Super Admin) - switched to
   `document_view`. Every section (OPD, Admission, Surgery, Lab,
   Radiology, Prescriptions, Billing, Documents) is now a native
   `<details>` block so it's expandable/collapsible with zero JS, per
   spec 8's "Each section should be expandable."
6. **Patient-side gap found**: `patient_portal` had no route to the
   `documents.PatientDocument` uploads at all - "My Lab Reports" /
   "My Radiology Reports" only ever showed the legacy single
   `result_file` field on `LabTestRequest`/`RadiologyRequest`. That means
   every multi-file upload added in batches 1-2 was invisible to the
   patient who's supposed to be able to download it (spec 8 & 19). Added
   `patient_portal.views.my_documents` / `my_document_download` (scoped
   to `request.portal_patient.patient` only - `PatientAccount` isn't a
   staff `accounts.User`, so it can't reuse the staff-side view/download
   split), a new "My Documents" nav item, and `my_documents.html`.
7. Fixed the walk-in Q()-filter bug a third time, this round in
   `patient_portal.views.my_lab_report_detail` /
   `my_radiology_report_detail` - these used
   `get_object_or_404(..., consultation__visit__patient=patient)`, which
   would 404 for any walk-in record the moment a patient clicked into it
   from their own portal.

## Still open (updated)

- Medical Records upload-per-department buttons on the EMR page itself
  (spec 8 "Every authorized department should have: Write Note / Upload
  PDF ... Save to Medical History" directly inside the record view) -
  currently the EMR page links out to the shared `documents:document_
  upload` screen rather than embedding per-section upload forms; the
  shared screen covers the requirement functionally but not the exact
  in-page layout spec 8 describes.
- Ownership-level lock on "Doctor cannot edit/delete records created by
  others" - `document_replace` is still open to any authorized role
  regardless of who uploaded the original; only deletion is Super-Admin-
  gated so far.
- Nursing, Admission/IPD, OT, Blood Bank, Insurance, Accounts (spec
  9-14) - Nursing is next.
- Patient ID Card download lock to Registration + Super Admin only
  (spec 20).
- Full role-based access matrix pass (spec 21).

Next batch: Nursing Dashboard (spec 9) - assigned patients, today's
admissions/discharges, nursing notes/vitals/MAR, upload PDF/scanned docs,
no billing access.

---

# Batch 5 - Nursing Dashboard (Part 3, section 9)

1. `nursing/models.py` - `NursingNote.NoteType` gained `PROGRESS` and
   `OBSERVATION` (spec 9 lists Nursing Notes/Vital Signs/Progress Notes/
   Observation Notes/Medication Administration Notes as five distinct
   types; only four existed, Progress and Observation were both missing -
   General Note was covering for both).
2. `nursing/migrations/0002_nursingnote_progress_observation.py`.
3. `documents/models.py` - added `DocumentCategory.NURSING_NOTE` (nursing
   uploads were going to land under generic "Other" otherwise, which
   would've made them hard to filter out of a patient's document list -
   spec 18 lists Nursing Notes as its own EMR timeline category).
   `documents/migrations/0003_patientdocument_nursing_category.py`.
4. `nursing/views.py` - dashboard rebuilt: search box + QR scanner (same
   `_qr_scanner.html` partial Lab/Radiology/Registration all share),
   Today's Admissions / Today's Discharges counts, and a genuine "Pending
   Nursing Notes" count (admitted patients with zero note recorded today)
   with its own list section on the dashboard. New `search_patient` view/
   template (Patient ID/QR/Phone/Name). `admission_notes` now accepts
   multiple files via `request.FILES.getlist('attachment_files')`,
   pushed into `documents.PatientDocument` the same way every other
   department's uploads work, so nursing notes' attachments sync to the
   EMR/Doctor Dashboard/Patient Portal automatically.
5. `templates/nursing/admission_notes.html` - added the file input and a
   list of previously uploaded nursing documents (linking to the shared
   `documents:document_view` built-in viewer from batch 4, not a raw
   download link).

## One limitation flagged, not fixed this batch

"My Assigned Patients" in spec 9 implies a nurse sees *their own*
patients, not the whole ward. There's no per-nurse assignment model in
this project (admissions aren't assigned to a specific nurse anywhere),
so the dashboard currently shows every currently-admitted patient instead
- functionally usable for a single-ward or small-hospital deployment, but
not what the spec literally describes for a multi-nurse floor. Flagging
rather than inventing an assignment system without being asked, since
that's a real data-model decision (per-shift? per-ward? per-bed-range?)
that affects Admission/Ward too, not just Nursing.

## Still open (updated)

- Admission/IPD, OT, Blood Bank, Insurance, Accounts (spec 10-14) -
  Admission is next; large parts of it already existed pre-batch (see
  PASS4_STATUS.md), so that pass will focus on gaps against spec 10
  specifically rather than a rebuild.
- Patient ID Card download lock to Registration + Super Admin only
  (spec 20).
- Full role-based access matrix pass (spec 21).
- Nurse-to-patient assignment model (see limitation above) - flagged for
  a future batch if wanted, not started.

Next batch: Admission (IPD) - spec 10.

---

# Batch 6 - Admission / IPD (Part 3, section 10)

Admission was already the most complete module in the project going into
this batch - admission numbering, bed allocation with auto-occupy/free,
discharge with condition/summary/follow-up, admission slip, and (unique
to this module) a working "doctor recommends admission during
consultation -> shows up as a pending admission" pipeline that spec 10
describes almost exactly. This batch closed the remaining dashboard/
permission gaps rather than rebuilding anything.

1. **Real permission bug found**: every admissions template's sidebar
   links to "Wards & Beds", but `ward_list` was `@super_admin_required`.
   Ward/Admission staff - the role this entire module exists for - would
   click their own sidebar link and get refused. Changed `ward_list` to
   `admissions_staff_required` (Super Admin, Registration, Doctor, Ward/
   Admission); `ward_create`/`bed_create` stay Super-Admin-only, and the
   "Add Ward"/"Add Bed" buttons on the page are now only rendered for
   Super Admin so non-admin staff see a clean read-only Bed
   Allocation / Ward Information view (spec 10 dashboard item) instead of
   buttons that would 403.
2. Added `admissions:search_patient` (Patient ID/QR/Phone/Name + QR
   scanner, same shared `_qr_scanner.html` partial as every other module)
   - replaces the sidebar's link out to the generic `patients:patient_
   search`, matching the pattern from Lab/Radiology/Nursing.
3. Added a **Discharge Queue** section to the Admission dashboard (spec
   10 explicitly lists this) - currently-admitted patients, oldest
   admission first, with a direct Discharge action. Interpreted
   pragmatically as "currently admitted, oldest first" since there's no
   separate "cleared for discharge" status in the data model to filter
   on - flagging this interpretation rather than inventing a new status
   without being asked.

## Gap found, not fixed this batch

`admission_detail.html` has a "Bill IPD Charges" button pointing at
`billing:create_bill`. That view requires Cashier/Laboratory/Radiology/
Super Admin (see batch 3's `billing_counter_required`) - **Ward/Admission
staff were never in that list**, before or after this batch's changes.
So the button is visible to Admission staff but will 403 for anyone in
that role who isn't also Cash Counter. This predates this batch (it was
`@cash_counter_required`-only before too), but spec 10's workflow
("Admission staff assigns Ward/Bed -> Generate Admission Bill") reads as
if Admission staff should be able to do this themselves, which conflicts
with spec 7's "Cashier is the central payment authority." Flagging the
conflict rather than picking a side unilaterally - happy to either add
Admission staff to `billing_counter_required` (mirroring the Lab/
Radiology Counter pattern from batch 3) or leave it Cashier-only and
remove/relabel the button, whichever matches the intended workflow.

## Still open (updated)

- Operation Theatre, Blood Bank, Insurance, Accounts (spec 11-14).
- Patient ID Card download lock to Registration + Super Admin only
  (spec 20).
- Full role-based access matrix pass (spec 21).
- The Admission-vs-Cashier billing permission conflict noted above.

Next batch: Operation Theatre - spec 11.

---

# Batch 7 - Operation Theatre (Part 3, section 11)

OT already had the doctor-schedules-surgery workflow, its own barcode-
numbered Surgery record, a printable OT slip, and patient search with QR
scan built in. The one real gap: **no document upload existed anywhere
in the module** - every field was text-only (pre_op_notes, operative_
notes, post_op_notes), so spec 11's "Upload PDF / Upload Scanned Consent
Form" (at scheduling) and "Upload Operative Report / Surgical Notes /
Procedure Summary / Scanned Documents" (at completion) had nothing behind
them.

1. `operation_theatre/views.py::surgery_schedule` now accepts multiple
   files via `request.FILES.getlist('consent_files')`, saved as
   `documents.PatientDocument` (category = Consent Form).
2. `surgery_detail` now accepts multiple files via `request.FILES.
   getlist('operative_files')` on the same "Update Operative Record" form
   (category = Operation / Surgery Record), and lists everything already
   uploaded for that surgery underneath it.
3. Dashboard gained a "Recent Uploaded Documents" panel (consent forms +
   operative reports), matching the Lab/Radiology/Nursing dashboards.
4. Added a "Full Patient History" link on the surgery detail page
   alongside the existing "Patient Documents" link, covering spec 11's
   "OT can view Medical History / Laboratory Reports / Radiology Reports
   / Blood Bank History" permission via the same shared, already-built
   views rather than duplicating report browsers inside OT itself.
5. Both templates switched to `enctype="multipart/form-data"` (required
   for file inputs to actually submit - easy to miss, would have silently
   dropped every file with no error).

## Same billing-permission conflict as batch 6, noted not re-litigated

`surgery_detail.html`'s "Bill Surgery" button points at `billing:create_
bill`, which OT staff can't access (not in `billing_counter_required`,
same as Ward/Admission staff in batch 6). Not fixing unilaterally here
either - it's the same open question about whether department staff
should have their own billing counter or strictly hand off to Cashier.

## Still open (updated)

- Blood Bank, Insurance, Accounts (spec 12-14).
- Patient ID Card download lock to Registration + Super Admin only
  (spec 20).
- Full role-based access matrix pass (spec 21).
- The Admission/OT-vs-Cashier billing permission conflict (batches 6 & 7).

Next batch: Blood Bank - spec 12.

---

# Batch 8 - Blood Bank (Part 3, section 12)

Blood Bank had a solid inventory model (bag numbering, expiry tracking,
stock-by-group) and a direct issue flow, but the actual spec 12 workflow
- "Doctor requests blood -> Blood Bank receives request -> Blood Bank
issues blood -> Upload Issue Report" - didn't exist. Issuing only ever
happened by Blood Bank staff searching a patient directly; there was no
request step, and nothing to upload.

1. New `BloodRequest` model (patient, optional consultation link,
   blood group/component/units needed, urgency, clinical note, status
   Pending/Issued/Cancelled, `requested_by`). `BloodIssue` gained
   `blood_request` (OneToOne, links an issue back to the request it
   fulfilled) and `issue_report` (FileField - spec 12's "Upload Issue
   Report" step).
2. `blood_bank/migrations/0002_bloodrequest_and_issue_report.py`.
3. Added `DocumentCategory.BLOOD_ISSUE_REPORT` and `BillType.BLOOD_BANK`
   (the latter was explicitly flagged as deferred back in batch 3's
   status notes - now that the module exists, added it). Migrations
   `documents/migrations/0004_...` and `billing/migrations/0006_...`.
4. Added `AuditLog.Action.BLOOD_REQUESTED` (was about to reuse
   `BLOOD_ISSUED` for a request log line, same reasoning as batch 4's
   `DOCUMENT_DELETED` decision - a request and an issue are different
   events and the audit trail should say which one happened). Migration
   `accounts/migrations/0005_...`.
5. `blood_bank/views.py`:
   - `doctor_patient_lookup` + `doctor_request_create` - new doctor-side
     entry point (`@doctor_required`), linked from the Doctor Dashboard
     sidebar as "Request Blood Bank". This is a standalone screen, not an
     inline formset on the consultation form the way Lab/Radiology
     requests work - flagged below, not worth the risk of touching the
     consultation form's formset handling blind in this batch.
   - `request_queue` - Blood Bank's own pending/issued/cancelled list.
   - `dashboard` - added Pending Requests count + list, each request
     linking straight into `issue_blood` pre-attached to that request.
   - `issue_blood` now accepts an optional `request_id`, marks the
     originating `BloodRequest` Issued, accepts an `issue_report` file,
     and pushes it into `documents.PatientDocument` the same way every
     other department's uploads do.
6. **Gap found while wiring this up**: no module anywhere let Nursing/OT
   staff (both of whom spec 9 & 11 explicitly grant "View Blood Bank
   History" to) actually see a patient's blood bank history -
   `patients.views.patient_section` had no `blood_bank` branch at all.
   Added one, following the exact `section_map` / `allowed_roles_for_
   section` / template pattern already used for Laboratory and Radiology
   sections - same role list (Super Admin, Blood Bank, Doctor, Ward/
   Admission, Nursing, OT), new `blood_bank/_patient_blood_history.html`
   partial, new tab on `patient_detail.html` and every section sidebar.

## Flagged, not built this batch

Doctor's blood request is a separate standalone page, not embedded in the
consultation form's inline formset the way Lab/Radiology requests are
(spec 17 groups "Request Blood Bank" alongside those as one of the
doctor's request actions). Functionally equivalent - the request still
reaches Blood Bank immediately - but the doctor has to leave the
consultation screen to use it, rather than checking a box inline. Wiring
it into the consultation formset directly is a reasonable follow-up if
wanted, just riskier to do blind without seeing that view's full formset
handling in this pass.

## Still open (updated)

- Insurance, Accounts (spec 13-14).
- Patient ID Card download lock to Registration + Super Admin only
  (spec 20).
- Full role-based access matrix pass (spec 21).
- Admission/OT-vs-Cashier billing permission conflict (batches 6 & 7) -
  Blood Bank doesn't have this problem since it has no separate counter,
  Cashier already covers it per spec 7's list.
- Doctor blood-request-as-inline-formset (see above).

Next batch: Insurance - spec 13.
