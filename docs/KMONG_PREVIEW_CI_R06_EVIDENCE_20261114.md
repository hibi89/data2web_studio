# DATA2WEB 0원 크몽 합성 시연물 자동재생성 게이트 증거 — 2026-11-14 KST

## 실제 결함과 최소 수정
기존 .github/workflows/kmong-synthetic-preview.yml은 data2web_web.py·data2web_single.py·delivery.py 등 일부 변경에만 실행되었고, 핵심 data2web.py/data2web_tabular.py/path_policy.py/receipt_utils.py/verify_delivery.py 수정에서는 최신 합성 시연물이 자동 갱신되지 않을 수 있었다. 실행과 산출물이 서로 다른 SHA가 되는 위험을 줄이기 위해 경로필터 6개를 추가했고, 별도 R06 검증 test_xlsx_inspection_snapshot.py + test_output_snapshot_security.py (12 종) 실행이 성공한 후에만 실제 합성 시연 HTML·ZIP·영수증·스크린샷을 생성하고 7일 artifact로 업로드하도록 했다. Windows 구매자/고객 실제 자료는 접근하지 않음.

## 정확 검증 SHA
- 단일/append 빌더의 최신 보안기능 소스 SHA ed89a0dcc852c755f8de5c824d0e9b3308b80ebd. 이전 정확 SHA에서 Windows357PASS, Ubuntu356PASS+1SKIP, Mac356PASS+1SKIP, Chrome Edge Chromium PASS, CodeQL PASS.
- 워크플로 수정 포함 SHA 12a9c433d7f4155fba6649f3064185feca696982: [합성 Preview workflow #43546219045](https://github.com/hibi89/data2web_studio/actions/runs/43546219045) 1/1 SUCCESS, [Windows/Linux Python+Browser #43546218953](https://github.com/hibi89/data2web_studio/actions/runs/43546218953) SUCCESS 4/4, [CodeQL #43546218944](https://github.com/hibi89/data2web_studio/actions/runs/43546218944) SUCCESS, [고정 점수 #43546219333](https://github.com/hibi89/data2web_studio/actions/runs/43546219333) SUCCESS. macOS 워크플로는 이 workflow-only SHA에서 트리거되지 않았고 소스 ed89a0dc의 Mac #43545781226 SUCCESS가 기능 검증 기준이다.
- GitHub artifact ID 14093583848, 이름 DATA2WEB-KMONG-SYNTHETIC-DEMO, 만료 2026-11-21 KST. 실제 다운로드한 ZIP 164,888 bytes, 9 entries, ZIP CRC PASS, 합성 GUI PNG 2장 PNG signature 확인, HTML script SHA256 CSP 정확 매칭, inline unsafe script 없음. 고객자료 및 토큰0.
- 임시 ZIP/PNG는 영구 공급 원본이 아니다. 승인된 배송물은 자체 로컬 생성/검증해야 한다.

## 명확한 인수 판정
전체 사용자 R01–R33 고정100점 기준 VERIFIED22=72/100, 11PENDING=28점. R06/07/21/23/25/26/27/29/30/32/33 법적권리/고객·독립 OS/보안/판매 심사 미완. 기술 CI와 합성시연만으로 100 달성/크몽 등록완료라고 표기하지 않는다. R29 무료 독립 자원검토 GitHub issue #5 OPEN/댓글0. User 2026-11-14 13:00 KST 별도 자동화의 폰/PC 작업으로 실제 소유자만 가능한 확인을 모아두었다. 0원; 공개 판매/실고객 납품 여전히 RELEASE HOLD/SALE NO-GO, 중앙 원장 [작업중] 보존.
