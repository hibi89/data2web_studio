## 2026-11-15 KST — exact SHA `320aebc23163019f85e1c345857ff4ed3da8147a`

- Windows native preview output-path fix is covered by [native preview #43644268111](https://github.com/hibi89/data2web_studio/actions/runs/43644268111) PASS. The synthetic manifest confirms the native Tk window appeared, customer PC is unverified, and sale is not approved. GPT-6 High source review found no actionable issue.
- [Python/browser #43644268104](https://github.com/hibi89/data2web_studio/actions/runs/43644268104) FAIL: Windows 531 tests (524 PASS, 5 ERROR, 1 FAIL, 1 SKIP); Ubuntu 531 (521 PASS, 5 ERROR, 1 FAIL, 4 SKIP). All six failures are the R21 source-provenance HOLD for four producer blob changes. Focused P00/P01, R25 retention, R26 preflight and R29 internal preaudit steps passed. Browser/Chromium and Windows Chrome/Edge/Tk jobs passed.
- [CodeQL #43644268143](https://github.com/hibi89/data2web_studio/actions/runs/43644268143) PASS. [Final gate #43644268362](https://github.com/hibi89/data2web_studio/actions/runs/43644268362) workflow PASS but report is `UNASSESSED`, with no approved evidence manifest. macOS was not run at this SHA.
- Score evidence and all five R packets remain unchanged: 72/100, 22 VERIFIED / 11 PENDING, zero points added. R21 pin reconciliation awaits authorized source review; R07/R21/R25/R26 acceptance evidence and independent R29 audit evidence remain incomplete. Existing R25 policy approvals and synthetic destruction drill remain accepted.

## 2026-11-15 KST — screenshot artifact path hardening at exact SHA `b3850cde8249ac39aae474326cbdb02274ad0fd1`

The synthetic Chromium preview now buffers each PNG and writes PNGs plus the evidence manifest using `secure_output.py` held-directory relative create. Exact-SHA [preview #43643553075](https://github.com/hibi89/data2web_studio/actions/runs/43643553075) passed, created three synthetic screenshots, and recorded zero remote requests and zero JS errors. The associated Chromium and Windows Chrome/Edge/Tk jobs passed; CodeQL passed. The Python/Ubuntu jobs still fail only on the previously documented R21 producer source-pin drift; no macOS job ran at this SHA. The final gate is `UNASSESSED`, no accepted manifest and score addition 0.

## 2026-11-15 KST — latest output-path hardening evidence at `92dca18`

The exact code/test revision is `92dca1824e24700dc38f8f9fa4ae3775488c2d3f`. New `secure_output.py` routes create-only output through verified directory handles; hosted Windows verifies ancestor rename denial and relative creation, while Ubuntu/macOS pass POSIX trusted-ancestry and relative-create regressions. The source-only GPT-6 High review found no actionable issue in these changes or test seams. Internal R29 preaudit reports all seven synthetic checks passing, but still says `INTERNAL_SYNTHETIC_ONLY_EXTERNAL_AUDIT_PENDING`.

Current Actions: Python/browser #43641997390 and macOS #43641997419 are **FAIL** because the R21 provenance guard rejects four changed producer blobs; browser, Windows Chrome/Edge/Tk, CodeQL #43641997418, synthetic preview #43641997407 and final gate #43641997648 succeeded. The gate itself reports `UNASSESSED`, with no approved manifest. Current exact suite logs show the output-race, A07 consent-reset, A25 retention, and A26 privacy/consent regressions pass; the R21 source pin tests fail closed.

The original `data/r21_source_provenance_v1.json` remains untouched. Four producer files now differ from their historic pins; see the latest R21 source evidence note. Therefore M85-E05's historic pin evidence does not verify the current producer source set and is now `INCOMPLETE`. No rights, customer acceptance, external audit, or points are inferred from this internal engineering work.

# M85 acceptance evidence index — 2026-11-15 KST

Scope: R07/R21/R25/R26/R29. Public-safe repository evidence only; no private customer proof, signatures or legal attestations. No partial points.

## Requirement-level evidence register — 2026-11-15 KST

Evidence IDs below are stable, non-identifying tracking references, not signatures or proof by themselves. `VERIFIED` means the linked artifact was checked for the narrow scope stated; `INCOMPLETE` means an available artifact does not cover the full item; `MISSING` means the required proof was not supplied through this public GitHub-only task. Every R07/R21/R25/R26/R29 item packet remains **INCOMPLETE** and receives no points.

| Requirement packet | Overall evidence state | Evidence IDs | Remaining acceptance proof |
|---|---|---|---|
| R07 | INCOMPLETE | M85-E01–E04 | Real source authority/consent and case-bound source integrity proof |
| R21 | INCOMPLETE | M85-E05–E07 | Commercial redistribution rights, NOTICE decision and authorized package verification |
| R25 | INCOMPLETE | M85-E08–E11 | Actual customer custody, retention, return/disposal records |
| R26 | INCOMPLETE | M85-E12–E13 | Customer-specific lawful basis, data scope and plaintext consent |
| R29 | INCOMPLETE | M85-E14–E18 | Approved independent evaluator, external report/findings, remediation retest and signoff |

| Evidence ID | Req. | Evidence or tracked proof slot | State | Source / scope limit |
|---|---|---|---|---|
| M85-E01 | R07 | Source-flow, no-upload, consent-reset and fail-closed technical controls | VERIFIED | `P01_A07_01_SOURCE_CUSTODY_REVIEW_20261114.md`, A07 consent regression, latest hosted CI; synthetic/technical scope only |
| M85-E02 | R07 | Per-order rights, shared-data, plaintext and privacy checklist template | VERIFIED | `A07_PER_ORDER_RIGHTS_CHECKLIST_20261114.md`; blank form, not customer assent |
| M85-E03 | R07 | Actual rightsholder/provider authority and scoped customer permission to use/transform/deliver a real source | MISSING | No customer or private legal proof supplied; the checklist cannot establish it |
| M85-E04 | R07 | Before/after source identity and bytes tied to an authorized real acceptance case | MISSING | No real source case or private hash record supplied |
| M85-E05 | R21 | Historic shipped asset inventory and producer blob pins | INCOMPLETE | At 92dca18 four producer blobs differ from the historic pin manifest; source-change review required; pin identity is not ownership or commercial rights |
| M85-E06 | R21 | Rightsholder chain, derivative-work rights, commercial redistribution license and third-party NOTICE obligations | MISSING | No actual rights instrument or approved NOTICE decision supplied |
| M85-E07 | R21 | Rights-driven LICENSE/NOTICE package decision and allowed/forbidden-member migration tests | MISSING | Depends on M85-E06; no license is invented or added |
| M85-E08 | R25 | Seven owner-approved internal policies and named operator record | VERIFIED | `R25_OWNER_APPROVAL_AND_SYNTHETIC_CUSTODY_20261114.md`; policy approval only |
| M85-E09 | R25 | Synthetic manual disposal drill and retention-report regression suite | VERIFIED | R25 record plus [latest hosted CI](https://github.com/hibi89/data2web_studio/actions/runs/43619050999); no customer custody asserted |
| M85-E10 | R25 | Blank source/result custody, expiry, return/disposal, legal-exception and no-copy record form | VERIFIED | `A25_02_COPY_CUSTODY_RECORD_TEMPLATE_20261115.md`; template only |
| M85-E11 | R25 | Actual customer source/result custody, retention notice, return or disposal trace and responsible-party evidence | MISSING | No customer handling record supplied; existing policy/drill do not replace it |
| M85-E12 | R26 | Privacy scope matrix, default HOLD and consent-reset/plaintext-warning technical flow | VERIFIED | `A26_01_PRIVACY_SCOPE_MATRIX_20261115.md`, hosted synthetic GUI/regression tests; not legal advice or customer consent |
| M85-E13 | R26 | Customer-specific data scope/access/retention basis and informed plaintext/use consent | MISSING | No customer-specific agreement or approved nonpersonal-only boundary supplied |
| M85-E14 | R29 | Synthetic attack matrix, direct-caller spoof/report-forgery defenses, path/ZIP/XLSX/CSP/network controls, and Windows source/output junction rejection | VERIFIED | `R29_SYNTHETIC_PREAUDIT_HANDOFF_20261114.md`, `test_order_intake_preflight.py`, `test_path_policy.py` at exact HEAD `c99f3d4`; author-run synthetic/hosted scope only, not independent audit or host-wide egress monitoring |
| M85-E15 | R29 | CodeQL scan and GPT-6 High internal read-only review at the pinned code/test SHA | VERIFIED | CodeQL and internal review only; neither is an independent external audit |
| M85-E16 | R29 | Owner approval of a genuinely independent evaluator, permitted scope and disclosure conditions | MISSING | No evaluator/scope approval or authorized external sharing record supplied |
| M85-E17 | R29 | Independent dated audit report with environment, commands, findings, severity and omissions at a frozen SHA | MISSING | No external report supplied; AI, Codex and CodeQL cannot create this evidence |
| M85-E18 | R29 | Independent retest after fixes and evaluator signoff/remaining-risk statement | MISSING | Depends on external findings and authorized retest; no signoff supplied |

These are evidence inventory states, not R-item completion states. The scorecard remains 72/100; weighting and release status are unchanged.

## Latest exact-SHA rerun — 2026-11-15 KST

At exact code/test SHA `512af5000658f40ed7deefae096f29b886bd1ec0`, [Python/browser #43617898725](https://github.com/hibi89/data2web_studio/actions/runs/43617898725) passed: Windows 525/525; Ubuntu 524 PASS + 1 Windows-only SKIP; hosted Chromium plus installed Chrome/Edge and Tk flows succeeded. [macOS offline #43617898816](https://github.com/hibi89/data2web_studio/actions/runs/43617898816) passed 524 + 1 Windows-only SKIP. [CodeQL #43617898719](https://github.com/hibi89/data2web_studio/actions/runs/43617898719) passed with no new alert; [evidence gate #43617898943](https://github.com/hibi89/data2web_studio/actions/runs/43617898943) succeeded.

Product code commit `3a6d758` uses a Windows read handle that denies concurrent write/delete sharing through the bounded snapshot and final identity check. The follow-up test commit `512af500` corrected platform-specific test assumptions; both affected Windows regressions and the full suite passed at the exact SHA. GPT-6 High review found no actionable code issue.

Internal test/code review scope only. This does not prove directory ancestry race protection, buyer Windows 10/11 acceptance or independent R29 review. The fixed score remains 72/100, 22 VERIFIED / 11 PENDING, score addition 0. OWNER/EXTERNAL proofs for R07, R21, R25, R26 and independent audit/findings/retest for R29 remain missing; G85 remains blocked.


### R29 direct-caller forgery coverage at exact PR HEAD

At `25dd273eb1903ab283293de906de214114dcb3af`, the hosted jobs reran `test_order_intake_preflight.py` (24/24 on Windows, Ubuntu and macOS). The suite covers direct `assess()` calls with forged booleans, undeclared personal fields and malformed nested source shapes, and `write_new_report()` calls with identifiers/unapproved fields, fake release/rights, forged prices and free text. The full suite passed 525/525 on Windows and macOS and 524 PASS + 1 Windows-only SKIP on Ubuntu. [Python/browser #43634647382](https://github.com/hibi89/data2web_studio/actions/runs/43634647382), [macOS offline #43634647412](https://github.com/hibi89/data2web_studio/actions/runs/43634647412), [CodeQL #43634647356](https://github.com/hibi89/data2web_studio/actions/runs/43634647356), and [evidence gate #43634647742](https://github.com/hibi89/data2web_studio/actions/runs/43634647742) succeeded at that exact HEAD.

This closes the internal regression recheck for these synthetic attack cases only. Issue #5 still has no comments or independent volunteer response; the 72/100 score, R29 PENDING state, and RELEASE HOLD / SALE NO-GO are unchanged.

### Exact-SHA Windows directory-junction regressions

At tested PR HEAD `c99f3d482a3972ff4de52c6df91f118854c383db`, `test_path_policy.py` creates a real Windows directory junction with `mklink /J`, verifies the reparse-point attribute and that `junction/source.csv` resolves to the fixture with `samefile()`, then requires the specific reparse-point rejection for source reads and output-parent use. The output case also confirms no target file was created.

[Python/browser #43636589005](https://github.com/hibi89/data2web_studio/actions/runs/43636589005) SUCCESS: Windows and Ubuntu each ran 527 tests; both junction cases PASS on Windows and explicitly SKIP on Ubuntu. The Ubuntu run has 3 skips total (two Windows-only junction cases and one Windows cmd.exe-only case). [macOS offline #43636589137](https://github.com/hibi89/data2web_studio/actions/runs/43636589137) SUCCESS: 527 tests, 3 platform-specific skips including the junction cases. [CodeQL #43636589034](https://github.com/hibi89/data2web_studio/actions/runs/43636589034) and [evidence gate #43636589543](https://github.com/hibi89/data2web_studio/actions/runs/43636589543) succeeded. The gate output remains `UNASSESSED`; there is no approved evidence manifest or official score.

A read-only High review first found that the initial junction tests could pass for an unrelated `ValueError`; commit `af0b530` closed that finding by requiring the fixture identity and specific guard message. The follow-up found no actionable issue. This static junction coverage does not prove directory-swap TOCTOU resistance or independent R29 acceptance; score addition remains 0.

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