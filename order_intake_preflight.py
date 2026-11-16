"""Offline anonymous scope matching: NEVER inspects customer files or approves sale."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from path_policy import assert_no_links, read_bounded_source
from secure_output import create_output_file
from zero_cost_gate import POLICY, SCORE, _read, validate_policy

CONTRACT = "DATA2WEB_ANONYMOUS_PREORDER_V2"
PRIVACY_CLASSES = frozenset({
    "NO_PERSONAL_DATA_REVIEWED",
    "PERSONAL_OR_IDENTIFYING_DATA_PRESENT",
    "SENSITIVE_OR_MEDICAL_DATA_PRESENT",
    "PAYMENT_DATA_PRESENT",
    "THIRD_PARTY_CONFIDENTIAL_OR_SHARED_DATA",
    "UNKNOWN_OR_MIXED_SCOPE",
})
SAFE_PRIVACY_CLASS = "NO_PERSONAL_DATA_REVIEWED"
FIELDS = {"contract", "sources", "rights_claimed", "contains_personal_or_sensitive",
          "contains_third_party_confidential", "privacy_classification",
          "plaintext_ack", "mapping_3_distinct_columns", "same_headers"}
SOURCE_FIELDS = {"format", "estimated_bytes", "estimated_rows", "estimated_columns"}
FORMATS = {"CSV", "TSV", "JSON", "XLSX"}
BASIC_FORMATS = {"CSV", "TSV", "JSON"}
MAX_INPUT_BYTES = 16384

def _unique_pairs(pairs):
    doc = {}
    for key, value in pairs:
        if key in doc:
            raise ValueError("Duplicate metadata key")
        doc[key] = value
    return doc

def _validate_request(doc):
    # Shared schema check. Internal callers cannot bypass type and privacy
    # guards by calling assess() directly with an unparsed Python dict.
    if not isinstance(doc, dict) or set(doc) != FIELDS or doc["contract"] != CONTRACT:
        raise ValueError("Only anonymous whitelisted metadata is allowed")
    for field in FIELDS - {"contract", "sources", "privacy_classification"}:
        if type(doc[field]) is not bool:
            raise ValueError("Explicit boolean metadata required")
    if (type(doc["privacy_classification"]) is not str or
            doc["privacy_classification"] not in PRIVACY_CLASSES):
        raise ValueError("Explicit whitelisted privacy classification required")
    sources = doc["sources"]
    if not isinstance(sources, list) or not 1 <= len(sources) <= 40:
        raise ValueError("Expected 1 to 40 anonymous file summaries")
    for source in sources:
        if not isinstance(source, dict) or set(source) != SOURCE_FIELDS:
            raise ValueError("Source names/paths/columns/content must not be collected")
        if type(source["format"]) is not str or source["format"] not in FORMATS:
            raise ValueError("Unsupported format")
        for field in SOURCE_FIELDS - {"format"}:
            value = source[field]
            if type(value) is not int or not 0 <= value <= 1_000_000_000:
                raise ValueError("Count must be bounded nonnegative integer")
    return doc

def parse_request(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_INPUT_BYTES:
        raise ValueError("Oversized metadata")
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs,
                     parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite value")))
    return _validate_request(doc)

def result(reason, sku=None):
    return {
        "contract": "DATA2WEB_ANONYMOUS_PREORDER_RESULT_V1",
        "status": "SCOPE_CANDIDATE_ONLY" if sku else "HOLD_PREORDER",
        "reason": reason,
        "sku": sku["name"] if sku else None,
        "suggested_price_krw": sku["price_krw"] if sku else None,
        "real_customer_file_read": False,
        "customer_rights_independently_verified": False,
        "order_accepted": False,
        "sale_approved": False,
        "release": "RELEASE_HOLD_SALE_NO_GO",
        "new_cash_spend_krw": 0,
    }

def assess(doc):
    doc = _validate_request(doc)
    policy = _read(POLICY)
    validate_policy(policy, _read(SCORE))
    sources = doc["sources"]
    if doc["contains_personal_or_sensitive"] or doc["contains_third_party_confidential"]:
        return result("PERSONAL_OR_CONFIDENTIAL_HOLD")
    if doc["privacy_classification"] != SAFE_PRIVACY_CLASS:
        return result("PRIVACY_SCOPE_HOLD")
    if not doc["rights_claimed"] or not doc["plaintext_ack"]:
        return result("RIGHTS_OR_PLAINTEXT_ACK_MISSING")
    if not doc["mapping_3_distinct_columns"]:
        return result("THREE_COLUMN_MAPPING_NOT_CONFIRMED")
    if len(sources) > 1 and not doc["same_headers"]:
        return result("SAME_HEADERS_NOT_CONFIRMED")
    if len(sources) > 10:
        return result("TOO_MANY_SOURCES")
    if any(not 1 <= s["estimated_bytes"] <= 8_000_000 or s["estimated_rows"] < 1 or
           not 3 <= s["estimated_columns"] <= 20 for s in sources):
        return result("SOURCE_EXCEEDS_TECHNICAL_LIMIT")
    count = len(sources)
    rows = sum(s["estimated_rows"] for s in sources)
    kinds = [s["format"] for s in sources]
    if count == 1 and kinds[0] in BASIC_FORMATS and rows <= 1000:
        return result("BASIC_CANDIDATE_REAL_SOURCE_REVIEW_PENDING", policy["skus"][0])
    if rows <= 5000 and ((count == 1 and kinds[0] == "XLSX") or
                         (1 <= count <= 3 and all(k in BASIC_FORMATS for k in kinds))):
        return result("PRO_CANDIDATE_REAL_SOURCE_REVIEW_PENDING", policy["skus"][1])
    if 2 <= count <= 10 and rows <= 10000:
        return result("BUSINESS_CANDIDATE_REAL_SOURCE_REVIEW_PENDING", policy["skus"][2])
    return result("NO_APPROVED_PACKAGE_MATCH")

def synthetic_example():
    return {
        "contract": CONTRACT, "sources": [
            {"format": "CSV", "estimated_bytes": 400,
             "estimated_rows": 8, "estimated_columns": 4}
        ], "rights_claimed": True, "contains_personal_or_sensitive": False,
        "contains_third_party_confidential": False,
        "privacy_classification": SAFE_PRIVACY_CLASS, "plaintext_ack": True,
        "mapping_3_distinct_columns": True, "same_headers": True,
    }

# This output format is intentionally closed. An embedded email, path,
# free-text reason or forged approval is never permitted in saved reports.
CANDIDATE_REASONS = {
    "BASIC": ("BASIC_CANDIDATE_REAL_SOURCE_REVIEW_PENDING", 49000),
    "PRO": ("PRO_CANDIDATE_REAL_SOURCE_REVIEW_PENDING", 129000),
    "BUSINESS": ("BUSINESS_CANDIDATE_REAL_SOURCE_REVIEW_PENDING", 249000),
}
HOLD_REASONS = frozenset({
    "PERSONAL_OR_CONFIDENTIAL_HOLD", "PRIVACY_SCOPE_HOLD",
    "RIGHTS_OR_PLAINTEXT_ACK_MISSING",
    "THREE_COLUMN_MAPPING_NOT_CONFIRMED", "SAME_HEADERS_NOT_CONFIRMED",
    "TOO_MANY_SOURCES", "SOURCE_EXCEEDS_TECHNICAL_LIMIT",
    "NO_APPROVED_PACKAGE_MATCH",
})
REPORT_FIELDS = frozenset((
    "contract", "status", "reason", "sku", "suggested_price_krw",
    "real_customer_file_read", "customer_rights_independently_verified",
    "order_accepted", "sale_approved", "release", "new_cash_spend_krw",
))


def validate_report(record):
    if not isinstance(record, dict) or set(record) != REPORT_FIELDS:
        raise ValueError("Only anonymous exact-schema preorder reports can be saved")
    if record["contract"] != "DATA2WEB_ANONYMOUS_PREORDER_RESULT_V1":
        raise ValueError("Unknown report contract")
    for field in ("real_customer_file_read",
                  "customer_rights_independently_verified",
                  "order_accepted", "sale_approved"):
        if record[field] is not False:
            raise ValueError("Customer source or approval cannot be certified")
    if record["release"] != "RELEASE_HOLD_SALE_NO_GO" or (
            type(record["new_cash_spend_krw"]) is not int or
            record["new_cash_spend_krw"] != 0):
        raise ValueError("Report cannot spend or authorize sale")
    if record["status"] == "SCOPE_CANDIDATE_ONLY":
        expected = CANDIDATE_REASONS.get(record["sku"])
        if expected is None or (
                record["reason"], record["suggested_price_krw"]) != expected or (
                type(record["suggested_price_krw"]) is not int):
            raise ValueError("Unapproved candidate reason or price")
    elif record["status"] == "HOLD_PREORDER":
        if (record["reason"] not in HOLD_REASONS or
                record["sku"] is not None or
                record["suggested_price_krw"] is not None):
            raise ValueError("Unapproved HOLD reason or nonempty candidate")
    else:
        raise ValueError("Only HOLD and unapproved scope candidate statuses exist")
    return record


def write_new_report(path, record):
    validate_report(record)
    target = Path(path)
    assert_no_links(target, allow_missing_leaf=True)
    if target.is_symlink() or target.exists() or not target.parent.is_dir():
        raise FileExistsError("Report path must be new")
    with create_output_file(target) as dest:
        dest.write((json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n").encode("utf-8"))

def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline anonymous pre-order scope review")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--synthetic-self-check", action="store_true")
    group.add_argument("--metadata-file", type=Path)
    parser.add_argument("--new-report-file", type=Path)
    args = parser.parse_args(argv)
    try:
        doc = synthetic_example() if args.synthetic_self_check else parse_request(
            read_bounded_source(args.metadata_file, max_bytes=MAX_INPUT_BYTES))
        record = assess(doc)
        if args.new_report_file is not None:
            write_new_report(args.new_report_file, record)
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))
        return 0 if record["status"] == "SCOPE_CANDIDATE_ONLY" else 2
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, json.JSONDecodeError):
        print(json.dumps({"status": "HOLD_PREORDER", "reason": "INVALID_METADATA",
                          "sale_approved": False}, sort_keys=True))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
