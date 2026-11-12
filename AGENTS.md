> **[OWNER-FINAL-BLUEPRINT-100 | 2026-11-13 KST | 사용자 확정·전체 저장소 최우선]** 제품 공식 **최종완성률은 사용자 확정 최종설계도 전체 100%**를 분모로 한다. 총괄·작업자는 임의로 설계를 축소하거나, 해커톤용 MVP·합성 테스트·CI PASS·85/95% 내부 마일스톤을 최종완성률로 혼용할 수 없다. 최종설계 요구사항 ID→코드→정확 SHA 실제 검증→미구현/미검증 및 사용자 승인 가중치를 추적해 계산한다. 근거·가중치가 미비하면 **최종설계 기준 UNASSESSED(재산정 대기)**로 표시하고 종전 수치는 **과거 내부 마일스톤**으로 보존한다. 크몽 관련 완성률은 해총 `kmong-productization` 원장에 동기화한다. [작업중]/등록완료/RELEASE HOLD 등 기존 별도 상태는 보존한다. 상충하는 구형 진척률 산정 지시보다 우선. [공통 전체 규칙](https://github.com/hibi89/hackathon-command-center-2026/blob/kmong-productization/docs/strategy/FINAL_BLUEPRINT_COMPLETION_STANDARD_20261113.md). 정책 커밋은 코드 수정·성공 테스트·제품 출시·재산정 완료를 의미하지 않는다.

# DATA2WEB Studio — 개발 규율 (2026-11-12 KST)

## 역할과 절차
- 사용자 목적: 기존 REA_Web은 웹사이트 분석·재구축으로 되돌리고, 본 저장소는 CSV/JSON/XLSX/TSV → 로컬 HTML 웹앱 생성 **독립 제품**으로 개발.
- 시작: `HANDOFF.md` → `STATUS.md` → `AGENTS.md` → `REQUIREMENTS.md` → `docs/FINAL_DESIGN.md` → 실제 최신 원격 소스·GitHub CI.
- 모든 %는 **새 DATA2WEB 정본 설계**의 항목·실행·인수 근거로만 산정. 구 REA_Web Lite 95%를 복사하지 않는다. 새 repo 독립 소스는 아직 미이관.
- GPT 담당 직접 설계/코드/테스트/검증, 실패 사유 분석 후 변경된 방식 1회 재시도, 두 번 무진전이면 중단·피벗.
- 기존 REA_Web Pro/원본/Fable/Astra와 고객 원본을 **변경하지 않는다**. upstream/source SHA 보존, 새 기능 독립 브랜치에서 구현, Draft PR·원본 백업·실제 동등성 회귀.
- 보안: 고객 파일 전송·실 API·유료 AI·보안권한/배포/환경변수 변경은 소유자 사전 승인. 출력/실패시 삭제 금지·HOLD, 비밀과 고객데이터 GitHub 업로드 금지.
- 배포: 테스트 성공 != 판매 승인; 실제 고객 Win10/11·원본 사용권/3rd party NOTICE·가격·환불·지원 확인 전 RELEASE HOLD.
- 완료/중단: STATUS/HANDOFF 최신 GitHub SHA와 테스트 PASS/FAIL/SKIP·미검증·출처·다음 범위·승인 항목 기록. 코드 없는 문서화로 구현률 상승 금지.

## 크몽 중앙 [작업중] 게이트
- `hibi89/hackathon-command-center-2026@kmong-productization/docs/audits/KMONG_16_CURRENT_20261111.md`에 실제 제품 개발 시작 시 본 제품을 등록하고 목표·증거를 명시한다.
- **사용자 확정 단계 목표를 검증하여 달성하기 전에는 [작업중]을 제거하지 않는다.** 채팅 종료·중단·담당 변경도 제거 사유 아니다. 목표 변경은 사용자 승인.
- 제품 설정·문서 등록과 독립 executable 제품 진척률을 구분한다. 병렬 담당 제품 수치·표식 임의 변경 금지.

## GitHub 브랜치
- `main`: 제품 정본 문서·안정화 통합, 원본 소스 검증 전 판매 불가.
- `feature/lite-independent-migration`: 기존 Lite 소스 계약 조사·안전 이관·독립 파서/HTML/ZIP·회귀.
- `feature/xlsx-tsv-import`: 안전한 Excel/TSV import, 정규화·수식/시트·ZIP 위험 거부.
- 후속은 필요 근거 생길 때만 별도 생성; 모든 브랜치의 사용자 데이터/비밀·원본 변경 금지.
