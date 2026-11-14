"""Shipping asset chain audit is synthetic, zero-permission and fail-closed."""
from __future__ import annotations

import json
import unittest
from copy import deepcopy

from shipping_rights_preflight import (
    _unique_keys, read_inventory, synthetic_shipping_preflight,
    validate_inventory,
)


class ShippingRightsPreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = read_inventory()

    def test_manifest_matches_real_synthetic_zip_receipt_and_stays_hold(self):
        result = synthetic_shipping_preflight()
        self.assertTrue(result["technical_synthetic_integrity_verified"])
        self.assertEqual(result["shipping_member_count"], 4)
        self.assertEqual(result["status"], "HOLD_OWNER_IP_NOTICE_EXTERNAL_AUDIT")
        self.assertFalse(result["commercial_release_approved"])
        self.assertFalse(result["external_independent_audit_completed"])
        self.assertEqual(result["score_addition"], 0)

    def test_unapproved_rights_and_external_audit_claims_rejected(self):
        for field in ("rights_owner_attested", "commercial_distribution_approved",
                      "third_party_vendor_inventory_complete", "audit_is_independent",
                      "any_customer_source_inspected", "scorecard_change_requested"):
            with self.subTest(field=field):
                changed = deepcopy(self.record)
                changed[field] = True
                with self.assertRaises(ValueError):
                    validate_inventory(changed)

    def test_extra_or_removed_shipping_assets_rejected(self):
        for mode in ("extra", "removed", "duplicate"):
            with self.subTest(mode=mode):
                doc = deepcopy(self.record)
                if mode == "extra":
                    doc["artifacts"].append(
                        dict(doc["artifacts"][0], name="PRIVATE_CUSTOMER.csv"))
                elif mode == "removed":
                    doc["artifacts"].pop()
                else:
                    doc["artifacts"][1] = doc["artifacts"][0]
                with self.assertRaises(ValueError):
                    validate_inventory(doc)

    def test_license_notice_falsely_inserted_rejected(self):
        doc = deepcopy(self.record)
        doc["actual_shipped_license_notice_files"] = ["LICENSE"]
        with self.assertRaises(ValueError):
            validate_inventory(doc)
        doc = deepcopy(self.record)
        doc["rights_approval_state"] = "APPROVED"
        with self.assertRaises(ValueError):
            validate_inventory(doc)

    def test_fake_commercial_license_in_technical_rights_state_rejected(self):
        doc=deepcopy(self.record)
        doc["artifacts"][0]["rights_state"]="LICENSE_GRANTED"
        with self.assertRaises(ValueError):
            validate_inventory(doc)
        doc=deepcopy(self.record)
        doc["artifacts"][1]["vendor_notice_reviewed"]=True
        with self.assertRaises(ValueError):
            validate_inventory(doc)

    def test_duplicate_registry_json_key_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"sale_approved": false, "sale_approved": true}',
                       object_pairs_hook=_unique_keys)


if __name__=="__main__":
    unittest.main()
