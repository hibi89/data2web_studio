# H10 / R06 — source-handle race hardening and synthetic reproduction (2026-11-15 KST)

**Scope:** DATA2WEB Studio A, R06 technical engineering. **Status:** implemented in HIGH branch, hosted CI under verification. External independent Windows/real-user source handling remains PENDING. Official score 72/100; no release or sale authorization.

## Threat matrix / expected fail-closed behavior

| Threat | Baseline before H10 | H10 response | Evidence |
|---|---|---|---|
| Reviewed source is a hardlink alias to a different pathname | No st_nlink check; read accepted | Refuse any source with link count != 1 before opening | `test_hardlinked_source_is_not_accepted` |
| Second hardlink appears between lstat and open | Open/file identity checks but no link-count check | Inspect fstat link count after open; HOLD | `test_hardlink_added_after_precheck_is_rejected` |
| Hardlink alias appears while reading | Metadata comparison omitted st_nlink | Refuse if post-read or named-path link count != 1 | Code guard; full process race still requires external adversarial validation |
| POSIX regular file path becomes FIFO between lstat/open | Blocking `os.open(..., O_RDONLY)` can wait indefinitely | `O_NONBLOCK` on POSIX descriptor open, then fstat must confirm regular file | `test_regular_source_swapped_to_fifo_cannot_block_open` |
| Same-length regular file atomically replaces path during read | Start/end inode metadata comparison | Retain comparison and prove it rejects via synthetic race | `test_same_length_atomic_replacement_during_read_is_rejected` |
| Windows junction/symlink/reparse/rename | Existing link checks and share-deny-write/delete handle | Preserve existing behavior and current Windows negative tests | Prior tests; actual Win10/11 test still external PENDING |
| Bounded SHA256 / size/bytes and original preservation | Source read uses a single fd and recheck after rendering | Preserve; extra link guards prevent external alias ingestion | `test_normal_bounded_source_unchanged`; prior integration tests |
| POSIX directory rename between validated ancestry operations | Best-effort lstat path chain; no anchored read directory fd | **Known remaining limitation**: local untrusted same-UID writer or ancestor rename races require separate architecture/OS validation | Do not claim race-free R06 |
| Output create-only / failure after output creation | Relative directory handle and O_EXCL; failed partial output remains for investigation | No modification to output semantics in H10 | Existing `test_secure_output.py`; release HOLD |

## Options reviewed

- **A. Conservative fail-closed checks (selected):** reject multi-linked source, prevent POSIX blocking FIFO opens, reuse existing fstat/path identity and bounded SHA256 logic. Low maintenance, stdlib only, Windows-compatible; minimal performance overhead (extra metadata checks). Cannot prove resilience against a fully malicious same-UID namespace actor.
- **B. Directory-FD / Windows handle anchored complete source traversal:** stronger ancestry pinning against rename/symlink swaps; complex OS-specific handle-lifetime, path integration and ACL implementation, higher risk of changing normal workflows. Defer until real adversarial threat scenario or independent audit justifies it. Existing output directory uses anchored handles.

## Verification, external boundaries and instructions

Technical patch: `path_policy.py` (HIGH owned), added `test_r06_source_race.py`. Only synthetic temporary files; no customer files, network, external data transfer, checkout or payment. Source filename and bytes are not sent to diagnostics. Tests are automatically discovered by `python -m unittest discover -v` in `.github/workflows/parallel-branch-ci.yml`, with Windows/Ubuntu/macOS runners. CI run for code SHA `7576e3291981e7bffc2eda0b059ccb7931bf6f5f`: https://github.com/hibi89/data2web_studio/actions/runs/43683639426 (result to be recorded after completion).

**Completion gate:** hosted CI passing does not prove R06 acceptance. Independent Win10/11 real-device concurrency/reparse/hardlink retest, source rights/privacy and customer acceptance must be supplied. R06 remains PENDING and score addition 0 until full evidence exists. PR #7 remains Draft; do not merge automatically.

**Recovery:** GitHub immutable pre-change commit `ded01ce3576a3ea06769fc8e18e917bd98b54ab2`, surgical fix commit `87bdf58196a50c91898781217786fb942d05a8d7`, negative test commit `7576e3291981e7bffc2eda0b059ccb7931bf6f5f`. Revert the isolated commits through normal history if proven regressive; never force-push or overwrite owner/customer data.
