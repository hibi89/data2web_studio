# DATA2WEB Studio — 오프라인 XLSX / TSV / CSV / JSON 웹앱 생성기

**CSV·평면 JSON·TSV·보수적 Excel `.xlsx` 값 파일**을 사용자 PC에서 명시적 검수 후 독립 검색/분류/정렬/상세 HTML과 검증 ZIP으로 전환. 기존 REA_Web 웹사이트 분석 제품과 무관하며 원본 데이터를 서버/AI로 전송하지 않습니다. Python 3.11+ 기본 모듈만 사용하며 인터넷·계정·결제·데이터베이스 불필요.

> **2026-11-13 P85 검증:** [Windows145/145, Ubuntu145/145, Windows Google Chrome·Microsoft Edge, Ubuntu Chromium `file://` 전 경로 PASS(총 4/4 CI jobs)](https://github.com/hibi89/data2web_studio/actions/runs/43385035408), 정확 기능 SHA `709b2e5d5540893b9f7ad1b391584c6400899672`. **기술 85% 단계 검증**, 최종설계 전체 **공식 완성률 UNASSESSED**, 판매/납품 **RELEASE HOLD**. 고객 실제 Win10/11과 라이선스는 미검증.

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

## 새 85% 기술 단계: 오프라인 차트·KPI·Chrome/Edge

- 원본 승인 데이터의 **전체 건수·표시 건수·고유 분류**를 표시하고, 현재 검색·필터 기준 **범주별 막대 차트**(최대 상위9+기타)를 그립니다. 지원 가능한 비음수 숫자열은 선택형 브라우저 **근사 산술합**으로 집계합니다. 단위·회계/재무 의미를 자동 확정하지 않습니다.
- 별도 라이브러리/서버/외부 폰트 없이 반응형·인쇄용 CSS로 작동하며, HTML·CSV의 스크립트처럼 보이는 내용은 실행하지 않고 문자로 렌더링합니다.
- 브라우저에서 동일 헤더 CSV를 새로 가져와 HTML을 저장하면 **기존 원본 SHA 및 XLSX 시트/수식 캐시 승인 메타는 지워지고, 새 데이터는 검증 전 상태로 표시됩니다.** 이전 ZIP 무결성 증거를 새 파일에 재사용하지 마십시오.
- 실제 GitHub hosted **Windows Server 2025의 Chrome/Edge**에서 앱·XLSX/TSV·ZIP/내보내기·재열기 E2E PASS; **개인/고객 Windows10/11 검증은 여전히 미완료**.
- 10,000×20 합성 행 CI 시연: 빌드 0.784s, Python 메모리 peak 31.85MiB, Linux Chromium 초기 0.256s·검색 0.027s·정렬 0.154s (**CI 1회 표본이며 고객 사용 성능 보증 아님**). 상세 [P85 수용 근거](docs/P85_UI_CROSSBROWSER_ACCEPTANCE_20261113.md).

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
python browser_p85_probe.py --channel chromium
python browser_perf_probe.py
# Windows 브라우저 검증 환경(Playwright Python 설치 후):
python browser_p85_probe.py --channel chrome
python browser_p85_probe.py --channel msedge
python browser_tabular_probe.py --channel chrome
python browser_tabular_probe.py --channel msedge
```

정본: [REQUIREMENTS.md](REQUIREMENTS.md), [docs/FINAL_DESIGN.md](docs/FINAL_DESIGN.md). 정확 검증 [P70 증거](docs/P70_XLSX_TSV_ACCEPTANCE_20261113.md), 현재 상태 [STATUS.md](STATUS.md), 인수인계 [HANDOFF.md](HANDOFF.md). 출고 금지 `RELEASE HOLD`.
