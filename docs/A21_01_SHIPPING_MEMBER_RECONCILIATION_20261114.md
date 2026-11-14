# A21-01 — exact shipping-member / origin reconciliation (2026-11-14 KST)

**Scope:** Read-only source inspection plus hosted synthetic-only package execution. No customer data, commercial rights or third-party approvals.

| Delivered artifact | Container | Producer | Current technical verification |
|---|---|---|---|
| `index.html` | Customer folder and ZIP | `data2web_web.py` via `data2web_single.py` / `data2web_append.py` | `delivery.py` compares receipt output SHA256; `verify_delivery.py` verifies HTML hash and CSP; `verify_customer_folder.py` compares disk HTML to ZIP |
| `manifest.json` | ZIP only | `delivery.py` | `verify_delivery.py` checks exact contract/keys, SHA256, release HOLD, provenance |
| `README_KO.txt` | ZIP only | `delivery.py` GUIDE | `verify_delivery.py` checks guide SHA256 against manifest |
| `receipt.json` | Customer folder only | `receipt_utils.py` | `verify_customer_folder.py` checks exact receipt contract, hash, privacy classification and ZIP cross-reference |

Exact allowed ZIP names: `index.html`, `manifest.json`, `README_KO.txt`. Exact customer folder names: `index.html`, `delivery.zip`, `receipt.json`. Extra LICENSE/NOTICE is **not** currently shipped; adding it requires separate rights-holder decision and versioned verifier migration. `shipping_rights_preflight.py` compares both allowlists against `data/shipping_rights_inventory_v1.json` and creates a disposable synthetic delivery. At exact SHA `bfa808b0815b7e5be1bd11de8d6833717be0dcfd`, the Windows and Ubuntu Actions ran it successfully: four allowed artifacts, synthetic integrity true, rights approval false.

### Source pin and origin
- `data/r21_source_provenance_v1.json` references immutable source snapshot `0219a10c03cab826220a78af128cffdae995ac9f` and six Git blob SHA-1 pins. The hosted Actions command `python r21_source_provenance.py` verified all six producer blobs against their pins (6/6) at exact SHA `bfa808b0815b7e5be1bd11de8d6833717be0dcfd`; the immutable source snapshot remains `0219a10c03cab826220a78af128cffdae995ac9f`. This is source identity only.
- Inline CSS/JS are generated within `data2web_web.py`, not separately shipped vendor files according to existing inventory. Actual authorship and any copied/derived code chain require R21-02 investigation.
- Owner-only EXE and Python/Tcl/Tk/PyInstaller, read-only upstream `REA_Web`, Playwright/pypdf test dependencies remain excluded from A customer ZIP. B EXE rights are separately pending.

### Acceptance boundaries
- Technical ZIP integrity is **not** origin authenticity, copyright ownership, legal redistribution authorization or independent security audit.
- Current inventory explicitly marks `rights_owner_attested=false`, `commercial_distribution_approved=false`, `third_party_vendor_inventory_complete=false`, `audit_is_independent=false`. No approval inferred.
- Hosted execution evidence: [Python/browser Actions #43606247844](https://github.com/hibi89/data2web_studio/actions/runs/43606247844), Windows and Ubuntu jobs; `python r21_source_provenance.py` 6/6, `python shipping_rights_preflight.py` synthetic integrity PASS. A21-02 remains technical provenance review; A21-03 actual rights-holder confirmation is still needed.
- **Status:** A21-01 static and synthetic runtime reconciliation complete at `bfa808b0815b7e5be1bd11de8d6833717be0dcfd`; actual author/IP/commercial/NOTICE acceptance remains pending. R21 PENDING, official 72/100, RELEASE HOLD / SALE NO-GO.
