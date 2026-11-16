# DATA2WEB — 크몽 652×488 메인이미지 자동 생성 및 수용증거 (2026-11-14 KST)

## 설계 비교 및 채택
- 채택: 기존 8개 합성 CSV와 Chromium 브라우저 시연을 활용하여 HTML/CSS로 652×488 대표이미지를 자동 렌더링. 외부 디자인 자산, AI 이미지 API, 유료 폰트, 고객 자료 0.
- 미채택: 매 실행마다 사람이 이미지 편집 툴로 수동 제작. 사용자 PC 개입과 재현성 비용이 늘어남.

크몽 공식 규격 가이드 https://kmong.com/support/expert-center/posts/752 (2025-01-31): 메인이미지 652×488 픽셀 JPG/PNG, 유색 배경, 주요 문구 50px 이상 여백 권장; 가격·할인·최고·1위·연락처·크몽 공식 로고·제3자 무단 자산 금지. 메인 PNG는 청색 배경, 약 52px 여백, 합성 시연임을 명시하며 가격·과장문구를 포함하지 않음.

## 정확 코드 및 실행 증거
- 기능 SHA 5afd7726ac3556d2b44d3ae1ba51678cb9e53019.
- kmong_preview_screenshot.py: 1440×900 실제 합성 브라우저 화면 2장 후, 652×488 대표이미지 screenshots/03-kmong-main-652x488.png 추가 생성, 외부 요청 없음.
- kmong_registration_kit.py: 기존 11→**12멤버**(등록 원고 7, PNG 3, 합성 납품 ZIP 1, SHA 목록 JSON 1). 메인이미지 PNG IHDR 정확 크기 검사, 각 파일 SHA256/바이트 길이 및 합성원본 불변 체크.
- test_kmong_registration_kit.py: 대표이미지 652×488이 아닌 변조 파일은 재계산된 SHA를 갖고도 거부, 정상 12파일 패키지 수용 2개 신규 회귀 PASS.
- [Windows/Linux+browser #43552090456](https://github.com/hibi89/data2web_studio/actions/runs/43552090456) 4/4 SUCCESS Windows 386 PASS, Ubuntu 385 PASS/1 SKIP, Chrome/Edge/Chromium. [실제 PNG+ZIP #43552090412](https://github.com/hibi89/data2web_studio/actions/runs/43552090412) SUCCESS; CodeQL #43552090437 SUCCESS, 점수 게이트 #43552090619 SUCCESS.
- GitHub 생성 ZIP artifact 14096786765 (만료 예정 약 2026-11-21), ChatGPT에서 내려받아 CRC/12명/전체 멤버 해시 검증, SHA256 d224f0b5ce6237a951010679fc329e9f6311dc8ab8db9ce2b0e9f780b0fcada9, 371191바이트. 개별 메인 PNG 실제 652×488/154940바이트 확인. 이전 11파일 패키지는 과거 버전으로 보존.
- ChatGPT 파일 DATA2WEB-KMONG-REGISTRATION-12FILES-20261114.zip 및 DATA2WEB-KMONG-MAIN-652x488.png 는 **영구 Library/Drive/GitHub 업로드가 아님**; 형이 다운로드해야 영구 보관 가능.

## 수용/외부 차단
이 추가 작업은 상품 게시의 이미지 규격 문제를 줄였을 뿐, 외부 독립 R29 보안감사·실고객 소유/사용권·제3자 LICENSE/NOTICE·고객/구매자 OS 검증·크몽 계정 실제 등록을 완료시키지 않음. 공식 R01–33 72/100(22 VERIFIED, 11 PENDING28), 전체 목표100 미달, [작업중], RELEASE HOLD, SALE NO-GO. 현금 신규지출0, 고객자료 처리0.

## 13:00 일괄 사용자 작업
폰: 메인이미지/등록 설명 검토, 본인이 가진 권리 사실 확인, 크몽 인증/정산 상태 가능 범위에서 확인. PC(귀가 후): 크몽 웹 등록화면에서 카테고리와 서비스 필수 필드 확인, 652×488 이미지 등록·임시저장 준비. 실제 게시/권리 허가는 사전 독립 검증/사용자 승인 없이는 하지 않음. 이미 승인된 가격·무료 정책 재승인 요청 금지.
