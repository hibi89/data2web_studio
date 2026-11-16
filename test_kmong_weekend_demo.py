"""Synthetic product-demo smoke/negative tests; no customer data or network."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path

from kmong_weekend_demo import (
    DEMO_ROWS, LEAF, NOTICE, REPORT, SOURCE, build_demo, sample_csv_bytes
)
from verify_customer_folder import verify_customer_folder


class KmongWeekendDemoTests(unittest.TestCase):
    def test_complete_synthetic_delivery_and_verified_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh-demo"
            report = build_demo(root)
            self.assertTrue(report["sample_only"])
            self.assertFalse(report["customer_data_used"])
            self.assertFalse(report["sale_approved"])
            self.assertFalse(report["independent_security_audit_completed"])
            self.assertEqual(report["new_cash_spend_krw"], 0)
            self.assertEqual(report["rows"], len(DEMO_ROWS))
            self.assertEqual((root / SOURCE).read_bytes(), sample_csv_bytes())
            self.assertEqual({p.name for p in root.iterdir()}, {
                SOURCE, LEAF, NOTICE, REPORT
            })
            self.assertEqual({p.name for p in (root / LEAF).iterdir()}, {
                "index.html", "delivery.zip", "receipt.json"
            })
            self.assertTrue(verify_customer_folder(root / LEAF)["verified"])
            self.assertEqual(json.loads((root / REPORT).read_text("utf-8")), report)
            self.assertIn("가상", (root / NOTICE).read_text("utf-8"))
            self.assertTrue((root / LEAF / "index.html").read_bytes().startswith(b"<!doctype html>"))

    def test_existing_output_rejected_without_modification(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "already-exists"
            root.mkdir()
            original = root / "owner.txt"
            original.write_bytes(b"PRESERVE")
            with self.assertRaises(FileExistsError):
                build_demo(root)
            self.assertEqual(original.read_bytes(), b"PRESERVE")
            self.assertEqual({p.name for p in root.iterdir()}, {"owner.txt"})

    def test_repeating_same_destination_cannot_clobber(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "demo"
            build_demo(root)
            before = (root / LEAF / "delivery.zip").read_bytes()
            with self.assertRaises(FileExistsError):
                build_demo(root)
            self.assertEqual((root / LEAF / "delivery.zip").read_bytes(), before)

    def test_independent_rebuild_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "one"
            second = Path(temporary) / "two"
            a, b = build_demo(first), build_demo(second)
            for item in ("source_sha256", "html_sha256", "zip_sha256", "receipt_sha256"):
                self.assertEqual(a[item], b[item])
            for name in ("index.html", "delivery.zip", "receipt.json"):
                self.assertEqual((first / LEAF / name).read_bytes(), (second / LEAF / name).read_bytes())

    def test_demo_only_contains_known_fictitious_rows(self):
        content = sample_csv_bytes().decode("utf-8")
        self.assertEqual(content.count("\n"), len(DEMO_ROWS) + 1)
        self.assertNotIn("@", content)
        self.assertNotIn("http", content.lower())
        self.assertNotIn("010-", content)
        self.assertIn("가상", content)


if __name__ == "__main__":
    unittest.main()
