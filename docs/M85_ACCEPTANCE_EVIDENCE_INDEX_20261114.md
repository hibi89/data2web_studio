# M85 acceptance evidence index — 2026-11-15 KST

Scope: R07/R21/R25/R26/R29. Public-safe repository evidence only; no private customer proof, signatures or legal attestations. No partial points.

| Requirement | Public-safe evidence ID | Technical evidence at exact tested SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661` | Missing acceptance evidence | Status |
|---|---|---|---|---|
| R07 (2) | D2W-M85-R07-OWNER-001 | Python/browser #43609470587 SUCCESS: full 522-test Windows suite, Ubuntu 521 PASS + 1 Windows-only SKIP; hosted Tk single/batch consent reset and Chrome/Edge/Chromium local-file flows PASS. Preflight V2 requires explicit privacy class. | Actual source rights/authority and specific customer use, sharing and transformation consent | MISSING_OWNER |
| R21 (4) | D2W-M85-R21-RIGHTS-001 | Python/browser #43609470587 ran `r21_source_provenance.py`: six producer blobs pinned; `shipping_rights_preflight.py`: four synthetic shipping artifacts integrity verified. | Commercial redistribution rights, actual authorship/third-party chain, and authorized LICENSE/NOTICE decision | MISSING_OWNER |
| R25 (2) | D2W-M85-R25-OPS-001 | Blank source/result/no-copy custody form; direct `test_operator_copy_retention` 19/19 PASS on Windows/Ubuntu/macOS at exact SHA. Existing seven owner-approved policies and synthetic drill remain recorded. | Actual customer/operator custody, retention, return/deletion trace and acceptance of real practice | INCOMPLETE_OWNER |
| R26 (2) | D2W-M85-R26-PRIVACY-001 | Privacy V2 matrix and fail-closed classes; direct `test_order_intake_preflight` 24/24 PASS on Windows/Ubuntu/macOS; hosted consent-reset UI/browser flows PASS. | Customer-specific processing scope, lawful basis and informed consent | MISSING_OWNER |
| R29 (3) | D2W-M85-R29-EXTERNAL-001 | `security_audit_preaudit.py` 7/7 synthetic checks PASS on Windows/Ubuntu/macOS; CodeQL #43609470563 SUCCESS; Python/browser #43609470587 and macOS #43609470565 SUCCESS; High internal follow-up found no actionable workflow issue. | Independent external audit of exact source, dated findings, remediation evidence, independent retest and signoff | MISSING_EXTERNAL |

## Fixed score and exact-SHA Actions

Scorecard remains 33 requirements, denominator 100, 22 VERIFIED = 72, 11 PENDING = 28; target 85 is 13 short. Official score increase this cycle: **0**. The historical scorecard baseline remains unchanged.

- [Python/browser #43609470587](https://github.com/hibi89/data2web_studio/actions/runs/43609470587) — SUCCESS at `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`; Windows full suite 522/522, Ubuntu 521 PASS + 1 Windows-only SKIP; direct A25 19/19 and A26 24/24; 7/7 synthetic preaudit; Chrome/Edge/Chromium and hosted Tk flows PASS.
- [macOS offline #43609470565](https://github.com/hibi89/data2web_studio/actions/runs/43609470565) — SUCCESS at `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`; full suite 521 PASS + 1 Windows-only SKIP; direct A25 19/19, A26 24/24, preaudit 7/7; offline Chromium/file URL/A4 PASS.
- [CodeQL #43609470563](https://github.com/hibi89/data2web_studio/actions/runs/43609470563) — SUCCESS.
- [Final blueprint gate #43609470850](https://github.com/hibi89/data2web_studio/actions/runs/43609470850) — SUCCESS; log states no approved evidence manifest and no official score.
- Zero-cost check: spend 0 KRW, 72 points, RELEASE HOLD/SALE NO-GO. R21 source pins 6/6 and four synthetic artifacts are technical integrity only; owner rights, third-party notices and external audit remain false/pending.

PR #4 remains Draft/Open/Unmerged. `[작업중]`, RELEASE HOLD / SALE NO-GO. Hosted/internal checks do not establish customer legal acceptance, buyer-device acceptance or independent audit. R25’s prior owner-approved policies and synthetic drill are retained and are not being requested again.
