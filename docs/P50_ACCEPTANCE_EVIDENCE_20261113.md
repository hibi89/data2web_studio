# DATA2WEB — 사용자 최종설계 R01–R33 추적 · 2026-11-13 15:20 KST

**검증 코드 SHA:** `90da878ffa29926dda39f6c67913353ec7a3b390` · [GitHub Actions #43377913444](https://github.com/hibi89/data2web_studio/actions/runs/43377913444) · Python3.11 Windows/Ubuntu **97/97 각각 통과**, 실제 Linux Playwright Chromium `file://` **PASS**, 3/3 Jobs SUCCESS, 외부 HTTP(S) 요청0·JS 오류0.

**판정:** 2026-11-12 `docs/FINAL_DESIGN.md`가 지정한 **0→50 기술 단계의 CSV/JSON→오프라인 HTML→ZIP·독립 검사·브라우저 실제 경로** 구현·테스트를 완료했다. REA 원본 골든 전체 동등성은 **미검증**, 대표 계약 fixture만 확인했다. **사용자 최종설계 전체 R01–R33의 공식 완성률은 `UNASSESSED`** — 전체 100점 요구 가중치에 대한 사용자의 독립 승인·전수 기능 인수가 없어 임의로 50%라는 공식 값을 부여할 수 없다. 상품 중앙의 `[작업중]` 표식과 `RELEASE HOLD` 유지.

## 요구사항 추적 (전수, 33/33 식별; 가중치 미승인)

| ID | 사용자 최종설계 요구 | 상태 | 검증 코드/한계 |
|---|---|---|---|
| R01 | CSV UTF-8/BOM, 인용 필드 | 검증 | data2web.py / test_acceptance.py |
| R02 | JSON 평면 레코드 | 부분 | JSON 배열 지원; 객체형 레코드 추가 범위 미검증 |
| R03 | XLSX 안전/시트/수식 | 미구현 | feature/xlsx-tsv-import 후속 |
| R04 | TSV 인용/탭 | 미구현 | 후속 |
| R05 | 입력 파일·행·열·셀 상한 | 부분 | CSV/JSON·ZIP 상한 구현, 복잡 XLSX 미구현 |
| R06 | 원본 SHA256·변경 재검수 | 부분 | inspect/CLI hash gate·생성 전후 SHA, 경로 교체 경합 종단 미검증 |
| R07 | 원본 보존/소유권 승인 | 부분 | 자동 수정0·CLI 명시 ack, 실고객 사용권 대기 |
| R08 | 헤더·형 힌트·NULL/중복 preview | 부분 | 헤더·행수·SHA 노출, 통계/형식 진단 부족 |
| R09 | ID/제목/분류 명시 매핑 | 검증 | data2web.py / 승인 플래그와 중복 ID |
| R10 | 승인 영수증 모든 항목 고정 | 부분 | SHA·행수·컬럼·매핑 영수증, 서명/별도 수락 기록 없음 |
| R11 | 오류·변경시 HOLD | 부분 | 잘못된 CSV/JSON·SHA 변경·중복/초과 HOLD, 복잡 XLSX 없음 |
| R12 | XSS/공식셀/삽입 방어 | 부분 | HTML textContent·JSON script-escape, Excel/TSV 별도 미구현 |
| R13 | 복수 파일/append 승인 | 미구현 | 후속 2단계 |
| R14 | 서버 없는 HTML/CSS/JS | 검증 | data2web_web.py + file:// Chromium |
| R15 | 검색/분류/정렬/상세/페이지/반응형 | 검증 | Chromium 실 DOM UI PASS |
| R16 | 테마/제목/메타/인쇄 | 부분 | 3테마·제목 escaping·CSS print, 실제 한국어 인쇄 미검증 |
| R17 | 동일 헤더 CSV 교체/HTML 저장·재열기 | 검증 | 브라우저 명시 ack, 다운로드/새 파일 file:// 재열기 PASS |
| R18 | 표·차트/요약 지표 | 미구현 | 선택형 차트 후속 |
| R19 | 평문 포함 고지/동의 | 검증 | CLI --ack-plaintext, 브라우저 checkbox·문구 |
| R20 | 외부 요청0/CSP/계정0 | 검증 | 실 Chromium 요청 감시 HTTP(S)0·JS 오류0 |
| R21 | 결정적 ZIP/manifest/README/NOTICE | 부분 | ZIP 해시 바이트 반복동등·manifest·한국어 README; 라이선스 출고승인 대기 |
| R22 | 독립 verifier SHA/CRC/ZIP-slip | 검증 | verify_delivery.py / tamper·extra·compression·traversal 테스트 |
| R23 | Windows10/11 Chrome/Edge file:// | 부분 | Linux Chromium 통과, Windows runner Python만; 실 Windows 브라우저 미검증 |
| R24 | 새 경로·무덮어쓰기/복구 | 부분 | O_EXCL HTML/ZIP; 새 폴더 자동 워크플로 미구현 |
| R25 | 보유·삭제 금지 정책 | 부분 | 코드 자동 삭제0, 고객 안내·보유정책 미승인 |
| R26 | 개인정보 승인 분류 | 부분 | 평문 ack 구현, 민감정보 식별/규정 검수 미완료 |
| R27 | 크몽 SKU·지원·환불 승인 | 미구현 | 사용자 출고/영업 승인 필요 |
| R28 | 10k×20 성능 계측 | 미검증 | Python·브라우저 부하 수용 기준 미실시 |
| R29 | XSS/CSP/CSV/XLSX 보안 회귀 | 부분 | HTML 안전과 CSV 합성; XLSX 보안 미구현 |
| R30 | Win/Linux E2E·실 브라우저/패키지 | 부분 | Win/Ubuntu Python CI·Linux Chromium PASS, 구매자/Chrome·Edge 미검증 |
| R31 | 기존 Lite 완전 골든 동등 | 부분 | 기존 test_lite_builder.py 2건 fixture 계약 비교; 원본 런타임 직접 실행 안 함 |
| R32 | 재현 CI·패키징 | 부분 | Python3.11 stdlib runtime·97 테스트×2 + browser CI, 구매자 포터블 배포·서명 대기 |
| R33 | 상업 재배포·원본 사용권·실고객 | 미구현 | 명시 승인 전 RELEASE HOLD |

**중요:** `검증`은 명시된 기술 계약/합성 또는 실제 Chromium 테스트의 범위만 뜻한다. 실 고객·원본 소유권·물리 Windows·판매 GO가 아니다. 미검증을 0% 점수로 환산하거나 `부분`에 임의 가중치를 부여하지 않는다.

## P50 기술 실행 관문 증거
- **A1 원본 분리:** `hibi89/REA_Web`은 read-only 참조, 재사용 코드는 새 독립 구현. 참조 `REA_Web@feature/lite-owner-delivery-p95-20261112`, `tests/test_lite_builder.py`의 한국어 2행 합성 계약 fixture 비교. 실제 전체 원본 런타임 골든 재실행은 **미검증**.
- **A2 로컬 입력:** `python studio.py inspect` 셀 원문 없는 SHA/헤더/행수 → 동일 SHA를 `build --source-sha256 ... --confirm APPROVE --ack-plaintext`에 전달, 데이터 권리 확인 전 fail-closed.
- **A3 결과 HTML:** 검색/분류/정렬/상세/50행 페이징/3테마/출력 이름·프린트 CSS·반응형, 출력 평문 고지, CSP `connect-src 'none'`. 브라우저 검증은 **실 Chrome 계열 Chromium file://**.
- **A4 교체:** 동일 헤더·같은 순서 CSV만 명시적 local ACK → 교체 후 새 HTML 저장 → 다운로드한 `.html` 별도 재열기/검색. 브라우저 합성 악성 `</script>`/HTML 삽입은 비실행, 외부 HTTP(S)0.
- **A5 납품:** 결정적 create-only ZIP의 `index.html`, `manifest.json`, `README_KO.txt`; 별도 `verify_delivery.py` 허용목록/CRC/멤버 SHA/압축/경로 traversal/크기 거부; **디지털 서명·상업적 진위 보증은 아님**.
- **A6 CI:** `python -m unittest discover -v` **97 PASS×2 OS**, `python browser_probe.py` **PASS×1 Chromium**, run #43377913444 정확 SHA. 기존 Windows cp1252 오류·CRLF 바이트 SHA 문제, Playwright runner 버전·비동기/Eval CSP/다운로드 확장자 문제는 실행 로그 근거로 해결.

## 다음 필수 검증
원본 Lite real-runtime 전체 골든, XLSX/TSV 안전 import, 실제 고객 Win10/11 Chrome+Edge, 10k×20 성능 계측, 권리·라이선스·판매정책과 사용자 요구 항목별 가중치 확정. **이 자료만으로 공식 50% 또는 출시 가능 판단 금지.**
