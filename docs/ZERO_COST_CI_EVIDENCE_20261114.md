# DATA2WEB Studio — 0원 정책 구현/검증 증거 (2026-11-14 KST)

## 정본/변경
- 공개 저장소: `hibi89/data2web_studio`, 브랜치 `feature/final-blueprint-p85-evidence-20261113`
- **코드·정책 정확 SHA:** `f7fc5607404d7349b95a85a0ebdb30a76ccc58ca`; 이전 안전 SHA `ea29ecec1a1fc272ed968e4f703d64d341086944`.
- 신규 `zero_cost_gate.py`, `test_zero_cost_gate.py`, `data/zero_cost_owner_policy_v1.json`, `.github/workflows/codeql-zero-cost.yml`, `docs/ZERO_COST_OWNER_AUTHORIZATION_20261114.md`. 기존 scorecard/가중치/ZIP verifier/REA 원본/고객자료/main 무수정.
- 비용: 공개 저장소 표준 GitHub runner+CodeQL, 로컬 stdlib, 외부 유료 결제/새 계정/호스팅/API/코드 서명/외부 고객데이터 업로드 0. **GitHub 계정 결제/청구서 자체 조회는 이번 검증에 포함되지 않음**; 공식 정책상 공개저장소 표준 runner 무료.

## 실행 증거 (실제 정확 SHA)
| 검증 | Actions | 판정 | 범위 |
|---|---|---|---|
| [Windows/Ubuntu Python + hosted browser](https://github.com/hibi89/data2web_studio/actions/runs/43540222122) | 43540222122 | **4/4 SUCCESS** | Windows Python 322/322 PASS, Ubuntu Python 322중321 PASS/1 SKIP, hosted Chrome/Edge/Chromium 브라우저 |
| [무료 Python CodeQL](https://github.com/hibi89/data2web_studio/actions/runs/43540222284) | 43540222284 | **1/1 SUCCESS** | Python 53/53 파일 및 GitHub Actions 4/4 파일 분석, SARIF 업로드 실행 |
| [최종설계 점수 게이트](https://github.com/hibi89/data2web_studio/actions/runs/43540222285) | 43540222285 | **1/1 SUCCESS** | 정본 R01–R33 100점, VERIFIED 72점, 85 목표, RELEASE HOLD |

- 신규 `test_zero_cost_gate.py` 7개 테스트 두 OS CI에서 모두 PASS: 정책변조/유료서비스/외부송신/보관기간/허위감사/허위점수/가격설정/중복 JSON 검증.
- CodeQL workflow 완료=보안 취약점 0건을 뜻하지 않음. **GitHub Security 탭의 alert 목록 자체는 아직 직접 감사/분류하지 않았음.** R29에 필요한 *사람에 의한 외부 독립 보안평가*와는 별도. CodeQL은 정적 분석이며 TOCTOU 실제 기기/시나리오의 모든 위험을 인증하지 않음.
- [무료 독립 외부 리뷰 요청 이슈 #5](https://github.com/hibi89/data2web_studio/issues/5) 생성. 현재 리뷰어/보고서/수용/수정후 재검증 미확보. 고객/원본/비밀 정보는 이슈에 포함하지 않음.

## 점수·권리·운영 정책
- 사용자 0원 일괄 내부 정책 승인: A 납품형 우선, B EXE 판매 후속, BASIC 49,000원/PRO 129,000원/BUSINESS 249,000원, 개인정보·민감/권리 미확인 원본 HOLD, 로컬 임시 사본은 고객 인수 후 최대7일 내 허가받은 수동 파기(법정 의무보존 예외), 법률/플랫폼 환불권 우선.
- 고객별 자료 사용권/개인정보 동의, 작성자/제3자 재배포 라이선스/NOTICE, 외부 독립 리뷰와 실제 고객 수용은 **실제 자료가 아직 없음**. 사용자 기본 정책 승인으로 법적 사실을 창작할 수 없음.
- R01–R33 고정 **72/100**, 목표85에13점 부족, R29 독립수용 0, 11개 PENDING. **[작업중] / RELEASE HOLD / SALE NO-GO / 상품 미등록**. PR #4 Draft 유지.
- 후속: 무료 외부 검토가 실제 진행되면 SHA pin/기기/재현/수정후 감사 보고서 확보; R07/21/25/26/27은 IP·고객별 문서에 근거해 개별 완전수용. 점수 상승은 그 이후에만. 별도 유료 경로는 채택하지 않는다.
