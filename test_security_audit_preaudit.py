"""Independent auditor handoff tests: no actual audit or customer data."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import security_audit_preaudit as a


class SyntheticPreauditTests(unittest.TestCase):
    def test_all_scoped_adversarial_probes(self):
        checks = a.internal_synthetic_probes()
        self.assertEqual(set(checks), set(a.SCOPE))
        self.assertEqual(len(checks), 7)
        self.assertTrue(all(checks.values()), checks)

    def test_report_holds_rights_release_and_external_review(self):
        r = a.report()
        self.assertEqual(r["contract"], a.CONTRACT)
        self.assertEqual(r["score_addition"], 0)
        self.assertFalse(r["independent_security_audit_completed"])
        self.assertFalse(r["owner_rights_attested"])
        self.assertFalse(r["commercial_release_approved"])
        self.assertFalse(r["external_transfer_performed"])
        self.assertFalse(r["customer_source_inspected"])
        self.assertEqual(r["status"], "INTERNAL_SYNTHETIC_ONLY_EXTERNAL_AUDIT_PENDING")
        self.assertEqual(r["production_status"], "RELEASE_HOLD_SALE_NO_GO")

    def test_report_is_explicit_create_only_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "report.json"
            r = a.write_report(p)
            before = p.read_bytes()
            self.assertEqual(r["report_sha256"], a._sha(before))
            self.assertEqual(json.loads(before)["check_count"], 7)
            with self.assertRaises(FileExistsError):
                a.write_report(p)
            self.assertEqual(p.read_bytes(), before)

    def test_failure_does_not_write_any_report(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "report.json"
            with patch.object(a, "internal_synthetic_probes",
                              return_value={k: False for k in a.SCOPE}):
                with self.assertRaises(AssertionError):
                    a.write_report(p)
            self.assertFalse(p.exists())

    def test_output_contains_no_source_rows_or_machine_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "report.json"
            a.write_report(p)
            raw = p.read_text(encoding="utf-8")
            for forbidden in (
                "FAKE-DATA", "S1,", "S2,", "invalid.example",
                "XSS_PROBE=1", str(p), str(Path(temp)),
                "customer-original", "approval_signature", "actual_customer_acceptance",
            ):
                self.assertNotIn(forbidden, raw)


if __name__ == "__main__":
    unittest.main()
