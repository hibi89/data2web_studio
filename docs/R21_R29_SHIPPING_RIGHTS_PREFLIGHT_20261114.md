# R21/R29 준비 — 실제 A 납품 구성/권리 사전검증 (2026-11-14 KST)

## 설계 비교
| 방법 | 성능·비용 | 유지보수·위험 | 판정 |
|---|---|---|---|
| A. 상태 문서에만 ZIP 자산·저작권 체크리스트 기재 | 추가 실행비0, 소스 변경에도 자동 검증 없음 | ZIP 변경·LICENSE 누락/허위승인을 CI가 놓칠 수 있음 | 배제 |
| B. 사전 승인되지 않은 자산을 **HOLD**로 취급하고, 합성 납품을 실제로 생성→독립 검증→JSON 조사표와 대조 | stdlib·서버/API0, 동일 CI에서 반복 검증 | 사양 변경 시 검증 스키마/허용멤버를 같이 갱신해야 함 | **채택** |

## 구현·검증 범위
- 코드 정확 SHA `37a06cd77efcf71dd1576576157daef412adf70f`: `shipping_rights_preflight.py`는 **합성 CSV 1건**으로 `deliver_single`이 생성한 고객 폴더 `index.html`/`delivery.zip`/`receipt.json`을 `verify_customer_folder` 및 `verify_zip`로 재검증하고 ZIP 내부 `index.html`/`manifest.json`/`README_KO.txt` 허용멤버와 `data/shipping_rights_inventory_v1.json`의 진술을 대조한다.
- 내장 `ALLOWED`·`EXPECTED`와 실제 파일 구성이 달라지면 **fail closed**. 가짜 `LICENSE`/NOTICE shipping, 허위 `rights_owner_attested`/`commercial_distribution_approved`/`audit_is_independent` 등 선언, 동일 필드 중복 JSON, 예상 외 자산을 거부한다. 이 검사는 권리자·법무·외부 보안감사자의 **인증서가 아님**.
- 결괏값은 의도적으로 `status=HOLD_OWNER_IP_NOTICE_EXTERNAL_AUDIT`, `technical_synthetic_integrity_verified=true`, `commercial_release_approved=false`, `external_independent_audit_completed=false`, `score_addition=0`.
- 실행: `python shipping_rights_preflight.py`(합성 임시파일 생성/내부 기술검증), `python -m unittest test_shipping_rights_preflight -v` (6종). GitHub Actions [#43535767796](https://github.com/hibi89/data2web_studio/actions/runs/43535767796) **Python+browser 4/4 SUCCESS**: Windows `304/304` PASS, Ubuntu `303 PASS+1 Windows-only SKIP`, Chrome/Edge/Chromium 실브라우저 E2E PASS; [최종설계 게이트 #43535767926](https://github.com/hibi89/data2web_studio/actions/runs/43535767926) SUCCESS.
- **중요:** `LICENSE`와 `NOTICE`는 아직 생성/포함/허락되지 않는다. 해당 파일이 실제 필요하다고 권리자가 확정하면 `delivery.py`/독립 verifier의 v1 계약을 동시에 변경하고 구버전 동등성도 검증해야 한다. 실제 A 고객 재배포 권리가 없으면 `R21=PENDING` 유지.
- `R29`: 악성 자료 테스트와 기술 게이트를 돌렸더라도 개발자가 스스로 수행한 보안 테스트는 **외부 독립 보안감사**를 대체하지 못한다. 감사자·비용·자료 전송 범위는 사용자 별도 승인 필요. [감사 수용표](R29_INDEPENDENT_SECURITY_ACCEPTANCE_SCOPE_20261114.md).
- 원본/고객 데이터 무관. 고객 본인 PC의 원본이나 산출물을 변경하지 않고, GitHub repo에 실데이터·인증·기기경로를 저장하지 않는다.

## 85점 후보 완료 조건과 현재 차단
- **R07 2점**: 실제 원본 사용권·자료 제공자 동의, 원본 미변경 증거 + 법적/개인정보 권한 확인.
- **R21 4점**: 제품/상업 HTML 자산 권리 및 제3자 LICENSE/NOTICE 승인 + 승인된 납품 패키지 verifiable; 사전검증기만으로 안 됨.
- **R25 2점**: 실제 고객 데이터 보존기간·관리 주체·반환/파기 정책 사용자의 명시 승인/실행 책임.
- **R26 2점**: 개인정보·민감자료 처리 범위, 평문 고지, 적법한 사용·제공 권한의 고객 동의 및 사용자 확인.
- **R29 3점**: 별도 독립 평가자의 XSS/악성 XLSX·ZIP·TOCTOU/실OS 범위 감사 보고서 및 수정·재검증.
- **합계 잠재 +13 → 85**는 모든 요구 *전체* 수용 후에만. 현재 추가 인정점수0.
