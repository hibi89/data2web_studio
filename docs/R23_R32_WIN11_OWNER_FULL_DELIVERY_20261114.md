# DATA2WEB Studio — 소유자 Windows11 합성 CSV 실제 납품 폴더 검증

**증거 일시:** 2026-11-14 KST. **출처:** 소유자가 대화에서 직접 전달한 Windows PowerShell 5.1 콘솔 출력 + 직전 소유자 PC GUI 스크린샷, 별도 원격 실행·외부 고객감사 아님.

## 실제 OS·바이너리(이전 확인 사실)
- Windows 11 Pro, Build 26200 (Win32 Version 10.0.26200).
- GitHub hosted-native [Actions #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029) 원본 `DATA2WEB-LOCAL.exe` SHA256 = `87d0d28222a052cd5c8f4da48922376ec72a604283b8021a775199f4fa0f4718` = 소유자 PC PowerShell SHA256 대소문자 무시 완전 일치.
- 선행 소유자 `self-check --browsers`: Chrome/Edge `PASS_SYNTHETIC_LOCAL_FILE`, 전체 `PASS_SYNTHETIC_ONLY`. 원본 고객 데이터나 서버 송신 없음.
- 소유자가 생성한 합성 CSV `id,title,category` 2행·3열 / `SHA256=641fcfb8e6e4a522993e0894d2e0fac3d0d4784a19911e4a3f9e42ec25e15fd1`는 GUI 시각증거, 실제 원본 bytes는 모델·GitHub에 수집하지 않음.

## 새로운 사용자 제공 현장 납품·독립 검증 출력
- 사용자는 실제 Win11 GUI에서 합성 데이터 파일 선택/검수·열 매핑, 권리·평문 체크(소유자 직접 생성한 합성 입력에만 한정), 개인정보 없음 분류, 새로운 출력 폴더 지정 및 생성으로 진행한 뒤, 동일 exe의 `verify-customer` 명령 결과를 전달.
- `contract = DATA2WEB_CUSTOMER_FOLDER_V1`
- `status = LOCAL_INTEGRITY_VERIFIED_RELEASE_HOLD_NOT_SALE_APPROVED`
- `verified = true`
- `rows = 2`
- `html_sha256 = 8ebe90998f5155b2ca73c8a8db2782c3fe8999e33e873f45cc48eee1d49c32a2`
- `zip_sha256 = 5c16d93a56e432718cce5ebbf8d84564eb93c1dd176d6dd25604772e8b47677f`
- `receipt_sha256 = 970994186449b9ad5dd521f02cc49b0ed01ebe5d6bdbf664f5f89ee117474a3a`
- `sale_approved = false`
- **판정:** 소유자 실제 Win11에서 합성 표 CSV→새 폴더의 HTML+ZIP+receipt를 생성해 독립 verifier로 무결성 확인하는 최종 흐름 **사용자 제공 현장 PASS**. 해당 출력의 근거는 소유자 콘솔 제출이며 모델이 원격 직접 읽기/재해시한 것은 아님. 한 번에 생성 완료되었다는 것은 사용자의 구두 보고와 verified 결과에서 합리적으로 확인되며 자동 앱 동작 전 단계와 혼동 금지.
- **남은 확인:** HTML을 Chrome/Edge에서 실제 열어 테이블·검색·차트의 현장 시각 동작 점검은 이번 출력에 포함되지 않음(기존 GitHub hosted E2E는 별도로 PASS). Windows10/macOS/독립 고객·법적 자료 사용권/배포 권리·코드 서명/고객지원/실 구매/환불은 여전히 미검증.

## 특이 로그: GUI 중단 예외와 납품 검증 분리
- 같은 콘솔의 앞선 `DATA2WEB-LOCAL.exe desktop` 스택트레이스 마지막에 `tkinter.mainloop -> KeyboardInterrupt` 및 PyInstaller `Failed to execute script ... due to unhandled exception` 관찰.
- `KeyboardInterrupt`는 인터럽트 신호(예: Ctrl+C)로 흔히 발생. 정확히 어떤 사용자 조작으로 발생했는지는 미확인하며 **프로그램 GUI의 일반 종료 문제인지 단정 금지**. 이후 독립 `verify-customer` 정상 종료 및 `verified: true`와는 별도 사건이다.
- 별도 UX 개선 후보: CLI desktop 모드의 수동 인터럽트에 대한 명시적 종료 처리(정상 Windows 창 닫기와 별개) 및 hosted regression. 사용자가 다운로드한 EXE 파일을 임의 교체하지 않고, 코드 수정 시 새 SHA·Windows 실검증 재시행 필요.

## 최종설계 점수 판정
- 승인된 고정 배점 R01~R33: **72/100** (22 verified 요구), **11 pending=28점**, 목표85까지 **13점**.
- 이번 실PC 납품 성공은 R23, R24(이미 검증), R32의 환경·현장 수용 증거를 실질 강화한다. 그러나 R23의 Win10/macOS·독립 고객 수용, R32의 서명/상업 라이선스·고객 수용 등이 남아 있어 **완전 충족된 새로운 R항목이 없음 → 신규 가중점수 0**. R24는 이중 계산 금지.
- `[작업중]` / RELEASE HOLD / SALE NO-GO / Draft PR#4. 개인 계정명·PC 원본 경로·실제로 생성된 고객 파일 내용을 GitHub에 기록하거나 업로드하지 않음. Vercel/Production 미적용.
