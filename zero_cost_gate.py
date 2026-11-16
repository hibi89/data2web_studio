"""Fail-closed zero-upfront-cost internal policy gate. No user file or network access."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POLICY = ROOT / "data" / "zero_cost_owner_policy_v1.json"
SCORE = ROOT / "data" / "final_blueprint_scorecard_v1.json"

def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate key in zero-cost policy")
        result[key] = value
    return result

def _read(path):
    raw = Path(path).read_bytes()
    if len(raw) > 20_000:
        raise ValueError("Oversized zero-cost policy document")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite JSON")))

def validate_policy(doc, score=None):
    if not isinstance(doc, dict) or doc.get("contract") != "DATA2WEB_ZERO_UPFRONT_COST_POLICY_V1":
        raise ValueError("Wrong policy contract")
    expected = {
        "approved_upfront_budget_krw": 0,
        "any_paid_service_or_purchase_allowed": False,
        "use_paid_code_signing": False,
        "use_paid_security_audit": False,
        "use_paid_ai_or_cloud_api": False,
        "use_paid_runner": False,
        "deployment_track": "A_OFFLINE_HTML_ZIP_RECEIPT_FIRST",
        "exe_track": "B_UNSIGNED_OWNER_PREVIEW_ONLY_NOT_CUSTOMER_SALE",
        "security_scan": "GITHUB_PUBLIC_REPO_STANDARD_RUNNER_CODEQL_NO_ADDED_CASH",
        "security_scan_is_independent_human_audit": False,
        "external_independent_audit_completed": False,
        "source_customer_upload_to_github_or_ai": False,
        "operator_local_customer_data_max_retention_days": 7,
        "source_deletion_mode": "MANUAL_AUTHORIZED_ONLY_NO_AUTODELETE_CUSTOMER_ORIGINAL",
        "output_plaintext_warning_required": True,
        "customer_internal_use_nonexclusive_only_after_rights_cleared": True,
        "external_disclosure_scope": "ONLY_EXISTING_PUBLIC_REPO_SOURCE_AND_SYNTHETIC_FIXTURES_NO_CUSTOMER_DATA",
        "sku_policy_status": "OWNER_APPROVED_INTERNAL_DEFAULTS_NOT_PUBLISHED",
        "refund_policy": "FOLLOW_APPLICABLE_LAW_AND_MARKETPLACE_POLICY_NO_BLANKET_NO_REFUNDS",
        "actual_marketplace_listing_approved": False,
        "shipping_ip_rights_evidence_complete": False,
        "per_customer_data_rights_verified": False,
        "release_status": "RELEASE_HOLD_SALE_NO_GO",
        "final_blueprint_score_unchanged": 72,
        "final_blueprint_denominator": 100,
        "target_score": 85,
        "work_marker": "[작업중]",
        "owner_authorization": "OWNER_APPROVED_ALL_ZERO_UPFRONT_COST_OPERATIONAL_DEFAULTS",
        "owner_approval_limit": "INTERNAL_OPERATIONAL_POLICY_ONLY_NOT_CUSTOMER_OR_THIRD_PARTY_RIGHTS_PROOF",
        "customer_source_policy": "REJECT_PERSONAL_SENSITIVE_OR_UNCLEAR_RIGHTS_REQUIRE_PER_ORDER_RIGHTS_CONSENT",
    }
    for key, required in expected.items():
        if type(doc.get(key)) is not type(required) or doc[key] != required:
            raise ValueError("Zero-cost / rights / release policy was weakened: " + key)
    skus = doc.get("skus")
    intended = [
        ("BASIC", 49000, 1, 1000, 1, 7),
        ("PRO", 129000, 3, 5000, 2, 14),
        ("BUSINESS", 249000, 10, 10000, 3, 30),
    ]
    if not isinstance(skus, list) or len(skus) != 3:
        raise ValueError("Three approved internal SKUs required")
    for item, (name, price, sources, rows, revisions, days) in zip(skus, intended):
        if not isinstance(item, dict) or item != {
            "name": name, "price_krw": price, "source_limit": sources,
            "row_limit": rows, "revision_count": revisions, "defect_support_days": days
        }:
            raise ValueError("Internal SKU terms changed without versioned approval")
    if score is not None:
        if score.get("denominator") != 100 or score.get("target_score") != 85:
            raise ValueError("Score denominator/target changed")
        items = score.get("items")
        if not isinstance(items, list) or len(items) != 33:
            raise ValueError("Final design has 33 requirements")
        total = sum(item["weight"] for item in items if item["state"] == "VERIFIED")
        pending = {item["id"] for item in items if item["state"] == "PENDING"}
        if total != 72 or not {"R07","R21","R25","R26","R27","R29"}.issubset(pending):
            raise ValueError("Zero-cost authorization cannot manufacture completion evidence")
        if score.get("release_status") != "RELEASE_HOLD_SALE_NO_GO":
            raise ValueError("Zero-cost policy cannot auto-release product")
    return True

def inspect_policy(policy_path=POLICY, score_path=SCORE):
    policy = _read(policy_path)
    score = _read(score_path)
    validate_policy(policy, score)
    return {
        "contract": "DATA2WEB_ZERO_COST_GATE_V1",
        "policy_valid": True,
        "new_spend_krw": 0,
        "default_operational_terms_owner_approved": True,
        "independent_human_audit": False,
        "customer_rights_or_ownership_proven": False,
        "weighted_verified_score": 72,
        "target_score": 85,
        "sale_status": "RELEASE_HOLD_SALE_NO_GO",
    }

if __name__ == "__main__":
    print(json.dumps(inspect_policy(), sort_keys=True, ensure_ascii=True))
