# DATA2WEB Studio — 전체 최종설계 R01–R33 수용 감사 (2026-11-14 KST)

**2026-11-14 KST 신규 승인된 100점 B안 가중치 적용:** 33개 전체 분모 100점, **검증 완료 가중치 72점**, 미검증 28점, 목표 85점까지 13점. [승인된 배점표](FINAL_BLUEPRINT_WEIGHTING_100_APPROVED_20261114.md) 및 [기계 판독 점수표](../data/final_blueprint_scorecard_v1.json). **이전 UNASSESSED 문구들은 승인 이전의 역사 기록**이며 현행 평가 분모 미합의 상태를 뜻하지 않는다. 합성 CI 테스트 수에 비례해 점수를 부여한 것이 아니라 요구별 수용 근거가 있는 22개 요구에 고정배점을 적용했고, 외부·실고객·상업적 수용이 필요한 11개 요구는 0점으로 둔다. `[작업중]`·RELEASE HOLD/SALE NO-GO 유지.

**실행 증거:** 소스 441506eda275b1e3766a4d018741ebfa1ae030b7, [GitHub Actions #43501097784](https://github.com/hibi89/data2web_studio/actions/runs/43501097784) 4/4 SUCCESS. 호스팅 Windows Server2025 Python3.11 249/249 PASS, Ubuntu24.04 Python3.11 249/249 PASS. Windows 실제 Tkinter UI에서 합성 CSV/XLSX 두 경로를 파일선택·시트·열·권리/개인정보 승인·고객폴더 생성까지 버튼 클릭 PASS. Windows 설치 Chrome·Edge에서 Playwright와 네이티브 headless HTML 직접 렌더 PASS; Ubuntu Chromium 및 실제 upstream REA Lite pinned golden PASS. 고객 Windows10/11 PC/실업무 Excel/상용 권리는 미검증.

> **현행 판정 우선:** 이 감사표의 이전 일자별 섹션에 있는 ‘미승인 A/B’와 ‘UNASSESSED’는 사용자 가중치 선택 전의 이력이다. 현재는 **R01–R33 고정 100점/검증 가중치72점/목표85점 미달**로 재평가했다. 실고객 Windows10/11·실업무 Excel·상업 사용권/법적 수용은 여전히 미검증이다.

## 2026-11-14 KST · R16 인쇄·접근성 실검증 보강 (공식률 미확정)
- 정확 소스 `4dc55cd73664db0e15b2554fc7b6c7087ffc8e85` [GitHub CI #43506243118](https://github.com/hibi89/data2web_studio/actions/runs/43506243118) **4/4 SUCCESS**. Win/Ubuntu Python 각249 PASS, Chromium·Chrome·Edge에서 실제 A4 PDF 1/3·2/3 화면 페이징/키보드 Space 확인, 파일 외부요청0. 현재 페이지 50행 출력 범위 명시, 실 고객 프린터 육안/Win10/11 인수 미검증.
- 기존 R16 '부분'에 추가 기술 근거 확보. R01–R33 최종설계 전체/사용자 승인 가중치 원칙은 그대로며, **가중치 B안 72/100·A안 22/33은 미승인 참고 시뮬레이션**. 공식 최종률 `UNASSESSED`.
- [R16 증거와 실패 복구 기록](R16_PRINT_AND_KEYBOARD_ACCEPTANCE_20261114.md).

## 2026-11-14 KST · ZIP 단일 스냅샷·Windows 고객 실행 근거 추가
- 기능 SHA 23a2d1293755294a58a20b98dc34e229a1e54f82 [CI #43509224663](https://github.com/hibi89/data2web_studio/actions/runs/43509224663) **4/4 SUCCESS**, Win Python269 PASS/Ubuntu268 PASS·Windows 전용 CMD1 SKIP.
- R06/R22/R29: bounded ZIP 단일 snapshot/교차 SHA, 중복·비유한 JSON/경로 교체 거부. R32: unsigned Python 포터블 zipapp+Windows CMD3+README·manifest 및 실제 Win cmd.exe synthetic Chrome/Edge PASS.
- R29의 외부 보안감사, R32의 고객 Win10/11·서명 EXE/판매 지원은 미충족. 기술 범위 참고 22/33, 미승인 B 가중 72/100 유지(공식률 아님). [새 검증 상세](docs/FINAL_BLUEPRINT_R22_R32_PACKAGE_INTEGRITY_20261114.md).

## 최종설계 전체 33개 요구별 검증표

| 요구 | 사용자 정본 수용 범위 | 승인 가중치 | 코드·실행근거 | 확인된 범위 | 남은 한계 |
|---|---|---|---|---|---|
| R01 | CSV UTF-8/BOM·RFC4180 인용/개행 | **3점 고정** | `data2web.py, test_acceptance.py` | 합성 PASS | 실고객 손상 CSV 별도 |
| R02 | 평면 JSON 배열·객체형 레코드 검수 | **3점 고정** | `data2web.py, test_single_delivery.py`, 단일 평면 객체 또는 평면 객체 배열·NaN/중첩 HOLD | 합성 PASS | 임의 중첩 records wrapper 자동추정/객체 키 기반 JOIN 미지원 |
| R03 | XLSX 시트/헤더 위치·수식/외부링크·캐시 HOLD | **4점 고정** | `data2web_tabular.py, test_tabular.py` | 제한 XLSX 합성 PASS | 실제 Excel 다양한 서식/날짜 형식·사용자 실제 검수 |
| R04 | TSV 인코딩·탭·인용 | **2점 고정** | `data2web_tabular.py, test_tabular.py` | 합성 PASS | 실고객 파일 호환 |
| R05 | 원본 파일/행·열·셀/ZIP 상한 | **2점 고정** | `data2web.py, data2web_tabular.py` | 합성 PASS | OS별 전체 공격 표면 독립 감사 |
| R06 | SHA256·경로·크기·원본 바이트 재확인 | **2점 고정** | path_policy.py, verify_delivery.py, data2web_append.py, test_archive_snapshots.py | bounded FD ZIP 스냅샷+승인 manifest 64KB 제한, Win269/Ubuntu268+1SKIP PASS | 실제 Win10/11 OS 경쟁조건·외부 감사 미검증 |
| R07 | 원본 보존·사용권·개인/공유 데이터 동의 | **2점 고정** | `data2web_append.py, studio.py` | 부분 | 실제 소유자 권리와 개인정보 사용동의 외부 승인 없음 |
| R08 | 로컬 컬럼명·형 힌트/NULL·중복/분류 검수 | **4점 고정** | data2web_profile.py / data2web_desktop.py / desktop_ui_owner_flow_probe.py | Windows 호스팅 실제 Tk CSV+XLSX 파일·시트 선택/검수 PASS | 고객 민감정보의 법적 분류 자동 보증 불가 |
| R09 | ID/제목/분류 3열 사용자 명시 매핑 | **3점 고정** | `data2web.py, data2web_append.py` | 합성 PASS | 실고객 매핑 확인 필요 |
| R10 | 원본 SHA·시트·행·헤더·매핑 승인 영수증 | **4점 고정** | `receipt_utils.py, delivery.py, verify_delivery.py` | 합성 PASS | 해시/매니페스트는 법적 서명 아님 |
| R11 | 데이터/시트/중복/인코딩/변경 오류 HOLD | **3점 고정** | `test_tabular.py, test_final_blueprint.py` | 합성 PASS | 경합·대규모 실원본 추가 검증 |
| R12 | Excel/CSV/TSV 수식처럼 보이는 텍스트/XSS 보호 | **3점 고정** | `data2web_web.py, test_tabular.py` | 합성·브라우저 PASS | 고객 독립 보안 점검 미검증 |
| R13 | 최대 10개 파일 개별 SHA·승인·동일 순서 헤더 append만, JOIN 금지 | **3점 고정** | `data2web_append.py, test_final_blueprint.py, browser_final_blueprint_probe.py` | 합성·브라우저 PASS | 고객 실제 다중파일 승인 필요 |
| R14 | 완전 독립 오프라인 HTML/CSS/JS | **5점 고정** | `data2web_web.py, browser_p85_probe.py` | 실브라우저 합성 PASS | 실고객 전달 하드웨어 검증 별도 |
| R15 | 검색/다중 카테고리/정렬/상세/페이지/반응형 | **5점 고정** | `data2web_web.py, browser_p85_probe.py` | 실브라우저 합성 PASS | 복수 선택 UX 실구매자 검수 미실시 |
| R16 | 3테마/제목·메타/한국어 A4 인쇄 대응 | **3점 고정** | `data2web_web.py`, `browser_print_accessibility_probe.py`, `test_acceptance.py` (3테마·A4 PDF 인쇄·최대50행 현재페이지 범위 명시, Space/Enter 키 상세보기) | **Chromium·Win Chrome·Edge 실제 file:// A4 PDF·DOM 출력 PASS**, 코드 `4dc55cd73664db0e15b2554fc7b6c7087ffc8e85`, Actions #43506243118 | 실제 고객 Win10/11/종이 프린터·한글 글리프 시각 확인은 미검증, 전체 행 PDF 인쇄 기능은 계약 범위 밖 |
| R17 | 동일 헤더 CSV 교체·명시 승인·새 HTML 저장/재열기 | **3점 고정** | `browser_probe.py, browser_final_blueprint_probe.py` | 실브라우저 합성 PASS | 변경자료는 원본 SHA/소유권 새로 확인 필요 |
| R18 | 선택형 설명 가능 막대차트·요약·출처/계산법 | **4점 고정** | `data2web_web.py, browser_p85_probe.py` | 실브라우저 합성 PASS | 금액 합계는 JS 부동소수 근사; 회계 정확성 미보장 |
| R19 | 평문 포함 경고와 동의 | **3점 고정** | `studio.py, data2web_web.py` | 합성·실브라우저 PASS | 개인정보 실 사용권 확인 별도 |
| R20 | 외부 요청/로그인/광고 기본 0 | **3점 고정** | `browser_p85_probe.py, browser_final_blueprint_probe.py` | 실브라우저 합성 PASS | 개별 구매자 확장프로그램 간섭 미검증 |
| R21 | 결정적 create-only ZIP·manifest·안내와 승인된 LICENSE/NOTICE만 납품 | **4점 고정** | delivery.py / verify_delivery.py / verify_customer_folder.py | 샘플 HTML·ZIP·영수증 무결성 PASS | 상용 LICENSE/NOTICE 아직 사용자 승인 없음 |
| R22 | ZIP SHA/CRC·허용멤버/압축위험·중복 키·변조 거부 독립검사 | **4점 고정** | verify_delivery.py, verify_customer_folder.py, test_archive_snapshots.py | ZIP 단일 bounded snapshot의 CRC/manifest/HTML/SHA, 재검사 ZIP SHA 차이·NaN/중복 JSON/바꿔치기 HOLD, CI #43509224663 PASS | 법적/암호학적 작성자 서명·적대적 실폴더 전체 경합 미검증 |
| R23 | 실제 Win10/11 Chrome·Edge 및 macOS/Linux 실제 수용 | **3점 고정** | client_local_rehearsal.py / browser_p85_probe.py / desktop_ui_owner_flow_probe.py | hosted Win2025 Chrome·Edge Playwright+네이티브 HTML, Linux Chromium PASS | 고객 실 Win10/11 및 macOS 독립 인수 미확인 |
| R24 | 새 고객 폴더 create-only HTML+ZIP+receipt·충돌시 HOLD | **3점 고정** | data2web_single.py / data2web_append.py / verify_customer_folder.py / desktop_ui_owner_flow_probe.py | 호스팅 실제 Tk 파일 선택→검수→명시 승인→생성·독립검증 PASS | 고객 PC 파일/권한·실고객 인수 미검증 |
| R25 | 원본/결과 무단 삭제 금지·보유기간/책임 고지 | **2점 고정** | OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md / create-only 코드 | 기존 고객파일 무삭제 테스트 PASS | 실제 보존기간·고객자료 파기/책임 정책 사용자 미승인 |
| R26 | 고객 민감·개인정보 범위/평문/사용권 명시 승인 | **2점 고정** | data2web_desktop.py / data2web_append.py / test_desktop_controller.py | 실제 Tk 승인 체크박스와 검수 경로 hosted PASS | 법적 사용권/개인정보 적합성 자동 인증 아님 |
| R27 | SKU별 판매·수정·지원·환불 조건 승인 전 판매 금지 | **2점 고정** | `docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md` | 대기 | 사용자 판매 조건 승인·실 크몽 상품등록 없음 |
| R28 | 10k×20 메모리·정렬/검색 응답 실측 | **3점 고정** | `browser_perf_probe.py` | 합성 CI PASS | GH Ubuntu 단일 벤치마크; 실고객 PC 재측정 필요 |
| R29 | XSS/CSP·경로경합·ZIP/원본 변조·악성 XLSX 보호 | **3점 고정** | path_policy.py, verify_delivery.py, verify_customer_folder.py, test_archive_snapshots.py, browser_p85_probe.py | 합성 경로·ZIP 중복 JSON·CRC 재작성·snapshot SHA 불일치 HOLD, Win269/Ubuntu268+1SKIP PASS | 외부 침투·실 고객 OS/고급 TOCTOU 감사 미검증 |
| R30 | Win/Linux 실제 E2E·Chrome/Edge·독립 사용자·패키지/서명/권리 감사 | **2점 고정** | Actions #43501097784 / desktop_ui_owner_flow_probe.py | 호스팅 Windows/Linux 브라우저·GUI·자가검증 PASS | 실제 고객 Win10/11·서명 EXE·라이선스 독립 감사 미검증 |
| R31 | REA Lite 원본 공통 기능 실제 golden 비교 | **2점 고정** | upstream_runtime_golden.py 공개 pin 7b6b68111efd906f9d929b5e2f577699b26399ee | 실제 원본 CLI·Chromium CSV/JSON/테마/교체/재열기 PASS | 픽셀 일치/확장 기능·실업무 파일 동등성 미검증 |
| R32 | 재현 가능 Python 패키징·자동시험·포터블 고객 실행 | **3점 고정** | package_portable.py, package_windows_bundle.py, test_windows_bundle.py | unsigned Python3.11 pyz+CMD3·README·SHA manifest 새폴더 무덮어쓰기/변조거부, 실제 hosted Win CMD Chrome/Edge 셀프체크 PASS, CI #43509224663 | 실고객 Win10/11 Python/Tk 설치·서명 EXE·지원/라이선스/고객 인수 미검증 |
| R33 | 저작권/자료권·실고객 수용·재배포·구매/환불 운영 승인 | **3점 고정** | OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md | 사용자 외부 승인 대기 | 판매 GO 주장 금지 |

## 추가 개발·판정 근거

- 소스 파일은 최대 8 MB bounded 파일핸들 읽기로 전환, 운영체제 지원 시 O_NOFOLLOW 사용, fd의 파일식별자·mtime·ctime·크기와 종료 시 경로 정보를 비교한다. 변경 전/도중 파일바꿔치기 시험을 Windows/Ubuntu에서 실제 통과했지만, 모든 TOCTOU 공격 방지를 보증하지 않는다.
- 고객 파일을 읽지 않는 python studio.py self-check --browsers 는 내부 합성 CSV 2행으로 납품폴더·ZIP·영수증을 검증하고, 설치된 Chrome·Edge로 file:// DOM 렌더를 확인한다. 누락·오류는 PARTIAL_HOLD, 성공해도 PASS_SYNTHETIC_ONLY이며 고객 사용권·상용 출시의 증거가 아니다.
- GUI는 호스팅 Windows에서 실제 파일/시트/매핑·승인 컨트롤을 자동 조작했다. 실제 고객 Windows10/11 설치/사용자 조작 수용은 별도 미확인.
- 원본 REA_Web 공개 SHA 7b6b68111efd906f9d929b5e2f577699b26399ee는 CI 임시 읽기전용 실행 비교만 했고 코드/사용자자료 복사·수정 없음. 상용 라이선스를 승계했다는 뜻이 아니다.

**최종 상태:** [작업중] 유지, RELEASE HOLD/SALE NO-GO, main/기존 P50/P70/P85/REA_Web 원본 불변, Vercel/Production 미적용. 실제 구매자 PC·실 Excel·상품 가격/지원/환불·개인정보 보유/파기·사용권/LICENSE/NOTICE 및 R별 가중치 사용자 승인 전 공식85 달성 주장 금지. 상세 근거: [2026-11-14 파일 안정성 및 로컬 자체검증](FINAL_BLUEPRINT_P85_INPUT_RACE_NATIVE_BROWSER_20261114.md).
