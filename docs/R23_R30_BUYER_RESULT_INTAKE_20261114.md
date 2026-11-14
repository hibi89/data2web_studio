
# DATA2WEB R23/R30 external buyer self-report intake — 2026-11-14 KST

## Purpose and comparison
User final 33-requirement goal = 100 points. Current official frozen score = 72/100, 22 VERIFIED, 11 PENDING 28. Existing GitHub CI and a generated real-device test REQUEST are not independent buyer acceptance.

Chosen zero-cash path: verify a manually edited, local real-device test form against the exact original synthetic test-request ZIP and Git SHA, using Python3.11 stdlib and a fixed report contract. Input is never uploaded; stdout returns only a bounded classification and SHA256. A completed PASS self-report is a human-review *candidate*, NOT an independently authenticated result.

Alternative: automatically mark PASS submissions as independent acceptance. Rejected: author/user could simply edit JSON; no reviewer identity, actual device proof, or third-party audit can be inferred. Alternative paid reviewer/device farm remains unapproved and was not engaged.

## Code and evidence
- buyer_self_report_intake.py: validates exact schema from original REVIEW_FORM_BLANK.json, rejects extra identifying keys, strings in boolean flags, absent steps, unsupported OS/browser syntax, contradictory aggregate/step PASS/FAIL/NOT_RUN, false run or false independence, and any attempted sale, 100-point, source rights or independent security certification.
- All buyer-report states remain: HOLD_INCOMPLETE_DEVICE_TEST, HOLD_OBSERVED_FAILURE, HOLD_NOT_INDEPENDENT, or CANDIDATE_FOR_EXTERNAL_HUMAN_REVIEW_ONLY. For every state, report_is_authenticated=false, external_human_verified=false, buyer_acceptance_verified=false, sale_approved=false and score_added=0.
- Uses one bounded snapshot for the completed report file: both schema validation and report_sha256 are derived from exactly the same bytes, avoiding a second-open race.
- No customer contents, personal IDs, names, emails, device identifiers, IP or outgoing HTTP/S requests. Actual buyer evidence must be collected under authorized agreement and provenance checked by a human.
- Source code SHA dc12a9483a0e595bef31f31cc898a854adc95ba4 first added 10 synthetic negative/positive tests. SHA 377c6f5ae28c3f1d18ee0738045cfb80f95ee7ea added one single-snapshot regression.
- [Windows/Linux and actual browser CI #43554270079](https://github.com/hibi89/data2web_studio/actions/runs/43554270079) **4/4 SUCCESS**, Windows403 PASS, Ubuntu402 PASS/1 SKIP, Chrome Edge Chromium real offline test suite. [CodeQL #43554270040](https://github.com/hibi89/data2web_studio/actions/runs/43554270040) SUCCESS; [frozen score #43554270238](https://github.com/hibi89/data2web_studio/actions/runs/43554270238) SUCCESS.
- No actual independent buyer has returned any completed report; no independent R29 security audit. A claimed pass is not a legally/cryptographically signed attestation. Real customer/source/IP rights are separately pending. This work does NOT raise final R23 or R30 score.

## Usage when and only when authorized human result arrives
1. From exact immutable synthetic original request ZIP and newly received local test result JSON, run: python buyer_self_report_intake.py --request-zip <local-request.zip> --result-json <manual-review.json>. Do not place either file in a public repo; both must be tested in a local controlled path. Only synthetic request content is allowed.
2. A reviewer marks seven PASS/FAIL/NOT_RUN steps and reports real OS as Windows 10, Windows 11, macOS, or Linux, browser as Chrome/Edge/Chromium with numeric version. No names, identifiers or actual client data are collected.
3. A candidate status MUST be independently verified by the actual right-holder/reviewer process; failure or incomplete status remains HOLD. Any new code SHA requires new independent evidence. No automatic score, sale GO, registration or PII collection.
4. No automatic file deletion; original reviewer report and submitted request path unchanged. Extra spending 0 KRW.

## Platform and 13:00 owner work
Seller registration kit with 652x488 main thumbnail and three owner-internal SKU prices remains ready. Kmong actual PC web form, owner rights/NOTICE, independent R29 and actual buyer OS acceptance remain external blockers.
2026-11-14 13:00 KST: DATA2WEB standalone task was DISABLED due 5-active-task cap, while existing general '오후 1시 사용자 작업 통합' task is active and already includes generic DATA2WEB. A direct 13:00 owner action summary was delivered in conversation. Never claim the disabled standalone automation fired or that updating an already-past 13:00 schedule succeeded.
Actual PC work deferred to return after 5h+ outside, phone owner IP and seller status only.
