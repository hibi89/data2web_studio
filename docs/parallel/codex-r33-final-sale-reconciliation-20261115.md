# R33 final delivery, platform receipt, and sale-process reconciliation — 2026-11-15

## Purpose

This checklist prepares a human to reconcile an actual authorized order with its approved rights, delivery, and refund evidence. It does not create an order, payment, refund, platform listing, commercial license, customer acceptance, or release decision. Synthetic tests and GitHub files are never substituted for a real transaction.

## Per-order evidence packet

A designated owner must reconcile each row from the actual authorized records before any sale is accepted. Use redacted references and hashes in technical notes; keep private customer documents in the authorized owner-controlled system, not in this public repository or CI.

| Gate | Required evidence | Technical cross-check | Missing evidence state |
|---|---|---|---|
| Customer and source authority (R07/R26) | Actual per-customer use/processing permission, data categories, plaintext notice and approved route | Confirm consent is bound to the exact source digest and recipient/context; inspect the fresh output receipt | OWNER/EXTERNAL_PENDING |
| Shipped asset rights (R21) | Rights-holder approval and required third-party LICENSE/NOTICE scope | Compare the approved inventory to the exact shipped HTML/ZIP/verifier contract; no fabricated license | OWNER_PENDING |
| Retention operation (R25) | Actual operator custody, retention end, authorized manual deletion record, or legal exception | Reconcile the local operator log to the named copy set without uploading its paths or contents | OWNER_PENDING |
| Sale terms (R27) | Final SKU, price, scope, revision/support terms, platform fees and tax/merchant handling | Cross-check approved contract/listing text against the frozen internal SKU defaults | OWNER_PENDING |
| Independent buyer acceptance (R23/R30) | Real authorized customer/examiner device run and acceptance tied to exact source SHA | Review request ZIP SHA, actual device/browser labels, core E2E checklist and output receipt/ZIP hashes | EXTERNAL_PENDING |
| Security (R29) | Independent human audit report, remediation evidence, and auditor retest | Compare audit target SHA and finding closure to exact source diff | EXTERNAL_PENDING |
| Native distribution (R32) | Owner-approved scope, reproducible runtime/package, target-device/install or portable run, rights and signing evidence where applicable | Rebuild independently and compare complete bundle manifest/member hashes | OWNER/EXTERNAL_PENDING |
| Order, payment, delivery and consumer remedies (R33) | Actual platform order/transaction receipt, agreed order terms, delivered artifact hashes, buyer receipt, cancellation/refund record where applicable | Match the order reference to delivery ZIP SHA256 and `receipt.json`; retain platform evidence under owner policy | OWNER/EXTERNAL_PENDING |

## Integrity receipt versus commercial receipt

DATA2WEB `receipt.json` and SHA256 values establish only technical integrity for specific bytes. They do not establish identity, payment, contract acceptance, source rights, sale authorization, delivery acknowledgement, consumer-law compliance, or a refund. A marketplace receipt/order record is a separate external artifact and must not be imitated with a local JSON file.

## Safe closeout sequence

1. Start with a genuine platform order and an already approved internal/external rights and terms packet. If any gate is missing, mark HOLD and do not receive or process customer source files.
2. Capture the exact source Git commit SHA and the hash of each authorized delivery artifact; compare the delivered folder using the independent verifier.
3. Reconcile any cancellation/refund in the actual platform system and preserve its resulting record; do not initiate payments or refunds from this checklist.
4. Have the designated human reviewer check the unredacted evidence in its authorized location. Write only redacted result state, evidence kind/reference, and hashes in technical worklog.
5. Keep missing rights, payment, customer acceptance, refund, tax/platform review, or independent audit marked OWNER_PENDING or EXTERNAL_PENDING. Never mark GO from synthetic evidence or a self-report.

## Current state

No real marketplace listing, customer order, payment, delivery acknowledgement, or refund transaction has been recorded by this technical work. R33 remains pending. RELEASE HOLD / SALE NO-GO. No customer or personal data was transmitted to GitHub or CI.
