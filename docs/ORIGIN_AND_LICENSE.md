# DATA2WEB Studio 출처·이관·권리 관리

## 원본/복구 정본
- 원형 저장소 `hibi89/REA_Web`, Lite 브랜치 `feature/lite-owner-delivery-p95-20261112`, 정확 기능 CI 기준 `cb7df1f4d1ce517c5940570af5bb1085410de268`.
- 원래 Pro `feature/d27-windows-python-discovery@97b6e5cab7b8ffb4e1ee7f5e593021f4dac2598d`. Fable source `import/fable51-bbe72c0@7e6f273b359b207fad8f92016226e3058cbcb839`, Astra P4 partial `import/astra-p4-b3166b6@f044b66e799289a5a353fdb9cbfdb324e683ffa3`.
- 원본 브랜치를 삭제·merge·force push·라이선스 지우기 금지. 신 저장소로 이관하는 파일마다 정확 blob SHA, 파일 변경, authored/third-party RIGHTS/LICENSE/NOTICE 대응, 테스트/판정 결과 기록.
- 현재 새 저장소로 코드·원본 파일 **미이관**. 실제 권리 증거 완비 전 고객 배포 HOLD.
- REA_Web의 기술 P95 성적은 원본 코드 범위에만 유효. DATA2WEB의 상업적 권리·골든 E2E를 자동 승인하지 않음.

## 이관 전 승인 체크
1. 원본과 현재 브랜치 원격 SHA 확인 및 원본 소스·검증기·템플릿 파일 목록 정리.
2. Pro/MVP 종속성 중 권한 있는 코드만 독립형으로 추출하거나 출처 확인 후 재구성. PyPI/Node/XLSX parser 포함 모든 NOTICE·직접/전이 라이선스 인벤토리.
3. 인풋/아웃풋/테스트의 사용자·고객·민감 데이터 없는 합성 fixture 사용.
4. 동일 XLSX/TSV/CSV/JSON 합성 goldens, 원본 변조·출력 중단·Win/Ubuntu real browser를 검증.
5. 실제 고객·사용권·상업가격·제공방법 승인되기 전 RELEASE HOLD.

## 권리 불확실성
- 원본 코드의 정확한 작성·저작권/상용권리, 제3자 라이선스/NOTICE, 엑셀 파서의 권리는 **미승인**.
- 단순 GitHub PRIVATE 설정이나 코드 SHA/CI SUCCESS가 법적 사용권을 증명하지 않는다.

## 2026-11-13 실제 원본 동등성 테스트 참고 (상업적 이관 아님)
- 원본 공개 `hibi89/REA_Web` 브랜치 HEAD `7b6b68111efd906f9d929b5e2f577699b26399ee`를 DATA2WEB CI Ubuntu runner에 `actions/checkout` `persist-credentials:false`로 **일시 읽기 전용 checkout**. 다음 단계에서 GitHub 작업 디렉터리만 삭제되며, upstream 원본 브랜치/소스 수정0, 신규 DATA2WEB Git 트리에 upstream source blob/원본 템플릿 추가0.
- 새 독립 비교 스크립트 `upstream_runtime_golden.py`는 원본 `rea.mvp`/ `rea.lite_builder` **실제 Python CLI**와 원본 Lite HTML `file://` 렌더를 구동; DATA2WEB 결과와 공통 CSV/JSON 의미 동등 및 업데이트/재저장·수치/테마/오류를 검사. `d311c47f1b85382f1d4ce43dfacdabcdc7e85612` [CI #43392272159](https://github.com/hibi89/data2web_studio/actions/runs/43392272159) PASS.
- 원본 라이선스/상업적 재배포권이 승인됐다는 뜻이 아님; 원본 소스는 고객 상품에 포함/판매하지 않음. 새로 만든 standalone Python/CSS/JS의 상업적 라이선스/고객 약관도 미승인, RELEASE HOLD. 원본 프로젝트의 SHA·공개 상태가 향후 달라지면 본 검증은 **위 핀 커밋 한정**.
