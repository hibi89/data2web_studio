# A26-01 — privacy scope matrix and exposure map

**Status: technical decision aid only.** The classifications below are synthetic and contain no customer examples. A class is a user-supplied scope statement, not machine detection, legal advice, customer consent, anonymization, or proof of rights. Actual customer-specific lawful basis and consent remain pending; R26 stays PENDING.

## Synthetic class matrix

The anonymous preorder contract is now V2. It requires an exact privacy_classification value plus strict contains_personal_or_sensitive and contains_third_party_confidential booleans. A candidate requires the explicit safe class and both risk booleans set to false, plus the existing rights and plaintext declarations. A class alone never accepts an order or approves a sale.

| Class | Synthetic examples only | Preflight decision |
|---|---|---|
| NO_PERSONAL_DATA_REVIEWED | Explicit human review found no direct or indirect identifiers, sensitive/medical values, payment identifiers or third-party confidential/shared content; scope and rights are understood | Candidate scope only if all other checks pass; no order or sale approval |
| PERSONAL_OR_IDENTIFYING_DATA_PRESENT | Name, email, phone, address, account/member number, device/location identifier, or a field combination that identifies a person | HOLD_PREORDER |
| SENSITIVE_OR_MEDICAL_DATA_PRESENT | Health, diagnosis, treatment, disability, biometric, or other sensitive/special-category information | HOLD_PREORDER |
| PAYMENT_DATA_PRESENT | Card/bank/payment credentials, transaction identifiers tied to an identifiable person, or payment account detail | HOLD_PREORDER |
| THIRD_PARTY_CONFIDENTIAL_OR_SHARED_DATA | Confidential material, another organization's/customer's records, shared dataset, or unclear onward-use restriction | HOLD_PREORDER |
| UNKNOWN_OR_MIXED_SCOPE | Not reviewed, uncertain column meaning, mixed classes, unknown source, or a disagreement about permitted use | HOLD_PREORDER |

Missing, malformed, legacy V1, or unrecognized classification metadata fails closed. The older risk booleans remain as independent negative checks: either true still yields HOLD even when the class says NO_PERSONAL_DATA_REVIEWED. The test suite also rejects undeclared identifier keys and invalid values. No raw field values, names, paths, or customer files enter this preflight.

## Data flow and plaintext/offline exposure

| Stage | What the product does | Privacy and exposure boundary |
|---|---|---|
| Anonymous preflight | Reads only bounded format/count metadata, risk booleans and a privacy class supplied by the operator; never opens a customer source file | The class is self-reported and cannot discover identifiers hidden in data |
| Local source inspection | Reads the selected local file for parsing, SHA, header and profile checks | The desktop says it does not upload the source; column names can still be sensitive |
| Transform and browser output | Builds an offline HTML result from the approved rows and columns | index.html may contain source values in plaintext. There is no encryption, access control, or automatic anonymization |
| ZIP and receipt | Creates a local ZIP and receipt for the output | ZIP/receipt integrity checks do not prove privacy, rights, or consent |
| file:// viewing | Opens the HTML locally in a supported browser without a product server | Offline use does not make the file confidential: recipients with file access can read, copy, or forward it |
| Operator retention | May leave an operator-controlled source or result copy | Source and result retention are recorded separately; manual deletion/return authority is required |

The UI offers NO_PERSONAL_DATA_REVIEWED and OWNER_APPROVED_LOCAL_ONLY. Both are explicit owner assertions; OWNER_APPROVED_LOCAL_ONLY does not mean encrypted, anonymized, legally permitted, or customer-consented. Direct/indirect identifiers, sensitive or medical data, payment data, third-party confidential/shared data, and any unknown or mixed scope remain on HOLD until the required customer-specific rights, processing basis, recipient, plaintext and retention scope are established. The desktop's current wording calls out these limits in single and batch flows.

The UI review indicators and preflight are safeguards against accidental scope expansion; they cannot independently validate a customer's legal authority. Do not upload customer data, signatures, actual paths, evidence, or source code to external services.

## Exact hosted verification requested

- python -m unittest test_order_intake_preflight -v
- python -m unittest test_operator_copy_retention -v
- Full existing Python, Windows/Ubuntu, Chrome/Edge/Chromium, CodeQL and final blueprint workflows at the exact code SHA after commit.
- Unexecuted actions remain unverified. Synthetic PASS does not satisfy customer acceptance or independent external audit.
