# DATA2WEB - zero-cost anonymous scope gate and macOS evidence / 2026-11-14 KST

## What actually changed
- Anonymous pre-order scope triage: order_intake_preflight.py, test_order_intake_preflight.py (12 tests), data/kmong_anonymous_request_example.json, docs/KMONG_LOCAL_PREORDER_TRIAGE_20261114.md.
- A locally evaluated tentative seller SKU scope, not customer onboarding or legal consent. Only enum file formats, integer counts and boolean declarations. Never open source data or accept names/paths/custom free-text; on error HOLD, sale_approved false. Auto-upload, network service and paid tools not used. Only suggest owner-approved BASIC49k, PRO129k, BUSINESS249k prices.
- Free standard public GitHub macOS runner with Python 3.11+Chromium file:// source-dash and package tests. This is independent operating system coverage, NOT independent security audit or buyer acceptance.
- Prior Windows/Linux Python 327 suite kept; additional 12 tests => 339 total test cases.

## Exact code acceptance SHA
e4fc8c4616248902cf26ee7e4fcb1ba7f4d8aeb3

| Workflow | ID | Confirmed status | Scope |
|---|---|---|---|
| Python and browser | [43542743086](https://github.com/hibi89/data2web_studio/actions/runs/43542743086) | 4/4 SUCCESS | Windows Python 339PASS; Ubuntu 338PASS 1SKIP; Win Chrome/Edge, Linux Chromium |
| macOS free synthetic | [43542743163](https://github.com/hibi89/data2web_studio/actions/runs/43542743163) | SUCCESS | macos-15, Python338PASS 1SKIP; Chromium dashboard+ZIP+receipt+A4 print+keyboard; network0 |
| CodeQL public free source | [43542743141](https://github.com/hibi89/data2web_studio/actions/runs/43542743141) | SUCCESS | static analysis; no human independent R29 verification and no standalone alert-list review |
| Fixed final blueprint score gate | [43542743517](https://github.com/hibi89/data2web_studio/actions/runs/43542743517) | SUCCESS | R01–33 original 100-point scale remains verified72/pending28; sale NO-GO |

## Real failure and corrected environment
- [Initial macOS run #43542666539](https://github.com/hibi89/data2web_studio/actions/runs/43542666539) FAILED: Python unittest 339, failures13/errors184/skip1 due original macOS /var -> /private/var symlink chain, rejected by fail-closed path_policy.assert_no_links and triggered across temp tests.
- Code and original path security were NOT weakened. One improved retry: macOS runner sets TMPDIR to a physically created .ci-real-temp within the checked-out workspace, success on exact SHA above. Do not change global path_policy to follow untrusted customer symlinks.
- Hosted Mac tests are not real-customer Win10/11/macOS acceptance and do not by themselves grant R23=3 or R06=2.

## Evidence limits and next blockers
- Permission to commercialize third-party code and generated HTML/CSS/JS, legitimate client dataset rights, privacy retention/processing, marketplace seller/settlement conditions, human independent R29 report, real customer acceptance remain missing.
- User-approved KRW 0 outlay. Free volunteer review [issue #5](https://github.com/hibi89/data2web_studio/issues/5) had no confirmed reviewer at this review point.
- Official full blueprint score **72/100**, target 100 unmet. Previous 85 intermediate is also unmet. Completion and actual Krmong listing are distinct; RELEASE HOLD/SALE NO-GO/[작업중] preserved, no real purchase or platform post.
