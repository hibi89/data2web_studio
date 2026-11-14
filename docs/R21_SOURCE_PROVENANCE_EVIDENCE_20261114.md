## 2026-11-15 KST update — exact six-file blob comparison at `320aebc23163019f85e1c345857ff4ed3da8147a`

The PR code tree at `320aebc23163019f85e1c345857ff4ed3da8147a` was read through GitHub's Git tree endpoint and compared with the original R21 pin manifest snapshot `0219a10c03cab826220a78af128cffdae995ac9f`. This is a source identity comparison only.

| R21 producer | Pinned blob | Actual blob at `320aebc` | State |
|---|---|---|---|
| `data2web_web.py` | `65bd8fe16d7b284f553d5185ed369650cc83d82f` | `65bd8fe16d7b284f553d5185ed369650cc83d82f` | MATCH |
| `delivery.py` | `52075fc6ebdb5f886a2c05725b4c1aabf4b0dbba` | `c0013e445f3d4b419314c795d387643abc176f48` | DRIFT |
| `receipt_utils.py` | `02378bc8b18e6a37f225dc2c132fa9456551af64` | `137f4086fe08cfe22722186ffc0b47aa30957817` | DRIFT |
| `data2web_single.py` | `bc1c8499f48c7f1f8b7b0d0b3b713d9328d05fc6` | `b24e7495f4c43131dcbd986ac7bb75dfd3d979c0` | DRIFT |
| `data2web_append.py` | `3770f6bfc3bbe9e634e694226027eda0bd0c8f38` | `92ccab387a61f9546d13bf9c48a97875e84ae740` | DRIFT |
| `data2web_tabular.py` | `66c2fb8910b1202ae3b0301e8b615158d9a5fac9` | `66c2fb8910b1202ae3b0301e8b615158d9a5fac9` | MATCH |

The customer A delivery boundary was cross-checked in current code and tests:
- `delivery.py` emits `index.html`, `manifest.json`, `README_KO.txt` into the ZIP; `verify_delivery.py` independently allows exactly those three members.
- `verify_customer_folder.py` independently requires exactly `index.html`, `delivery.zip`, and `receipt.json`.
- `receipt_utils.py` creates the local receipt. The synthetic inventory lists all four A artifacts and keeps every rights state pending.
- The HTML renderer keeps CSS/JS inside the generated HTML. At exact `320aebc23163019f85e1c345857ff4ed3da8147a`, hosted Chromium and Windows Chrome/Edge logs report local-file owner flows with `network0`. The owner-only Windows EXE/runtime, upstream golden test source, and CI-only test dependencies are excluded from A customer delivery.
- Exact [Python/browser #43644268104](https://github.com/hibi89/data2web_studio/actions/runs/43644268104) logs show customer-folder, single-delivery, receipt, and create-only regressions passing on Windows and Ubuntu. The integrated `test_manifest_matches_real_synthetic_zip_receipt_and_stays_hold` cannot complete because the first source-provenance check correctly rejects the four changed blobs. Thus the detailed output-contract checks pass, while the full integrated shipping preflight remains blocked.

A21-01 technical inventory reconciliation is recorded; source-origin acceptance and real rights/NOTICE decisions remain separate A21-02/A21-03 work. No source pins, score, license, or sale state were changed. This table is not an owner source review, copyright opinion, commercial permission, or external audit.

## 2026-11-15 KST update — producer source drift; R21 review required

At code/test SHA `92dca1824e24700dc38f8f9fa4ae3775488c2d3f`, the four delivery producer files below contain handle-anchored create-only output changes and no longer match the historic pins in `data/r21_source_provenance_v1.json` (snapshot `0219a10c03cab826220a78af128cffdae995ac9f`):

- `data2web_single.py`: `b24e7495f4c43131dcbd986ac7bb75dfd3d979c0`
- `data2web_append.py`: `92ccab387a61f9546d13bf9c48a97875e84ae740`
- `delivery.py`: `c0013e445f3d4b419314c795d387643abc176f48`
- `receipt_utils.py`: `137f4086fe08cfe22722186ffc0b47aa30957817`

The R21 provenance check deliberately remains fail-closed with `Shipping producer source drift requires R21 review`. The historic pin manifest has **not** been mechanically refreshed. GPT-6 High read-only review found the anchored writer changes reasonable, but that code review is not an owner source-origin/rights review, commercial license, NOTICE decision, or R29 independent audit. R21 source-change review and actual commercial redistribution rights remain distinct pending gates. Until the authorized source review is recorded, the current R21 source provenance and full exact-SHA test matrix are blocked.

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

## 2026-11-14 21:36 KST 코드 및 CI 정정 기록
- 최종 기능 SHA `1be21c6a3f4ba2426c93a71201d96e274ce22ee7`; GitHub Actions [Windows/Ubuntu/browser #43595570078](https://github.com/hibi89/data2web_studio/actions/runs/43595570078) 4/4 SUCCESS, Windows 507/507 PASS, Ubuntu 506 PASS + 1 SKIP. [CodeQL #43595570039](https://github.com/hibi89/data2web_studio/actions/runs/43595570039) SUCCESS, [blueprint #43595570534](https://github.com/hibi89/data2web_studio/actions/runs/43595570534) SUCCESS. 이 SHA의 macOS 미실행.
- 중간 SHA `5a8d94a`의 Windows CRLF git worktree 변환으로 인한 1 FAIL / 4 ERROR와 `abc0ab86` 테스트 fixture 1 FAIL은 원인 구별 후 수정. Windows/Linux를 동등하게 다루는 source Git blob 검사는 CRLF checkout 표현만 정상화하며 진짜 소스 변경은 반드시 HOLD.
- **R21/R29 법적·독립 수용 불가**: 실제 권리자 서면 확인/의무 NOTICE 및 독립 외부 감사는 아직 없다. 85점을 허위로 선언하지 않고 현재 72/100, RELEASE HOLD 유지.
