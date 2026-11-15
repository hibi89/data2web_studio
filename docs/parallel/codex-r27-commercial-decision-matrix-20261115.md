# R27 internal commercial decision matrix and remaining review — 2026-11-15

## Decision source and scope

The owner-approved zero-cost policy is the source for internal SKU defaults: `data/zero_cost_owner_policy_v1.json`. The matching policy draft is `docs/COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md`. `commercial_terms_consistency.py` checks the published internal matrix against that source and rejects price, source-count, row/column, revision, or defect-support drift.

This is a private internal operating baseline. It is not a marketplace listing, customer quote, executed contract, legal/tax determination, or authorization to sell. No item below adds final-blueprint points or releases the HOLD.

## Approved internal defaults (not published)

| SKU | Internal price | Input and ceiling | Revisions | Defect support |
|---|---:|---|---:|---:|
| BASIC | KRW 49,000 | One CSV/TSV/flat JSON source; 1,000 rows × 20 columns; one basic theme | 1 | 7 days |
| PRO | KRW 129,000 | One owner-selected XLSX sheet or up to 3 same-header appended CSV/TSV/JSON sources; 5,000 rows × 20 columns | 2 | 14 days |
| BUSINESS | KRW 249,000 | 2–10 same-schema sources, including selected XLSX sheets; combined ceiling 10,000 rows × 20 columns | 3 | 30 days |

Engine boundaries still apply: each input is limited to the existing source-size cap and the final HTML to the existing output-size cap. A mismatch or limit overflow is HOLD before accepting an order; it does not silently expand a SKU. The revision count is for agreed mapping, copy, or theme corrections; it does not promise new input structures, JOIN/DB, APIs, logins, hosting, crawling, or unlimited feature work. Defect support covers an agreed feature that fails its stated contract and does not exclude statutory consumer remedies.

## Already approved internal operating defaults

- Zero upfront spend. No paid signing, audit, API, cloud, or larger runner.
- Prefer synthetic/anonymous schema examples. Do not accept unclear rights, personal/sensitive information, or customer files through GitHub/ChatGPT/CI. Per-order source rights and processing authority remain to be confirmed.
- If an authorized local temporary copy is ever received, the operator manually destroys unnecessary copies no later than seven days after acceptance, earlier when the purpose ends, except legally required records; never automatically delete the customer's source or existing outputs.
- The delivered HTML may contain plaintext source values. The customer notice and rights/consent must be checked for each actual job.
- Refund and cancellation handling follows applicable law and current marketplace rules. No blanket “non-refundable” term. Platform charges, VAT/business tax treatment, merchant status, registration format, and current listing language remain unverified.

## Owner/external decisions still needed

| Decision or proof | Current status | Release gate |
|---|---|---|
| Final platform fees, merchant/tax handling, current marketplace listing form and final listing text | OWNER_PENDING / NOT_VERIFIED | Recheck before any listing or order |
| Per-customer source rights, privacy/consent and plaintext notice | OWNER/EXTERNAL_PENDING | No real file receipt or processing before evidence |
| Code, theme, and third-party redistribution rights/NOTICE | OWNER_PENDING | No commercial redistribution claim or LICENSE creation |
| Actual independent customer device/E2E review | EXTERNAL_PENDING | No R23/R30 acceptance |
| Independent security audit and any retest | EXTERNAL_PENDING | R29 remains pending |
| Actual marketplace order, platform receipt, delivery and refund/cancellation proof | OWNER/EXTERNAL_PENDING | R33 remains pending; do not simulate |

The internal SKU defaults are recorded as approved. Do not request the same internal policy approval again; request only genuinely missing owner/external choices and evidence when needed.
