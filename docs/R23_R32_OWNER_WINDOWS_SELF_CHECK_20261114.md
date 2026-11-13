# DATA2WEB Studio — 소유자 Windows 로컬 EXE 합성 검증 증거

**2026-11-14 KST · 최초 사용자 제공 PowerShell 콘솔 출력의 수용 범위 기록 · 상업 출시 승인 아님**

## 범위·증거의 출처
- **출처:** 소유자가 대화에서 직접 전달한 Windows PowerShell 5.1 실행 결과. 테스트 원본은 자신의 Windows PC에서 실행한 것으로 보고됨; GitHub Actions hosted Windows 로그와는 **별개**의 사용자 제공 근거.
- **실행명령:** `DATA2WEB-LOCAL.exe self-check --browsers` (현재 폴더의 EXE). 소유자 이름·계정명·PC 경로 등 개인정보는 이 문서와 저장소에 기록하지 않음.
- **콘솔이 확인한 필드:**
  - `status = PASS_SYNTHETIC_ONLY`
  - `browser_check_requested = true`
  - `browser_results.chrome = PASS_SYNTHETIC_LOCAL_FILE`
  - `browser_results.edge = PASS_SYNTHETIC_LOCAL_FILE`
  - `local_folder_verified = true`
  - `platform_family = Windows`
  - `sample_type = GENERATED_SYNTHETIC_NOT_CUSTOMER_INPUT`
  - `data_egress_required = false`
  - `customer_source_inspected = false`
  - `customer_rights_approved = false`
  - `commercial_release_approved = false`
- **판정:** 소유자 컴퓨터에서 EXE가 실행되고 Chrome·Edge 및 합성 로컬 폴더 검사가 통과했다는 **사용자 제공 실PC 스모크 증거 1건**. Python 독립 EXE 실운용 가능성에 긍정적이지만, OS 세부 버전·실 고객 납품·권리·서명/보안 검증을 대체하지 않음.

## 정확 산출물 매칭 미확인
- GitHub Windows test [native run #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029)에서 `source SHA=96e2e1dff9976773bf3d3b2670ba6763ee69292d`, `DATA2WEB-LOCAL.exe SHA256=87d0d28222a052cd5c8f4da48922376ec72a604283b8021a775199f4fa0f4718` 확인. Artifact `DATA2WEB-UNSIGNED-OWNER-PREVIEW-WINDOWS` ID `14085058847`, archive digest `9b32286b4b777e25a50a85fb154ba73fc81bc8d6f357c7913b8cd73ebf968dc3`.
- **소유자 실행 바이너리의 해시값은 아직 제시되지 않아 코드·EXE 정본과 암호학적 동일성 미검증.**
- `Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber` 출력도 없으므로 Windows 10/11 정확 버전은 **미확인**. PowerShell 5.1과 `platform_family:Windows`만 관찰됨.

## 다음 사용자 1회 최소 검증
기존 PowerShell 명령 위치에서 다음 두 명령을 실행 후, **OS명·빌드번호와 EXE SHA256 해시만** 회신:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber
(Get-FileHash .\DATA2WEB-LOCAL.exe -Algorithm SHA256).Hash
```
여전히 실 사용자 권리/계약/서명 검증은 별개이며, OS·SHA가 일치해도 R23/R32 전체 기준의 macOS/고객 독립 인수/법적 사용권·지원 범위를 자동 충족하지는 않음.

## 공식 100점 평가와 한계
- 고정 R01–R33 **72점 VERIFIED (22개)**, **28점 PENDING (11개)**, 목표85에 13점 부족. `R23`과 `R32`의 실제 사용자 컴퓨터에 대한 기술적 근거는 늘어났지만, 나머지 수용 요구가 모두 완료된 것은 아니므로 **점수 변경 없음**.
- `[작업중]` / `RELEASE HOLD` / `SALE NO-GO` / 고객 자료 수집0 / 외부 업로드0. 사용자 제공 로그에 원본 파일 데이터는 없음; 기밀 정보·개인 경로를 GitHub에 커밋하지 않음.
- GitHub 데이터2웹 기능·정본 점수표·기존 고객 원본 변경 없음. Vercel/Production 미적용.
