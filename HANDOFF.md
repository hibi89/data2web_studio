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
