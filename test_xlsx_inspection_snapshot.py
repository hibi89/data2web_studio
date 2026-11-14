"""R06: the CLI's unselected XLSX sheet listing must use a bounded FD snapshot."""
from __future__ import annotations
import contextlib
import hashlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import path_policy
import studio
from test_xlsx_fixtures import workbook_bytes


class XlsxSheetInspectionSnapshot(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / "synthetic.xlsx"
        self.workbook = workbook_bytes()
        self.source.write_bytes(self.workbook)

    def call_inspect(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = studio.main(["inspect", str(self.source)])
        return code, json.loads(out.getvalue())

    def test_real_sheet_listing_matches_single_bounded_snapshot(self):
        with patch.object(path_policy, "read_bounded_source",
                          wraps=path_policy.read_bounded_source) as reader:
            code, answer = self.call_inspect()
        self.assertEqual(code, 0)
        self.assertEqual(answer["status"], "XLSX_SHEETS_REQUIRE_EXPLICIT_SELECTION")
        self.assertEqual(answer["source_sha256"], hashlib.sha256(self.workbook).hexdigest())
        self.assertEqual(answer["sheets"][0]["name"], "Inventory")
        self.assertTrue(answer["plaintext_warning"])
        self.assertEqual(reader.call_count, 1)
        self.assertEqual(reader.call_args.kwargs["max_bytes"], 8_000_000)

    def test_sheet_inspection_never_uses_unsafe_path_read_bytes(self):
        # pathlib.read_bytes used to read after separate path checks. It must
        # no longer be on the execution path for this action.
        with patch.object(Path, "read_bytes",
                          side_effect=AssertionError("UNSAFE_DIRECT_READ")):
            code, answer = self.call_inspect()
        self.assertEqual(code, 0)
        self.assertEqual(answer["source_sha256"], hashlib.sha256(self.workbook).hexdigest())

    def test_oversized_sheet_file_is_rejected_without_parsing(self):
        self.source.write_bytes(b"PK\x03\x04" + b"X" * 8_000_000)
        with patch("data2web_tabular.list_xlsx_sheets",
                   side_effect=AssertionError("PARSER_MUST_NOT_RUN")):
            code, answer = self.call_inspect()
        self.assertEqual(code, 2)
        self.assertEqual(answer["status"], "HOLD")
        self.assertEqual(answer["reason_type"], "ValueError")
        self.assertNotIn(str(self.source), json.dumps(answer))

    def test_same_size_path_swap_during_fd_open_is_rejected(self):
        replacement = self.root / "replacement.xlsx"
        replacement.write_bytes(self.workbook)
        real_open = path_policy._open_source_readonly
        swapped = [False]
        def rename_before_open(path, flags, *args, **kwargs):
            if Path(path) == self.source.absolute() and not swapped[0]:
                swapped[0] = True
                os.replace(replacement, self.source)
            return real_open(path, flags, *args, **kwargs)
        with patch("path_policy._open_source_readonly", side_effect=rename_before_open):
            code, answer = self.call_inspect()
        self.assertTrue(swapped[0])
        self.assertEqual(code, 2)
        self.assertEqual(answer["status"], "HOLD")
        self.assertEqual(answer["reason_type"], "ValueError")

    def test_unreadable_or_changed_snapshot_is_generic_hold(self):
        with patch.object(path_policy, "read_bounded_source",
                          side_effect=ValueError("PRIVATE_SNAPSHOT_CHANGED")):
            code, answer = self.call_inspect()
        self.assertEqual(code, 2)
        self.assertEqual(answer, {"status": "HOLD", "reason_type": "ValueError"})
        self.assertNotIn("PRIVATE_SNAPSHOT_CHANGED", json.dumps(answer))

    def test_broken_xlsx_header_never_returns_success(self):
        self.source.write_bytes(b"not a zip")
        code, answer = self.call_inspect()
        self.assertEqual(code, 2)
        self.assertEqual(answer["status"], "HOLD")

    def test_missing_source_stays_hold_with_no_path_leak(self):
        self.source.unlink()
        code, answer = self.call_inspect()
        self.assertEqual(code, 2)
        self.assertEqual(answer["status"], "HOLD")
        self.assertNotIn(str(self.source), json.dumps(answer))


if __name__ == "__main__":
    unittest.main()
