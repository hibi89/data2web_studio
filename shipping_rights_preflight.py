"""Synthetic-only verification of the *actual* A delivery and IP inventory.

A passing build here NEVER supplies owner IP permission, legal advice or an
independent audit. All paths and files are generated in disposable tempdirs.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from zipfile import ZipFile

from data2web_single import deliver_single
from r21_source_provenance import check_source_provenance
from verify_customer_folder import EXPECTED as FOLDER_EXPECTED, verify_customer_folder
from verify_delivery import ALLOWED as ZIP_EXPECTED, verify_zip

CONTRACT = "DATA2WEB_SHIPPED_ASSET_RIGHTS_INVENTORY_V1"
INVENTORY = Path(__file__).resolve().parent / "data" / "shipping_rights_inventory_v1.json"
_EXPECTED = {
    ("index.html", "folder_and_zip"),
    ("manifest.json", "zip_only"),
    ("README_KO.txt", "zip_only"),
    ("receipt.json", "folder_only"),
}
_ALLOWED_RIGHTS = {
    "index.html": "PENDING_IP_AND_SOURCE_DATA_RIGHTS",
    "manifest.json": "PENDING_IP_REVIEW",
    "README_KO.txt": "PENDING_IP_REVIEW",
    "receipt.json": "PENDING_IP_REVIEW",
}


def _unique_keys(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise ValueError("Duplicate registry key")
        d[key] = value
    return d


def validate_inventory(doc):
    if not isinstance(doc, dict) or set(doc) != {
        "contract", "source_scope", "rights_approval_state",
        "rights_owner_attested", "commercial_distribution_approved",
        "any_customer_source_inspected", "third_party_vendor_inventory_complete",
        "artifacts", "excluded_assets", "actual_shipped_license_notice_files",
        "future_license_notice_action", "audit_is_independent",
        "scorecard_change_requested",
    }:
        raise ValueError("Registry fields must match unsigned release hold")
    if doc["contract"] != CONTRACT or doc["source_scope"] != (
        "A_OFFLINE_HTML_ZIP_RECEIPT_ONLY_NOT_WINDOWS_EXE"
    ):
        raise ValueError("Unrecognized shipping asset inventory")
    if doc["rights_approval_state"] != "PENDING_OWNER_AND_THIRD_PARTY_REVIEW":
        raise ValueError("Right-state override requires separate legal review and version")
    for key in (
        "rights_owner_attested", "commercial_distribution_approved",
        "any_customer_source_inspected", "third_party_vendor_inventory_complete",
        "audit_is_independent", "scorecard_change_requested",
    ):
        if doc[key] is not False:
            raise ValueError("An unverified approval flag was set")
    if doc["actual_shipped_license_notice_files"] != [] or not isinstance(
        doc["future_license_notice_action"], str
    ):
        raise ValueError("Unapproved LICENSE/NOTICE files cannot be shipped")
    artifacts = doc["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) != 4:
        raise ValueError("All four shipped assets must be accounted for")
    pairs = set()
    for a in artifacts:
        if not isinstance(a, dict) or set(a) != {
            "name", "location", "origin", "rights_state", "vendor_notice_reviewed"
        }:
            raise ValueError("Invalid asset record")
        if (a["name"], a["location"]) in pairs:
            raise ValueError("Duplicate shipping asset")
        pairs.add((a["name"], a["location"]))
        if (a["name"] not in _ALLOWED_RIGHTS or
                a["rights_state"] != _ALLOWED_RIGHTS[a["name"]] or
                a["vendor_notice_reviewed"] is not False or
                not isinstance(a["origin"], str) or not a["origin"]):
            raise ValueError("Shipped asset rights must stay pending")
    if pairs != _EXPECTED:
        raise ValueError("Shipped asset inventory disagrees with v1")
    excluded = doc["excluded_assets"]
    if not isinstance(excluded, list) or {
        a.get("name") for a in excluded if isinstance(a, dict)
    } != {
        "DATA2WEB-LOCAL.exe", "REA_Web upstream code",
        "Python Tcl Tk PyInstaller", "Playwright pypdf"
    } or any(not isinstance(a,dict) or
             set(a) != {"name","reason"} or not a["reason"]
             for a in excluded):
        raise ValueError("Builder, upstream and test assets must remain excluded")
    return True


def read_inventory(path=INVENTORY):
    blob = Path(path).read_bytes()
    if len(blob) > 16_000:
        raise ValueError("Unreasonably long unsigned inventory")
    doc = json.loads(blob.decode("utf-8"),
                     object_pairs_hook=_unique_keys,
                     parse_constant=lambda _: (_ for _ in ()).throw(ValueError(
                         "Non-finite registry value")))
    validate_inventory(doc)
    return doc


def synthetic_shipping_preflight(*, inventory=None):
    doc = read_inventory() if inventory is None else inventory
    validate_inventory(doc)
    # Source pins are technical ancestry checks, never legal rights approval.
    check_source_provenance()
    if ZIP_EXPECTED != {"index.html", "manifest.json", "README_KO.txt"} or (
        FOLDER_EXPECTED != {"index.html", "delivery.zip", "receipt.json"}
    ):
        raise ValueError("Package contract changed; inventory must be remapped")
    with tempfile.TemporaryDirectory(prefix="data2web-shipping-ip-") as temp:
        folder = Path(temp)
        source = folder / "noncustomer-sample.csv"
        source.write_text("id,title,category\nS1,FAKE-DATA,A\n", encoding="utf-8")
        before = source.read_bytes()
        output = folder / "new-customer-folder"
        deliver_single(
            source, output, expected_sha256=hashlib.sha256(before).hexdigest(),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )
        if source.read_bytes() != before:
            raise AssertionError("Source bytes were modified")
        verified = verify_customer_folder(output)
        if not verified["verified"] or verified["sale_approved"] is not False:
            raise AssertionError("Synthetic customer folder integrity failed")
        if {p.name for p in output.iterdir()} != FOLDER_EXPECTED:
            raise AssertionError("Unexpected shipped customer folder asset")
        with ZipFile(output / "delivery.zip") as z:
            if set(z.namelist()) != ZIP_EXPECTED or len(z.namelist()) != 3:
                raise AssertionError("Unapproved ZIP members shipped")
        if not verify_zip(output / "delivery.zip")["verified"]:
            raise AssertionError("ZIP integrity failed")
    return {
        "contract": "DATA2WEB_A_SHIPPING_RIGHTS_PREFLIGHT_V1",
        "status": "HOLD_OWNER_IP_NOTICE_EXTERNAL_AUDIT",
        "technical_synthetic_integrity_verified": True,
        "shipping_member_count": 4,
        "rights_owner_attested": False,
        "commercial_release_approved": False,
        "external_independent_audit_completed": False,
        "score_addition": 0,
        "customer_source_ever_required": False,
    }


if __name__ == "__main__":
    print(json.dumps(synthetic_shipping_preflight(), ensure_ascii=True,
                     sort_keys=True))
