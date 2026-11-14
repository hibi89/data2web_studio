"""Regression: do not alter owner-approved R01–R33 denominator or fake 85%."""
import json
import tempfile
import unittest
from pathlib import Path

from blueprint_score import APPROVED_WEIGHTS,DEFAULT,evaluate_scorecard


class ApprovedBlueprintScale(unittest.TestCase):
    def setUp(self):
        self.doc=json.loads(DEFAULT.read_text(encoding="utf-8"))

    def evaluate_modified(self,change):
        with tempfile.TemporaryDirectory() as root:
            out=Path(root)/"score.json"
            change(self.doc)
            out.write_text(json.dumps(self.doc,ensure_ascii=False),encoding="utf-8")
            return evaluate_scorecard(out)

    def test_legacy_windows_console_cp1252_score_json_is_safe(self):
        # The CLI is invoked in a Windows runner whose PowerShell output
        # encoding can be cp1252, regardless of JSON data language.
        import subprocess
        import sys
        process=subprocess.run([sys.executable,"blueprint_score.py"],
             cwd=DEFAULT.parent.parent,capture_output=True,text=True,
             encoding="cp1252",errors="strict",check=False)
        self.assertEqual(process.returncode,0,process.stdout+process.stderr)
        payload=json.loads(process.stdout)
        self.assertEqual(payload["weighted_verified_score"],72)
        self.assertEqual(payload["work_marker"],"[작업중]")
        self.assertTrue(process.stdout.isascii())

    def test_true_full_denominator_and_locked_r_weights(self):
        score=evaluate_scorecard()
        self.assertEqual(score["all_requirements"],33)
        self.assertEqual(len(APPROVED_WEIGHTS),33)
        self.assertEqual(sum(APPROVED_WEIGHTS),100)
        self.assertEqual(score["weighted_verified_score"],72)
        self.assertEqual(score["weighted_pending_score"],28)
        self.assertEqual(score["remaining_to_target"],13)
        self.assertFalse(score["target_reached"])
        self.assertEqual(score["sale_status"],"RELEASE_HOLD_SALE_NO_GO")

    def test_unapproved_weight_change_fails(self):
        def mutate(x):
            x["items"][0]["weight"]+=1
            x["items"][1]["weight"]-=1
        with self.assertRaisesRegex(ValueError,"Frozen owner-selected"):
            self.evaluate_modified(mutate)

    def test_delete_requirement_fails(self):
        with self.assertRaises(ValueError):
            self.evaluate_modified(lambda x:x["items"].pop())

    def test_duplicate_requirement_fails(self):
        with self.assertRaises(ValueError):
            self.evaluate_modified(lambda x:x["items"].__setitem__(1,x["items"][0]))

    def test_premature_release_fails(self):
        with self.assertRaisesRegex(ValueError,"Never auto-release"):
            self.evaluate_modified(lambda x:x.update(release_status="SALE_GO"))

    def test_fake_completed_without_sha_fails(self):
        with self.assertRaisesRegex(ValueError,"exact source SHA"):
            self.evaluate_modified(lambda x:x["items"][5].update(state="VERIFIED"))

    def test_pending_item_cannot_claim_verified_sha(self):
        with self.assertRaisesRegex(ValueError,"Pending requirement"):
            self.evaluate_modified(lambda x:x["items"][5].update(source_code_sha="f"*40))

    def test_changed_blueprint_source_fails(self):
        with self.assertRaisesRegex(ValueError,"denominator"):
            self.evaluate_modified(lambda x:x.update(original_blueprint=["README.md"]))

    def test_corrupt_json_duplicate_key_fails(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"duplicate.json"
            s=DEFAULT.read_text(encoding="utf-8")
            self.assertIn('"denominator": 100',s)
            path.write_text(s.replace('"denominator": 100',
                     '"denominator": 100, "denominator": 100',1),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"Duplicate"):
                evaluate_scorecard(path)

    def test_scope_customer_acceptance_never_automatically_certified(self):
        with self.assertRaisesRegex(ValueError,"Customer acceptance"):
            self.evaluate_modified(lambda x:x["evidence_baseline"].update(
                actual_customer_acceptance="VERIFIED"))

if __name__=="__main__":
    unittest.main()
