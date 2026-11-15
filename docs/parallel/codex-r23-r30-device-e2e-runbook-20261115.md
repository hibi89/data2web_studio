# R23/R30 independent-device and end-to-end test runbook — 2026-11-15

## Purpose and evidence boundary

This runbook joins the existing synthetic buyer-request generator, result intake, hosted browser probes, and Windows native-preview workflow. It prepares an authorized examiner to exercise the full customer path without sending customer files to GitHub. A hosted runner, owner device, or self-reported result is technical preparation only; R23/R30 remain pending until the required independent real-device/customer evidence is collected and human-verified.

Reusable tools:
- `kmong_weekend_demo.py` creates the synthetic preview.
- `kmong_independent_buyer_request.py` creates the deterministic, create-only ZIP pinned to the tested 40-character source commit.
- `buyer_self_report_intake.py` validates the original blank report and emits only a redacted status and hashes.
- `native_windows_acceptance.py` verifies the unsigned hosted Windows preview using synthetic input. `.github/workflows/native-windows-owner-preview.yml` is a hosted build, not a buyer machine.
- `browser_p85_probe.py`, `browser_single_delivery_probe.py`, and `browser_print_accessibility_probe.py` are hosted supporting probes.

## Examiner preflight

1. Use a fresh, local test folder on an authorized device; use only the synthetic buyer-request ZIP. Do not add customer or personal data.
2. Record the exact tested source SHA from the request. Confirm the local request ZIP hash before unpacking; retain the original ZIP unchanged.
3. Record only approved coarse labels: OS family/version, browser name/version, UTC test time, exact source SHA, test IDs, and PASS/FAIL/NOT_RUN. Do not record a person name, email, phone, account, machine/user name, IP, local path, device serial, screenshot, or source bytes in a public report.
4. If the examiner cannot verify their device/version or is not independent of development, mark the relevant item NOT_RUN and stop the acceptance claim.

## Independent device matrix (each row is a separate run)

| Device profile | Required local browser path | Evidence interpretation |
|---|---|---|
| Windows 10, supported current build | Installed Chrome and installed Edge, opening the local `file://` result | Independent buyer evidence only when executed and reviewed on the real device |
| Windows 11, supported current build | Installed Chrome and installed Edge, opening the local `file://` result | Independent buyer evidence only when executed and reviewed on the real device |
| macOS, report exact major version locally | Installed Chrome or Edge; use Chromium only if Chrome/Edge are unavailable and record that substitution | Hosted macOS CI does not substitute for a buyer device |
| Linux, report distribution/version locally | Installed Chrome, Edge, or Chromium; record browser and version | Hosted Ubuntu CI does not substitute for a buyer device |

Do not infer Windows 10/11 support from `windows-latest`, hosted Chromium, a Windows build label, or a Tk/EXE smoke test.

## R30 end-to-end sequence

Use the synthetic fixture and the exact code SHA. For every step, preserve inputs and pre-existing outputs; the product is create-only and does not perform automatic deletion.

1. **Authorization and consent:** review the source-rights/usage confirmation and plaintext warning. Exercise both consent states. Without an explicit affirmative rights/consent decision, confirm processing remains on HOLD and no output folder is created. Change the source or recipient context and confirm the existing consent-reset bindings require a fresh decision.
2. **Import and mapping:** run representative synthetic CSV, JSON, XLSX, and TSV inputs from repository synthetic test fixtures. Verify sheet/header/ID/title/category selection and preview values. Do not use live customer examples.
3. **Deterministic delivery:** create a new output folder; record source SHA, receipt output SHA, delivery ZIP SHA, row/column counts, and mapping only in the local examiner copy. Repeat in a second empty folder and compare deterministic HTML/ZIP results where the contract specifies determinism.
4. **Independent verification:** run the independent customer-folder and ZIP/receipt verifiers. Confirm an intact synthetic folder passes and tampered receipt or ZIP returns HOLD.
5. **Browser and print:** open local HTML in each selected browser; verify search, category, sort, detail, keyboard focus, narrow/mobile viewport, and print/PDF output. Observe browser Network for zero external requests and Console for zero runtime errors.
6. **Replacement and append:** exercise only the permitted same-header replacement and approved same-schema append paths. Confirm a different header, changed file digest, unapproved source, or occupied destination is refused and the old result stays untouched.
7. **Failure preservation:** inject a synthetic digest mismatch and destination collision. Confirm source bytes and old output bytes remain unchanged; failed partial outputs stay in HOLD for operator inspection. Do not automatically clean them up.
8. **Evidence closeout:** complete the supplied buyer form's seven named steps (offline open, search, category/sort/detail, print, network zero, console, ZIP/receipt review). Keep supplemental checklist notes local until an authorized human review path exists. A passing form is an unauthenticated candidate, never acceptance or sale authorization.

The current form does not collect customer identity or source content and intentionally does not claim to capture supplemental evidence. Do not add free-text fields or screenshots to the public repository.

## Hosted technical coverage

The branch workflow `.github/workflows/parallel-branch-ci.yml` runs Python regressions on Ubuntu, Windows and macOS plus Chromium on Ubuntu and Chrome/Edge on Windows. `native-windows-owner-preview.yml` is currently scoped to the integration branch; on this branch, `test_windows_bundle.py` exercises the portable bundle and real `cmd.exe` on hosted Windows. Hosted green is recorded against its exact commit SHA. Device rows above remain NOT_RUN until actual independent hardware evidence is returned.

## Acceptance status

- Existing synthetic request generator and report intake: reuse; no parallel evidence schema.
- Hosted functional/browser/package checks: technical support only.
- Win10/Win11, macOS and Linux independent buyer runs: **EXTERNAL_PENDING**.
- Customer authorization/rights, real customer E2E and any private evidence transfer: **OWNER/EXTERNAL_PENDING**.
- R23/R30 points and official score: unchanged; RELEASE HOLD / SALE NO-GO.
