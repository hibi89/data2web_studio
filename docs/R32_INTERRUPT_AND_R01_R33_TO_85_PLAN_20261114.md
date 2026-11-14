# DATA2WEB Studio — Windows GUI Ctrl+C 중단 처리·85점 수용조건 재평가

**기준:** 2026-11-14 KST. 기존 고정 `R01–R33` 100점, 검증 22개 72점, 잔여 11개 28점, 목표85점까지13점. 고객 원본·프로덕션·상품판매 미변경.

## 구현 접근 비교
| 방안 | 성능·사용자 체감 | 비용·한도 | 유지보수 | 판정 |
|---|---|---|---|---|
| A. Python `studio.main(['desktop'])` 경계에서 `KeyboardInterrupt` 명시 처리 | 정상 GUI 유지, 콘솔 Ctrl+C 시 raw traceback 방지, 고정 JSON 및 exit 130 | stdlib, API/서버 비용0 | Python/zipapp/EXE 공통 경로의 작은 변경 | **적용** |
| B. Tkinter 이벤트·signal/asyncio 별도 래퍼 추가 | 플랫폼별 신호 및 GUI 디스패치 영향 | OS별 추가 실기기 시험 필요 | 고유 위험·복잡도 증가 | **미채택** |

### 실제 수정·테스트
- `studio.py`: `desktop_main()`에서 `KeyboardInterrupt`가 발생하면 `{"action":"desktop","sale_approved":false,"status":"INTERRUPTED"}` JSON을 출력하고 종료코드 **130**을 반환; 정상 GUI 닫기는 기존 **0** 유지. 고객자료/예외 메시지 노출 금지.
- `test_desktop_interrupt.py`: 중단 시 비민감/비성공 응답, 정상 닫기, 출시 승인 false 회귀 **3개** 추가.
- 최초 코드 SHA `0995e5824dea0c667ab13bc5fea191eca3ce705c`: [일반 Python/브라우저 CI #43531946750](https://github.com/hibi89/data2web_studio/actions/runs/43531946750) **4/4 SUCCESS**, Windows **294/294 PASS**, Ubuntu **293 PASS + Windows-only 1 SKIP**, Chrome/Edge/Chromium 실브라우저 E2E PASS. [정본 점수 게이트 #43531947120](https://github.com/hibi89/data2web_studio/actions/runs/43531947120) SUCCESS.
- 이 정확 SHA의 첫 [native EXE workflow #43531946776](https://github.com/hibi89/data2web_studio/actions/runs/43531946776)는 PyInstaller EXE 빌드 PASS였으나, Python 없는 환경에서 `self-check --browsers` 반환코드가 기대값0이 아니라 **FAIL**. 로그의 이전 진단기는 반환 상태를 기록하지 않아 **정확한 브라우저 실패 원인 미확인**. 제품 bug/Chrome 설치 오류로 단정하지 않음.
- 이어 `native_windows_acceptance.py`에서 **민감값/사용자 경로를 유출하지 않는 allowlist 기반 종료코드/브라우저 상태 진단**을 보강(SHA `4af5b70cd6340f334ed16f293b80d923688265bc`, 프로덕션 소스는 `0995e5824`와 동일). [다시 진행한 Windows native workflow #43532271904](https://github.com/hibi89/data2web_studio/actions/runs/43532271904) **1/1 SUCCESS**: native Python 없는 PATH→Chrome/Edge 합성 self-check, SHA PIN 합성 전달/verify·tamper/no-clobber, 실제 Tk 창 표시 및 정상 닫기 모두 PASS. 실패가 재현되지 않았으므로 **간헐성 원인은 미해결**, 후속 모니터링 조건.
- 새로운 unsigned 테스트 전용 EXE의 SHA256 `9e275ade3a250c663df6c77c2b1f40bd3146ddd353dd947e093a5ad75cb906e3`; private GitHub artifact `DATA2WEB-UNSIGNED-OWNER-PREVIEW-WINDOWS` ID `14087264349`, archive `sha256:749a24b95c95704add4f27c8ba79b6b06320eaadad4ab96bad83e12a9426d12d`; GitHub `2026-11-21T00:10:20Z` 만료(2026-11-21 09:10 KST). 바이너리 Git 리포지토리에 커밋하지 않음.
- 사용자 기존 Win11 Pro Build26200 native EXE `87d0d28222a052cd5c8f4da48922376ec72a604283b8021a775199f4fa0f4718`는 **구버전**이며 사용자가 직접 테스트한 합성 납품/무결성 PASS를 보존. 신규 빌드 `9e275ad`에 대한 사용자 실장비 검증은 아직 **미실시**; 새로운 코드 수정이 고객 Win11에서 확인됐다는 주장은 금지.

## 85점 최소외부수용 경로 — 고정배점 변조 금지
점수는 원래 승인된 33개 요구 중 **전체 수용조건이 충족된 항목에만** 준다. 아래는 **미래 계획/시나리오**이며 지금 취득한 점수가 아니다.

| 계획 | 신규로 완전히 충족해야 하는 요구 | 인정될 가능 가중치 | 달성 가능 점수 | 차단조건 |
|---|---|---:|---:|---|
| A. 계약·라이선스·개인정보·운영 정리 + 외부 보안감사 | R07(2)+R21(4)+R25(2)+R26(2)+R27(2)+R29(3) | 15 | 87/100 | 작성자/상용·제3자/LICENSE/NOTICE, 실제 자료 사용권·고객 개인정보 처리책임·보관/삭제, SKU/지원/환불, **외부 독립 XSS·CSP·XLSX·TOCTOU 보안 감사** 모두 승인·통과 필요 |
| B. 실기기·패키지/서명·외부 수용 중심 | R06(2)+R23(3)+R29(3)+R30(2)+R32(3) | 13 | 85/100 | Win10/11 및 macOS/Linux 실기기 수용, 외부 보안·권리 독립검증, 실행파일 서명/고객 수용·지원정책·패키징 증거 필요 |

- **기본 선택:** A가 하드웨어/코드서명 경로보다 외부 기기 범위가 좁고 기존 오프라인 HTML 납품형 운영안과 부합하지만, 사용자 계약/권리 승인과 독립 감사가 선행돼야 함. B는 현실 구현/외부 기기 접근·권리 비용 및 서명 이슈로 부담 높음.
- **이번 주기 실제 점수:** 72/100 유지(새 verified 항목0). 문서 작성·자가검수·기존 R24 중복 실증만으로 가중치 부여하지 않음. `[작업중]`·RELEASE HOLD/SALE NO-GO·Draft PR#4 유지.
- **사용자가 꼭 결정할 항목:** `docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md`의 실제 원본 취급·보존/파기·개인정보 처리 책임·가격/지원/환불 및 본인 코드/제3자 라이선스·NOTICE 승인. 합성 시험에 대한 체크는 실제 고객/상업 권리 승인과 완전히 다름. 외부 독립 보안감사 및 고객 인수·코드서명은 인프라/제3자 작업이며 사용자 허락 없이 유료 서비스 의뢰 금지.
- **다음 개발자 작업:** 정책 승인 뒤 적법한 LICENSE/NOTICE 납품 포함과 독립 검증기로 R21을 다시 테스트, 그리고 선택한 외부 감사 범위에서 R29의 실제 취약점 수정·재검증. 확인된 의사결정 없이 위험이 있는 상업 배포/권한 수정 금지.
