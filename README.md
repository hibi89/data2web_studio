# DATA2WEB Studio

CSV/flat JSON 파일을 **고객의 컴퓨터에서 직접** 검수한 뒤 독립 실행형 오프라인 HTML과 무결성 검증 ZIP으로 변환하는 도구입니다. 기존 REA_Web의 웹사이트 분석 기능과 별개입니다. 고객 데이터 업로드·계정·API·서버가 없습니다.

> **2026-11-13 상태:** CSV/JSON 기술 P50 핵심 경로 자동 검증 완료([97×2 Python + Chromium `file://` PASS](https://github.com/hibi89/data2web_studio/actions/runs/43377913444), 소스 `90da878ffa29926dda39f6c67913353ec7a3b390`). XLSX/TSV·상용 권리·실고객 Windows 검증은 미구현/미검증. 사용자 최종설계 기준 공식 완성률은 **UNASSESSED**, RELEASE HOLD.

## 실행 (Python 3.11+, 판매자 컴퓨터)

```bash
# 먼저 헤더·행수·SHA 확인. 실제 셀 값은 stdout에 표시되지 않습니다.
python studio.py inspect sample.csv

# 출력된 SHA와 실제 소유권/평문 포함 여부를 검토한 다음 승인
python studio.py build sample.csv output.html \
  --source-sha256 <검수한 SHA256> --id id --title title --category category \
  --confirm APPROVE --ack-plaintext --theme office --name "내 목록" \
  --zip-path output.zip

# 독립 ZIP 허용 목록/CRC/SHA/크기 검증
python studio.py verify output.zip
```

새 HTML은 Chrome/Edge에서 네트워크 없이 열 수 있습니다. 검색·분류·정렬·상세·페이지와 3개 테마가 제공됩니다. 로컬 CSV 교체는 정확히 같은 헤더/순서와 명시적 평문 승인만 허용하며, **새 HTML 다운로드 후 다시 열어야** 반영됩니다. 기존 출력·원본은 자동 삭제하거나 덮어쓰지 않습니다. 변경·백업된 HTML 모두 **자료 평문 포함**이므로 안전한 파일 취급이 필요합니다.

## 개발 검증

```bash
python -m unittest discover -v
# 브라우저 추가 테스트에만: pip install playwright==1.56.0 && python -m playwright install chromium
python browser_probe.py
```

## 범위·제약
- 구현: CSV UTF-8/UTF-8 BOM, flat JSON 배열, 제한된 셀/컬럼/행/파일 크기, 입력 SHA, ID 중복 검사, HTML XSS 안전 이스케이프, 사용자 필드 매핑, 서버 없는 로컬 뷰어, create-only ZIP·독립 무결성 확인.
- **아직 미구현:** XLSX/TSV, 차트·고객 폴더 패키징/라이선스 안내의 최종 사용승인, 원본 Lite 직접 동등성 재현, 10k×20 성능 인수, 실제 구매자 Windows10/11 Chrome/Edge 검수, 데이터 사용권/판매 승인.
- SHA/CRC는 전송 손상 검출이지 암호학적 배포자 신원 보증·서명이 아닙니다. 다운로드/생성 HTML에 고객 데이터가 평문 포함됩니다.
- 기획·최종설계 [REQUIREMENTS.md](REQUIREMENTS.md), [docs/FINAL_DESIGN.md](docs/FINAL_DESIGN.md), 실제 검증 [docs/P50_ACCEPTANCE_EVIDENCE_20261113.md](docs/P50_ACCEPTANCE_EVIDENCE_20261113.md), 인수 [HANDOFF.md](HANDOFF.md). 원본 REA_Web은 변경하지 않았습니다.
