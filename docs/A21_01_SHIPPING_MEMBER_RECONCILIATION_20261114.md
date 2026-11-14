# A21-01 — exact shipping-member / origin reconciliation (2026-11-14 KST)

**Scope:** Read-only source inspection of current feature branch. No customer data, package execution, commercial rights or third-party approvals.

| Delivered artifact | Container | Producer | Current technical verification |
|---|---|---|---|
| `index.html` | Customer folder and ZIP | `data2web_web.py` via `data2web_single.py` / `data2web_append.py` | `delivery.py` compares receipt output SHA256; `verify_delivery.py` verifies HTML hash and CSP; `verify_customer_folder.py` compares disk HTML to ZIP |
| `manifest.json` | ZIP only | `delivery.py` | `verify_delivery.py` checks exact contract/keys, SHA256, release HOLD, provenance |
| `README_KO.txt` | ZIP only | `delivery.py` GUIDE | `verify_delivery.py` checks guide SHA256 against manifest |
| `receipt.json` | Customer folder only | `receipt_utils.py` | `verify_customer_folder.py` checks exact receipt contract, hash, privacy classification and ZIP cross-reference |

Exact allowed ZIP names: `index.html`, `manifest.json`, `README_KO.txt`. Exact customer folder names: `index.html`, `delivery.zip`, `receipt.json`. Extra LICENSE/NOTICE is **not** currently shipped; adding it requires separate rights-holder decision and versioned verifier migration. `shipping_rights_preflight.py` compares the two allowlists against `data/shipping_rights_inventory_v1.json` and creates a disposable synthetic delivery; **not executed this turn**.

### Source pin and origin
- `data/r21_source_provenance_v1.json` references immutable source snapshot `0219a10c03cab826220a78af128cffdae995ac9f` and six Git blob SHA-1 pins. Directly retrieved `delivery.py` Git blob SHA `52075fc6ebdb5f886a2c05725b4c1aabf4b0dbba` agrees with its pin. Other five files' bytes and pins were **not** independently recomputed this turn; `r21_source_provenance.py` checks all six at runtime.
- Inline CSS/JS are generated within `data2web_web.py`, not separately shipped vendor files according to existing inventory. Actual authorship and any copied/derived code chain require R21-02 investigation.
- Owner-only EXE and Python/Tcl/Tk/PyInstaller, read-only upstream `REA_Web`, Playwright/pypdf test dependencies remain excluded from A customer ZIP. B EXE rights are separately pending.

### Acceptance boundaries
- Technical ZIP integrity is **not** origin authenticity, copyright ownership, legal redistribution authorization or independent security audit.
- Current inventory explicitly marks `rights_owner_attested=false`, `commercial_distribution_approved=false`, `third_party_vendor_inventory_complete=false`, `audit_is_independent=false`. No approval inferred.
- Next: execute `python shipping_rights_preflight.py` and `python r21_source_provenance.py` on a complete checkout; A21-02 origin/author/vendor obligations, then actual owner rights confirmation A21-03.
- **Status:** A21-01 static reconciliation completed; runtime evidence pending. R21 PENDING, official 72/100, RELEASE HOLD / SALE NO-GO.
