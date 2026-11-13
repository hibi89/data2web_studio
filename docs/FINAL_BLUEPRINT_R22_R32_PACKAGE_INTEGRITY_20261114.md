# DATA2WEB Studio — R06/R22/R29/R32 검증·인수인계 (2026-11-14 KST)

**공식 전체 최종완성률: UNASSESSED / 사용자 목표 85% 미인증.** 분모는 REQUIREMENTS.md의 R01–R33 전체와 docs/FINAL_DESIGN.md이다. 소유자의 요구별 가중치 합100, 실제 구매자·상업 권리·지원 조건은 아직 승인되지 않았다.

## 확인된 변경과 범위
- 정확 기능 SHA: 23a2d1293755294a58a20b98dc34e229a1e54f82. [Actions #43509224663](https://github.com/hibi89/data2web_studio/actions/runs/43509224663) **4/4 SUCCESS**. Windows Python3.11 269 PASS/0 FAIL/0 SKIP, Ubuntu Python3.11 268 PASS/0 FAIL/1 Windows 전용 CMD SKIP. 실제 Windows Chrome·Edge 및 Linux Chromium 브라우저 기존 file:// E2E와 원본 REA Lite pinned golden 등 회귀 PASS.
- R06/R22/R29: verify_delivery.py는 동일 ZIP 원본을 여러 번 다시 열던 방식 대신 24MB 이내 단일 bounded FD snapshot을 대상으로 ZIP CRC/허용 멤버/HTML/manifest/원본 SHA를 검증·해시한다. 승인 manifest는 64KB, 고객 HTML 20MB와 receipt 256KB로 bounded file-handle 읽기. verify_customer_folder.py는 독립 ZIP 검증에서 얻은 SHA와 고객폴더가 후속으로 읽은 ZIP snapshot SHA가 다르면 HOLD. 승인 manifest와 ZIP 내 JSON의 중복 key·NaN/Infinity도 거절.
- test_archive_snapshots.py: 실제 CRC를 다시 만든 조작 ZIP의 중복 JSON/NaN, 내장 데이터 조작, ZIP 교체·추가파일, 원본 승인 JSON 제한읽기/링크 차단 등 **8개 신규 회귀**. 파일 교체 경합 일부를 방어하지만 공격자 소유 전체 디렉터리의 모든 운영체제 경쟁조건, 권리·전자서명/외부 보안감사를 완료했다고 주장하지 않는다.
- R32: package_windows_bundle.py는 새 경로에 DATA2WEB.pyz, RUN_DESKTOP.cmd, RUN_SELFCHECK.cmd, VERIFY_CUSTOMER.cmd, README_LOCAL_KO.txt, BUNDLE_MANIFEST.json을 생성·내부 SHA 무결성 검증한다. 동일 실행환경에 대해 결정적 바이너리·기존 파일 무덮어쓰기·변조/추가파일/링크 거부. test_windows_bundle.py **12개 신규 회귀** 중 Windows hosted에서 실제 cmd.exe로 RUN_SELFCHECK.cmd를 실행한 Chrome·Edge synthetic file:// 결과가 모두 PASS, Ubuntu에서는 해당 실행 1개만 SKIP.
- 신설 실행 파일은 **서명된 Windows EXE가 아니며**, 고객 PC에서 Python3.11+가 필요하고 GUI에는 Tcl/Tk가 필요하다. 번들에는 고객파일·비밀·고객 개인정보·유료 API/원격 업로드 없음. 사용권·LICENSE/NOTICE·판매 승인·물리 Windows10/11 인수는 여전히 HOLD.

## 설계 2안 비교 및 선택
| 항목 | A안 | B안(채택) |
|---|---|---|
| ZIP 검사 | 경로 반복 open 후 해시; 빠른 구현이나 파일 교체 경쟁조건 | 단일 bounded file-handle snapshot 검사·해시; 추가 최대24MB 메모리, 기존 보안 경계 강화 |
| Windows 실행 | 서명 EXE/설치파일; 인증서·새 배포/라이선스 승인 필요 | Python3.11 zipapp + CMD 3종, 비용0·기존 패키징 재사용. 고객 Python 설치 필요 |
| 권리·출시 | 사용자 승인 없이 진행 불가 | **RELEASE HOLD**, 서명·상용권·실장비 인수 미검증 유지 |

## 재현
- Python3.11+: python -m unittest discover -v
- 새 실행 폴더 생성: python package_windows_bundle.py create ./new-windows-local-bundle
- 폴더 검증: python package_windows_bundle.py verify ./new-windows-local-bundle
- Windows 고객 로컬에서 합성 데이터 검증: new-windows-local-bundle/RUN_SELFCHECK.cmd
- 실제 고객 원본 파일은 자동으로 읽지 않으며, 합성 자가검증 결과는 구매자 데이터 사용권이나 실 Windows10/11 수용을 보증하지 않는다.

## 정본 최종상태
R01–R33 중 합성/호스팅 기술근거 22개, 일부 미완/외부 수용 11개라는 보수적 분류는 **변경하지 않는다**. R29 외부 보안감사와 R32 고객 실기기·서명 EXE/지원정책은 아직 미검증이기 때문이다. 미승인 참고 가중치 A안 22/33(66.7%), B안 72/100(85 대비 추가13)은 공식 최종완성률이 아니다. 요구별 승인 가중치 합100·실고객 Windows10/11/Excel/권리·보존/파기·SKU/환불/지원 승인 전 공식 85%를 주장하지 않는다.

**[작업중], RELEASE HOLD/SALE NO-GO** 유지. 제품 main·원본 REA_Web·기존 P50/P70/P85·실고객 데이터/비밀 수정0, Draft PR 미병합, Vercel 미적용. 변경 브랜치는 Git parent SHA로 복구 가능.
