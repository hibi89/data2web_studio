# DATA2WEB Studio — R22/R29/R32 오프라인 ZIP 패키징 강제검증

**기준일:** 2026-11-14 KST. **기능·테스트 정확 SHA:** `0cb09f86280f860b008e008da6ccaea8be068e29`. 브랜치 `feature/final-blueprint-p85-evidence-20261113`, Draft PR #4, `main` 미변경.

## 목표와 구현 두 방식 비교
- **A (선택):** 현재 Python 표준 라이브러리 ZIP_STORED/manifest 계약을 유지하며 입력 크기를 사전에 제한하고, ZIP 컨테이너 구조·승인 상태를 fail closed 검증. 유료 API·신규 설치·외부 업로드0. 기존 수용테스트와 호환; 버전·검증기로 통제.
- **B (보류):** CMS/Authenticode/PKI 서명 체계와 EXE 빌드 추가. 작성자·사업자 명의/코드서명 인증서/Windows 실제 기기·라이선스 승인이 필요하고 유료 비용·운영 부담 증가. 서명 미구현을 승인된 배포로 취급 금지.

## 수정과 공격 재현
1. `verify_delivery.verify_zip`: `status`를 반드시 `RELEASE_HOLD`로 확인, 승인되지 않은 키(예: `vendor_signature_valid`)와 비정상 rows bool 거부. Manifest contract의 필수 키를 정확하게 고정.
2. 동일 ZIP bounded FD 스냅샷에서 로컬 ZIP 헤더·EOCD 종단 시그니처·댓글 길이·멤버 offset·extra/comment·flag 및 중앙 디렉터리 경계를 검사. 숨겨진 앞/뒤 데이터나 판매허가를 가장한 ZIP 주석 거부. 이 검증은 **발행자 서명이나 변조 불가능한 암호학적 출처 증명은 아님**.
3. `delivery.package_html`: HTML을 `read_bounded_source(..., max_bytes=20_000_000)`로 한정해 전체 파일을 먼저 읽는 메모리 과소평가/경합 위험을 줄이고 SHA 대조 유지. 기존 고객 파일 및 ZIP을 자동 삭제하지 않음.
4. `package_portable.create_portable`: 패키징 입력 Python 모듈과 생성된 .pyz를 정해진 상한/동일성 확인으로 다시 읽음.
5. `test_archive_snapshots`: forged ZIP 상태, 임의 서명 플래그, bool 행수, ZIP 댓글, 앞/뒤 데이터, 재패키징 bounded read, 초과크기 HTML 무생성 **7개 회귀**.

## 실제 검증 범위/회귀
- SHA `0cb09f86280f860b008e008da6ccaea8be068e29`, [Windows/Ubuntu/브라우저 Actions #43524908011](https://github.com/hibi89/data2web_studio/actions/runs/43524908011) **4/4 SUCCESS**. Windows Python3.11 **291/291 PASS**; Ubuntu Python3.11 **290 PASS/1 Windows-only SKIP**; Windows 설치 Chrome/Edge 및 Ubuntu Chromium 실제 `file://` E2E PASS.
- [최종설계 게이트 #43524908506](https://github.com/hibi89/data2web_studio/actions/runs/43524908506) **SUCCESS** (코드 SHA 동일).
- 첫 구현 SHA `914c0e1dfea3c7d3e6e105eb0182e5ff498e2659`의 binary signature 문자열 이스케이프 오류는 시험 실행에서 **FAIL** 재현, 이후 `0cb09f86`에서 실제 ZIP 시그니처 바이트로 수정·완전 회귀 PASS. 실패 기록 보존.
- 이 CI는 합성 입력과 hosted Windows/Ubuntu에 한정. **실 고객 원본, 물리 Win10/11, 맥OS, 고객 인수/라이선스 권한/외부 침투 테스트는 미실시**.

## 최종설계 점수 잠금
R01~R33 전체 100점 고정, **22개 Verified = 72점**, 11개 Pending = 28점, 목표 **85까지 13점** 부족. 이번 코드는 R06/R21/R22/R29/R32 중 원래 이미 검증된 R22의 결함 위험을 더 줄이고 나머지의 기술적 준비를 강화함. 단, R06(실 Windows OS 경쟁), R21(LICENSE/NOTICE 상업 승인), R29(독립 보안·고급 공격 감사), R32(실장비·서명/권리/고객 수용) 각각 기존 수용조건이 남아 있어 **추가 점수 0점**.
**[작업중]** 유지, **RELEASE HOLD/SALE NO-GO**, 크몽 미등록. 사용자/고객 자료·원본 손대지 않음; Production/Vercel 미적용.

## 다음 작업·실제 수용
고객과 제품 소유자의 명시적 권리·자료수용/운영 정책 승인 및 실제 Win10/11+Excel+Chrome/Edge 사용자 QA, 제3자 LICENSE/NOTICE 확인. 실행증거가 충족된 R항목만 **원래 고정 점수**에 따라 재산정하고 85 미달 시 목표 완료 주장 금지.
