# DATA2WEB — 최종설계 85% 목표 추가 보안/자체검증 근거 (2026-11-14 KST)

검증 소스 SHA 441506eda275b1e3766a4d018741ebfa1ae030b7, [Actions #43501097784](https://github.com/hibi89/data2web_studio/actions/runs/43501097784) 4/4 SUCCESS. Win/Ubuntu 각 249 PASS, Windows hosted Tk 실 CSV·XLSX GUI 클릭, native Chrome·Edge 및 Linux Chromium file://·원본 Lite golden PASS. 고객 실장비/사업적 승인과 구분한다.

## 선택한 두 설계
- A: Path.read_bytes 반복은 간단·런타임 의존0이나 파일 경로가 바뀌는 시점과 읽는 핸들 식별자를 묶기 어렵다.
- B(채택): bounded os.open 단일 파일핸들·fstat/lstat의 inode/device/mtime/ctime/size 확인 및 O_NOFOLLOW 가능 환경 적용. Python stdlib만 사용하고 원본 변경/경로 바꿔치기를 보수적으로 HOLD. 운영체제의 모든 경합 공격에 대한 완전 보장은 아니다.
- 고객 PC 검증은 별도 원격 서버 웹 앱보다 로컬 합성 CLI self-check 방식을 선택했다. 원격 서버·포트·업로드·유료 라이브러리 없이 같은 장비에서 Python으로 실행 가능하나 Python/Tk 설치가 필요하다.

## 재현과 한계
- python -m unittest discover -v : hosted Win/Ubuntu 각 249 PASS, 실패/skip 0.
- python desktop_ui_owner_flow_probe.py : hosted Windows Tk 실제 파일선택→CSV/XLSX 검수·시트 선택→열·SHA·권리/평문·PII 체크→새 고객폴더 HTML/ZIP/영수증 생성 및 독립검증 PASS. 고객 Windows10/11 직접 수용 아니다.
- python studio.py self-check --browsers : 내부 합성 소스로만 실행; Windows hosted 실제 설치 Chrome·Edge 2개 모두 PASS_SYNTHETIC_LOCAL_FILE, 전체 결과 PASS_SYNTHETIC_ONLY. 설치 누락·렌더불량은 PARTIAL_HOLD. 고객 원문/개인정보 및 디바이스 상세 경로 외부 전송·출력 없음.
- python browser_probe.py, browser_tabular_probe.py, browser_p85_probe.py, browser_single_delivery_probe.py, browser_final_blueprint_probe.py, browser_perf_probe.py, upstream_runtime_golden.py : 기존 Linux/Windows hosted file:// 경로 및 REA Lite 원본 공통 계약 PASS.
- 초기 append HTML 생성 결과 경로에 bounded input 읽기함수를 잘못 적용하여 10개 회귀 FAIL/ERROR → 출력은 html_path.read_bytes 복구; 다음 CI PASS. 초기에 네이티브 검증기가 존재하지 않는 span count를 찾아 Chrome/Edge HOLD → 실제 p#count role=status로 수정·정상/미렌더 부정 테스트 추가, 최신 CI 성공. 단순 재실행으로 실패를 숨기지 않았다.

**보류:** 소유자 가중치 R01~R33 합100, 고객 실 Win10/11 PC, macOS, 실업무 Excel, 개인정보·상용 재배포 권리, LICENSE/NOTICE, SKU 판매가격/지원/환불, 고객 인수·서명 EXE. 공식 완성률 UNASSESSED, [작업중] 및 RELEASE HOLD 유지.
