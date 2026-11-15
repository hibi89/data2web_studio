## 2026-11-15 KST — H20 R29 strict read-only ZIP path / reviewed JS-CSS hashes (5/5 CI PASS)

- Confirmed CODEX PR #6 remains Draft unchanged at `afe6ed055cf4b9405da91d1028f9889555b41e00`; shipping HTML verifier defect R29-NAV-001 OPEN. No parallel edits to CODEX files.
- Found a real compatibility gap in High-only earlier candidate guard: browser's `document.documentElement.outerHTML` persists dynamic row/option/chart elements, so rigid tag counts would fail legitimate saved files. Corrected `r29_html_surface_policy.py`: static head/CSP/script controls fixed, dynamic safe tags bounded; tag-scoped attrs and chart-width-only styles; pinned SHA256 for reviewed V1 JS and CSS, independent of attacker-recomputed ZIP manifest and CSP. Test with synthetic dynamic-DOM, not actual downloaded browser file.
- Added read-only `r29_strict_zip_verifier.py` reviewer CLI and `test_r29_strict_zip_verifier.py` six focused tests: approved ZIP accepted without sale claim, rehashed extra meta refresh rejected, rehashed executable JS plus matching CSP rejected, rehashed CSS rejected, changed snapshot rejected, CLI path redaction. Existing legacy ZIP verifier accepts the same three rehash attacks; strict reviewer path rejects. No customer data, networking, destructive writes or release actions.
- **Exact code/test SHA `7fef5cb7af3e66d98206d48c8940e505a89aab15`**, [Actions 5/5 SUCCESS #43688532026](https://github.com/hibi89/data2web_studio/actions/runs/43688532026): Windows Python 565 = 562 PASS / 3 SKIP, Ubuntu/macOS each 565 = 561 PASS / 4 SKIP, Chromium and Chrome/Edge PASS. Production verifier still vulnerable; green CI is defensive gate coverage only.
- CODEX PR #6 comment #6890876238 requests shipping integration with its source provenance v3/versioned update and Windows packaging/include tests, no bypass. Future full combined-code CI required. Official 72/100 unchanged. R29 independent external audit PENDING and R06 real Windows10/11 PENDING, market release HOLD.

## 2026-11-15 KST — H20 passive HTML markup guard + differential replay, 5/5 CI PASS

- Codex PR #6 last checked at `afe6ed055cf4b9405da91d1028f9889555b41e00`: no `verify_delivery.py` change, confirmed R29-NAV-001 open. To avoid interfering with CODEX-owned files, High created `r29_html_surface_policy.py` and `test_r29_html_surface_policy.py` with a fixed static tag/attribute/metadata/script contract and 8 test cases.
- Baseline CI at `889f723068eaf1eabda2d50165cf2832446a1ec5` failed normal HTML due to legitimate boolean `hidden`, `multiple`, `selected`. Fixed only these whitelisted tag-specific forms at `0698eccb31dfc97b1e62dd9ecb5b7151906a497c` -> full [CI #43687004043](https://github.com/hibi89/data2web_studio/actions/runs/43687004043) 5/5 PASS.
- H20 differential replay amended `r29_zip_navigation_diagnostic.py` and `test_r29_zip_navigation_diagnostic.py` to verify the **same** meta-refresh tampered bytes: High guard rejects while legacy ZIP verifier accepts. Hosted 3 OS logs report `high_guard_accepted_pristine_html=true`, `high_guard_rejected_modified_html=true`, `verifier_accepted_rehashed_navigation=true`. No network request performed.
- **Latest exact full-code/test SHA `1e34652b0bf105c85835c7e3bc04a576cadfbf08`**, [CI #43687114162](https://github.com/hibi89/data2web_studio/actions/runs/43687114162) **5/5 jobs SUCCESS**. Python Windows 556=553 PASS/3 SKIP, Ubuntu/macOS 556=552 PASS/4 SKIP. Chromium/Chrome/Edge hosted PASS. The vulnerable production verifier is **not fixed yet**; this is detection and safe reusable guard, not acceptance.
- Candidate independent guard handed to Codex PR #6 via comment #6890564392. Codex owns `verify_delivery.py` and `test_zip_offline_csp.py` and is responsible for shipping integration and regression. PRs remain Draft, no merge. R29 external independent assessment PENDING, R06 Win10/11 owner acceptance PENDING, score **72/100**, release HOLD.

## 2026-11-15 KST — R29-NAV-001 reproduced and security HOLD reported; exact-SHA 5/5 hosted CI PASS

- HIGH-owned `r29_zip_navigation_diagnostic.py` generates new, synthetic, canonical three-member ZIP; injects meta-refresh into HTML; recomputes manifest HTML SHA; calls real `verify_zip`; never opens a browser or performs external requests. `test_r29_zip_navigation_diagnostic.py` records verdict without mislabeling insecurity as a security PASS.
- **Confirmed across 3 hosted OS environments:** `verifier_accepted_rehashed_navigation=true`, `status=SECURITY_HOLD_CANDIDATE_CONFIRMED`. This demonstrates a verifier input-validation gap; actual network navigation/exfiltration not tested.
- HIGH-owned `security_audit_preaudit.py` exposes redacted finding and `technical_security_clearance=false`, with targeted test in `test_security_audit_preaudit.py` to ensure open finding cannot be concealed by original 14 passing probes. The acceptance score, rights, external audit status and release remain unchanged.
- Tested exact code/test SHA `87d0038a2d7650a8b5010ba54802e3004ac4db58`: [CI https://github.com/hibi89/data2web_studio/actions/runs/43686263198](https://github.com/hibi89/data2web_studio/actions/runs/43686263198) **5/5 SUCCESS**: Windows Python 548 = 545 PASS/3 SKIP; Ubuntu/macOS 548 = 544 PASS/4 SKIP, Chromium/Chrome/Edge PASS. This is diagnostic PASS only, not R29 security clearance.
- Codex PR #6 explicitly notified (comment #6890445038); CODEX ownership of `verify_delivery.py` and `test_zip_offline_csp.py` preserved, no concurrent edits or automatic merge. Next: Codex fix SHA + focused negative tests → High exact-SHA independent retest → external auditor. Official **72/100**, RELEASE HOLD/SALE NO-GO.

## 2026-11-15 KST — H20 R29 provenance-grade fixture specificity regression (PASS)

- **Found test-quality defect (not evidence of a live exploitation):** earlier `_adversarial_xlsx` samples lacked a valid worksheet/sheet list, and ZIP Slip added a fourth member. As a result, the internal probe might accept an unrelated rejection as evidence that a *specific* attack was blocked.
- Fixed High-owned `security_audit_preaudit.py`: valid synthetic OOXML workbook baseline, single mutation per XLSX attack (external relationship, 180x compression bomb, macro part), canonical three-member ZIP malformed path/symlink, semantic forged-status manifest with canonical ZIP structure, exact cause matching rather than generic ValueError. Added `test_r29_probe_specificity.py` 4 tests and valid-control assertions. Existing 14 internal flags and external-audit PENDING semantics unchanged.
- Code/test exact SHA `99246c0813263cdcdc95cf557ed7649341d224bb`: [CI https://github.com/hibi89/data2web_studio/actions/runs/43685811003](https://github.com/hibi89/data2web_studio/actions/runs/43685811003) **5/5 SUCCESS**. Windows 546 tests 543 PASS/3 SKIP, Ubuntu/macOS 546 tests 542 PASS/4 SKIP, Chromium & Windows Chrome/Edge PASS. No customer data used.
- Codex PR #6 `afe6ed055cf4b9405da91d1028f9889555b41e00` remained Draft at observation; previous potential ZIP modified-HTML/meta-refresh concern still a **hypothesis**, delegated to Codex comment #6890324060. No merging or code-owner overlap. Current official 72/100, R29 EXTERNAL_PENDING and RELEASE HOLD.

## 2026-11-15 KST — H20 R29 internal adversarial harness extended; 5/5 hosted CI PASS

- High-owned `security_audit_preaudit.py`: internal synthetic R29 probe set expanded 7 -> 14 (new fixed static CSP script hash, absent network markup, ZIP ZipSlip/symlink, XLSX external relationship/ratio bomb/macro-part rejection). Uses only ephemeral synthetic bytes and isolated local folder; no client data or external transfers. Report contract V1 retained with additive check names; no score addition.
- High-owned `test_security_audit_preaudit.py`: updated scope/count expectations and added three negative/guard tests, including fail-closed report creation when a ZIP/XLSX verifier no longer rejects an attack.
- **Exact code + tests SHA `dd77d7c68a8c79f45e1439f3d59cb85131bfbac3`**, [parallel full CI #43685167287](https://github.com/hibi89/data2web_studio/actions/runs/43685167287) **5/5 SUCCESS**: Windows 542 tests = 539 PASS/3 SKIP; Ubuntu/macOS each 542 = 538 PASS/4 SKIP; Chromium/Chrome/Edge hosted smoke SUCCESS. Initial pre-test synchronization CI on only the first code commit failed because old tests still required 7; resolved with test update; no persistent defect observed on final SHA.
- Redacted synthetic replay packet: [R29 assessor packet](docs/parallel/R29_EXTERNAL_AUDITOR_REPLAY_PACKET_20261115.md), GitHub doc commit `17f1a3a61c409eb3011a091be6295a25c38e19f6`. This is **not** an independent external audit.
- **Potential unconfirmed CODEX-owned gap:** ZIP verifier appears not to reject injected meta-refresh navigation when HTML SHA is rehashed and static CSP hash unchanged. Requested a synthetic reproduction and constrained fix on Codex PR #6 via comment `6890324060`. No claim of exploited/confirmed vulnerability or acceptance; no overlapping CODEX file edit.
- Official 72/100, R29 PENDING/EXTERNAL_PENDING, R06 independent Win10/11 PENDING. Draft PRs unmerged. Next: Codex reproduction review → exact combined SHA regression if approved, then external independent assessor and customer consent evidence.

## 2026-11-15 KST — H10 CI failure repaired, exact-SHA full regression PASS

- 1st CI SHA `7576e3291981e7bffc2eda0b059ccb7931bf6f5f`: five new R06 tests passed on Ubuntu/macOS; existing `test_snapshot_safety.test_hardlink_alias_mutation_during_bounded_read_is_rejected` failed because the stronger preflight rejected the hardlink earlier than the old expected post-read exception. Confirmed actual log failure, not a source data regression.
- `test_snapshot_safety.py` updated at SHA `88c9123be526e947ec2fae5955f6933daf9fadee` to expect early hardlink HOLD **and** separately retain direct-source POSIX mutation detection / Windows write-denial test. No rollback of hardlink defense.
- **Exact source/test SHA `88c9123be526e947ec2fae5955f6933daf9fadee`**: https://github.com/hibi89/data2web_studio/actions/runs/43684105120 **5/5 jobs SUCCESS**. Python Windows 539 total / 536 PASS / 3 SKIP; Ubuntu/macOS each 539 / 535 PASS / 4 SKIP. Chromium, Chrome, Edge hosted offline probes PASS. Expected customer Win10/11 & independent R29 remain UNVERIFIED.
- Codex technical SHA `a13de6a2d498788d14e69b480899398c0257c18d`: separate 5/5 CI PASS. Later Codex PR #6 HEAD `6a849fbf1446ebb9f3ab4d4a87eb9a20bc1195bf` differs by docs only (verified compare). Partial independent PR comment #6890141705 requests exact combined-SHA test after integration; no merge approval. Official 72/100 and SALE NO-GO.

## 2026-11-15 KST — H10 R06 actual implementation (hosted CI pending)

- Confirmed baseline defects: absent hardlink count guard; POSIX FIFO substitution between precheck and open could block. No customer material used.
- Fixed `path_policy.py`: require single-link regular source at pre/post checks; nonblocking POSIX source open with post-open regular-file validation.
- Added 5 synthetic tests in `test_r06_source_race.py`: normal source, existing hardlink, injected new hardlink, POSIX FIFO swap, equal-length POSIX atomic replacement.
- Exact **source/test SHA**: `7576e3291981e7bffc2eda0b059ccb7931bf6f5f`; baseline `ded01ce3576a3ea06769fc8e18e917bd98b54ab2`. Threat/tradeoff/evidence: `docs/parallel/H10_R06_SECURITY_THREAT_REPRO_20261115.md`.
- GitHub parallel CI: https://github.com/hibi89/data2web_studio/actions/runs/43683639426 (**PENDING at this record's write**); predecessor code-only CI https://github.com/hibi89/data2web_studio/actions/runs/43683637215 (superseded/cancel in progress). Evidence gate on exact source/test SHA SUCCESS, but **UNASSESSED** for acceptance; no score uplift.
- Remains: confirm 5/5 hosted jobs, Windows 10/11 real-device negative acceptance, ancestor race analysis / independent R29 audit. Official 72/100, R06 PENDING, SALE NO-GO.

# High DATA2WEB R06/R29 security and integration evidence log

- Owner: GPT-6 High in this ChatGPT conversation; no unattended background execution
- Branch: `work/high-data2web-security-r06-r29-20261115`
- Shared source base SHA `cfc56fe4492f445d7f6a1fd12bb8d45c422de46e`
- Technical verified prior code SHA `9c8cfdcb1c10482ad6184a581991626b7e42138c`
- Current official score **72/100** and RELEASE HOLD/SALE NO-GO
- Scope: `docs/parallel/HIGH_SECURITY_AND_INTEGRATION_20261115.md`
- Codex lane: `work/codex-data2web-to100-20261115`; do not overlap source files

## Real work log — append only when executed

| KST | Task | Change | Code SHA | Test/run link | Observed result | Independent/external limitations | Next |
|---|---|---|---|---|---|---|---|
| 2026-11-15 | H00 branch guard | planning files only | initial branch | not executed for this branch | branch prepared, not tested code | full R06/R29 independent proof pending | H10 R06 focused threat reproduction |

## Integration restriction

PRs must be Draft against `feature/final-blueprint-p85-evidence-20261113`. High reviews Codex output, does not silently merge, force push, alter scorecard or claim independent external R29 status. After approved integration, update central `HANDOFF.md` + `STATUS.md` with ten-field handoff and exact SHA CI.
