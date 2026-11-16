"""Zero-cost directive may approve policy, never fabricate customer/IP/independent-audit evidence."""
import unittest
from copy import deepcopy
from zero_cost_gate import _no_duplicate_keys, inspect_policy, validate_policy, _read, POLICY, SCORE

class ZeroCostGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = _read(POLICY)
        cls.score = _read(SCORE)

    def test_current_policy_and_original_score_safe(self):
        result = inspect_policy()
        self.assertTrue(result["policy_valid"])
        self.assertEqual(result["new_spend_krw"], 0)
        self.assertEqual(result["weighted_verified_score"], 72)
        self.assertFalse(result["independent_human_audit"])
        self.assertEqual(result["sale_status"], "RELEASE_HOLD_SALE_NO_GO")

    def test_paid_infrastructure_and_security_service_refused(self):
        for field, bad in (("approved_upfront_budget_krw",1),
                           ("any_paid_service_or_purchase_allowed",True),
                           ("use_paid_code_signing",True),
                           ("use_paid_security_audit",True),
                           ("use_paid_ai_or_cloud_api",True),
                           ("use_paid_runner",True)):
            with self.subTest(field=field):
                changed=deepcopy(self.policy)
                changed[field]=bad
                with self.assertRaises(ValueError): validate_policy(changed,self.score)

    def test_unapproved_data_and_fake_audit_refused(self):
        for field in ("source_customer_upload_to_github_or_ai",
                      "security_scan_is_independent_human_audit",
                      "external_independent_audit_completed",
                      "actual_marketplace_listing_approved",
                      "shipping_ip_rights_evidence_complete",
                      "per_customer_data_rights_verified"):
            with self.subTest(field=field):
                changed=deepcopy(self.policy)
                changed[field]=True
                with self.assertRaises(ValueError): validate_policy(changed,self.score)

    def test_retention_and_no_autodelete_constrained(self):
        doc=deepcopy(self.policy)
        doc["operator_local_customer_data_max_retention_days"]=365
        with self.assertRaises(ValueError):validate_policy(doc,self.score)
        doc=deepcopy(self.policy)
        doc["source_deletion_mode"]="AUTOMATIC_DELETE"
        with self.assertRaises(ValueError):validate_policy(doc,self.score)

    def test_zero_budget_not_same_as_zero_price(self):
        self.assertEqual([x["price_krw"] for x in self.policy["skus"]],
                         [49000,129000,249000])
        changed=deepcopy(self.policy)
        changed["skus"][0]["price_krw"]=0
        with self.assertRaises(ValueError):validate_policy(changed,self.score)

    def test_score_cannot_change_without_acceptance(self):
        score=deepcopy(self.score)
        next(x for x in score["items"] if x["id"]=="R29")["state"]="VERIFIED"
        with self.assertRaises(ValueError):validate_policy(self.policy,score)

    def test_duplicate_json_key_rejected(self):
        with self.assertRaises(ValueError):
            __import__("json").loads('{"budget":0,"budget":1}',object_pairs_hook=_no_duplicate_keys)

if __name__=="__main__":
    unittest.main()
