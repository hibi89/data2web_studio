# M85 acceptance evidence index — 2026-11-15 KST

Scope: R07/R21/R25/R26/R29. Public-safe repository evidence only; no private customer proof, signatures or legal attestations. No partial points.

| Requirement | Public-safe evidence ID | Technical evidence at exact tested SHA `d3aef514f0847b9f05789ad0e9eb4acf6b503105` | Missing acceptance evidence | Status |
|---|---|---|---|---|
| R07 (2) | D2W-M85-R07-OWNER-001 | P00/P03 Actions #43611527779: full Windows 522/522, Ubuntu 521 PASS + 1 Windows-only SKIP; hosted Tk single/batch consent reset and Chrome/Edge/Chromium local-file flows PASS. A07/A26 preflight direct 24/24 on Windows/Ubuntu/macOS. | Actual source authority and customer-specific use/share/transform permission and consent | MISSING_OWNER |
| R21 (4) | D2W-M85-R21-RIGHTS-001 | At `d3aef514f0847b9f05789ad0e9eb4acf6b503105`, `r21_source_provenance.py` verified six pinned source producers; `shipping_rights_preflight.py` verified four synthetic shipped artifacts. | Commercial redistribution rights, actual authorship/third-party chain, authorized LICENSE/NOTICE decision | MISSING_OWNER |
| R25 (2) | D2W-M85-R25-OPS-001 | Blank source/result/no-copy custody form; direct retention tests 19/19 PASS on Windows/Ubuntu/macOS. Prior seven owner-approved policies and synthetic disposal drill are retained. | Actual customer/operator custody, retention, return/deletion trace and acceptance of real practice | INCOMPLETE_OWNER |
| R26 (2) | D2W-M85-R26-PRIVACY-001 | V2 privacy matrix; preflight tests 24/24 PASS on Windows/Ubuntu/macOS; hosted UI consent-reset flows PASS. | Customer-specific processing scope, lawful basis and informed consent | MISSING_OWNER |
| R29 (3) | D2W-M85-R29-EXTERNAL-001 | `security_audit_preaudit.py` 7/7 synthetic checks PASS on Windows/Ubuntu/macOS; CodeQL #43611527768 SUCCESS; Python/browser #43611527779 and macOS #43611527786 SUCCESS; High reviewed the macOS path trigger and found no remaining issue. | Independent external audit of exact source, dated findings, remediation evidence, independent retest and signoff | MISSING_EXTERNAL |

## Fixed score and exact-SHA Actions

The scorecard remains 33 requirements / 100, 22 VERIFIED = 72, 11 PENDING = 28; target 85 is 13 short. Score increase: **0**. Historical weighting and evidence baseline remain unchanged.

- [Python/browser #43611527779](https://github.com/hibi89/data2web_studio/actions/runs/43611527779) SUCCESS at `d3aef514f0847b9f05789ad0e9eb4acf6b503105`: Windows 522/522 PASS; Ubuntu 522 run, 521 PASS + 1 Windows-only SKIP. P00 11/11, P01 15/15, A25 19/19, A26 24/24 and R29 preaudit 7/7 PASS; hosted Chrome/Edge, Chromium, Tk single/batch and file:// flows PASS.
- [macOS offline #43611527786](https://github.com/hibi89/data2web_studio/actions/runs/43611527786) SUCCESS: full suite 521 PASS + 1 Windows-only SKIP; direct P00 11/11, P01 15/15, A25 19/19, A26 24/24 and preaudit 7/7 PASS; offline Chromium/file URL/A4 PASS.
- [CodeQL #43611527768](https://github.com/hibi89/data2web_studio/actions/runs/43611527768) SUCCESS.
- [Final blueprint gate #43611527971](https://github.com/hibi89/data2web_studio/actions/runs/43611527971) SUCCESS, but the log states no approved evidence manifest and no official score.

- `zero_cost_gate.py`: spend 0 KRW, verified score 72, RELEASE HOLD/SALE NO-GO.
- `r21_source_provenance.py`: six source pins pass, commercial rights/NOTICE remain pending.
- `shipping_rights_preflight.py`: four synthetic artifacts pass integrity only; owner rights, commercial release and external audit are false.
- Final gate reports no approved evidence manifest and no official score.
- GPT-6 High identified a P3 macOS path-filter gap at `26367ab01d4fcbd727698c3392705ee02238608d`; `d3aef514f0847b9f05789ad0e9eb4acf6b503105` adds `data/**`. Follow-up review found the gap closed and no further finding. This is internal workflow review, not R29 external audit.

PR #4 remains Draft/Open/Unmerged. `[작업중]`, RELEASE HOLD / SALE NO-GO. Hosted checks do not establish actual customer rights, buyer Windows 10/11 acceptance or independent audit. R25’s seven policy approvals and synthetic test are retained; no repeat request is made.
