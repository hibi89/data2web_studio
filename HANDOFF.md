## [2026-11-13 KST] DATA2WEB 정본 지문 실 검증 인수인계 10항
1. **목표·확정요구·기술:** 기존 DATA2WEB CSV/JSON/XLSX/TSV→오프라인 HTML/ZIP 전체 설계 보존, 같은 저장소 main `docs/FINAL_DESIGN.md` 정본 변경 감지.
2. **변경/결정:** 제품 코드 수정 없이 문서-only 파일럿 `docs/audits/FINAL_BLUEPRINT_CANONICAL_GATE_PILOT_20261113.md` 생성하여 기존 `.github/workflows/final-blueprint-gate.yml` 트리거.
3. **실행 검증:** `main@3400ab7eb84fb7141acacfc0df213e0b0186da83` [Actions #43348157583](https://github.com/hibi89/data2web_studio/actions/runs/43348157583) SUCCESS; job log 정본 `canonical=MATCHED`, 공식 `UNASSESSED`, 오류 출력 없음. Python 제품 코드 테스트 신규 0건.
4. **완료·진행·차단:** 파일 정본 지문 파일럿만 완료. 사용자 승인 100점 가중치/전체 기능 실제 E2E·Windows/권리 불확정, 공식률 UNASSESSED, RELEASE HOLD.
5. **문제/대안:** 기존 main의 최종설계와 feature 개발 사이 원본 변경 감지 공백을 중앙 공유 검사기로 완화. 파일 동일성은 최종설계 의미 충족 증거가 아니므로 범위 축소·점수 승격 금지.
6. **저장소/브랜치/SHA·주요경로:** `hibi89/data2web_studio@main` 파일럿 SHA `3400ab7eb84fb7141acacfc0df213e0b0186da83`, `docs/FINAL_DESIGN.md` blob `7cd268...`; 중앙 verifier 기능 최초 범용 시행 SHA `5f71af9cb1b4b1ff6ba46876ba0f506543b3aeaf`. 본 docs-only 후속 커밋 SHA GitHub 재조회.
7. **Production/실행 환경:** GitHub hosted Ubuntu `contents:read`; 고객 파일/브라우저/설치/Production 미적용.
8. **원본·백업·인증:** 원본 앱·REA_Web·Git history·고객 데이터·시크릿·유료 API·권한 변경 없음. 문서 갱신 Git 이전 커밋으로 복구 가능.
9. **다음 우선순위/승인:** 고객 동의 가진 합성 E2E→실 Windows/브라우저/납품·권리 검수; 최종설계 요구 전수+승인 가중치 확정 후 전체 공식률 평가. 중앙 자동 cross-repo write는 별도 보안 자격증명 조달 필요.
10. **갱신 시각·검증범위:** 2026-11-13 KST; GitHub Actions 실 run/jobs/log 증거 재조회, 제품 기능검증0, 공식률 UNASSESSED.

# DATA2WEB Studio — HANDOFF (2026-11-12 KST)

1. **목표/확정 요구/기술:** 사용자가 새 `hibi89/data2web_studio`를 만들고, REA_Web 원래 웹사이트 분석 기능과 분리 승인. DATA2WEB은 CSV/flat JSON + 확장 XLSX/TSV 파일을 고객 로컬에서 승인 받아 독립 HTML 웹앱/납품 ZIP으로 만드는 제품. Python3.11+·HTML/JS·오프라인.
2. **완료/변경/결정 근거:** 신규 저장소 정본 설계·요구사항·작업/검증 정책·출처/권리 가이드 작성. REA_Web Lite의 기능 전체 복붙(A)은 결합/권리/지원 부담으로 거절, 독립 코드와 테스트 계약(B) 채택. 사용자 원래 REA_Web 보존.
3. **테스트 명령·수:** 신규 제품 코드/실행·QA 없음, `NOT RUN`. 기존 REA Lite 원본 기능 검증 `cb7df1f4`, Actions #43186105405 Windows688PASS/19SKIP, Ubuntu677PASS/20SKIP, 각0FAIL은 **기존 프로젝트 근거**이지 본 제품 테스트가 아니다.
4. **상태:** 저장소·문서 초기화 DONE / 코드 이관 NOT STARTED / XLSX·TSV NOT STARTED / 독립 상품률 UNASSESSED, 실행 검증률0 / SALE HOLD, Production N/A.
5. **문제·시도·대안:** 새 저장소 비어 있어 실행 제품 없음; 이전 Lite는 Pro `rea.mvp`에 의존. 기존 통째 이식은 종속/법적 범위 커서 최소 기능 독립 추출+골든 검증(B)으로 전환. 실제 라이선스/고객 자료는 미승인.
6. **저장소·브랜치/SHA:** `hibi89/data2web_studio@main`, `feature/lite-independent-migration`, `feature/xlsx-tsv-import`; 기능 SHA 없음. 실제 최종 문서 HEAD는 GitHub 새 조회가 기준. 원본 REA Lite `cb7df1f4d1ce517c5940570af5bb1085410de268`, Pro `97b6e5cab7b8ffb4e1ee7f5e593021f4dac2598d`.
7. **Production/환경:** 오프라인 프로그램, Vercel/Production URL 없음, Python3.11+ 후보 / 실행 명령 아직 미구현; 새 시스템·CI 실행 없음.
8. **원본/복구/보안:** REA_Web 원본 브랜치들 변경 금지; 출처/권한 확인 `docs/ORIGIN_AND_LICENSE.md`; 문서/브랜치 Git SHA 복구. GitHub Private라도 민감정보 업로드 금지. 원본 ZIP/권리/실 고객 승인 전 배포 금지.
9. **다음 작업·완료 조건·승인:** `feature/lite-independent-migration`에서 파서/템플릿/CLI/zip verify·테스트 이관·독립 CSV/JSON 정상 사용자 경로를 검증하면 **50% gate 후보**; 후속 Excel/TSV 안전 import, Windows+browser, 납품과 권리 검수. 유료 API/자료 전송/권리·판매 GO는 사용자 승인 필요.
10. **갱신·검증범위:** 2026-11-12 KST. 저장소 메타·기존 Lite GitHub SHA 검증; 본 저장소 내용 readback 전까지 문서 저장 검증 대기. 최종 문서 커밋은 완료 후 조회 기록으로 갈음.

**중요:** 기존 REA_Web Lite 내부95% ≠ DATA2WEB 신 최종설계95%; 문서만으로 개발 점수 증액 금지.
