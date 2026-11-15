"""Internal commercial terms must match approved zero-cost defaults."""
import copy
import json
from pathlib import Path
import unittest
from commercial_terms_consistency import validate_commercial_terms

ROOT = Path(__file__).resolve().parent


class CommercialTermsConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.markdown = (ROOT / "docs" / "COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md").read_text("utf-8")
        cls.defaults = json.loads((ROOT / "data" / "zero_cost_owner_policy_v1.json").read_text("utf-8"))

    def test_approved_internal_matrix_matches_source_policy(self):
        result = validate_commercial_terms(self.markdown, self.defaults)
        self.assertTrue(result["internal_terms_consistent"])
        self.assertTrue(result["owner_approved_internal_defaults"])
        self.assertFalse(result["marketplace_listing_approved"])
        self.assertFalse(result["tax_or_legal_review_completed"])
        self.assertFalse(result["sale_approved"])
        self.assertEqual(result["score_added"], 0)

    def test_price_revision_support_and_scope_drift_rejected(self):
        changes = (
            ("**49,000원**", "**49,001원**"),
            ("**1회**", "**9회**"),
            ("**7일**", "**30일**"),
            ("최대 1,000행·20열", "최대 1,001행·20열"),
            ("최대 3개", "최대 4개"),
        )
        for old, new in changes:
            with self.subTest(old=old):
                with self.assertRaises(ValueError):
                    validate_commercial_terms(self.markdown.replace(old, new, 1), self.defaults)

    def test_external_or_unpublished_gate_cannot_be_weakened(self):
        for key, value in (
            ("actual_marketplace_listing_approved", True),
            ("sku_policy_status", "PUBLISHED"),
            ("release_status", "SALE_GO"),
        ):
            changed = copy.deepcopy(self.defaults)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_commercial_terms(self.markdown, changed)

    def test_removed_rights_and_refund_disclosures_rejected(self):
        for phrase in ("법률상", "전면 환불불가 금지", "SALE NO-GO"):
            changed = self.markdown.replace(phrase, "삭제", 1)
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                validate_commercial_terms(changed, self.defaults)


if __name__ == "__main__":
    unittest.main()
