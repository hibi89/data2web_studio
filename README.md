# DATA2WEB Studio

**제품:** 승인된 CSV/JSON 데이터를 로컬 독립 웹앱으로 변환하고, Excel(.xlsx)/TSV까지 확장하는 오프라인 웹앱 빌더.

> 2026-11-12 KST — 신규 **Private** 독립 저장소. 이 README는 **설계 기준점**, 실행 가능한 완제품이나 기존 REA_Web Lite 기능 이관 완료 증거가 아니다. 현재 신규 저장소의 독립 코드·테스트·납품 검증은 **NOT RUN / RELEASE HOLD**.

## 역할 분리
- 본 저장소: **DATA2WEB Studio** — 사용자가 제공·승인한 로컬 표형 데이터로 독립형 HTML 웹앱 생성.
- 기존 [REA_Web](https://github.com/hibi89/REA_Web): **웹사이트 분석·증거화·독립 웹서비스 재구축** 원래 목적을 유지.
- 기존 검증된 Lite 원본: `hibi89/REA_Web@feature/lite-owner-delivery-p95-20261112` (정확 기능 테스트 SHA `cb7df1f4d1ce517c5940570af5bb1085410de268`); **기존 제품의 좁은 범위 엔지니어링 95% 잠정이지 DATA2WEB 전체 완성률이 아님**.

## 최종 제품 규격
- 입력: CSV UTF-8/UTF-8-SIG, 평면 JSON, XLSX(추가 구현), TSV(추가 구현); Excel .xls와 원격 URL/DB 직접 접속은 초기 버전 제외.
- 로컬 전처리: 형식·시트·헤더 선택, 명시적 필드 매핑, 데이터 형식/중복/NULL·권한·원본 SHA 검증.
- 산출: 카탈로그/검색/필터/정렬/상세/페이지·반응형 테마·선택적 차트, 서버 없이 열리는 자체 포함 HTML, 독립 검증 가능한 ZIP·SHA/manifest/한국어 설명서.
- 보안: 사용자가 승인한 로컬 파일만, 최초 업로드·외부전송·자동 수집 없음, CSV formula injection 방어, XLSX ZIP bomb·외부링크/매크로/수식 실행 차단, HTML XSS/CSP, 출력 충돌시 무덮어쓰기/HOLD.
- 상품: Basic/Pro/Business 기능 분리, 고객 자료 권리·라이선스·Windows 실사용·납품/환불/지원 승인 전 유료 판매 금지.
- 운영: `main`은 정본 설계·승인된 코드; `feature/lite-independent-migration`에서 기존 Lite의 허용된 코드·테스트를 안전하게 재구성하고 원본 기능 동등성 확인; XLSX/TSV 확장은 별도 단계.
- 필수 증거: GitHub exact SHA + Python/Node/브라우저 Windows·Linux 테스트, 순수한 신규 독립 앱에서 install/생성/내보내기/재열기 검증.

## 문서
- `REQUIREMENTS.md`: 최종 요구사항·명시적 범위.
- `docs/FINAL_DESIGN.md`: 100% 기준 설계·구조·데이터 흐름·테스트 수용조건.
- `AGENTS.md`, `STATUS.md`, `HANDOFF.md`: 개발·검증 정책, 현재 사실, 다음 단계.
