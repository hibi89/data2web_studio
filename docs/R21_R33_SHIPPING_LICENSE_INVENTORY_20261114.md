# DATA2WEB Studio — 배포 자산·제3자 사용권 조사표 (R21/R33 준비)

**2026-11-14 KST GitHub 소스 조사 범위:** `hibi89/data2web_studio@feature/final-blueprint-p85-evidence-20261113` HEAD 기준, 직접 조회한 파일 `data2web_web.py`, `data2web_tabular.py`, `delivery.py`, `package_windows_bundle.py`, `upstream_runtime_golden.py`, `.github/workflows/python-tests.yml`, `docs/ORIGIN_AND_LICENSE.md`. 외부 권리자 직접 확인/법률감정은 **미완료**.

## 구분별 자산 재배포 경계
| 대상 | 확인된 기술 형태 | 고객 A 결과물 포함 여부 | 라이선스/권리 확정 여부 | 다음 증거 |
|---|---|---|---|---|
| DATA2WEB HTML 인라인 CSS/JS | `data2web_web.py` 내부 `TEMPLATE`의 self-contained CSS·JS; 외부 CDN 요청 지시 없음 | **예**, `index.html`에 포함 | 실제 저작권자·중간 출처 증빙 미확정 | source history/작업기록/자산 지적재산권자 승인 |
| 생성된 고객 데이터 | 고객 입력을 명시 승인 후 HTML에 **평문 포함** | **예** | 특정 고객의 자료 권리·개인정보 동의는 요청마다 별도 | 동의 기록 및 데이터 유형/삭제 책임 |
| 영수증·결정적 ZIP | `delivery.py`는 `index.html`, `manifest.json`, `README_KO.txt`만 ZIP 포함 | **예** | GUIDE 텍스트와 생성 스크립트에 관한 재배포권 검토 필요 | 승인된 `LICENSE/NOTICE`가 필요할 경우 추가 설계와 verifier 회귀 |
| 소유자 Windows 미서명 EXE | PyInstaller6.22.3 onedir / Python3.11+Tcl/Tk 포함, 로컬 GUI | **A에서는 아니오**, 후속 B에서만 후보 | Python/Tcl/Tk/PyInstaller·Bundled DLL 구성요소와 책임·서명 검증 미완 | 각 배포 파일의 origin/version/license 및 LICENSE/NOTICE 동봉/서명 검수 |
| XLSX/TSV parser | `data2web_tabular.py`에서 Python `zipfile`, `xml.etree.ElementTree` 등 stdlib 직접 파싱 | **아니오**, A 납품 HTML에 parser 번들 없음 | stdlib 런타임·비표준 라이브러리 포함 여부는 최종 inventory 재확인 | 소스 의존성 검토+SCA |
| 테스트 Playwright / pypdf | `.github/workflows/python-tests.yml`에서 `playwright==1.56.0`, `pypdf==5.9.0` 테스트 설치 | **아니오**, 현 `delivery.py` ZIP 멤버에 없음 | 테스트/CI 라이선스는 별도 검토 | 실제 런타임/패키징 SBOM 확인 |
| REA_Web 원본 | `upstream_runtime_golden.py`는 CI에서 SHA pin read-only upstream 실행 비교 | **코드 포함 없음**(정본 기록상); 복사했다고 결론 내리지 않음 | 원본과 새 코드의 유래/저작권 출처 확인은 필요 | 원본 기여/상업권리 chain 및 diff/영향 범위 기록 |

## 확인 사항과 금지
- GitHub 현재 브랜치 트리 목록에서 **루트 `LICENSE`, `NOTICE` 파일이 보이지 않음**. 이 사실이 곧 권리 부재나 침해를 뜻하지는 않지만, 승인 없이 임의 MIT/Apache/상용 라이선스를 생성하거나 오픈소스의 `NOTICE`를 생략할 수 없다.
- `delivery.py`의 정해진 ZIP 3개 파일·`verify_delivery.py`/고객 폴더의 허용멤버 목록은 **변경 전 승인·동시 수정·회귀**가 필요하다. 고객 출력에 임의 LICENSE 파일을 그냥 끼워 넣으면 기존 독립 검증기가 거절한다.
- GitHub PRIVATE/PUBLIC, 본인이 만든 코드라는 추정, Source SHA256, 테스트 PASS, PyInstaller가 무료라는 사실 중 어느 것도 고객용 상업 배포권의 독립 증거가 아니다.
- 진짜 IP/상표·제3자 저작물과 상업 배포 권한의 심사·책임은 실제 권리자 확인 필요. 고객의 실제 자료 제출/수신·개인정보 처리 권한도 별도 계약 조건이다.

## R21 승인 후 구현 경로 (아직 실행하지 않음)
1. 사용자/정당한 권리자가 서면으로 사용할 수 있는 라이선스 형태와 고객 이용범위, 제3자 `NOTICE` 필요 여부를 확정; License ID, 출처, 버전, 권리자, 재배포 규정, 허용되는 상업적 사용을 기록.
2. 결정적 ZIP은 **기존 3파일 동작을 보존**한다. 승인된 LICENSE/NOTICE가 실재로 필요하면 새 manifest contract·`verify_delivery.py`·`verify_customer_folder.py`의 allowlist/분류를 설계·마이그레이션 테스트로 동시 변경하고 기존 v1 고객 영수증 검증 유지.
3. 고객 데이터 없는 합성 fixture로 LICENSE/NOTICE 일치성, 멤버 변조/중복/누락, 서명/권리와 암호학적 SHA 검증 차이, 중도 실패 시 원본 무삭제를 CI와 실제 Windows에서 재검증.
4. 실제 승인된 권리문서의 법적 적합성, 통합 패키지 근거 확인 후 **그때만 R21 전체 수용 판정**. R21이 충족되어도 전체 release GO는 아님.

**현 상태:** 조사 일부 완료, 라이선스/권리 미확정. `R21=PENDING`, `R33=PENDING`, `SALE NO-GO`.
