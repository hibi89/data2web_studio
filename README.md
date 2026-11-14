## 2026-11-14 · R29 독립 감사 준비: 고객자료 없는 내부 합성 증거
- `python security_audit_preaudit.py`(외부 업로드0) 또는 `python security_audit_preaudit.py --output <새로 만들 로컬>.json`(create-only)으로 합성 데이터의 XSS/CSV수식문자·ZIP허위판매·고객폴더변조·동일폴더무덮어쓰기·CSP 7개 시험. `test_security_audit_preaudit.py` 회귀5종. 내장 결과 `INTERNAL_SYNTHETIC_ONLY_EXTERNAL_AUDIT_PENDING`, 독립감사/권리승인 false, 추가점수0. [상세](docs/R29_SYNTHETIC_PREAUDIT_HANDOFF_20261114.md).
- 최근 hosted Windows 브라우저 시작 간헐 실패 [#43537183883](https://github.com/hibi89/data2web_studio/actions/runs/43537183883) → 독립된 새 프로필로 최대1회 실패 복구. 첫 수정 [#43537507617](https://github.com/hibi89/data2web_studio/actions/runs/43537507617)에서는 정규식 이스케이프 실수로 FAIL. SHA `7b00aba8dcb674f138493a4b3e04a29e12b801fa`에서 복구했지만 **정확 HEAD CI 미확인 상태**. 실패를 숨기지 않고 검증 전 성공 주장 금지.
- 공식 최종설계 72/100, 85까지13점·외부독립 감사와 실권리 정책 미완·RELEASE HOLD/SALE NO-GO.

## 2026-11-14 · A안 고객 납품 구성·상업적 권리 HOLD 자동검증

`python shipping_rights_preflight.py`를 실행하면 **고객 원본이 아닌 합성 CSV**로 실제 HTML/ZIP/receipt 패키지를 생성/재검증하고, [권리 인벤토리](data/shipping_rights_inventory_v1.json)와 허용 멤버가 일치하는지 확인한다. `python -m unittest test_shipping_rights_preflight -v`는 허위 상업 권리·외부 보안감사·LICENSE/NOTICE 주장/멤버 삽입 등을 **6종 회귀**로 거부한다. [CI #43535767796](https://github.com/hibi89/data2web_studio/actions/runs/43535767796) Windows/Ubuntu + Chrome/Edge/Chromium 4/4 SUCCESS. [근거와 한계](docs/R21_R29_SHIPPING_RIGHTS_PREFLIGHT_20261114.md).

**의도된 결과는 HOLD**(`status=HOLD_OWNER_IP_NOTICE_EXTERNAL_AUDIT`)이며 승인된 저작권/사용권, 고객 자료 권리, 제3자 LICENSE/NOTICE, 외부독립 R29 감사의 증거가 아니다. 최종설계72/100 유지, 85까지13점. 기존 고객 파일·폴더, 현재 ZIP verifier v1, 미서명 EXE/권리·판매 설정 변경 없음.

## 2026-11-14 · 사용자 확정 A 우선 납품 + 후속 B EXE / 전체 개발 로드맵

**상업화 우선순위:** 고객 로컬용 HTML·ZIP·검증영수증 **A 결과물 제작 서비스 먼저** → Python/Tk/PyInstaller의 **B 독립 Windows EXE 라이선스·상용배포는 후속**. 기존 R01–R33 가중치100/검증72, 타 원본 제품 보존, 승인 전 판매·외부 전송·유료 감사 금지.

- [A/B 전체 제품·72→85→95→100 개발 로드맵](docs/A_FIRST_B_LATER_PRODUCT_ROADMAP_20261114.md)
- [R21/R33 실제 납품 자산·저작권·제3자 라이선스 조사표](docs/R21_R33_SHIPPING_LICENSE_INVENTORY_20261114.md)
- [형이 실제 승인할 것만 한데 모은 승인 패킷](docs/OWNER_APPROVAL_PACKET_A_20261114.md)
- [고객 미수집 사전질문·로컬 납품 검수 단계](docs/A_CUSTOMER_INTAKE_AND_DELIVERY_QA_DRAFT_20261114.md)
- [R29 독립 외부 보안감사 요청서/수용기준](docs/R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md)
- [기계검증 로드맵](data/a_first_b_later_roadmap_v1.json) / `python -m unittest test_strategy_roadmap -v`

**현재 공식 최종설계 72/100; 목표85까지13점.** R07/R21/R25/R26/R29의 사용자 권리·개인정보/운영 승인 및 외부독립 감사 미완. `[작업중]`, RELEASE HOLD/SALE NO-GO 유지. 형의 A안 **방향승인만** 확정; 가격/상업사용권/상품등록/고객 자료 수신/감사비용의 포괄승인 아님.

## 2026-11-14 · Windows GUI 인터럽트 명시 종료 및 실EXE 회귀

`studio.py`의 Tk `KeyboardInterrupt`는 `{"action":"desktop","sale_approved":false,"status":"INTERRUPTED"}`와 종료코드130으로 기록하고 원본/경로/민감내용을 노출하지 않는다. 정상 창 닫기는 기존 코드0 유지. 정확 기능 SHA `0995e5824dea0c667ab13bc5fea191eca3ce705c`: [Windows·Ubuntu/Browser CI #43531946750](https://github.com/hibi89/data2web_studio/actions/runs/43531946750) **4/4 SUCCESS** (Win294 PASS, Ubuntu293PASS/1SKIP, Chrome/Edge/Chromium PASS). 첫 네이티브 빌드 자체검증 실패는 [#43531946776](https://github.com/hibi89/data2web_studio/actions/runs/43531946776)에 기록되고, redacted 상태 진단을 추가한 SHA `4af5b70cd6340f334ed16f293b80d923688265bc`에서 [native 재검증 #43532271904](https://github.com/hibi89/data2web_studio/actions/runs/43532271904) **SUCCESS**. 간헐 원인 미확인, 소유자 PC 새 EXE 검증 대기. [세부와 실제 최종85 수용 경로](docs/R32_INTERRUPT_AND_R01_R33_TO_85_PLAN_20261114.md).

**R01–R33 정본 최종72/100, 85까지13점**, `[작업중]` / RELEASE HOLD/SALE NO-GO 유지. 실제 실사용·권리·계약·외부 감사가 미완인 점수 항목을 기술 테스트로 대체하지 않는다.

## 2026-11-14 · Windows 독립 EXE 오너 전용 시범 빌드 (상업배포 불가)

정확 코드 SHA `96e2e1dff9976773bf3d3b2670ba6763ee69292d`: [Windows EXE native acceptance #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029) **1/1 SUCCESS**, [Python/Browser #43527161036](https://github.com/hibi89/data2web_studio/actions/runs/43527161036) **4/4 SUCCESS**, [Blueprint #43527161439](https://github.com/hibi89/data2web_studio/actions/runs/43527161439) SUCCESS. PyInstaller6.22.3 onedir의 embedded Python + Tk 동작을 합성 입력·Chrome/Edge·고객폴더 tamper/no-clobber까지 확인. 비공개 Actions artifact `DATA2WEB-UNSIGNED-OWNER-PREVIEW-WINDOWS` (2026-11-21 08:27 KST 자동 만료). `main` 미병합, 고객 PC·소유권/제3자 라이선스/상업 승인·서명은 미완성. [시범 실행 검증·사용자 최소수용 묶음](docs/R32_NATIVE_WINDOWS_OWNER_PREVIEW_20261114.md).

**고정 R01–R33 최종점수 72/100, 목표85까지13점**, `[작업중]`·RELEASE HOLD/SALE NO-GO. 기술 테스트 성공이 실구매자 인수나 권리 승인 아님.

## 2026-11-14 · ZIP 무결성 보안 강화, 고정 72점 유지

정확 소스 SHA `0cb09f86280f860b008e008da6ccaea8be068e29` [CI #43524908011](https://github.com/hibi89/data2web_studio/actions/runs/43524908011) **4/4 SUCCESS**, Windows291 PASS, Ubuntu290 PASS/1 SKIP, 브라우저 E2E PASS. 승인 상태 변조/가짜 서명·ZIP 앞뒤 숨은 데이터/댓글 거부, HTML/pyz 사전 bounded FD 점검 및 신규 보안회귀 7개. [보안 검증과 잔여 수용 게이트](docs/R22_R29_R32_HARDENED_ZIP_ACCEPTANCE_20261114.md).

**최종설계 R01~R33 72/100, 85점까지13점 미달.** 실 Windows10/11, 고객 원본·외부 라이선스/NOTICE·상업 승인·독립 보안감사는 별도. `[작업중]`, RELEASE HOLD/SALE NO-GO 유지. 비공개 소스/고객자료 외부 송신 없음.

## 2026-11-14 · Actions 한도 복구 및 동일 SHA 4/4 검증 완료

GitHub Actions 한도 문제 해결 후 정확 검증 HEAD `880586d7e63f38bd2c5e20f73f5bf46aa87d5d49`에서 [Python/브라우저 #43520777896 attempt2](https://github.com/hibi89/data2web_studio/actions/runs/43520777896) **4/4 SUCCESS**, [final blueprint #43520778342 attempt2](https://github.com/hibi89/data2web_studio/actions/runs/43520778342) SUCCESS. Windows 284 PASS, Ubuntu 283 PASS/1 SKIP; Windows Chrome·Edge, Ubuntu Chromium file:// E2E PASS.

신규 로컬 보고서 저장·비유한 JSON 영수증 거부 회귀가 포함된 **코드 검증은 PASS**, 그러나 R01–R33 인정 가중치 **72/100** 유지(실고객·권리·상업 승인 별도). **[작업중]/RELEASE HOLD/SALE NO-GO**. 아래 '신규 CI 검증 대기'는 해결 이전의 작업이력이며 현행 CI 판정이 아닙니다.

## 2026-11-14 · 로컬 장비 합성 검증 기록(신규 CI 검증 대기)

```bash
# 고객 원본은 읽지 않으며, 사용자 PC에서 신뢰하는 새 로컬 경로에만 저장
python studio.py self-check --browsers --evidence-output ./new-device-evidence.json
# 보고서 없이 기존 검사만 실행
python studio.py self-check --browsers
```

증거 파일은 unsigned 합성 실행 보고서이며 고객 실제 인수·저작권/개인정보 동의·판매 권리의 증거가 아니다. 파일을 자동으로 업로드하지 않으며 이미 존재하면 HOLD. 신규 코드 HEAD `b524cec2`에서 Actions가 실행 단계 0개로 실패하므로 **새 기능 미검증**; 기존 기준 `c2956397` CI 4/4 PASS와 혼동 금지. 최종완성률 **72/100**, 목표 85 미달. [증거/실행 장애 상세](docs/R23_R32_LOCAL_EVIDENCE_AND_CI_BLOCKER_20261114.md). **[작업중]/RELEASE HOLD/SALE NO-GO** 유지.

## 2026-11-14 · 최종설계 전체 100점 고정 평가 기준

사용자 지시로 점수 척도 선택을 위임받아 **5/20점 대신 100점 만점 + 기존 B안 가중치**를 고정 확정했다. REQUIREMENTS.md R01–R33 전체가 분모(축소0), 33개 가중치 합100, 22개 검증 요구 점수 합 **72/100**, 85 목표까지13점. 실사용/법적 판매·권리 수용과 구분하며 **[작업중]/RELEASE HOLD/SALE NO-GO**.

```bash
python blueprint_score.py
python -m unittest test_blueprint_score -v
```

[가중치 확정·실증 범위·차액](docs/FINAL_BLUEPRINT_WEIGHTING_100_APPROVED_20261114.md) · [요구33개 전체 감사](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md) · [기계 판독 점수표](data/final_blueprint_scorecard_v1.json).

## 2026-11-14 · 소유자 위임 3번 정책 기본안

최초 상용화는 **오프라인 HTML·ZIP 결과물의 1회성 납품 서비스**로 제안, 빌더 프로그램/서명 EXE 직접 판매는 보류. 내부 SKU 기본안 BASIC49,000원/PRO129,000원/BUSINESS249,000원(각 범위·수정/지원은 정책 참고), 원본·개인정보의 외부 업로드 기본 금지, 기밀/민감자료·사용권 불명확하면 HOLD, 원본 평문 복사 고지, 법정 소비자 권리를 제한하지 않는 환불/결함 시정. 실제 상업 저작권·LICENSE/NOTICE/약관·고객 자료 권리 확인/가격·출시 승인 전 **RELEASE HOLD**. [상품·데이터·권리·환불 운영 정책 초안](docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md).

## 2026-11-14 · R06/R22/R29/R32 고객 ZIP 검증/Windows 실행 개선

검증 코드 SHA 23a2d1293755294a58a20b98dc34e229a1e54f82. [Actions #43509224663](https://github.com/hibi89/data2web_studio/actions/runs/43509224663) **4/4 SUCCESS, Win Python269 PASS/Ubuntu268 PASS·Windows CMD1 SKIP**. 결정적 unsigned Python3.11 Windows bundle + 단일 ZIP bounded snapshot 내부 SHA 검사.

    python package_windows_bundle.py create ./new-unsigned-windows-bundle
    python package_windows_bundle.py verify ./new-unsigned-windows-bundle

생성 폴더의 RUN_SELFCHECK.cmd는 **합성 파일로만 Chrome/Edge 동작 확인**, RUN_DESKTOP.cmd는 소유자 직접 데이터/권리 승인, VERIFY_CUSTOMER.cmd는 고객 폴더 검증에 사용. 별도 Python3.11+·GUI Tcl/Tk 설치가 필요하며, 서명된 EXE·실 Windows10/11 수용·상업권리 승인 제품이 아니다. [기능·보안 근거](docs/FINAL_BLUEPRINT_R22_R32_PACKAGE_INTEGRITY_20261114.md). 공식 최종률 UNASSESSED, [작업중]·RELEASE HOLD 유지.

## 2026-11-14 KST · 인쇄·키보드 R16 실제 브라우저 검증

- A4 PDF(인쇄 현재 화면 최대50행 범위 명시)·표 줄바꿈/반복헤더, Chromium·Chrome·Edge `file://` PDF 생성·페이지/키보드 Space/ARIA E2E **실제 PASS**. [CI #43506243118](https://github.com/hibi89/data2web_studio/actions/runs/43506243118) 코드 SHA `4dc55cd73664db0e15b2554fc7b6c7087ffc8e85`, Windows/Ubuntu Python 각249 PASS, 4/4 SUCCESS.
- **최종설계 전체 공식률 `UNASSESSED`**; 소유자 미승인 B안 기술 상한72/100(이전69+R16 3), A안22/33 참고. 형의 가중치 승인 및 실 고객 PC·실 Excel/라이선스·고객인수 전 전체85% 달성 주장 금지.
- [R16 PDF/키보드 실증 및 실패 수정](docs/R16_PRINT_AND_KEYBOARD_ACCEPTANCE_20261114.md) · [전체 정본33요구](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md).

## 2026-11-14 · 공식 전체 85% 미도달 원인 및 사용자 결정안

[33개 최종설계 요구의 A/B 산정 기준과 최소 사용자 개입](docs/OWNER_85_COMPLETION_DECISION_20261114.md)을 작성했다. **가중치와 임시 시뮬레이션은 미승인**이며 공식 완성률은 `UNASSESSED`. 동일 합성/호스팅 실행 증거를 85%로 바꾸지 않는다. 실고객 Windows10/11·고객 Excel·상업 사용권·SKU/지원·환불/개인정보 보유 정책은 별도.

## 2026-11-14 · 고객PC 합성 자체검증·소스변경 방어 추가

기능 SHA 441506eda275b1e3766a4d018741ebfa1ae030b7 [실검증 CI #43501097784](https://github.com/hibi89/data2web_studio/actions/runs/43501097784) Win/Ubuntu 각249 PASS, hosted Windows Tk CSV/XLSX 실제 버튼 E2E 및 Chrome·Edge 네이티브 headless 합성 HTML PASS.

    python studio.py self-check --browsers
    python studio.py desktop
    python studio.py verify-customer ./new-client-folder

self-check는 고객 파일/개인정보를 열거나 업로드하지 않고 **합성 샘플만** 시험한다. 결과 PASS_SYNTHETIC_ONLY 는 해당 장비에서의 합성 기술점검이 통과했다는 뜻이지 사용자 권리·법률/상품 판매/실 Excel 수용이 아니다. [안전성·결과 근거](docs/FINAL_BLUEPRINT_P85_INPUT_RACE_NATIVE_BROWSER_20261114.md) / [R01–R33 전체 수용](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md). 공식 전체 85% 미인증/UNASSESSED, RELEASE HOLD 유지.

# DATA2WEB Studio — 데이터 파일을 오프라인 웹앱으로

**로컬 PC에서 CSV·JSON·TSV·제한 XLSX 입력 → 명시 권리/개인정보 검수 → 오프라인 HTML·ZIP·영수증.** 서버/원격 API 없이 작동. 모든 사용자 자료는 출력물에 평문 포함될 수 있다.

## 새 로컬 데스크톱 검수 및 폴더 전체 검증 (2026-11-13)

```bash
# Python 3.11+ 및 Tcl/Tk 포함 로컬 PC에서 실행 (외부 서버 없음)
python studio.py desktop
# 또는
python data2web_desktop.py

# GUI/CLI가 새로 만든 customer 폴더에 HTML·ZIP·영수증이 모두 일치하는지 검증
python studio.py verify-customer ./new-client-folder
python tool.pyz verify-customer ./new-client-folder
```

- 데스크톱 GUI는 현재 **단일 입력 파일**만 처리한다. 다중파일 `deliver-append`는 기존 수동 승인 매니페스트 기반 CLI를 사용한다. GUI가 고객의 파일 권리·민감정보를 법적으로 검사하거나 자동으로 판매를 승인하지 않는다.
- Windows 호스팅 환경의 실제 Tk GUI 렌더와 데이터 선택/동의/생성 컨트롤 headless 계약 테스트는 PASS, **실제 구매자 Win10/11 GUI 클릭 시나리오와 배포 서명 EXE는 미검증**. UI 구성요소가 설치된 Python에서만 실행 가능하다.
- `verify-customer`는 서명이 아니라 `index.html`, `delivery.zip`, `receipt.json`의 **같은 폴더 내부 무결성 일치**만 확인한다. 원본/실구매자 계약·개인정보 동의·상업권리·신원은 확인하지 않는다. 추가 파일·불일치 데이터는 HOLD.
- GUI 방식 선택 이유/제약 및 변조 시험: [docs/FINAL_BLUEPRINT_GUI_DELIVERY_20261113.md](docs/FINAL_BLUEPRINT_GUI_DELIVERY_20261113.md). 소유자 가중치 미승인으로 공식 85% 여전히 미인증.


**검증된 최신 코드 SHA `74f5f5a6b4625be3d510be5f59f1983be150b26e`** [Actions #43395679294](https://github.com/hibi89/data2web_studio/actions/runs/43395679294) GitHub 호스팅 Windows/Ubuntu 각 235 Python 테스트·Windows Tk GUI 41개 UI 컨트롤 렌더, Chrome/Edge/Chromium file:// QA 통과. **그러나 고객 실제 Win10/11, Excel 실문서, 권리/상용 라이선스 및 출시 전 최종 85% 승인 가중치 미완료.** `RELEASE HOLD`, `[작업중]`, 공식 `UNASSESSED` 유지.

## 기존 기능·전체 프로젝트 실행 지침(이력 보존)

## 최신 최종설계 전체 기준 개발·검증 (2026-11-13 KST)

**공식 최종완성률은 여전히 UNASSESSED; 전체 최종설계 85% 미인증**. 단, [정확 코드 `d311c47f1b85382f1d4ce43dfacdabcdc7e85612`의 CI #43392272159](https://github.com/hibi89/data2web_studio/actions/runs/43392272159)에서 **Windows·Ubuntu Python 각 210 PASS, Chrome·Edge·Chromium 실 `file://` 단일·다중 고객 폴더 HTML/ZIP·영수증 E2E PASS**, 원본 공개 REA Lite pinned commit `7b6b6811...`의 실제 런타임과 공통 CSV/JSON·테마·검색/분류·CSV 교체/재저장·거부 테스트 비교 PASS를 검증했다.

**새 단일 파일 고객 납품 CLI** (원본 권리·민감자료 검토 후):
```bash
python studio.py inspect input.csv
python studio.py deliver input.csv ./new-client-folder \
 --source-sha256 <inspect에서 얻은 64글자 SHA256> \
 --id id --title title --category category \
 --confirm APPROVE --ack-plaintext --privacy-classification NO_PERSONAL_DATA_REVIEWED
python studio.py verify ./new-client-folder/delivery.zip
```
XLSX는 `--sheet "실제 시트명"`도 필수. 명령은 **기존 고객 폴더/파일을 덮어쓰지 않으며** 출력에 평문 포함, 사용자 권리·개인정보 확인은 프로그램이 대신하지 않는다. 임의 JSON 중첩을 펼치지 않고 평면 단일 객체 또는 평면 객체 배열만 지원한다. [이번 추가 검증·미완료 범위](docs/FINAL_BLUEPRINT_85_REASSESSMENT_20261113.md).

# DATA2WEB Studio — 오프라인 XLSX / TSV / CSV / JSON 웹앱 생성기

## 사용자 최종설계 R01–R33 기준 재감사 · 2026-11-13 16:52 KST

**공식 최종완성률은 UNASSESSED, 최종설계 85% 미인증.** 기존의 '85% 기술 단계 완료'는 사용자가 요구한 최종설계 전체 85%가 아니었다. 이번엔 전체 33 요구를 재분해하고 R08/R13/R15/R24/R29/R32 등 실제 미구현 기능을 보완하여 [Windows/Ubuntu 190 PASS·브라우저 3종 합성 실제 실행 4/4 SUCCESS](https://github.com/hibi89/data2web_studio/actions/runs/43388705727)를 확인했다. **실고객 Win10/11·원본 Lite 실코드 full golden·가격/환불/지원·자료권리·가중치 사용자 승인 미충족이므로 판매·완료 주장 금지**. [요구별 증거/미충족](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md) · [고객자료/납품 HOLD 체크리스트](docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md).

### 신규 복수 파일 고객 납품 명령

```bash
python studio.py inspect first.csv
python studio.py inspect second.tsv
# 파일별 실제 SHA256, 동일 헤더와 사용권/민감정보를 확인한 후 approval.json 생성
python studio.py deliver-append approval.json ./new-customer-folder --confirm APPROVE --ack-plaintext
python studio.py verify ./new-customer-folder/delivery.zip
python package_portable.py local-builder.pyz
python local-builder.pyz inspect first.csv
```

승인 JSON 샘플/보안 한도/필수 입력은 [사용자 승인 대기 운영 가이드](docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md)에 있다. 파일 경로·SHA/원본 권리/민감정보 검토 없이 위 명령을 바로 실행하면 안 된다. 개별 파일은 같은 순서의 헤더만 append하며 JOIN·자동 추정/외부 업로드는 하지 않는다. `local-builder.pyz`는 **Python3.11이 반드시 필요한 서명되지 않은 zipapp**, Windows 설치형 EXE가 아니다.


**CSV·평면 JSON·TSV·보수적 Excel `.xlsx` 값 파일**을 사용자 PC에서 명시적 검수 후 독립 검색/분류/정렬/상세 HTML과 검증 ZIP으로 전환. 기존 REA_Web 웹사이트 분석 제품과 무관하며 원본 데이터를 서버/AI로 전송하지 않습니다. Python 3.11+ 기본 모듈만 사용하며 인터넷·계정·결제·데이터베이스 불필요.

> **2026-11-13 P85 검증:** [Windows145/145, Ubuntu145/145, Windows Google Chrome·Microsoft Edge, Ubuntu Chromium `file://` 전 경로 PASS(총 4/4 CI jobs)](https://github.com/hibi89/data2web_studio/actions/runs/43385035408), 정확 기능 SHA `709b2e5d5540893b9f7ad1b391584c6400899672`. **기술 85% 단계 검증**, 최종설계 전체 **공식 완성률 UNASSESSED**, 판매/납품 **RELEASE HOLD**. 고객 실제 Win10/11과 라이선스는 미검증.

## XLSX inspect → 시트 명시 승인 → build

```bash
python studio.py inspect workbook.xlsx
# status XLSX_SHEETS_REQUIRE_EXPLICIT_SELECTION, sheets + source_sha256
python studio.py inspect workbook.xlsx --sheet "Inventory" --header-row 1
python studio.py build workbook.xlsx new.html --source-sha256 <INSPECT의 실제 SHA256> \
  --sheet "Inventory" --header-row 1 \
  --id id --title title --category category \
  --confirm APPROVE --ack-plaintext --theme office --zip-path new.zip
python studio.py verify new.zip
```

셀 수식이 있는 경우 **기본 거절(HOLD)**. 캐시값을 사용해도 되는 소유자만 **inspect와 build 양쪽**에 `--allow-cached-formulas`를 별도 명시할 수 있습니다. 캐시가 없는 수식은 항상 거절하며 **Excel 수식/날짜 표시형식은 재계산·재현하지 않습니다**. 출력 HTML은 고객자료 **평문 포함**입니다.

## CSV/JSON/TSV

```bash
python studio.py inspect data.tsv
python studio.py build data.tsv app.html --source-sha256 <INSPECT의 실제 SHA256> \
  --id id --title title --category category \
  --confirm APPROVE --ack-plaintext --zip-path delivery.zip
```

CSV·JSON도 동일 명령에서 입력 확장자만 변경합니다. 새 HTML과 ZIP은 기존 경로를 **절대 덮어쓰지 않습니다**. HTML에는 3테마, 로컬 검색·카테고리·정렬·상세·페이징, **동일 헤더 CSV**의 사용자 동의 후 새 HTML 생성 기능이 포함됩니다. 생성·재저장 파일의 평문 포함과 공유 위험을 인지해야 합니다.

## 새 85% 기술 단계: 오프라인 차트·KPI·Chrome/Edge

- 원본 승인 데이터의 **전체 건수·표시 건수·고유 분류**를 표시하고, 현재 검색·필터 기준 **범주별 막대 차트**(최대 상위9+기타)를 그립니다. 지원 가능한 비음수 숫자열은 선택형 브라우저 **근사 산술합**으로 집계합니다. 단위·회계/재무 의미를 자동 확정하지 않습니다.
- 별도 라이브러리/서버/외부 폰트 없이 반응형·인쇄용 CSS로 작동하며, HTML·CSV의 스크립트처럼 보이는 내용은 실행하지 않고 문자로 렌더링합니다.
- 브라우저에서 동일 헤더 CSV를 새로 가져와 HTML을 저장하면 **기존 원본 SHA 및 XLSX 시트/수식 캐시 승인 메타는 지워지고, 새 데이터는 검증 전 상태로 표시됩니다.** 이전 ZIP 무결성 증거를 새 파일에 재사용하지 마십시오.
- 실제 GitHub hosted **Windows Server 2025의 Chrome/Edge**에서 앱·XLSX/TSV·ZIP/내보내기·재열기 E2E PASS; **개인/고객 Windows10/11 검증은 여전히 미완료**.
- 10,000×20 합성 행 CI 시연: 빌드 0.784s, Python 메모리 peak 31.85MiB, Linux Chromium 초기 0.256s·검색 0.027s·정렬 0.154s (**CI 1회 표본이며 고객 사용 성능 보증 아님**). 상세 [P85 수용 근거](docs/P85_UI_CROSSBROWSER_ACCEPTANCE_20261113.md).

## 지원 XLSX 보안 범위와 한계

- **지원:** `.xlsx` Open XML 기본 시트, inline/shared strings, 숫자 원시 문자열, Boolean, 헤더 1–50행, 시트명 명시 선택, 최대 10,000 데이터행·40열·16,000자/셀, SHA256 핀·ZIP CRC/압축비·외부 요청 방지.
- **거절:** 매크로/XLSM, OLE/임베디드 첨부, 외부 관계/하이퍼링크, DTD/ENTITY, 관계 경로 위조, 압축 폭탄, 중복 ZIP·열·헤더, 병합 셀, 숨김 시트, 미지원 OOXML 파트, Excel error, 수식 캐시 누락/명시 승인 없음. 서식·수식 계산·날짜 변환·연결/동적 배열은 완전 호환되지 않습니다.
- **실행 비용:** Python stdlib 0 추가 패키지/원격 API 비용0, 검증 CI에만 Playwright Chromium 별도 설치.
- **아직 미검증:** 실제 고객 Microsoft Excel·LibreOffice의 다양한 확장 포맷, 물리 Windows10/11 Edge·Chrome, 큰 데이터 10k×20 성능/원본 Lite real-runtime, 권리·라이선스·상용 판매 승인.

## 개발 검증
```bash
python -m unittest discover -v
# 브라우저 테스트 전용: pip install playwright==1.56.0; python -m playwright install chromium
python browser_probe.py
python browser_tabular_probe.py
python browser_p85_probe.py --channel chromium
python browser_perf_probe.py
# Windows 브라우저 검증 환경(Playwright Python 설치 후):
python browser_p85_probe.py --channel chrome
python browser_p85_probe.py --channel msedge
python browser_tabular_probe.py --channel chrome
python browser_tabular_probe.py --channel msedge
```

정본: [REQUIREMENTS.md](REQUIREMENTS.md), [docs/FINAL_DESIGN.md](docs/FINAL_DESIGN.md). 정확 검증 [P70 증거](docs/P70_XLSX_TSV_ACCEPTANCE_20261113.md), 현재 상태 [STATUS.md](STATUS.md), 인수인계 [HANDOFF.md](HANDOFF.md). 출고 금지 `RELEASE HOLD`.
