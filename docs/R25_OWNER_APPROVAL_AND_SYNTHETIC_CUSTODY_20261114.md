# DATA2WEB R25 — owner authorization and synthetic custody drill

## Owner authorization (2026-11-14 KST, in-chat explicit approval)
The product owner explicitly approved these seven operational defaults and appointed themselves as accountable operator:
1. Product owner is the operator responsible for temporary customer copies.
2. Never modify or delete customer originals without separate authorization.
3. Operator-held temporary customer copies: at most 7 days, manually dispose earlier once purpose is complete.
4. Check legal retention exceptions separately and keep their evidence separate.
5. Customer-by-customer rights and privacy consent remain mandatory and unapproved.
6. Mark disposal complete only after actual deletion and record verification.
7. Synthetic evidence never substitutes for real customer handling approval.

**Scope:** internal zero-cost synthetic testing only. No customer data, sale, release, cloud upload, auto-delete, or exception to existing hold. The owner approved policy, **not** actual disposal or acceptance evidence.

## Synthetic drill checklist — evidence is pending until executed
- [x] Isolated assistant container: synthetic-only temporary text file created (not owner local device).
- [x] UTC timestamp and synthetic-content SHA-256 recorded below, no absolute paths.
- [ ] Record operator custody and completion of the synthetic purpose. Validate the seven-day deadline using `operator_copy_retention.py` with anonymous metadata.
- [ ] Inspect the synthetic target and ensure it is **not** a customer original, backup, shared folder, or another application's file.
- [x] Assistant explicitly removed its own synthetic-only temporary file, not a customer file or application auto-delete.
- [x] Post-deletion absence checked in assistant container; independent external witness **not** obtained.
- [ ] Independently review synthetic trace against R25 requirements, then separately decide whether R25 technical simulation is accepted. Do not certify real-customer custody/disposal.

## Status
- Owner policy approval: **APPROVED — in chat, 2026-11-14 KST**.
- Synthetic assistant-container disposal drill: **PASS, not real customer custody evidence**.
- Real customer data authorization/consent: **NOT APPROVED**.
- Independent real-world disposal confirmation: **NOT EVIDENCED**.
- R25 item: **PENDING**; official score **72/100**, RELEASE HOLD.

## Executed synthetic drill — isolated assistant container (2026-11-14 UTC)
- Scope: one newly created, known synthetic-only temporary text file in an isolated temporary directory; **not** user's Windows PC or any real customer environment.
- UTC creation/hash check: `2026-11-14T13:36:15.499709+00:00`.
- Synthetic content SHA-256: `90ea32ae87f8ab7f8c868ed436cd634dc159ed99f4bebce6a7c22441f901e9ea`.
- Explicitly scoped manual deletion step: removed only that newly created synthetic file with `Path.unlink()`, not via the product or an automated retention sweep.
- Post-action absence check: **PASS** at `2026-11-14T13:36:15.499782+00:00`; original bytes verified before deletion. Temporary directory cleaned.
- No customer source read; no external transmission, customer deletion, or production execution. This is a synthetic *technical* demonstration only, not an independently witnessed operator/customer custody trace.
- R25 owner approval recorded, synthetic drill PASS, real-customer custody and independent acceptance still PENDING. Official score **72/100**; RELEASE HOLD.


## Owner risk-control instruction (2026-11-14 KST)
The owner reiterated that preventing unlawful handling and avoiding personal legal exposure is the highest priority. Treat this as a **risk-control instruction**, not a waiver, a legal compliance certification, permission to process customer data, or proof of disposal. Preserve fail-closed customer intake, no unauthorized deletion, no automatic source purge, customer-specific rights and privacy review, statutory exception checks, and RELEASE HOLD until independently evidenced acceptance. Legal obligations vary by data, contract, jurisdiction, and record type; seven days is an internal temporary-copy default only.


## 2026-11-14 23:47 KST — R25 report consistency fix and exact-SHA regression
- Independent internal review identified that a forged overdue sensitive/rights-pending report could set `manual_disposal_action_due=false`. No customer disposal or policy approval was involved; existing seven owner-approved rules remain unchanged.
- Result JSON is now contract `DATA2WEB_OPERATOR_COPY_RETENTION_RESULT_V2`, carrying explicit `purpose_completed_claimed` and `legal_retention_exception_claimed` booleans. The validator recomputes the action flag from copy presence, due time, purpose completion, and exception claim; a legal exception remains manual-evidence HOLD and suppresses the flag by design.
- Exact-SHA tests [#43606247844](https://github.com/hibi89/data2web_studio/actions/runs/43606247844) and [macOS #43606247722](https://github.com/hibi89/data2web_studio/actions/runs/43606247722) passed. This validates internal report consistency only; it is not evidence of actual customer custody or disposal. R25 remains PENDING, official 72/100, RELEASE HOLD.
