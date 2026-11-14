# DATA2WEB Studio — R07/R25/R26 운영자 사본 보유 점검 (합성·로컬 전용)

**상태: 내부 운영 보조 도구, 법적/실제 고객 수용 증거 아님 · 공식 최종완성률 72/100 · RELEASE HOLD**

## 목적·선택 설계
승인된 0원 운영 기본정책에 따라 외부 전송 없이 **운영자 로컬 임시 사본을 최대 7일, 목적 달성 시 지체 없이 수동 파기 검토**한다. 고객 PC의 원본·기존 산출물을 자동 삭제하거나 수정하지 않는다. 개인정보/민감/제3자 비밀·권리 불명 자료는 별도 고객별 계약·안전성 판단 전 HOLD.

비교한 설계:
- A. 자동 삭제/고객파일 스캔: 외부전송은 없어도 원본 훼손·오탐·삭제권한·동의 불명 위험이 크므로 **배제**.
- B. 독립된 익명 메타데이터의 날짜·상태를 **읽기 전용**으로 판정하고, 필요 시 새 로컬 보고서만 create-only 저장: **선택**. 고객 데이터 원문·원본 경로·성명·파일명은 접수하지 않음.

## 사용법
```bash
python operator_copy_retention.py --synthetic-self-check
python operator_copy_retention.py --metadata-file <local-anonymous-metadata.json> --new-report-file <new-report.json>
python -m unittest test_operator_copy_retention -v
```

메타데이터 형식 (아래는 **가상 일시/가상 상황**이며 고객 동의가 아니다):

```json
{
  "contract": "DATA2WEB_OPERATOR_COPY_RETENTION_REVIEW_V1",
  "operator_copy_present": true,
  "received_at_utc": "2026-11-13T12:00:00Z",
  "source_scope": "NONPERSONAL_NONCONFIDENTIAL",
  "purpose_completed": false,
  "legal_retention_exception_claimed": false,
  "per_order_rights_claimed": false,
  "per_order_plaintext_ack_claimed": false
}
```

반환값은 현재 UTC 대비 보유 최종 시점과 확인이 필요한 **정형 코드**만 표시한다. 데이터 수신 확인·실제 고객 동의·권리 증명·법정 예외의 유효성·파기 완료를 자동 인증하지 않는다. 표기된 7일은 법률상 모든 기록의 보존기한이라는 뜻이 아니라 **이번에 승인된 내부 임시 사본의 기본 최대 보유기간**이다. 실제 법률상 별도 보존이 필요한 자료는 분리해 법률·책임자 근거를 수동 확인한다.

도구는 고객 원본이나 사본 파일을 읽지 않으며, 운영자 자기신고를 독립 증명으로 간주하지 않는다. 결과 생성이 고객 수집·판매나 공개 배포 승인이 되는 것은 아니다. 파기가 필요하다고 나오면 **권한자 본인이 보존 예외·대상·백업·법적 의무를 검토한 후** 별도 수동 절차로 진행하고, 실제 독립 증빙 없이 R25 점수를 올리지 않는다.

## A25-02 빈 사본 custody·보유·반환·파기 기록 서식

공개 저장소에는 실제 고객 기록이 아닌 [빈 운영자 사본 기록 서식](A25_02_COPY_CUSTODY_RECORD_TEMPLATE_20261115.md)을 둔다. 이 서식은 운영자 로컬 원본 사본과 생성 결과 사본을 별도 기록하고, 실제 사본이 없는 경우도 기록한다. 완료된 고객별 기록·식별자·경로·증빙은 비공개 통제 위치에만 보관한다.

## 남은 의존성
R07 고객의 실제 자료 사용·공유권 확인과 동의, R25 실제 판매자 사본의 보존/파기 및 수령자 확인 기록, R26 실제 개인정보 범위·접근권·평문 노출 고객 동의, R21 승인된 IP/NOTICE 및 R29 외부 독립 보안평가는 모두 PENDING. 판매·실고객 데이터 처리·외부 전송은 별도 승인 전 금지.
