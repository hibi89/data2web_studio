# P01 / A07-01 — rollback boundary and source-custody review (2026-11-14 KST)

## P01: non-destructive recovery and protected surfaces
- Latest pre-review documentation commit: `7137dccb9036b68b0a8a778734774281a1ceb6ce`.
- Last functionally verified commit: `1be21c6a3f4ba2426c93a71201d96e274ce22ee7`. Preserve as a recovery *reference*, not an instruction to force-reset history.
- Earlier independent upstream reference: `hibi89/REA_Web@7b6b68111efd906f9d929b5e2f577699b26399ee` (read-only golden comparison); do not merge or overwrite.
- Protected surfaces: `main`, REA_Web upstream branches, all customer original files and prior delivery folders, existing LICENSE/NOTICE, existing output receipts, Git history and repo permissions. Create-only outputs only; no customer materials in GitHub.
- GitHub connector commit metadata on `7137dcc...` reports author and committer login `hibi89`; actual email fields were unavailable. No credential or billing changes made.
- Previous functional CI results are historical: hosted Windows 507 PASS, Ubuntu 506 PASS / 1 SKIP, browser jobs PASS, CodeQL PASS, score gate PASS, as documented in HANDOFF. Current-turn CI rerun: **NOT PERFORMED**. Workflow-run query for exact SHA returned an empty subset, so it is not evidence of a failure or of a new success.

## A07-01: source and rights boundary
| Step | Source / custody | Potential disclosure or mutation | Existing safeguard | Residual acceptance gap |
|---|---|---|---|---|
| Anonymous pre-order | Only whitelisted format/count/boolean metadata | Customer identifiers in free text | `order_intake_preflight.py` exact keys and types; unknown fields rejected; no customer file reads | Boolean `rights_claimed` is a customer assertion, not legal proof |
| Local intake | Customer-owned source in owner-authorized local workflow | PII and third-party secrets | `docs/A_CUSTOMER_INTAKE_AND_DELIVERY_QA_DRAFT_20261114.md` requires consent, HOLD for sensitive/unknown rights | No real dated customer/source-specific permission |
| Local inspect/transform | Approved local file, SHA and mapping | Changed source, unauthorized sheet, plaintext copied into HTML | Existing approved SHA/mapping/validation and create-only output design (historical synthetic CI) | Real source byte-for-byte before/after evidence and buyer review missing |
| Delivery ZIP/receipt | New customer folder, standalone HTML, ZIP, receipt | Plaintext embedded in HTML; unauthorized distribution | `verify-customer` and `sale_approved:false` per intake guide; R21 source provenance pinning | Rights to redistribute actual data and producer assets unconfirmed |
| Retention/return | Operator local copy (if created) | Over-retention or accidental deletion | Manual maximum-7-day policy described in AGENTS; no automatic customer file deletion | Real custody log, return/destruction authorization and proof missing |

### Static code observations
- `order_intake_preflight.py` uses exact anonymous metadata schema, validates booleans strictly, and returns `order_accepted:false`, `sale_approved:false`, `customer_rights_independently_verified:false`.
- `write_new_report` uses exclusive creation and rejects existing report paths. These are code observations, **not a fresh runtime test**.
- The intake guide explicitly states that `index.html` may contain original plaintext, requires customer acknowledgment, and prohibits uploading real customer files to GitHub/AI.
- No confirmed source mutation or missing guard was reproduced in this static review; do not change stable production code without a failing case.
- Required follow-up: A07-02 private blank rights checklist; A07-03 synthetic CLI/desktop consent reset regression; A07-04 actual owner/customer permission (BLOCKED_OWNER); A07-05 final item review after real evidence.

**Disposition:** P01 read-only recovery boundary documented. A07-01 static technical dataflow reviewed; runtime validation and real authorization remain unverified. R07 remains PENDING, official score 72/100, RELEASE HOLD.
