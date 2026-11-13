# XLSX/TSV 입력 확장 작업 브랜치 (2026-11-12 KST)

- 정본 `REQUIREMENTS.md`/ `docs/FINAL_DESIGN.md`; 새 DATA2WEB Studio에만 적용, 원래 REA_Web 엔진과 Lite 원본을 변경하지 않는다.
- `.xlsx`: workbook signature/ZIP 허용 개수·압축률·크기 제한, worksheet 선택, 날짜/수식/빈 캐시/외부링크/매크로 안전 HOLD. 사용 가능한 오프라인 파서/LICENSE/NOTICE 검토 후 채택. 새 workbook을 실행/외부 조회하지 않는다.
- `.tsv`: UTF-8(BOM) 문자·탭/줄바꿈/인용부호/중복헤더 오류 처리, 기존 CSV/JSON 공통 canonical schema/명시 매핑에 연결.
- CSV/JSON 독립 MVP와 동등한 골든 비교 + 악성 XLSX/수식·압축폭탄·TSV 인젝션 + Windows/Ubuntu 동작 회귀 필요.
- **P70 기술 단계 구현·검증:** 정확 SHA `42b832c5e18521d3edcf53b69cbf92c272f245cb`, Actions #43381537805 Win·Ubuntu 145 PASS/OS 및 브라우저 XLSX/TSV E2E PASS. 정본 최종완성률 UNASSESSED·RELEASE HOLD, 개발 브랜치만 반영. 상세 `docs/P70_XLSX_TSV_ACCEPTANCE_20261113.md`., 이 브랜치 존재만으로 DATA2WEB 완성률 상승 없음; 먼저 Lite 독립 마이그레이션 검증 필요.
