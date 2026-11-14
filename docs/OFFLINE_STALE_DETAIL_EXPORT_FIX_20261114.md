# DATA2WEB — stale detail disclosure when replacing offline CSV: FIXED

Date: 2026-11-14 KST.

## Actual issue
Earlier versions rendered a selected row's full JSON in the #details <pre>. Subsequent category, search, or local replacement rendered new table records but did not clear that selected detail. Saving replacement HTML serialized document.documentElement.outerHTML, which can preserve stale DOM text from the old source despite a new #dataset. This is a privacy/data-integrity issue: the old row could appear in a separately downloaded new HTML.

## Design and minimal change
- A) Clear the detail component whenever the table/filter is re-rendered. **Selected**: one new line, ensures stale row does not survive source replacement or new filters and preserves all existing source SHA, CSP, render and delivery logic.
- B) Track an explicit selected-record identity across every search/filter/source import to decide when to clear. More state and higher maintenance/cost for no required behavior, not selected.

Changed `data2web_web.py`: `render()` now always sets `#details` to "항목을 선택하세요." before the current filtered rows are built.
Changed `browser_p85_probe.py`: selects the original XSS/Injection detail, replaces source CSV with two new rows, asserts details reset, saves HTML, checks downloaded HTML contains neither old `Injection` nor prior `row-239` sentinel, reopens from file:// and checks source/import status, sums and responsive behavior. Existing browser tests cover malformed UTF-8, reconsent, source provenance and no external requests. No actual customer values in tests, only synthetic data.

## Exact evidence
- Source code SHA **0d0bd184564b74200dbe667630f2cd4fda4b0646**; first implementation 5bc8c30ffbda9dce5110cab6be7d20d0cdcd8fb6 with stronger selected-XSS regression in final commit.
- [Windows, Linux, Chrome, Edge, Chromium #43559980414](https://github.com/hibi89/data2web_studio/actions/runs/43559980414) **4/4 SUCCESS**. Windows Python **417 PASS**, Ubuntu Python **416 PASS / 1 SKIP**. Browser markers `P85_CROSS_BROWSER_PASS channel=chrome`, `msedge`, and `chromium`, 0 HTTP(S) requests, file:// HTML export/reopen checks.
- [macOS offline acceptance #43559980421](https://github.com/hibi89/data2web_studio/actions/runs/43559980421) SUCCESS.
- [CodeQL #43559980452](https://github.com/hibi89/data2web_studio/actions/runs/43559980452) SUCCESS.
- [Frozen final blueprint score #43559980691](https://github.com/hibi89/data2web_studio/actions/runs/43559980691) SUCCESS.

## Boundaries/next
The GitHub CI proof covers only generated synthetic files; Chrome/Edge/Chromium inspected stale-detail replacement under CI. The owner's previous real Win11 Tk batch GUI+Chrome synthetic end-to-end PASS is separately recorded under docs/OWNER_WINDOWS11_GUI_SEARCH_SCREENSHOT_ACCEPTANCE_20261114.md, but this new patch was **not** deployed/run again on owner's physical PC. No customer source, real client approval, external R29 human security review, IP/NOTICE license authorization or actual marketplace publication evidence was added. Official fixed 100-point final score stays **72/100, 22 VERIFIED, 11 PENDING 28**, [작업중], RELEASE HOLD / SALE NO-GO. User explicitly deferred marketplace listing to Codex; prioritize frontend/backend work. No owner PC action required or requested during outing. No paid costs, user originals, upstream REA_Web or Vercel changes.
