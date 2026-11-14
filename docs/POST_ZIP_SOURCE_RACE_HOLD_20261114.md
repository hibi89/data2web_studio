# DATA2WEB — prevent source mutation after ZIP creation before final receipt

2026-11-14 KST | zero cost | exact tested feature SHA `cbf6a908a09fee0cba058ccfe2cb9e41e87568cb`

## Confirmed issue and design choice
Existing source SHA-256 was checked before and after HTML write, but source data could change while packaging the customer ZIP. A valid ZIP might still be produced from the prior approved snapshot and be followed by a fresh acceptance receipt even though the source has now changed.

- **Selected A:** rehash each bounded, link-safe approved source **after ZIP packaging and before final receipt creation**. This is a small direct addition to the existing single-source and append code, preserves documented create-only and partial-output HOLD behavior, no dependency or additional service cost, and fails closed.
- **Rejected B:** refactor all packaging to staging/transactional atomic replace. This changes filesystem semantics and might delete the partial folder needed for evidence/recovery, adding substantial risk; not needed for the concrete window being protected.

## Specific code
- `data2web_single.py`: after `package_html` returns, read the source again using the bounded snapshot reader and compare SHA to the owner-approved hash; if changed, raise `ValueError(... output HOLD)` **before** `receipt.json` is written.
- `data2web_append.py`: after `package_html`, recheck SHA of **every** approved source in the 2–10 file batch; if any differ, hold prior to `receipt.json`.
- `test_output_snapshot_security.py`: two new regression tests use synthetic-only source files, inject a source rewrite **inside the packaging call**, assert an exception, check that the new output remains for human inspection and that no `receipt.json` was issued. Pre-existing CLI and GUI paths remain unchanged.
- This narrows the TOCTOU exposure but **does not eliminate filesystem races entirely or authenticate external data rights**. It does not automatically certify the entire R06 requirement.

## Executed acceptance and exact SHA
- Feature/validation commit: `cbf6a908a09fee0cba058ccfe2cb9e41e87568cb`.
- [Windows/Linux + installed browser test run #43560878349](https://github.com/hibi89/data2web_studio/actions/runs/43560878349) **4/4 SUCCESS**; Windows **419/419 PASS**, Ubuntu **418 PASS + 1 SKIP**, Chrome, Edge and Chromium offline file:// paths.
- [macOS offline run #43560878353](https://github.com/hibi89/data2web_studio/actions/runs/43560878353) SUCCESS.
- [CodeQL #43560878318](https://github.com/hibi89/data2web_studio/actions/runs/43560878318) SUCCESS.
- [Synthetic seller preview #43560878354](https://github.com/hibi89/data2web_studio/actions/runs/43560878354) SUCCESS (no actual listing).
- [100-point fixed blueprint evidence gate #43560878493](https://github.com/hibi89/data2web_studio/actions/runs/43560878493) SUCCESS.
- Historical real user Windows11 synthetic Tk/Chrome GUI passed earlier; **this latest code SHA was not rerun by the owner on a physical Windows PC**.

## Score and authorization boundaries
- Full owner R01–R33 score remains **72/100 (22 verified; 11 pending/28 points)**, no self-awarded R06 improvement to formal full requirement acceptance.
- Independent external R29 human audit, actual independent buyer OS test, commercial IP/NOTICE/client source rights and sale GO all remain unverified, status `[작업중]`, `RELEASE HOLD / SALE NO-GO`.
- No customer originals, third-party private assets, key/PII, Vercel runtime, Github binary, paid reviewer or Kmong listing were changed. Owner is outside; no PC tasks needed.

## Technical commands
`python -m unittest test_output_snapshot_security -v`
`python -m unittest discover -v`
Browser/OS commands and prerequisites are in `.github/workflows/python-tests.yml` and the associated run IDs.
