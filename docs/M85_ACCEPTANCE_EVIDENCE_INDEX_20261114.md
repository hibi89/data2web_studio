# M85 acceptance evidence index — 2026-11-15 KST

Scope: R07/R21/R25/R26/R29. Public-safe repository evidence only; no private customer proof, signatures or legal attestations. No partial points.

| Requirement | Public-safe evidence ID | Technical evidence at exact tested SHA `e42b570eae7aadbb21e5c93ae4664cc567f0dfba` | Missing acceptance evidence | Status |
|---|---|---|---|---|
| R07 (2) | D2W-M85-R07-OWNER-001 | P00/P03 Python/browser #43613095734; hosted Windows Tk single/batch consent reset and Chrome/Edge/Chromium local-file flows PASS. A07/A26 preflight direct 24/24 on Windows/Ubuntu/macOS. | Actual source authority and customer-specific use/share/transform permission and consent | MISSING_OWNER |
| R21 (4) | D2W-M85-R21-RIGHTS-001 | At the tested SHA, `r21_source_provenance.py` verified six pinned source producers; `shipping_rights_preflight.py` verified four synthetic shipped artifacts. | Commercial redistribution rights, actual authorship/third-party chain, authorized LICENSE/NOTICE decision | MISSING_OWNER |
| R25 (2) | D2W-M85-R25-OPS-001 | Blank source/result/no-copy custody form; direct retention tests 19/19 PASS on Windows/Ubuntu/macOS. Prior seven owner-approved policies and synthetic disposal drill are retained. | Actual customer/operator custody, retention, return/deletion trace and acceptance of real practice | INCOMPLETE_OWNER |
| R26 (2) | D2W-M85-R26-PRIVACY-001 | V2 privacy matrix; preflight tests 24/24 PASS on Windows/Ubuntu/macOS; hosted UI consent-reset flows PASS. | Customer-specific processing scope, lawful basis and informed consent | MISSING_OWNER |
| R29 (3) | D2W-M85-R29-EXTERNAL-001 | `security_audit_preaudit.py` 7/7 synthetic checks PASS on Windows/Ubuntu/macOS; 524-test full suite covers corrupt CRC and duplicate ZIP member regressions; CodeQL #43613095750 SUCCESS; High review closed the test assertion finding. | Independent external audit of exact source, dated findings, remediation evidence, independent retest and signoff | MISSING_EXTERNAL |

## Fixed score and exact-SHA Actions

The scorecard remains 33 requirements / 100, 22 VERIFIED = 72, 11 PENDING = 28; target 85 is 13 short. Score increase: **0**. Historical weighting and evidence baseline remain unchanged.

- [Python/browser #43613095734](https://github.com/hibi89/data2web_studio/actions/runs/43613095734) SUCCESS at `e42b570eae7aadbb21e5c93ae4664cc567f0dfba`: Windows 524/524 PASS; Ubuntu 523 PASS + 1 Windows-only SKIP. The two new ZIP tests and internal preaudit PASS; hosted Chrome/Edge/Chromium and Tk flows PASS.
- [macOS offline #43613095675](https://github.com/hibi89/data2web_studio/actions/runs/43613095675) SUCCESS: 523 PASS + 1 Windows-only SKIP; P00 11/11, P01 15/15, A25 19/19, A26 24/24, preaudit 7/7, offline Chromium/file URL/A4 and both new ZIP regressions PASS.
- [CodeQL #43613095750](https://github.com/hibi89/data2web_studio/actions/runs/43613095750) SUCCESS.
- [Final blueprint gate #43613096103](https://github.com/hibi89/data2web_studio/actions/runs/43613096103) SUCCESS, but the report says `UNASSESSED`, no approved evidence manifest and no official score.

- `zero_cost_gate.py`: spend 0 KRW, verified score 72, RELEASE HOLD/SALE NO-GO.
- `r21_source_provenance.py`: six source pins pass, commercial rights/NOTICE remain pending.
- `shipping_rights_preflight.py`: four synthetic artifacts pass integrity only; owner rights, commercial release and external audit are false.
- GPT-6 High review found the mismatched test assertion in intermediate SHA `e2664bae4bf3e4904b29a1e4861a46e0ab5f1dee`; `e42b570` corrected the expected message, and follow-up review found no remaining issue. This is internal review, not R29 external audit.

PR #4 remains Draft/Open/Unmerged. `[작업중]`, RELEASE HOLD / SALE NO-GO. Hosted checks do not establish actual customer rights, buyer Windows 10/11 acceptance or independent audit. R25’s seven policy approvals and synthetic test are retained; no repeat request is made.