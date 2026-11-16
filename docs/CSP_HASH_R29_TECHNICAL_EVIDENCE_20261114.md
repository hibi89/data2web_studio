# DATA2WEB JS CSP SHA-256 강화 기술 증거 / 2026-11-14 KST

## 구현 선택
A안: 단일 HTML 안의 정적 JavaScript만 SHA-256 Base64 hash로 허용하는 CSP. 추가 지출0원, Python 표준라이브러리 hashlib/base64 사용. 기존 모든 inline script를 허용하던 CSP보다 제한적이다. 오프라인 HTML/ZIP/receipt 구조 유지. 미선택 B안은 unsafe-inline 그대로 유지(보안 취약), C안은 외부 JS파일 분리(단일HTML 계약 변경).
- data2web_web.py에서 고정 JS의 정확한 문자열(공백/개행 포함)을 SHA-256으로 해시하고 meta Content-Security-Policy의 script-src에 허용한다.
- 사용자 데이터 JSON은 type application/json 비실행. 위험한 태그 종료문자는 이스케이프 처리. 사용자 CSV 교체 이후 새 HTML을 저장해도 JS 원문은 동일하여 CSP hash 일치.
- CSS style-src unsafe-inline은 유지. CSP 전체가 임의 코드를 완벽 차단한다고 주장하지 않는다. 외부독립 보안감사나 제3자 사용권 증명이 아님.
- 테스트 test_script_hash_csp.py 신규6종: 스크립트 unsafe-inline 제거, 정확 hash 대조, 변조 hash 거부, script 종료문자 이스케이프, 데이터 변경에도 동일 정적 hash, inline 이벤트속성 부재.
- 근거: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src

## 정확 소스 SHA와 실행
정확 CODE SHA: cab44263633be01a192d48a97e61e88f4a2a846f. 복구 기준 SHA: 02ef2b5d7cac5a09aec04bd479147ca0059a07fe.
- Windows/Ubuntu full Python/browser: https://github.com/hibi89/data2web_studio/actions/runs/43544123800 => 4/4 SUCCESS; Windows 345/345 PASS, Ubuntu 344 PASS+1 SKIP, Chrome/Edge/Chromium real file://, replacement/reopen/print/ZIP.
- macOS15 Python/Chromium: https://github.com/hibi89/data2web_studio/actions/runs/43544125433 => SUCCESS; macOS344 PASS+1 SKIP, Chromium file://, A4, keyboard.
- CodeQL public source: https://github.com/hibi89/data2web_studio/actions/runs/43544123781 => SUCCESS. 이는 코드 분석 워크플로 성공이며 Security alert 0개나 독립감사 완료를 인증하지 않는다.
- Synthetic product sample/screenshots: https://github.com/hibi89/data2web_studio/actions/runs/43544123843 => SUCCESS.
- Frozen R01–R33 100pt gate: https://github.com/hibi89/data2web_studio/actions/runs/43544123995 => SUCCESS.

기술강화는 R29 외부 독립 사람검증을 대체하지 못한다. 원본·scorecard·라이선스/NOTICE·고객 데이터 변경0. 공식72/100, 11 PENDING28점, RELEASE HOLD/SALE NO-GO, [작업중], 실제 크몽 미등록.
