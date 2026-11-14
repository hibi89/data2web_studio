# M85 acceptance evidence index — 2026-11-15 KST

Scope: R07/R21/R25/R26/R29. Public-safe repository evidence only; no private customer proof, signatures or legal attestations. No partial points.

## Latest exact-SHA rerun — 2026-11-15 KST

At exact code/test SHA `512af5000658f40ed7deefae096f29b886bd1ec0`, [Python/browser #43617898725](https://github.com/hibi89/data2web_studio/actions/runs/43617898725) passed: Windows 525/525; Ubuntu 524 PASS + 1 Windows-only SKIP; hosted Chromium plus installed Chrome/Edge and Tk flows succeeded. [macOS offline #43617898816](https://github.com/hibi89/data2web_studio/actions/runs/43617898816) passed 524 + 1 Windows-only SKIP. [CodeQL #43617898719](https://github.com/hibi89/data2web_studio/actions/runs/43617898719) passed with no new alert; [evidence gate #43617898943](https://github.com/hibi89/data2web_studio/actions/runs/43617898943) succeeded.

Product code commit `3a6d758` uses a Windows read handle that denies concurrent write/delete sharing through the bounded snapshot and final identity check. The follow-up test commit `512af500` corrected platform-specific test assumptions; both affected Windows regressions and the full suite passed at the exact SHA. GPT-6 High review found no actionable code issue.

Internal test/code review scope only. This does not prove directory ancestry race protection, buyer Windows 10/11 acceptance or independent R29 review. The fixed score remains 72/100, 22 VERIFIED / 11 PENDING, score addition 0. OWNER/EXTERNAL proofs for R07, R21, R25, R26 and independent audit/findings/retest for R29 remain missing; G85 remains blocked.

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