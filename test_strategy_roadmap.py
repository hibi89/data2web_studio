"""Roadmap is declarative: cannot grant points or commercial permission."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
ROADMAP = ROOT / "data" / "a_first_b_later_roadmap_v1.json"
SCORE = ROOT / "data" / "final_blueprint_scorecard_v1.json"


class RoadmapContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
        cls.score = json.loads(SCORE.read_text(encoding="utf-8"))

    def test_authorization_does_not_grant_release(self):
        doc=self.roadmap
        self.assertEqual(doc["contract"],"DATA2WEB_A_FIRST_B_LATER_ROADMAP_V1")
        self.assertEqual(doc["owner_direction_authorized"],
                         "A_RESULT_DELIVERY_FIRST_B_NATIVE_EXE_LATER")
        self.assertIn("NOT_LICENSE",doc["authorization_limits"])
        controls=doc["release_controls"]
        self.assertFalse(controls["sale_approved"])
        self.assertFalse(controls["product_listing_approved"])
        self.assertFalse(controls["customer_source_upload_approved"])
        self.assertFalse(controls["paid_external_audit_approved"])
        self.assertEqual(controls["working_marker"],"[작업중]")
        self.assertEqual(controls["release_status"],"RELEASE_HOLD_SALE_NO_GO")

    def test_scorecard_is_immutable_source_of_truth(self):
        doc=self.roadmap
        score=self.score
        self.assertEqual(doc["scorecard_path"],"data/final_blueprint_scorecard_v1.json")
        self.assertEqual(score["denominator"],100)
        self.assertEqual(score["item_count"],33)
        items=score["items"]
        self.assertEqual(len({x["id"] for x in items}),33)
        self.assertEqual(sum(x["weight"] for x in items),100)
        actual=sum(x["weight"] for x in items if x["state"]=="VERIFIED")
        self.assertEqual(actual,doc["baseline_verified_points"])
        self.assertEqual(actual,72)
        self.assertEqual(doc["target_points"],85)
        self.assertEqual(score["release_status"],"RELEASE_HOLD_SALE_NO_GO")

    def test_milestones_are_all_pending_and_do_not_double_count(self):
        doc=self.roadmap
        weights={x["id"]:x["weight"] for x in self.score["items"]}
        outstanding={x["id"] for x in self.score["items"] if x["state"]=="PENDING"}
        milestones=doc["milestones"]
        self.assertEqual([x["id"] for x in milestones],
                         ["A_TO_85","A_85_TO_95","FULL_BLUEPRINT_95_TO_100"])
        seen=set()
        verified=doc["baseline_verified_points"]
        for milestone in milestones:
            ids=milestone["requirements"]
            self.assertEqual(len(ids),len(set(ids)))
            self.assertFalse(seen.intersection(ids))
            self.assertTrue(set(ids).issubset(outstanding))
            seen.update(ids)
            self.assertEqual(milestone["current_points_added"],0)
            verified+=sum(weights[item] for item in ids)
            self.assertEqual(milestone["target_points_after_full_acceptance"],verified)
            self.assertNotEqual(milestone["status"],"COMPLETE")
        self.assertEqual(seen,outstanding)
        self.assertEqual(verified,100)
        self.assertEqual(sum(weights[i] for i in milestones[0]["requirements"]),13)

    def test_future_tracks_not_implicitly_published(self):
        ids={m["id"] for m in self.roadmap["post_blueprint_future"]}
        self.assertEqual(ids,{"B_NATIVE_EXE_COMMERCIAL","AX_SCALE_AUTOMATION"})
        for item in self.roadmap["post_blueprint_future"]:
            self.assertTrue(item["status"].startswith("FUTURE"))
            self.assertTrue(item["prerequisites"])


if __name__=="__main__":
    unittest.main()
