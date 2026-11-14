# M85 acceptance evidence index — 2026-11-15 KST

Scope: R07/R21/R25/R26/R29. Public-safe repository evidence only; no private customer proof, signatures or legal attestations. No partial points.

## Latest exact-SHA rerun — 2026-11-15 KST

At docs-only SHA `ac5f6cf`, the Windows full suite had one failure in the hardlink regression (`ValueError not raised`); the same-size test write depended on an immediately observable OS timestamp. Test-only commit `61b9ecab976518d28b732395f8ac3e1d40f9c5bf` pins a distinct mtime and asserts changed bytes/time. Exact-SHA Python/browser #43615731394, macOS #43615731344, CodeQL #43615731368 and final gate #43615731598 all succeeded. Windows: 525/525 PASS; Ubuntu/macOS: 524 PASS + 1 Windows-only SKIP; hardlink regression did not skip. The final gate remains `UNASSESSED`; official score is still 72/100. GPT-6 High found no actionable issue; the regression does not prove detection of a metadata-preserving stealth write and is not an independent R29 audit.

| Requirement | Public-safe evidence ID | Technical evidence at exact tested SHA `61b9ecab976518d28b732395f8ac3e1d40f9c5bf` | Missing acceptance evidence | Status |
|---|---|---|---|---|
| R07 (2) | D2W-M85-R07-OWNER-001 | P00/P03 Python/browser #43615731394; hosted Windows Tk single/batch consent reset and Chrome/Edge/Chromium local-file flows PASS. A07/A26 preflight direct 24/24 on Windows/Ubuntu/macOS. | Actual source authority and customer-specific use/share/transform permission and consent | MISSING_OWNER |
| R21 (4) | D2W-M85-R21-RIGHTS-001 | At the tested SHA, `r21_source_provenance.py` verified six pinned source producers; `shipping_rights_preflight.py` verified four synthetic shipped artifacts. | Commercial redistribution rights, actual authorship/third-party chain, authorized LICENSE/NOTICE decision | MISSING_OWNER |
| R25 (2) | D2W-M85-R25-OPS-001 | Blank source/result/no-copy custody form; direct retention tests 19/19 PASS on Windows/Ubuntu/macOS. Prior seven owner-approved policies and synthetic disposal drill are retained. | Actual customer/operator custody, retention, return/deletion trace and acceptance of real practice | INCOMPLETE_OWNER |
| R26 (2) | D2W-M85-R26-PRIVACY-001 | V2 privacy matrix; preflight tests 24/24 PASS on Windows/Ubuntu/macOS; hosted UI consent-reset flows PASS. | Customer-specific processing scope, lawful basis and informed consent | MISSING_OWNER |
| R29 (3) | D2W-M85-R29-EXTERNAL-001 | Internal `security_audit_preaudit.py` 7/7 PASS on Windows/Ubuntu/macOS; 525-test suite includes corrupt CRC, duplicate ZIP member and hardlink-alias mutation regressions; CodeQL #43615731368 SUCCESS; High review found no actionable issue. | Independent external audit, dated findings, remediation evidence, independent retest and signoff | MISSING_EXTERNAL |

## Fixed score and exact-SHA Actions

The scorecard remains 33 requirements / 100, 22 VERIFIED = 72, 11 PENDING = 28; target 85 is 13 short. Score increase: **0**. Historical weighting and evidence baseline remain unchanged.

- [Python/browser #43615731394](https://github.com/hibi89/data2web_studio/actions/runs/43615731394) SUCCESS at `61b9ecab976518d28b732395f8ac3e1d40f9c5bf`: Windows 525/525 PASS; Ubuntu 524 PASS + 1 Windows-only SKIP. Direct P00 11/11, P01 15/15, A25 19/19, A26 24/24 and internal preaudit 7/7 PASS; Chrome/Edge/Chromium and Tk flows PASS.
- [macOS offline #43615731344](https://github.com/hibi89/data2web_studio/actions/runs/43615731344) SUCCESS: 524 PASS + 1 Windows-only SKIP; direct P00 11/11, P01 15/15, A25 19/19, A26 24/24, preaudit 7/7; Chromium/file URL/A4 and hardlink regression PASS.
- [CodeQL #43615731368](https://github.com/hibi89/data2web_studio/actions/runs/43615731368) SUCCESS.
- [Final blueprint gate #43615731598](https://github.com/hibi89/data2web_studio/actions/runs/43615731598) SUCCESS, but the report says `UNASSESSED`, no approved evidence manifest and no official score.

- `zero_cost_gate.py`: spend 0 KRW, verified score 72, RELEASE HOLD/SALE NO-GO.
- `r21_source_provenance.py`: six source pins pass, commercial rights/NOTICE remain pending.
- `shipping_rights_preflight.py`: four synthetic artifacts pass integrity only; owner rights, commercial release and external audit are false.
- GPT-6 High review of `61b9ecab` found no actionable issue. Review is internal, not R29 external audit.

PR #4 remains Draft/Open/Unmerged. `[작업중]`, RELEASE HOLD / SALE NO-GO. Hosted checks do not establish actual customer rights, buyer Windows 10/11 acceptance or independent audit. R25’s seven policy approvals and synthetic test are retained; no repeat request is made.