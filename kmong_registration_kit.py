"""Create-only, reproducible synthetic-only weekend listing archive (stdlib).

This is a seller's draft asset package, not a commercial license,
customer-data rights proof, independent audit, or sale authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import struct
from zipfile import ZipFile, ZipInfo, ZIP_STORED

from kmong_weekend_demo import LEAF, REPORT, SOURCE, sample_csv_bytes
from path_policy import assert_no_links, read_bounded_source
from secure_output import create_output_file, open_output_directory
from verify_customer_folder import verify_customer_folder

ROOT = Path(__file__).resolve().parent
CONTRACT = "DATA2WEB_KMONG_REGISTRATION_KIT_V1"
DOCS = (
    "docs/KMONG_WEEKEND_REGISTRATION_READY_20261114.md",
    "docs/KMONG_WEEKEND_LISTING_20261114.md",
    "docs/OWNER_APPROVAL_PACKET_A_20261114.md",
    "docs/OWNER_ACTIONS_1300_KST_20261114.md",
    "docs/ZERO_COST_OWNER_AUTHORIZATION_20261114.md",
    "docs/KMONG_LOCAL_PREORDER_TRIAGE_20261114.md",
    "docs/R22_ZIP_STRICT_CSP_INTEGRITY_20261114.md",
)
SHOTS = ("01-dashboard.png", "02-search-filter.png", "03-kmong-main-652x488.png")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
MAX_KIT = 32_000_000


def _canonical_png(blob, *, filename=None):
    if len(blob) < 33 or not blob.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Missing or invalid synthetic PNG")
    if blob[12:16] != b"IHDR" or blob[8:12] != b"\x00\x00\x00\r":
        raise ValueError("Missing PNG IHDR")
    width, height = struct.unpack(">II", blob[16:24])
    if filename == "03-kmong-main-652x488.png":
        if (width, height) != (652, 488):
            raise ValueError("Main image must be exactly 652x488 pixels")
    elif not 800 <= width <= 4096 or not 500 <= height <= 4096:
        raise ValueError("Screenshot has unexpected geometry")


def _json_no_duplicate(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate evidence key")
        result[key] = value
    return result


def _loads(blob):
    return json.loads(blob.decode("utf-8"), object_pairs_hook=_json_no_duplicate,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite evidence")))


def _input_members(preview, source_root):
    assert_no_links(preview)
    assert_no_links(source_root)
    source = read_bounded_source(preview / SOURCE, max_bytes=8_000_000)
    if source != sample_csv_bytes():
        raise ValueError("Registration package cannot use non-synthetic source")
    report = _loads(read_bounded_source(preview / REPORT, max_bytes=20_000))
    if (report.get("contract") != "DATA2WEB_KMONG_SYNTHETIC_DEMO_V1"
            or report.get("sample_only") is not True
            or report.get("customer_data_used") is not False
            or report.get("sale_approved") is not False
            or report.get("rows") != 8):
        raise ValueError("Not an approved synthetic-only preview")
    verified = verify_customer_folder(preview / LEAF)
    if (verified["verified"] is not True
            or verified["sale_approved"] is not False
            or verified["zip_sha256"] != report.get("zip_sha256")):
        raise ValueError("Synthetic delivery integrity mismatch")
    capture = _loads(read_bounded_source(preview / "screenshots" / "CAPTURE_EVIDENCE.json",
                                         max_bytes=20_000))
    if (capture.get("contract") != "DATA2WEB_SYNTHETIC_BROWSER_SCREENSHOTS_V1"
            or capture.get("customer_data_used") is not False
            or capture.get("real_browser_chromium") is not True
            or capture.get("sale_approved") is not False
            or capture.get("offline_http_requests") != 0
            or capture.get("js_errors") != 0):
        raise ValueError("Missing real synthetic browser screenshot evidence")
    records = capture.get("screenshots")
    if (not isinstance(records, list) or len(records) != len(SHOTS)
            or [x.get("filename") for x in records if isinstance(x, dict)] != list(SHOTS)):
        raise ValueError("Unexpected synthetic screenshot inventory")
    members = {}
    for path in DOCS:
        members[path] = read_bounded_source(source_root / path, max_bytes=256_000)
    for filename, item in zip(SHOTS, records):
        data = read_bounded_source(preview / "screenshots" / filename, max_bytes=8_000_000)
        _canonical_png(data, filename=filename)
        if (item.get("sha256") != hashlib.sha256(data).hexdigest()
                or type(item.get("bytes")) is not int or item["bytes"] != len(data)):
            raise ValueError("Screenshot SHA/length differs from browser evidence")
        members["screenshots/" + filename] = data
    members["synthetic-demo-delivery.zip"] = read_bounded_source(
        preview / LEAF / "delivery.zip", max_bytes=24_000_000
    )
    if len(members) != 11:
        raise AssertionError("Unexpected registration kit inventory")
    return members


def verify_kit(path):
    raw = read_bounded_source(path, max_bytes=MAX_KIT)
    with ZipFile(io.BytesIO(raw), "r") as archive:
        members = archive.infolist()
        names = [x.filename for x in members]
        if (len(names) != 12 or len(names) != len(set(names))
                or archive.testzip() is not None
                or any(x.compress_type != ZIP_STORED for x in members)
                or any(x.is_dir() or x.flag_bits or x.extra or x.comment for x in members)):
            raise ValueError("Unexpected or damaged registration archive")
        if set(names) != set(DOCS) | {"KIT_EVIDENCE.json", "synthetic-demo-delivery.zip"} | {
            "screenshots/" + shot for shot in SHOTS
        }:
            raise ValueError("Unapproved registration archive member")
        manifest = _loads(archive.read("KIT_EVIDENCE.json"))
        if (manifest.get("contract") != CONTRACT or
                manifest.get("sale_approved") is not False or
                manifest.get("customer_data_used") is not False or
                manifest.get("independent_security_audit_completed") is not False or
                manifest.get("verified_points") != 72 or
                manifest.get("full_goal_points") != 100):
            raise ValueError("Registration pack falsely claims sale or security approval")
        expected = manifest.get("files")
        if not isinstance(expected, dict) or set(expected) != set(names) - {"KIT_EVIDENCE.json"}:
            raise ValueError("Incomplete file provenance inventory")
        for name, digest in expected.items():
            if digest != hashlib.sha256(archive.read(name)).hexdigest():
                raise ValueError("Registration member hash mismatch")
        for name in SHOTS:
            _canonical_png(archive.read("screenshots/" + name), filename=name)
    return {"verified": True, "contract": CONTRACT, "sha256": hashlib.sha256(raw).hexdigest(),
            "member_count": 12, "sale_approved": False, "customer_data_used": False}


def create_registration_kit(output, preview, *, source_sha, source_root=ROOT):
    if not isinstance(source_sha, str) or not SHA_RE.fullmatch(source_sha):
        raise ValueError("Exact public source SHA required")
    members = _input_members(Path(preview), Path(source_root))
    manifest = {
        "contract": CONTRACT,
        "source_commit_sha": source_sha,
        "source_sha_is_cryptographic_signature": False,
        "sample_only": True,
        "customer_data_used": False,
        "sale_approved": False,
        "independent_security_audit_completed": False,
        "release": "RELEASE_HOLD_SALE_NO_GO",
        "full_goal_points": 100,
        "verified_points": 72,
        "files": {key: hashlib.sha256(value).hexdigest() for key, value in sorted(members.items())},
    }
    members["KIT_EVIDENCE.json"] = (
        json.dumps(manifest, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n"
    ).encode("ascii")
    target = Path(output)
    assert_no_links(target, allow_missing_leaf=True)
    if (target.suffix.lower() != ".zip" or target.is_symlink() or target.exists()
            or not target.parent.is_dir() or target.parent.is_symlink()):
        raise FileExistsError("Fresh registration ZIP in existing real directory required")
    parent_info=target.parent.lstat()
    output_directory=open_output_directory(
        target.parent,expected_identity=(parent_info.st_dev,parent_info.st_ino)
    )
    try:
        with create_output_file(target,directory=output_directory) as file:
            with ZipFile(file, "w", compression=ZIP_STORED, allowZip64=False) as archive:
                for name, data in sorted(members.items()):
                    info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                    info.compress_type = ZIP_STORED
                    info.external_attr = 0o100600 << 16
                    archive.writestr(info, data)
        checked = verify_kit(target)
        if checked["member_count"] != 12:
            raise AssertionError("Registration pack was not verified")
        return checked
    finally:
        output_directory.close()


def main():
    parser = argparse.ArgumentParser(description="Create synthetic-only Kmong registration ZIP")
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-sha", type=str, required=True)
    a = parser.parse_args()
    print(json.dumps(create_registration_kit(a.output, a.preview, source_sha=a.source_sha),
                     ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
