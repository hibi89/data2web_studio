"""Read-only whole-blueprint 100-point GO/NO-GO report.

The locked original scorecard still carries the older 85-point milestone.
The owner's current FINAL goal is 100/100, not a reweighted or narrowed scope.
Never converts an interim milestone, synthetic CI, CodeQL, or self-attestation
into actual buyer, rights, independent-audit, or commercial release evidence.
"""
from __future__ import annotations

import json
from blueprint_score import DEFAULT, evaluate_scorecard
from zero_cost_gate import POLICY, _read, validate_policy

CONTRACT = "DATA2WEB_FULL_BLUEPRINT_GOAL_100_REPORT_V1"
FINAL_GOAL = 100
NONNEGOTIABLE_EXTERNAL = frozenset({
    "R06","R07","R21","R23","R25","R26","R27","R29","R30","R32","R33"
})


def full_goal_report(score_path=DEFAULT, policy_path=POLICY):
    score = evaluate_scorecard(score_path)
    original = _read(score_path)
    policy = _read(policy_path)
    validate_policy(policy, original)
    items = original["items"]
    pending = [item for item in items if item["state"] == "PENDING"]
    if not pending or {item["id"] for item in pending} != NONNEGOTIABLE_EXTERNAL:
        # This v1 attests exactly to the current baseline; it never
        # silently treats future evidence changes as official authorization.
        raise ValueError("Any completed requirement needs a versioned evidence review")
    pending_weight = sum(item["weight"] for item in pending)
    verified = score["weighted_verified_score"]
    if verified + pending_weight != FINAL_GOAL or verified != 72:
        raise ValueError("Frozen 100-point ledger is inconsistent")
    if policy["approved_upfront_budget_krw"] != 0:
        raise ValueError("Unapproved spending")
    if score["sale_status"] != "RELEASE_HOLD_SALE_NO_GO":
        raise ValueError("Unexpected release approval")
    return {
        "contract": CONTRACT,
        "owner_final_goal": FINAL_GOAL,
        "locked_scorecard_checkpoint": score["target"],
        "checkpoint_reached": score["target_reached"],
        "official_verified_points": verified,
        "official_unverified_points": pending_weight,
        "remaining_to_full_goal": FINAL_GOAL - verified,
        "pending_requirement_ids": [item["id"] for item in pending],
        "pending_requirement_weights": {
            item["id"]: item["weight"] for item in pending
        },
        "all_33_final_blueprint_requirements_in_scope": True,
        "fully_completed": False,
        "buyer_acceptance_verified": False,
        "independent_human_security_audit_verified": False,
        "shipping_ip_and_customer_data_rights_verified": False,
        "marketplace_sale_approved": False,
        "cash_spend_approved_krw": 0,
        "release_status": "RELEASE_HOLD_SALE_NO_GO",
        "work_marker": "[작업중]",
        "scorecard_version_change": "REQUIRES_REAL_EVIDENCE_AND_VERSIONED_APPROVAL",
    }


def main():
    # ASCII-safe to display on older Windows console code pages.
    print(json.dumps(full_goal_report(), ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
