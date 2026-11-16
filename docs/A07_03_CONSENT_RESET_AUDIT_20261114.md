# A07-03 — desktop and CLI consent-reset audit (static review, runtime pending)

Reviewed at branch after `c01b2dc3c232fa276e06ab303983268dda1004e2`. No customer files used.

## Existing guards confirmed in source
- Single desktop `data2web_desktop.py`: `source,sheet,header,cached` write traces invoke `reset_review()` and clear rights, plaintext, privacy and inspected state; `id_key,title_key,category_key` write traces invoke `reset_consent()`. File picker also calls `reset_review()`.
- Batch desktop: selecting a new file set calls `clear_batch_review()`; changes to `batch_id,batch_title,batch_category` invoke `clear_batch_consent()`. Source-specific sheet/header choices are made as part of new batch selection.
- CLI single: `data2web_single.py` requires explicit `confirm == "APPROVE"` and `ack_plaintext is True`; source modification during package creation raises HOLD.
- CLI append: `data2web_append.py` validates manifest approval, source hashes and explicit confirmation; changed approved source during ZIP packaging raises HOLD.
- These are **source observations**. `python -m unittest discover -v` and actual Tk interactions were not run in this review.

## Potential gap requiring reproduction
- Desktop consent is not traced to output recipient/location (`parent`, `folder`, `batch_parent`, `batch_leaf`) or output app title/theme. Whether recipient/location change must invalidate dataset-specific consent depends on the approved scope; the A07-02 checklist explicitly requires renewed review when recipient/channel changes. A different local folder alone is not proof of a different recipient.
- Next: add synthetic Tk variable-change regression for single and batch recipient/channel changes (with fake Tk variables or headless test); reproduce before patch. Avoid resetting consent on harmless theme edits unless scope policy demands it.
- Keep `R07=PENDING` and `72/100`. No external rights, real consent, or new test PASS claimed.

## Pending technical evidence
`python -m unittest test_order_intake_preflight -v`; `python -m unittest discover -v`; Windows Tk interactive checks for single and batch, and SHA checks on synthetic source replacement. All pending in this turn.
