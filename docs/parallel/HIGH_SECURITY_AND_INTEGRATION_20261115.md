# DATA2WEB — GPT-6 High parallel lane: R06/R29 security engineering, review and integration

**Status:** branch instructions only, not evidence of implemented tests. User approved the two-branch parallel structure on 2026-11-15 (KST). Actual work advances only when user reopens/commands the relevant ChatGPT or Codex session.

## 1. Source of truth, exact branches and split
- Repository: `hibi89/data2web_studio`
- Integration base: `feature/final-blueprint-p85-evidence-20261113`; exact shared initial commit `cfc56fe4492f445d7f6a1fd12bb8d45c422de46e`.
- **This High branch:** `work/high-data2web-security-r06-r29-20261115`. The **Codex branch:** `work/codex-data2web-to100-20261115`.
- Last trusted exact tested technical code SHA `9c8cfdcb1c10482ad6184a581991626b7e42138c`: Python/Browser [#43647752145](https://github.com/hibi89/data2web_studio/actions/runs/43647752145) 4/4 jobs PASS, macOS [#43647752125](https://github.com/hibi89/data2web_studio/actions/runs/43647752125) PASS, CodeQL [#43647752124](https://github.com/hibi89/data2web_studio/actions/runs/43647752124) PASS. All hosted/synthetic, not external acceptance. Score evidence gate #43647752518 UNASSESSED.
- Read before any change: HANDOFF.md → STATUS.md → AGENTS.md → REQUIREMENTS.md → docs/FINAL_DESIGN.md → data/final_blueprint_scorecard_v1.json → data/gpt6_execution_plan_r01_r33_v1.json → current exact source/tests. Current official **72/100**: 22/33 VERIFIED + 11 pending, 85 +13, 95 +10, 100 +5. Scorecard denominator/weights/states immutable until real complete acceptance proof.
- Existing upstream PR #4 is Draft/unmerged and currently targets `feature/p85-ui-crossbrowser-20261113` (not main); THIS High branch's PR and Codex branch's PR should be Draft against integration base. Never touch main or force-push.

## 2. The technical HIGH work (do concurrently with CODEX)
**H00 Baseline & lockfiles (0 points):**
- Verify source/branch/CI/tag refs and source lineage; preserve originals and earlier R21 registry v1 blob `11796f9174fec88e29335d5f19bfe3038636787a`, active v2; no new CodeQL run just for a document change.
- Inspect Codex branch and overlap prevention; share findings via PR comment, never edit Codex-owned file concurrently.

**H10 R06 TOCTOU / provenance input-source and output path race (2 points PENDING):**
- Define a threat matrix for Windows 10/11 path replacement/reparse/hardlink/symlink/changed file identity, POSIX atomic path rename, FD-vs-path read, create-only output, SHA256 size and byte snapshot validation, ZIP/manifest verification, malicious same-length replacement, concurrent threads/processes, and rollback.
- Compare strategy A strict reject-and-HOLD against strategy B directory-FD/handle anchored reopen+pin: robustness, Windows portability, stdlib maintenance, zero cost. Prefer safe minimal implementation after exact observed defect; preserve stable original files.
- Implement synthetic deterministic race injection/negative cases in **HIGH-owned** `path_policy.py`, `secure_output.py`, `test_path_policy.py`, `test_secure_output.py` or dedicated `test_r06_race_*.py`, with focused tests. If fix needs Codex-owned `verify_customer_folder.py`, `delivery.py`, `receipt_utils.py`, `native_windows_acceptance.py`, open precise Codex PR request with failing reproducer; do NOT edit these files simultaneously.
- Validate exact-SHA Windows/Ubuntu/macOS hosted Actions, explicitly separate true Win10/11 tester proof (R06 external task `C06-02`) from hosted. R06 stays PENDING until real independent runtime test/retest passes.

**H20 R29 XSS/CSP/path/ZIP/XLSX external audit readiness (3 points PENDING):**
- Run focused internal synthetic adversarial assessment: source plain-text and rich-cell escaping/DOM XSS, script hash CSP consistency, content sniffing, URL/network0/CORS/file://, ZIP member count/duplication/symlink/CRC/ZipSlip/malicious rehashed manifest, XLSX OOXML cached external links/zipbomb, bounded input size, customer input redaction and source SHA, FD race behaviors, preserve-only output, error messages leak no data.
- Validate existing `security_audit_preaudit.py`/`test_security_audit_preaudit.py` and add only new negative/reproduction tests on High-owned paths; no false claims of independently qualified audit.
- Prepare a **public-code / synthetic-data-only redacted external auditor evidence bundle** with exact source/test SHA, commands, constraints, threat matrix, results template, reproducible failure tests, responsible disclosure route, minimum scope and data transfer permission gate. Auditors are human and independently appointed by owner; cannot self-attest R29 or treat GitHub CodeQL as external audit. No external sharing or paid service without user approval.
- If actual external findings later arrive, register reproduction and owner review, fix only High-owned code in this branch, ask Codex for fixes to their owned files, re-test exact SHA. R29 remains PENDING until third-party report and independent retest/signoff.

**H30 50 task map and review:**
- Codex branch has `data/parallel_codex_to100_tasks_v1.json` mapping **all 50 WBS tasks** to CODEX/HIGH/OWNER/EXTERNAL (CODEX 24, HIGH 12, OWNER 8, EXTERNAL 6) with exact stage gates and nondelegable blockers.
- Codex responsible for R23/R27/R30/R32 engineering, conditional R21 package changes after rights clearance, safe R07/R25/R26 intake prep and R33 reconciliation. High is responsible for security R06/R29 plus final scoring/review gates; OWNER/EXTERNAL retain their respective genuine evidence.
- In your branch update only `docs/parallel/high-security-worklog-20261115.md` and additional dedicated high docs. No `STATUS.md`/`HANDOFF.md` edit while Codex is preparing its PR; update central docs once integration is reviewed and approved to avoid conflict. Do not update official scorecard on either branch without complete item proof and approved integration.

**H40 final integration and score review:**
- Verify both Draft PR diffs from exact root SHA; enforce file ownership rules, untouched scorecard, safe 0-KRW/zero-external-data policies, author/committer user match, negative tests and file-source provenance. Never treat `Ready` or workflow SUCCESS with `UNASSESSED` as full acceptance.
- On review: test focused subset, compare against parent base to detect stale conflicts, run full existing free workflows at exact integration SHA only if owner approves merge to integration branch. Prioritize current build and preserve 22 accepted items and customer files, and record regression findings without silently reverting user sources.
- Owner/EXTERNAL missing evidence must be recorded as `BLOCKED_OWNER`/`BLOCKED_EXTERNAL` using opaque references, never invented signoffs. Stage gates G85/G95/G100 are High's final evidence review; no +2/+3/+4 unless each complete requirement verified.
- After approved integration: top-update STATUS.md, HANDOFF.md full ten required fields, complete source SHA, Actions job logs and runtime/browser test status, privacy/security/rights pending, Production/Vercel `N/A` for offline A. Keep PR #4 Draft and main unchanged until explicit release approval.

## 3. Forbidden overlap and security invariants
**High-owned only:** `path_policy.py`, `secure_output.py`, `security_audit_preaudit.py`, `test_path_policy.py`, `test_secure_output.py`, `test_security_audit_preaudit.py`, security-only test files, High worklog/packet, review comments. **Codex-owned only:** `native_windows_acceptance.py`, `buyer_self_report_intake.py`, `package_windows_bundle.py`, `delivery.py`, `receipt_utils.py`, `verify_delivery.py`, `verify_customer_folder.py`, SKU draft, R23/R30 buyer tests/guide, their worklog.
- Highest risk shared issue: R21 producer source provenance v2 WILL fail closed if Codex edits `delivery.py`, `receipt_utils.py` etc. Require reviewed versioned v3 (keep v1/v2 historical), never disable provenance. Do not silently accept any new vendor license.
- Fixed global guards: no 3rd-party client data upload, no new spend, no releasing to market, no permission change, no auto-deletion/overwrite, no unpublished rights grant/altered scorecard, no main merge, no force push. Customer rights and external R29 are nondelegable. Production/Vercel not applicable for offline A.
- If any regression or a user-provided proof is ambiguous, clearly label verified/partial/unverified, STOP/PIVOT after 2 nonprogress attempts. Present 1–3 alternatives if blocked. When resumed with `ㄱ`, implement the next High-owned task rather than repeating inspections or reporting progress only.

## 4. Acceptance and handoff
- High code changes need reproduced before/after tests, SHA and exact free GitHub Actions logs, real OS pending noted.
- Codex PR review must include exact SHA, source diff, boundary checks, contract and 100-point scorecard unchanged, test/CI pass, blocked external gates, correction request or reviewer acceptance. Only user can approve any actual commercial GO.
- Required 10-field HANDOFF after integration (not both branches concurrently): 1 requirements/tech, 2 changes/rationale, 3 tests/pass-fail-skip, 4 status/blockers, 5 errors/attempts/pivots, 6 repo/branch/SHA/files, 7 production/environment, 8 originals/backups/security, 9 next actions/approvals, 10 KST + verified SHA/range.
