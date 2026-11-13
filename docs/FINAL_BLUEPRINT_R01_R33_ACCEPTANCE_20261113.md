| R32 | Python·의존성잠금·QA·실행/포터블 배포·재현 빌드 | **미승인** | `package_portable.py`, `data2web_desktop.py`, `test_desktop_controller.py`·호스팅 Win Tk41 화면·Python zipapp | 235x2 OS+Win GUI smoke PASS | Python/Tk 실제 구매자 설치·서명 EXE·실고객 인수 미검증 |

## 계산 기준: 사용자 확정 원본 100% 전체
- **정본:** `REQUIREMENTS.md`(2026-11-12), `docs/FINAL_DESIGN.md`(v1), owner 정책 `OWNER-FINAL-BLUEPRINT-100`. R01–R33을 완전히 포함하며 요구 범위/상용 조건을 축소하지 않았다.
- **공식 최종완성률: `UNASSESSED`(85% 미인증).** 전체 33개 요구에 대한 소유자의 `가중치 합계100` 확정 문서가 없고, 실 고객·Win10/11·이용권/법적 승인/원본 full golden/제품 납품 수용이 미충족이다. 아래 합성 기술 테스트 PASS 수를 85%로 나누지 않는다.
- **기능 검증 소스 SHA:** `d311c47f1b85382f1d4ce43dfacdabcdc7e85612`, [Actions #43392272159](https://github.com/hibi89/data2web_studio/actions/runs/43388705727) **4/4 SUCCESS**, Win·Ubuntu Python3.11 각각 **210/210 PASS**, Linux Chromium+Windows Chrome/Edge 실제 `file://` 합성 데이터 E2E PASS. GitHub hosted Windows Server 2025이지 실제 구매자 Win10/11이 아니다.
- **사용자 요청 재해석:** 본 작업은 기술단계85가 아닌 정본 전체 final-design 85를 목표로 시작. 아래의 미충족 사항이 남으므로 **최종설계 85% 완료라고 주장하지 않는다.**
- **가중치 정책:** `승인 가중치` 열은 **모두 미승인**이다. 추정 균등 가중치 1/33을 지정하지 않는다. 부분 구현/미검증에는 임의 점수 없음.

## 전체 33개 요구, 누락 없이 대조
| ID | 정본 요구/수용조건 | 소유자 승인 가중치 | 실제 구현·실행 근거 | 상태 | 반드시 남길 한계 |
|---|---|---|---|---|---|
| R01 | CSV UTF-8/BOM·RFC4180 인용/개행 | **미승인** | `data2web.py, test_acceptance.py` | 합성 PASS | 실고객 손상 CSV 별도 |
| R02 | 평면 JSON 배열·객체형 레코드 검수 | **미승인** | `data2web.py, test_single_delivery.py`, 단일 평면 객체 또는 평면 객체 배열·NaN/중첩 HOLD | 합성 PASS | 임의 중첩 records wrapper 자동추정/객체 키 기반 JOIN 미지원 |
| R03 | XLSX 시트/헤더 위치·수식/외부링크·캐시 HOLD | **미승인** | `data2web_tabular.py, test_tabular.py` | 제한 XLSX 합성 PASS | 실제 Excel 다양한 서식/날짜 형식·사용자 실제 검수 |
| R04 | TSV 인코딩·탭·인용 | **미승인** | `data2web_tabular.py, test_tabular.py` | 합성 PASS | 실고객 파일 호환 |
| R05 | 원본 파일/행·열·셀/ZIP 상한 | **미승인** | `data2web.py, data2web_tabular.py` | 합성 PASS | OS별 전체 공격 표면 독립 감사 |
| R06 | 경로·크기·바이트·SHA 변경확인 | **미승인** | `path_policy.py, data2web.py, test_path_policy.py` | 부분 | 대상 교체경합·전구간 TOCTOU 보장 미검증 |
| R07 | 원본 보존·사용권·개인/공유 데이터 동의 | **미승인** | `data2web_append.py, studio.py` | 부분 | 실제 소유자 권리와 개인정보 사용동의 외부 승인 없음 |
| R08 | 원문 미노출 헤더·형힌트·NULL/중복·범주 검수 | **미승인** | `data2web_profile.py, test_final_blueprint.py` | 합성 PASS | 실 고객 개인정보 안전성 자동 판정 불가 |
| R09 | ID/제목/분류 3열 사용자 명시 매핑 | **미승인** | `data2web.py, data2web_append.py` | 합성 PASS | 실고객 매핑 확인 필요 |
| R10 | 원본 SHA·시트·행·헤더·매핑 승인 영수증 | **미승인** | `receipt_utils.py, delivery.py, verify_delivery.py` | 합성 PASS | 해시/매니페스트는 법적 서명 아님 |
| R11 | 데이터/시트/중복/인코딩/변경 오류 HOLD | **미승인** | `test_tabular.py, test_final_blueprint.py` | 합성 PASS | 경합·대규모 실원본 추가 검증 |
| R12 | Excel/CSV/TSV 수식처럼 보이는 텍스트/XSS 보호 | **미승인** | `data2web_web.py, test_tabular.py` | 합성·브라우저 PASS | 고객 독립 보안 점검 미검증 |
| R13 | 최대 10개 파일 개별 SHA·승인·동일 순서 헤더 append만, JOIN 금지 | **미승인** | `data2web_append.py, test_final_blueprint.py, browser_final_blueprint_probe.py` | 합성·브라우저 PASS | 고객 실제 다중파일 승인 필요 |
| R14 | 완전 독립 오프라인 HTML/CSS/JS | **미승인** | `data2web_web.py, browser_p85_probe.py` | 실브라우저 합성 PASS | 실고객 전달 하드웨어 검증 별도 |
| R15 | 검색/다중 카테고리/정렬/상세/페이지/반응형 | **미승인** | `data2web_web.py, browser_p85_probe.py` | 실브라우저 합성 PASS | 복수 선택 UX 실구매자 검수 미실시 |
| R16 | 3테마/제목/메타/한국어 인쇄 | **미승인** | `data2web_web.py, test_acceptance.py, browser_p85_probe.py` | 부분 | 실 프린터/인쇄 PDF 검증 미완 |
| R17 | 동일 헤더 CSV 교체·명시 승인·새 HTML 저장/재열기 | **미승인** | `browser_probe.py, browser_final_blueprint_probe.py` | 실브라우저 합성 PASS | 변경자료는 원본 SHA/소유권 새로 확인 필요 |
| R18 | 선택형 설명 가능 막대차트·요약·출처/계산법 | **미승인** | `data2web_web.py, browser_p85_probe.py` | 실브라우저 합성 PASS | 금액 합계는 JS 부동소수 근사; 회계 정확성 미보장 |
| R19 | 평문 포함 경고와 동의 | **미승인** | `studio.py, data2web_web.py` | 합성·실브라우저 PASS | 개인정보 실 사용권 확인 별도 |
| R20 | 외부 요청/로그인/광고 기본 0 | **미승인** | `browser_p85_probe.py, browser_final_blueprint_probe.py` | 실브라우저 합성 PASS | 개별 구매자 확장프로그램 간섭 미검증 |
| R21 | 결정적 create-only ZIP·manifest·안내/실제 승인 LICENSE/NOTICE | **미승인** | `delivery.py, test_final_blueprint.py` | 부분 | 고객 상용 LICENSE/NOTICE 최종 승인 미실시 |
| R22 | 독립 ZIP SHA/CRC/멤버·중복/zip-slip/변조 거부 | **미승인** | `verify_delivery.py, test_final_blueprint.py` | 합성 PASS | 배포자 신원서명과 구별 |
| R23 | Windows10/11 Chrome·Edge file:// 최종 수용, macOS/Linux 확인 | **미승인** | `browser_p85_probe.py, browser_final_blueprint_probe.py` | 부분 | CI는 Windows Server2025·Ubuntu Chromium; 실제 Win10/11/macOS 사용자 검증 없음 |
| R24 | 고객 새 폴더 납품·충돌 무삭제 HOLD·복구 영수증 | **미승인** | `data2web_single.py, data2web_append.py, receipt_utils.py, test_single_delivery.py, browser_single_delivery_probe.py` | 합성/호스팅 실브라우저 PASS | 고객 직접 Win10/11 PC 실제 인수 미검증, 실패 후 남은 폴더 수동 HOLD |
| R25 | 원본·임시·결과 무자동삭제/보유정책 | **미승인** | `docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md` | 부분 | 실 운영 개인정보 보존기간·파기 책임 승인 대기 |
| R26 | 개인정보/민감범위 명시 검수·승인 | **미승인** | `data2web_profile.py, data2web_append.py` | 부분 | 실 고객 자료 개인/민감 범주 및 동의 법적 확인 미실시 |
| R27 | SKU별 판매·수정·지원·환불 조건 승인 전 판매 금지 | **미승인** | `docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md` | 대기 | 사용자 판매 조건 승인·실 크몽 상품등록 없음 |
| R28 | 10k×20 메모리·정렬/검색 응답 실측 | **미승인** | `browser_perf_probe.py` | 합성 CI PASS | GH Ubuntu 단일 벤치마크; 실고객 PC 재측정 필요 |
| R29 | XSS/CSP/CSV·XLSX 폭탄/경로·재검증 테스트 | **미승인** | `test_tabular.py, test_path_policy.py, browser_p85_probe.py` | 합성/브라우저 PASS | 물리 Win10/11 junction/TOCTOU, 외부 보안감사 미실시 |
| R30 | Win/Linux 실제 경로 E2E, Chrome/Edge, 독립 사용자·패키지/서명·라이선스 감사 | **미승인** | `GitHub Actions 4 jobs, browser_final_blueprint_probe.py` | 부분 | CI hosted 환경만; 구매자 독립 시험·서명·라이선스 별도 |
| R31 | 원본 Lite 대비 각 지원 기능의 실제 golden 결과 비교 | **미승인** | `upstream_runtime_golden.py`, 공개 REA Lite 원본 정확 `7b6b68111efd906f9d929b5e2f577699b26399ee` 실 CLI·Chromium CSV/JSON 정규 데이터·SHA/테마·검색/분류·CSV 업데이트·저장/재열기/오류 HOLD | 공통 지원 기능 실제 원본 PASS(범위 제한) | 페이지 길이·기능 추가·픽셀 일치는 계약상 별개; 모든 고객 데이터/원본 프로덕트 판매 동등성 검증 아님 |
| R32 | 새 저장소 Python·의존성 잠금·자동QA·실행/포터블 배포·재현 빌드 | **미승인** | `package_portable.py, test_portable.py, test_single_delivery.py`, 결정적 `.pyz` 단일/다중 파일 CLI 실행 CI PASS | 합성·호스팅 CI PASS/구매자 부분 | 고객 Python 설치/포터블 배포 서명 EXE·지원 정책 미검증 |
| R33 | 상업적 재배포·자료권리·실고객 인수·구매/환불 승인 | **미승인** | `docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md` | 대기 | 사용자/법무/고객의 실제 승인 필요 |

여기서 '합성 PASS'는 QA 목적으로 직접 만든 합성 데이터에 대한 **GitHub CI 실제 실행**이다. '실브라우저 합성 PASS'는 호스팅 Windows Chrome/Edge 및 Ubuntu Chromium에서 실제 `file://` URL을 연 결과지만 **실고객 파일·디바이스 사용자 인수는 아니다**. `부분`·`대기`에 대해 완료 점수는 배정하지 않는다.

## 2026-11-13 추가 데스크톱·고객폴더 독립 검증 (공식 85% 미확정)
- `74f5f5a6b4625be3d510be5f59f1983be150b26e` [CI #43395679294](https://github.com/hibi89/data2web_studio/actions/runs/43395679294) Windows·Ubuntu **각 235 PASS**, hosted Windows Tkinter 실제 41개 UI 렌더링, Chrome·Edge/Chromium local file://, 원본 Lite 실제 golden 기존 경로 PASS.
- R08/R09/R19/R24/R26: Python Tkinter 로컬 검수·명시 승인 GUI, 실제 고객 파일 SHA/시트 변경은 새 폴더 생성 전에 HOLD; 데이터 브라우저·외부 API 전송0.
- R21/R22/R24: 전체 고객 폴더 HTML+ZIP+receipt 내부 SHA/행수/매핑 출처 대조, receipt 바꿔치기/중복/누락/추가 파일 거부; 독립 서명·판매권 승인과 구분.
- 사용자 승인 가중치 합100·실 고객 Win10/11/권리/판매/지원 미충족으로 **공식 전체 85% UNASSESSED 유지**. [완전한 실증과 미검증](FINAL_BLUEPRINT_GUI_DELIVERY_20261113.md).

## 2026-11-13 후속 정확 QA 추가 (공식 점수 미산정)
- **추가 기능 검증 SHA** `d311c47f1b85382f1d4ce43dfacdabcdc7e85612` [GitHub Actions #43392272159](https://github.com/hibi89/data2web_studio/actions/runs/43392272159) Windows/Ubuntu **210 PASS 각각**, 실제 Windows Chrome·Edge 및 Ubuntu Chromium `file://` 단일 고객 새 폴더 HTML/ZIP/receipt, 소유자 SHA·PII 동의, 이전 다중결합·검색/차트·CSV 교체 PASS.
- **원본 실제 실행 골든:** 원본 `hibi89/REA_Web@7b6b68111efd906f9d929b5e2f577699b26399ee` public SHA를 임시 checkout하여 `rea.lite_builder` 원본 Python과 JS `file://`를 **직접 실행**, 새 구현 CSV/JSON 75행/2행·테마·정렬/검색/필터·CSV 업데이트/HTML 내보내기/재열기·승인 오류를 실제 비교 PASS. 고객자료0/원본 Git write0, 동일 픽셀 복제 주장 금지.
- **추가 입력:** JSON 평면 단일 객체(1행), nonfinite JSON 거절; XLSX 단일 납품 시 explicit sheet 빠지면 새 고객 폴더 생성 **전** HOLD.
- **최종판정 유지:** 전체 R01–R33 소유자 가중치 미승인, 고객 Win10/11·판매 LICENSE/PII 실 승인 미충족이므로 **공식 85% 미인증/UNASSESSED**.

## 이번 최종설계 기준 실제 신설 항목
- **R08**: `data2web_profile.py`가 데이터 셀을 출력하지 않고 컬럼별 형 힌트·빈 셀·중복/고유수·전체 중복행을 검사; 개인정보 자동 허용 아님.
- **R13**: `data2web_append.py`는 문서 내 파일별 SHA와 권리·평문·개인정보 범위의 명시적 소유자 확인이 모두 있어야 **같은 순서 헤더**로만 append. CSV/JSON/XLSX/TSV 혼합 가능, 외부 JOIN/업로드/수식 실행·스키마 추측 없음, 중복 ID/변경 원본/비인가 입력 즉시 HOLD. ZIP manifest→HTML source receipts 합동 해시·원본 행수 독립 검증, 브라우저에서 CSV 재수정하면 이전 승인 출처 무효화.
- **R15**: 단일 분류에 머물렀던 기존 UI를 Ctrl/⌘ 다중 분류 선택으로 확장. Chrome/Edge/Chromium 실제 DOM 검색·복수 분류 검증.
- **R24**: `studio.py deliver-append`로 신규 고객 폴더 생성 후 `index.html`, `delivery.zip`, `receipt.json` 파일을 **create-only** 제공; 기존 폴더·고객 파일 덮어쓰기 거부, 잘못된 사전 SHA는 폴더 생성 전 거부. 실패 후 생성물이 있으면 자동 삭제하지 않고 재검수 대상.
- **R26**: 승인 매니페스트에 `rights_and_plaintext_ack=true` 및 `privacy_classification=NO_PERSONAL_DATA_REVIEWED|OWNER_APPROVED_LOCAL_ONLY`을 필수로 지정. 이는 **서명이 아닌 소유자 자기 확인**, 실제 법적 승인·민감정보 검사 자동 보증 아님.
- **R29**: `path_policy.py`에서 Python3.11 Linux symlink/Windows reparse/junction 속성 및 `..` 경로 별칭을 막고 소스·출력·ZIP·receipt·portable 파일에 결합. 경로 교체 경합·실 Windows10/11 junction은 추가 점검.
- **R32**: `package_portable.py`로 동일 소스 바이트에서 항상 같은 단일 Python `.pyz`를 create-only 생성, Python3.11+ 설치 PC에서 `inspect`, `build`, `deliver-append` 실행. 코드 서명/실제 구매자 설치 보증 아님.

## 해소 불가 또는 미실행 의존성
- **소유자 외부 승인 필요:** R07/R26/R27/R33의 실제 원본 파일 권리·개인정보 사용허가·크몽 판매 범위/가격/지원/환불/상업 재배포 정책.
- **구매자 환경 실제 검증 필요:** R03 실제 Microsoft Excel 복잡 시트/서식/캐시, R23/R30 사용자 Windows 10/11 설치된 Chrome/Edge·macOS, 성능 R28 고객 PC.
- **원본 접근 실실행 과제:** R31 `hibi89/REA_Web@feature/lite-owner-delivery-p95-20261112`에서 `rea.lite_builder` + `rea.mvp`를 **동일 합성 입력과 동일 실제 환경으로 원본 직접 실행**한 full golden 결과. 현행은 소스 열람 및 대표 2행 계약 fixture에 불과.
- **납품/품질 최종:** R21 라이선스/NOTICE(사용자 승인 자료만), R32 고객 독립 설치/실행 번들·서명/지원, R25 파기·보유기간 확정. URL/Vercel **미적용**(오프라인 앱).
- 제품 `[작업중]` 및 `RELEASE HOLD/SALE NO-GO`는 해총 원장에 유지하며 등록완료로 표시하지 않는다.

**판정:** 신규 기능 실행검증은 실질 진전. **정본 전체 85%는 미산정·미인증**이며, 소유자 승인 가중치와 미검증 항목을 증거 없이 PASS로 전환하지 않는다.
