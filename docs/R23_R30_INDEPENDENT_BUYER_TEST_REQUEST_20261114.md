
# DATA2WEB independent real-device buyer test REQUEST (2026-11-14 KST)

## Goal and design choice
Full R01–R33 target is 100 points. Official verified 72/100 and 11 PENDING=28. Developer-run GitHub CI and CodeQL never substitute for independent actual buyer devices, human R29 auditor, owner IP rights, or customer data consent.

Approach A: ask owner to repeat Windows self-check or rely on hosted CI. Rejected: cannot prove independent buyer acceptance and wastes owner PC time.
Approach B (chosen): a separate, reproducible, create-only, 7-file synthetic-only ZIP that a real independent buyer tester can use without the builder or installing Python, with original verified HTML+delivery.zip+receipt, fake eight-row CSV, Korean instructions, blank test form and all member hashes. Public synthetic content only, no extra cash or paid services.

## Implemented and verified
- Code modules: kmong_independent_buyer_request.py, test_kmong_independent_buyer_request.py, .github/workflows/kmong-synthetic-preview.yml. Exact source SHA de9d629087407f16364cee35e0d7a645fe797815.
- Blank REVIEW_FORM_BLANK.json: OS/browser tasks ALL NOT_RUN; buyer_accepted, actual_real_device_run, reviewer_independent_of_development, sale_approved, independent human audit, rights verified are all FALSE. No accepted result is generated.
- Test cases (6): valid synthetic request, exact reproducibility, no overwrite, source replacement HOLD, forged sale flag HOLD, malformed SHA/preapproved test form HOLD.
- Windows and Ubuntu plus actual browser CI #43553284509: 4/4 SUCCESS, Windows392PASS, Ubuntu391PASS+1SKIP; Chrome Edge Chromium real file://. Synthetic package and reviewer request #43553284548 SUCCESS; CodeQL #43553284624 SUCCESS; score #43553284865 SUCCESS.
- Actual GitHub artifact DATA2WEB-SYNTHETIC-INDEPENDENT-BUYER-TEST-REQUEST ID 14096768471 downloaded and unwrapped into ChatGPT file DATA2WEB-INDEPENDENT-BUYER-TEST-REQUEST-20261114.zip. 46,739 bytes, sha256 a33b35e551e1329b5d232e051992d46948e2da52331ab3841e3fcca7462438ce. Zip CRC clean, 7 members, exact manifest SHA match, 8 fake rows + one header, no customer data or human acceptance. Artifact expires ~2026-11-21; chat download not permanent Library backup.

## Independent acceptance procedure
1. Authorized outside reviewer on actual Win10/11, Mac or Linux saves and extracts synthetic package in a new folder. No real customer data/identifiers/accounts needed. Any external distribution/communication follows owner approval.
2. Human opens index.html in installed Chrome/Edge offline, tests search for 가상 노트 yielding one row, filter/sort/details, print, offline request/error scope, and optionally compares included receipt/zip.
3. Human records genuine OS/browser version, PASS/FAIL/NOT_RUN and reproduction details in a separate report. Technical author/CI cannot authenticate those facts; owner/human reviewer must verify provenance. Any fail blocks acceptance and demands remediation plus independent re-run on exact new SHA.
4. Real customer use rights, legal license and separate independent R29 security audit are still missing. The request alone gives R23/R30/R29 zero new score. No scorecard reweighting or SALE GO.

## User action batching
User away more than five hours. Existing one-time 13:00 KST task Automation_fb2b044b906c8191a2b2adbf69add50e: phone checks owner rights/expert profile where supported, PC service edit/thumbnail/category only after returning. No repeated synthetic Windows tests, reapproval of free SKU, paid auditor or actual private source upload. Full official score 72/100, [작업중] RELEASE HOLD SALE NO-GO, actual Kmong seller listing not submitted.
