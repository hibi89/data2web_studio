## 2026-11-15 KST — confirmed R29 verifier-acceptance finding (synthetic only; NOT external exploit)

**Finding R29-NAV-001, mitigation pending in CODEX-owned `verify_delivery.py`:** A canonical three-member ZIP containing a modified `index.html` with an added meta refresh directive and a recomputed `manifest.json.html_sha256` was **accepted** by the current independent ZIP verifier. The original static script hash and CSP were unchanged. This is evidence of a structural verifier gap, **not** evidence of actual browser navigation, networking, exfiltration, a customer incident, or a qualified external audit. Real browser navigation was deliberately not executed.

The HIGH-owned read-only replay script `r29_zip_navigation_diagnostic.py` and test `test_r29_zip_navigation_diagnostic.py` log only redacted enumerated findings. Their output was independently observed on hosted Windows/macOS/Ubuntu with `verifier_accepted_rehashed_navigation=true` and `external_network_request_performed=false`. The internal preaudit `security_audit_preaudit.py` now explicitly sets `status=INTERNAL_SYNTHETIC_SECURITY_HOLD_EXTERNAL_AUDIT_PENDING`, `technical_security_clearance=false`, and `open_security_findings=[R29_REHASHED_ZIP_HTML_NAVIGATION_ACCEPTED]` while the observed flaw remains. All normal 14 synthetic checks can pass and still **must not** be interpreted as R29 security clearance.

- **Exact code/test verification SHA** `87d0038a2d7650a8b5010ba54802e3004ac4db58`; [full hosted CI 5/5 SUCCESS](https://github.com/hibi89/data2web_studio/actions/runs/43686263198). Python Windows 548 total=545 PASS/3 SKIP, Ubuntu/macOS 548=544 PASS/4 SKIP; Chromium and Windows Chrome/Edge PASS. Green CI means the diagnostic detects and **reports the open defect**, not that the ZIP issue is fixed.
- [Codex PR #6](https://github.com/hibi89/data2web_studio/pull/6) comment #6890445038 requests CODEX-owned negative regression and minimum safe correction. The High lane deliberately did **not** edit that file. After Codex fixes its branch, rerun the same diagnostic and require `verifier_accepted_rehashed_navigation=false` at the exact reviewed combined SHA, then seek independent auditor replay.
- **Official score remains 72/100. R29 remains PENDING and security HOLD / SALE NO-GO.** No user/source/rightsholder approval, external assessor, data transfer or market release is implied.

## 2026-11-15 KST — auditor notice: R29 synthetic fixture validity tightened (current evidence)

Prior R29 synthetic probe fixtures could pass on unrelated malformed-OOXML / extra-ZIP-member errors. **Do not use the earlier standalone 14/14 result as attack-specific rejection evidence.** The High-owned generator now begins with `test_xlsx_fixtures.workbook_bytes()` (valid normal control), mutates one attack dimension at a time, checks named parser errors, and creates canonical three-member ZIP mutations instead of trivially adding a fourth member. Status forgery preserves ZIP envelope and exercises the manifest status guard.

**Exact tested SHA `99246c0813263cdcdc95cf557ed7649341d224bb`** — [3 OS + browser CI 5/5 SUCCESS](https://github.com/hibi89/data2web_studio/actions/runs/43685811003): 546 Python tests on each OS (Windows 543 PASS/3 SKIP; Ubuntu/macOS 542 PASS/4 SKIP), Chromium/Chrome/Edge PASS. New `test_r29_probe_specificity.py` adds 4 cases (accepted normal XLSX control; three specific XLSX attack causes and actual ratio; canonical three-member ZIP status/traversal/link rejection; unrelated errors do not count as attack-blocking).

Replay before external audit:

```bash
python -m unittest test_r29_probe_specificity test_security_audit_preaudit -v
python security_audit_preaudit.py
```

The independent evaluator must still challenge whether additional HTML elements (including `meta http-equiv=refresh`) are accepted after a same-container manifest rehash. That possible flaw is assigned to Codex-owned `verify_delivery.py` with a request for separate reproduction/fix. No real security certification, seller approval, external data transfer or score increase is claimed.

# DATA2WEB Studio — R29 external security assessor replay packet (synthetic only)

**Prepared:** 2026-11-15 KST. **Owner of this preparation:** GPT-6 High, not an independent auditor.
**Repository:** `hibi89/data2web_studio`. **HIGH branch:** `work/high-data2web-security-r06-r29-20261115`, Draft PR #7.
**Exact code + tests validation SHA:** `dd77d7c68a8c79f45e1439f3d59cb85131bfbac3`.
**CI:** https://github.com/hibi89/data2web_studio/actions/runs/43685167287 — 5/5 job SUCCESS, Windows Python 539 PASS/3 SKIP, Ubuntu/macOS Python each 538 PASS/4 SKIP, hosted Chromium/Chrome/Edge PASS.
**Documented state:** R29 EXTERNAL_PENDING, R06 EXTERNAL_PENDING, R01–R33 official 72/100. RELEASE HOLD / SALE NO-GO. This document does **not** claim an audit, legal review, product signing, customer acceptance or permission to publish source/client data.

## 1. Minimum authorized audit scope

The intended product is an offline, create-only transformation of explicitly approved CSV/JSON/TSV/XLSX tabular data to local HTML, ZIP and a JSON integrity receipt. Source data is plaintext in generated HTML. An independent evaluator should review:
- HTML/JavaScript renderer output (literal text/HTML injection, script end tags, markup/event attributes, formula-looking cells, dynamic CSV replacement, static JS SHA256 CSP, embedded JSON).
- No external network/browser loads under local `file://`; evaluate real Chromium/Chrome/Edge behavior, links/refresh/navigation, clipboard and file chooser boundaries. CSP alone is not proof of absence of navigation or data disclosure.
- ZIP verification (canonical envelope, file member set, duplicate names, ZipSlip, symlinks, CRC, excessive size, rehashed manifest, injected active markup and changed CSP/script).
- XLSX/OOXML parsing (external relationships, DTD/entity, macro parts, ZIP bombs/ratio, compression, malicious cached formulas, hidden rows/columns, ambiguous XML, cross-format fallback).
- Input file source SHA256, hardlink/reparse/junction/symlink/fd race, strict size limits, concurrent writes and same-length rename; output create-only/partial output HOLD.
- Local reports and error paths: no source rows/paths/device identity/tokens in redacted external evidence, no automatically deleted or overwritten customer files.

**Boundary:** CodeQL and assistant-run synthetic tests are *internal* evidence only. They do not satisfy the qualified independent human audit and retest required for R29.

## 2. Synthetic replay commands

Authorized evaluator should use a fresh isolated checkout at the exact SHA, Python >=3.11, no customer source or secrets, no admin requirement, and offline or sandboxed hosts. Do not change rights/permissions of existing customer folders.

```bash
git checkout dd77d7c68a8c79f45e1439f3d59cb85131bfbac3
python -m unittest test_security_audit_preaudit -v
python -m unittest test_r06_source_race test_snapshot_safety test_zip_offline_csp -v
python -m unittest discover -v
python security_audit_preaudit.py
```

The final command prints a **synthetic-only** report with exactly 14 enumerated boolean checks and `independent_security_audit_completed=false`, `commercial_release_approved=false`, `score_addition=0`. Optional create-only report: `python security_audit_preaudit.py --output /new/safe/empty/report.json` where the parent must exist and the report path must not already exist. Never upload that artifact or source samples without explicit separate authorization.

The source/test CI run above includes a 3-OS regression and browser smoke. Compare the exact SHA and logs before marking hosted test coverage. The hosted Windows runner is **not** a customer's Windows 10/11 device.

## 3. Current synthetic checks (not an acceptance score)

| Check group | Exact synthetic case name(s) | Expected |
|---|---|---|
| Output escaping | `XSS_SCRIPT_END_TAG`, `CSV_FORMULA_TEXT` | Customer cells retained as text, no injected active tag |
| HTML integrity | `STATIC_SCRIPT_HASH_MATCHED`, `NETWORK_MARKUP_ABSENT`, `OFFLINE_LOCAL_DELIVERY` | Current generated HTML only: static JS hash aligns with CSP, network markup absent |
| Source preservation | `ORIGINAL_BYTES_PRESERVED`, `EXISTING_DESTINATION_NOT_OVERWRITTEN` | No rewrite/no destructive overwrite |
| ZIP integrity | `ZIP_STATUS_FORGERY_BLOCKED`, `ZIP_SLIP_BLOCKED`, `ZIP_SYMLINK_BLOCKED`, `CUSTOMER_FOLDER_TAMPER_BLOCKED` | Invalid archive/folder cannot verify |
| XLSX parser | `XLSX_EXTERNAL_REL_BLOCKED`, `XLSX_ZIP_BOMB_BLOCKED`, `XLSX_MACRO_MEMBER_BLOCKED` | Unsafe in-memory synthetic OOXML must HOLD |

**Evidence nuance:** A fixed generated template passing `NETWORK_MARKUP_ABSENT` does not prove the standalone `verify_zip` structural policy rejects *a modified HTML file with its manifest recomputed*. This is a separate adversarial question.

## 4. Unresolved code-review hypothesis / separate CODEX ownership

An attacker changing `index.html` inside a ZIP and recomputing `manifest.json.html_sha256` may be able to introduce an additional `<meta http-equiv="refresh" content="0;url=https://invalid.example/">` while leaving the approved static script and CSP unchanged. `verify_delivery.py::_validate_offline_html_csp` appears to validate the exact static CSP hash and script count but not every additional meta-refresh/navigation element. This is **code-review suspected**, not confirmed in a clean reproducible execution. Do not label as a confirmed exploit.

A non-customer synthetic reproduction and a narrow fix/test have been requested on Codex Draft PR #6 (comment ID `6890324060`) because `verify_delivery.py` and `test_zip_offline_csp.py` are Codex-owned. Any fix must preserve legitimate local HTML updates and create-only contracts. High will review independent evidence and then test the exact combined SHA, without cross-branch parallel file edits.

## 5. Independent assessor record template

Store any identity-sensitive assessment details in an owner-approved private channel; only export a redacted summary afterward.

```text
Assessment scope/approval reference: OWNER-PENDING
Assessor independence and credentials: REVIEW-PENDING (not GPT-6/self-run)
Repo commit SHA (40 characters): ________________________________
OS/browser/Python versions: ______________________________________
Method & reproducible commands: __________________________________
Finding ID / severity / affected path: ____________________________
Synthetic-only reproduction evidence hash: ________________________
Observed PASS / FAIL / HOLD / NOT_RUN: ____________________________
Fix commit and independent re-test SHA: __________________________
Unresolved security risk and owner decision: _____________________
R29 verdict: NOT_ASSESSED / REJECT / CONDITIONAL / ACCEPT
Commercial/legal/data-rights approval (separate): NOT_GRANTED
```

Do not store actual customer records, access tokens, machine serials, system usernames or local absolute paths in a public PR, log or report. A security finding should not be closed solely because a new CI check is green.

## 6. Disclosure and explicit permission gates

- No engagement with an external professional or third-party service has been initiated. The product owner must appoint and authorize any assessor and approve the specific scope, costs and any data transfer before work.
- Share only this **synthetic-only** packet and repository source that the owner has explicitly authorized for the specific recipient. No source rights, shipping redistribution rights, or customer permission may be inferred from repository access.
- Report vulnerabilities by a private channel approved by the owner. Do not publish exploit payloads containing sensitive/customer data in public issues, discussions, Actions logs or automated artifacts.
- For a finding: reproduce safely with synthetic inputs, identify affected exact SHA and path, assign remediation to HIGH or CODEX file owner, rerun focused + full test at the precise combined code SHA, then seek independent assessor retest and documented owner sign-off.
- R29 can move to `VERIFIED` only if the fixed owner-approved requirement's complete independent audit and retest criteria are evidenced. Otherwise remain `PENDING`; never add its three official points merely for this preparation or CI success.
