# A07-02 — per-order source rights and plaintext disclosure checklist (blank template)

**Status:** TEMPLATE ONLY; no customer approval, rights verification, acceptance score, or permission to collect real data. Use in an authorized private/local channel only. Never commit a completed customer form or customer identifiers to GitHub. Related preflight: `order_intake_preflight.py`; reference: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`.

## Order-specific rights and custody questions (all require explicit answers)
| ID | Confirmation required | Answer | Evidence retained privately |
|---|---|---|---|
| R07-C01 | The actual source provider and lawful data owner have been identified and their authority checked, including joint owners | UNANSWERED | Private dated authorization reference |
| R07-C02 | Provider may lawfully give the specified dataset to the operator for the specified transformation | UNANSWERED | Private authorization reference |
| R07-C03 | Third-party copyright, database rights, contract confidentiality and downstream sharing restrictions have been separately checked | UNANSWERED | Private third-party clearance reference |
| R07-C04 | Exact approved formats, sheets, headers, columns, output audience and transformation purpose are specified | UNANSWERED | Private scoped instructions |
| R07-C05 | Data subjects' privacy permissions/lawful basis and special-category handling have been checked; no unsupported sensitive content is sent | UNANSWERED | Private privacy review reference |
| R07-C06 | Customer acknowledges standalone HTML/ZIP can expose source values in plaintext and can be copied or forwarded | UNANSWERED | Private acknowledgment reference |
| R07-C07 | Permitted delivery channel, recipient, sharing/redistribution boundaries and revocation/cancellation procedure are explicit | UNANSWERED | Private agreement reference |
| R07-C08 | Source owner retains original; operator uses only approved local copies; retention/return/destruction authority and deadlines are agreed | UNANSWERED | Private custody reference |
| R07-C09 | New source, sheet, header, ID mapping, recipient, intended use or changed permissions triggers a new review, not inherited approval | UNANSWERED | Private change-approval reference |
| R07-C10 | Dated customer and operator confirmation is obtained before any actual source processing or delivery | UNANSWERED | Private approval reference |

## Machine-independent decision procedure
1. Start with `HOLD`. Collect only anonymous format/size/count metadata in the preflight. `rights_claimed:true` is a self-report, never independent proof.
2. For any unanswered/negative/unclear C01–C10, conflicting permission, special-category data, or unclear third-party rights, stay `HOLD`; do not ingest, transmit, transform, or distribute actual customer content.
3. If authorization is later verified privately, record an opaque evidence ID, consent scope and date in a private controlled record. No names, signatures, paths, raw rows or evidence documents in the repo.
4. At actual processing, verify approved source SHA before and after read-only operation; any mismatch or changed sheet/header/ID mapping returns to `HOLD` for renewed scope authorization.
5. Keep `sale_approved:false` and `RELEASE HOLD` until **all** separate R07/R21/R25/R26/R29 and launch gates pass. This template never changes the scorecard.

## Revocation and changed-scope triggers
- Rights-holder withdraws or narrows permission; third-party restriction discovered; data subject/contract restrictions change.
- Input file or hash changes, sheet/header/ID mapping changes, plaintext output gains unapproved fields, or output recipient/channel changes.
- Retention period expires, unauthorized copy discovered, or custody/access boundary changes.

On trigger: stop new processing/delivery, preserve legal hold records if applicable, isolate existing authorized copies without unilateral deletion, request new specific authorization and document a private resolution. Do not silently reuse a prior boolean or erase customer originals.

**Acceptance:** A07-02 template preparation only. R07 remains PENDING, 0/2 new points. Next A07-03 inspect consent reset paths and reproduce failures using synthetic tests.
