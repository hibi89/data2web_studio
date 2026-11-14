"""R06 create-only output verification uses bounded FD snapshots on both paths."""
from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data2web
import data2web_append
from test_xlsx_fixtures import workbook_bytes


class OutputSnapshotSecurity(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.csv = self.root / "synthetic.csv"
        self.csv.write_text("id,title,category\nS1,Synthetic item,A\n",encoding="utf-8")
        self.ssha = hashlib.sha256(self.csv.read_bytes()).hexdigest()
        self.html = self.root / "new.html"

    def build_single(self):
        return data2web.build(self.csv, self.html, "id", "title", "category",
                              approved=True, expected_sha256=self.ssha)

    def test_single_creation_uses_no_direct_read_bytes_for_verification(self):
        with patch.object(Path, "read_bytes",
                          side_effect=AssertionError("UNBOUNDED_OUTPUT_READ_FORBIDDEN")):
            receipt = self.build_single()
        self.assertEqual(receipt["rows"], 1)
        self.assertTrue(self.html.is_file())
        self.assertFalse(receipt["sale_approved"])

    def test_single_output_changed_at_verified_read_remains_hold(self):
        safe = data2web.read_bounded_source
        def wrong_bytes(path, **kwargs):
            if Path(path) == self.html:
                return b"tampered output"
            return safe(path, **kwargs)
        with patch.object(data2web, "read_bounded_source", side_effect=wrong_bytes):
            with self.assertRaisesRegex(ValueError, "Output integrity mismatch"):
                self.build_single()
        self.assertTrue(self.html.exists())

    def test_single_oversize_html_rejected_without_any_output(self):
        with patch("data2web_web.render_html", return_value="X" * 20_000_001):
            with self.assertRaisesRegex(ValueError, "Output HTML exceeds"):
                self.build_single()
        self.assertFalse(self.html.exists())
        self.assertEqual(self.csv.read_text("utf-8"),
                         "id,title,category\nS1,Synthetic item,A\n")

    def setup_approved_append(self):
        second = self.root / "second.csv"
        second.write_text("id,title,category\nS2,Synthetic second,B\n", encoding="utf-8")
        manifest = self.root / "approved.json"
        document = {
            "contract": "DATA2WEB_INPUT_APPROVALS_V1",
            "sources": [
                {"filename":p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in (self.csv, second)
            ],
            "mapping": {"id": "id", "title": "title", "category": "category"},
            "approval": {"rights_and_plaintext_ack": True,
                         "privacy_classification": "NO_PERSONAL_DATA_REVIEWED"},
            "name": "Synthetic only",
            "theme": "office",
        }
        manifest.write_text(json.dumps(document), encoding="utf-8")
        return manifest

    def test_append_uses_bounded_output_fd_not_pathlib_read_bytes(self):
        manifest = self.setup_approved_append()
        with patch.object(Path, "read_bytes",
                          side_effect=AssertionError("UNBOUNDED_OUTPUT_READ_FORBIDDEN")):
            receipt = data2web_append.build_approved_append(
                manifest, self.html, confirm="APPROVE", ack_plaintext=True
            )
        self.assertEqual(receipt["rows"], 2)
        self.assertTrue(self.html.is_file())
        self.assertFalse(receipt["sale_approved"])

    def test_append_output_tamper_fails_without_deleting_hold_file(self):
        manifest = self.setup_approved_append()
        safe = data2web_append.read_bounded_source
        def wrong_bytes(path, **kwargs):
            if Path(path) == self.html:
                return b"tampered output"
            return safe(path, **kwargs)
        with patch.object(data2web_append, "read_bounded_source", side_effect=wrong_bytes):
            with self.assertRaisesRegex(ValueError, "Output differs"):
                data2web_append.build_approved_append(
                    manifest, self.html, confirm="APPROVE", ack_plaintext=True
                )
        self.assertTrue(self.html.exists())


if __name__ == "__main__":
    unittest.main()
