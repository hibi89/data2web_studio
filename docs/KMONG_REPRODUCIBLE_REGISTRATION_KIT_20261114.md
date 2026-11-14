> **LATEST 2026-11-14 KST — 크몽 공식 652×488 메인이미지 포함, 12파일 자동생성:** 이전 11파일 ZIP은 역사 버전임. [자동생성 #43552090412](https://github.com/hibi89/data2web_studio/actions/runs/43552090412) SUCCESS, 원본코드 SHA 5afd7726ac3556d2b44d3ae1ba51678cb9e53019, 직접 내려받은 12파일 ZIP SHA256 d224f0b5ce6237a951010679fc329e9f6311dc8ab8db9ce2b0e9f780b0fcada9, CRC/멤버 SHA PASS, 가상 데이터 PNG 652×488 정확 크기 확인. [근거](docs/KMONG_MAIN_IMAGE_652X488_EVIDENCE_20261114.md). Windows386PASS/Ubuntu385PASS+1SKIP, Chrome/Edge/Chromium/CodeQL/score SUCCESS. *이 데이터는 판매권/실고객 인수/독립감사를 대체하지 않음.* 사용자 최종목표100, 인정72/100·미수용28·크몽 미등록·RELEASE HOLD. 기존 13:00 KST 사용자 요청 한 번만, PC는 귀가 후.

# 2026-11-14 KST — Reproducible synthetic-only Kmong registration archive

## Purpose and tradeoff
The prior 10-file ChatGPT-only ZIP was verified but its container copy and GitHub's 7-day preview screenshots were not a repeatable single production route. For a weekend seller draft, this could require additional manual assembly just as the owner is away from their PC.

Chosen design: free existing GitHub Actions Ubuntu pipeline takes exactly the verified synthetic eight-row inventory, two **actual Chromium** captures and seven allowlisted registration documents and creates one deterministic, create-only ZIP (11 members with KIT_EVIDENCE.json). It checks source data, screenshot SHA/size, independently verified delivery ZIP, no false sale/audit claims, and exact source commit SHA. The second GitHub artifact exposes the ready-to-copy package for retrieval. Cost: KRW0, additional runtime dependencies0, normal public runner quotas apply.

Rejected alternative: manually reassemble ephemeral ChatGPT ZIP and repost screenshots after each change. It is harder to reproduce and trace to the tested code SHA. External hosted file services or paid storage would add cost/transfers and are not authorized.

## Artifacts and verified scope
- GitHub exact SHA a84f018ec2b4994390860b7f2f4488f88c84c1cf.
- Code: kmong_registration_kit.py, test_kmong_registration_kit.py and .github/workflows/kmong-synthetic-preview.yml. Six new synthetic regressions, including tampered screenshot, substituted original, missing capture, invalid SHA, no overwrite and same-byte rebuild.
- [Preview + registration kit CI #43551045748](https://github.com/hibi89/data2web_studio/actions/runs/43551045748): SUCCESS. Two GitHub artifacts: DATA2WEB-KMONG-SYNTHETIC-DEMO ID 14096810988 and DATA2WEB-KMONG-REGISTRATION-KIT ID 14096591307, both expire around 2026-11-21T03:21Z. GitHub artifact is downloadable from the run with repository access but is not an indefinite asset store.
- [Windows/Ubuntu Python+browser #43551045711](https://github.com/hibi89/data2web_studio/actions/runs/43551045711): 4/4 SUCCESS, Windows384PASS and Ubuntu383PASS/1SKIP, real Chrome Edge Chromium browser flows. [CodeQL #43551045695](https://github.com/hibi89/data2web_studio/actions/runs/43551045695) SUCCESS. [Fixed R01–33 score #43551045958](https://github.com/hibi89/data2web_studio/actions/runs/43551045958) SUCCESS.
- Unwrapped actual GitHub-produced registration ZIP downloaded to ChatGPT conversation path DATA2WEB-KMONG-REGISTRATION-READY-20261114.zip, 214297 bytes, exact SHA256 e7bd7818fb380e0f6886f4512e8c2a67e2ddb4af6f88f547c7f0856dbdce6dd3. 11 members, no duplicate names, all KIT_EVIDENCE.json SHA values equal source member bytes; ZIP CRC clean and two valid PNG signatures. Manifest pins exact commit and falsely claiming approval is forbidden. The conversation download needs owner local saving; **not** uploaded to Library or a permanent storage provider.
- Seven Markdown docs in the kit include title, FAQ, 3 SKU prices, owner checklist, rights/consent, security evidence. The nested delivery.zip contains only the eight fictional inventory items, never actual buyer records. The customer-data/sale/audit status is explicitly false.

## What the archive does NOT prove
- A file SHA and internal code identity is not independent publisher signing or proof of IP/third-party NOTICE rights.
- GitHub CI/CodeQL and the synthetic screenshot workflow are not independent human R29 security audits, real buyer Windows10/11/macOS acceptance or Kmong marketplace approval.
- A service draft does not equal a real submitted service. Owner must enter/verify PC web seller form, category, optional profile/settlement, thumbnail dimensions and real terms; submission requires explicit release and legal approval.
- Official 33-item user final goal =100; currently 22 VERIFIED =72/100 and 11 PENDING =28. [작업중], RELEASE HOLD, SALE NO-GO. No scoring or original customer files changed. No money spent.

## Reproduce from repository
Run from project root with Python3.11 and an existing real browser screenshot preview root:
1. python -m unittest test_kmong_registration_kit -v
2. python kmong_weekend_demo.py --output ./new-synthetic-demo
3. python kmong_preview_screenshot.py --root ./new-synthetic-demo
4. python kmong_registration_kit.py --preview ./new-synthetic-demo --output ./new-registration-kit.zip --source-sha <exact 40-character source commit SHA>
The screenshot step needs Playwright and Chromium locally; the GitHub workflow installs them in its free test runner. The command always requires a fresh unused ZIP filename, and the code does not accept arbitrary source record files in place of the eight fictional rows.
