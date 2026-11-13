"""Fixed, owner-delegated 100-point R01–R33 completion contract.

This validates the arithmetic and evidence ledger, NOT the underlying customer
rights or hosted CI log independently. No network, GitHub credentials, or
customer input is opened. The 85% goal and SALE_NO_GO are separate gates.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DEFAULT=ROOT/"data"/"final_blueprint_scorecard_v1.json"

APPROVED_WEIGHTS=(
    3,3,4,2,2,2,2,
    4,3,4,3,3,3,
    5,5,3,3,4,3,3,
    4,4,3,3,2,2,2,
    3,3,2,2,3,3,
)
EXPECTED_IDS=tuple(f"R{i:02d}" for i in range(1,34))
VALID_STATES=frozenset(("VERIFIED","PENDING"))


def _unique_pairs(pairs):
    out={}
    for key,value in pairs:
        if key in out:
            raise ValueError(f"Duplicate scorecard JSON key: {key}")
        out[key]=value
    return out


def _reject_constant(value):
    raise ValueError("NaN/Infinity not valid in scorecard")


def evaluate_scorecard(path=DEFAULT):
    doc=json.loads(Path(path).read_text(encoding="utf-8"),
                   object_pairs_hook=_unique_pairs,parse_constant=_reject_constant)
    if not isinstance(doc,dict) or doc.get("contract")!="DATA2WEB_OWNER_APPROVED_100_POINT_SCORECARD_V1":
        raise ValueError("Unexpected scoring contract")
    if doc.get("denominator")!=100 or doc.get("target_score")!=85:
        raise ValueError("Only whole-blueprint 100 point scale and owner 85 target allowed")
    if doc.get("weights_status")!="OWNER_DELEGATED_APPROVED" or doc.get("owner_approval_scope")!=(
        "SCORING_SCALE_AND_FIXED_R01_R33_WEIGHTS_ONLY_NOT_RELEASE"):
        raise ValueError("Owner approval only covers weights, not sales")
    if (doc.get("release_status")!="RELEASE_HOLD_SALE_NO_GO" or
        doc.get("owner_work_marker")!="[작업중]"):
        raise ValueError("Never auto-release or clear the in-progress marker")
    if doc.get("original_blueprint")!=["REQUIREMENTS.md","docs/FINAL_DESIGN.md"]:
        raise ValueError("Do not change the final-blueprint denominator")
    if doc.get("item_count")!=33 or len(doc.get("items",[]))!=33:
        raise ValueError("Exactly 33 final-design requirements must be scored")
    ids,weights,states=[],[],[]
    for item in doc["items"]:
        if not isinstance(item,dict):
            raise ValueError("Malformed requirement item")
        ids.append(item.get("id"))
        weight=item.get("weight")
        if type(weight) is not int or weight<=0:
            raise ValueError("Each requirement has a positive integer weight")
        weights.append(weight)
        state=item.get("state")
        if state not in VALID_STATES:
            raise ValueError("Unsupported verification state")
        states.append(state)
        if not isinstance(item.get("requirement"),str) or not item["requirement"].strip():
            raise ValueError("Missing requirement definition")
        if not isinstance(item.get("evidence_scope"),str) or not item["evidence_scope"].strip():
            raise ValueError("Missing acceptance evidence description")
        if not isinstance(item.get("remaining_limitations"),str):
            raise ValueError("Missing remaining limitation record")
        if state=="VERIFIED" and not re.fullmatch(r"[0-9a-f]{40}",str(item.get("source_code_sha"))):
            raise ValueError("Verified requirement needs an exact source SHA")
        if state=="PENDING" and item.get("source_code_sha") is not None:
            raise ValueError("Pending requirement cannot be claimed accepted through source SHA")
    if tuple(ids)!=EXPECTED_IDS:
        raise ValueError("R01 through R33 must all be present once and in order")
    if tuple(weights)!=APPROVED_WEIGHTS or sum(weights)!=100:
        raise ValueError("Frozen owner-selected B weighting changed without explicit approval")
    evidence=doc.get("evidence_baseline")
    if not isinstance(evidence,dict) or evidence.get("code_sha")!=(
        "23a2d1293755294a58a20b98dc34e229a1e54f82"):
        raise ValueError("Missing verified code baseline")
    if evidence.get("actual_customer_acceptance")!="NOT_VERIFIED":
        raise ValueError("Customer acceptance cannot be certified by scorecard")
    scored=sum(w for w,s in zip(weights,states) if s=="VERIFIED")
    unverified=100-scored
    return {
        "contract":"DATA2WEB_FINAL_BLUEPRINT_SCORE_V1",
        "scale":"100_POINT_OWNER_DELEGATED_APPROVED",
        "all_requirements":len(ids),
        "verified_requirements":states.count("VERIFIED"),
        "pending_requirements":states.count("PENDING"),
        "weighted_verified_score":scored,
        "weighted_pending_score":unverified,
        "denominator":100,
        "target":85,
        "remaining_to_target":max(0,85-scored),
        "target_reached":scored>=85,
        "evidence_scope":"HOSTED_SYNTHETIC_AND_BROWSER_AS_ITEMIZED",
        "buyer_windows10_11":"NOT_VERIFIED",
        "sale_status":"RELEASE_HOLD_SALE_NO_GO",
        "work_marker":"[작업중]",
        "source_code_sha":evidence["code_sha"],
        "actions_run":evidence.get("github_actions_run"),
    }


def main():
    parser=argparse.ArgumentParser(description="Inspect the frozen R01-R33 whole-blueprint score")
    parser.add_argument("--path",type=Path,default=DEFAULT)
    args=parser.parse_args()
    print(json.dumps(evaluate_scorecard(args.path),ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
