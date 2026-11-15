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
        self.assertEqual(len(checks), 14)
        self.assertTrue(all(checks.values()), checks)

    def test_extended_xlsx_negatives_are_rejected_without_network(self):
        for key, opts in (
            ("XLSX_EXTERNAL_REL_BLOCKED", {"external": True}),
            ("XLSX_ZIP_BOMB_BLOCKED", {"compress_bomb": True}),
            ("XLSX_MACRO_MEMBER_BLOCKED", {"macro": True}),
        ):
            with self.subTest(probe=key):
                self.assertTrue(a._rejected_xlsx(a._adversarial_xlsx(**opts)))

    def test_tampered_xlsx_or_zip_verifier_cannot_generate_report(self):
        # A softened security verifier must cause HOLD, not a PASS report.
        for func in ("_rejected_xlsx", "_rejected_zip"):
            with self.subTest(verifier=func), tempfile.TemporaryDirectory() as temp:
                report_path = Path(temp) / "never-published.json"
                with patch.object(a, func, return_value=False):
                    with self.assertRaisesRegex(
                        AssertionError, "Internal synthetic threat probes"
                    ):
                        a.write_report(report_path)
                self.assertFalse(report_path.exists())

    def test_network_and_static_csp_probes_have_explicit_result_flags(self):
        checks = a.internal_synthetic_probes()
        for critical in (
            "STATIC_SCRIPT_HASH_MATCHED", "NETWORK_MARKUP_ABSENT",
            "ZIP_SLIP_BLOCKED", "ZIP_SYMLINK_BLOCKED",
            "XLSX_EXTERNAL_REL_BLOCKED", "XLSX_ZIP_BOMB_BLOCKED",
            "XLSX_MACRO_MEMBER_BLOCKED",
        ):
            with self.subTest(probe=critical):
                self.assertIn(critical, checks)
                self.assertIs(checks[critical], True)

    def test_report_holds_rights_release_and_external_review(self):
        r = a.report()
        self.assertEqual(r["contract"], a.CONTRACT)
        self.assertEqual(r["score_addition"], 0)
        self.assertFalse(r["independent_security_audit_completed"])
        self.assertFalse(r["owner_rights_attested"])
        self.assertFalse(r["commercial_release_approved"])
        self.assertFalse(r["external_transfer_performed"])
        self.assertFalse(r["customer_source_inspected"])
        self.assertIn(r["status"], (
            "INTERNAL_SYNTHETIC_SECURITY_HOLD_EXTERNAL_AUDIT_PENDING",
            "INTERNAL_SYNTHETIC_ONLY_EXTERNAL_AUDIT_PENDING",
        ))
        self.assertIs(r["technical_security_clearance"], False)
        self.assertEqual(bool(r["open_security_findings"]),
                         r["status"].startswith("INTERNAL_SYNTHETIC_SECURITY_HOLD"))
        self.assertEqual(r["production_status"], "RELEASE_HOLD_SALE_NO_GO")

    def test_navigation_finding_cannot_be_concealed_by_clean_original_probes(self):
        for accepted in (False, True):
            with self.subTest(rehashed_navigation_accepted=accepted):
                synthetic = {
                    "verifier_accepted_rehashed_navigation": accepted,
                    "external_network_request_performed": False,
                    "actual_browser_navigation_tested": False,
                    "status": ("SECURITY_HOLD_CANDIDATE_CONFIRMED" if accepted
                               else "MODIFIED_NAVIGATION_REJECTED_BY_VERIFIER"),
                }
                with patch.object(a, "assess_rehashed_navigation",
                                  return_value=synthetic):
                    result = a.report()
                self.assertIs(result["technical_security_clearance"], False)
                self.assertEqual(bool(result["open_security_findings"]), accepted)
                self.assertEqual(result["rehashed_navigation_probe"],
                                 synthetic["status"])
                self.assertFalse(result["independent_security_audit_completed"])
                self.assertFalse(result["commercial_release_approved"])
                self.assertEqual(result["score_addition"], 0)
                if accepted:
                    self.assertEqual(
                        result["status"],
                        "INTERNAL_SYNTHETIC_SECURITY_HOLD_EXTERNAL_AUDIT_PENDING",
                    )
                else:
                    self.assertEqual(
                        result["status"],
                        "INTERNAL_SYNTHETIC_ONLY_EXTERNAL_AUDIT_PENDING",
                    )

    def test_report_is_explicit_create_only_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "report.json"
            r = a.write_report(p)
            before = p.read_bytes()
            self.assertEqual(r["report_sha256"], a._sha(before))
            self.assertEqual(json.loads(before)["check_count"], 14)
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
