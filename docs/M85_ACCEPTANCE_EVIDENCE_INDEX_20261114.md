# M85 acceptance evidence index — 2026-11-15 KST

Scope: R07/R21/R25/R26/R29. Public-safe repository evidence only; no private customer proof, signatures or legal attestations. No partial points.

| Requirement | Public-safe evidence ID | Technical evidence at latest tested SHA | Missing acceptance evidence | Status |
|---|---|---|---|---|
| R07 (2) | D2W-M85-R07-OWNER-001 | Exact SHA `4e6808b80023157cf9f849f600e18ed123e258e0`; 522-test suite and hosted Windows Tk single/batch consent-reset plus Chromium/Chrome/Edge local-file flows PASS | Actual source rights and specific customer consent | MISSING_OWNER |
| R21 (4) | D2W-M85-R21-RIGHTS-001 | Exact SHA #43608095426: 6/6 pinned producer blobs; four synthetic shipping artifacts verified against exact v1 allowlists | Commercial redistribution rights, authorship/third-party chain, LICENSE/NOTICE decision | MISSING_OWNER |
| R25 (2) | D2W-M85-R25-OPS-001 | A25-02 blank source/result/no-copy custody form; exact SHA `4e6808b80023157cf9f849f600e18ed123e258e0` full 522-test suite PASS across Win/Ubuntu/macOS including retention checks; seven owner-approved policies and synthetic drill retained | Real authorized custody/retention/disposal trace and independent acceptance of actual practice | INCOMPLETE_OWNER |
| R26 (2) | D2W-M85-R26-PRIVACY-001 | V2 explicit privacy class matrix and fail-closed negative tests on exact SHA `4e6808b80023157cf9f849f600e18ed123e258e0`; full 522-test suite PASS Win/Ubuntu/macOS; hosted Tk/browser flows pass | Customer-specific processing scope, lawful basis and informed consent | MISSING_OWNER |
| R29 (3) | D2W-M85-R29-EXTERNAL-001 | CodeQL #43608095464 SUCCESS; Python/browser #43608095426 all jobs SUCCESS; macOS #43608095412 SUCCESS; internal synthetic XSS/CSP/formula/ZIP/path regressions; High internal review no findings | Independent external audit, dated findings, remediation evidence and independent retest/signoff | MISSING_EXTERNAL |

Baseline remains 33 requirements, total 100, 22 VERIFIED = 72, 11 PENDING = 28; target 85 is 13 short. Fixed scorecard baseline is unchanged; latest tested code SHA is `4e6808b80023157cf9f849f600e18ed123e258e0`. Evidence: [Python/browser #43608095426](https://github.com/hibi89/data2web_studio/actions/runs/43608095426), [macOS #43608095412](https://github.com/hibi89/data2web_studio/actions/runs/43608095412), [CodeQL #43608095464](https://github.com/hibi89/data2web_studio/actions/runs/43608095464), [native preview #43608095408](https://github.com/hibi89/data2web_studio/actions/runs/43608095408), [final gate #43608095618](https://github.com/hibi89/data2web_studio/actions/runs/43608095618).

PR #4 remains Draft/Open/Unmerged. `[작업중]`, RELEASE HOLD / SALE NO-GO. Hosted/internal checks do not establish customer legal acceptance or independent audit.



The final gate run #43608095618 succeeded but its log states that there was no approved evidence manifest and no official score was awarded. The technical review does not change any R status. GPT-6 High read-only review of commit 4e6808b reported no actionable findings; this is not the R29 external audit.
