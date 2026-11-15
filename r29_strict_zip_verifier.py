"""Strict read-only R29 ZIP check while the shipping verifier is being remediated.

Applies CODEX-owned verify_zip package integrity checks AND the independent
HIGH-owned reviewed offline HTML surface guard to the same bounded ZIP bytes.
This is a reviewer/owner opt-in command, not a replacement shipping verifier.
No writes, extraction, customer upload, network access, audit certification,
proof of publisher authenticity, or authorization to sell.
"""
from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

from path_policy import assert_no_links, read_bounded_source
from r29_html_surface_policy import assert_passive_offline_html_markup
from verify_delivery import MAX_ARCHIVE, verify_zip


def verify_zip_r29_strict(path):
    """Reject rehashed active HTML while retaining existing ZIP policy."""
    path = assert_no_links(Path(path))
    # CODEX verifier checks the canonical envelope, package members, CRC,
    # allowed sizes, receipt/embedded JSON consistency and static CSP policy.
    validated = verify_zip(path)
    snapshot = read_bounded_source(path, max_bytes=MAX_ARCHIVE)
    expected = validated.get("zip_sha256")
    if not isinstance(expected, str) or hashlib.sha256(snapshot).hexdigest() != expected:
        raise ValueError("ZIP changed between independent security checks")
    with ZipFile(BytesIO(snapshot), "r") as archive:
        html = archive.read("index.html")
    policy = assert_passive_offline_html_markup(html)
    # Checking the exact same snapshot across the two readers narrows races,
    # but does not guarantee atomicity against a privileged concurrent writer.
    if read_bounded_source(path, max_bytes=MAX_ARCHIVE) != snapshot:
        raise ValueError("ZIP changed during strict security verification")
    return {
        "verified": validated["verified"],
        "strict_passive_html_verified": policy["passive_template_surface_verified"],
        "zip_sha256": expected,
        "source_authenticity_verified": False,
        "independent_security_audit_completed": False,
        "commercial_release_approved": False,
        "production_status": "RELEASE_HOLD_SALE_NO_GO",
        "score_addition": 0,
    }


def main():
    parser = argparse.ArgumentParser(
        description="R29 strict, read-only ZIP verification; release HOLD"
    )
    parser.add_argument("zip_path")
    args = parser.parse_args()
    try:
        result = verify_zip_r29_strict(args.zip_path)
    except (ValueError, OSError, KeyError):
        # Never print unchecked source paths, source data, or exceptions.
        print(json.dumps({
            "verified": False,
            "status": "R29_STRICT_SECURITY_HOLD",
            "commercial_release_approved": False,
            "score_addition": 0,
        }, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
