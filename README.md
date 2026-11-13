# DATA2WEB Studio — 오프라인 XLSX / TSV / CSV / JSON 웹앱 생성기

**CSV·평면 JSON·TSV·보수적 Excel `.xlsx` 값 파일**을 사용자 PC에서 명시적 검수 후 독립 검색/분류/정렬/상세 HTML과 검증 ZIP으로 전환. 기존 REA_Web 웹사이트 분석 제품과 무관하며 원본 데이터를 서버/AI로 전송하지 않습니다. Python 3.11+ 기본 모듈만 사용하며 인터넷·계정·결제·데이터베이스 불필요.

> **2026-11-13:** 기술 단계 P70 구현/검증([Windows145/145, Ubuntu145/145, Linux Chromium CSV·XLSX·TSV `file://` PASS](https://github.com/hibi89/data2web_studio/actions/runs/43381537805), 정확 코드 `42b832c5e18521d3edcf53b69cbf92c272f245cb`). 최종설계 전체의 공식 완성률은 **UNASSESSED**, 상업적 판매/납품 **RELEASE HOLD**.

## XLSX inspect → 시트 명시 승인 → build

```bash
python studio.py inspect workbook.xlsx
# status XLSX_SHEETS_REQUIRE_EXPLICIT_SELECTION, sheets + source_sha256
python studio.py inspect workbook.xlsx --sheet "Inventory" --header-row 1
python studio.py build workbook.xlsx new.html --source-sha256 <INSPECT의 실제 SHA256> \
  --sheet "Inventory" --header-row 1 \
  --id id --title title --category category \
  --confirm APPROVE --ack-plaintext --theme office --zip-path new.zip
python studio.py verify new.zip
```

셀 수식이 있는 경우 **기본 거절(HOLD)**. 캐시값을 사용해도 되는 소유자만 **inspect와 build 양쪽**에 `--allow-cached-formulas`를 별도 명시할 수 있습니다. 캐시가 없는 수식은 항상 거절하며 **Excel 수식/날짜 표시형식은 재계산·재현하지 않습니다**. 출력 HTML은 고객자료 **평문 포함**입니다.

## CSV/JSON/TSV

```bash
python studio.py inspect data.tsv
python studio.py build data.tsv app.html --source-sha256 <INSPECT의 실제 SHA256> \
  --id id --title title --category category \
  --confirm APPROVE --ack-plaintext --zip-path delivery.zip
```

CSV·JSON도 동일 명령에서 입력 확장자만 변경합니다. 새 HTML과 ZIP은 기존 경로를 **절대 덮어쓰지 않습니다**. HTML에는 3테마, 로컬 검색·카테고리·정렬·상세·페이징, **동일 헤더 CSV**의 사용자 동의 후 새 HTML 생성 기능이 포함됩니다. 생성·재저장 파일의 평문 포함과 공유 위험을 인지해야 합니다.

## 지원 XLSX 보안 범위와 한계

- **지원:** `.xlsx` Open XML 기본 시트, inline/shared strings, 숫자 원시 문자열, Boolean, 헤더 1–50행, 시트명 명시 선택, 최대 10,000 데이터행·40열·16,000자/셀, SHA256 핀·ZIP CRC/압축비·외부 요청 방지.
- **거절:** 매크로/XLSM, OLE/임베디드 첨부, 외부 관계/하이퍼링크, DTD/ENTITY, 관계 경로 위조, 압축 폭탄, 중복 ZIP·열·헤더, 병합 셀, 숨김 시트, 미지원 OOXML 파트, Excel error, 수식 캐시 누락/명시 승인 없음. 서식·수식 계산·날짜 변환·연결/동적 배열은 완전 호환되지 않습니다.
- **실행 비용:** Python stdlib 0 추가 패키지/원격 API 비용0, 검증 CI에만 Playwright Chromium 별도 설치.
- **아직 미검증:** 실제 고객 Microsoft Excel·LibreOffice의 다양한 확장 포맷, 물리 Windows10/11 Edge·Chrome, 큰 데이터 10k×20 성능/원본 Lite real-runtime, 권리·라이선스·상용 판매 승인.

## 개발 검증
```bash
python -m unittest discover -v
# 브라우저 테스트 전용: pip install playwright==1.56.0; python -m playwright install chromium
python browser_probe.py
python browser_tabular_probe.py
```

정본: [REQUIREMENTS.md](REQUIREMENTS.md), [docs/FINAL_DESIGN.md](docs/FINAL_DESIGN.md). 정확 검증 [P70 증거](docs/P70_XLSX_TSV_ACCEPTANCE_20261113.md), 현재 상태 [STATUS.md](STATUS.md), 인수인계 [HANDOFF.md](HANDOFF.md). 출고 금지 `RELEASE HOLD`.
