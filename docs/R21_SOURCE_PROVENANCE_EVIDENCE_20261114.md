# R21 — 납품 생성 소스 Git blob 핀 및 권리 미확정 증거 (2026-11-14 KST)

**공식 완성률: 72/100. R21 = PENDING / R29 = PENDING / RELEASE HOLD.**

## 이미 확인한 사실
- A 납품물은 고객 폴더 `index.html`, `delivery.zip`, `receipt.json`의 3파일이다. ZIP에는 `index.html`, `manifest.json`, `README_KO.txt`만 포함한다.
- `index.html` 생성 소스는 `data2web_web.py`, ZIP과 README/manifest 소스는 `delivery.py`, 영수증 생성 소스는 `receipt_utils.py`이며, 로컬 생성·배치 처리는 `data2web_single.py`, `data2web_append.py`, `data2web_tabular.py`가 관여한다.
- 위 6개 파일의 **현재 Git blob SHA**를 `data/r21_source_provenance_v1.json`에 고정했다. `r21_source_provenance.py`가 실제 Git blob 바이트와 비교하며, 부정확한 해시·미등록 파일·위조된 권리/감사/점수 플래그를 거부한다. 기존 합성 납품 preflight에 통합해 원본의 묵시적 변경이 자동으로 무검토 통과되지 않도록 한다.
- 이 SHA는 소스 revision 식별자이며 **진위 서명/저작권·상업 사용권 증거가 아니다**. 소스가 정당하게 바뀌면 R21 추적 목록을 검토한 뒤 승인된 소스 해시를 갱신해야 한다. 임의로 해시 자동 수정하는 기능은 없다.
- 루트 `LICENSE`/`NOTICE`, 고객 산출물에 대한 정당한 저작권자의 서면 승인, 제3자 구성요소의 의무적 라이선스/고지 여부, 고객이 제공할 실제 자료 권리는 **여전히 미확인**이다. 임의 라이선스 파일을 생성하거나 ZIP에 삽입하지 않았다.

## 설계 비교와 선택
- **A**: 소스명·권리 현황을 문서에만 열거. 비용은 0원이지만 소스 변경에 취약.
- **B (선택)**: 고정 whitelist + Git blob SHA + CI-연계 합성 납품 결과를 교차검증. 표준 라이브러리, 추가 현금지출 0원, 소스 수정 시 확인 필요. 다만 법적 권리 판단 불가능.

## 독립 권리자 확인 시 필요한 사용자 입력 (한 번에 모음)
1. 생성된 HTML/CSS/JS/README/영수증 및 원본 참조 소스의 실제 권리자·공동 기여자·제3자 포함 부분을 구분한 권리 증거.
2. 각 의무적 제3자 라이선스와 NOTICE 배포 조건에 대한 확인. 없다고 주장하려면 어떤 자산/의존성을 조사했는지 근거 포함.
3. 고객이 받을 결과물의 사용 허락 범위와 실제 개별 고객의 데이터 처리·재배포 권리/평문 동의.
4. 독립 R29 보안 검토자에 관한 범위·SHA·비용(사용자 승인 0원 조건), 검토 결과와 수정 후 재검증. 개발자 자체 CI와 CodeQL만으로 R29 3점 인정 불가.

**명령**: `python r21_source_provenance.py`, `python shipping_rights_preflight.py`, `python -m unittest test_r21_source_provenance -v`.

**점수 판정**: R21 +4 / R29 +3 및 R07/R25/R26 +6을 포함한 +13 인정에는 각각의 최종설계 전체 수용 증거가 필요하다. 내부 기능 테스트 또는 이 자료 자체로 점수 상승 없음.
