# M85 acceptance evidence index — 2026-11-14 KST

Scope: R07/R21/R25/R26/R29. This index contains no customer content, private locations, signatures, or legal attestations. Status labels reflect repository evidence only; none awards score.

| Requirement | Public-safe evidence ID | Technical evidence available | Missing acceptance evidence | Status |
|---|---|---|---|---|
| R07 (2) | D2W-M85-R07-OWNER-001 | `order_intake_preflight.py`; synthetic source-preservation tests | Dated authorization for actual source, sharing/transform rights, specific customer consent | MISSING_OWNER |
| R21 (4) | D2W-M85-R21-RIGHTS-001 | `shipping_rights_preflight.py`, `r21_source_provenance.py`, `data/r21_source_provenance_v1.json` | Actual commercial redistribution rights, third-party licenses and applicable NOTICE decision | MISSING_OWNER |
| R25 (2) | D2W-M85-R25-OPS-001 | Local retention controls and synthetic retention checks described in STATUS | Owner-approved actual operating retention/disposal responsibility and real redacted execution records | INCOMPLETE_OWNER |
| R26 (2) | D2W-M85-R26-PRIVACY-001 | Synthetic data classification/preflight | Actual processing scope, lawful basis and specific informed customer consent | MISSING_OWNER |
| R29 (3) | D2W-M85-R29-EXTERNAL-001 | CodeQL and synthetic security regressions on functional SHA `1be21c6a3f4ba2426c93a71201d96e274ce22ee7` | Independent external security audit, findings/remediation and independent retest | MISSING_EXTERNAL |

Baseline: 33 requirements, weights total 100, 22 VERIFIED = 72 points, 11 PENDING = 28 points. No partial task awards. Latest documented HEAD before this file: `ef6ba6c00e4aef7febca5b0a86568729d2b8252d`. Functional CI baseline (not rerun here): Windows 507 PASS; Ubuntu 506 PASS/1 SKIP; browser PASS; CodeQL SUCCESS. PR #4 remains draft/unmerged pending live recheck.

Next technical work: A07-01, A21-01, A25-01, A26-01, A29-01. Real owner/external evidence must remain private; only opaque reference and independent review status may be committed. RELEASE HOLD / SALE NO-GO.
