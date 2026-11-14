## 2026-11-15 KST · Windows share-deny hardening and exact-SHA review

- Latest tested code/test SHA: `512af5000658f40ed7deefae096f29b886bd1ec0`; product change at `3a6d7588e8f5e58e51b1b0f7e6c1eaf9b2a917cf` opens Windows sources with `CreateFileW(GENERIC_READ, FILE_SHARE_READ)`. The handle denies new write/delete sharing requests and remains open through the final lstat/metadata comparison. POSIX continues through `os.open`.
- At `3a6d758`, the hardlink alias writer was denied, but test code incorrectly required `PermissionError.winerror == 32`; another race test intercepted `os.open`, which Windows no longer calls. `512af500` fixes these tests. Exact-SHA Windows full suite passed 525/525; Ubuntu passed 524 with one Windows-only skip; both affected cases ran on Windows and Ubuntu.
- [Python/browser #43617898725](https://github.com/hibi89/data2web_studio/actions/runs/43617898725), [macOS offline #43617898816](https://github.com/hibi89/data2web_studio/actions/runs/43617898816), [CodeQL #43617898719](https://github.com/hibi89/data2web_studio/actions/runs/43617898719) and [evidence gate #43617898943](https://github.com/hibi89/data2web_studio/actions/runs/43617898943) all completed successfully at this SHA. Chromium, installed Chrome and Edge hosted synthetic browser flows passed.
- GPT-6 High read-only review at `512af500`: no actionable finding. Internal code review and synthetic CI do not meet R29 external audit acceptance.
- **Residual scope:** share-deny narrows concurrent file writes/deletes through standard Windows file sharing. This does not prove an atomic snapshot of directory ancestry; pre-existing writable mappings, privileged/direct-volume mutations, junction/reparse behavior on real supported customer Windows versions, broad malicious-XLSX resource behavior and host-wide egress telemetry remain outside demonstrated coverage.
- R29 remains PENDING. Needed: an owner-approved genuinely independent evaluator and permitted scope, dated independent findings against frozen source/real environments, fixes and regressions for findings, external retest and signoff. Do not substitute GPT-6 High, Codex, CodeQL or hosted synthetic checks.

## 2026-11-14 23:47 KST · High 검수 후속 및 R25/Mac CI 보완
- Read-only High review of `0689ff1..48ea586` found two pre-existing issues: R25 overdue report could suppress the manual-action flag when the reason stayed in privacy/rights HOLD; macOS path filter omitted retention source/test and explicit policy/source/shipping checks.
- At `bfa808b0815b7e5be1bd11de8d6833717be0dcfd`, report contract V2 carries purpose-completion and legal-exception claims and validates the manual-action flag against copy presence, deadline, purpose completion and exception. Added positive legal-exception and negative forged-flag regressions. MacOS path filter now includes `operator_copy_retention.py`, its tests, `zero_cost_gate.py`, source pinning and shipping preflight.
- Follow-up High review confirmed both findings closed and found no new actionable issue. [Python/browser #43606247844](https://github.com/hibi89/data2web_studio/actions/runs/43606247844), [macOS #43606247722](https://github.com/hibi89/data2web_studio/actions/runs/43606247722), [CodeQL #43606247728](https://github.com/hibi89/data2web_studio/actions/runs/43606247728) and [blueprint gate #43606248064](https://github.com/hibi89/data2web_studio/actions/runs/43606248064) all SUCCESS at exact SHA. The review was internal/read-only and **does not satisfy independent external R29 audit**.
- R29 remains PENDING, score addition 0, RELEASE HOLD / SALE NO-GO.

## 2026-11-14 23:31 KST · 최신 exact-SHA 기술 검증 / 외부감사 차단 유지
- 보안 검사 변경: `security_audit_preaudit.py`가 HTML을 파싱해 활성 요소/URI/event 속성을 검사하고 JSON dataset은 데이터로 처리한다. `verify_delivery.py` 및 script hash 회귀 검사는 HTML script 태그 대소문자를 무시하며, 회귀 테스트는 승인된 executable script 블록이 하나만 남는지 비교한다.
- **SHA `48ea586b6ef712176b26c33d1809d3cd9a782d94`:** [Python/browser #43604742332](https://github.com/hibi89/data2web_studio/actions/runs/43604742332) 4/4 SUCCESS (Windows 519/519, Ubuntu 518 PASS+1 Windows-only SKIP, Chromium/Chrome/Edge; hosted Tk UI). [macOS #43604742400](https://github.com/hibi89/data2web_studio/actions/runs/43604742400) SUCCESS (518 PASS+1 SKIP; offline Chromium + A4); [CodeQL #43604742371](https://github.com/hibi89/data2web_studio/actions/runs/43604742371) SUCCESS; [blueprint gate #43604742623](https://github.com/hibi89/data2web_studio/actions/runs/43604742623) SUCCESS.
- b57 SHA의 Python #43603754152 및 macOS #43603754125는 새 테스트가 정상 data-script와 UI executable-script 경계를 오인해 FAIL. 제품 공격 성공 보고가 아니다. assertion을 `21a6fda`에서 executable script만 비교하도록 최소 수정했고 위의 `48ea586` exact-SHA 전체 검증과 macOS 재검증에서 PASS. CodeQL 인라인 3개 review thread는 corrected scan 후 resolved/outdated 상태.
- 이 모든 결과는 내부 자체/합성·hosted CI. **독립 외부 보안 감사, 외부 findings/retest/signoff는 수행되지 않았으며 R29 PENDING, score addition 0.** Windows10/11 실제 고객기기, 고급 NTFS/TOCTOU independent audit, 고객 data 및 IP/개인정보 승인 필요. RELEASE HOLD / SALE NO-GO 유지.

# R29 전환 실행 — 독립 감사용 합성 보안 사전증거 (2026-11-14 KST)

## 차단·피벗 분석
- **현재 법적/외부 차단:** 최종설계 72/100에서 85까지13점의 후보 R07(2)+R21(4)+R25(2)+R26(2)+R29(3) 중 R29는 **제품 개발자와 다른 독립 보안 평가자가 실제 코드를 감사하고, 발견 위험을 조치 후 재검증하는 조건**이 있음. AI의 자체 테스트를 외부 감사라고 바꿔 부를 수 없음.
- **대안 A (선택):** 독립 전문가에게 넘길 수 있는 단일 reproducible 내부 합성 pre-audit 실행기/증거 JSON + 정확 Git SHA/위협 매트릭스. 초기 현금비용/API0, 고객 자료 0, 실체 보안검증 반복 가능. 다만 실제 독립 검증자 승인·소스 접근·보고서까지는 별도.
- **대안 B (보류):** 상품 가중치/R29 정의를 85점 목표에 맞게 수정하거나, 스스로 감사자로 간주. 비용 낮지만 사용자가 승인한 최종설계·가중치 위조가 되므로 **불가**.
- **대안 C (별도 협의):** 계약된 독립 보안 전문가를 외부 서비스로 의뢰. 인력 비용/자료 제공·접근범위/법적 계약·NDA 확인 필수, **사용자 별도 승인 전 호출·비밀코드 제공·유료 구매 금지**.

## 구현
- `security_audit_preaudit.py`: 사용자 경로/고객 파일 인수를 **아예 받지 않는** 합성 입력 2건(HTML script 종료 태그, CSV formula 의심 문자열) 생성 → 실제 `deliver_single` → `verify_customer_folder` → 외부 연결 금지 CSP·escape 확인 → 같은 출력 재사용 거부 → ZIP manifest status 위조 거부 → 고객 폴더 HTML 변조 거부. **7개 기술 검증 범위**는 임시 로컬 폴더에서만 실행하며 원본 수정/실고객 자료 전송이 없다.
- 명령어:
  - `python security_audit_preaudit.py` — 표준 출력으로 synthetic-only 결과(상태는 항상 `INTERNAL_SYNTHETIC_ONLY_EXTERNAL_AUDIT_PENDING`)
  - `python security_audit_preaudit.py --output <새로운/빈 로컬 경로>.json` — 사용자 **명시 경로에만** O_EXCL로 새로운 redacted 보고서 작성, 기존 파일이 있으면 실패/무덮어쓰기, 네트워크/외부 전송 기능 없음.
  - `python -m unittest test_security_audit_preaudit -v` — 검증 범위 7개 + fail-closed/중복 불가·민감기록 제거 회귀 5종.
- 보고서의 **의도된 제한**: `independent_security_audit_completed:false`, `owner_rights_attested:false`, `commercial_release_approved:false`, `score_addition:0`, `external_transfer_performed:false`. 파일에는 실제 합성 데이터 내용·원본 경로·계정/장비 식별자·토큰/로그 없음.
- 외부 감사자는 `docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md`를 따라 **실제 고급 TOCTOU/NTFS·Windows10/11/악성 XLSX·CSP/XSS·재현·근본 원인·수정 후 재검증**을 확인해야 한다. preaudit 7개 성공은 R29 전체 수용 증거가 **절대 아님**.
- 내부 검증과 외부 감사의 범위 혼동 금지: HTML 자체 검사·합성 샘플 2건 / Windows/Ubuntu CI / 외부 독립 감사 각각 다른 수준의 증거. 현재 점수표·RELEASE HOLD/SALE NO-GO 변경0.

## 다음 단계와 형 개입 최소화
- 무료·외부 전송 없이 내부 preaudit CI 완료 후, 형의 `OWNER_APPROVAL_PACKET_A_20261114.md` 권리·개인정보·보존 정책 일괄 승인 및 **R29에 실제 독립 평가자를 쓰는 방법/비용/공유범위**만 사용자 결정 대기.
- 동의 전: 유료 감사·계정권한 확대·상업 배포·고객파일 수령·실고객 접속 **전부 미시행**.

## 2026-11-14 KST · Windows hosted Chrome 간헐 실패와 제한된 복구
- [1차 #43537183883](https://github.com/hibi89/data2web_studio/actions/runs/43537183883): 전체 CI FAIL, 기존 CMD 기반 self-check에서 Chrome `HOLD_EXECUTION_FAILED`, Edge 정상. 악성 입력 R29 프로브 failure가 아님.
- [2차 #43537507617](https://github.com/hibi89/data2web_studio/actions/runs/43537507617): transient launch retry 신규 추가됐으나 regex 두 번 이스케이프해 기존 DOM 보기도 실패. `7b00aba8dcb674f138493a4b3e04a29e12b801fa`에서 한 줄 정규식 복구. **최신 빌드/실브라우저 CI 통과 확인 전 미검증**.
- 리트라이 1번은 Chrome/Edge 명령 실행 실패/비0 종료에만, 독립된 새 임시 프로필로 수행. 정상 종료지만 렌더/2개 합성값이 빠지면 그대로 `HOLD`. 실행횟수로 수용점수 부풀림 금지.

## 2026-11-14 KST · 최신 실제 기능 SHA CI 검증 완료
- **SHA `d7e029ae838a15f6f7a952cdf920341a6e3ad6b0`**: [Python/browser #43538001797](https://github.com/hibi89/data2web_studio/actions/runs/43538001797) **4/4 SUCCESS**, Win315/315, Ubuntu314PASS/1SKIP, Chrome·Edge·Chromium E2E. [점수 게이트 #43538002050](https://github.com/hibi89/data2web_studio/actions/runs/43538002050) SUCCESS.
- 중간 [Chrome 실패 #43537183883](https://github.com/hibi89/data2web_studio/actions/runs/43537183883) 및 [regex 회귀 실패 #43537507617](https://github.com/hibi89/data2web_studio/actions/runs/43537507617)는 이력 보존. 프로세스 시작 장애 시 독립 프로필 1회 재시도(최대2회), 브라우저 DOM/행 미검증 시 무조건 HOLD, regex는 정상 복구. GitHub Actions에서 실제 동작 PASS. **R29 외부 독립 보안감사 여전히 NOT VERIFIED**, 추가점수0.
