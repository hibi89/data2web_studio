# DATA2WEB R22 — Independent ZIP CSP structural verification
Date: 2026-11-14 KST. Upfront cash spending: KRW 0.

## Design comparison and choice
- Chosen: preserve single offline HTML/ZIP/receipt contract, and independently validate the exact Content-Security-Policy plus the static JavaScript SHA-256 Base64 digest inside ZIP verification (Python stdlib only). This blocks accidentally relaxed CSP even if a package manifest SHA is recomputed. No server, API or customer content needed.
- Rejected: continue accepting any HTML if its SHA matches the manifest, because SHA is self-consistency, not security policy. Third-party cryptographic publisher signing would require actual owner rights/key/approved deployment; not attempted.

## Implementation
Source SHA: 02bd0f6f5920e90511633686866eecf7a9d1c50c.
- verify_delivery.py: exactly one CSP meta, exactly one static executable inline script, exactly one nonexecuting JSON dataset script, and a strict policy with default-src none, connect-src none, form-action none, base-uri none and correct static script SHA. Reject malformed/unapproved policy before returning verified.
- test_zip_offline_csp.py: six tests cover a genuine package, modified script, broader connect-src, unsafe-inline, missing CSP and duplicate script, even if the attacker regenerates manifest HTML SHA.
- Caveat: hash and CSP do not prove code authorship if a malicious party can rewrite BOTH the JavaScript and matching CSP and manifest. Independent R29 security audit and rights verification are separate requirements.

## Exact GitHub validation
- Python and browser run 43548658681: 4/4 SUCCESS; Windows 378 PASS, Ubuntu 377 PASS + 1 SKIP; Chrome/Edge/Chromium real offline browser flows.
- Synthetic Kmong preview run 43548658668: SUCCESS; artifact 14095536521 downloaded and CRC verified, 9 members, two PNG screenshots and CSP script digest match.
- CodeQL 43548658658 SUCCESS; fixed score gate 43548658954 SUCCESS.
- macOS workflow path trigger repaired at workflow-only SHA a56737ab3690339e00bfef5664639ecd4a41eeb7. Run 43548812460 SUCCESS (macOS 377 PASS + 1 SKIP, real Chromium, print, ZIP/receipt, network0). Windows/Linux run 43548812433 4/4 SUCCESS, CodeQL 43548812448 SUCCESS, score 43548812656 SUCCESS.

## Legacy compatibility and release limits
- Previous generated ZIP files carrying the old unsafe-inline script CSP will intentionally fail the strict new verifier. Keep the originals unchanged. Only regenerate into a new folder when source authority and customer data rights are established. No silent migration, deletion, or overwrite.
- CodeQL and developer-run CI success does not equal zero security flaws, digital signature, independent human R29 audit, or customer acceptance.
- Official frozen R01–R33 score remains 72/100, 11 pending = 28 points, entire goal 100 not reached, [작업중], RELEASE HOLD, SALE NO-GO, Kmong not registered.
