# DATA2WEB Studio — P85 UI·차트·실 브라우저·성능 검증 · 2026-11-13 16:21 KST

## 최종 판정
- **85% 기술 마일스톤에 정의된 범위 구현·자동 검증 PASS.** 사용자 최종설계 전체 공식 완성률 **UNASSESSED**(요구 R01–R33 가중치 소유자 승인 및 현실 인수 증빙 부족). 기술 목표를 공식 최종률 85% 또는 판매 승인으로 전용 금지.
- 소스: `hibi89/data2web_studio@feature/p85-ui-crossbrowser-20261113`, 검증 기능 SHA `709b2e5d5540893b9f7ad1b391584c6400899672`, [실 GitHub Actions #43385035408](https://github.com/hibi89/data2web_studio/actions/runs/43385035408) **4/4 jobs SUCCESS**.
- Windows hosted runner **Windows Server 2025**, Python3.11: **145 PASS·0 FAIL·0 SKIP**, **설치된 Google Chrome와 Microsoft Edge에서 각각** 합성 CSV의 실제 `file://` 차트/검색/필터/정렬/상세/동의 CSV 교체/다운로드/재열기/모바일·인쇄 검증 PASS; 두 브라우저에서 XLSX·TSV 합성 실파일→승인 HTML·ZIP→`file://` 조회도 각각 PASS.
- Ubuntu24.04 Python3.11 **145 PASS·0 FAIL·0 SKIP**, Playwright Chromium headless `file://` CSV/JSON, XLSX/TSV, P85 차트/수정·보관/성능 PASS, 외부 HTTP(S) 요청0·브라우저 JS pageerror0.
- **주의:** GitHub hosted Windows Server 2025에서 Chrome/Edge 실행 성공 ≠ 고객의 실제 Windows10/11 컴퓨터 검수 완료. 실제 고객 Excel 복잡 시트/Excel 버전도 미검증. Playwright/Chromium은 테스트 전용, 납품 프로그램 외부 의존 없음.

## UI·차트의 사용자 기능과 경계
1. 다크·반응형 UI: 전체 행수/필터 행수/범주 종류 KPI, 기존 검색·범주 필터/정렬·페이지/키보드 상세, 화면 크기별 CSS, 인쇄 전용 숨김. 기존 원본 XLSX/TSV/CSV/JSON 파서와 승인 게이트 보존.
2. 데이터 기반 **범주별 막대**: 필터/검색 결과만 정확한 레코드 건수로 집계. 범주가 10종 초과면 상위 9개+기타(잔여 합계). HTML·JS·CSS 내장, 외부 차트 라이브러리/네트워크0. 분류 문자열이 악성 HTML이어도 `textContent`만 사용.
3. 선택형 숫자열 요약: ID/제목/분류를 제외하고 12자리 정수·소수 4자리 이하·비음수·최대 1e12 형태가 전체의 비어 있지 않은 셀에만 성립한 열을 선택 후보로 노출. 차트 설명에 **산술합/빈값 제외/회계·단위 의미 추정 없음** 명시. JS Number의 부동소수 근사 계산이라 세금/회계/정밀 재무 확정 수치로 사용 불가.
4. **CSV 로컬 교체 시 재검증 표시:** 명시적 소유권/평문 승인 없이 교체 차단; 교체 후 `source_sha256=null`, 원래 `source_sheet=null`, `cached_formulas=false`, `USER_LOCAL_CSV_REPLACEMENT_NOT_VERIFIED`을 새 HTML 안에 고정; UI에서 새 SHA 검수 필요 경고. 기존 ZIP의 승인 영수증은 새 HTML에 사용 불가. 기존 파일 자동 덮어쓰기/삭제0.
5. 납품 ZIP: `index.html`, `manifest.json`, `README_KO.txt` 결정적 create-only; 별도 표준 라이브러리 verifier에서 SHA256, ZIP CRC, 메타 데이터·행수·시트·헤더 행·캐시승인 대조. 이는 **출처 서명/판매권리 보증이 아닌 파일 무결성 검증**.

## 재현 가능한 정확 테스트와 범위
- 원본/기준: P50 `feature/lite-independent-migration@f613305dee8c8ceb8636632bce001b1c02532e35` 및 P70 `feature/xlsx-tsv-import@0fee0f84c35f377bdfffea7b1a66e62191abb81a`. P85 새 브랜치 생성으로 기존 SHA·기능/원본 변경 없음.
- 단위: `python -m unittest discover -v` Win 145/145, Ubuntu145/145; 악성 XLSX/매크로/외부 관계/DTD/압축 폭탄/누락 수식 캐시·CSV 인용/XSS·ZIP 전송변조 등 기존 회귀 통과.
- 실제 브라우저:
  `python browser_probe.py`,
  `python browser_tabular_probe.py --channel chromium|chrome|msedge`,
  `python browser_p85_probe.py --channel chromium|chrome|msedge`.
  Chrome·Edge 각 P85와 XLSX/TSV 경로, Linux Chromium 각 모든 경로 검증. 390px 모바일 viewport 스크롤 폭, 인쇄 CSS 모드, 악성 HTML 비삽입, 외부 요청0, JS 예외0.
- 대용량 합성 10,000행×20열 `python browser_perf_probe.py` **1회 측정치** (GitHub Ubuntu runner, 합성 데이터):
  - CSV **1,125,142 bytes**, HTML **3,563,255 bytes**.
  - Python HTML 생성 **0.784초**, tracemalloc peak **31.85 MiB**.
  - Chromium 첫 `file://` 로딩·DOM count **0.256초**, 검색 **0.027초**, 정렬 **0.154초**.
  - 성능 기준: 빌드 20초·초기 로딩 15초·검색/정렬 각 12초, Python peak 320MiB·HTML 20MB 미만. **이 CI 결과는 실제 구매자 하드웨어·브라우저·고객파일의 속도를 보증하지 않음**.
- 정확 GitHub 검증: [Actions #43385035408](https://github.com/hibi89/data2web_studio/actions/runs/43385035408) 2026-11-13 16:21 KST 종료 SUCCESS. 이후 문서 반영 커밋은 별도 SHA이고 다시 CI 확인한다.

## 설계 대안 및 선택
| 방식 | 성능·품질 | 비용 | 유지관리/보안 | 결정 |
|---|---|---|---|---|
| A. Chart.js 등 외부 그래프 런타임 번들 | 종류 다양·시각 기능 풍부 | 별도 npm 배포·라이선스/잠금·번들 크기·초기화 비용 | 업데이트·CSP·원본 출처 관리 부담 | 지금은 보류 |
| B. 자체 DOM/CSS 범주 막대와 숫자 합계 | 웹앱에 적합한 단순 읽기형·범주 10개 요약 | **런타임 의존0, 원격 비용0** | XSS textContent·범위/계산법 명시, 공급망 부담 적음 | **이번 P85 채택** |

범위 변경이 아닌 설계 R18의 **선택형 요약 차트** 구현. 전체 Excel 포맷 지원·무단 호스팅·결제/광고/원격 API 미추가.

## 요구 추적 (기존 R01–R33 승인 정본 유지)
| 요구 | P85 근거 | 한계 |
|---|---|---|
| R01–R12 | CSV/JSON/XLSX/TSV 145 tests×2 OS 및 3브라우저 실제 조회 | XLSX strict OOXML 외 미지원, 실고객 원본·복잡 Excel 미검증 |
| R13 | 다중 파일 개별 승인 append | **미구현** |
| R14–R17 | HTML 단독, UI 필터/정렬/페이지·반응형/테마·다운로드 재열기, Chrome/Edge/Chromium 통과 | 고객 실제 장비 검수 별도 |
| R18 | 독립 HTML 분류별 막대·숫자열 선택형 합계·출처 기준 설명 | 다변량 차트·회계 검수 아님, 브라우저 부동소수 근사 |
| R19–R22 | 평문 승인/무외부망/ZIP 독립 verifier. CSV 재저장 시 원본 SHA 증거 초기화 | 서명/판매 허가 아니다 |
| R23 | Windows Server hosted Chrome·Edge `file://` E2E PASS | **실 Windows10/11 사용자 PC 미검증**, macOS 미검증 |
| R24–R27 | 기존 create-only·HOLD·권리 경고·데이터 보유 원칙 | 구매자 폴더/PII/지원·반품·상용권 미승인 |
| R28 | 합성 10k×20 실측 및 시간/메모리 시험 | **1회 GitHub CI 환경 측정**, 사용자 PC 대표 성능 보장 아님 |
| R29–R30 | 합성 악성 셀 차단, CSP·브라우저/XLSX/TSV/ZIP 4/4 CI | 독립 레드팀·고객 현장/코드 서명 미수행 |
| R31 | 2행 원본 Lite 합성 fixture 계약 수준 | **원본 Lite 실제 소스 실행 전체 골든 비교 미검증** |
| R32 | Python3.11 stdlib 런타임, Win/Linux/브라우저 CI 증거 | 실 구매자 독립 설치 EXE/서명 미구현 |
| R33 | 판매 전 정책·재사용권·고객 인수 | **사용자 승인/법무/고객 원본 미검증, RELEASE HOLD** |

**공식 최종완성률 UNASSESSED** (전체 R01–R33 승인 가중치·고객 증빙 미확정). **기술 P85 단계 검증 성공, 해총 `[작업중]`·상품 SALE HOLD 유지**. Production/Vercel 미적용, Draft PR만 작성(병합/출고 안 함).
