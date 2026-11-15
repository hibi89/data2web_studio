# DATA2WEB Studio — Codex GPT-6 Luna Extra High: parallel engineering to final R01–R33 acceptance

> **Authority:** user-approved parallel implementation split, 2026-11-15 KST. This file delegates **all remaining CODEX-owned technical engineering toward 100/100**, not legal attestation, customer consent, external audit, scoring, production deployment, or release. Operate on THIS branch only. Work independently and comprehensively until technically blocked; do not stop after short status updates. Work is triggered only when user starts Codex; no unattended orchestration from ChatGPT.

## 0. Exact source and objective
- Repo: `hibi89/data2web_studio`; **only working branch**: `work/codex-data2web-to100-20261115`.
- Starting parent and integration target: `feature/final-blueprint-p85-evidence-20261113` at `cfc56fe4492f445d7f6a1fd12bb8d45c422de46e` (the parent may advance later; never blindly reset/rebase/force).
- Parallel High branch: `work/high-data2web-security-r06-r29-20261115`. **Do not edit High-owned files.**
- Parent PR #4 -> main remains DRAFT and unmerged. Your PR must target `feature/final-blueprint-p85-evidence-20261113`, remain **DRAFT**, and must never merge itself.
- **Actual fixed scoring:** R01–R33 33 requirements, denominator 100, 22 VERIFIED = **72/100**, 11 PENDING = 28 points. Stage scenarios (not a promise of awards): M85 R07=2/R21=4/R25=2/R26=2/R29=3; M95 R23=3/R27=2/R30=2/R32=3; M100 R06=2/R33=3. No partial points, no state/weight changes without independently verified full-item evidence. Sale = RELEASE HOLD / SALE NO-GO.
- Protected source order: HANDOFF.md → STATUS.md → AGENTS.md → REQUIREMENTS.md → docs/FINAL_DESIGN.md → data/final_blueprint_scorecard_v1.json → data/gpt6_execution_plan_r01_r33_v1.json → latest source/tests/actions. Read **newest top sections**; older records are historical. Do not rewrite the 160KB STATUS or 220KB HANDOFF on this branch.
- Exact last real technical CI: `9c8cfdcb1c10482ad6184a581991626b7e42138c`. Python/browser [#43647752145](https://github.com/hibi89/data2web_studio/actions/runs/43647752145) 4/4 PASS; Windows 533 tests 532 pass/1 skip, Ubuntu 529 pass/4 skip; macOS [#43647752125](https://github.com/hibi89/data2web_studio/actions/runs/43647752125) 529 pass/4 skip; CodeQL [#43647752124](https://github.com/hibi89/data2web_studio/actions/runs/43647752124) SUCCESS. Evidence gate [#43647752518](https://github.com/hibi89/data2web_studio/actions/runs/43647752518) workflow SUCCESS BUT result UNASSESSED. Previous R21 v1 provenance drift has been fixed via active v2; never repeat this failure or misclaim legal rights.
- Objective: finish independent R23/R27/R30/R32 engineering and customer-safe R07/R21/R25/R26/R33 technical prep, tests, and evidence handoff, with free hosted Actions and synthetic data. **Do not waste time recreating already verified tests or engineering outside assigned scope.**

## 1. Exclusive ownership to avoid concurrent conflict
**CODEX owns (only as needed):**
- R23 / R30 customer-safe device and browser E2E intake, `native_windows_acceptance.py`, `buyer_self_report_intake.py`, related R23/R30 tests, `docs/R23_R30_BUYER_RESULT_INTAKE_20261114.md`; prefer new dedicated `docs/parallel/codex-*` evidence files rather than competing edits.
- R27 actual SKU/limit/support/refund/tax conditions consistency: `docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md` and related commercial *draft* tests; NO publishing, final prices, tax/legal determination.
- R32 reproducible, unsigned owner preview/portable package engineering: `package_windows_bundle.py`, packaging-specific tests and preview docs; no signing purchases, B release or signed assertion.
- R21 **conditional** approved delivery license/NOTICE packaging/verification, if and only if true owner/rightsholder permission is supplied: `delivery.py`, `verify_delivery.py`, `verify_customer_folder.py`, `test_customer_folder.py`, `test_shipping_rights_preflight.py`, `receipt_utils.py`, `docs/R21_R33_SHIPPING_LICENSE_INVENTORY_20261114.md`. Until approval: audit/prepare isolated proposals and test fixtures, do NOT insert a fabricated LICENSE or change shipping contract.
- R07/R25/R26 customer-safe consent/retention runbooks or test utilities only when a **reproducible technical gap** exists; preserve existing owner-approved 7 internal policies and synthetic disposal tests.
- R33 **technical only** receipt SHA/contract and customer purchase/refund evidence-verifier templates, never execute a payment, publish a listing, produce fake orders, or assert GO.
- New dedicated docs `docs/parallel/CODEX_TO100_EXECUTION_20261115.md`, `docs/parallel/codex-worklog-20261115.md` and `data/parallel_codex_to100_tasks_v1.json` are Codex-owned.
**HIGH owns / CODEX MUST NOT TOUCH:** `path_policy.py`, `secure_output.py`, `security_audit_preaudit.py`, `test_path_policy.py`, `test_secure_output.py`, `test_security_audit_preaudit.py`, R06 file-identity/race tests, R29 security tests/audit methodology, `data/final_blueprint_scorecard_v1.json`, `blueprint_score.py`, `AGENTS.md`, `REQUIREMENTS.md`, `docs/FINAL_DESIGN.md`, `STATUS.md`, `HANDOFF.md`, `main`, final Gate/score/PR merging. Existing `r21_source_provenance.py` and v1/v2 pin registries are frozen; if a Codex-owned producer changes, flag TECHNICAL_PIN_DRIFT to High and propose auditable v3 with old versions preserved, never delete/bypass the check. Shared files not explicitly owned require a PR comment to High; no simultaneous edits.

## 2. Parallel work queues — do not block on M85 to prepare M95/M100
**C00 — source/CI/rollback gate (0 points):** verify source branch/SHA, already accepted 22 items, frozen scores, exact previous passing runs, Git author/committer linked to hibi89, no external access, 0 KRW spend. Inspect code before changing. Reference `data/gpt6_execution_plan_r01_r33_v1.json`. No redundant `CI rerun` if no code change.

**C10 — M95 R23 independent real-device acceptance preparation (3 points pending):**
1. Implement one portable *customer-safe* acceptance runbook and optional stdlib evidence verifier: Windows **10 and 11**, installed Chrome and Edge file://, macOS/Linux actual runtime, local CSV/JSON/XLSX/TSV, ZIP/receipt SHA, print, accessibility, mobile viewport, network calls 0. Collect OS/browser/runtime/test SHA/time/result without customer names, source bytes, paths, tokens, photos; make positive/negative fixtures and tests.
2. Validate on existing GitHub-hosted Windows/macOS/Ubuntu and browser jobs where possible; hosting image ≠ independent user Win10/11. R23 remains PENDING until independent authorized device evidence.

**C20 — M95 R27 real commercial-terms preapproval (2 points pending):**
1. Compare BASIC/PRO/BUSINESS SKU limits, customer source handling, fixes/revision counts, support, tax/platform fees, cancellation/refund statutory rights, customer copy retention with code and already owner-approved internal 0-cost defaults.
2. Produce *one* decision matrix listing exact missing external/owner selections and safe default TBD, NO tax or legal guarantee, no extra SKUs, no listing upload, no unilateral price/terms. Unit-test drafts/validators if appropriate. R27 PENDING until explicit owner signoff + actual platform evidence.

**C30 — M95 R30 integrated E2E (2 points pending):**
1. One real-device QA tool/script usable alongside C10 for source authorization → sheet/header/ID/category consent → deterministic HTML/ZIP/receipt → independent verify → Chrome/Edge file:// → local PDF print → allowed replacement/append → negative safety/digest failure → safe rollback/cleanup by operator.
2. Ensure sensitive data stays on examiner machine; GitHub only synthetic fixtures/redacted IDs. Integrate existing `native_windows_acceptance.py` and `buyer_self_report_intake.py` rather than duplicating. Simulated/hosted success is NOT independent real buyer acceptance. For R30, signing/rights audit still pending.

**C40 — M95 R32 portable preview/install/reproducibility (3 points pending):**
1. Audit clean Python 3.11 stdlib runtime, Tk dependency, Windows 10/11 install/uninstall, CMD/pyz/EXE preview build, deterministic manifest & SHA, unsigned/SmartScreen warnings, atomic create-only no overwrite, dependency origin/legal notices, no customer files in artifacts.
2. Fix real packaging defects and add cross-run CI tests/negative malicious ZIP and replay tests; produce a customer-safe offline verification guide. Do not auto-generate code-signing cert or claim signed EXE; B product sale is LATER and owner-controlled. R32 remains PENDING until approved rights/signing/real device/owner acceptance.

**C50 — M85 R07/R21/R25/R26 conditional closure engineering (0 automatic points):**
1. Reuse existing rights checklists, customer intake and retention utilities; inspect missing *technical* acceptance steps only, no duplicate flows. Existing 7 internal R25 policies and synthetic manual deletion were APPROVED; do not ask to approve them again.
2. R21: verify shipped HTML/CSS/JS, zip/verifier/receipt contracts & source provenance v2. If actual signed rightsholder scope and approved license/notice appear, create versioned, backwards-compatible conditional delivery contract and dedicated security/compatibility tests. **If no evidence, stop this R21 change at technical proposal; never create purported legal clearance.** Source Git metadata is not IP ownership.
3. R07/R26: build exact consent/approval validation and privacy-safe evidence intake only, no invented signed customer approvals. R25: build redacted actual lifecycle checklist and offline operator log schema without declaring a real disposal occurred.

**C60 — M100 R33 technical sale/receipt review (3 points pending):**
1. Prepare one public-safe final reconciliation checklist linking authorised customer source, delivered ZIP SHA, receipt, rights scope, agreed SKU, support/refund policy, sales proofs; identify false/absent evidence as BLOCKED.
2. Write negative tests preventing fake GO/false commerce receipts where relevant. Do not list on Kmong, perform charge/refund, process customer private records, fake transactions or assert payment/lifecycle completion.
3. All true commercial release, source consent, buyer/payments/refunds & marketplace decisions remain OWNER/EXTERNAL; R33 PENDING.

**C70 — stage gates, no fabricated score:**
1. After each independently testable increment, focused unit test; each substantial code change run existing free GitHub Actions at **exact feature SHA** including Windows/Ubuntu/macOS/browser as covered by changed-file triggers. Verify run IDs + job logs, not 'Ready' alone.
2. Produce M85/M95/M100 **technical readiness-only** reports with req IDs and each class `TECHNICAL_PASS`, `OWNER_PENDING`, `EXTERNAL_PENDING`, `NOT_RUN`, `FAIL`; no R07/R21/R25/R26/R29/R23/R27/R30/R32/R06/R33 unearned points, no modification to scorecard. High will perform final acceptance gate once proof exists.
3. Never block independent C10/C20/C30/C40/C60 engineering on G85-04/G95-01 if doing preparatory work is safe; later dependent **actual customer/paid actions remain blocked**.

## 3. Required decision and safety policy
- Compare at least two implementation strategies for major changes (e.g. custom test tool vs reuse existing; source path safety vs real-handle anchored). Select minimal safe, free and maintainable. Existing design approval permits implementation of scoped technical work; request explicit user approval for paid services, real external data sharing, publishing/listing, permission changes, score weights, original customer data, changes to source outside this branch, reduction of quality, or risky file handling.
- Any unexpected new external library: license, redistribution, network cost and security review; prefer stdlib and current pinned dev-only dependencies. Never leak originals, user home paths, identities, license documents, passwords or tokens into public repo or CI.
- Preserve working baseline and v1 provenance; forbid force push/rebase of shared branch, git history rewrite, CI disable, tests skipped to turn red green, scorecard state tweaks, auto-merging PR, external release. Existing 0KRW budget and sale HOLD always.
- If two attempts on unchanged cause fail without meaningful progress: STOP/PIVOT, record attempt/evidence/alternative/user decision; do not brute retry.
- '100%' is **full 33/33 acceptance only**, including real legal and independent evidence. Codex may complete its software work but MUST clearly label overall result `PARTIAL / EXTERNAL_PENDING`.

## 4. Mandatory deliverables to leave on YOUR branch
1. Code/tests and one draft PR against integration base (if PR was pre-created, reuse it). No merge.
2. `docs/parallel/codex-worklog-20261115.md`: per-task IDs, implementation decisions, changed file paths, tested SHA, commands, per OS/test PASS/FAIL/SKIP, remaining pending, exact run URLs, security/rollback.
3. Update your own `data/parallel_codex_to100_tasks_v1.json` statuses from evidence, NOT the official scorecard. Keep `docs/parallel/CODEX_TO100_EXECUTION_20261115.md` stable unless a true erratum.
4. PR description/comment with exact commit SHA, measured test count, unresolved OWNER/EXTERNAL gates, next High review request. High later updates central STATUS/HANDOFF in integration branch to avoid merge conflict.

## 5. Do-now instructions
Start **C00→C10/C20/C30/C40→C50 conditional→C60→C70**, group coherent commits, run focused tests before hosted suite. Work as far as possible without customer secrets, paid purchases, real signatures or owner-only approvals. When an item blocks, mark it BLOCKED and advance the next independent task. **No planning-only completion.** Report a concise technical PASS summary and exact GitHub PR/SHA when stopping, never claim official point gain without actual full evidence.
