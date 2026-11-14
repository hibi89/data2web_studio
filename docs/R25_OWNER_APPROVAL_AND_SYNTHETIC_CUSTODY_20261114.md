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
- [ ] Create a new temporary directory on an authorized local device, containing only a clearly marked synthetic text file (no actual customer information).
- [ ] Record creation UTC timestamp and a SHA-256 digest of synthetic bytes in a private log. No absolute paths or identifiers in public GitHub.
- [ ] Record operator custody and completion of the synthetic purpose. Validate the seven-day deadline using `operator_copy_retention.py` with anonymous metadata.
- [ ] Inspect the synthetic target and ensure it is **not** a customer original, backup, shared folder, or another application's file.
- [ ] Authorized operator **manually** deletes only the synthetic temporary file. The application and this document never delete it.
- [ ] Independently check the target is absent, and retain dated verification evidence privately. Record evidence reference only (opaque token) in the public tracker.
- [ ] Independently review synthetic trace against R25 requirements, then separately decide whether R25 technical simulation is accepted. Do not certify real-customer custody/disposal.

## Status
- Owner policy approval: **APPROVED — in chat, 2026-11-14 KST**.
- Synthetic custody/disposal actual execution: **NOT YET EVIDENCED**.
- Real customer data authorization/consent: **NOT APPROVED**.
- Independent real-world disposal confirmation: **NOT EVIDENCED**.
- R25 item: **PENDING**; official score **72/100**, RELEASE HOLD.
