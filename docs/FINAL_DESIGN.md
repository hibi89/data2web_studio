# DATA2WEB Studio — 최종 설계 정본 v1.0
**2026-11-12 KST / 제품 소유자 목표 확인 / 구현 전 설계**

## 1. 제품 약속
고객이 권리 보유한 **CSV, JSON, Excel .xlsx, TSV** 파일을 로컬에서 검수한 뒤, 개발 지식이나 서버 없이 열 수 있는 **읽기 중심 대화형 웹앱(단일 HTML 및 검증 ZIP)**으로 변환한다. DATA2WEB은 표형 데이터 변환기이며 **사이트 분석기는 REA_Web**이다. 원본 파일·개인정보·지급 자료를 기계적으로 서버에 올리지 않는다.

### 고객 가치
- 주문·재고·상품·업무대장·교육용 레코드 등 명확한 구조를 사용자 지정 ID/제목/분류 열로 변환
- 검색/분류·정렬/상세/페이지/간단 KPI·선택 차트를 한 번에 조회
- 전달된 HTML/ZIP을 독립 확인하고, 새 데이터는 명시적 승인 후 로컬에서 교체/재저장

### 제한·정직성
PDF·웹사이트 자체 분석, AI가 표의 의미를 추측해 확정하는 작업, 셀 수식의 Excel 호환 재계산, 일반 DB JOIN, 공개 웹호스팅·로그인/실거래는 기본 제품에 포함되지 않는다. 모든 출력은 승인 데이터의 **평문 사본**을 포함할 수 있으며 암호화된 보안 저장소라고 홍보하지 않는다.

## 2. 구현 방식 비교와 선택
| 방식 | 속도 | 비용·한도 | 유지보수·권리 | 선택 |
|---|---|---|---|---|
| A. REA_Web Lite·Pro 전체 소스 그대로 복제 | 초기 1차 구현 빠름 | Python FastAPI/SQLite 및 Fable/Astra 의존성·패키지 비대화 | 원 제품과 결합, 릴리스·권리·회귀 부담 증가 | 배제 |
| B. Lite의 기능·테스트 계약만 가져와 독립 stdlib 데이터 어댑터와 정적 HTML 빌더로 재구성 | 초기에 독립성 증빙 필요 | 로컬 기본비용 0, XLSX용 적법 라이선스 확정 필요 | 제품 책임 경계 명확, 기능 테스트·재사용 용이 | **선택** |
| C. 브라우저 전용 전부 구현 | 고객 설치 0 | 브라우저 Excel parsing bundle/코드 크기 증가 | 입력 제한·원본 파일 메모리·ZIP 보안 복잡 | 향후 옵션 |

**선택 B:** 원본 Pro의 동작·파일을 수정하지 않는다. 허용된 작은 파서 함수/HTML 템플릿과 동등성 테스트만 새 저장소로 **출처·LICENSE·SHA 기록 후** 재구성한다. 신규 저장소에서 실제 설치와 검증 성공하기 전 이관 성공이라 쓰지 않는다.

## 3. 시스템·데이터 흐름
```text
[고객 PC: 읽기 전용 입력 CSV | JSON | XLSX | TSV]
    -> Intake (확장자만 신뢰하지 않음, size/SHA/MIME/basic signature, .xlsx ZIP-bomb limits)
    -> Parse (CSV·TSV Python csv, JSON 표형 제한, XLSX safe workbook reader)
    -> Preview (시트/컬럼/데이터 건수, 파싱 위험·중복, 원본 바이트 불변)
    -> Owner Gate (ID/title/category 명시 매핑, privacy/권리 및 평문 고지 승인)
    -> Canonical Table (고정 schema·셀 타입·행/열 상한·원본 SHA·승인 영수증)
    -> Render (정적 HTML, CSS/JS escaping/CSP, local search/filter/sort/page/detail/chart)
    -> Build (임시 신규 대상 -> HTML 재파싱/manifest -> create-only ZIP)
    -> Independent Verify (허용 멤버, SHA bytes, CRC, schema/approval, no-clobber)
    -> Human File Browser QA (file:// 열기 -> 검색/교체/저장 -> 신규 HTML 재열기)
    -> RELEASE HOLD until seller/legal/customer approvals
```

읽기/쓰기 분리: 파일 intake/preflight는 원본 read-only, 렌더 결과는 별도 새 폴더에만 생성한다. 생성 후에도 입력원본을 재읽어 SHA 확인, 출력은 temp에서 검증 완료 후 원자적인 신규 경로로만 게시한다. 폴더 바꾸기/symlink/파일 대체 경합 시 자동 삭제 대신 HOLD·수동 복구. 중복 실행은 같은 job id·출력 경로·SHA라면 무덮어쓰기 HOLD, 다른 이름은 명시 생성 허용. 예외·취소 시 원본 및 이전 출력 보존.

## 4. 구성 모듈 (목표 파일 위치)
- `data2web/intake.py`: 합법적 로컬 입력 경로/확장자/실제 파일 형식/상한·해시 처리
- `data2web/parsers/csv_json.py`: 재사용 계약에 맞는 CSV/flat JSON
- `data2web/parsers/xlsx_tsv.py`: .xlsx 안전 파서(실제 시트/수식/cache/외부링크 제한) 및 TSV
- `data2web/schema.py`: 정규 스키마/필드명·식별자/행/경고 계약
- `data2web/approval.py`: 승인 영수증·개인정보 평문/권리 승인
- `data2web/render.py` + `data2web/assets/template.html`: 오프라인 web UI
- `data2web/delivery.py`: 고객 ZIP·SHA/manifest/한국어 안내
- `data2web/verify.py`: 배포물 독립 검증기
- `data2web/cli.py`: inspect → approve → build → verify; auto-submit/remote none
- `tests/golden/`: REA_Web Lite 대비 골든 카탈로그/동작 회귀 (합성)
- `tests/browser/`: 실제 파일의 Chrome/Edge 다운로드·reopen
- `docs/ORIGIN_AND_LICENSE.md`: 원 출처·SHA·자체/제3자 라이선스 증거

## 5. canonical schema v1
```json
{
  "schema_version": "data2web.table.v1",
  "source": {"kind": "csv|json|xlsx|tsv", "sha256": "<hex64>", "sheet": null, "byte_count": 0},
  "mapping": {"id": "column", "title": "column", "category": "column"},
  "columns": [{"name":"column","kind":"text|number|date|boolean","nullable":true}],
  "rows": [{"id":"...", "cells":{}}],
  "warnings": [],
  "approval": {"mode":"explicit-owner", "digest":"<hex64>", "plaintext_ack":false}
}
```
- JSON 위 예시는 **문서 스키마**, 고객 실데이터·실제 생성결과 아님. 빈값·정밀 숫자는 문자열 보존 우선, 날짜/금액은 출처와 표시 분리, 자동 비즈니스 의미 확정 금지. 민감 열 등 사전 명시 허용 항목만 출력.
- 각 표 출력 수/페이지/요약 값이 source SHA와 승인 매핑에서 유도됨을 독립 verifier로 대조.

## 6. UI·상품 패키지
- 고객 홈: 제목/데이터 버전/레코드 수/필터/정렬/상세/다운로드, 접근성 키보드/모바일.
- CSV/JSON/XLSX/TSV import는 **판매자 빌더 단계**에서 필수 지원. 클라이언트에서 원본 XLSX를 임의 브라우저 업로드 없이 자동 교체한다고 약속하지 않는다. 브라우저의 교체는 승인된 동일 헤더 CSV로 제한하고 새 HTML 저장 시 명시 경고.
- Basic: 1파일, 로컬 목록·검색·필터·3테마·HTML+ZIP
- Pro: 다중 시트 선택/컬럼 검수·요약 차트·추가 테마·CSV 재가져오기
- Business: 2개 승인 동일 구조 append, 고급 무결성/검수 보고·맞춤 템플릿
- 위 SKU 가격·지원범위는 제안이며 **사용자 판매승인 전 미확정**.

## 7. 비용·배포·운영
- 기본 로컬 stdlib CSV/JSON/TSV: API 호출0·서버0·토큰 비용0.
- XLSX는 안정된 오프라인 parser/library가 필요. 오픈소스 라이선스/상용 재배포·버전·ZIP decoding 제한을 사전 확인. 디바이스 호환성과 설치 난도 검증.
- Public SaaS, 결제/회원/클라우드 저장·고객 파일 수집은 이번 설계에서 제외, 필요시 독립 승인·개인정보 영향평가.
- GitHub에는 실행 코드·문서·테스트·합성 fixture만; 고객 원본·비밀·실 사용 데이터 업로드 금지.
- 실행은 신뢰되는 로컬 환경의 명시적 CLI/GUI; README 원클릭 후보는 검증되기 전 미구현.
- Production/Vercel: 해당 없음. 오프라인 납품형, 최초 배포 RELEASE HOLD.

## 8. 장애·보안·복구
- Inputs: 경로·symlink/junction/zip-slip/상대경로, 과대 xlsx ZIP/셀/시트, unsafe formula/link/대용량, XML entity/network references 방어.
- Parsing: Unicode/BOM/CSV 개행·제어문자·중복 헤더·JSON 중복키·비정상 Excel, 결과 HOLD와 구체적 한국어 오류.
- Output: script 종료·XSS·CSP·CSV formula injection·malformed JSON 차단; 외부 CSP connect none, template HTML 이스케이프; local HTML plaintext 공개위험 고지.
- Delivery: 새 폴더 create-only, 검수 JSON과 산출 데이터가 안 맞거나 SHA mismatch면 fail closed, 자동 재귀 삭제 금지.
- Recovery: 원본 read-only, 마지막 승인 영수증·백업/ZIP와 GitHub 정확 소스 SHA로 수동 재생성; 변경 중 원본으로 건너뛰기 불가.

## 9. 완성률 산정과 필수 수용 게이트
| 단계 | 정의 | 확인 자료 |
|---|---|---|
| 0→50 | 신규 저장소에서 CSV/JSON 독립 로컬 HTML 생성·검증, Lite와 기능 계약 동등 | 소스 존재·CLI 원본 독립 실행·50+ 합성 및 브라우저 QA |
| 50→70 | XLSX/TSV 실제 파일 안전 파싱·명시적 시트/매핑·오류 차단 | 복잡 시트/수식·위조·용량 한도/독립 회귀 |
| 70→85 | UI·템플릿/차트·ZIP·재열기/Windows+Linux 브라우저 | 전체 경로 same-SHA CI PASS, Chrome/Edge |
| 85→95 | 고객사용 오프라인 납품검증·서명 아닌 SHA 성격 명확화·실사용 회귀 | 문서/라이선스/패키징/물리 Windows 검증 목록 |
| 95→100 | 제품 최종설계 전 항목 확인, 고객 시범/권리·약관·지원·승인 | 실제 인수 및 사용권·사용자 GO. **자동 100% 목표 생성 금지** |

현재 상태: **신규 리포지토리 생성·설계만 완료**, source migration·XLSX/TSV·테스트는 아직 실행하지 않음. REA_Web Lite의 95% 잠정은 원본 브랜치 한정. DATA2WEB 전체 최종상품 완성률은 **정식 미산정(UNASSESSED)**, 독립 신규 앱 실행 검증은 **0%**, 현재 단계 목표는 검증 가능한 **50% 독립 MVP**. 숫자를 문서·브랜치 개수만으로 추가하지 않는다.
