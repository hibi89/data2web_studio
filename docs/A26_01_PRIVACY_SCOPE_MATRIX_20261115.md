# A26-01 — 개인정보 범위 분류표와 노출 경로

**상태: 기술 검토 보조물만 제공.** 아래 분류는 합성 범위만 설명하며 고객 사례가 아니다. 분류값은 사용자가 제출하는 자기검토 진술이며 기계 탐지·법률 자문·고객 동의·익명화·권리 증명이 아니다. 고객별 적법한 처리근거와 명시 동의가 미확보되어 R26은 계속 PENDING이다.
## 2026-11-15 exact-SHA technical recheck

At tested source/workflow SHA `635db258ee3e8b5d1e8f0418c8a3db8cd19ed661`, `python -m unittest test_order_intake_preflight -v` passed 24/24 on Windows, Ubuntu and macOS. Full hosted regression and Windows Tk/Chrome/Edge plus Ubuntu/macOS Chromium local-file flows also passed. These checks confirm the technical fail-closed path only; the classification remains operator self-report, and customer-specific lawful basis/consent are still missing. R26 remains PENDING and the official score is unchanged at 72/100.


## 합성 개인정보 분류표

익명 사전검수 입력 계약은 V2다. 정확한 privacy_classification 값과 엄격한 contains_personal_or_sensitive, contains_third_party_confidential 불리언을 모두 요구한다. 기존 권리·평문 확인도 여전히 필요하다. scope candidate가 될 수 있는 범위는 명시적으로 검토한 NO_PERSONAL_DATA_REVIEWED뿐이고, 주문 수락이나 판매 승인은 항상 false다.

| 분류값 | 합성 예시 범위 | 사전검수 결과 |
|---|---|---|
| NO_PERSONAL_DATA_REVIEWED | 직접·간접 식별자, 민감/의료정보, 결제 식별자, 제3자 비밀/공유 자료가 없고 범위와 권리가 검토됨 | 나머지 조건을 모두 충족해도 scope candidate에 한정 |
| PERSONAL_OR_IDENTIFYING_DATA_PRESENT | 이름, 이메일, 전화, 주소, 계정/회원번호, 기기/위치 식별자 또는 조합으로 식별 가능한 열 | HOLD_PREORDER |
| SENSITIVE_OR_MEDICAL_DATA_PRESENT | 건강, 진단, 치료, 장애, 생체정보 또는 기타 민감 정보 | HOLD_PREORDER |
| PAYMENT_DATA_PRESENT | 카드/은행/결제 자격정보, 식별 가능한 거래/계정 정보 | HOLD_PREORDER |
| THIRD_PARTY_CONFIDENTIAL_OR_SHARED_DATA | 계약상 비밀, 제3자/다른 고객 자료, 공유 데이터, 재배포 제한이 불명확한 자료 | HOLD_PREORDER |
| UNKNOWN_OR_MIXED_SCOPE | 미검토, 의미 불명 열, 여러 범주의 혼재, 출처 불명, 허용범위 이견 | HOLD_PREORDER |

분류 누락, 잘못된 형식, V1 구형 입력, 미등록 값은 fail-closed 처리된다. 기존 두 위험 불리언 중 하나가 true면 안전 분류를 선택했더라도 HOLD다. 미등록 식별자 키와 잘못된 분류값은 회귀시험에서 거부한다. 이 사전검수는 원본 파일을 열지 않으며 행값, 고객명, 경로를 받지 않는다.

## 데이터 흐름과 평문/오프라인 노출

| 단계 | 제품 동작 | 개인정보·노출 경계 |
|---|---|---|
| 익명 사전검수 | 운영자가 입력한 형식·건수·위험 불리언·개인정보 분류값만 읽고 고객 원본은 열지 않음 | 분류는 자기진술이며 실제 값 속 식별자를 탐지하지 못함 |
| 로컬 원본 검수 | 선택된 로컬 파일을 파싱해 SHA·헤더·프로파일을 확인 | 데스크톱은 원본을 업로드하지 않지만 열 이름 자체가 민감할 수 있음 |
| 변환 및 브라우저 결과 | 승인한 행·열을 오프라인 HTML로 생성 | index.html에 원본 값이 평문으로 들어갈 수 있으며 암호화·접근제어·자동 익명화 기능은 없음 |
| ZIP 및 영수증 | 출력물과 함께 로컬 ZIP/영수증 생성 | 무결성 검증은 개인정보 보호, 권리, 동의를 증명하지 않음 |
| file:// 열기 | 제품 서버 없이 지원 브라우저에서 로컬 HTML 열기 | 오프라인이어도 기밀성이 보장되지 않는다. 파일 접근자는 읽거나 복사·전달할 수 있음 |
| 운영자 보유 | 운영자가 원본 또는 결과 사본을 보유할 수 있음 | 원본/결과 사본은 별도 기록하며 수동 삭제·반환 권한이 필요 |

단일·다중 GUI는 NO_PERSONAL_DATA_REVIEWED와 OWNER_APPROVED_LOCAL_ONLY를 제공한다. 두 값 모두 소유자의 자기진술이다. OWNER_APPROVED_LOCAL_ONLY는 암호화, 익명화, 법적 허용 또는 고객 동의를 뜻하지 않는다. 직접/간접 식별자, 민감·의료정보, 결제정보, 제3자 비밀/공유 자료 및 불명·혼합 범위는 고객별 권리·처리근거·수신자·평문·보유 범위가 확인되기 전 HOLD다. GUI에 이러한 제한과 평문 노출 안내가 표시된다.

이 절차는 우발적 범위 확대를 막는 보조장치이며 고객의 법적 권한을 독립 검증하지 않는다. 실제 고객 데이터, 서명, 경로, 비공개 증거를 외부 서비스에 올리지 않는다.

## 정확 SHA hosted 검증 (2026-11-15)

- 코드 SHA 4e6808b80023157cf9f849f600e18ed123e258e0에서 전체 522개 unittest가 실행됐다: Windows 522 PASS, Ubuntu/macOS 각 521 PASS + Windows 전용 1 SKIP.
- 새 개인정보 분류 부정 케이스가 각 실행에서 PASS했다. Python/browser Actions #43608095426, macOS #43608095412, CodeQL #43608095464도 SUCCESS다.
- [GPT-6 High 내부 재검수](https://github.com/hibi89/data2web_studio/commit/4e6808b80023157cf9f849f600e18ed123e258e0)는 조치 가능한 finding이 없었다. 이는 R29 독립 외부감사가 아니다.
- R26의 실제 고객별 처리근거·범위·명시 동의는 미확보이며, 공식 점수 72/100과 RELEASE HOLD / SALE NO-GO를 유지한다.
