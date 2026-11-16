# DATA2WEB Studio — R29 외부 독립 보안감사 요청서 및 수용 기준 초안

**2026-11-14 KST / 주의:** 이 문서는 **감사 발주가 아니라 감사를 위한 범위 정의**. 유료/무상이라도 외부로 **비공개 코드·파일/데이터를 전송하거나 별도 계정/권한을 부여하려면** 실제 범위와 대상을 형이 먼저 승인해야 한다. 고객 자료·실제 경로·토큰 없이 **합성/공개 소스만** 검증. 감사자 확정/계약/보고서 없음 → **R29=PENDING**.

## 감사 목적과 신뢰경계
- 임의의 파일/ZIP/XLSX/JSON/CSV/TSV가 읽기 전용 원본에서 오프라인 HTML/ZIP/receipt로 이동하는 과정에서 XSS, 외부 요청, 파일 교체/링크/경합, ZIP 탈출/중복/폭탄, 수식/위조·개인정보 평문 노출 위험을 탐지한다.
- 핵심 경로: `data2web.py`, `data2web_tabular.py`, `path_policy.py`, `data2web_web.py`, `delivery.py`, `verify_delivery.py`, `verify_customer_folder.py`, `data2web_single.py`, `data2web_append.py`, `studio.py`, `data2web_desktop.py`. 정확 commit SHA pin, 분석 결과 재현 가능해야 한다.
- 신뢰 경계: 로컬 원본(잠재 공격), 사용자 권리/평문 승인, create-only 새 폴더, HTML JS/CSP, ZIP/receipt, 제3자 EXE/bundled runtime. 외부 API/클라우드 데이터 전송, 서버 인증 기능은 원래 제품에 없으며 추가 금지.

## 외부 평가 최소 매트릭스
| 범위 | 공격·입력 | 요청할 증거 및 수용 조건 |
|---|---|---|
| XSS/HTML·JSON escaping | `<script>`, `</script>`, HTML event attrs, JSON end-tags, Unicode line separators | 화면에 데이터 텍스트만 표시, 실행/외부 요청 불가, CSP 확인 |
| CSV formula injection | `=SUM`, `+cmd`, `@function`, 탭/개행과 사용자 입력 | 외부 앱·수식/매크로 실행되지 않음, CSV 내보내기 경계 검증 |
| XLSX OOXML | malformed ZIP, XML entity, 과다 압축·시트·수식 캐시/외부 link/매크로 | 메모리·용량/시간 제한 내 HOLD, 공격코드·외부네트워크 없음 |
| ZIP/manifest/영수증 | ZIP-slip, duplicate names, fake CRC, duplicate JSON keys, NaN, 숨겨진 prefix/suffix, symlink | verifier fail closed, 원본/정상 납품물 무수정·무삭제 |
| 경로 교체/TOCTOU | 승인 뒤 rename/symlink/hardlink/junction, 파일·폴더 교체, mtime/ctime 경합 | 실제 Win11+가능한 Win10/Linux/NTFS와 지원파일시스템에서 위험·제약 보고, 우회 성공 발견 시 BLOCK |
| 파일 생성·복구 | 기존 타깃 재실행, 롤백, 권한 오류, 전원/프로세스 중단 | 덮어쓰기/삭제 금지, HOLD 및 수동 복구 가능 |
| 오프라인 네트워크 | HTML `file://` Chrome/Edge/Chromium DevTools/헤드리스 실행 | 요청·비밀 유출0, 개발도구 권한 요구 없음 |
| 오너 동의/평문 | 승인 누락/변조/미승인 자료 전송 | 계약·권리의 **법적 타당성은 별도**지만 기술에서 승인 우회/자동출력이 없어야 함 |

## 재현성·독립성 정의
- 평가 주체: 제품 개발자가 아닌 별도 권한 있는 **독립 보안 평가자**. 이 저장소의 CI/ChatGPT 자기점검 또는 코드 생성기 보고서만으로 `R29`의 외부독립 감사 요건을 충족했다고 할 수 없음.
- 필요 산출물: 독립 평가자 신원/소속(외부 공유 가능 범위), 감사자·일자, SHA pin, 합성 fixture 범위, OS/브라우저 버전, 실행 명령/테스트 스냅샷, 재현 단계·심각도/위험·취약점 목록, 제한/미실행 항목, 코드 수정 후 재검증 사인. 직접 스크린샷/실고객 원본·IP를 공개할 필요 없음.
- 감사 FAIL·미검증이면 `[작업중]`/RELEASE HOLD/SALE NO-GO 지속; 어떤 취약점도 CI 녹색으로 상쇄하지 않음. 독립 감사를 진행하되 실제 고객 파일을 감사자에게 제공하지 않으며, 계약상 제공 필요시 형의 명시 승인과 자료권리 확인이 별도 필요.

## 실천 순서(형 개입 최소)
1. AI: 리포 source SHA/합성 test harness·위협목록·현재 회귀 증거 정리.
2. 형: 독립 감사 기관/사람, 비용·전송 범위·접근/계약/NDA를 사전 승인; 비용 승인 전 견적 의뢰/결제/권한 부여 없음.
3. 승인된 외부 평가자: 합성/권리 허용 자료만으로 환경/취약점 재현, 미확인 영역 기록.
4. AI: 증거 기반 최소 수정·새 SHA/회귀, 평가자 재검증.
5. 내부 최종 점수 게이트: **R29 전체 통과가 증빙된 경우에만 3점**. 사용자 권리/라이선스·출시 GO는 별도 요건.
