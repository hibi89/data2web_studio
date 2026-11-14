"""Manual evidence intake must not silently grant independent buyer acceptance."""
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from kmong_weekend_demo import build_demo
from kmong_independent_buyer_request import create_request
from buyer_self_report_intake import assess_self_report


class BuyerSelfReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.preview = self.root / "demo"
        build_demo(self.preview)
        self.sha = "a" * 40
        self.request = self.root / "request.zip"
        create_request(self.request, self.preview, source_sha=self.sha)
        with ZipFile(self.request) as archive:
            self.form = json.loads(archive.read("REVIEW_FORM_BLANK.json"))
        self.report = self.root / "report.json"

    def submit(self, form=None):
        self.report.write_text(json.dumps(self.form if form is None else form), "utf-8")
        return assess_self_report(self.request, self.report)

    def claimed_pass(self):
        record = dict(self.form)
        record["actual_real_device_run"] = True
        record["reviewer_independent_of_development"] = True
        record["reviewer_device_os"] = "Windows 11"
        record["browser_and_version"] = "Edge 143.0.0.0"
        record["observed_result"] = "PASS"
        record["steps"] = {key: "PASS" for key in self.form["steps"]}
        return record

    def test_blank_cannot_be_pretended_as_completed(self):
        result = self.submit()
        self.assertEqual(result["status"], "HOLD_INCOMPLETE_DEVICE_TEST")
        self.assertEqual(result["score_added"], 0)
        self.assertFalse(result["buyer_acceptance_verified"])

    def test_claimed_independent_all_pass_still_needs_human_verification(self):
        result = self.submit(self.claimed_pass())
        self.assertEqual(result["status"], "CANDIDATE_FOR_EXTERNAL_HUMAN_REVIEW_ONLY")
        self.assertFalse(result["external_human_verified"])
        self.assertFalse(result["report_is_authenticated"])
        self.assertFalse(result["sale_approved"])
        self.assertEqual(result["score_added"], 0)

    def test_failed_step_cannot_be_marked_pass(self):
        form = self.claimed_pass()
        form["steps"]["network_zero"] = "FAIL"
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.submit(form)
        form["observed_result"] = "FAIL"
        self.assertEqual(self.submit(form)["status"], "HOLD_OBSERVED_FAILURE")

    def test_not_independent_never_candidate(self):
        form = self.claimed_pass()
        form["reviewer_independent_of_development"] = False
        self.assertEqual(self.submit(form)["status"], "HOLD_NOT_INDEPENDENT")

    def test_private_fields_and_free_text_forbidden(self):
        for key in ("email", "reviewer_name", "customer_filename", "contact"):
            form = self.claimed_pass()
            form[key] = "sensitive"
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "identifying"):
                    self.submit(form)

    def test_claimed_sale_security_rights_and_100pts_refused(self):
        for key in ("sale_approved", "buyer_acceptance_verified",
                    "independent_human_security_audit_completed",
                    "source_data_rights_verified", "claim_to_100_points"):
            form = self.claimed_pass()
            form[key] = True
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "cannot authorize"):
                    self.submit(form)

    def test_invalid_os_browser_and_types_rejected(self):
        forms = []
        form = self.claimed_pass()
        form["reviewer_device_os"] = "Windows 11 user@example.com"
        forms.append(form)
        form = self.claimed_pass()
        form["browser_and_version"] = "Edge 143 /John Doe"
        forms.append(form)
        form = self.claimed_pass()
        form["actual_real_device_run"] = "true"
        forms.append(form)
        form = self.claimed_pass()
        form["steps"]["print"] = True
        forms.append(form)
        for form in forms:
            with self.assertRaises(ValueError):
                self.submit(form)

    def test_source_commit_must_match_request(self):
        form = self.claimed_pass()
        form["request_source_sha"] = "b"*40
        with self.assertRaisesRegex(ValueError, "Wrong origin"):
            self.submit(form)

    def test_fake_steps_without_declared_run_refused(self):
        form = self.claimed_pass()
        form["actual_real_device_run"] = False
        with self.assertRaisesRegex(ValueError, "without a claimed"):
            self.submit(form)

    def test_missing_step_and_oversized_report_refused(self):
        form = self.claimed_pass()
        del form["steps"]["network_zero"]
        with self.assertRaisesRegex(ValueError, "All named"):
            self.submit(form)
        self.report.write_bytes(b" " * 9000)
        with self.assertRaises(ValueError):
            assess_self_report(self.request, self.report)


    def test_report_path_is_read_once_for_integrity_and_validation(self):
        from unittest.mock import patch
        import buyer_self_report_intake as intake
        self.report.write_text(json.dumps(self.claimed_pass()), "utf-8")
        original = intake.read_bounded_source
        paths = []
        def tracking(path, **kw):
            paths.append(str(path))
            return original(path, **kw)
        with patch.object(intake, "read_bounded_source", side_effect=tracking):
            verdict = assess_self_report(self.request, self.report)
        self.assertEqual(paths.count(str(self.report)), 1)
        self.assertEqual(verdict["report_sha256"],
                         __import__("hashlib").sha256(self.report.read_bytes()).hexdigest())
        self.assertFalse(verdict["buyer_acceptance_verified"])


if __name__ == "__main__":
    unittest.main()
