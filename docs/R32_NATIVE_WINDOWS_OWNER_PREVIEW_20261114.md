# DATA2WEB Studio — 네이티브 Windows EXE 시범 빌드·독립 수용

**확인 일시:** 2026-11-14 KST / **정확 소스 SHA:** `96e2e1dff9976773bf3d3b2670ba6763ee69292d`. **검증된 것은 비공개·서명 없는 Windows hosted 러너 시범판이며 고객 OS/판매 적합성은 아니다.**

## 설계 A/B 비교와 B 시범판 채택
| 방식 | 실행 성능·사용성 | 비용/권리 | 유지보수·결론 |
|---|---|---|---|
| A: 기존 Python 3.11+ zipapp / CMD | 사용자의 Python/Tk 설치 필요; zipapp 빠르고 작은 파일 | 런타임 무료/stdlib, Windows 설치 부담 | 이전 안정 버전으로 유지 |
| B: PyInstaller 6.22.3 onedir EXE | Python/Tcl/Tk 번들, 사용자 PATH에 Python 필요 없음; EXE + `_internal` 폴더 | 빌드용 오픈소스 무료/빌드 시간·보안 검수 필요, **서명되지 않음** | **내부 시범 검증만**. 별도 고객 Win10/11·사용권·배포 인증 전 판매 금지 |

PyInstaller 공식 라이선스는 GPLv2 예외를 통해 상업용 실행파일 생성이 가능하다고 설명하나, **앱 본체와 동봉된 서드파티 라이선스 검토·권리자의 서면 승인·고객 사용허가는 별개**: https://www.pyinstaller.org/en/stable/license.html. 특정 라이선스 승인 없이 상업적 GO를 주장하지 않는다.

## 구현 내역
- `native_windows_entry.py`: 기존 `studio.main`을 그대로 호출하는 Windows EXE 진입점. 표형 데이터 원본을 자동 전송/삭제하지 않으며 기존 승인 Gate 유지.
- `native_windows_acceptance.py`: Windows 실제 EXE 프로세스로 순수 합성 CSV 생성·원본 SHA PIN → 고객폴더 `deliver` → 독립 `verify-customer`, 동일 폴더 재납품 거부, 영수증 변조 시 HOLD, Chrome·Edge `file://` 로컬 실행, 설치 Python 경로를 제외한 PATH 검사, 동일 프로세스 PID의 실제 Tk 최상위 창 표시와 정상 종료. **고객 입력은 일절 사용하지 않음**. 개인 PC/법률적 인증 등 미검증 필드를 명시 false로 남긴다.
- `.github/workflows/native-windows-owner-preview.yml`: `windows-latest`/Python3.11+테스트용 PyInstaller6.22.3(버전 고정), `--onedir --console --noupx`, 숨겨진 로컬 모듈 포함, 실행 자체를 통한 검증 후에만 비공개 GitHub Actions artifact 업로드(보존7일, 실제 고객자료 없음).
- `native-dist/DATA2WEB-LOCAL/DATA2WEB-LOCAL.exe`는 서명 없는 Windows runner 생성물. `PRIVATE_PREVIEW_MANIFEST.json`에 내부 파일 SHA256·크기·생성 소스 SHA·검증 범위 수록. GitHub 저장소에 바이너리/고객데이터는 커밋하지 않음.

## 정확 실행 증거와 장애
- **성공:** source `96e2e1dff9976773bf3d3b2670ba6763ee69292d`, [Windows EXE build+GUI+Browser+integrity run #43527161029](https://github.com/hibi89/data2web_studio/actions/runs/43527161029) **1/1 SUCCESS**.
- **검증 아카이브:** GitHub artifact `DATA2WEB-UNSIGNED-OWNER-PREVIEW-WINDOWS`, artifact ID `14085058847`, GitHub SHA256 `9b32286b4b777e25a50a85fb154ba73fc81bc8d6f357c7913b8cd73ebf968dc3`, 압축 12,423,815 bytes, 만료 **2026-11-21 08:27 KST**(GitHub 기록 UTC 2026-11-20 23:27). 이 아카이브/EXE는 **고객 배포 승인되지 않음**.
- **회귀:** [Python/브라우저 run #43527161036](https://github.com/hibi89/data2web_studio/actions/runs/43527161036) **4/4 SUCCESS**: Windows Python **291/291 PASS**, Ubuntu **290 PASS/1 Windows 전용 SKIP**, Windows Chrome/Edge 및 Ubuntu Chromium E2E PASS.
- **고정 평가:** [Final Blueprint gate #43527161439](https://github.com/hibi89/data2web_studio/actions/runs/43527161439) **SUCCESS**.
- **실패·복구 이력:** 최초 source `2ee4950475a34f8a2870b85ac3f67996ff346afe`의 시범 acceptance는 합성 CSV의 줄바꿈 escape 오류로 **FAIL**(native EXE build는 PASS). 수정 SHA `96e2e1df`에서 같은 test 경로 재실행→1/1 SUCCESS, 실패 기록·원본 보존. 실제 고객 기록이 유출된 것은 아님.
- **적용 범위 한계:** Windows GitHub-hosted 환경의 시범판. Win10/11 물리 고객 장비, Python·Tk 없는 실제 독립 PC 설치, SmartScreen/백신, macOS, 악성 파일 제3자 감사, Authenticode, 저작권/NOTICE 및 실제 구매·환불은 미검증.

## 최종설계 수용·실제 85점 경로
사용자 승인 `R01–R33=100점` 정본과 요구별 가중치 불변. **현행 검증 22개 72/100, 미검증 11개 28점, 85까지 13점**. R32 EXE 기술 근거 강화에도 **R32 3점은 PENDING**: real Win10/11·서명·지원/라이선스/고객 수용 조건 미완. R23(3), R21(4), R25(2), R27(2), R07(2), R26(2), R29(3), R30(2), R33(3)도 동일하게 실제 수용 충족 전 점수 미인정.

### 사용자/외부 수용이 필요한 최소 묶음 (승인 요청·자동 승인 아님)
1. **물리 Windows10/11에서 본 EXE 내부 시범판 실행**: Chrome/Edge 실 데이터 없는 자체검증, GUI 실행·한글/인쇄·합성 납품, 바이너리 SHA/SmartScreen 및 OS 확인 증거. 고객 원본 자동수집 금지.
2. **작성자·권리자 정책 결정**: DATA2WEB Python/HTML/JS 소유·제3자 NOTICE 검토/승인(R21), 입력물 계약상 사용권·민감정보/평문 동의와 보유·파기 책임(R07/R25/R26).
3. **판매 운영 별도 승인**: 이미 마련된 `COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md`의 SKU·서비스 범위/수정·지원·환불·배포권 확인(R27/R33); 크몽 실제 상품 게시·등록은 그 뒤 별도 허가. 실행 자체는 법률적 사용권 증거가 아님.
4. **외부 독립 수용**: 제3자 보안 침투/Windows 경합, 실제 고객 수용, 서명 또는 서명 불필요 배포 전략의 권리·법률 검토(R06/R23/R29/R30/R32/R33).

**판매와 공개배포는 보류:** `[작업중]` / RELEASE HOLD / SALE NO-GO. 목표85가 불가능한 경우 점수를 높여 보이게 만들거나 배점·요구를 축소하지 않는다. Production/Vercel 미적용.
