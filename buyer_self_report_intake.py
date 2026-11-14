"""Offline intake for a manually completed synthetic buyer device report.

This checks shape, consistency and provenance only. A self-reported PASS
cannot prove a real independent device, rights, identity or security audit.
No network/PII/storage; returns CANDIDATE for separate human verification.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
from pathlib import Path
from zipfile import ZipFile

from kmong_independent_buyer_request import (
    _blank_form, _read_json, verify_request, SHA40, MAX_ZIP,
)
from path_policy import read_bounded_source

OS_NAMES = frozenset({"Windows 10", "Windows 11", "macOS", "Linux"})
BROWSER = re.compile(r"(?:Chrome|Edge|Chromium) [0-9]{1,3}(?:\.[0-9]{1,5}){0,3}\Z")
STATES = frozenset({"PASS", "FAIL", "NOT_RUN"})


def assess_self_report(request_zip, report_path):
    # Existing independent structural request verifier rejects changed
    # delivery, source, signed-off flags or altered blank reviewer form.
    package = verify_request(request_zip)
    raw = read_bounded_source(request_zip, max_bytes=MAX_ZIP)
    package_hash = hashlib.sha256(raw).hexdigest()
    if package_hash != package["sha256"]:
        raise ValueError("Request ZIP changed between verification and intake")
    with ZipFile(io.BytesIO(raw), "r") as archive:
        origin = _read_json(archive.read("REQUEST_MANIFEST.json"))
        source_sha = origin["source_commit_sha"]

    # Read one bounded local snapshot; never send it anywhere.
    doc = _read_json(read_bounded_source(report_path, max_bytes=8192))
    blank = _blank_form(source_sha)
    if set(doc) != set(blank):
        raise ValueError("Unknown/identifying fields are forbidden in reviewer result")
    if (doc["contract"] != blank["contract"]
            or doc["request_source_sha"] != source_sha
            or doc["synthetic_only"] is not True
            or doc["requires_further_human_review"] is not True):
        raise ValueError("Wrong origin or invalid test-request contract")
    for f in ("buyer_acceptance_verified",
              "independent_human_security_audit_completed",
              "source_data_rights_verified", "sale_approved",
              "claim_to_100_points"):
        if doc[f] is not False:
            raise ValueError("A self-report cannot authorize a sale, audit, or final score")
    for f in ("actual_real_device_run", "reviewer_independent_of_development"):
        if type(doc[f]) is not bool:
            raise ValueError("Actual-run and independence must be explicit booleans")
    if not isinstance(doc["steps"], dict) or set(doc["steps"]) != set(blank["steps"]):
        raise ValueError("All named buyer test steps must be present")
    if any(type(value) is not str or value not in STATES for value in doc["steps"].values()):
        raise ValueError("Test step states restricted to PASS/FAIL/NOT_RUN")
    if type(doc["observed_result"]) is not str or doc["observed_result"] not in STATES:
        raise ValueError("Invalid observed result")
    values = tuple(doc["steps"].values())
    expected_summary = (
        "FAIL" if "FAIL" in values
        else "PASS" if all(x == "PASS" for x in values)
        else "NOT_RUN"
    )
    if doc["observed_result"] != expected_summary:
        raise ValueError("Overall result conflicts with step evidence")
    os_name = doc["reviewer_device_os"]
    browser_name = doc["browser_and_version"]
    if (type(os_name) is not str or
            (os_name != "NOT_RECORDED" and os_name not in OS_NAMES)):
        raise ValueError("Reviewer OS must use non-identifying supported labels")
    if (type(browser_name) is not str or
            (browser_name != "NOT_RECORDED" and not BROWSER.fullmatch(browser_name))):
        raise ValueError("Browser/version must use an approved non-identifying syntax")
    if not doc["actual_real_device_run"] and any(s != "NOT_RUN" for s in values):
        raise ValueError("Test steps cannot be passed without a claimed real-device run")
    if not doc["actual_real_device_run"] and (
            os_name != "NOT_RECORDED" or browser_name != "NOT_RECORDED"):
        raise ValueError("No OS/browser details without a declared run")
    if doc["actual_real_device_run"] and (
            os_name == "NOT_RECORDED" or browser_name == "NOT_RECORDED"):
        raise ValueError("A claimed real-device run requires OS and browser evidence")
    if expected_summary == "FAIL":
        status = "HOLD_OBSERVED_FAILURE"
    elif expected_summary == "NOT_RUN" or not doc["actual_real_device_run"]:
        status = "HOLD_INCOMPLETE_DEVICE_TEST"
    elif not doc["reviewer_independent_of_development"]:
        status = "HOLD_NOT_INDEPENDENT"
    else:
        status = "CANDIDATE_FOR_EXTERNAL_HUMAN_REVIEW_ONLY"
    return {
        "contract": "DATA2WEB_BUYER_SELF_REPORT_INTAKE_V1",
        "status": status,
        "report_is_authenticated": False,
        "external_human_verified": False,
        "technical_report_shape_valid": True,
        "claim_of_real_device_run": doc["actual_real_device_run"],
        "claim_of_independence": doc["reviewer_independent_of_development"],
        "observed_result_claim": expected_summary,
        "source_commit_sha": source_sha,
        "request_zip_sha256": package_hash,
        "report_sha256": hashlib.sha256(read_bounded_source(
            report_path, max_bytes=8192)).hexdigest(),
        "buyer_acceptance_verified": False,
        "independent_human_security_audit_completed": False,
        "sale_approved": False,
        "score_added": 0,
    }


def main():
    p = argparse.ArgumentParser(description="Offline buyer TEST REPORT intake, not acceptance")
    p.add_argument("--request-zip", type=Path, required=True)
    p.add_argument("--result-json", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(assess_self_report(args.request_zip, args.result_json),
                     ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
