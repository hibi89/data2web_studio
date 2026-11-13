# DATA2WEB Studio — STATUS

## 2026-11-14 KST · 소유자 PC의 Windows 11 Pro 빌드 및 EXE 정본 SHA256 일치 확인
- **사용자 제공 실제 Windows 명령:** `Get-CimInstance Win32_OperatingSystem` 출력 `Microsoft Windows 11 Pro`, `Version=10.0.26200`, `BuildNumber=26200` → **Windows 11 Pro 26200 확인**(Windows 시스템의 내부 버전 10.0은 Windows11과 모순 아님).
- `Get-FileHash .\\DATA2WEB-LOCAL.exe -Algorithm SHA256` 소유자 출력 `87D0D28222A052CD5C8F4DA48922376EC72A604283B8021A775199F4FA0F4718`; GitHub native workflow [#43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029) EXE `sha256=87d0d28222a052cd5c8f4da48922376ec72a604283b8021a775199f4fa0f4718`와 **대소문자 무시한 64자리 완전 일치**. 출처와 실행물 버전 동일성 사용자 제공 증거 확보.
- 앞선 소유자 PC `self-check --browsers`의 Windows/Chrome/Edge 합성 스모크 `PASS_SYNTHETIC_ONLY`와 **연결된 정본 EXE**임이 확인됨. **소유자 Windows11 실제 PC의 로컬 합성 자가검사는 PASS**, 고객 실원본/실납품/Windows10/macOS/서명·판매 적합성/독립 보안감사는 미검증. 콘솔 출력은 사용자 보고값이며 기기 원격 직접 제어·제3자 attestation 아님.
- **가중 최종완성률 72/100 유지 (85까지13, 11항목 PENDING).** R23/32에 실제 Win11 실장비 증거를 추가하였으나 개별 항목의 *전체* 수용조건(Win10/macOS, 고객 독립 인수, 권리/서명/지원)을 충족하지 못해 각 점수는 0. `[작업중]`/RELEASE HOLD/SALE NO-GO, PR#4 Draft, 원본·점수표 수정0.
- 검증된 기초 제품 문서 SHA `37d4ee803c88c302c3a7d82838cb8717aecfb911`: [Python+browser CI #43528997740](https://github.com/hibi89/data2web_studio/actions/runs/43528997740) **4/4 SUCCESS**, [blueprint gate #43528998070](https://github.com/hibi89/data2web_studio/actions/runs/43528998070) SUCCESS. 다음: 실제 소유자 GUI `DATA2WEB-LOCAL.exe desktop` 사용성 검증, 고객 사용권/운영 정책 명시 승인 별도.


## 2026-11-14 KST · 소유자 실제 Windows PC에서 EXE + Chrome·Edge 합성 자체검증 PASS 보고
- **사용자 제공 PowerShell 5.1 콘솔:** `DATA2WEB-LOCAL.exe self-check --browsers` → `PASS_SYNTHETIC_ONLY`; `chrome=PASS_SYNTHETIC_LOCAL_FILE`, `edge=PASS_SYNTHETIC_LOCAL_FILE`, `local_folder_verified=true`, `platform_family=Windows`. 외부 데이터 업로드 필요0; 고객 원본·상업 권리 미승인 필드 `false` 그대로.
- 이는 기존 [native workflow #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029)의 hosted 검사와 구별되는 **사용자 제공 실PC 검사 결과**. **Windows10/11 정확 버전과 설치 EXE SHA256은 아직 미제공**, 실제 고객·소유권 독립 수용은 미검증. 정본 exe 해시 `87d0d28222a052cd5c8f4da48922376ec72a604283b8021a775199f4fa0f4718`(hosted CI 원본), 사용자 값과 대조 대기.
- R23/R32 수용 관련 증거 진전은 있으나 고정 R01–33 전체 **72/100 그대로**, 목표85까지13점 부족, `[작업중]`·RELEASE HOLD·SALE NO-GO. 보안·권리·실고객 수용은 대체 불가. 개인 계정명/PC 경로를 GitHub에 저장하지 않음. [상세/다음 OS·SHA 확인](docs/R23_R32_OWNER_WINDOWS_SELF_CHECK_20261114.md).


## 2026-11-14 KST · R32 독립 Windows EXE 시범판 최초 성공 (Python 경로 의존성 축소)
- **정확 제품 소스 SHA `96e2e1dff9976773bf3d3b2670ba6763ee69292d`**, [hosted Windows native EXE workflow #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029) **1/1 SUCCESS**, PyInstaller6.22.3 onedir 빌드 + 합성 Chrome/Edge + ZIP·receipt 검증 + no-clobber/tamper HOLD + 실제 Tk GUI 창 검사 PASS. 비공개 시범 artifact `DATA2WEB-UNSIGNED-OWNER-PREVIEW-WINDOWS` ID14085058847, 7일 보존(2026-11-21 08:27 KST 만료). Python 바이너리가 기본 PATH에 없는 조건에서 독립 EXE 실행 검증.
- 같은 정확 SHA [Windows/Ubuntu/browser CI #43527161036](https://github.com/hibi89/data2web_studio/actions/runs/43527161036) **4/4 SUCCESS** (Win Python291PASS, Ubuntu290PASS/1SKIP, Chrome·Edge/Chromium E2E PASS), [R01–33 최종설계 게이트 #43527161439](https://github.com/hibi89/data2web_studio/actions/runs/43527161439) SUCCESS.
- `native_windows_entry.py`, `native_windows_acceptance.py`, `.github/workflows/native-windows-owner-preview.yml` 추가. 첫 시험 SHA `2ee49504` 합성 CSV newline 오류 발견→수정→정확 SHA 성공. **R32 시범 EXE는 서명 없음/상업판 아님**; 실제 Win10/11 고객 장비/권리·서명·지원은 미검증.
- **전체 72/100 그대로** (고정 33요구, 11 pending, 85까지13점). 성공한 EXE 기술검증을 고객/법적 수용으로 대체하지 않음. `[작업중]`, RELEASE HOLD/SALE NO-GO, PR#4 Draft, 원본·main 불변. [상세와 남은 실수용 조건](docs/R32_NATIVE_WINDOWS_OWNER_PREVIEW_20261114.md).


## 2026-11-14 KST · ZIP 승인 위조·숨은 데이터·메모리 상한 보안 실증 (4/4 CI PASS)
- **기능/테스트 SHA `0cb09f86280f860b008e008da6ccaea8be068e29`** [CI #43524908011](https://github.com/hibi89/data2web_studio/actions/runs/43524908011) **4/4 SUCCESS** (Win 291/291 PASS, Ubuntu 290 PASS/1 Windows 전용 SKIP, hosted Chrome·Edge·Chromium E2E PASS), [final gate #43524908506](https://github.com/hibi89/data2web_studio/actions/runs/43524908506) SUCCESS.
- `verify_delivery` ZIP의 `RELEASE_HOLD` 상태/허용된 manifest keys 고정, 거짓 판매허가와 불필요한 signer 플래그·ZIP 댓글·앞뒤 숨은 데이터·비정형 member offset 거부. `delivery` 20MB bounded FD로 HTML 처리, `package_portable` 제한된 source/pyz 스냅샷. **악성/경계 회귀 7개 추가**, 기존 통과 기능 보존 확인. 중간 실패 `914c0e1d` 이스케이프 결함 수정 후 정확 SHA CI PASS.
- R01–R33 **공식 72/100 유지**: R06/R21/R29/R32 등 실장비·외부 라이선스/독립 감사의 잔여 수용 조건 변함 없음, 85까지13점. `[작업중]`/RELEASE HOLD/SALE NO-GO. 원본·기존 사업 상품 상태/배점 변경0. [상세](docs/R22_R29_R32_HARDENED_ZIP_ACCEPTANCE_20261114.md).


## 2026-11-14 KST · GitHub Actions 한도 해소 후 정확 SHA CI 복구 검증
- **코드/문서 정확 SHA `880586d7e63f38bd2c5e20f73f5bf46aa87d5d49`**, [GitHub Actions #43520777896 attempt 2](https://github.com/hibi89/data2web_studio/actions/runs/43520777896) **4/4 SUCCESS**, [final-blueprint evidence gate #43520778342 attempt 2](https://github.com/hibi89/data2web_studio/actions/runs/43520778342) **SUCCESS**.
- Windows Python3.11 **284/284 PASS**, Ubuntu Python3.11 **283 PASS/1 Windows 전용 SKIP**, Ubuntu Chromium `file://` E2E PASS, Windows 설치 Chrome·Edge의 `file://` E2E 및 Tk GUI/브라우저 자체검증 PASS. 이번에 추가한 synthetic self-check의 create-only JSON/sha 결과와 비유한 receipt JSON 차단 회귀 시험도 포함.
- 최초 attempts는 GitHub Actions 실행 단계 0개에서 조기 실패(한도 문제), 사용자가 한도 해결한 뒤 기존 failed jobs만 재실행하여 정상 PASS. 이전 failed attempts 기록 보존. **기존 문제를 앱 코드 오류로 오인하지 않음**.
- **평가 72/100 그대로:** 정본 R01–R33 고정100·22 VERIFIED/11 PENDING (28점), 목표85까지13점. 이번 성공은 신규 코드·합성 GUI/브라우저 보안 회귀 검증이지 실제 고객 Windows10/11·실업무 Excel/상업권리·계약/고객 인수 충족이 아님. R06/R07/R21/R23/R25/R26/R27/R29/R30/R32/R33 계속 PENDING.
- GitHub PR #4 Draft 미병합, 다른 소스·main·가중치 불변, `[작업중]`·RELEASE HOLD/SALE NO-GO. Vercel/Production 미적용. 다음은 사용자 승인·권리와 실제 기기/Excel 검증이 필요한 요구의 실수용 증거 수집 및 점수 재평가.


## 2026-11-14 KST · R23/R32 실장비 검증 증거 준비 및 영수증 JSON 안전성 보강 (신규 코드 CI 미검증)
- **최신 코드/테스트 HEAD:** `b524cec21c670f4696fc469fe96ed96bfd3cf562` (Draft PR #4, feature/final-blueprint-p85-evidence-20261113, main 미병합). `client_local_rehearsal.py`에 `save_rehearsal_evidence()` 추가: 실제 입력파일은 읽지 않는 합성 self-check를 사용자가 지정한 **신규 로컬 JSON 경로에 create-only** 저장, 기존 파일 덮어쓰기 금지, 보고서 SHA256 계산, 네트워크 전송 기능 없음. CLI: `python studio.py self-check --browsers --evidence-output ./new-local-device-report.json`. Python 3.11+ Chrome/Edge 필요, 기존 .pyz에도 모듈 포함.
- `verify_customer_folder.py` 고객 receipt/manifest JSON에서 NaN/Infinity/-Infinity 거부하도록 `parse_constant` 차단; 기존 중복키 거절 유지. `test_client_rehearsal.py` 및 `test_customer_folder.py`에 합성보고서 무덮어쓰기·HOLD·변조거부 회귀 테스트 추가. **해당 테스트는 신규 코드가 실제 성공했다는 증거가 아직 아님**.
- **CI 비실행 장애:** 신규 HEAD `b524cec2` [Python/browser Actions #43520221605](https://github.com/hibi89/data2web_studio/actions/runs/43520221605) **FAILURE**, [final-blueprint gate #43520221969](https://github.com/hibi89/data2web_studio/actions/runs/43520221969) **FAILURE**. 모든 Python/브라우저/최종 설계 job에 실행 step 0개, 시작 직후 실패. job logs 다운로드 404, checks는 annotation 수만 보이며 상세 판독 불가. **테스트 코드 실패로 단정 금지**; runner/계정 Actions 실행제한·워크플로 인증/결제 상태 등 계층 확인 필요. 반복 리런 금지, 실제 Windows/Ubuntu 회귀 **미검증**. 사전 기준 HEAD `c295639744e6bba06ab909070602c6235305fff9` [#43515478830](https://github.com/hibi89/data2web_studio/actions/runs/43515478830) 4/4 SUCCESS는 **새 코드에 적용 금지**.
- **점수/출시 판정 변동 없음:** R01~R33 전체 고정 100점, 검증 완료 22개/72점, 미검증 11개/28점, 목표85까지 13점. R23/R29/R32 및 상업/법적 수용은 자동 PASS 불가. **[작업중] / RELEASE HOLD / SALE NO-GO**, 상업 LICENSE/NOTICE 미승인, 실고객 Win10/11·Excel 미수용. 고객/실원본 업로드0, 기존 원본·고정 배점·main 불변. [실행 절차·진단](docs/R23_R32_LOCAL_EVIDENCE_AND_CI_BLOCKER_20261114.md).


## 2026-11-14 KST · 100점 만점 평가기 Windows 콘솔 회귀 최종 PASS
- 정확 채점기 SHA `6ce083ef763257b9ccb03bd3d81caad9a4ce4f66` [Actions #43515052630](https://github.com/hibi89/data2web_studio/actions/runs/43515052630) **4/4 SUCCESS**, Windows Python3.11 **280/280 PASS**, Ubuntu Python3.11 **279 PASS/1 Windows CMD-only SKIP**, Windows Chrome·Edge/Ubuntu Chromium 합성 file:// E2E PASS. Final blueprint evidence gate #43515053057 SUCCESS.
- `blueprint_score.py`의 stdout JSON 한글 `[작업중]` 때문에 일부 Windows PowerShell cp1252에서 `UnicodeEncodeError` 발생한 failed run #43514788415 원인을 ASCII-safe JSON으로 수정. `test_blueprint_score.py`에 cp1252 출력·JSON 재파싱 회귀 추가, `python blueprint_score.py` 양 OS 직접 실행에서 72/100·목표85·차이13/RELEASE HOLD 확인.
- 사용자 위임 R01–R33 전체 **100점/B안 고정 배점** 유지, 검증 가중치 **72/100**, 85 목표 미달 **13점**. 고객·법적·상업 승인 별개. **[작업중]**, RELEASE HOLD/SALE NO-GO, Draft PR 미병합. 원본/고객파일 변경0.

## 2026-11-14 KST · 실제 Windows 콘솔 채점 출력 회귀 수정
- `1f590d18f2448c294f23150f485c4278912613d6` [Actions #43514788415](https://github.com/hibi89/data2web_studio/actions/runs/43514788415) Windows Python 단위 테스트는 통과했지만 추가 `python blueprint_score.py` 직접 실행에서 Windows 콘솔 cp1252가 JSON의 `[작업중]` 한글을 출력하지 못해 UnicodeEncodeError/CI failure 발생. **점수 72/100 산정 오류 아님, Windows 출력 인코딩 문제**.
- `blueprint_score.py` CLI를 ASCII-safe `json.dumps(...,ensure_ascii=True)`로 수정하고 `test_blueprint_score.py`에 cp1252 환경 출력/파싱 회귀 추가. Linux 일반 유니코드 JSON 읽기 및 구조는 그대로. **정확 수정 SHA와 최신 CI 결과는 별도 검증 전 성공 주장 금지**.
- 배점 33개·총100, 인정 가중치72, 목표85/차이13, 출시 HOLD 상태/고객파일·원본 그대로.

## 2026-11-14 KST · 소유자 위임 100점 만점 최종설계 평가 확정
- **평가 기준 최종 확정: 전체 R01–R33 = 100점, 기존 B안 33개 고정 정수 배점(2~5점)**. 사용자가 5/20/100 중 선택과 진행을 위임해 100점 선택. 분모: REQUIREMENTS.md + docs/FINAL_DESIGN.md **전체, 범위 축소 0**. 부문 배점 입력18·검수20·생성26·납품20·비기능16.
- **현행 최종설계 기준 증거 가중치 72/100점, 85점 목표까지 13점 미달.** 22개 요구는 정확 SHA의 합성/호스팅·브라우저 증거로 해당 요구 범위 충족 처리; 11개 요구(외부 고객·권리/운영 수용 포함) 가중치 28점은 아직 0점. 72점은 판매가능성/고객 사용권/법률적 준수의 72% 증명 아님. 출시 `RELEASE HOLD/SALE NO-GO` 별개.
- **고정 검산·회귀:** `data/final_blueprint_scorecard_v1.json`, `blueprint_score.py`, `test_blueprint_score.py`. 무단 요구 누락·배점 합 변경·증거없는 VERIFIED·판매 GO 거절. `python blueprint_score.py`로 전체 R01–R33 100점 평가 출력. 33요구/22근거/11대기 추적; 추가 검증 없이는 점수 증가 불가.
- **기능 코드 기준 SHA `23a2d1293755294a58a20b98dc34e229a1e54f82`** [Actions #43509224663](https://github.com/hibi89/data2web_studio/actions/runs/43509224663) **4/4 SUCCESS**, hosted Windows269/269·Ubuntu268+1WinCMD skip, 이전 브라우저/실 Windows GUI/ZIP/원본 Lite golden PASS. 100점 채점기 첫 commit `380055beea7c92ad8dd58dd76b953654498eab08` 새 채점기 CI #43513559502에서는 Win279/279·Ubuntu278+1SKIP PASS지만 Edge 자가검증 1회 일시 HOLD; **정확 문서 HEAD 1a2440cbe6fc57cae51bbfae6732b79eab440caa Actions #43514132305 4/4 SUCCESS**와 정본 검증 게이트 #43514132935 SUCCESS로 재확인. Edge 일시 실패 기록은 보존.
- [현행 100점 배점과 목표차](docs/FINAL_BLUEPRINT_WEIGHTING_100_APPROVED_20261114.md), [요구별 실행 근거](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md), [3번 내부 정책](docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md). 배점 변경은 별도 명시적 재승인·버전 갱신 필요. **[작업중], RELEASE HOLD/SALE NO-GO**, 미서명 EXE·실고객 Win10/11/실Excel/저작권·개인정보·크몽 출시 승인 미검증.

## 이전 기록(점수 기준 승인 전 이력 포함)
## 2026-11-14 KST · 사용자 위임: 3번 상품/데이터/환불/라이선스 운영안 설계
- 사용자는 **3번 정책 판단·문서 작성을 AI에 위임**, 가중치 개념을 질문. 이번에 [상품화 운영 정책 초안](docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md) 신규 작성: 오프라인 HTML/ZIP **1회성 납품 대행형**을 초기 채택, 별도 판매자/고객 Python/Tk 설치가 필요한 **빌더 자체 라이선스 배포형**은 보류.
- 제안 SKU(미게시/미확정 가격): BASIC **49,000원** 단일 CSV/JSON/TSV 1천행·20열·1수정·7일 결함지원, PRO **129,000원** XLSX 1시트 또는 3개 동일스키마 append·5천행·2수정·14일, BUSINESS **249,000원** 2~10개 동일스키마 append·1만행·3수정·30일. 일반 A4/브라우저/검색·차트·ZIP·영수증은 기존 제품 기능/요구 안에서만 제공. **실제 크몽 상품 등록·표시가격 확정 아님**; 원본 처리·현실 납기/세무/플랫폼 검토 전 판매 금지.
- 데이터 기본안: 고객 실원본 제3자/AI/GitHub 자동 업로드0, 민감/PII·사용권 불분명한 자료 기본 HOLD, 고객 PC 원본 무삭제, 처리한 판매자 복제본은 목적달성/보존의무에 따라 별도 적법한 폐기 절차·기록 수립. 실제 프로그램에 자동 삭제/익명화 기능 있다고 홍보하지 않음. 상용 코드/출력 LICENSE·NOTICE는 권리 체인 검증 전 배포 승인 금지.
- 환불: 주문/용역 개시 전 원칙적 전액환불, 진행 중에는 제공하지 않은 범위를 포함해 법령·크몽 운영규정에 따라 정산, 결함·계약 불이행 시 시정/재납품·법정 소비자 권리 보존. '디지털 결과물이니 무조건 환불 불가' 금지. [개인정보 보호법 제21조](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1029335641)와 [전자상거래법 제17조](https://www.law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1027063323) 확인 근거를 정책 문서에 기록.
- **요구 R25/R27/R33은 정책 초안을 작성했다는 이유만으로 구현/권리·판매 수용 PASS 처리하지 않음.** 공식 최종완성률 `UNASSESSED`, 기술 참고 B 72/100(사용자 미승인), `[작업중]`·RELEASE HOLD/SALE NO-GO 유지. 코어/CI 마지막 검증 SHA `23a2d1293755294a58a20b98dc34e229a1e54f82`, [Actions #43509224663](https://github.com/hibi89/data2web_studio/actions/runs/43509224663) 4/4 SUCCESS, Win269/269·Ubuntu268+1 WinCMD SKIP. 이번 문서 변경은 별도 기능 테스트 진전이 아님.

## 2026-11-14 KST · 최종설계 전체 85% 목표 후속 R06/R22/R29/R32 실제 개발
- **공식 최종완성률 UNASSESSED / 사용자 전체 R01–R33 85% 미인증.** 전체 사용자 정본 가중치 합100·실 고객/권리 수용 미승인, 내부 기술 테스트 건수로 공식 퍼센트 추정 금지.
- 정확 기능 SHA 23a2d1293755294a58a20b98dc34e229a1e54f82, [GitHub Actions #43509224663](https://github.com/hibi89/data2web_studio/actions/runs/43509224663) **4/4 SUCCESS**. Windows Python3.11 **269/269 PASS 0FAIL/0SKIP**, Ubuntu3.11 **268 PASS/1 Windows CMD 전용 SKIP/0FAIL**. 기존 Chromium/Windows Chrome·Edge file:// GUI·A4 인쇄·원본 Lite golden·성능 회귀 PASS.
- R06/R22/R29: ZIP 검사·SHA를 24MB bounded **한 파일핸들 스냅샷**으로 수행, 두 시점 ZIP SHA가 다르면 고객 폴더 검증 HOLD; 승인 JSON·HTML/receipt 제한읽기, 중복 JSON·비유한 숫자/바꿔치기 부정 테스트 8개 추가.
- R32: **미서명 Python3.11 .pyz + Windows CMD 3종 + README + SHA manifest** 새폴더 생성·독립 검증. Windows hosted 실제 CMD 실행·Chrome/Edge 자가검증 PASS. 12개 새 시험; 실제 Win10/11 고객 설치, 서명 EXE·고객 지원 정책 미검증.
- 33개 정본 기술 범위 분류 **22개 근거 확보/11개 부분 또는 외부승인** 유지. 이전 미승인 참고 A안 22/33≈66.7%, B안 72/100 유지(공식률 아님). 외부 독립 보안감사·실 PC/데이터·권리 조건이 남아 R29/R32 전체 완료 판정 아님.
- [신규 R06/R22/R29/R32 검증 보고](docs/FINAL_BLUEPRINT_R22_R32_PACKAGE_INTEGRITY_20261114.md), [R01–R33 전수 감사](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md). [작업중], RELEASE HOLD/SALE NO-GO, 기존 main/P50/P70/P85/REA_Web 원본 유지. Production/Vercel 미적용.

## 2026-11-14 KST · 사용자 전체 최종설계 85% 목표 진행(기술 R16 추가 검증)
- **사용자 정본 전체 R01~R33 기준 공식 완성률 `UNASSESSED` · 85% 미인증.** 최초 21개 합성 기술 근거에서 **R16 인쇄·키보드 기능**이 실브라우저 QA PASS를 확보해 **22개 기술 범위**로 증가. 사용자 승인 가중치 없으므로 기술 근거 수를 공식률로 환산하지 않는다.
- 정확 기능 SHA `4dc55cd73664db0e15b2554fc7b6c7087ffc8e85` [Actions #43506243118](https://github.com/hibi89/data2web_studio/actions/runs/43506243118) **4/4 SUCCESS**, Windows Server2025/Ubuntu24.04 Python3.11 각 249/249 PASS. 실제 file:// Chromium/Win Chrome·Edge **A4 PDF 생성·화면 페이지별 50행 범위·Space/Enter·ARIA 및 원격요청0 PASS**. 기존 실제 Tk CSV/XLSX·입력 SHA·고객폴더 ZIP+영수증·원본 Lite golden·1만행 성능 회귀도 PASS.
- 변경 기능: `data2web_web.py` A4 @page, 인쇄 테이블 줄바꿈/반복 헤더 및 범위 고지, 출력 시 이전 선택 상세 숨김, 키보드 Space/Enter 및 행 접근성 라벨. `browser_print_accessibility_probe.py` 실제 페이지 1/2 PDF 구조·A4·pdf text extraction과 키보드 E2E. **실물 프린터 시각 검증/실구매자 OS는 미검증**.
- **실패 복구:** 최초 Actions #43505858144는 PDF 텍스트 추출 순서와 이전 선택 상세를 잘못 가정하여 브라우저 QA FAIL. 검증방법과 인쇄 콘텐츠를 분리 개선하여 #43506243118 PASS. [자세한 실증](docs/R16_PRINT_AND_KEYBOARD_ACCEPTANCE_20261114.md).
- **미승인 참고 산정안만:** A 동등 22/33≈66.7%, B 가중 72/100 기술 근거 상한. 둘 다 **공식률 아님**, 형의 가중치 확정과 실 고객/권리 수용 전에는 `UNASSESSED` 유지. B안 시뮬레이션상 남은 13점 추가 수용 증거 필요, 사용자 의사로 사후 가중치 변경 금지.
- 남은 필수 R06/R07/R21/R23/R25/R26/R27/R29/R30/R32/R33의 일부·외부 승인/실장비 수용. `[작업중]`·`RELEASE HOLD/SALE NO-GO` 유지; 기존 원본/브랜치/main·판매정보 변경0, Production/Vercel 미적용.
- [최종 R01–R33 전수 감사](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md), [가중치 승인안](docs/OWNER_85_COMPLETION_DECISION_20261114.md). 개발 기능/문서 증거 GitHub 및 중앙 크몽 상품 원장 동기화 예정.

## 이전 진행 기록(보존)
## 2026-11-14 KST · 85% 공식 완료 판정 왜 보류되는가 (산정 근거 확정 대기)
- **최종설계 공식 완성률: UNASSESSED / 사용자 목표85 미인증.** 33개 정본 요구의 소유자 승인 가중치가 존재하지 않고, 12개 항목에는 실환경/법적·고객 수용이 남아 있음. 70→85 UI·ZIP 단계 기술 통과와 전체 공식85% 완료는 별개.
- [**소유자 승인 최소 개입 결정안**](docs/OWNER_85_COMPLETION_DECISION_20261114.md)을 새로 작성. 전수 33개를 누락 없이 두 대안 A=동등비중 21/33(기술 증거 63.6%), B=입력18·전처리20·생성26·납품20·비기능16(기술 증거 69/100)으로 **시험만** 수행. 둘 다 **사용자 미승인/비공식/고객 법적 수용 미인증**; 85를 맞추기 위한 가중치 재조정 금지. B를 승인해도 추가 최소 16점 수용 근거가 필요.
- 형이 직접 결정해야 할 최소 사항: 가중치 A/B 또는 수정안 승인, 실제 Win10/11 PC에서 `python studio.py self-check --browsers` 실행 증거; 실제 상용 판매 전 데이터권/개인정보·LICENSE/NOTICE·SKU·지원/환불은 **별도 명시 승인**. 코딩·QA·문서·크몽 원장 동기화는 AI 담당.
- 최신 검증 기능 SHA `441506eda275b1e3766a4d018741ebfa1ae030b7`, [Actions #43501097784](https://github.com/hibi89/data2web_studio/actions/runs/43501097784) Windows/Ubuntu 249×2 PASS, 4/4 SUCCESS, hosted Tk CSV/XLSX 실제 GUI 클릭·네이티브 Chrome/Edge 합성 PASS. **실 고객 OS·권리 승인으로 전용하지 않음.**
- [작업중]·RELEASE HOLD/SALE NO-GO 유지, 원본 및 고객자료/기존 브랜치 보존, Production/Vercel 미적용. 문서 제안은 공식률 변경이나 판매 승인 아님.

## 이전 상태 이력
## 2026-11-14 KST · 최종설계 R01–R33 전체85% 목표 추가 개발
- **공식 최종완성률 UNASSESSED, 전체 85% 미인증.** 사용자 승인 합100 요구 가중치·실고객 Win10/11/Excel·사용권/사업자 인수 부족. 내부 기술 단계 85%와 혼용 금지.
- **기능 SHA 441506eda275b1e3766a4d018741ebfa1ae030b7** [Actions #43501097784](https://github.com/hibi89/data2web_studio/actions/runs/43501097784) **4/4 SUCCESS**, Windows2025/Ubuntu24.04 Python3.11 각각 249/249 PASS·0 FAIL/0 SKIP, hosted Tk 실제 CSV/XLSX UI 버튼 전경로 PASS, 설치 Chrome/Edge 네이티브 headless self-check PASS, Playwright Chrome/Edge/Chromium·Lite 원본 골든·10k×20 합성 PASS.
- **신규:** path_policy bounded file handle/O_NOFOLLOW+fstat/lstat 원본 식별 및 변경확인, data2web/append/desktop 독립 읽기에 적용; test_snapshot_safety 경로 교체/파싱변경 HOLD. 고객 파일 없는 client_local_rehearsal + studio.py self-check --browsers + portable .pyz, test_client_rehearsal. Windows Tk 실제 소유자 버튼 탐색 desktop_ui_owner_flow_probe 추가.
- **실패·수정:** append 출력 HTML 잘못 치환 NameError 회귀 10건 수정, Chrome/Edge native 셀프체크 존재하지 않는 span 검색 수정, 동일 입력/반대 사례 추가 후 최신 SHA 정상 PASS. 원본 데이터/REA_Web/main/P50/P70/P85 보존.
- **전수 감사:** [docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md) R01~R33 손상된 상단 행/이전 테스트 수치를 수정하고 정확한 최신 근거로 재구성. [이번 구현 증거](docs/FINAL_BLUEPRINT_P85_INPUT_RACE_NATIVE_BROWSER_20261114.md).
- **미검증·보류:** 실제 고객 Win10/11·macOS Tk/Chrome/Edge, 업무 Excel, 고급 OS TOCTOU 공격, 상업적 LICENSE/NOTICE, 고객자료 권리·개인정보 보유/파기, 상품 가격/지원/환불·독립 인수·서명 EXE. [작업중] / RELEASE HOLD / SALE NO-GO 유지. Vercel·Production 미적용.

## 과거 상태 이력
## 2026-11-13 KST · 최종설계 전체 85% 실작업(추가) · 정확 기능 SHA 74f5f5a6b462
- **공식 최종완성률 UNASSESSED / 전체 정본 85% 미인증.** 사용자 최종설계 전부 `REQUIREMENTS.md` R01–R33을 100%로 하는 공통 `OWNER-FINAL-BLUEPRINT-100` 준수. 승인 가중치 합100, 실제 고객/권리·판매 수용 없이 합성 테스트 건수를 퍼센트 환산하지 않음.
- **이번 구현:** 선택형 독립 로컬 Tkinter GUI(`data2web_desktop.py`, `studio.py desktop`)에서 소스/시트/컬럼/원본 SHA/권리·평문·개인정보 수동 검수→기존 SHA pinned single-file HTML·ZIP·JSON receipt 고객 신규폴더 생성. `verify_customer_folder.py`는 전체 고객 폴더 HTML/ZIP/receipt 교차검증, 불일치/추가파일/영수증 변조/ZIP 교체 등을 HOLD. `studio.py verify-customer`, `.pyz` 동일 실행.
- **검증 SHA `74f5f5a6b4625be3d510be5f59f1983be150b26e`** [Actions #43395679294](https://github.com/hibi89/data2web_studio/actions/runs/43395679294): Win Server2025/Ubuntu24.04 Python3.11 **각 235 PASS / 0 FAIL / 0 SKIP**, Linux Chromium·Windows 실제 Chrome/Edge의 합성 CSV/JSON/XLSX/TSV 단일/복수 데이터 `file://` 테스트/원본 Lite golden, 호스팅 Windows Tkinter 실제 41 컨트롤 생성 PASS. 독립 GUI 컨트롤/승인기 계약·파일 바꿔치기 경계 테스트 포함.
- **남은 수용:** 실제 구매자 Win10/11 Chrome/Edge와 GUI 직접 조작·고객 Excel 워크북/영수증, macOS 기기, R25 보유/삭제 정책, R21 LICENSE/NOTICE·R27 SKU/가격/지원/환불·R33 고객 파일 사용권/상용 재배포/실 고객 인수, R06/29 경합·외부 보안감사·실장비 테스트, R32 Python/Tk 설치 지원/서명 EXE. 출시 `RELEASE HOLD/SALE NO-GO`.
- **사용자 [작업중] 유지:** 승인된 요구가 충족됐다는 전체 최종설계 85% 증거가 없어 마커 해제 금지. `main`, P50/P70/P85 baseline, 원본 REA_Web 수정 없음. [전체 33요구 추적](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md), [GUI/고객 폴더 수용근거](docs/FINAL_BLUEPRINT_GUI_DELIVERY_20261113.md). Production/Vercel **미적용**(오프라인 제품).

## 과거 상태 (보존, 현행 공식률 아님)
## 2026-11-13 KST — 사용자 지정 전체 최종설계 85% 목표 후속 결과
- **정식 전체 최종완성률 UNASSESSED, 최종 85% 미인증**. 확인된 개발 기능이 많아져도 최종설계 R01–R33 승인 가중치·실 고객/권리 수락 없이는 퍼센트 임의 산정 금지.
- 정확 검증 **코드 SHA `d311c47f1b85382f1d4ce43dfacdabcdc7e85612`**, [GitHub Actions #43392272159](https://github.com/hibi89/data2web_studio/actions/runs/43392272159) **4/4 SUCCESS**; Python Windows/Ubuntu **각 210 PASS·0 FAIL·0 SKIP**, Windows Chrome·Edge / Linux Chromium에서 CSV/JSON/XLSX/TSV 단일/다중 납품 및 검색·교체·재저장 실제 `file://` QA PASS. 데이터 외부전송0.
- 신규 R02 평면 JSON 단일 객체·비유한 숫자 HOLD, R24 단일 파일 새 고객 폴더 HTML+ZIP+영수증 납품, R31 원본 공개 REA_Web `7b6b6811...` 실제 코드와 합성 CSV/JSON·테마·동일 헤더 CSV 업데이트·HTML 재열기 기능 골든 비교 PASS. **전체 픽셀/모든 확장동작 동등성은 미주장**.
- 신규 코드 `data2web_single.py`, `test_single_delivery.py`, `browser_single_delivery_probe.py`, `upstream_runtime_golden.py`. GitHub Actions에 exact upstream read-only checkout 단계 추가. 이전 R08/R13/R15/R24/R26/R29/R32와 호환 유지.
- 사용자 최종설계 전체 기준 잔여: 실 구매자 Win10/11/macOS·실 Excel 고객자료, R21 LICENSE/NOTICE·R25 보유/파기·R27 SKU/지원/환불·R33 고객자료 권리/재배포/사용자 인수 **대기**; 공식 R01–R33 가중치 미확정, 실경합/보안 독립감사 부분 미검증. 판매/배포 금지.
- 신규 [최종설계 후속 개발·검증 보고](docs/FINAL_BLUEPRINT_85_REASSESSMENT_20261113.md), [33요구 전수 감사](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md) 업데이트. 원본 REA_Web/P50/P70/P85 기존 브랜치와 `main` 원본 SHA 불변.
- 브랜치 `feature/final-blueprint-p85-evidence-20261113`. 크몽 `[작업중]`, RELEASE HOLD/SALE NO-GO 유지. 프로그램 로컬·Vercel N/A.

## 이전 상태 기록 (보존, 최신 산정이 아님)
## 최신: 2026-11-13 16:52 KST · 사용자가 지정한 최종설계 85% 재검증 작업
- **최종설계 전체 공식 완성률 = UNASSESSED / 85% 미인증(목표 미달 판정).** 이전 '85% 기술단계 완료' 답변을 정식 최종완성률 85%로 해석한 것은 오류였다. 사용자 최종설계 `REQUIREMENTS.md` R01~R33 전체/소유자 확정 가중치/실고객 인수를 기준으로만 공식 산정한다.
- **R01~R33 전수 추적:** [docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md](docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md) 완성. 모든 행의 가중치는 승인 전으로 비워두었고 합성 CI/실 고객/법적 승인/미검증 구분. 전체 85% 수치를 임의 생성하지 않는다.
- **실 기능 추가:** R08 개인정보 자동 통과를 주장하지 않는 원문 미출력 컬럼 프로파일·NULL/중복/형 힌트; R13 각 원본의 실 SHA·권리/평문·개인정보 수동 분류 승인 후 동일 순서 헤더 최대10개 CSV/JSON/XLSX/TSV append(추정 JOIN 금지), 파일 간 ID 중복/경로/시트 SHA 오류 HOLD; R15 Ctrl/⌘ 다중 분류 필터; R24 신규 고객 폴더에만 HTML+ZIP+SHA 영수증 생성·무덮어쓰기; R29 입력/출력 전체 경로 symlink/reparse/junction `..` 거부; R32 Python3.11 표준 라이브러리만 쓰는 결정적 `.pyz` 빌더/실행 검증. 기존 P50/P70/P85 구현과 REA_Web 원본 불변.
- **실제 CI 증거:** 기능 검증 정확 SHA `0ee4a9d8810d78c47b35cbd41bc69725674db4cc`, [Actions #43388705727](https://github.com/hibi89/data2web_studio/actions/runs/43388705727) **4/4 SUCCESS**. Windows Server2025 Python3.11 **190 PASS/0 FAIL/0 SKIP**, Ubuntu24.04 Python3.11 **190 PASS/0 FAIL/0 SKIP**. Windows 설치 Chrome·Edge와 Linux Chromium에서 CSV/XLSX/TSV→HTML·ZIP·요약 차트·복수 원본/파일별 SHA·CSV 재교체/재열기와 출처 무효화 실제 `file://` E2E PASS, 외부 HTTP(S)0/pageerror0. 합성 10,000×20 성능 시험 PASS(자세한 값 CI 로그).
- **아직 충족하지 못한 수용 조건:** R23/R30 실제 사용자의 Windows10/11 Chrome·Edge/macOS 독립 인수, R31 원본 REA Lite full actual-runtime 비교, R21/R27/R33 LICENSE·판매·재배포·가격·지원·환불/고객자료 실제 소유권 승인, R25 개인정보 보유·파기 정책 승인, R32 실제 고객용 포터블 패키지/EXE 서명·지원. XLSX strict OOXML 범위 밖 Excel 서식·캐시 실제 호환은 실고객 미검증. R24 단일파일 새 폴더 workflow 등도 부분.
- **보안·운영:** RELEASE HOLD/SALE NO-GO, `[작업중]` 유지. `main` 및 `feature/lite-independent-migration`, `feature/xlsx-tsv-import`, `feature/p85-ui-crossbrowser-20261113` 변경하지 않음. Vercel/Production 미적용(단일 HTML 로컬 제품).
- **현재 개발 브랜치:** `feature/final-blueprint-p85-evidence-20261113`. 사용자 개입 없이 가능한 기능 보완과 합성/호스팅 브라우저 CI는 완료. 사용자 승인/실 고객 PC/권리 검증은 **검증 대기**. 실행·법적 승인 없는 85% 달성 주장 금지.
- **운영정책:** [소유자 고객자료·납품 보류 체크리스트](docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md), 다음 단계는 요구/승인/고객 현장 근거가 마련되면 검증한 범위만 갱신. 해총 크몽 브랜치 상품 원장은 별도 커밋/HEAD 확인 후 동기화.

## 과거 개발 이력 (역사 자료로 보존, 최신 판정 아님)
## 2026-11-13 16:21 KST · P85 기술 단계 구현·실기능 검증
- **공식 최종설계 완성률 UNASSESSED**. 사용자 지시 P70→P85 **기술 단계 검증 통과**; 전체 `REQUIREMENTS.md` R01–R33의 소유자 확정 가중치·실고객 인수가 없어 최종 85%를 공식 수치로 대체하지 않는다.
- **GitHub:** `hibi89/data2web_studio@feature/p85-ui-crossbrowser-20261113` 기능 검증 `709b2e5d5540893b9f7ad1b391584c6400899672`. `main`, P50, P70 기존 원본 기능은 그대로 보존, 미병합.
- **UI:** 기존 CSV/JSON/XLSX/TSV → 승인 HTML/ZIP 유지. 범주별 상위9+기타 막대 차트·실시간 필터/검색·숫자열 비음수 합계(단위·회계 의미 추정 금지)/전체·표시·분류 KPI·모바일 반응형·인쇄 CSS 추가. `textContent`으로 카테고리 XSS 방어.
- **보안:** 웹에서 CSV 교체 후 저장 시 원본 SHA·Excel 시트/수식 캐시 승인 메타 초기화, 출처 **재검증 필수** 경고; 원본 승인 ZIP 증거 재사용 금지. 외부 HTTP(S) 요청0·JS 오류0, 기존 create-only ZIP/독립 verifier 유지.
- **검증:** [Actions #43385035408](https://github.com/hibi89/data2web_studio/actions/runs/43385035408) **4/4 SUCCESS**. Windows Server 2025 Python3.11 **145/145 PASS**, Ubuntu24.04 **145/145 PASS**, Windows 설치 Google Chrome·Microsoft Edge의 `file://` 차트/다운로드/재열기와 XLSX·TSV 각 E2E **PASS**, Ubuntu Chromium의 P50/P70/P85 경로 **PASS**.
- **실측:** 10,000×20 합성 CSV **1,125,142B**, HTML **3,563,255B**, 빌드 0.784s·peak Python 31.85MiB, Chromium 초기0.256s·검색0.027s·정렬0.154s (GitHub runner **1회**, 고객 PC 성능 보장 아님). [상세 수용 감사](docs/P85_UI_CROSSBROWSER_ACCEPTANCE_20261113.md).
- **남은 작업:** R13 다중 승인 파일 append, R23 실제 Windows10/11 Chrome·Edge 구매자 장비 시험, R31 REA Lite 원본 full real-runtime 비교, 고객 Microsoft Excel 복잡 워크북/날짜·서식·시트, 고급 UX/실고객 인수·외부 설치/서명/법적 상용권·고객 지원 약관. R18 요약 차트는 합성 검증 범위에 한정.
- **운영:** `[작업중]`(공식 사용자 목표 미인증)·`RELEASE HOLD/SALE NO-GO` 유지. Vercel/Production **미적용**(완전 로컬 HTML 제품). 유료 API·클라우드/민감정보/인증변경/고객파일 업로드 없음.

## 과거 P70 기록(보존)
## 최신 · 2026-11-13 KST · P70 기술 단계 검증
- 대상 `hibi89/data2web_studio@feature/xlsx-tsv-import`. 과거 `feature/lite-independent-migration` 검증 P50 코드/원본 SHA `f613305dee8c8ceb8636632bce001b1c02532e35`는 병합 부모로 보존(이력상 P50 검증 기술 SHA `90da878ffa29926dda39f6c67913353ec7a3b390`).
- **최종설계 공식 완성률 UNASSESSED(미산정)**, 사용자 **70% 목표의 기술 단계** 구현·검증 PASS. R01–R33 사용자 승인 가중치 미존재, 기술 마일스톤을 공식 퍼센트로 오인 금지.
- **기능:** `data2web_tabular.py` 독립 XLSX 정적 값·시트/헤더행/명시적 캐시 승인·매크로/외부링크/압축/XML/중복 위험 HOLD + TSV UTF-8/인용구문; inspect → SHA/시트 선택/권리·평문 승인 → HTML/ZIP → 독립 verifier. 기존 CSV/JSON·브라우저 기능 유지, 데이터 외부 전송 없음.
- **실행 증거:** 정확 코드 `42b832c5e18521d3edcf53b69cbf92c272f245cb` [Actions #43381537805](https://github.com/hibi89/data2web_studio/actions/runs/43381537805) **3/3 SUCCESS**. Windows2025 Python3.11 **145 PASS/0 FAIL/0 SKIP**, Ubuntu24.04 **145 PASS/0 FAIL/0 SKIP**, 실제 Linux Playwright Chromium `file://` P50+XLSX+TSV 2경로 E2E PASS, 네트워크0/JS 오류0. 실제 Microsoft Excel 복합 사용원본·실구매자 Win10/11 Chrome/Edge 미검증.
- **잔여:** R13 복수 파일 append, R18 차트, R28 대용량 성능, R31 원본 Lite real-runtime 전체 골든, R23 실 Windows 고객 장비, R33 사용권/상업 인수/법무; XLSX 셀 서식·날짜·완전한 Excel 수식 계산은 지원 범위 아님. 안전 지원 OOXML 프로필 밖은 HOLD.
- **출시:** RELEASE HOLD/SALE NO-GO, Production/Vercel 미적용. 기존 `REA_Web`/P50 개발 브랜치 원본 변경 금지. 크몽 `[작업중]` 제거 금지.
- **인수증거:** [docs/P70_XLSX_TSV_ACCEPTANCE_20261113.md](docs/P70_XLSX_TSV_ACCEPTANCE_20261113.md). 다음 개발 목표는 **사용자 요청 전 임의 설정 금지**.

## 이전 P50 기록
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