# DATA2WEB Studio — GPT-6 High 설계 정본 / Instant 실행 지시서 (R01–R33, 72→85→95→100)

> **2026-11-14 KST | 문서 상태: 실행계획 확정·구현 수용 이전**  
> **공식 최종완성률 72/100, 22 VERIFIED / 11 PENDING, 85점까지 13점 부족.** `[작업중]`, `RELEASE HOLD/SALE NO-GO` 유지. 문서 공시는 새 기능 구현, 실제 고객 동의, 법적 권리, 외부 독립 감사 또는 완성률 상승을 뜻하지 않는다.

## 0. 정본·역할·우선순위
- **법적/기능 정본:** `REQUIREMENTS.md` → `docs/FINAL_DESIGN.md` → `data/final_blueprint_scorecard_v1.json` (33요구·100점 변경 금지). 배점 해설 `docs/FINAL_BLUEPRINT_WEIGHTING_100_APPROVED_20261114.md`. 본 문서는 *실행 지도*이지 원 요구사항 수정안이 아니다.
- **기준 저장소/브랜치:** `hibi89/data2web_studio` / `feature/final-blueprint-p85-evidence-20261113`, Draft PR #4 Open, 기존 `main` 미변경. 설계 직전 HEAD `bd2500a703d82420a542145ec2804ee1303355b9`; 마지막 **기능 CI 검증 SHA** `1be21c6a3f4ba2426c93a71201d96e274ce22ee7` ([Actions #43595570078](https://github.com/hibi89/data2web_studio/actions/runs/43595570078): Windows 507/507, Ubuntu 506 PASS+1 SKIP, browsers PASS, CodeQL/score gate 별도 SUCCESS). 이 설계 docs-only HEAD는 기능 검증 SHA가 아니다.
- **GPT-6 High(설계·검수):** 이 세부 계획과 최종설계 일치성 판단. 100점 개발 이후 `G100-02`에서만 기능/권리/독립 검증 증거를 최종 재감사. 85·95 중간 관문은 Instant 담당. High 스스로는 **외부 독립감사자(R29)**가 아니다.
- **GPT-6 Instant(구현):** 다음 `ㄱ`부터 `P00` 선행점검 후 가능한 READY 작업을 **실제 코드/테스트/회귀/문서**로 수행. 85·95점 중간 수용 판정까지 맡고 매 작업 끝에 exact tested source SHA와 docs HEAD 분리, PASS/FAIL/SKIP, `STATUS.md`/`HANDOFF.md` 갱신. 계획·상태 설명만 반복하지 말 것. **사용자 계정의 다른 ChatGPT 모드/채팅이 자동 실행되는 것은 아니므로** 해당 실행 담당에게 본 레포지토리 문서가 전달되어야 함.
- **OWNER/EXTERNAL:** 실제 고객 권리·개인정보 서면 동의, 자산 저작권/제3자 라이선스, 보존·파기 운영 책임, 외부 감사·실 OS·실 구매 인수는 코드를 작성하는 AI가 대리할 수 없음. OWNER/EXTERNAL 작업은 별도 사용자 승인·증거가 확보될 때까지 `BLOCKED`.
- **보호 경계:** 추가 현금 0원, 고객 원본/비밀 GitHub·AI·제3자 전송 금지, 고객 파일/이전 산출물 자동삭제·덮어쓰기 금지, 비승인 LICENSE/NOTICE 생성·판매·실고객 납품 금지, 권한/배포/Vercel/프로젝트 설정·`main` 변경 금지. 외부 공개 소스라도 평가자·범위·전송은 사전 승인.
- **실행 설계 비교:** (A) 단순 일괄 ‘85% 만들기’는 지연 위험을 숨기고 증거 없이 득점할 유인이 큼. (B) **고정 REQ별 원자 작업 + 선행/차단조건 + 별도 사람 검증 + 자동기술 게이트(선택)**는 관리 비용이 조금 증가하지만 재작업·비용·법적 위험이 낮음. **B 선택.** 기존 구현이 있으면 재작성하지 말고 **근거를 재검사**한 다음 실제 누락만 보완.

## 1. 점수·마일스톤: 확정 배점 변경 금지

| 단계 | 조건 | 가점 | 누적 목표 | 최초 상태 |
|---|---|---:|---:|---|
| 기준선 | R01–R33 중 기존 완전수용 22개만 인정 | 0 | **72** | VERIFIED 22 / PENDING 11 |
| **M85** | R07(2)+R21(4)+R25(2)+R26(2)+R29(3) **각각 전체 수용** | **13** | **85** | **전부 PENDING** |
| M95 | R23(3)+R27(2)+R30(2)+R32(3) 각 전체 수용 | 10 | 95 | 전부 PENDING |
| M100 | R06(2)+R33(3) 각 전체 수용 | 5 | 100 | 전부 PENDING |

**증거 결여 시 자동 점수 증가 0**. 중간 작업 완료, 문서 초안, 테스트 PASS, owner 내부 운영 정책 승인, CodeQL, 기존 계정 GitHub SHA만으로 어느 PENDING 요구도 자동 VERIFIED가 아니다. ‘85점’과 **공개판매·고객 원본 수령 승인**은 별도. 이 계획의 85→95→100은 상기 11개가 실제 모두 완전수용될 경우의 경로이며 보장 일정이 아니다.

## 2. 세부 Task 정의와 판정 형식
각 Task는 **ID·작업자·선행·동작·완료 판정·증거·실행 명령·소스 범위·차단원인**을 가진다. 기계 정본은 `data/gpt6_execution_plan_r01_r33_v1.json`. 작업별 `score_awarded_by_task=0`: 실제 점수는 **REQ 전체 인수시** 한 번만 반영. 이 계획에서 `TECHNICAL_PASS`와 `VERIFIED_ITEM`을 혼동하지 말 것.

기록 템플릿: `TASK_ID | 현재 HEAD | 실제 테스트 코드 SHA | 변경 파일 | 명령 | PASS/FAIL/SKIP | 합성/실OS/실고객/외부 범위 | 외부/owner 증거 ID(비식별) | 남은 차단 | 다음 작업 | 공식점수 | release 상태`. 고객명·개인 경로·원본·서면동의 원문은 공개 GitHub에 기록하지 않는다.


## 3. 필수 준비·보존·기준선 검증 (M0, 0점)

**P00 — INSTANT / READY**  
- **실행:** Read HANDOFF→STATUS→AGENTS→REQUIREMENTS→FINAL_DESIGN→scorecard→latest source; compare repo branch and PR SHA.
- **완료 조건:** Enumerate actual 33/100, 22 VERIFIED, 11 PENDING, latest tested code SHA separately from docs HEAD.
- **필수 증거:** Read-only SHA, scorecard contract, baseline diff in STATUS.
- **검증:** `python blueprint_score.py` / `python -m unittest test_blueprint_score -v`  
- **변경·참고 경로:** `HANDOFF.md`, `STATUS.md`, `data/final_blueprint_scorecard_v1.json`

**P01 — INSTANT / READY** · 선행 `P00`  
- **실행:** Secure previous non-destructive rollback reference and inventory customer/REA_Web protected paths; check auth identity, existing branch and CI budget.
- **완료 조건:** Explicit rollback SHA and original/no-overwrite boundary; no new branch/release/repo/rights change.
- **필수 증거:** Git commit parent SHA + protected paths listed; no private materials.
- **검증:** `python -m unittest test_customer_folder -v`  
- **변경·참고 경로:** `AGENTS.md`, `docs/ORIGIN_AND_LICENSE.md`

**P02 — INSTANT / READY** · 선행 `P00`  
- **실행:** Open evidence index per R with unique opaque IDs and a public-safe checklist; no customer names, data, screenshots, private paths or permission tokens.
- **완료 조건:** Each R07/R21/R25/R26/R29 evidence indexed as VERIFIED/INCOMPLETE/MISSING without assigning points.
- **필수 증거:** New redacted evidence reference index and missing list.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`, `docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md`

**P03 — INSTANT / READY** · 선행 `P00`  
- **실행:** Freeze regression commands against the last feature SHA; classify existing hosted/synthetic results as such, no buyer-acceptance assertion.
- **완료 조건:** No regression and no mistaken CI-Ready=customer-approved claim.
- **필수 증거:** Test run URLs exact SHA, PASS/FAIL/SKIP log and OS/browser scope.
- **검증:** `python -m unittest discover -v` / `python shipping_rights_preflight.py` / `python zero_cost_gate.py`  
- **변경·참고 경로:** `test_blueprint_score.py`, `shipping_rights_preflight.py`

## 4. 핵심 실행 WBS — 72→85점 (13점)

### R07 (2점, **현재 PENDING**)
**A07-01 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `P02`  
- **실행:** Map raw-source custody, user-of-record, owner-created copies, browser plaintext output and shared-data rights; reuse existing order_intake_preflight to avoid duplicate workflow.
- **완료 조건:** Data flow states input rights, no cloud upload, source hash invariance, unsafe types HOLD; missing legal rights clearly isolated.
- **필수 증거:** Redacted dataflow/threat review linked to source SHA.
- **검증:** `python -m unittest test_order_intake_preflight -v`  
- **변경·참고 경로:** `order_intake_preflight.py`, `docs/A_CUSTOMER_INTAKE_AND_DELIVERY_QA_DRAFT_20261114.md`

**A07-02 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A07-01`  
- **실행:** Prepare per-order right-to-use/transform/distribute confirmation checklist, user/third-party shared rights distinction, plaintext delivery and revocation triggers; only anonymous template.
- **완료 조건:** Specific customer/source/authority/consent/date scope fields for future private records; no fictional signatures or third-party agreement.
- **필수 증거:** Unfilled and redacted customer-rights form; review labels not approvals.
- **검증:** `python -m unittest test_order_intake_preflight -v`  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`

**A07-03 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A07-02`  
- **실행:** Audit both desktop single/batch consent-reset paths and CLI on source/sheet/header/ID mapping/file replacement; fix only reproduced omission.
- **완료 조건:** Invalid/missing consent or changed input fails closed; source bytes and existing customer outputs identical to pretest.
- **필수 증거:** Synthetic changed-source SHA, direct CLI and GUI regression evidence.
- **검증:** `python -m unittest discover -v`  
- **변경·참고 경로:** `data2web_desktop.py`, `data2web_single.py`, `data2web_append.py`, `test_acceptance.py`

**A07-04 — OWNER / BLOCKED_OWNER** · 선행 `A07-02 → A07-03`  
- **실행:** Confirm actual rights/authority and obtain specific owner/provider permission plus scope for one authorized acceptance case using approved private/local channel only.
- **완료 조건:** Real source authorization and consent can be independently checked; no private proof or source uploaded to public GitHub/ChatGPT.
- **필수 증거:** Owner/customer dated authorization held privately; GitHub only opaque status/reviewer reference.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `NON_DELEGABLE_RIGHTS_AND_CUSTOMER_CONSENT`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**A07-05 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A07-01 → A07-03 → A07-04`  
- **실행:** Review rights/consent provenance and source-before/after SHA, exact tested code SHA and residual privacy limits.
- **완료 조건:** Entire R07 source preservation + actual rights/consent satisfied; otherwise leave R07 PENDING.
- **필수 증거:** Signed/referenced Instant item-level review without customer data in repo.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`

### R21 (4점, **현재 PENDING**)
**A21-01 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `P01 → P02`  
- **실행:** Reconcile actual zipped HTML, manifest and README with local receipt, source Git blob pins, all shipped CSS/JS/vendor assets, excluded EXE/test deps.
- **완료 조건:** Complete real A shipping inventory vs whitelist; all provenance unknowns labeled pending, no fake LICENSE.
- **필수 증거:** Git-linked inventory with source SHA and actual synthetic ZIP member evidence.
- **검증:** `python shipping_rights_preflight.py` / `python r21_source_provenance.py`  
- **변경·참고 경로:** `data/shipping_rights_inventory_v1.json`, `data/r21_source_provenance_v1.json`, `docs/R21_R33_SHIPPING_LICENSE_INVENTORY_20261114.md`

**A21-02 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A21-01`  
- **실행:** For every shipped asset/derivation enumerate author, origin SHA, upstream reference, vendor license/NOTICE obligations and unresolved chains; do not infer IP ownership from AI generation or GitHub owner.
- **완료 조건:** Every actually shipped text/JS/CSS artifact has a rights-evidence or explicit unresolved flag; no accidental EXE bundling.
- **필수 증거:** Versioned chain-of-title/third-party dependency matrix, unknowns kept as blockers.
- **검증:** `python shipping_rights_preflight.py`  
- **변경·참고 경로:** `docs/ORIGIN_AND_LICENSE.md`, `docs/R21_SOURCE_PROVENANCE_EVIDENCE_20261114.md`

**A21-03 — OWNER / BLOCKED_OWNER** · 선행 `A21-02`  
- **실행:** Obtain actual rights-holder confirmation or license for derived code/templates, commercial redistribution scope and any third-party NOTICE; explicitly decide customer usage terms.
- **완료 조건:** Rights documents and each required notice licensed for the actual A deliverable; not merely owner planning direction.
- **필수 증거:** Private owner/legal/rights-holder evidence and public-safe approval scope, reviewer ID.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `RIGHTSHOLDER_IP_THIRD_PARTY_LICENSE_NOTICES`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**A21-04 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A21-03`  
- **실행:** Only after verified rights decision: choose (1) no extra member when legally justified; or (2) versioned approved LICENSE/NOTICE packaging contract, migrating builder/verifier/receipt together without breaking v1.
- **완료 조건:** Allowed contents match actual authorized rights text and deterministic ZIP, versioned v2 when needed; no overwrite, no invented license.
- **필수 증거:** Exact legal text provenance ref, package contract version, signed owner authorization, code diff.
- **검증:** `python -m unittest test_shipping_rights_preflight -v` / `python -m unittest test_customer_folder -v`  
- **변경·참고 경로:** `delivery.py`, `verify_delivery.py`, `verify_customer_folder.py`

**A21-05 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A21-04`  
- **실행:** Run synthetic allowed/forbidden license member, duplicate/ZIP-slip/modified notice, old v1 compatibility, receipt hash and create-only failure rollback.
- **완료 조건:** Valid authorized package passes independent verifier; malicious/unapproved member and old-data corruption fail closed, old v1 still accepted.
- **필수 증거:** Windows/Ubuntu and Chrome/Edge exact-SHA source/test evidence, ZIP hash and manifest contract.
- **검증:** `python -m unittest discover -v` / `python shipping_rights_preflight.py`  
- **변경·참고 경로:** `test_shipping_rights_preflight.py`, `test_customer_folder.py`

**A21-06 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A21-03 → A21-05`  
- **실행:** Review owner/third-party rights proof, final shipped bytes and license text/NOTICE obligations, migration, exact-SHA CI.
- **완료 조건:** Entire R21 including real commercial use permission and v1/v2 verifier correctness accepted or 4 points stay pending.
- **필수 증거:** Instant item review and exact rights decision reference, not hypothetical license.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`

### R25 (2점, **현재 PENDING**)
**A25-01 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `P02`  
- **실행:** Map owner-approved max 7-day temporary operator copy, earlier purpose-completion handling, legal exceptions, originals/outputs never auto-delete; compare current retention utility.
- **완료 조건:** No accidental deletion/upload; policy mismatch fails closed and actual disposal is not certified by metadata.
- **필수 증거:** Policy-vs-code map and synthetic time boundary tests.
- **검증:** `python -m unittest test_operator_copy_retention -v`  
- **변경·참고 경로:** `operator_copy_retention.py`, `data/zero_cost_owner_policy_v1.json`

**A25-02 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A25-01`  
- **실행:** Prepare an unfilled custody/owner role, where/when data copied, rights, purpose, manual deletion or return authority, legal exception and record checklist.
- **완료 조건:** Customer source and result retention separate; explicit records for custody, expiry, action and no-copy case; no customer identifiers in public repo.
- **필수 증거:** Redacted receipt/retention notice and operator manual checklist.
- **검증:** `python -m unittest test_operator_copy_retention -v`  
- **변경·참고 경로:** `docs/R07_R25_R26_LOCAL_COPY_RETENTION_20261114.md`

**A25-03 — OWNER / BLOCKED_OWNER** · 선행 `A25-02`  
- **실행:** Actually confirm responsible operator, permitted custody, disposal/return procedure and where separate private evidence is retained; execute a real authorized no-copy/copy-retention acceptance trace.
- **완료 조건:** Owner explicitly owns policy and genuine handling log exists; never claim physical deletion without action evidence.
- **필수 증거:** Private acceptance evidence/ref, public-safe policy signoff only.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `NON_DELEGABLE_OPERATOR_RETENTION_AND_DISPOSAL_EVIDENCE`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**A25-04 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A25-01 → A25-03`  
- **실행:** Compare actual operator evidence with source-preservation, duration and manual-only protocol; check legal exceptions not silently bypassed.
- **완료 조건:** Complete R25 policy notice and actual accountable practice satisfied; else hold.
- **필수 증거:** Instant item review plus retention acceptance reference.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`

### R26 (2점, **현재 PENDING**)
**A26-01 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `P02`  
- **실행:** Reconcile personal/sensitive/medical/payment identifiers, shared/confidential, unknown scope, allowed nonpersonal only; map plaintext and offline exposure.
- **완료 조건:** Default HOLD for personal/sensitive/unclear rights and explicit safe classification; no encryption/anonymous-data fiction.
- **필수 증거:** Synthetic privacy class matrix, mappings and negative cases.
- **검증:** `python -m unittest test_order_intake_preflight -v`  
- **변경·참고 경로:** `order_intake_preflight.py`, `data2web_desktop.py`

**A26-02 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A26-01`  
- **실행:** Audit frontend checkbox reset for replaced/altered source, rights, plaintext and privacy classification across single and batch; update tests only for reproduced gap.
- **완료 조건:** No persistence of stale sensitive approval across dataset revisions; file values not sent over network.
- **필수 증거:** CI/browser negative-flow evidence, clear notices/HOLD response.
- **검증:** `python -m unittest discover -v`  
- **변경·참고 경로:** `data2web_desktop.py`, `browser_final_blueprint_probe.py`

**A26-03 — OWNER / BLOCKED_OWNER** · 선행 `A26-01 → A26-02`  
- **실행:** For an actual lawful use case obtain owner and client decisions about data type/accessors/retention/transfers, explicit plaintext use and whether sensitive-data flow is rejected.
- **완료 조건:** Specific scoped customer agreement or documented nonpersonal-only boundary; no blanket approval inferred.
- **필수 증거:** Private dated consent and operator acceptance; public-safe redacted reference.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `NON_DELEGABLE_PER_CUSTOMER_PRIVACY_CONSENT`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**A26-04 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A26-02 → A26-03`  
- **실행:** Verify privacy scope and actual permission against implementation and plaintext warnings; never treat program checkbox alone as legal agreement.
- **완료 조건:** Full R26 personally sensitive data handling/rejection and real consent scope accepted; otherwise pending.
- **필수 증거:** Instant item review plus consent reference.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`

### R29 (3점, **현재 PENDING**)
**A29-01 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `P01 → P02`  
- **실행:** Freeze independent evaluator's threat scope: XSS/CSP/CSV formula, XLSX zip bomb and XML entities, ZIP/receipt, TOCTOU symlink/hardlink/junction, interruptions, offline network.
- **완료 조건:** Threat matrix has reproducible positive/negative test cases, supported OS constraints and residual risks; no claim of external audit.
- **필수 증거:** Synthetic case inventory, fixture hashes, exact source SHA.
- **검증:** `python security_audit_preaudit.py` / `python -m unittest discover -v`  
- **변경·참고 경로:** `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`

**A29-02 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A29-01`  
- **실행:** Prepare public-source-only reproducible audit bundle/instructions, source freeze and risk register, with existing internal CodeQL and browser CI clearly labeled self-check.
- **완료 조건:** Another evaluator can independently run tests without customer data, secrets, private access or false PASS.
- **필수 증거:** SHA-pin commands/expected outputs and failure reporting template.
- **검증:** `python security_audit_preaudit.py` / `python shipping_rights_preflight.py`  
- **변경·참고 경로:** `docs/R29_SYNTHETIC_PREAUDIT_HANDOFF_20261114.md`

**A29-03 — OWNER / BLOCKED_OWNER** · 선행 `A29-02`  
- **실행:** Select/approve a genuinely independent external reviewer and specific scope, any agreement or public-source sharing, zero-cost budget; no paid purchase or access grant absent new approval.
- **완료 조건:** Documented external evaluator independence, permitted public-only materials and no unauthorized spend/transmission.
- **필수 증거:** Owner approval/evaluator identity scope held privately, public-safe reference.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `INDEPENDENT_REVIEWER_AND_EXTERNAL_DISCLOSURE_APPROVAL`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**A29-04 — EXTERNAL / BLOCKED_EXTERNAL** · 선행 `A29-03`  
- **실행:** Independently reproduce attack matrix against frozen exact SHA in real supported environments and issue dated findings with severity, omissions, environment, command logs.
- **완료 조건:** Actual independent signed/attributable findings and limit descriptions, not a self-run AI/CodeQL report.
- **필수 증거:** External SHA-pinned review report, anonymized location and finding IDs.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`  
- **차단:** `REAL_INDEPENDENT_HUMAN_AUDIT_REQUIRED`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**A29-05 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A29-04`  
- **실행:** Implement least-invasive fixes for confirmed external findings, preserve originals/v1 ZIP and no-network contract, add reproducing regressions.
- **완료 조건:** Each finding has fix commit or documented accepted blocker, Windows/Ubuntu/browser CI on exact fix SHA.
- **필수 증거:** Finding→fix SHA→test table, data and secrets absent.
- **검증:** `python -m unittest discover -v` / `python blueprint_score.py`  
- **변경·참고 경로:** `path_policy.py`, `verify_delivery.py`, `verify_customer_folder.py`

**A29-06 — EXTERNAL / BLOCKED_EXTERNAL** · 선행 `A29-05`  
- **실행:** Same independent evaluator retests fixes on new SHA, records unfixable risks, gaps, and signoff/remaining-blocker status.
- **완료 조건:** External final retest confirms closure or explicitly blocks R29; no self-signed completion.
- **필수 증거:** Independent dated recheck SHA report, signed/attributable reviewer.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`  
- **차단:** `EXTERNAL_RETEST_AND_SIGNOFF`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**A29-07 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A29-04 → A29-06`  
- **실행:** Independently review external reviewer identity, scope completeness, outstanding findings, SHA and field/OS limits; don't conflate Instant with external.
- **완료 조건:** Complete R29 acceptance only after external signoff and verified no blocking findings; else PENDING.
- **필수 증거:** Instant R29 score review linking external IDs and code SHA.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`

### 단계별 최종 검증 게이트
**G85-01 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `A07-05 → A21-06 → A25-04 → A26-04 → A29-07`  
- **실행:** Assemble five complete item-level evidence packets with provenance and no private material in repo; reconcile 2+4+2+2+3 points.
- **완료 조건:** Each requirement fully accepted independently; none receives partial point for templates, self tests or false attestations.
- **필수 증거:** R07/R21/R25/R26/R29 acceptance matrix, exact SHA of reviewed functionality.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `docs/FINAL_BLUEPRINT_WEIGHTING_100_APPROVED_20261114.md`

**G85-02 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `G85-01`  
- **실행:** Run last exact-code-SHA Windows/Ubuntu Python, Chrome/Edge/Chromium, portable v1/v2, privacy/R21/R29 regression and CodeQL using existing free runners.
- **완료 조건:** All required CI jobs SUCCESS at exact code SHA with PASS/FAIL/SKIP, browser assets/API/zip/receipt intact; buyer acceptance separate.
- **필수 증거:** Actions URL/run/job, browser and no-network evidence; no doc-SHA confusion.
- **검증:** `python -m unittest discover -v` / `python blueprint_score.py` / `python shipping_rights_preflight.py`  
- **변경·참고 경로:** `.github/workflows/python-tests.yml`, `.github/workflows/final-blueprint-gate.yml`

**G85-03 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `G85-02`  
- **실행:** Only if five full acceptance proofs exist and Instant item evidence checks agree, update those five R states in existing 100-point locked scorecard; no weight changes; run score checker.
- **완료 조건:** Score mechanically equals 85/100, 33 items and 100 denominator unchanged, all five VERIFIED and other six PENDING; publish audit diff.
- **필수 증거:** Scorecard JSON diff, exact SHA score command and evidence links.
- **검증:** `python blueprint_score.py` / `python -m unittest test_blueprint_score -v`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`, `blueprint_score.py`

**G85-04 — INSTANT / QUEUED_DEPENDENCIES** · 선행 `G85-03`  
- **실행:** Instant 85 milestone evidence gate (High final review only after 100): confirm source SHA CI, complete real rights/consent/retention/legal/independent audit evidence, no sale or customer upload authorized by score.
- **완료 조건:** Authorize 85 report only when all five complete; otherwise return blocked IDs to Instant and preserve prior score; keep RELEASE HOLD.
- **필수 증거:** Instant acceptance memo with item verdicts, STATUS/HANDOFF consistency.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `STATUS.md`, `HANDOFF.md`

## 5. 후속 실행 WBS — 85→95점 (10점)

### R23 (3점, **85단계 완료 후**)
**B23-01 — INSTANT / FUTURE_STAGE** · 선행 `G85-04`  
- **실행:** Prepare exact browser/OS supported acceptance script for Win10/11 Chrome/Edge and macOS/Linux, real file:// access, ZIP + print/mobile, network0.
- **완료 조건:** Independent examiner reproducible steps and evidence intake fields.
- **필수 증거:** Device/browser matrix and safe synthetic benchmark.
- **검증:** `python -m unittest discover -v`  
- **변경·참고 경로:** `docs/R23_R30_BUYER_RESULT_INTAKE_20261114.md`

**B23-02 — EXTERNAL / BLOCKED_EXTERNAL** · 선행 `B23-01`  
- **실행:** Independent real supported buyer device tests, including full Win10/11 in contract, macOS/Linux additional cases; collect no sensitive uploads.
- **완료 조건:** Every mandated OS/browser combination supported or explicitly blocked; buyer proof not hosted CI.
- **필수 증거:** Independent version/environment/device acceptance.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/R23_R30_BUYER_RESULT_INTAKE_20261114.md`  
- **차단:** `REAL_INDEPENDENT_BUYER_DEVICE_NEEDED`; 실제 외부/사용자 확인 전 완료·점수변경 금지

### R27 (2점, **85단계 완료 후**)
**B27-01 — INSTANT / FUTURE_STAGE** · 선행 `G85-04`  
- **실행:** Reconcile SKU BASIC/PRO/BUSINESS data limits, revisions, support, refund non-waiver, platform fee and tax conditions against code and owners 0-cost internal defaults.
- **완료 조건:** Pricing/service/refund page contains no unsupported claim and no auto-listing.
- **필수 증거:** Draft publish-ready but unpublished SKU/FAQ/checklist.
- **검증:** `python -m unittest test_order_intake_preflight -v`  
- **변경·참고 경로:** `docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md`

**B27-02 — OWNER / BLOCKED_OWNER** · 선행 `B27-01`  
- **실행:** Explicitly approve real listing price and actual platform/tax/business support/refund operations separate from the internal zero-upfront defaults.
- **완료 조건:** Final operator policy signed off; posting/sale remains separate release decision.
- **필수 증거:** Private owner business approval and public-safe decision.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `OWNER_PRICING_PLATFORM_LEGAL_REVIEW`; 실제 외부/사용자 확인 전 완료·점수변경 금지

### R30 (2점, **85단계 완료 후**)
**B30-01 — INSTANT / FUTURE_STAGE** · 선행 `B23-02 → B27-02`  
- **실행:** Build customer-safe real E2E runbook for approved source, SHA, print, XLSX/TSV/batch, output compare, error/log redaction.
- **완료 조건:** Runbook and independent examiner run reproduce end-to-end flow without leaked originals.
- **필수 증거:** Per-OS sanitized actual E2E evidence.
- **검증:** `python -m unittest discover -v`  
- **변경·참고 경로:** `native_windows_acceptance.py`, `buyer_self_report_intake.py`

**B30-02 — EXTERNAL / BLOCKED_EXTERNAL** · 선행 `B30-01`  
- **실행:** Complete independent actual-user E2E and packaging/signing/licensing review in required OS/browser environments.
- **완료 조건:** Human test evidence, remediation and acceptable remaining limitations; no hosted-only substitution.
- **필수 증거:** External customer acceptance/test transcript; private source restricted.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/R23_R30_BUYER_RESULT_INTAKE_20261114.md`  
- **차단:** `EXTERNAL_CUSTOMER_E2E_REVIEW`; 실제 외부/사용자 확인 전 완료·점수변경 금지

### R32 (3점, **85단계 완료 후**)
**B32-01 — INSTANT / FUTURE_STAGE** · 선행 `G85-04`  
- **실행:** Audit clean Python/portable/Windows owner preview build reproducibility, executable dependencies + licensing, offline installation/uninstallation and rollback instructions; no B commercial distribution.
- **완료 조건:** Repeatable clean build hashes and commands, dependency manifests and CI success; non-free signing or installer gating flagged.
- **필수 증거:** Build manifest/binary SHA/runner version/NOTICE table, no customer data.
- **검증:** `python -m unittest discover -v`  
- **변경·참고 경로:** `package_windows_bundle.py`, `docs/R21_R33_SHIPPING_LICENSE_INVENTORY_20261114.md`

**B32-02 — OWNER / BLOCKED_OWNER** · 선행 `B32-01`  
- **실행:** Approve bounded intended executable distribution/support/signing approach and rights after field test; costs require separate explicit advance approval; no paid signing assumed.
- **완료 조건:** User acceptance of reproducible actual delivery/runtime and safe rights; B remains unsigned preview until separate GO.
- **필수 증거:** Owner/independent build-rights and device evidence.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `NATIVE_RELEASE_RIGHTS_SIGNING_APPROVAL`; 실제 외부/사용자 확인 전 완료·점수변경 금지

### 단계별 최종 검증 게이트
**G95-01 — INSTANT / FUTURE_STAGE** · 선행 `B23-02 → B27-02 → B30-02 → B32-02`  
- **실행:** Review R23=3,R27=2,R30=2,R32=3 full evidence, rerun score/CI and update only verified items through Instant.
- **완료 조건:** If and only if four complete items accepted, confirmed score=95/100; sale still HOLD.
- **필수 증거:** Instant milestone review, revised exact SHA scorecard/CI and handoff.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`, `STATUS.md`

## 6. 최종 실행 WBS — 95→100점 (5점)

### R06 (2점, **95단계 완료 후**)
**C06-01 — INSTANT / FUTURE_STAGE** · 선행 `G95-01`  
- **실행:** Reassess file replacement/collision/TOCTOU, hardlink and Windows reparse, identity snapshots and OS concurrency; compare OS-specific secure-handle plan vs fail-closed documented limitation.
- **완료 조건:** Demonstrated deterministic OS-specific race regression and safe source/target preservation; no claim fully atomic without proof.
- **필수 증거:** Adversarial synthetic+real OS evidence and design decision.
- **검증:** `python -m unittest test_customer_folder_member_identity -v` / `python -m unittest test_customer_folder_root_races -v`  
- **변경·참고 경로:** `path_policy.py`, `verify_customer_folder.py`

**C06-02 — EXTERNAL / BLOCKED_EXTERNAL** · 선행 `C06-01`  
- **실행:** Independent runtime tester exercises scoped realistic concurrent source/destination file swaps on supported Windows and Linux, records failures and mitigation acceptance.
- **완료 조건:** Source SHA/size/bytes, customer folder race and residual risk accepted on real OS; otherwise R06 pending.
- **필수 증거:** Independent OS/TOCTOU final acceptance, exact code SHA.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`  
- **차단:** `INDEPENDENT_OS_RACE_PROOF`; 실제 외부/사용자 확인 전 완료·점수변경 금지

### R33 (3점, **95단계 완료 후**)
**C33-01 — OWNER / BLOCKED_OWNER** · 선행 `G95-01`  
- **실행:** Verify full commercial IP chain, actual buyer data use and redistribution rights, public deliverable contents, legal refund support obligations and final owner acceptance.
- **완료 조건:** Real lawful source/contract/license/right holder and signed commercial operational authorization; no AI-created evidence.
- **필수 증거:** Private owner/legal/customer rights record with redacted public index.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/OWNER_APPROVAL_PACKET_A_20261114.md`  
- **차단:** `REAL_COMMERCIAL_RIGHTS_AND_OWNER_APPROVAL`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**C33-02 — EXTERNAL / BLOCKED_EXTERNAL** · 선행 `C33-01`  
- **실행:** Obtain actual buyer acceptance evidence and legitimate purchase/refund lifecycle operational proof under approved marketplace terms; no artificial order or fake sale.
- **완료 조건:** Independent legitimate buyer/customer acceptance and lifecycle, or remain blocked pending actual buyer.
- **필수 증거:** Private customer/marketplace evidence and compliant redacted reference.
- **검증:** 서면/외부 독립 증거(기술 CI만으로 대체 불가)  
- **변경·참고 경로:** `docs/A_FIRST_B_LATER_PRODUCT_ROADMAP_20261114.md`  
- **차단:** `REAL_CUSTOMER_PURCHASE_AND_REFUND_PROCESS`; 실제 외부/사용자 확인 전 완료·점수변경 금지

**C33-03 — INSTANT / FUTURE_STAGE** · 선행 `C33-01 → C33-02`  
- **실행:** Cross-check exact delivered artifact and receipt SHA/rights/acceptance with actual signed operational evidence, without posting, charging, uploading or changing security policy.
- **완료 조건:** No inconsistency between contract/ZIP/source/SKU/consumer rights; no automatic release GO.
- **필수 증거:** Legal+technical signoff matrix, evidence redacted.
- **검증:** `python shipping_rights_preflight.py` / `python blueprint_score.py`  
- **변경·참고 경로:** `docs/R21_R33_SHIPPING_LICENSE_INVENTORY_20261114.md`

### 단계별 최종 검증 게이트
**G100-01 — INSTANT / FUTURE_STAGE** · 선행 `C06-02 → C33-03`  
- **실행:** Re-run full regression and entire 33-item acceptance ledger; only after R06/R33 full evidence change scorecard, run exact SHA gates and prepare support/rollback handoff.
- **완료 조건:** 100/100 mechanically and evidentially justified, 33/33 VERIFIED, no missing independent evidence, original files preserved.
- **필수 증거:** Exact SHA 3OS/real buyer/independent reports, reviewer approval matrix and scorecard.
- **검증:** `python -m unittest discover -v` / `python blueprint_score.py`  
- **변경·참고 경로:** `data/final_blueprint_scorecard_v1.json`, `HANDOFF.md`, `STATUS.md`

**G100-02 — HIGH / FUTURE_STAGE** · 선행 `G100-01`  
- **실행:** Independent High end-to-end final audit of code+CI, UI/browser, artifacts, legal/privacy/customer evidence, security, origin and score; separate commercial release authorization from 100%.
- **완료 조건:** Either issue documented final 100 acceptance with evidence and explicit remaining release gates, or reject and return exact task IDs.
- **필수 증거:** High final verdict with SHA and nondelegable evidence references; release never auto-approved.
- **검증:** `python blueprint_score.py`  
- **변경·참고 경로:** `HANDOFF.md`, `STATUS.md`

## 7. Instant 실행 순서와 병렬 작업 선택
1. 새 채팅·새 모델에서 우선 `HANDOFF.md` → `STATUS.md` → `AGENTS.md` → `REQUIREMENTS.md` → 이 계획 → scorecard → 최신 코드/PR/Actions 순서로 읽는다. **`P00`, `P01`, `P02`, `P03`을 우선**하고 이미 검증된 내용은 중복 개발하지 않는다.
2. **85 우선 실제 진행 큐:** `A07-01` → `A21-01` → `A25-01` → `A26-01` → `A29-01`. 그다음 각 Req 내부의 INSTANT 작업을 선행순으로 수행한다. OWNER/EXTERNAL 차단 작업은 넘겨 **다른 독립 INSTANT 작업**을 진행한다. 승인 요청은 가능한 한 `OWNER` 항목을 모아 한 번에 제시한다.
3. 불가역/비용/보안·권리 변경 전 **최종 승인**은 선행 단계. 특히 `A21-04`는 실승인된 LICENSE/NOTICE 판단 없이 구현·추가하지 않는다. `A29-04`/06은 실제 외부인이 맡아야 하고 ChatGPT High는 대체자가 아니다.
4. 매 `ㄱ` 작업 회차: **읽기(최신 원본) → 위험/대안 최소2개 비교 → 최소수정 → 합성 회귀·현실 가능한 hosted 브라우저 → GitHub 커밋(Author/Committer 계정 확인) → exact SHA Actions 결과 → `STATUS/HANDOFF` 최신화 → 공식점수·차단/다음 ID**. 우선순위 없는 테스트만 반복하거나 ‘완료율을 올리기 위한 문서’만 반복하지 않는다.
5. 실패는 `시도 / 실제 실패 근거 / 수정 경로 / 최대1회 개선 재시도 / 전환/사용자 선택`. GitHub CI 잠시 대기면 공개/합성 가능한 **다른 미완료 Task** 실행. **두 번 무진전**이면 같은 해결책 반복 금지, 차단을 솔직히 기록.
6. Owner/evaluator 증거가 없어 작업이 막혀도 72%를 85%로 표기하지 않는다. 현재는 **판매, 게시, 고객 원본 수령, 유료 서비스, GitHub 공개권한 변경, 자동 데이터 파기, `main` merge** 모두 미승인 또는 별도 법적 게이트로 HOLD.

## 8. 마일스톤 완료 조건 및 High 최종 검수
- **G85-04:** R07/R21/R25/R26/R29 **모두 전체 증거**, 85점 scorecard fixed 100, CodeQL+Windows/Ubuntu+Chrome/Edge/Chromium exact tested SHA, 독립 R29 외부 감사·재검증 확인, RIGHTS/PII/RETENTION 실제 증빙 확인. 출시/판매는 여전히 HOLD.
- **G95-01:** R23/R27/R30/R32 전체 실제 사용자/운영/재현 빌드 수용 및 95점. Customer Win10/11 및 필요한 macOS/Linux는 hosted CI로 대체 불가.
- **G100-02:** R06·R33까지 전체 수용, 33개 요구 전수 감사, 소스 SHA=실행 증거/패키지와 일치, 원본 불변, 고객 계약·환불/재배포·저작권 증거 점검, 100점 진위 검증. **100점 자체가 실제 판매 게시/유료 결제/접근권 변경의 포괄적 승인 아님.**
- 100점 이후 High 최종 검수자가 발견한 반례는 `FAIL/BLOCKED`로 기록하고 근거 없는 기존점수 조정 금지. 최소 수정은 Instant 담당으로 되돌리고 동일 인수기준으로 재검수.

## 9. 최초 수행 범위·수용 증거의 차이
- **이미 있음(재작성 금지):** Python stdlib CSV/TSV/JSON/XLSX, GUI 단일·배치/승인 리셋, create-only HTML/ZIP/receipt, 3브라우저 호스팅 E2E, 샘플 기반 507 Windows PASS, 사전권리/개인정보 익명 분류, 운영자 7일 보관 점검, R21 source pins 및 shipping preflight, CodeQL/R29 내부 synthetic preaudit. **이 모두가 실 고객/외부 법률·감사 수용을 보증하지 않음.**
- **실외부 증거 없이는 AI가 완료 불가능:** `A07-04`, `A21-03`, `A25-03`, `A26-03`, `A29-03`/`04`/`06` 및 95/100단계 real buyer/legal acceptance. 0원 무료 독립 평가자가 실제 확보되지 않으면 R29는 HOLD. **85점 달성 무기한 보장 금지.**
- **출시 상태:** 현재 `[작업중]`, `RELEASE_HOLD_SALE_NO_GO`; 판매 기록이 없는 크몽 중앙 원장을 변경하거나 `등록완료`로 표시 금지.

## 10. 문서 관리 및 회차 인수인계
- **Primary (실행·공시):** 이 문서와 `data/gpt6_execution_plan_r01_r33_v1.json`, `AGENTS.md`의 역할 규칙.
- **Every substantive turn:** `STATUS.md`와 `HANDOFF.md` 갱신, exact code SHA/문서 HEAD/PR Draft 상태 확인, 비밀·원본 데이터 비포함. 기존 기록 전체 보존; docs-only `[skip ci]` SHA는 기능 CI가 아님.
- 변경 기준: 실제 소스/검증 근거가 문서와 다르면 **검증된 최신 실제 실행**을 우선, 차이 명시. 단계/배점 변경은 owner 승인·versioned plan/scorecard 없이 불가.
