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

    def test_single_source_mutated_during_zip_never_issues_receipt(self):
        from data2web_single import deliver_single
        import data2web_single
        genuine=data2web_single.package_html
        dest=self.root / "single-customer"
        def mutate_during_zip(*args,**kwargs):
            result=genuine(*args,**kwargs)
            self.csv.write_text("id,title,category\nS1,Changed item,A\n", encoding="utf-8")
            return result
        with patch.object(data2web_single,"package_html",side_effect=mutate_during_zip):
            with self.assertRaisesRegex(ValueError,"during package creation"):
                deliver_single(self.csv,dest,expected_sha256=self.ssha,
                    id_column="id",title_column="title",category_column="category",
                    confirm="APPROVE",ack_plaintext=True,
                    privacy_classification="NO_PERSONAL_DATA_REVIEWED")
        self.assertTrue((dest/"index.html").exists())
        self.assertTrue((dest/"delivery.zip").exists())
        self.assertFalse((dest/"receipt.json").exists())

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

    def test_append_source_mutated_during_zip_never_issues_receipt(self):
        import data2web_append
        manifest=self.setup_approved_append()
        zip_path=self.root/"fresh.zip"
        receipt_path=self.root/"receipt.json"
        second=self.root/"second.csv"
        genuine=data2web_append.package_html
        def mutate_during_zip(*args,**kwargs):
            result=genuine(*args,**kwargs)
            second.write_text("id,title,category\nS2,Changed second,B\n",encoding="utf-8")
            return result
        with patch.object(data2web_append,"package_html",side_effect=mutate_during_zip):
            with self.assertRaisesRegex(ValueError,"during ZIP packaging"):
                data2web_append.build_approved_append(
                    manifest,self.html,confirm="APPROVE",ack_plaintext=True,
                    zip_path=zip_path,receipt_path=receipt_path)
        self.assertTrue(self.html.exists())
        self.assertTrue(zip_path.exists())
        self.assertFalse(receipt_path.exists())

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
