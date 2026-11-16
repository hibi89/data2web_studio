# DATA2WEB - zero-cost anonymous pre-order scope gate (2026-11-14 KST)

## Two designs
1. **Chosen: local stdlib-only gate, KRW 0.** Anonymous file counts/types/size and boolean rights/privacy/plaintext declarations; never opens customer originals, emails, names, file paths, or values. No new server, login, SaaS, API, or external transfer.
2. Rejected: third-party form/SaaS or always-online quotation. Possible extra cost, data transfers and maintenance, violating the owner's 0-cash and offline A-first rule.

## Use
- The seller prepares a copy of data/kmong_anonymous_request_example.json with ONLY the enumerated anonymous metadata. No customer identifier or source filenames, even when a buyer offers one. Do not place real consultation metadata or rights attestation in GitHub or ChatGPT.
- Run: python order_intake_preflight.py --synthetic-self-check
- For an actually authorized local metadata file run: python order_intake_preflight.py --metadata-file path-to-local-summary.json --new-report-file fresh-quote-status.json
- Existing output files are never overwritten. Failure prints a generic HOLD, without customer paths or file contents.
- BASIC: one CSV/TSV/JSON <=1000 rows; PRO: one XLSX or up to 3 same-header non-XLSX <=5000 rows; BUSINESS: 2-10 same-header files <=10000 rows. Each <=8MB; columns 3-20; distinct ID/title/category mapping confirmation required. The owner-approved SKU 49k/129k/249k is read from the locked zero-cost policy.
- Suspected personal/sensitive or confidential data, uncertain rights, lack of explicit plaintext warning, unsupported volume, or incompatible headers => HOLD. Never accept raw files here.

## Distinguish scope vs legal/sale acceptance
Even a match returns SCOPE_CANDIDATE_ONLY with order_accepted=false, customer_rights_independently_verified=false, and sale_approved=false. These booleans are intentionally immutable and do NOT attest rights to third-party content, customer consent, actual Excel sheet/formula compatibility, marketplace approvals, or external independent security audits. Current R01-R33 score 72/100 remains unchanged.

## Evidence
The normal Python unittest discover job covers 12 new tests on Windows+Ubuntu. Only a successful CI at an exact Git SHA demonstrates execution. Consumer terms follow docs/KMONG_WEEKEND_LISTING_20261114.md, rights and other blockers follow docs/ZERO_COST_72_TO_100_ACTION_MATRIX_20261114.md. Do not ship the builder/unsigned EXE or publish the listing until release approval.
