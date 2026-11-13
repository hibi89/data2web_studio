# DATA2WEB Studio — STATUS

## 최신: 2026-11-13 15:20 KST · 코드 검증 SHA `90da878ffa29926dda39f6c67913353ec7a3b390`
- **공식 사용자 최종설계 완성률: UNASSESSED(정본 가중치 사용자 승인·R01–R33 전수 수용 미확정).** 50%를 공식 값으로 임의 등록하지 않음.
- **기술 P50 단계 핵심 경로 구현·통과:** CSV/JSON 표형 데이터 → owner 매핑/inspect SHA/명시적 승인 → 서버 없는 HTML·검색/필터/정렬/상세/페이지·3테마/한글·로컬 동일 구조 CSV 교체·새 HTML 다운로드 및 `file://` 재열기 → 결정적 ZIP/독립 verifier. CLI와 원본 분리.
- **실제 테스트:** 정확 소스 [Actions #43377913444](https://github.com/hibi89/data2web_studio/actions/runs/43377913444) Windows Python 3.11 **97 PASS/0 FAIL**, Ubuntu 24.04 Python 3.11 **97 PASS/0 FAIL**, 별도 실제 Playwright Chromium `file://` E2E **PASS**(검색/분류/정렬/페이지/상세/CSV 승인·교체·다운로드·재열기, XSS payload 안전, 외부 HTTP(S) 요청0·JS pageerror0), 3/3 jobs SUCCESS.
- **오류 수정:** Windows cp1252 검사·출력과 CRLF 바이너리 SHA 불일치, GitHub ubuntu-26 Playwright 호환, 비동기 파일 처리·CSP 테스트 방식·다운로드 임시 확장자 문제 모두 정확 로그 근거로 수정. 실패한 오래된 실행을 성공으로 간주하지 않음.
- **미완료·미검증:** XLSX/TSV, 고객 원본/민감데이터 권리, 실제 Windows10/11 Chrome/Edge 수동 `file://`, REA Lite 원본 소스를 실행한 전체 골든 비교(현재 원본 테스트 fixture 계약만), 대량 10k×20 성능 예산, 고급 차트, 패키지 서명/상용 라이선스/고객 인수. 상세 요구 추적 [docs/P50_ACCEPTANCE_EVIDENCE_20261113.md](docs/P50_ACCEPTANCE_EVIDENCE_20261113.md).
- **출시:** RELEASE HOLD/SALE NO-GO. Vercel/Production **미적용** (오프라인 제품), API 비용0·고객자료 클라우드 업로드0. REA_Web 원본 저장소 불변. `main` 병합 미실시(개발 feature 브랜치에서 검증).
- **크몽 해총:** 중앙 `kmong-productization`에 `DATA2WEB [작업중]`·목표 공식 50%·증거·미확인을 유지. 공식 최종 가중치 미확정이므로 작업 표식 임의 해제하지 않음.
- **다음:** 사용자 승인된 최종설계 R01–R33 가중치 확정/재산정 → XLSX/TSV 안전 import·실 고객 브라우저 검수 → SHA 귀속 재감사. 다음 단계 무단 착수 금지.

## 역사 상태 기록
## 2026-11-12 KST 시작 상태
- **정식 최종상품률: UNASSESSED(미산정)**. 신규 독립 저장소 실행 코드·테스트 확인 **0%** (현재 서류·개발 브랜치 구성만).
- 원 출처 `hibi89/REA_Web@feature/lite-owner-delivery-p95-20261112` **95% 엔지니어링 잠정**은 그 저장소의 **CSV/JSON Lite 한정**. DATA2WEB 신규 XLSX/TSV/독립 실행·상업권 95%를 의미하지 않는다.
- 확정 최종 설계: CSV+flat JSON+XLSX+TSV → owner mapping/SHA → local HTML → ZIP/verifier → 브라우저 실파일 재열기; 원래 사이트 분석 기능은 REA_Web 소관.
- 제품 기술: Python3.11+ stdlib 우선, XLSX parser 적법성 검수, HTML/CSS/JS local-first, 제3자 비용/서비스는 승인 전 없음.
- 기존 원본: REA_Web main/Pro/Fable/Astra 유지, 이관 자체 아직 없음. 신규 저장소 Private/기본 main으로 확인.
- 출시: **RELEASE HOLD**, Production/Vercel **미적용**, 고객 라이선스·권리·실 Windows 검증 **미검증**.
- 다음 독립 단계: `feature/lite-independent-migration`에서 출처·저작권/재사용 범위 확인 → 최소 필수 파서/테스트/템플릿 재구성 → 합성 CSV·JSON·독립 HTML·ZIP·브라우저/Windows E2E → **50% 목표** 검토. Excel/TSV는 다음 단계.
- 명령·테스트: 신규 앱 없음 / NOT RUN; 문서 원격 readback만으로 구현 완료 판정 금지.

## 2026-11-13 구현 진행 — 50% 목표 미달/검증 대기
- 독립 `data2web.py` CSV/JSON 입력, SHA256, 명시적 3열 매핑, 승인 플래그, create-only HTML 및 검색/필터/페이지/상세 구현.
- `test_data2web.py` 8개 회귀 케이스와 Windows/Ubuntu Actions 워크플로 추가. 실제 CI PASS/FAIL 결과는 별도 확인 필요.
- 미구현: Lite 골든 비교, ZIP/독립 verifier, 브라우저 실 E2E, XLSX/TSV, 사용자 데이터 수용. 따라서 공식 최종완성률 UNASSESSED 유지, 50% 달성 주장 금지.
- 기능 변경 SHA `b7664bf1e0d7e6757a6b27f44e04c102809935e1` (워크플로 추가까지). RELEASE HOLD 유지.