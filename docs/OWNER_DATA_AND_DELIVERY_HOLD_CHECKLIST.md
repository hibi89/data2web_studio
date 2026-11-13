# DATA2WEB — 고객자료·로컬 납품 승인 대기 체크리스트 (2026-11-13)

**정책 상태: DRAFT / 사용자의 법무·판매·데이터 권리 승인 없음.** 공개 구매자 안내·약관/환불·소유권·개인정보 보호법 준수 사실을 여기서 확정하지 않는다.

## 소유자 검수 및 사용권
- 고객 제공 파일의 권리·개인정보 처리 목적/범위·계약 주체/처리자 지위를 사전에 확인한다. 고객이 실제 권리를 갖지 않는 파일을 AI나 GitHub에 업로드하지 않는다.
- `studio.py inspect file.csv`는 실제 셀 값을 stdout에 출력하지 않고 SHA/행수·헤더·타입/NULL/중복 요약만 제공. 컬럼명 자체가 비밀일 수 있으므로 로그 공유도 승인 없이 금지.
- 민감 컬럼이 있으면 이 제품이 **암호화/익명화/비식별화를 제공한다고 주장하지 않는다**. HTML/ZIP에 원본 셀 값 평문이 포함되며 사용권/접근 제한/고객 인수 별도 확인 전 RELEASE HOLD.
- 다중파일 승인 매니페스트의 privacy_classification `NO_PERSONAL_DATA_REVIEWED` 또는 `OWNER_APPROVED_LOCAL_ONLY`은 사용자가 선택한 자기 진술이다. 법적 허용/위험 없음의 증거가 아니다.

## 다중 원본 소유자 승인 매니페스트 예제(합성만)
```json
{
  "contract": "DATA2WEB_INPUT_APPROVALS_V1",
  "sources": [
    {"filename": "first.csv", "sha256": "<실제 첫 파일의 소문자 SHA256 64글자>"},
    {"filename": "second.tsv", "sha256": "<실제 둘째 파일의 소문자 SHA256 64글자>"}
  ],
  "mapping": {"id": "id", "title": "title", "category": "category"},
  "approval": {
    "rights_and_plaintext_ack": true,
    "privacy_classification": "NO_PERSONAL_DATA_REVIEWED"
  },
  "name": "내 데이터 보고서",
  "theme": "office"
}
```
본 JSON/예제의 SHA placeholder는 유효 SHA가 아니므로 **그대로 실행할 수 없다**. 각 파일을 먼저 독립 `inspect`하고 실제 SHA, 원본 데이터 사용권/개인정보 범위를 검수해야 한다. XLSX 항목은 `"sheet":"실제 시트명"`, 필요 시 `"header_row":1`·`"allow_cached_formulas":false`를 정확히 추가한다. 모든 파일은 매니페스트와 같은 실제 로컬 폴더의 단순 파일명이며 외부 링크·상위 경로·중복/서로 다른 헤더·ID 중복은 거절한다.

```bash
python studio.py inspect first.csv
python studio.py inspect second.tsv
# approval.json에 각 실제 SHA/허용 시트·동의를 명시적으로 넣은 다음
python studio.py deliver-append approval.json ./new-customer-folder --confirm APPROVE --ack-plaintext
python studio.py verify ./new-customer-folder/delivery.zip

# Python3.11만 필요한 재현 가능한 배포 도구(서명된 EXE 아님)
python package_portable.py portable.pyz
python portable.pyz inspect first.csv
```

`deliver-append`는 기존 디렉터리를 덮어쓰지 않는다. 생성 폴더에는 `index.html`, `delivery.zip`, `receipt.json`이 있다. 실패하면 기존/생성 파일 자동 삭제 없음, 남은 출력물을 불완전한 HOLD 증거로 간주하고 신규 폴더를 검수해 재생성한다.

## 납품·상업적 운영 보류 항목
- **미승인:** DATA2WEB 자체 소스 코드 고객 사용권/재배포 라이선스, 라이선스/NOTICE 파일, 고객 파일 저작권·PII 동의·접근제어, 크몽 SKU별 판매범위·수정 횟수·지원기간·가격·환불/하자처리, 고객 인수 증거·사후 보유/파기기간.
- **미검증:** 실제 고객 Windows10/11 Chrome·Edge, Excel 복잡 수식/서식/그림/외부연결, macOS, 원본 REA Lite의 실코드 full golden, 결제/상업적 배포.
- **현행 기술적 보존:** 소스 파일을 프로그램에서 삭제·덮어쓰지 않는다. HTML·ZIP·receipt는 create-only. GitHub/원격 API/고객 파일 자동전송 없음. 그러나 PC 운영체제·백업·고객이 직접 삭제/복사하는 행위나 완전한 데이터 보안을 보장하지 않는다.
- **원본 SHA:** 새 HTML에 브라우저 CSV를 교체하여 다시 다운로드하면 이전 승인 SHA·시트 선택/캐시 승인 이력은 검증 종료 처리한다. 재생성 전 새 원본의 SHA를 다시 inspect 해야 한다.
- 운영자 승인 없이는 `RELEASE HOLD`, `SALE NO-GO` 및 크몽 원장의 `[작업중]` 표시를 유지한다.

## 2026-11-13 단일 파일 고객 폴더 명령 추가
```bash
python studio.py inspect file.csv
python studio.py deliver file.csv new-client-folder --source-sha256 <실제 SHA256> \
 --id id --title title --category category \
 --confirm APPROVE --ack-plaintext --privacy-classification NO_PERSONAL_DATA_REVIEWED
python studio.py verify new-client-folder/delivery.zip
```
- `NO_PERSONAL_DATA_REVIEWED`는 실제 소유자 스스로 개인정보 검수를 했다는 **선언값일 뿐** 시스템의 법적 적합성 판정이 아니다. 개인정보가 존재하면 법적·고객 승인 없는 상용 납품 금지.
- 새 폴더만 생성, HTML·ZIP·영수증 파일을 create-only로 출력. XLSX는 `--sheet 실제시트명` 명시가 없으면 폴더를 만들기 **전** HOLD. 실제 고객 Win10/11 Chrome/Edge·업무 Excel 원본 샘플 인수는 미검증. Python3.11 .pyz 지원도 **서명/EXE가 아니다**.
- 원본 공용 REA Lite의 pinned SHA 실제 실행 및 `file://` 비교는 합성 데이터 범위 [최종설계 85 재검증](FINAL_BLUEPRINT_85_REASSESSMENT_20261113.md)에 기록했다. 상업 라이선스 승인 증명과 무관하다.

## 새 로컬 데스크톱 검수 및 폴더 전체 검증 (2026-11-13)

```bash
# Python 3.11+ 및 Tcl/Tk 포함 로컬 PC에서 실행 (외부 서버 없음)
python studio.py desktop
# 또는
python data2web_desktop.py

# GUI/CLI가 새로 만든 customer 폴더에 HTML·ZIP·영수증이 모두 일치하는지 검증
python studio.py verify-customer ./new-client-folder
python tool.pyz verify-customer ./new-client-folder
```

- 데스크톱 GUI는 현재 **단일 입력 파일**만 처리한다. 다중파일 `deliver-append`는 기존 수동 승인 매니페스트 기반 CLI를 사용한다. GUI가 고객의 파일 권리·민감정보를 법적으로 검사하거나 자동으로 판매를 승인하지 않는다.
- Windows 호스팅 환경의 실제 Tk GUI 렌더와 데이터 선택/동의/생성 컨트롤 headless 계약 테스트는 PASS, **실제 구매자 Win10/11 GUI 클릭 시나리오와 배포 서명 EXE는 미검증**. UI 구성요소가 설치된 Python에서만 실행 가능하다.
- `verify-customer`는 서명이 아니라 `index.html`, `delivery.zip`, `receipt.json`의 **같은 폴더 내부 무결성 일치**만 확인한다. 원본/실구매자 계약·개인정보 동의·상업권리·신원은 확인하지 않는다. 추가 파일·불일치 데이터는 HOLD.
- GUI 방식 선택 이유/제약 및 변조 시험: [docs/FINAL_BLUEPRINT_GUI_DELIVERY_20261113.md](docs/FINAL_BLUEPRINT_GUI_DELIVERY_20261113.md). 소유자 가중치 미승인으로 공식 85% 여전히 미인증.


## 2026-11-14 고객 PC 자기검증(합성 데이터만)
python studio.py self-check --browsers 를 실행하면 자동으로 2행 합성 CSV→새 고객폴더 HTML·ZIP·receipt→독립 검증 및 설치 Chrome/Edge 헤드리스 렌더를 확인한다. 실제 고객 파일을 건드리지 않으며 출력은 플랫폼 종류·브라우저별 PASS/HOLD만 포함한다. 브라우저 미설치/렌더 오류는 PARTIAL_HOLD, 통과해도 PASS_SYNTHETIC_ONLY, 상업권리/실 고객자료/계약 승인 아님. 실제 Windows10/11에서 사용자 승인 후 실행한 결과만 해당 PC 근거로 채택. Windows hosted 자동시험만으로 실제 Win10/11 인수확정 금지.


## 2026-11-14 KST · Windows Python 포터블 실행 정책 보류
새 package_windows_bundle.py는 Python3.11이 사전 설치된 PC에서 쓸 수 있는 미서명 .pyz+Windows CMD·manifest이며 서명된 독립 EXE가 아니고 사용권·고객 인수/상품 판매 허가가 없다. RUN_SELFCHECK.cmd는 합성 데이터만 생성/검사하고 기존 고객 자료는 읽거나 삭제하지 않는다. 실 Win10/11 사용자 설치와 고객원본 권리·개인정보 보유/파기·LICENSE/NOTICE·지원/환불·상품 SKU/가격은 사용자 별도 승인 필요.
