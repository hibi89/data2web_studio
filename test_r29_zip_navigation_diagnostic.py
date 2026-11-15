"""Do not misclassify a ZIP navigation diagnostic as security acceptance."""
import json
import unittest
from r29_zip_navigation_diagnostic import assess_rehashed_navigation, CONTRACT


class NavigationDiagnostic(unittest.TestCase):
    def test_modified_html_probe_always_reports_real_result_and_hold(self):
        report = assess_rehashed_navigation()
        self.assertEqual(report["contract"], CONTRACT)
        self.assertTrue(report["synthetic_control_verified"])
        self.assertTrue(report["high_guard_accepted_pristine_html"])
        self.assertTrue(report["high_guard_rejected_modified_html"])
        self.assertEqual(report["zip_member_count"], 3)
        self.assertFalse(report["actual_browser_navigation_tested"])
        self.assertFalse(report["external_network_request_performed"])
        self.assertFalse(report["independent_security_audit_completed"])
        self.assertFalse(report["commercial_release_approved"])
        self.assertEqual(report["score_addition"], 0)
        self.assertEqual(
            report["status"],
            ("SECURITY_HOLD_CANDIDATE_CONFIRMED"
             if report["verifier_accepted_rehashed_navigation"]
             else "MODIFIED_NAVIGATION_REJECTED_BY_VERIFIER")
        )
        # Diagnostic evidence only: a technical finding is never a PASS.
        print("R29_NAVIGATION_DIAGNOSTIC=" + json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
