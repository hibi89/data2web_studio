## 2026-11-15 KST — 최신 exact-SHA 실행 상태

- [Python/browser #43609470587](https://github.com/hibi89/data2web_studio/actions/runs/43609470587) SUCCESS at `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`: Windows 522/522 PASS; Ubuntu 522 run, 521 PASS + 1 Windows-only SKIP; Chrome/Edge and Chromium hosted browser flows PASS, including synthetic Tk single/batch consent reset.
- [macOS offline #43609470565](https://github.com/hibi89/data2web_studio/actions/runs/43609470565) SUCCESS: 522 run, 521 PASS + 1 Windows-only SKIP; offline Chromium, local-file and A4 checks PASS.
- [CodeQL #43609470563](https://github.com/hibi89/data2web_studio/actions/runs/43609470563) SUCCESS; [final blueprint gate #43609470850](https://github.com/hibi89/data2web_studio/actions/runs/43609470850) SUCCESS, but reports no approved evidence manifest and no official score.

기준 scorecard는 33/100, 22 VERIFIED, 11 PENDING, 72/100(+0)이다. 검증 코드/워크플로우 SHA는 `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`; 문서 갱신은 docs-only `[skip ci]`이다. 전체 522-test discovery와 A25 19/19, A26 24/24, R29 synthetic preaudit 7/7을 Windows/Ubuntu/macOS에서 통과했다. Exact browser/UI checks와 CodeQL도 성공했으며 final gate는 evidence manifest가 없어 공식 점수를 주지 않았다. 실제 owner/customer/independent-audit evidence는 미확보로 계속 차단한다.

# DATA2WEB Studio — Codex GPT-6 Luna Max · GitHub-only M85 실행 공시

**기준:** 2026-11-14 22:44 KST · 저장소 `hibi89/data2web_studio` · 브랜치 `feature/final-blueprint-p85-evidence-20261113` · Draft [PR #4](https://github.com/hibi89/data2web_studio/pull/4) · 공시 직전 HEAD `1c582db78fb3ac91f37ddbab27b18124c08a5419`.

> **현 공식 최종완성률 72/100. 85까지 +13점은 목표지, 달성 판정이 아니다.** R01–R33 전체 33개/100점 중 22 VERIFIED(72점), 11 PENDING(28점). 이번 공시는 개발 실행 계획일 뿐 점수 승격·출시·판매를 의미하지 않는다. `[작업중]`, `RELEASE HOLD / SALE NO-GO` 유지.

## 1. 담당·정본·실행 환경 고정

- **실행자:** Codex GPT-6 Luna Max. 기존 WBS `INSTANT` 태스크의 담당자를 이 M85 실행에 한해 Codex로 대체한다. **최종 검수자:** ChatGPT GPT-6 High(구현 담당자와 분리된 코드 감사). High도 독립 외부감사(R29)를 대체하지 않는다.
- **정본 읽기 순서:** `HANDOFF.md` → `STATUS.md` → `AGENTS.md` → `REQUIREMENTS.md` → `docs/FINAL_DESIGN.md` → `data/final_blueprint_scorecard_v1.json` → 이 문서 → `data/codex_gpt6_luna_max_m85_github_only_tasks_v1.json` → 실제 소스/CI.
- **방식:** GitHub 원격 저장소·PR #4·기존 GitHub Actions(무료 할당 범위)에서만 개발/테스트/인수인계. 사용자 PC/Windows 로컬 체크아웃·로컬 CLI·외부 AI 분석 서비스·새 Vercel 프로젝트·추가 결제·보안/권한/시크릿 변경 금지. GitHub-hosted Windows는 로컬 장비가 아니므로 기존 CI로만 사용한다.
- 고객 실자료·소스코드 비공개 사본·식별가능 증빙·토큰은 GitHub에 올리지 않는다. 합성 fixture만 새로 만들어 회귀를 진행하고 실제 권리/동의/운영 파기는 사칭하지 않는다.
- 원본 REA_Web, 기존 고객 출력·결과물, `main`, PR Draft/미병합, 고정 R01–R33 배점, 이미 성공한 기능은 보존. 기존 브랜치에 최소 변경 + 회귀. 새 저장소/브랜치/무의미한 빈 커밋/force push/무단 병합·릴리스 금지.
- 코드·테스트마다 **변경 SHA → Action Run ID·Job 상태 → PASS/FAIL/SKIP·OS/브라우저 → 보안/기능 결과**를 기록. 비필수 CI는 묶어서 실행해도 되지만, 새 코드에 대한 정확 SHA 테스트 없이 완료 또는 점수 상승 선언 금지. Actions 한도/실패 시 이유·증거를 적고 병렬 정적 검토로 전환한다.

## 2. 전략 비교·선택

- **안1 기존 50작업 JSON 직접 변형:** 단일 파일은 간결하나 다른 85→100 작업과 담당 기록 및 이미 확정한 의존성을 훼손할 위험이 크다.
- **안2 M85 전용 추적 문서+파생 태스크 JSON:** 34개(P00~P03 4개 + M85 30개)의 정본 ID·의존성·수용 조건을 그대로 참조하고 최신 이행/차단 이력을 덧입힌다. **이 안을 선택.** 원본 `data/gpt6_execution_plan_r01_r33_v1.json`을 수정하지 않는다.

## 3. M85 점수 및 선행 차단표

| 요구 | 점수 | 연결 작업 | GitHub에서 가능한 일 | 현재 비대체 차단 증거 |
|---|---:|---|---|---|
| R07 원본/사용권·동의 | +2 | `A07-01 → A07-02 → A07-03 → A07-04 → A07-05` | 사전동의·원본 불변·변경 시 동의 초기화·HOLD 회귀 | 고객별 실제 사용·공유·가공 허락 및 수권 증거 |
| R21 배포물/권리·NOTICE | +4 | `A21-01 → A21-02 → A21-03 → A21-04 → A21-05 → A21-06` | ZIP 목록·소스 출처 6/6 정합성·검증기 및 LICENSE-gate 회귀 | 실제 권리자·제3자 상용 재배포 허락/NOTICE 의무 판단 |
| R25 보유·파기 | +2 | `A25-01 → A25-02 → A25-03 → A25-04` | 이미 승인된 7개 정책 유지, 합성 삭제 증빙, 기한·구조변조·극단일자 회귀 | 실제 운영 주체의 고객별 인수/보관/반환·파기 입증(단순 합성 PASS 불충분) |
| R26 개인정보 범위 | +2 | `A26-01 → A26-02 → A26-03 → A26-04` | 개인·민감정보 기본 HOLD, 명시적 평문/권리 승인 및 GUI 상태 재설정 회귀 | 구체 고객 처리 근거와 정보주체·고객 사용 동의/비개인 범위 결정 |
| R29 보안 | +3 | `A29-01 → A29-02 → A29-03 → A29-04 → A29-05 → A29-06 → A29-07` | 공격 행렬, 합성 취약점 회귀, 기존 CodeQL, 공개 소스 SHA 고정 감사 패킷 | **실제 독립 외부감사자**의 검증/결함 재확인. Codex·High·CodeQL 자기감사 불인정 |
| **합계** | **+13** | **30개 M85 + 4개 준비 = 34개** | | **차단 증거가 없으면 72 유지** |

## 4. 실행 순서(반복 `ㄱ` 또는 Codex 연속 실행)

1. **GitHub 상태 동기화:** P00~P02는 기존 문서 증거가 존재하므로 처음부터 재구현하지 말고 SHA/정확성만 재검증. P03에서 최근 커밋이 포함된 최신 HEAD 기준 기존 Actions와 새 음수 테스트가 실행됐는지 확인한다.
2. **무료 작업 묶음 A — 이전 미검증 코드 재확인:** A07-03(동의 초기화와 확인 창 이전 fail-closed), A25-01(보존 보고서 모순·비정상 UTF-8·연도9999), A26-02(민감/권리 승인 초기화), A29-01(경로·ZIP·XLSX 공격행렬). 누락 테스트만 최소 구현하고 기존 hosted Windows/Ubuntu/Chrome/Edge/Chromium에서 정확 SHA 증거 확보.
3. **무료 작업 묶음 B — 출처/권리·운영:** A21-01/A21-02 기존 출처 목록/권리 공백 점검; A07-01/02·A25-02·A26-01 기존 안내/양식 확인. 실제 권리/개인정보를 가상 승인하지 말고 검증 가능한 작은 기술 결함만 수정한다.
4. **독립 작업 묶음 C — 보안 감사 준비:** A29-01/A29-02 공개 소스·합성 테스트·고정 SHA·범위·잠재 취약점/누락 목록을 작성한다. CodeQL과 내부 테스트는 사전감사로만 표시. 외부 전송·유료 감사·권한 요청을 자동 수행하지 않는다.
5. **차단 처리:** A07-04/A21-03/A25-03/A26-03/A29-03은 소유자/법적 권리 판단, A29-04/A29-06은 실제 외부 독립 검증. 비공개 자료를 업로드하지 않고 **증거가 없으면 BLOCKED_OWNER / BLOCKED_EXTERNAL**. 승인된 R25 운영 정책과 합성 파기 PASS는 이미 확보했으므로 다시 사용자에게 승인을 묻지 않는다. 실제 고객 데이터는 절대 임의 수집·삭제하지 않는다.
6. **후속 조건부 작업:** 실제 권리자 결정 뒤 A21-04/05, 권리·동의/외부 감사 뒤 A07-05/A21-06/A25-04/A26-04/A29-05/07. 고객 또는 제3자 승인 전 LICENSE/NOTICE 생성·출고/판매 금지.
7. **M85 수용 G85-01~04:** 다섯 요구 각각의 실제 증거를 독립 확인하고 GitHub-hosted 정확 SHA Python/브라우저/CodeQL/보안 테스트 PASS 후에만 잠금 scorecard의 5개 state를 변경해 합계85 확인. 고객 사용/출시는 계속 HOLD. 단 한 요구라도 미충족이면 **진행률 72/100 유지**하고 미완료 ID·필요 증거·기술적 잔여를 기록한다.

## 5. 실행 단위별 상세 명세 — 원본 WBS 그대로, Codex 담당으로 연결

아래 `RECORDED_*`는 기존 문서 이력이고 현 SHA의 기능 PASS는 아니다. `CODE_AND_TEST_COMMITTED_CI_PENDING`은 **코드가 있다고 하여 테스트 완료가 아님**을 뜻한다. 원본 작업의 `blocked_by`는 유지. 완전 수용되지 않는 작업별 부분 가점은 전부 0.

### P00 · PREP/GATE · Codex · COMPLETE_READ_ONLY_RECHECK
- 선행: 없음. 
- 실행: Read HANDOFF→STATUS→AGENTS→REQUIREMENTS→FINAL_DESIGN→scorecard→latest source; compare repo branch and PR SHA.
- 수용: Enumerate actual 33/100, 22 VERIFIED, 11 PENDING, latest tested code SHA separately from docs HEAD.
- 증거: Read-only SHA, scorecard contract, baseline diff in STATUS.
- GitHub Actions 내부 테스트: `python blueprint_score.py`, `python -m unittest test_blueprint_score -v`.
- 관련 파일: `HANDOFF.md`, `STATUS.md`, `data/final_blueprint_scorecard_v1.json`. **작업 자체 가점: 0**.

- 11/15 exact-SHA recheck: HEAD/PR/scorecard and the historical 100-point baseline were read from GitHub; `blueprint_score.py` returned 72/100. `test_blueprint_score` ran under full unittest discovery; its standalone command was not invoked separately.
### P01 · PREP/GATE · Codex · RECORDED_RECHECK
- 선행: P00. 
- 실행: Secure previous non-destructive rollback reference and inventory customer/REA_Web protected paths; check auth identity, existing branch and CI budget.
- 수용: Explicit rollback SHA and original/no-overwrite boundary; no new branch/release/repo/rights change.
- 증거: Git commit parent SHA + protected paths listed; no private materials.
- GitHub Actions 내부 테스트: `python -m unittest test_customer_folder -v`.
- 관련 파일: `AGENTS.md`, `docs/ORIGIN_AND_LICENSE.md`. **작업 자체 가점: 0**.

### P02 · PREP/GATE · Codex · RECORDED_RECHECK
- 선행: P00. 
- 실행: Open evidence index per R with unique opaque IDs and a public-safe checklist; no customer names, data, screenshots, private paths or permission tokens.
- 수용: Each R07/R21/R25/R26/R29 evidence indexed as VERIFIED/INCOMPLETE/MISSING without assigning points.
- 증거: New redacted evidence reference index and missing list.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`, `docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md`. **작업 자체 가점: 0**.

### P03 · PREP/GATE · Codex · PASS_EXACT_SHA_CI
- 선행: P00. 
- 실행: Freeze regression commands against the last feature SHA; classify existing hosted/synthetic results as such, no buyer-acceptance assertion.
- 수용: No regression and no mistaken CI-Ready=customer-approved claim.
- 증거: Test run URLs exact SHA, PASS/FAIL/SKIP log and OS/browser scope.
- 11/14 최신 증거 주의: Run full hosted regression at the new exact SHA; do not recycle earlier 507/506 PASS as latest.
- GitHub Actions 내부 테스트: `python -m unittest discover -v`, `python shipping_rights_preflight.py`, `python zero_cost_gate.py`.
- 관련 파일: `test_blueprint_score.py`, `shipping_rights_preflight.py`. **작업 자체 가점: 0**.

- 11/15 exact-SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`: full discovery, `shipping_rights_preflight.py`, `zero_cost_gate.py`, source provenance, focused A25/A26 modules, browser/UI and synthetic preaudit completed; OS-specific PASS/SKIP and run URLs are in STATUS/HANDOFF. This remains synthetic/hosted evidence, not buyer acceptance.
### A07-01 · R07 · Codex · STATIC_EVIDENCE_RECHECK
- 선행: P02. 
- 실행: Map raw-source custody, user-of-record, owner-created copies, browser plaintext output and shared-data rights; reuse existing order_intake_preflight to avoid duplicate workflow.
- 수용: Data flow states input rights, no cloud upload, source hash invariance, unsafe types HOLD; missing legal rights clearly isolated.
- 증거: Redacted dataflow/threat review linked to source SHA.
- GitHub Actions 내부 테스트: `python -m unittest test_order_intake_preflight -v`.
- 관련 파일: `order_intake_preflight.py`, `docs/A_CUSTOMER_INTAKE_AND_DELIVERY_QA_DRAFT_20261114.md`. **작업 자체 가점: 0**.

### A07-02 · R07 · Codex · TEMPLATE_RECORDED
- 선행: A07-01. 
- 실행: Prepare per-order right-to-use/transform/distribute confirmation checklist, user/third-party shared rights distinction, plaintext delivery and revocation triggers; only anonymous template.
- 수용: Specific customer/source/authority/consent/date scope fields for future private records; no fictional signatures or third-party agreement.
- 증거: Unfilled and redacted customer-rights form; review labels not approvals.
- GitHub Actions 내부 테스트: `python -m unittest test_order_intake_preflight -v`.
- 관련 파일: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`. **작업 자체 가점: 0**.

### A07-03 · R07 · Codex · PASS_EXACT_SHA_CI
- 선행: A07-02. 
- 실행: Audit both desktop single/batch consent-reset paths and CLI on source/sheet/header/ID mapping/file replacement; fix only reproduced omission.
- 수용: Invalid/missing consent or changed input fails closed; source bytes and existing customer outputs identical to pretest.
- 증거: Synthetic changed-source SHA, direct CLI and GUI regression evidence.
- 11/14 최신 증거 주의: Re-run consent reset and pre-confirmation gates in existing GitHub Actions; verify Windows hosted Tk and malicious metadata paths.
- GitHub Actions 내부 테스트: `python -m unittest discover -v`.
- 관련 파일: `data2web_desktop.py`, `data2web_single.py`, `data2web_append.py`, `test_acceptance.py`. **작업 자체 가점: 0**.

- 11/15 exact-SHA evidence: full discovery and hosted Windows Tk single/batch consent-reset flows, Chrome/Edge and Chromium local-file flows PASS. No actual rights/consent acceptance is implied.
### A07-04 · R07 · OWNER · BLOCKED_OWNER
- 선행: A07-02, A07-03. **차단:** NON_DELEGABLE_RIGHTS_AND_CUSTOMER_CONSENT.
- 실행: Confirm actual rights/authority and obtain specific owner/provider permission plus scope for one authorized acceptance case using approved private/local channel only.
- 수용: Real source authorization and consent can be independently checked; no private proof or source uploaded to public GitHub/ChatGPT.
- 증거: Owner/customer dated authorization held privately; GitHub only opaque status/reviewer reference.
- GitHub Actions 내부 테스트: 해당 없음(OWNER/EXTERNAL 인증을 자체 테스트로 대체 불가).
- 관련 파일: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`. **작업 자체 가점: 0**.

### A07-05 · R07 · Codex · REVALIDATE
- 선행: A07-01, A07-03, A07-04. 
- 실행: Review rights/consent provenance and source-before/after SHA, exact tested code SHA and residual privacy limits.
- 수용: Entire R07 source preservation + actual rights/consent satisfied; otherwise leave R07 PENDING.
- 증거: Signed/referenced Instant item-level review without customer data in repo.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `data/final_blueprint_scorecard_v1.json`. **작업 자체 가점: 0**.

### A21-01 · R21 · Codex · TECHNICAL_RECHECK_PASS_EXACT_SHA
- 선행: P01, P02. 
- 실행: Reconcile actual zipped HTML, manifest and README with local receipt, source Git blob pins, all shipped CSS/JS/vendor assets, excluded EXE/test deps.
- 수용: Complete real A shipping inventory vs whitelist; all provenance unknowns labeled pending, no fake LICENSE.
- 증거: Git-linked inventory with source SHA and actual synthetic ZIP member evidence.
- GitHub Actions 내부 테스트: `python shipping_rights_preflight.py`, `python r21_source_provenance.py`.
- 관련 파일: `data/shipping_rights_inventory_v1.json`, `data/r21_source_provenance_v1.json`, `docs/R21_R33_SHIPPING_LICENSE_INVENTORY_20261114.md`. **작업 자체 가점: 0**.

- 11/15 exact-SHA: `r21_source_provenance.py` confirmed six source blob pins and `shipping_rights_preflight.py` confirmed four synthetic artifact integrity checks. Owner/third-party commercial rights and LICENSE/NOTICE remain pending.
### A21-02 · R21 · Codex · TECHNICAL_RECHECK_PASS_EXACT_SHA
- 선행: A21-01. 
- 실행: For every shipped asset/derivation enumerate author, origin SHA, upstream reference, vendor license/NOTICE obligations and unresolved chains; do not infer IP ownership from AI generation or GitHub owner.
- 수용: Every actually shipped text/JS/CSS artifact has a rights-evidence or explicit unresolved flag; no accidental EXE bundling.
- 증거: Versioned chain-of-title/third-party dependency matrix, unknowns kept as blockers.
- 11/14 최신 증거 주의: Read the existing 6/6 source Git blob provenance evidence but keep derived-work/notice commercial rights unresolved.
- GitHub Actions 내부 테스트: `python shipping_rights_preflight.py`.
- 관련 파일: `docs/ORIGIN_AND_LICENSE.md`, `docs/R21_SOURCE_PROVENANCE_EVIDENCE_20261114.md`. **작업 자체 가점: 0**.

- 11/15 exact-SHA: six pinned producers are reproducible; owner/third-party chain-of-title, redistribution and notice decisions remain pending.
### A21-03 · R21 · OWNER · BLOCKED_OWNER
- 선행: A21-02. **차단:** RIGHTSHOLDER_IP_THIRD_PARTY_LICENSE_NOTICES.
- 실행: Obtain actual rights-holder confirmation or license for derived code/templates, commercial redistribution scope and any third-party NOTICE; explicitly decide customer usage terms.
- 수용: Rights documents and each required notice licensed for the actual A deliverable; not merely owner planning direction.
- 증거: Private owner/legal/rights-holder evidence and public-safe approval scope, reviewer ID.
- GitHub Actions 내부 테스트: 해당 없음(OWNER/EXTERNAL 인증을 자체 테스트로 대체 불가).
- 관련 파일: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`. **작업 자체 가점: 0**.

### A21-04 · R21 · Codex · REVALIDATE
- 선행: A21-03. 
- 실행: Only after verified rights decision: choose (1) no extra member when legally justified; or (2) versioned approved LICENSE/NOTICE packaging contract, migrating builder/verifier/receipt together without breaking v1.
- 수용: Allowed contents match actual authorized rights text and deterministic ZIP, versioned v2 when needed; no overwrite, no invented license.
- 증거: Exact legal text provenance ref, package contract version, signed owner authorization, code diff.
- GitHub Actions 내부 테스트: `python -m unittest test_shipping_rights_preflight -v`, `python -m unittest test_customer_folder -v`.
- 관련 파일: `delivery.py`, `verify_delivery.py`, `verify_customer_folder.py`. **작업 자체 가점: 0**.

### A21-05 · R21 · Codex · REVALIDATE
- 선행: A21-04. 
- 실행: Run synthetic allowed/forbidden license member, duplicate/ZIP-slip/modified notice, old v1 compatibility, receipt hash and create-only failure rollback.
- 수용: Valid authorized package passes independent verifier; malicious/unapproved member and old-data corruption fail closed, old v1 still accepted.
- 증거: Windows/Ubuntu and Chrome/Edge exact-SHA source/test evidence, ZIP hash and manifest contract.
- GitHub Actions 내부 테스트: `python -m unittest discover -v`, `python shipping_rights_preflight.py`.
- 관련 파일: `test_shipping_rights_preflight.py`, `test_customer_folder.py`. **작업 자체 가점: 0**.

### A21-06 · R21 · Codex · REVALIDATE
- 선행: A21-03, A21-05. 
- 실행: Review owner/third-party rights proof, final shipped bytes and license text/NOTICE obligations, migration, exact-SHA CI.
- 수용: Entire R21 including real commercial use permission and v1/v2 verifier correctness accepted or 4 points stay pending.
- 증거: Instant item review and exact rights decision reference, not hypothetical license.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `data/final_blueprint_scorecard_v1.json`. **작업 자체 가점: 0**.

### A25-01 · R25 · Codex · PASS_EXACT_SHA_CI
- 선행: P02. 
- 실행: Map owner-approved max 7-day temporary operator copy, earlier purpose-completion handling, legal exceptions, originals/outputs never auto-delete; compare current retention utility.
- 수용: No accidental deletion/upload; policy mismatch fails closed and actual disposal is not certified by metadata.
- 증거: Policy-vs-code map and synthetic time boundary tests.
- 11/14 최신 증거 주의: R25 seven-policy owner approval and isolated synthetic delete PASS already recorded; run new unexecuted max-date/invalid UTF-8/contradictory report negative tests on hosted runner.
- GitHub Actions 내부 테스트: `python -m unittest test_operator_copy_retention -v`.
- 관련 파일: `operator_copy_retention.py`, `data/zero_cost_owner_policy_v1.json`. **작업 자체 가점: 0**.

- 11/15 exact-SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`: direct `python -m unittest test_operator_copy_retention -v` PASS 19/19 on Windows, Ubuntu and macOS; full discovery PASS with one Windows-only skip on Ubuntu/macOS. Includes invalid UTF-8, extreme dates and forged-report regressions; no real disposal is certified.
### A25-02 · R25 · Codex · TECHNICAL_TEMPLATE_AND_TESTS_PASS_EXACT_SHA
- 선행: A25-01. 
- 실행: Prepare an unfilled custody/owner role, where/when data copied, rights, purpose, manual deletion or return authority, legal exception and record checklist.
- 수용: Customer source and result retention separate; explicit records for custody, expiry, action and no-copy case; no customer identifiers in public repo.
- 증거: Redacted receipt/retention notice and operator manual checklist.
- 11/15: the blank custody/retention form is committed; exact SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661` direct retention command PASS 19/19 on Windows, Ubuntu and macOS. The seven owner-approved internal policies and prior synthetic deletion drill remain recorded; no actual customer custody/disposal record exists.
- GitHub Actions 내부 테스트: `python -m unittest test_operator_copy_retention -v`.
- 관련 파일: `docs/R07_R25_R26_LOCAL_COPY_RETENTION_20261114.md`, `docs/A25_02_COPY_CUSTODY_RECORD_TEMPLATE_20261115.md`. **작업 자체 가점: 0**.

### A25-03 · R25 · OWNER · POLICY_APPROVED_SYNTHETIC_PASS_REAL_EVIDENCE_BLOCKED
- 선행: A25-02. **차단:** NON_DELEGABLE_OPERATOR_RETENTION_AND_DISPOSAL_EVIDENCE.
- 실행: Actually confirm responsible operator, permitted custody, disposal/return procedure and where separate private evidence is retained; execute a real authorized no-copy/copy-retention acceptance trace.
- 수용: Owner explicitly owns policy and genuine handling log exists; never claim physical deletion without action evidence.
- 증거: Private acceptance evidence/ref, public-safe policy signoff only.
- 11/14 최신 증거 주의: Owner named as operator and approved policy, NOT proof of real customer custody/deletion; actual authorized evidence remains unavailable under no-local/no-customer constraint.
- GitHub Actions 내부 테스트: 해당 없음(OWNER/EXTERNAL 인증을 자체 테스트로 대체 불가).
- 관련 파일: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`. **작업 자체 가점: 0**.

### A25-04 · R25 · Codex · REVALIDATE
- 선행: A25-01, A25-03. 
- 실행: Compare actual operator evidence with source-preservation, duration and manual-only protocol; check legal exceptions not silently bypassed.
- 수용: Complete R25 policy notice and actual accountable practice satisfied; else hold.
- 증거: Instant item review plus retention acceptance reference.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `data/final_blueprint_scorecard_v1.json`. **작업 자체 가점: 0**.

### A26-01 · R26 · Codex · TECHNICAL_MATRIX_AND_TESTS_PASS_EXACT_SHA
- 선행: P02. 
- 실행: Reconcile personal/sensitive/medical/payment identifiers, shared/confidential, unknown scope, allowed nonpersonal only; map plaintext and offline exposure.
- 수용: Default HOLD for personal/sensitive/unclear rights and explicit safe classification; no encryption/anonymous-data fiction.
- 증거: Synthetic privacy class matrix, mappings and negative cases.
- 11/15: V2 explicit privacy class/matrix and fail-closed cases; exact SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661` direct `python -m unittest test_order_intake_preflight -v` PASS 24/24 on Windows, Ubuntu and macOS. Classification remains self-reported, not detection or legal basis.
- GitHub Actions 내부 테스트: `python -m unittest test_order_intake_preflight -v`.
- 관련 파일: `order_intake_preflight.py`, `test_order_intake_preflight.py`, `data2web_desktop.py`, `docs/A26_01_PRIVACY_SCOPE_MATRIX_20261115.md`. **작업 자체 가점: 0**.

### A26-02 · R26 · Codex · CODE_AND_TEST_PASS_EXACT_SHA
- 선행: A26-01. 
- 실행: Audit frontend checkbox reset for replaced/altered source, rights, plaintext and privacy classification across single and batch; update tests only for reproduced gap.
- 수용: No persistence of stale sensitive approval across dataset revisions; file values not sent over network.
- 증거: CI/browser negative-flow evidence, clear notices/HOLD response.
- 11/15 exact-SHA evidence: direct A26 module 24/24 PASS on Windows/Ubuntu/macOS, full suite PASS, plus hosted Windows Tk single/batch consent-reset and Chrome/Edge/Chromium file:// flows PASS. Customer-specific privacy basis and consent remain blocked.
- GitHub Actions 내부 테스트: `python -m unittest discover -v`.
- 관련 파일: `data2web_desktop.py`, `browser_final_blueprint_probe.py`. **작업 자체 가점: 0**.

### A26-03 · R26 · OWNER · BLOCKED_OWNER
- 선행: A26-01, A26-02. **차단:** NON_DELEGABLE_PER_CUSTOMER_PRIVACY_CONSENT.
- 실행: For an actual lawful use case obtain owner and client decisions about data type/accessors/retention/transfers, explicit plaintext use and whether sensitive-data flow is rejected.
- 수용: Specific scoped customer agreement or documented nonpersonal-only boundary; no blanket approval inferred.
- 증거: Private dated consent and operator acceptance; public-safe redacted reference.
- GitHub Actions 내부 테스트: 해당 없음(OWNER/EXTERNAL 인증을 자체 테스트로 대체 불가).
- 관련 파일: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`. **작업 자체 가점: 0**.

### A26-04 · R26 · Codex · REVALIDATE
- 선행: A26-02, A26-03. 
- 실행: Verify privacy scope and actual permission against implementation and plaintext warnings; never treat program checkbox alone as legal agreement.
- 수용: Full R26 personally sensitive data handling/rejection and real consent scope accepted; otherwise pending.
- 증거: Instant item review plus consent reference.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `data/final_blueprint_scorecard_v1.json`. **작업 자체 가점: 0**.

### A29-01 · R29 · Codex · INTERNAL_PREAUDIT_PASS_EXACT_SHA_EXTERNAL_PENDING
- 선행: P01, P02. 
- 실행: Freeze independent evaluator's threat scope: XSS/CSP/CSV formula, XLSX zip bomb and XML entities, ZIP/receipt, TOCTOU symlink/hardlink/junction, interruptions, offline network.
- 수용: Threat matrix has reproducible positive/negative test cases, supported OS constraints and residual risks; no claim of external audit.
- 증거: Synthetic case inventory, fixture hashes, exact source SHA.
- GitHub Actions 내부 테스트: `python security_audit_preaudit.py`, `python -m unittest discover -v`.
- 관련 파일: `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`. **작업 자체 가점: 0**.

- 11/15 exact SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`: internal `security_audit_preaudit.py` reported 7/7 synthetic checks PASS on Windows/Ubuntu/macOS; full suite and CodeQL passed. No independent real-OS security audit is claimed.
### A29-02 · R29 · Codex · INTERNAL_PREAUDIT_PASS_EXACT_SHA_EXTERNAL_PENDING
- 선행: A29-01. 
- 실행: Prepare public-source-only reproducible audit bundle/instructions, source freeze and risk register, with existing internal CodeQL and browser CI clearly labeled self-check.
- 수용: Another evaluator can independently run tests without customer data, secrets, private access or false PASS.
- 증거: SHA-pin commands/expected outputs and failure reporting template.
- GitHub Actions 내부 테스트: `python security_audit_preaudit.py`, `python shipping_rights_preflight.py`.
- 관련 파일: `docs/R29_SYNTHETIC_PREAUDIT_HANDOFF_20261114.md`. **작업 자체 가점: 0**.

- 11/15 exact SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`: audit handoff updated with exact source pin, repeatable commands and current hosted evidence. High internal follow-up found no actionable workflow issue; Codex/High/CodeQL remain self-checks, and external audit/findings/retest are still missing.
### A29-03 · R29 · OWNER · BLOCKED_OWNER
- 선행: A29-02. **차단:** INDEPENDENT_REVIEWER_AND_EXTERNAL_DISCLOSURE_APPROVAL.
- 실행: Select/approve a genuinely independent external reviewer and specific scope, any agreement or public-source sharing, zero-cost budget; no paid purchase or access grant absent new approval.
- 수용: Documented external evaluator independence, permitted public-only materials and no unauthorized spend/transmission.
- 증거: Owner approval/evaluator identity scope held privately, public-safe reference.
- GitHub Actions 내부 테스트: 해당 없음(OWNER/EXTERNAL 인증을 자체 테스트로 대체 불가).
- 관련 파일: `docs/OWNER_APPROVAL_PACKET_A_20261114.md`. **작업 자체 가점: 0**.

### A29-04 · R29 · EXTERNAL · BLOCKED_EXTERNAL
- 선행: A29-03. **차단:** REAL_INDEPENDENT_HUMAN_AUDIT_REQUIRED.
- 실행: Independently reproduce attack matrix against frozen exact SHA in real supported environments and issue dated findings with severity, omissions, environment, command logs.
- 수용: Actual independent signed/attributable findings and limit descriptions, not a self-run AI/CodeQL report.
- 증거: External SHA-pinned review report, anonymized location and finding IDs.
- 11/14 최신 증거 주의: External real-independent person or qualified organization required; CodeQL, second model and Codex self-audit are NOT independent attestation.
- GitHub Actions 내부 테스트: 해당 없음(OWNER/EXTERNAL 인증을 자체 테스트로 대체 불가).
- 관련 파일: `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`. **작업 자체 가점: 0**.

### A29-05 · R29 · Codex · REVALIDATE
- 선행: A29-04. 
- 실행: Implement least-invasive fixes for confirmed external findings, preserve originals/v1 ZIP and no-network contract, add reproducing regressions.
- 수용: Each finding has fix commit or documented accepted blocker, Windows/Ubuntu/browser CI on exact fix SHA.
- 증거: Finding→fix SHA→test table, data and secrets absent.
- GitHub Actions 내부 테스트: `python -m unittest discover -v`, `python blueprint_score.py`.
- 관련 파일: `path_policy.py`, `verify_delivery.py`, `verify_customer_folder.py`. **작업 자체 가점: 0**.

### A29-06 · R29 · EXTERNAL · BLOCKED_EXTERNAL
- 선행: A29-05. **차단:** EXTERNAL_RETEST_AND_SIGNOFF.
- 실행: Same independent evaluator retests fixes on new SHA, records unfixable risks, gaps, and signoff/remaining-blocker status.
- 수용: External final retest confirms closure or explicitly blocks R29; no self-signed completion.
- 증거: Independent dated recheck SHA report, signed/attributable reviewer.
- GitHub Actions 내부 테스트: 해당 없음(OWNER/EXTERNAL 인증을 자체 테스트로 대체 불가).
- 관련 파일: `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`. **작업 자체 가점: 0**.

### A29-07 · R29 · Codex · REVALIDATE
- 선행: A29-04, A29-06. 
- 실행: Independently review external reviewer identity, scope completeness, outstanding findings, SHA and field/OS limits; don't conflate Instant with external.
- 수용: Complete R29 acceptance only after external signoff and verified no blocking findings; else PENDING.
- 증거: Instant R29 score review linking external IDs and code SHA.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `data/final_blueprint_scorecard_v1.json`. **작업 자체 가점: 0**.

### G85-01 · PREP/GATE · Codex · REVALIDATE
- 선행: A07-05, A21-06, A25-04, A26-04, A29-07. 
- 실행: Assemble five complete item-level evidence packets with provenance and no private material in repo; reconcile 2+4+2+2+3 points.
- 수용: Each requirement fully accepted independently; none receives partial point for templates, self tests or false attestations.
- 증거: R07/R21/R25/R26/R29 acceptance matrix, exact SHA of reviewed functionality.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `docs/FINAL_BLUEPRINT_WEIGHTING_100_APPROVED_20261114.md`. **작업 자체 가점: 0**.

### G85-02 · PREP/GATE · Codex · REVALIDATE
- 선행: G85-01. 
- 실행: Run last exact-code-SHA Windows/Ubuntu Python, Chrome/Edge/Chromium, portable v1/v2, privacy/R21/R29 regression and CodeQL using existing free runners.
- 수용: All required CI jobs SUCCESS at exact code SHA with PASS/FAIL/SKIP, browser assets/API/zip/receipt intact; buyer acceptance separate.
- 증거: Actions URL/run/job, browser and no-network evidence; no doc-SHA confusion.
- GitHub Actions 내부 테스트: `python -m unittest discover -v`, `python blueprint_score.py`, `python shipping_rights_preflight.py`.
- 관련 파일: ` .github/workflows/python-tests.yml`, `.github/workflows/final-blueprint-gate.yml`. **작업 자체 가점: 0**.

### G85-03 · PREP/GATE · Codex · REVALIDATE
- 선행: G85-02. 
- 실행: Only if five full acceptance proofs exist and Instant item evidence checks agree, update those five R states in existing 100-point locked scorecard; no weight changes; run score checker.
- 수용: Score mechanically equals 85/100, 33 items and 100 denominator unchanged, all five VERIFIED and other six PENDING; publish audit diff.
- 증거: Scorecard JSON diff, exact SHA score command and evidence links.
- GitHub Actions 내부 테스트: `python blueprint_score.py`, `python -m unittest test_blueprint_score -v`.
- 관련 파일: `data/final_blueprint_scorecard_v1.json`, `blueprint_score.py`. **작업 자체 가점: 0**.

### G85-04 · PREP/GATE · Codex · REVALIDATE
- 선행: G85-03. 
- 실행: Instant 85 milestone evidence gate (High final review only after 100): confirm source SHA CI, complete real rights/consent/retention/legal/independent audit evidence, no sale or customer upload authorized by score.
- 수용: Authorize 85 report only when all five complete; otherwise return blocked IDs to Instant and preserve prior score; keep RELEASE HOLD.
- 증거: Instant acceptance memo with item verdicts, STATUS/HANDOFF consistency.
- GitHub Actions 내부 테스트: `python blueprint_score.py`.
- 관련 파일: `STATUS.md`, `HANDOFF.md`. **작업 자체 가점: 0**.


## 6. 최종 보고 및 인수인계 계약

- 매 의미 있는 변경 후 `STATUS.md` 및 `HANDOFF.md`: 정확 브랜치 HEAD/코드 SHA/테스트 SHA, 100점/33요구 점수표, 완료·대기·차단 ID, run URL와 PASS/FAIL/SKIP, 기능별 증거·미검증, 원본/backup/권한/데이터 무변경, 다음 동작, KST 시각을 갱신한다.
- GitHub 자료 공개 범위는 소스·합성 fixture·비식별된 증거 ID만이다. 실제 고객 동의·권리자 허락·파기 증명·감사자 신원/서명 자료는 공개 커밋 금지. 별도 보관된 실증이 없다면 '미검증' 유지.
- 최종 결과는 `verified_score`, `technical_ready_items`, `nondelegable_blockers`, `exact_code_sha`, `ci_runs`, `main_unchanged`, `release_status`, `next_ids`로 보고. High 검수는 Codex의 기록된 코드/SHA/실증 한계에 대해 수행하며 독립 법률·감사 승인으로 둔갑하지 않는다.

**M85 작업 범위는 문서와 연결된 JSON 34개가 기준.** 과거 표의 담당 `INSTANT`는 이번 실행에서 Codex로 승계하나 OWNER와 EXTERNAL 태스크는 승계하지 않는다.
