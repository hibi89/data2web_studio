# A21-02 — shipped producer origin and dependency review (2026-11-14 KST)

**Evidence scope:** Direct GitHub contents API retrieval and hosted technical checks at `${verifiedSha}`; no customer file, external license-holder confirmation, or legal review.

## Verified source identity
All six `data/r21_source_provenance_v1.json` Git blob SHA-1 pins matched GitHub's returned current blob IDs (6/6):

| Producer | Verified Git blob |
|---|---|
| `data2web_web.py` | `65bd8fe16d7b284f553d5185ed369650cc83d82f` |
| `delivery.py` | `52075fc6ebdb5f886a2c05725b4c1aabf4b0dbba` |
| `receipt_utils.py` | `02378bc8b18e6a37f225dc2c132fa9456551af64` |
| `data2web_single.py` | `bc1c8499f48c7f1f8b7b0d0b3b713d9328d05fc6` |
| `data2web_append.py` | `3770f6bfc3bbe9e634e694226027eda0bd0c8f38` |
| `data2web_tabular.py` | `66c2fb8910b1202ae3b0301e8b615158d9a5fac9` |

Git blob equality is code identity, **not** author attribution, copyright clearance, or signed provenance. Source snapshot declared in manifest: `0219a10c03cab826220a78af128cffdae995ac9f`.

## Hosted technical recheck
- At exact SHA `48ea586b6ef712176b26c33d1809d3cd9a782d94`, [Actions #43604742332](https://github.com/hibi89/data2web_studio/actions/runs/43604742332) ran `python r21_source_provenance.py` on Windows and Ubuntu: `source_files_verified=6`, `SOURCE_BLOBS_PINNED_RIGHTS_PENDING`.
- The same exact SHA ran `python shipping_rights_preflight.py` on both runners: four synthetic artifacts, exact v1 folder/ZIP allowlists, source bytes preserved, technical integrity verified; owner rights, commercial release, third-party notices and independent audit all remain false.
- These checks prove pinned byte identity and package-contract behavior only. They do not identify the human author of embedded HTML/CSS/JS or grant redistribution rights.

## Direct import scan and A delivery boundary
- `data2web_web.py`: Python stdlib `base64`, `hashlib`, `html`, `json`, `re`; emits inline HTML/CSS/JS. No imported vendor JS module identified by Python import scan. Embedded script/template authorship **not verified**.
- `delivery.py`: Python stdlib `hashlib`, `json`, `pathlib`, `zipfile` and internal `path_policy`, `verify_delivery`.
- `receipt_utils.py`: Python stdlib `json`, `os`, `pathlib` and internal `path_policy`.
- `data2web_single.py`: Python stdlib `hashlib`, `pathlib`; internal `data2web`, `data2web_web`, `delivery`, `receipt_utils`, `path_policy`.
- `data2web_append.py`: Python stdlib `hashlib`, `json`, `os`, `pathlib`; same internal modules.
- `data2web_tabular.py`: Python stdlib `csv`, `io`, `posixpath`, `re`, `zipfile`, `pathlib`, `xml.etree.ElementTree`. XLSX XML namespace URLs are schema identifiers, not observed external requests.
- These Python modules are **not** shipped as Python source in the A ZIP. The actual embedded HTML/CSS/JS and guide are shipped and require separate authorship/derivation rights review.

## Unresolved provenance / license chain
1. Obtain actual author and contributor history for embedded HTML template, JS, CSS, README and receipt/manifest text; GitHub ownership alone is insufficient.
2. Compare against `REA_Web` and any reused templates or third-party assets to identify copied/derived content, then obtain actual redistribution permissions and required notices.
3. Determine any relevant customer-data/database rights and the exact intended customer redistribution scope per order; source-code rights do not grant rights over customer rows.
4. Inspect generated output bytes and dependency SBOM in a complete runnable checkout; source import scan does not prove absence of embedded third-party code.
5. Only after owner/legal confirmation, decide whether v1 requires LICENSE/NOTICE; do not ship invented text or change the strict allowlist before approval.

**Result:** A21-02 source identity and dependency inspection plus 6/6 runtime pin validation complete at `${verifiedSha}`; legal origin, authorship, redistribution and NOTICE evidence remain PENDING. No R21 score award; official 72/100, RELEASE HOLD.
