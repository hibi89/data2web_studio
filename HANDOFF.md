# DATA2WEB Studio — HANDOFF · 2026-11-14 KST · 100점 가중치 소유자 위임 확정

## 최신 사용자 PC 증거 인수인계 — 2026-11-14 KST
1. **목표·용도·정본:** DATA2WEB Studio CSV/JSON/TSV/XLSX→오프라인 HTML/ZIP/로컬 Windows EXE; R01~R33 고정100점, 목표85점.
2. **변경·진전:** 사용자 실Windows PC PowerShell5.1에서 unsigned native EXE `self-check --browsers` 실행 후 `PASS_SYNTHETIC_ONLY`, Chrome·Edge `PASS_SYNTHETIC_LOCAL_FILE`, `local_folder_verified=true` 사용자 전달. 코드/가중치/고객데이터 변경 없음.
3. **테스트:** 소유자 실PC 합성 self-check **PASS(사용자 제공 로그)**. 기존 native hosted SHA `96e2e1dff9976773bf3d3b2670ba6763ee69292d` [run #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029) 1/1, Python/browser [#43527161036](https://github.com/hibi89/data2web_studio/actions/runs/43527161036) 4/4. 실PC EXE SHA/OS10·11 정확 버전·고객 원본 검증은 **아직 없음**.
4. **현재:** 72/100 Verified·11 PENDING28점·85까지13점. `[작업중]`, RELEASE HOLD/SALE NO-GO/크몽 미등록.
5. **장애·대안:** GitHub hosted 검증과 사용자 제공 실PC 스모크는 출처 구분. 실PC SHA256/OS Caption·Build 미확인 → 사용자에게 2줄 PowerShell로 확인 요청. 원본 고객 데이터 업로드 금지.
6. **저장소/브랜치/기준:** `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113` 이전 검증 문서 HEAD `396c0206f7c8580e9d83f1d2ec396a57b5778cd6`. EXE 소스 `96e2e1df`; SHA256 정본 `87d0d28222a052cd5c8f4da48922376ec72a604283b8021a775199f4fa0f4718`. PR#4 Draft.
7. **환경·Production:** 소유자 PC Windows, PowerShell5.1, Chrome·Edge 로컬 파일 검사 PASS. Python 추가 설치 없이 Windows EXE. Production/Vercel 미적용.
8. **원본·백업·보안:** 고객 데이터 자동 수집0, 원본·점수표 수정0, 사용자 경로·계정명 GitHub 기록0; 최신 안전 소스는 이전 `396c0206`. 판매·실 고객 권리/서명 미승인.
9. **다음 순서:** OS+EXE SHA값 회신 확인→사용자 소유 합성 파일만으로 GUI 납품 추가 점검→라이선스/개인정보/운영 조건의 명시 승인→조건 만족 요구만 점수 인정, 85 미달시 HOLD 유지.
10. **검증 시점/범위:** 2026-11-14 KST 사용자 제공 실PC 터미널 출력 1건; **제삼자 attestation 및 정확 OS/EXE SHA 미검증**, 본 보고 문서 커밋은 별도 HEAD 확인. [세부 근거](docs/R23_R32_OWNER_WINDOWS_SELF_CHECK_20261114.md).

## 최신 인수인계 — 2026-11-14 KST · 네이티브 EXE 실구동 PASS / 85점 외부 수용 대기
1. **제품·기술·정본:** DATA2WEB Studio; CSV/JSON/TSV/XLSX → 로컬 GUI·HTML/ZIP, R01–R33 고정 배점 100점·목표85점.
2. **완료·근거:** source `96e2e1dff9976773bf3d3b2670ba6763ee69292d`에서 PyInstaller6.22.3 onedir native Windows `.exe` 신규 빌드, `native_windows_entry.py`, `native_windows_acceptance.py`, `.github/workflows/native-windows-owner-preview.yml` 추가. Python PATH 없는 native CLI/GUI·브라우저·synthetic deliver·verify·tamper/overwrite 거부 검증.
3. **테스트/성공/미검증:** [Native workflow #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029) 1/1 SUCCESS; [Full Python/browser #43527161036](https://github.com/hibi89/data2web_studio/actions/runs/43527161036) 4/4 SUCCESS(Windows291 PASS, Ubuntu290PASS+1SKIP); [blueprint gate #43527161439](https://github.com/hibi89/data2web_studio/actions/runs/43527161439) SUCCESS. 고객 Win10/11/사용권·Authenticode·상용 인수 **NOT VERIFIED**.
4. **상태:** 정본 전체검증 **72/100**, 목표85에 13점 부족. 11개28점 PENDING. `[작업중]`·RELEASE HOLD·SALE NO-GO·크몽 미등록, PR#4 Draft.
5. **장애/복구:** 첫 native workflow SHA `2ee49504`에서 합성 fixture newline 오기→EXE 빌드 PASS/실구동 감사 FAIL. 수정 SHA `96e2e1df`에서 재검증 PASS. 실고객·판매법률 검증으로 둔갑 금지.
6. **GitHub:** `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113`, 기준 소스 SHA `96e2e1dff9976773bf3d3b2670ba6763ee69292d`, [Draft PR#4](https://github.com/hibi89/data2web_studio/pull/4). 산출물은 Private Actions artifact ID `14085058847`(기한7일); 바이너리 저장소 커밋0.
7. **환경/Production:** Windows GitHub-hosted / Python3.11 build / PyInstaller 6.22.3; run `python native_windows_acceptance.py --exe native-dist/DATA2WEB-LOCAL/DATA2WEB-LOCAL.exe --manifest native-dist/PRIVATE_PREVIEW_MANIFEST.json`. EXE Python runtime 포함; Vercel/Production **미적용**.
8. **원본/백업:** 기능 전 안정 SHA `e676010fb5069ae8f337e4ae7f0c22a0fb1fac85`, 이후 통과 소스 `96e2e1df`; 요구/scorecard/고객 원본/기존 브랜치/데이터 변경0, 고객자료 GitHub·챗봇 전송0.
9. **다음 우선순위:** 물리 Win10/11 EXE·Chrome/Edge·한글/출력 실수용, 권리/NOTICE·원본 보유/파기, 가격·지원·환불·고객 인수·독립 보안감사 완료 뒤 R별 점수 산정. 현재 CI만으로 85 주장 금지; 사용자 최종 권리·상용 승인은 별도.
10. **갱신·범위:** 2026-11-14 KST 원격 GitHub 소스/Actions·artifact 확인, CI PASS는 소스 `96e2e1df` 정확 SHA. 새 문서 커밋은 새 정확 HEAD 확인 시 별도로 기록. 상세 [R32 Native](docs/R32_NATIVE_WINDOWS_OWNER_PREVIEW_20261114.md).
## 최신 인수인계 — 2026-11-14 KST · ZIP 보안 강화·정확 CI SHA
1. **제품/정본/기술:** DATA2WEB Studio, CSV/JSON/XLSX/TSV → 서버 없는 HTML/ZIP, R01–R33 고정 100점.
2. **변경:** `verify_delivery` 승인 상태 정확 대조·숨은 ZIP 구조 차단; `delivery` bounded HTML 스냅샷; `package_portable` bounded src/pyz; 악성 패키지 7개 회귀 추가. 선택 stdlib strict ZIP, 서명 방식은 인증서/배포권 부재로 보류.
3. **검증:** 정확 코드 SHA `0cb09f86280f860b008e008da6ccaea8be068e29`, [Actions #43524908011](https://github.com/hibi89/data2web_studio/actions/runs/43524908011) **4/4 SUCCESS** (Windows291 PASS, Ubuntu290 PASS/1SKIP, Win Chrome/Edge 및 Ubuntu Chromium E2E PASS), [gate #43524908506](https://github.com/hibi89/data2web_studio/actions/runs/43524908506) SUCCESS.
4. **상태:** 72/100 VERIFIED/85목표13미달, 11개28점 PENDING, `[작업중]`·RELEASE HOLD·SALE NO-GO.
5. **실패/회복:** 구현 SHA `914c0e1d`에서 ZIP raw magic byte 이스케이프 오류로 Python 테스트 실패; SHA `0cb09f86`에서 보정 후 합성/브라우저 CI PASS. Actions 계정 한도는 직전 턴에서 복구되어 이번 실행 정상.
6. **저장소/브랜치:** `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113`, PR#4 Draft 미병합, 소스 SHA `0cb09f86280f860b008e008da6ccaea8be068e29`. 수정경로 `verify_delivery.py`, `delivery.py`, `package_portable.py`, `test_archive_snapshots.py`.
7. **Production/실행:** 로컬 Python3.11+; `python -m unittest discover -v`, `python blueprint_score.py`, `python studio.py self-check --browsers`. Vercel/Production 미적용.
8. **원본/복구:** 정본 요구·점수표·main·원본 입력변경0. 직전 안정 SHA `3d5d2d657738ae27df8a527275a1e5381f36c52e`, 현재 성공 소스 `0cb09f86`, 고객 PII·키 업로드0, 무삭제/no-clobber.
9. **다음:** 실제 Win10/11·macOS 고객 인수, Excel 소유자 검수, 서명/권리/NOTICE, 상업 운영·법률 승인; 수용조건 충족 후에만 점수 재산정. 목표 미달시 `[작업중]` 유지.
10. **기준:** 2026-11-14 KST 정확 GitHub Actions SHA 기반, 마지막 문서 커밋은 이후 별도 확인. [실증/미검증](docs/R22_R29_R32_HARDENED_ZIP_ACCEPTANCE_20261114.md).

## 최신 인수인계 갱신 — 2026-11-14 KST · Actions 용량 복구 및 검증 4/4 SUCCESS
1. **용도/정본:** CSV·JSON·XLSX·TSV → 독립 오프라인 HTML/ZIP, R01–R33 전체 고정 100점.
2. **변경:** 기존 기능 SHA `b524cec21c670f4696fc469fe96ed96bfd3cf562`(로컬 합성 보고서 create-only/SHA, 영수증 비유한 JSON 거부, 신규 회귀), 검증 대상 제품 문서 HEAD `880586d7e63f38bd2c5e20f73f5bf46aa87d5d49`. 정본 점수표/기존 원본 변화 없음.
3. **테스트:** [Actions #43520777896 attempt2](https://github.com/hibi89/data2web_studio/actions/runs/43520777896) **4/4 SUCCESS**; Windows 284/284, Ubuntu 283 PASS/1 SKIP, Windows Chrome·Edge 및 Ubuntu Chromium E2E PASS. [final gate #43520778342 attempt2](https://github.com/hibi89/data2web_studio/actions/runs/43520778342) SUCCESS.
4. **현재:** 72/100점 VERIFIED, 목표85까지13, 11개 요구 28점 PENDING, `[작업중]` / RELEASE HOLD/SALE NO-GO.
5. **장애:** 한도 상태에 빠진 GitHub Actions가 step0에서 FAILURE; 사용자가 한도 해결 후 동일 failed jobs 재실행하여 원인 계층 분리/복구. 코드 테스트 실패와 구별, 재시도 금지 항목 없음(무한 자동 재실행은 금지).
6. **저장소:** `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113`; 검증 SHA `880586d7e63f38bd2c5e20f73f5bf46aa87d5d49`, PR#4 Draft. 해총 `hibi89/hackathon-command-center-2026@kmong-productization`에 결과 최신화.
7. **운영 환경:** Python3.11+, 로컬 전용, `python studio.py self-check --browsers --evidence-output ./new-evidence.json`; `python blueprint_score.py`. Production/Vercel 미적용.
8. **원본/복구:** 기존 CI 성공 `880586d7` 복구 지점. 원본·고객 파일/입력 데이터 변경0, 비밀/PII 자동 GitHub 업로드 금지, 정본 설계/고정 가중치 보존.
9. **다음:** 실 Windows10/11·고객 유사 실제 XLSX/브라우저/보안·LICENSE/NOTICE·자료권리·운영 조건 별도 수용 후 요구별 점수 재평가, 승인 전 판매금지.
10. **기준:** 2026-11-14 KST GitHub Actions 정확 SHA 재실행/원격 코드 검증, 실제 고객/법적 권리·판매 수용은 미검증. 이 문서 반영 커밋은 후속 검증 대상으로 구분.

## 최신 인수인계 보충 — 2026-11-14 KST · 코드 증거와 CI 장애
1. **제품 목적/설계:** 정본 R01~R33/고정 100점, 데이터 파일→로컬 HTML/ZIP, 고객 원본 서버 전송 금지.
2. **변경:** `b524cec2`까지 합성 디바이스 보고서 저장·create-only·SHA256, receipt JSON NaN/Infinity 거부, 회귀 4개 추가. 설계/가중치/원본 보존.
3. **검증:** 기준 `c2956397` 4/4 SUCCESS; 신규 `b524cec2` Actions #43520221605, gate #43520221969는 **시작 전 실패/steps 0/코드 테스트 NOT RUN**.
4. **상태:** 최종 72/100, 목표85 미달13, `[작업중]`/RELEASE HOLD/SALE NO-GO, 고객·라이선스 수용 미충족.
5. **오류/피벗:** 모든 Actions job 시작 즉시 실패, 로그 다운로드 404/annotation 본문 미접근. 무의미한 재시도 대신 Actions 계정·runner 실행상태 확인 및 로컬 소스시험 필요. 코드 문제로 단정하지 않음.
6. **GitHub:** `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113`, Draft PR #4 미병합, 이번 최신 기능 SHA `b524cec21c670f4696fc469fe96ed96bfd3cf562`.
7. **Production:** 오프라인 제품, Vercel/Production 미적용; `python -m unittest discover -v`, `python blueprint_score.py`, `python studio.py self-check --browsers --evidence-output ./new-device-evidence.json`.
8. **원본/복구:** 이전 성공 `c2956397` 복구 기준, 고객파일·원본·기존 브랜치/배점 불변, 기밀·PII/토큰 업로드 금지; 기존 파일 자동 삭제·덮어쓰기 금지.
9. **다음:** CI 시작 실패 원인 진단→코드 회귀(Windows/Ubuntu/브라우저)→실고객 기기·Excel/권리 승인 증거 취득→R별 점수 재평가; 상업 출시 승인은 별도.
10. **기준:** 2026-11-14 KST GitHub 원격 소스/CI 확인; 신규 코드 `b524cec2`, 신규 기능시험 아직 미실행, 이 문서의 최종 HEAD는 커밋 후 별도 검증. [상세](docs/R23_R32_LOCAL_EVIDENCE_AND_CI_BLOCKER_20261114.md).

> **최종 CI 정정(2026-11-14 KST):** 채점기 정확 코드 SHA `6ce083ef763257b9ccb03bd3d81caad9a4ce4f66`, [Actions #43515052630](https://github.com/hibi89/data2web_studio/actions/runs/43515052630) **4/4 SUCCESS**, Windows Python **280/280 PASS**, Ubuntu **279 PASS+1 Windows 전용 SKIP**, Windows Chrome·Edge/Ubuntu Chromium E2E PASS, final evidence gate #43515053057 SUCCESS. Windows cmd cp1252 JSON `UnicodeEncodeError`를 ASCII-safe JSON 출력으로 수정한 failed CI #43514788415 기록 보존. **정본100점/검증72점/85 목표차13점**, 고객·법적·상업 승인 HOLD.

1. **목표·정본·용도·기술:** R01–R33 + `docs/FINAL_DESIGN.md` 전체100점을 분모로 하는 로컬 CSV/JSON/XLSX/TSV → HTML/차트·검색·ZIP·영수증. Python3.11+ stdlib·Tk, API/원격 고객 업로드·유료 런타임0. 사용자 목표 **전체 최종설계 ≥85/100**.
2. **완료 기능·결정 근거:** 소유자가 점수척도(5/20/100) 선택/진행을 위임, 100점/B안 고정 (33요구별 배점2~5, 구간18/20/26/20/16). 5점은 세분화 부족, 20점은 소수 배점 요구, 100점은 정수 고정/감사 용이. `data/final_blueprint_scorecard_v1.json`, `blueprint_score.py`, `test_blueprint_score.py`로 각 항목 검증·미완료 분리. 사용자가 위임한 3번 상품·데이터·환불 운영안은 비공개 [초안](docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md) 보존, 상품 게시 승인은 아님. 기존 R06/R22/R29 보안·R32 Windows unsigned zipapp·R16 인쇄·REA Lite golden 유지.
3. **테스트 명령·PASS/FAIL/미검증:** 기능 검증 `23a2d1293755294a58a20b98dc34e229a1e54f82` [Actions #43509224663](https://github.com/hibi89/data2web_studio/actions/runs/43509224663) 4/4 SUCCESS, Windows269/269, Ubuntu268 PASS/1 Windows CMD SKIP. 신규 채점기·10가지 회귀 commit `380055beea7c92ad8dd58dd76b953654498eab08`, `python -m unittest discover -v` hosted Win **279/279 PASS**, Ubuntu **278 PASS+1SKIP**, 코드 실행 `python blueprint_score.py` 예상 72/100. 신규 코드 CI [#43513559502](https://github.com/hibi89/data2web_studio/actions/runs/43513559502) Win279/279·Ubuntu278+1SKIP PASS, Windows Edge native 1회 HOLD로 전체 FAILED; **후속 정확 HEAD #43514132305 4/4 SUCCESS** 및 blueprint gate #43514132935 SUCCESS. 해당 transient 실패/성공 이력 구분. 고객 물리 Win10/11·실 Excel/상업 라이선스·판매 계약 독립 검증 아님.
4. **완료·진행·대기·차단:** 전체 정본 100점 가중치 확정, 현재 **검증 인정 72/100 (22요구), 미검증28점(11요구), 목표85까지13점**. 외부 실고객·권리·보존/환불 등 남음. **[작업중], RELEASE HOLD/SALE NO-GO** 유지, 마커 제거/상품등록완료/PR 자동병합 금지.
5. **실패·원인·시도·대안:** 100점 채점 명령을 CI에서 추가 실행한 #43514788415의 Windows 테스트 job에서 cp1252 콘솔이 한글 `[작업중]`을 출력하지 못해 `UnicodeEncodeError` 발생(단위 279/279 PASS와 별개). CLI JSON을 `ensure_ascii=True`로 바꾸고 Windows cp1252 출력·JSON 재파싱 회귀를 추가, 수정 커밋 CI 판정 대기.  이전에는 배점 소유자 미승인으로 UNASSESSED. 5/20 척도는 33요구별 정수 배점/리스크 구분이 어려워 100점으로 승인 위임 범위 내 전환. 점수는 전체33개 중 검증된 요구의 고정 가중치 합일 뿐 테스트 성공 횟수 비례 아님. 85를 맞추려고 배점 사후 수정 금지. 과거 R16 pypdf 추출·출력 HTML 안전 읽기 버그 수정 기록 STATUS 보존. 실제 고객 기기/법률·상업승인 누락을 CI PASS로 덮지 않음.
6. **GitHub 저장소·브랜치/SHA/경로:** `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113`; 마지막 실제 기능 코드 `23a2d1293755294a58a20b98dc34e229a1e54f82`, 가중치 평가기 코드 `380055beea7c92ad8dd58dd76b953654498eab08`. `docs/FINAL_BLUEPRINT_WEIGHTING_100_APPROVED_20261114.md`, `data/final_blueprint_scorecard_v1.json`, `blueprint_score.py`, `test_blueprint_score.py`, 요구별 감사표·STATUS/HANDOFF. 중앙 해총 `hibi89/hackathon-command-center-2026@kmong-productization` 별도 SHA.
7. **Production·환경·실행명령:** Vercel/Production URL **미적용**(서버 없는 로컬 제품). `python blueprint_score.py` 최종설계 R별 합계·미달 확인. `python studio.py self-check --browsers` 합성 고객 PC 자가검증, `python studio.py desktop` Python/Tk, `python package_windows_bundle.py create ./new-bundle`. 실고객 Win10/11·Excel·서명 EXE 및 유료 설치 지원 미검증.
8. **원본·백업/인증·변경금지:** Git 기존 SHA·원본 main/P50/P70/P85/REA_Web 불변; customer data/비밀/.env/토큰 GitHub 업로드0; 기존 고객 폴더 무덮어쓰기·무자동삭제. 가중치 원본 제안 이력 `docs/OWNER_85_COMPLETION_DECISION_20261114.md` 보존. 점수 고정은 판매/상업 라이선스·고객 원본권리 승인으로 간주하지 않음.
9. **다음 작업 우선순위·완료기준:** 85까지 추가13점의 요구별 **실수용** 확보. AI는 독립 무료 코드·CI/라이선스 인벤토리·도움말/보안/고객 셀프체크와 정확 SHA를 계속 관리. 사용자/실고객만 제공 가능한 Win10/11·실Excel/자료 권리·상업 LICENSE/NOTICE·보유/환불/거래 조건/고객 인수는 별도 증거 및 승인 필요. 점수 인상은 정확한 R별 합격 근거 후에만 기록.
10. **KST 갱신시각·검증범위·문서 기준 SHA:** 2026-11-14 KST; 마지막 269/268+1 기능 CI 성공, 새 채점기 Windows279/279·Ubuntu278+1SKIP 단위 PASS, 실제 최종 문서 HEAD Actions #43514132305 4/4 SUCCESS 및 blueprint gate #43514132935 SUCCESS 확인. 이후 score CLI CI 직접 실행은 다음 HEAD에서 재검증. 문서 HEAD는 실제 커밋·검증 후 기록, 중앙 원장 동기화 여부 별도 확인.

**현행 평가:** 사용자 위임 100점 B안 확정, 검증 근거 72점, 85 미달13점. 출시 HOLD 유지.
