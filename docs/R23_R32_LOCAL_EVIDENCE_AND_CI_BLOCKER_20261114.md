# DATA2WEB Studio · R23/R32 로컬 디바이스 증거 준비와 CI 실행 장애

> **2026-11-14 최신 해소 판정:** 사용자 GitHub Actions 한도 조치 후 동일 정확 검증 SHA `880586d7e63f38bd2c5e20f73f5bf46aa87d5d49`에 대해 [#43520777896 attempt2](https://github.com/hibi89/data2web_studio/actions/runs/43520777896) 4/4 SUCCESS (Windows284 PASS, Ubuntu283PASS/1SKIP, Windows Chrome·Edge/Ubuntu Chromium 실브라우저 E2E PASS), [gate #43520778342 attempt2](https://github.com/hibi89/data2web_studio/actions/runs/43520778342) SUCCESS. 이하 '실행 장애'는 최초 attempt 당시 기록이며 현행 blocker는 아님. R23/R29/R32 실고객 수용 미충족, 최종72/100/출시 HOLD 불변.

기록: 2026-11-14 KST. 기능 소스: `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113`, 코드 커밋 `b524cec21c670f4696fc469fe96ed96bfd3cf562`, Draft PR #4. **신규 코드 CI 검증 대기, 목표85 미달.**

## 결정 비교
| 방식 | 사용자/데이터 영향 | 유지비/검증 | 결정 |
|---|---|---|---|
| A: 기존 stdlib 합성 self-check에서 선택한 로컬 신규 JSON으로만 결과 저장 | 고객 원본·호스트명·절대경로 기록 없음, 외부 전송0 | 외부 API/호스팅0, 기존 런타임 내 재현 | **채택** |
| B: 클라우드 원격 테스트·진단 업로드 | 권리/개인정보/비용 승인 요구 | 네트워크·자격증명·운영 부담 | 배제 |

## 로컬 실행 및 해석
신뢰할 수 있는 새 폴더에서 Python 3.11+, 설치된 Chrome/Edge가 있는 Windows 장비라면 실행한다.

```bat
python studio.py self-check --browsers --evidence-output .\new-device-evidence.json
```

- 새 파일이 없을 때만 exclusive create, `DATA2WEB_LOCAL_DEVICE_EVIDENCE_V1` contract와 UTC 시각, 합성 파일/브라우저 점검 결과, SHA256을 로컬에 기록. 표준 출력에는 SHA256/상태만 표시.
- 이미 존재하는 증거 파일은 절대 덮어쓰지 않고 `HOLD`/종료코드2. 경로 바꾸기/서명·실기기 독립성을 자동 인증하지는 않는다.
- Chrome/Edge가 없거나 DOM 수용에 실패하면 `PARTIAL_HOLD`를 기록한다. 성공이라도 `PASS_SYNTHETIC_ONLY`이며 실제 고객 기기 인수나 민감자료의 승인 증거가 아니다.
- 실제 고객 Excel 파일의 구조·값·출처 권리·개인정보·환불·설치/서명 문제는 별도 실수용 필요. 고객 원본·샘플·리포트 파일을 자동으로 GitHub/ChatGPT에 올리지 않는다.
- 추가: 독립 검증기 `verify_customer_folder._load_json`는 Receipt/ZIP manifest에 NaN/Infinity/-Infinity 값을 거부한다. 이전 `verify_delivery`가 이미 같은 비정상 JSON을 거부하던 범위를 고객폴더 영수증까지 확장.

## 신규 추가 회귀(코드만 GitHub 반영)
- 합성 보고서 create-only/JSON 파싱/암호학적 SHA 확인/동일 경로 재호출 거부.
- 브라우저 부재 시 PARTIAL_HOLD, 고객수용 필드 false.
- `studio.py self-check --evidence-output`의 실제 subprocess/덮어쓰기 실패.
- receipt 비유한 JSON 상수 3종과 변경된 영수증 JSON 거부.

## CI와 실패 계층 (현재 실행 근거)
- 마지막 신뢰 가능한 기존 기능·평가 HEAD `c295639744e6bba06ab909070602c6235305fff9`: [Windows/Ubuntu/브라우저 Actions #43515478830](https://github.com/hibi89/data2web_studio/actions/runs/43515478830) **4/4 SUCCESS**, [gate #43515479406](https://github.com/hibi89/data2web_studio/actions/runs/43515479406) SUCCESS. 신규 코드 검증으로 환산하지 않음.
- 신규 HEAD `b524cec21c670f4696fc469fe96ed96bfd3cf562`: [Actions #43520221605](https://github.com/hibi89/data2web_studio/actions/runs/43520221605) FAILURE, [gate #43520221969](https://github.com/hibi89/data2web_studio/actions/runs/43520221969) FAILURE. 현장 조회한 Python/Windows브라우저/Ubuntu브라우저 jobs 모두 **0개 steps, 시작 직후 failure**, logs fetch는 BlobNotFound/404. Check-run annotations 개수는 확인했으나 본문을 접근할 수 없어 원인 확정 불가. 코드 테스트 실행/실패로 해석 금지.
- **Stop/Pivot:** 동일 무진전 재실행 반복 금지. GitHub repo Actions 탭의 실패 job 상단 사유(할당량/결제/러너 정책/조직 권한 등) 확인 또는 실행 가능한 Windows/Ubuntu 환경에서 로컬 `python -m unittest discover -v`를 먼저 수행. 원인 판정 후에만 CI 재검증.

## 공식 상태와 종료 기준
R01~R33 **고정 100점**, 이전 증빙 인정 22개 가중 **72점**, 11개 28점 미검증. R23/R29/R32 모두 PENDING 유지. 신기능을 점수로 자동 인정하지 않는다. 85점까지 추가 13점은 **요구 자체의 완료·정확 SHA 성공·실고객 및 권리 수용(해당 시)**이 확보돼야만 인정한다.

`[작업중]` 유지, RELEASE HOLD/SALE NO-GO, 고객 원본/기존 main 및 점수표 불변, Vercel 미적용.
