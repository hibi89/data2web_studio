"""Regression: anonymous scope gate never touches a customer source or sells."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from order_intake_preflight import (
    assess, parse_request, synthetic_example, write_new_report
)

def check(doc):
    return assess(parse_request(json.dumps(doc).encode("utf-8")))

class PreorderTests(unittest.TestCase):
    def test_basic_3_formats(self):
        for kind in ("CSV", "TSV", "JSON"):
            data = synthetic_example()
            data["sources"][0]["format"] = kind
            r = check(data)
            self.assertEqual((r["sku"], r["suggested_price_krw"]), ("BASIC", 49000))
            self.assertFalse(r["sale_approved"])

    def test_pro_one_xlsx_and_three_csv(self):
        one = synthetic_example()
        one["sources"][0]["format"] = "XLSX"
        self.assertEqual(check(one)["sku"], "PRO")
        three = synthetic_example()
        three["sources"] = three["sources"] * 3
        self.assertEqual(check(three)["sku"], "PRO")

    def test_business_10_mixed(self):
        doc = synthetic_example()
        doc["sources"] = [dict(doc["sources"][0], format=kind, estimated_rows=800)
                          for kind in ("CSV","TSV","JSON","XLSX","CSV",
                                       "TSV","JSON","XLSX","CSV","TSV")]
        r = check(doc)
        self.assertEqual((r["sku"], r["suggested_price_krw"]), ("BUSINESS", 249000))

    def test_missing_rights_sensitive_confidential_plaintext(self):
        for key, value in (
            ("rights_claimed", False), ("contains_personal_or_sensitive", True),
            ("contains_third_party_confidential", True), ("plaintext_ack", False),
            ("mapping_3_distinct_columns", False),
        ):
            with self.subTest(key=key):
                doc = synthetic_example()
                doc[key] = value
                r = check(doc)
                self.assertEqual(r["status"], "HOLD_PREORDER")
                self.assertFalse(r["order_accepted"])
                self.assertIsNone(r["suggested_price_krw"])

    def test_multiple_sources_need_identical_headers(self):
        doc = synthetic_example()
        doc["sources"] = doc["sources"] * 2
        doc["same_headers"] = False
        self.assertEqual(check(doc)["reason"], "SAME_HEADERS_NOT_CONFIRMED")

    def test_limits_reject_without_adding_customer_info(self):
        for field, value in (
            ("estimated_bytes", 8000001), ("estimated_columns", 2),
            ("estimated_columns", 21), ("estimated_rows", 0)
        ):
            with self.subTest(field=field):
                d = synthetic_example()
                d["sources"][0][field] = value
                self.assertEqual(check(d)["status"], "HOLD_PREORDER")
        d = synthetic_example()
        d["sources"] = d["sources"] * 11
        self.assertEqual(check(d)["reason"], "TOO_MANY_SOURCES")

    def test_one_large_csv_no_business_fallback(self):
        d = synthetic_example()
        d["sources"][0]["estimated_rows"] = 6000
        self.assertIsNone(check(d)["sku"])

    def test_reject_unknown_personal_keys(self):
        for key, value in (("customer_name", "X"), ("file_path", "secret.csv"),
                           ("column_name", "name"), ("email", "any@example.com")):
            with self.subTest(key=key):
                d = synthetic_example()
                d[key] = value
                with self.assertRaises(ValueError):
                    parse_request(json.dumps(d).encode())

    def test_duplicate_nonfinite_and_oversized_json(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b" " * 16385, b"[]"):
            with self.assertRaises(ValueError):
                parse_request(raw)

    def test_bool_is_not_integer_and_strings_not_booleans(self):
        for invalid in (True, -1, "3", 1.5, 1000000001):
            d = synthetic_example()
            d["sources"][0]["estimated_rows"] = invalid
            with self.assertRaises(ValueError):
                parse_request(json.dumps(d).encode())
        d = synthetic_example()
        d["rights_claimed"] = "true"
        with self.assertRaises(ValueError):
            parse_request(json.dumps(d).encode())

    def test_new_report_no_overwrite_and_no_identifiers(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "new.json"
            result = check(synthetic_example())
            write_new_report(target, result)
            before = target.read_bytes()
            self.assertNotIn(b"@", before)
            with self.assertRaises(FileExistsError):
                write_new_report(target, result)
            self.assertEqual(before, target.read_bytes())

    def test_cli_offline_real_python(self):
        root = Path(__file__).parent
        p = subprocess.run([sys.executable, str(root / "order_intake_preflight.py"),
                            "--synthetic-self-check"], cwd=str(root),
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["sku"], "BASIC")
        self.assertFalse(json.loads(p.stdout)["sale_approved"])

if __name__ == "__main__":
    unittest.main()
