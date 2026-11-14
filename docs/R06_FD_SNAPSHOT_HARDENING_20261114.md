# DATA2WEB R06 원본·생성물 FD 스냅샷 보강 실행 증거 / 2026-11-14 KST

## 정본 목적과 선택
- 원래 R06: SHA256·경로·크기·원본 바이트 재확인. 사용자는 100점 전체 완료를 목표로 하지만, 현재 공식 인정점수72/100·R06 PENDING(2점) 유지. 개발/소유자 자기테스트는 독립 고객·외부 감사가 아니다.
- 방법A 채택: 기존 path_policy.read_bounded_source와 O_EXCL 출력기반에 통합. 파일 핸들의 타입·장치/inode·mtime·ctime·크기·실제 읽은 바이트를 전후 비교하고 최대크기 초과/경로 link·변조·경합은 HOLD; 비용0원, 추가 의존성0. 단점: Windows 고객이 통제하는 디렉터리에서 모든 TOCTOU 경합을 완전히 제거하는 증명은 아님.
- 방법B 미채택: 모든 파일을 Path.read_bytes()로 읽은 다음 SHA만 검사. 크기 무제한·경로 swap 윈도우가 남는다.
- 새로운 별도 파일스냅샷 서비스, 유료 도구, 서버, 고객 데이터 전송은 추가하지 않음.

## 실제 기능 수정 (새 SHA 기준)
1. studio.py XLSX --sheet 미지정 inspect: Path.stat -> Path.read_bytes 시트목록 대신 동일 파일의 8MB bounded FD snapshot. 목록·정확 sha·실제 시트 선택 안내 유지.
2. data2web.py 단일 HTML build: 20MB를 넘는 인코딩된 산출물은 출력 파일 생성 전 HOLD, 원본 SHA 재검증 후 생성 HTML도 20MB bounded FD로 재열람하여 작성 바이트 SHA 비교. 성공/실패 출력 재사용·자동삭제 없음.
3. data2web_append.py 다중파일 append build: 기존 원본 각각 개별 SHA 확인·결정적 HTML·ZIP 계약 보존, 생성 HTML 재검증은 Path.read_bytes() 대신 MAX_OUTPUT=20MB bounded FD snapshot.
4. test_xlsx_inspection_snapshot.py 신규 7회귀, test_output_snapshot_security.py 신규 5회귀: 실제 XLSX 목록 SHA, direct path read 금지, 과대파일 파싱 전 차단, 동일 크기 rename swap 차단, 변경·유효하지 않은 XLSX·누락 원본 HOLD, 단일/다중 HTML 출력 핸들 검증·변조·20MB 초과 무생성·원본 보존. 테스트는 합성만 사용.

## 검증된 GitHub 정확 SHA
- R06 XLSX 첫 구현 commit 80efc7f349be4db6ce7c2cb4b0b92b027090771a: Win 352PASS, Ubuntu351PASS+1SKIP, macOS351PASS+1SKIP; Python/browser #43545367042 SUCCESS; Mac #43545367062 SUCCESS; 미서명 native Win owner Preview #43545367017 SUCCESS; CodeQL #43545367094 SUCCESS; score #43545367252 SUCCESS. 원래 345개에서 7개 증가.
- R06 산출물 두 번째 구현 **기능 SHA ed89a0dcc852c755f8de5c824d0e9b3308b80ebd**: [Windows/Ubuntu Python+Browser #43545781220](https://github.com/hibi89/data2web_studio/actions/runs/43545781220) 4/4 SUCCESS, Windows 357/357 PASS, Ubuntu356PASS+1SKIP, Win Chrome/Edge와 Ubuntu Chromium real file URL; [macOS15 #43545781226](https://github.com/hibi89/data2web_studio/actions/runs/43545781226) SUCCESS 356PASS+1SKIP, Chromium offline; [CodeQL #43545781182](https://github.com/hibi89/data2web_studio/actions/runs/43545781182) SUCCESS; [고정 R01–R33 점수 #43545781503](https://github.com/hibi89/data2web_studio/actions/runs/43545781503) SUCCESS. 신규 총 12개 Win/Linux/macOS 테스트 합성 PASS.
- 코드서명된 고객EXE, 고객 소유 Win10/11 직접 최신 실험, 실고객 데이터/권리/외부 독립 보안감사는 미확인. CodeQL 워크플로 성공은 zero alerts 판정 아님. 유료 서버·API·라이선스·감사 사용 없음.

## 100% 달성까지 남은 외부 증거
- R06은 기술 보강되었으나 실제 Win10/11의 권한·경합, 외부 독립평가 미완으로 PENDING(2점).
- R07/R21/R25/R26/R27/R33: 실고객별 자료·개인정보 처리 권리/보관·파기, 실제 소프트웨어/제3자 저작권·NOTICE 및 크몽 계정·판매 조건 확인 필요. 자료를 GitHub·AI에 올리지 않음.
- R23/R30/R32: 실제 구매자/독립 고객의 Windows10/11·Mac/Linux 수용/포터블·배포 지원·라이선스 확인 필요.
- R29: GitHub 무료 외부 검토 요청 issue #5 OPEN, 댓글0/배정자0 (2026-11-14 확인). 독립 인간 감사/재검증 보고서 없음.
- R01–R33 100점 고정, **현재 VERIFIED22=72/100, PENDING11=28**, 100% 불인정, RELEASE HOLD/SALE NO-GO, 크몽 미등록·[작업중]. 시뮬레이션 성공을 실고객 성공으로 포장하지 않음.
