"""Local operator-copy retention readiness: redacted, read-only, never proof.

Only a separately authored, *anonymous* metadata record is inspected.
This tool never reads a customer source, deletes a file, certifies a customer
agreement, attests that disposal occurred, or approves a commercial release.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path

from path_policy import assert_no_links, read_bounded_source
from zero_cost_gate import POLICY, SCORE, _read, validate_policy

CONTRACT = "DATA2WEB_OPERATOR_COPY_RETENTION_REVIEW_V1"
KEYS = {
    "contract", "operator_copy_present", "received_at_utc", "source_scope",
    "purpose_completed", "legal_retention_exception_claimed",
    "per_order_rights_claimed", "per_order_plaintext_ack_claimed",
}
SCOPES = {
    "NONPERSONAL_NONCONFIDENTIAL", "PERSONAL_OR_SENSITIVE",
    "THIRD_PARTY_CONFIDENTIAL", "UNDETERMINED",
}
MAX_METADATA = 4096
MAX_REPORT = 4096


def _unique_pairs(pairs):
    record = {}
    for name, value in pairs:
        if name in record:
            raise ValueError("Duplicated metadata field")
        record[name] = value
    return record


def _parse_utc(value):
    if not isinstance(value, str) or len(value) != 20 or (
            value[4] != "-" or value[7] != "-" or
            value[10] != "T" or value[13] != ":" or value[16] != ":" or
            value[-1] != "Z"):
        raise ValueError("An exact UTC timestamp is required")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise ValueError("Invalid UTC timestamp") from error
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("Noncanonical UTC timestamp")
    return parsed.replace(tzinfo=timezone.utc)


def _utc(value):
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_metadata(doc):
    if not isinstance(doc, dict) or set(doc) != KEYS or doc["contract"] != CONTRACT:
        raise ValueError("No identifiers, paths, content or free text may be supplied")
    for name in (
        "operator_copy_present", "purpose_completed",
        "legal_retention_exception_claimed", "per_order_rights_claimed",
        "per_order_plaintext_ack_claimed",
    ):
        if type(doc[name]) is not bool:
            raise ValueError("Every review decision requires an explicit boolean")
    if type(doc["source_scope"]) is not str or doc["source_scope"] not in SCOPES:
        raise ValueError("Sensitive or unknown scope must be explicitly classified")
    if doc["operator_copy_present"]:
        if doc["received_at_utc"] is None:
            raise ValueError("Received date required for an operator-held copy")
        _parse_utc(doc["received_at_utc"])
    elif doc["received_at_utc"] is not None:
        # A self-reported absence does not prove past deletion. Do not turn
        # a previous receipt time into a fabricated disposal event.
        raise ValueError("Cannot claim disposal from a copy-absent record")
    return doc


def parse_metadata(raw):
    if type(raw) is not bytes or len(raw) > MAX_METADATA:
        raise ValueError("Metadata must be bounded bytes")
    doc = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_unique_pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(
            ValueError("Nonfinite metadata forbidden")
        ),
    )
    return validate_metadata(doc)


def _approved_limit():
    policy = _read(POLICY)
    validate_policy(policy, _read(SCORE))
    limit = policy["operator_local_customer_data_max_retention_days"]
    if type(limit) is not int or limit != 7:
        raise ValueError("Unexpected retention policy; owner reconfirmation required")
    if policy["source_deletion_mode"] != (
            "MANUAL_AUTHORIZED_ONLY_NO_AUTODELETE_CUSTOMER_ORIGINAL"):
        raise ValueError("Automatic deletion would violate local policy")
    if policy["release_status"] != "RELEASE_HOLD_SALE_NO_GO":
        raise ValueError("Unapproved commercial status")
    return limit


def review_copy(doc, *, as_of=None):
    """Classify time and copy-handling risk without touching source files.

    as_of is for synthetic deterministic tests. The CLI always uses live UTC.
    All observed rights/disposal fields are *claims*, never independent proof.
    """
    validate_metadata(doc)
    limit = _approved_limit()
    now = datetime.now(timezone.utc) if as_of is None else as_of
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise ValueError("A timezone-aware review instant is required")
    now = now.astimezone(timezone.utc)
    if doc["operator_copy_present"]:
        received = _parse_utc(doc["received_at_utc"])
        if received > now:
            raise ValueError("Future receipt cannot establish retention compliance")
        due = received + timedelta(days=limit)
    else:
        due = None

    if not doc["operator_copy_present"]:
        reason = "NO_OPERATOR_COPY_REPORTED_NOT_VERIFIED"
    elif doc["source_scope"] != "NONPERSONAL_NONCONFIDENTIAL":
        reason = "PERSONAL_CONFIDENTIAL_OR_UNKNOWN_SCOPE_HOLD"
    elif not doc["per_order_rights_claimed"] or not doc["per_order_plaintext_ack_claimed"]:
        reason = "PER_ORDER_RIGHTS_OR_PLAINTEXT_CONSENT_PENDING"
    elif doc["legal_retention_exception_claimed"]:
        reason = "LEGAL_EXCEPTION_REQUIRES_MANUAL_EVIDENCE_REVIEW"
    elif doc["purpose_completed"] or now >= due:
        reason = "MANUAL_DISPOSAL_ACTION_DUE_NO_AUTO_DELETE"
    else:
        reason = "WITHIN_7_DAYS_MANUAL_REVIEW_STILL_REQUIRED"

    # There is intentionally no 'disposal complete' output or approval.
    return {
        "contract": "DATA2WEB_OPERATOR_COPY_RETENTION_RESULT_V1",
        "status": "REVIEW_ONLY_RELEASE_HOLD",
        "reason_code": reason,
        "reviewed_at_utc": _utc(now),
        "operator_copy_present_claimed": doc["operator_copy_present"],
        "retention_due_utc": _utc(due) if due is not None else None,
        "retention_policy_max_days": limit,
        "manual_disposal_action_due": bool(
            doc["operator_copy_present"] and
            (doc["purpose_completed"] or now >= due) and
            not doc["legal_retention_exception_claimed"]
        ),
        "customer_source_bytes_read": False,
        "customer_rights_independently_verified": False,
        "actual_customer_consent_verified": False,
        "independent_disposal_verified": False,
        "automatic_deletion_performed": False,
        "sale_approved": False,
        "release": "RELEASE_HOLD_SALE_NO_GO",
        "score_addition": 0,
    }


def validate_result(record):
    if not isinstance(record, dict) or set(record) != {
        "contract", "status", "reason_code", "reviewed_at_utc",
        "operator_copy_present_claimed", "retention_due_utc",
        "retention_policy_max_days", "manual_disposal_action_due",
        "customer_source_bytes_read", "customer_rights_independently_verified",
        "actual_customer_consent_verified", "independent_disposal_verified",
        "automatic_deletion_performed", "sale_approved", "release",
        "score_addition",
    }:
        raise ValueError("Unexpected report fields")
    if (record["contract"] != "DATA2WEB_OPERATOR_COPY_RETENTION_RESULT_V1"
            or record["status"] != "REVIEW_ONLY_RELEASE_HOLD"
            or record["release"] != "RELEASE_HOLD_SALE_NO_GO"):
        raise ValueError("Report cannot authorize customer intake or commercial release")
    if record["reason_code"] not in {
        "NO_OPERATOR_COPY_REPORTED_NOT_VERIFIED",
        "PERSONAL_CONFIDENTIAL_OR_UNKNOWN_SCOPE_HOLD",
        "PER_ORDER_RIGHTS_OR_PLAINTEXT_CONSENT_PENDING",
        "LEGAL_EXCEPTION_REQUIRES_MANUAL_EVIDENCE_REVIEW",
        "MANUAL_DISPOSAL_ACTION_DUE_NO_AUTO_DELETE",
        "WITHIN_7_DAYS_MANUAL_REVIEW_STILL_REQUIRED",
    }:
        raise ValueError("Report reason cannot contain free text")
    for name in (
        "customer_source_bytes_read", "customer_rights_independently_verified",
        "actual_customer_consent_verified", "independent_disposal_verified",
        "automatic_deletion_performed", "sale_approved",
    ):
        if record[name] is not False:
            raise ValueError("Unverified activity cannot be certified")
    if (type(record["retention_policy_max_days"]) is not int or
            record["retention_policy_max_days"] != 7 or
            type(record["score_addition"]) is not int or record["score_addition"] != 0 or
            type(record["manual_disposal_action_due"]) is not bool or
            type(record["operator_copy_present_claimed"]) is not bool):
        raise ValueError("Invalid status or policy values")
    reviewed = _parse_utc(record["reviewed_at_utc"])
    due_text = record["retention_due_utc"]
    if record["operator_copy_present_claimed"]:
        if due_text is None:
            raise ValueError("Copy-present report must include retention deadline")
        due = _parse_utc(due_text)
        if due > reviewed + timedelta(days=7):
            raise ValueError("Retention deadline cannot exceed seven days from review")
        if record["reason_code"] == "NO_OPERATOR_COPY_REPORTED_NOT_VERIFIED":
            raise ValueError("Copy-present report cannot claim no copy")
        if (record["reason_code"] == "WITHIN_7_DAYS_MANUAL_REVIEW_STILL_REQUIRED"
                and due <= reviewed):
            raise ValueError("Expired copy cannot be reported within retention window")
    else:
        if due_text is not None or record["manual_disposal_action_due"]:
            raise ValueError("Copy-absent report cannot claim deadline or action due")
        if record["reason_code"] != "NO_OPERATOR_COPY_REPORTED_NOT_VERIFIED":
            raise ValueError("Copy-absent report must retain unverified status")
    if record["manual_disposal_action_due"] and record["reason_code"] != (
            "MANUAL_DISPOSAL_ACTION_DUE_NO_AUTO_DELETE"):
        raise ValueError("Manual disposal flag and reason disagree")
    if record["reason_code"] == "MANUAL_DISPOSAL_ACTION_DUE_NO_AUTO_DELETE" and not (
            record["manual_disposal_action_due"]):
        raise ValueError("Disposal-due report cannot suppress manual action")
    return record


def write_new_report(path, record):
    validate_result(record)
    target = Path(path)
    assert_no_links(target, allow_missing_leaf=True)
    if target.exists() or target.is_symlink() or not target.parent.is_dir():
        raise FileExistsError("Only a new local report path is permitted")
    data = (json.dumps(
        record, sort_keys=True, ensure_ascii=True, separators=(",", ":"
        )) + "\n").encode("utf-8")
    if len(data) > MAX_REPORT:
        raise ValueError("Retention report is too large")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(
        os, "O_BINARY", 0
    ) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(target, flags, 0o600)
    with os.fdopen(fd, "wb") as writer:
        writer.write(data)


def synthetic_example():
    return {
        "contract": CONTRACT,
        "operator_copy_present": True,
        "received_at_utc": _utc(datetime.now(timezone.utc).replace(
            microsecond=0
        ) - timedelta(days=2)),
        "source_scope": "NONPERSONAL_NONCONFIDENTIAL",
        "purpose_completed": False,
        "legal_retention_exception_claimed": False,
        "per_order_rights_claimed": False,
        "per_order_plaintext_ack_claimed": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read-only, metadata-only local copy retention review"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--synthetic-self-check", action="store_true")
    source.add_argument("--metadata-file", type=Path)
    parser.add_argument("--new-report-file", type=Path)
    args = parser.parse_args(argv)
    try:
        doc = synthetic_example() if args.synthetic_self_check else parse_metadata(
            read_bounded_source(args.metadata_file, max_bytes=MAX_METADATA)
        )
        result = review_copy(doc)
        if args.new_report_file is not None:
            write_new_report(args.new_report_file, result)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 0 if result["reason_code"] == (
            "NO_OPERATOR_COPY_REPORTED_NOT_VERIFIED"
        ) else 2
    except (OSError, ValueError, TypeError, KeyError, UnicodeError):
        print(json.dumps({
            "status": "HOLD",
            "reason_code": "INVALID_LOCAL_RETENTION_METADATA",
            "sale_approved": False,
        }, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
