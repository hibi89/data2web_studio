# DATA2WEB Studio — XLSX/TSV P70 기술수용 감사 · 2026-11-13 KST

**사용자 목표:** P50에서 P70 기술 단계 확장 (XLSX·TSV 안전 처리). **정본:** `REQUIREMENTS.md`의 R01–R33 및 `docs/FINAL_DESIGN.md`의 전체 제품 100% 설계. 두 문서의 기능 범위를 축소하거나 임의 가중치 변경하지 않았다.

## 정확한 실행 검증

- 저장소: `hibi89/data2web_studio`, 개발 브랜치 `feature/xlsx-tsv-import`.
- 기능 검증 커밋: `42b832c5e18521d3edcf53b69cbf92c272f245cb`; [GitHub Actions #43381537805](https://github.com/hibi89/data2web_studio/actions/runs/43381537805) 완료 SUCCESS (3/3 jobs).
- Windows GitHub hosted 2025 runner, Python 3.11: **145 PASS / 0 FAIL / 0 SKIP** `python -m unittest discover -v`.
- Ubuntu 24.04, Python 3.11: **145 PASS / 0 FAIL / 0 SKIP**, 같은 테스트.
- Ubuntu Chromium headless Playwright 1.56: **기존 CSV/JSON `file://` E2E PASS** (`browser_probe.py`) 및 **새 XLSX·TSV `file://` E2E PASS** (`browser_tabular_probe.py`).
- XLSX 브라우저 테스트: 실제 OOXML 구조의 **합성 다중 시트 .xlsx 파일**을 생성·선택 시트만 반영→새 HTML/ZIP 생성→독립 ZIP verifier 통과→실 Chromium에서 검색/필터, 주입 공격 문자 무해화, 다른 시트 데이터 미포함, HTTP(S) 네트워크 요청 0·JS pageerror 0. 실 고객이 만든 Microsoft Excel 대형/서식 복합 파일은 **미검증**.
- TSV 브라우저 테스트: 합성 TSV 인용·탭 데이터를 HTML에 렌더링→ZIP 검증→Chromium 검색 E2E PASS.
- 현재 [증거 코드](https://github.com/hibi89/data2web_studio/tree/feature/xlsx-tsv-import): `data2web_tabular.py`, `data2web.py`, `studio.py`, `data2web_web.py`, `delivery.py`, `verify_delivery.py`, `test_xlsx_fixtures.py`, `test_tabular.py`, `browser_tabular_probe.py`.

## 구현 설계 2안 비교 및 결정
| 방식 | 성능/지원 | 설치·API 비용 | 보안/유지보수 | 판정 |
|---|---|---|---|---|
| A. 범용 XLSX 라이브러리(openpyxl 등)를 실행 의존성으로 채택 | 복잡 서식/셀 형식 호환성 높음 | pip 배포/버전·NOTICE 관리 필요; 원격 API 비용 0 | 외부 의존·압축/XML 처리 보안 검토 및 지원범위 넓어짐 | 이번 엄격한 제한 범위에서 보류 |
| B. Python stdlib `zipfile`·ElementTree 제한 XLSX 서브셋 파서 | 읽기 중심 값·시트/헤더 선택 지원; 고급 Excel 기능은 HOLD | **실행 의존성 0, API 호출 0, 라이선스 추가 0** | ZIP 멤버/CRC/압축비·XML·외부링크·수식 경계 직접 검증; 보수적인 호환성 | **이번 P70 채택** |

선택 B의 제한은 **범용 Excel 재현을 약속하지 않으며 지원 범위 확대 시 독립 설계 승인이 필요**하다는 뜻이다. 본 제품은 계산기나 데이터베이스 관리기가 아니다.

## 신뢰 경계·실제 수용 조건
1. **TSV:** UTF-8/UTF-8 BOM, Python `csv.reader(delimiter='\t', strict=True)`, quoted tab/newline, 행·열·셀 한도·중복/빈 헤더·틀린 행 길이 차단. Excel 수식처럼 보이는 텍스트도 실행되지 않는다.
2. **XLSX signature / archive:** .xlsx 파일의 ZIP header 필수, 허용 OOXML 파일 이름만, 120개 이하 ZIP 멤버, 압축된 파일 8MB 이하, 최대 XML member 24MB/총 압축해제 크기 48MB/압축비 180:1, 중복·상대경로·symlink·매크로/임베디드·외부링크/worksheet rel 차단. 파일을 디스크에 무단 압축 해제하지 않는다.
3. **XML 안전:** DTD/ENTITY 금지, 파서 XML 형식·공식 관계 체크, 최대 30 시트, 시트명/선택/숨김 제어, 헤더 행 1–50, 최대 40열·데이터 10,000행·셀 길이 16,000자, 비연속/중복/조작 셀·합쳐진 셀·오류값 HOLD.
4. **시트/캐시 제어:** `python studio.py inspect file.xlsx`는 **시트 목록·SHA만** 반환. 행 데이터 미출력. `--sheet <이름> --header-row N`로 선택하고, `build`는 시트 명시 필수. 수식이 있으면 **기본 HOLD**, `--allow-cached-formulas`를 양측 검사·빌드에서 명시한 경우 **숫자/문자 캐시만** 수용; 캐시 없으면 HOLD, 수식 실행/외부 연동/재계산 없음. HTML에 원본 시트/표시형식·캐시 한계 경고 노출.
5. **출력 승인:** 원본 SHA/시트/헤더행/캐시승인/ID·title·category 세 컬럼 및 원본 재조회 SHA를 바탕으로 새 HTML만 생성. ZIP manifest와 HTML 내 선택된 시트·원본 SHA·캐시 승인·건수를 별도 verifier가 대조. 기존 HTML/ZIP 무덮어쓰기.
6. **복구/중복:** 실패 시 HOLD, 원본·이전 결과 자동 삭제 금지. ZIP/HTML은 새 파일에만 생성. 물리 Windows junction/파일 교체 경합은 추가 보안감사 대상.

## 최종설계 R01–R33 요구의 변화 (승인 가중치 미합의)
| 요구 ID | 증거/검증 범위 | 상태 |
|---|---|---|
| R01–R02 | 기존 CSV/flat JSON 실행·브라우저 회귀 | 이전 P50 경로 유지/검증 |
| R03 | `parse_xlsx`, `list_xlsx_sheets`, `--sheet`, `--header-row`, 수식 캐시 HOLD, 외부링크/매크로 거부 | **이번 기술 게이트 구현·합성 CI PASS**, 실제 고급 Excel 호환 미검증 |
| R04 | `parse_tsv` UTF-8/BOM/인용 셀, ZIP 및 Chromium E2E | **이번 기술 게이트 구현·합성 CI PASS** |
| R05–R06 | 파일/SHA·ZIP 멤버·압축비·XML/행·열·셀 상한, 명시적 검수 SHA | **구현·경계 테스트 PASS**, 경합/실고객 OS 미검증 |
| R07–R10 | 사용자 시트 선택, 헤더 행/3열 매핑 승인, 영수증 내 시트/캐시/원본 SHA | **구현**, 실제 고객 권리/PII 정책 미승인 |
| R11–R12 | 이상 XLSX/XML/TSV/누락 캐시·공식 텍스트 HOLD, XSS 비실행 | **합성 보안 회귀 PASS**, 일반 보안 감사 별도 |
| R13 | 다중 파일 동일 스키마 append | **미구현** |
| R14–R17 | 기존 오프라인 HTML/CSV 재교체/반응형 | **P50 브라우저 재검증 PASS** |
| R18 | 선택형 차트와 수식 방법론 | **미구현** |
| R19–R22 | 평문 승인/네트워크 0/ZIP 결정성/독립 SHA+CRC+manifest sheet identity | **구현·테스트 PASS**, 출고 권리 별도 |
| R23–R27 | 고객 Win10/11 Chrome+Edge·새 고객 폴더·보유·개인정보·지원·판매 | **부분 또는 미검증, RELEASE HOLD** |
| R28 | 10k×20 성능/메모리·응답 예산 | **미검증** |
| R29 | XLSX ZIP-bomb/외부링크/매크로/XSS 테스트 | **합성 경계 검증 PASS**, 독립 보안감사 미실시 |
| R30 | Win/Ubuntu parser + Linux Chromium, 고객 Windows 브라우저/판매/서명 | **자동 기능 CI PASS**, 물리 Win10/11·판매 미검증 |
| R31 | REA_Web Lite 실제 원본 Python 실행 동등성 | **2행 합성 fixture 한정**, 전체 미검증 |
| R32 | 런타임 stdlib Python 3.11, 재현 가능한 Actions | **개발 CI PASS**, 최종 구매자 패키징 미검증 |
| R33 | 상업적 자료 사용권·고객 인수·판매약관 | **미승인·HOLD** |

## 판정과 중단선
- **설계 문서의 P70 기술 단계**(CSV·JSON P50 유지 + XLSX·TSV 검증 가능한 안전 파서, 명시 시트/헤더/캐시, 오류 차단 및 OS/브라우저 CI)를 구현하고 확인했다.
- **공식 최종완성률: UNASSESSED**. 최종설계 전체의 가중치(분모100)에 대해 사용자가 독립 승인한 표가 없고 여전히 R13/R18/R23–R33에 잔여가 있으므로 **공식 70% 달성을 주장하지 않는다**.
- 판매 출시/고객자료 취급 승인: **RELEASE HOLD / SALE NO-GO**. Vercel·Production **미적용** (로컬 HTML 제품).
- 크몽 `DATA2WEB [작업중]` 목표 70% 유지. 사용자 승인 없는 마커 해제나 85% 후속 자동 착수 없음.
