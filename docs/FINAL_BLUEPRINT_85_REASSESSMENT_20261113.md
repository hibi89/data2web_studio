# DATA2WEB 최종설계 85% 요구 — 재검증/남은 조건 · 2026-11-13 KST

**공식 최종완성률: UNASSESSED. 85% 달성 미인증.** 정본 R01–R33 전체의 소유자 승인 가중치(합100)가 없고 실고객 Win10/11·실무 Excel 파일·권리/지원/환불·현장 인수 증빙이 없어 기술 테스트 통과만으로 수치를 확정할 수 없다. 사용자가 요청한 85%는 기술 P85 단계가 아니라 최종설계 전체 대비 85%라는 구분을 유지한다.

## 이번 추가 개발·실행 결과
- 검증 정확 소스 `d311c47f1b85382f1d4ce43dfacdabcdc7e85612`, [Actions #43392272159](https://github.com/hibi89/data2web_studio/actions/runs/43392272159) **4/4 SUCCESS**: Windows hosted Server2025 Python3.11 **210/210 PASS**, Ubuntu24.04 Python3.11 **210/210 PASS**; Linux Chromium 및 호스팅 Windows 실제 Chrome/Edge `file://` 신규 단일파일/기존 다중파일 HTML·ZIP·영수증, 검색·복수 분류·차트·권리동의·재저장·무원격 호출 **PASS**.
- **R02:** JSON **평면 단일 객체 1행** 또는 기존 **평면 객체 배열** 승인 입력. 중복 key·NaN/Infinity·중첩 스키마는 HOLD. 루트 `{"rows":[...]}`를 자동 추측해 펼치지 않는다.
- **R24/R32:** `studio.py deliver` 단일 고객원본의 SHA/시트·매핑/권리·평문/개인정보 명시 승인 후 **새 폴더**에 HTML·ZIP·JSON 영수증 create-only 납품. 실패/중복은 새폴더 생성 전 HOLD, 기존 폴더/고객 데이터 삭제하지 않음. `package_portable.py` 결과 `.pyz`에서 동일 명령 실제 검증(단, Python3.11+ 설치 요구, 고객 지원/서명 EXE 아님).
- **R31:** `hibi89/REA_Web` **공개 원본 브랜치** 정확 커밋 `7b6b68111efd906f9d929b5e2f577699b26399ee`를 CI 임시 폴더에 **읽기 전용 checkout**하고 `python -m rea.lite_builder` 원본 실제 CLI를 실행. `upstream_runtime_golden.py`가 새 DATA2WEB 생성물과 실제 CSV/JSON 정규 컬럼 매핑·전체 행/값·SHA·승인 상태, 3테마 일부, Playwright `file://` 검색/분류, 동일 헤더 CSV 교체/HTML 내보내기/재열기, 중복 ID·잘못된 매핑·옛 SHA 거부를 대조하여 **PASS**. 원본 리포지토리 수정0/소스 파일을 신규 Git 저장소에 복사0. **서로 다른 UI 디자인·페이지 크기/신규 XLSX·TSV·다중 파일은 1:1 픽셀/동작 동일성 범위 밖**이므로 완전 동등/판매 인수 주장 금지.
- **최종 설계 검증 자료:** `REQUIREMENTS.md`의 R01–R33 전수 추적 `docs/FINAL_BLUEPRINT_R01_R33_ACCEPTANCE_20261113.md`와 사용자 소유권 보류 `docs/OWNER_DATA_AND_DELIVERY_HOLD_CHECKLIST.md`. 초기/현행 기술 기능 SHA와 doc SHA 구분.

## 아직 사용자 외부 자원/승인 때문에 미확정인 것
1. 소유자가 **R01–R33 항목별 가중치 합100**를 확정해야 공인 `최종설계 85%` 계산 가능. 가중치를 임의 균등분할/상상해서 85%로 선언 금지.
2. R23/R30 실제 구매자 **Windows10/11 Chrome·Edge** PC 및 고객 Excel 실문서 파일을 사용한 독립 수락은 GitHub Windows Server2025 호스팅 CI와 별개다. macOS 실제 장비도 미검증.
3. R07/R21/R25/R26/R27/R33 개인정보·제3자 저작권/로컬 데이터 보유/상업 배포 LICENSE·NOTICE·가격/SKU별 수정/지원/환불·실고객 인수는 소유자 명시 결정 전 HOLD. 프로그램은 사용자 허가를 대신할 수 없다.
4. R06·R29 파일 시스템 동시교체 경합(TOCTOU)·외부 보안 점검과 XLSX 고급 서식/실 Excel 호환성 등은 별도 운영검증. `README.md`의 테스트 결과를 실제 고객 권리 증명으로 오용 금지.

## 상태 및 다음 작업 기준
- **[작업중] 유지, RELEASE HOLD/SALE NO-GO.** 오프라인 납품형이라 Vercel/Production **미적용**.
- 승인 가중치/실 고객 환경 자료를 확보하기 전에는 최종 85% 완료 및 크몽 상품 `등록완료` 표기 금지. 원본 Lite 전용 검증이 새 제품의 모든 기능/권리를 입증하지 않는다.
- 신규 코드와 검증된 기술 기능을 보존하고 작업 브랜치/정확 SHA·CI·결과를 해총 `kmong-productization` 원장에 같은 작업 단위로 기록.

