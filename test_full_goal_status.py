"""Whole-blueprint 100% goal remains separate from the 85-point checkpoint."""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from full_goal_status import full_goal_report
from blueprint_score import DEFAULT
from zero_cost_gate import POLICY


class FinalGoal100Tests(unittest.TestCase):
    def test_full_goal_is_exactly_100_not_interim_85(self):
        report = full_goal_report()
        self.assertEqual(report["owner_final_goal"], 100)
        self.assertEqual(report["locked_scorecard_checkpoint"], 85)
        self.assertEqual(report["official_verified_points"], 72)
        self.assertEqual(report["remaining_to_full_goal"], 28)
        self.assertFalse(report["fully_completed"])
        self.assertFalse(report["checkpoint_reached"])

    def test_all_11_pending_requirements_are_explicit(self):
        report = full_goal_report()
        self.assertEqual(report["pending_requirement_ids"], [
            "R06","R07","R21","R23","R25","R26","R27","R29","R30","R32","R33"
        ])
        self.assertEqual(sum(report["pending_requirement_weights"].values()), 28)
        self.assertTrue(report["all_33_final_blueprint_requirements_in_scope"])

    def test_no_fake_sale_or_independent_audit(self):
        report = full_goal_report()
        for field in (
            "buyer_acceptance_verified",
            "independent_human_security_audit_verified",
            "shipping_ip_and_customer_data_rights_verified",
            "marketplace_sale_approved",
            "fully_completed",
        ):
            self.assertIs(report[field], False)
        self.assertEqual(report["cash_spend_approved_krw"], 0)
        self.assertEqual(report["work_marker"], "[작업중]")
        self.assertEqual(report["release_status"], "RELEASE_HOLD_SALE_NO_GO")

    def test_fake_completed_score_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"fake_score.json"
            fake=json.loads(DEFAULT.read_text("utf-8"))
            for row in fake["items"]:
                if row["state"] == "PENDING":
                    row["state"] = "VERIFIED"
                    row["source_code_sha"] = "a" * 40
            target.write_text(json.dumps(fake, ensure_ascii=False), "utf-8")
            with self.assertRaises(ValueError):
                full_goal_report(score_path=target)

    def test_unapproved_paid_policy_never_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"paid_policy.json"
            paid=json.loads(POLICY.read_text("utf-8"))
            paid["approved_upfront_budget_krw"] = 1000
            target.write_text(json.dumps(paid, ensure_ascii=False), "utf-8")
            with self.assertRaises(ValueError):
                full_goal_report(policy_path=target)

    def test_cli_ascii_windows_compatible_and_not_falsely_100(self):
        root=Path(__file__).resolve().parent
        completed=subprocess.run(
            [sys.executable, str(root/"full_goal_status.py")],
            cwd=root, capture_output=True, text=True,
            encoding="cp1252", errors="strict", timeout=30,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(completed.stdout.isascii())
        doc=json.loads(completed.stdout)
        self.assertEqual(doc["remaining_to_full_goal"], 28)
        self.assertFalse(doc["fully_completed"])


if __name__ == "__main__":
    unittest.main()
