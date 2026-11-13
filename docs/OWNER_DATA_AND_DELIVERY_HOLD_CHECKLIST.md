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
