# DATA2WEB Studio — R15/R21/R22/R24/R32 오프라인 고객 UI·납품 검증 강화 · 2026-11-13 KST

**본 작업은 사용자의 '최종설계 전체 85%' 목표에 대한 실개발 진전이다. 단독 GUI/CI 성공이 공식 최종완성률 85%를 뜻하지 않는다.** 공식 100% 분모: `REQUIREMENTS.md` R01–R33 전부와 `docs/FINAL_DESIGN.md`; 사용자 소유 R별 가중치 합100 부재 → **UNASSESSED / 85% 공식 인증 보류**. 설계·SKU 범위 축소나 임의 R 가중치 생성 없음.

## 구현 전 2안 비교와 채택
| 안 | 실제 고객 사용 경로 | 성능·비용 | 유지·보안 | 결정 |
|---|---|---|---|---|
| A. Python 기본 Tkinter PC 검수 GUI → 기존 CLI 코어 호출 | 파일/시트·열 선택, SHA, 명시적 동의, 새 폴더 | 런타임 서버/API 0; Python3.11+와 OS Tk 필요 | 기존 Python 파서 재사용·새 네트워크 surface 없음 | **채택** |
| B. localhost 전용 HTTP 웹마법사 | 브라우저 화면 제공 | 추가 서버/포트·권한·방화벽 운영 필요 | CSRF/접근통제·주소 노출 경계 추가 | 보류 |

납품 무결성도 ZIP만 개별 확인(A)하던 기존 방식과 전체 폴더의 **HTML·ZIP·영수증 상호검증(B)**을 비교했다. 후자를 추가해 별도 파일 바꿔치기·receipt 수정 위험을 줄였다. 온라인 송신/인증/호스팅·유료 패키지는 추가하지 않았다.

## 새 기능 및 실제 QA 근거
- `data2web_desktop.py`: Tkinter 데스크톱 승인 화면. 로컬 소스 CSV/JSON/XLSX/TSV 선택, XLSX **사용자 직접 시트 선택**/헤더 위치·캐시 수식 승인, 원문 셀 제외 컬럼/공백/중복 요약, 3열 명시 매핑, 3테마, 파일 SHA 검수, 권리/평문 2개 체크박스 및 개인정보 수동 분류 후 새 고객 폴더 생성. 기존 DATA2WEB 코어 `deliver_single` 호출. 임의 원본/기존 파일 자동 삭제·덮어쓰기 없음.
- `studio.py desktop` / `python data2web_desktop.py`; Python3.11+ 및 Tcl/Tk가 설치돼야 함. `package_portable.py`의 결정적 zipapp에도 GUI 모듈 포함; GUI를 열지 않는 CLI/테스트에서 Tk 윈도우를 생성하지 않음.
- `verify_customer_folder.py`: 독립 검증기. 완전한 고객 새 폴더에 `index.html`, `delivery.zip`, `receipt.json` 3개만 허용, symlink/junction·외부/누락 파일 거부, ZIP 독립 SHA/CRC/manifest 결과와 로컬 HTML 바이트 완전 일치, receipt의 원본 SHA·출력 SHA·시트·헤더·수식 캐시·매핑·행수/컬럼·원본별 승인 기록 교차검사. 새 파일을 읽을 뿐 자동 삭제·수정 없음. 이는 상업적 저작권/배포자 신원 인증 서명이 아니다.
- `studio.py verify-customer <새 고객 폴더>`는 실행 결과를 로컬 JSON으로 확인하고, 실패 시 source 값/개인정보 셀을 로그에 출력하지 않는 `HOLD` 처리. `python tool.pyz verify-customer ...`에서도 실행.
- `test_desktop_controller.py` 등 단위/경계 테스트: 파일 SHA 변경 후 폴더 사전 차단, XLSX 숨김/명시 시트, 체크박스 false, 개인정보 자동승인 거부, 중복 호출 무덮어쓰기, Python `.pyz` 포함 확인.
- `test_customer_folder.py`: 고객 receipt 내 SHA·매핑·권리 상태 변조, ZIP 교환, 외부/숨김 파일 추가, receipt 누락, JSON 중복 키·링크 경로 거부, 단일/다중 소스 정상 검증.
- `desktop_ui_smoke.py`: **GitHub hosted Windows Server2025 실제 Tkinter UI 컨트롤 41개 렌더링 PASS**. 이는 GUI 컴포넌트 생성·기본 크기 테스트이고 **실제 구매자 Win10/11 조작·키보드 접근성·일반 고객용 설치/고급 UX 검증이 아님**.
- `browser_single_delivery_probe.py`: 파일 생성 후 ZIP뿐 아니라 **고객 새 폴더 전체 검증** 수행, Chrome/Edge/Chromium 실제 `file://` 사용 경로 보존.
- 기능 정확 코드 SHA `74f5f5a6b4625be3d510be5f59f1983be150b26e` [Actions #43395679294](https://github.com/hibi89/data2web_studio/actions/runs/43395679294), 앞선 화면 및 테스트 완주 검증 `f82e6396d1ac2aa0bfae3e850685082e6cd8bfdd` [Actions #43395400646](https://github.com/hibi89/data2web_studio/actions/runs/43395400646). Windows/Ubuntu Python3.11 각 **235/235 PASS**, Ubuntu Chromium·Windows 설치 Chrome/Edge 실제 `file://` 합성 소스 E2E, 원본 REA_Web Lite pinned SHA 실코드 golden, 호스팅 Win Tk 41 widgets PASS. 정확 HEAD 문서 커밋 CI는 이후 별도 재조회.

## R01–R33 전체 정본에서 확인 가능한 위치
- **R08, R09, R10:** 로컬 사전검수·SHA/시트 고정과 3열 명시 매핑을 GUI에서도 재현(실 고객 승인 미실시).
- **R15, R16:** 로컬 HTML 검색/복수 분류/정렬/상세/차트/브라우저·인쇄는 기존 synthetic E2E PASS, **GUI 화면 추가는 선택 기능**(반응형 웹과 별도).
- **R19, R20:** 고객이 권리·평문 고지 확인을 체크하지 않으면 새 납품 폴더 생성 전 HOLD. 네트워크/API 호출 코드 없음, E2E 외부 요청 0.
- **R21, R22, R24:** ZIP manifest 자체 + **고객 폴더 receipt**까지 독립 대조. 권리/NOTICE 실 승인 전 판매/내부 로컬 생성과 구분, 폴더 전체 검증 실패 시 출고 HOLD.
- **R26:** 분류 값은 소유자 자기진술, 개인·민감정보 자동 적합성이나 법무 확인을 보증하지 않음.
- **R29, R30:** Link/경로·tamper 경계 테스트 Win/Ubuntu PASS; hosted Windows Server2025 GUI 렌더 PASS ≠ 실제 고객 Win10/11.
- **R31:** 기존 REA lite 원본 public pin `7b6b68111efd906f9d929b5e2f577699b26399ee` 실제 CLI와 Chromium file:// CSV/JSON/테마/로컬 저장 동등성 PASS, 모든 픽셀·확장 기능의 동일성은 주장 금지.
- **R32:** ZIPAPP reproducible/offline CLI + GUI 모듈 PASS. **고객 Python/Tk 설치·독립 Win10/11 GUI 조작 인수/서명 EXE는 미검증**.
- **R23/R25/R27/R33:** 실제 사용자 Win10/11/macOS/고객 Excel, 현장 보유·폐기 정책, SKU·지원·환불·실데이터 사용권/상업 라이선스·NOTICE·샘플 인수 **승인 대기**.

**공식 결론:** 모든 33개 요구의 승인 가중치와 고객/법적/실환경 증거가 아직 확정되지 않아 **UNASSESSED, 85% 인증 보류**. `[작업중]`, `RELEASE HOLD/SALE NO-GO`; Vercel/Production 미적용. 타 제품/고객 자료/REA_Web 원본과 이전 검증 브랜치는 불변.
