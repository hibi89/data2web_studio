"""Independent local customer-folder verifier.

Cross-checks the on-disk HTML, exact deterministic ZIP, and the create-only
JSON receipt. Does not read or upload customer source files, never deletes or
modifies any artifact, and cannot prove its commercial rights/signature.
"""
from __future__ import annotations
import hashlib
import json
import re
import stat
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from path_policy import assert_no_links, read_bounded_source
from verify_delivery import verify_zip, MAX_ARCHIVE

EXPECTED={"index.html","delivery.zip","receipt.json"}
RECEIPT_FIELDS={
    "contract","status","source_sha256","output_sha256","rows","columns",
    "mapping","sheet","header_row","cached_formulas","source_receipts",
    "privacy_classification","sale_approved",
}
HEX="0123456789abcdef"

def _unique_pairs(pairs):
    target={}
    for k,v in pairs:
        if k in target:
            raise ValueError("Duplicate receipt or manifest key")
        target[k]=v
    return target

def _reject_nonfinite_constant(value):
    raise ValueError("Non-finite receipt or manifest JSON constant forbidden")

def _load_json(data, *, max_bytes=256_000):
    if len(data)>max_bytes:
        raise ValueError("Receipt/manifest exceeds safe size")
    doc=json.loads(data.decode("utf-8"),object_pairs_hook=_unique_pairs,
                   parse_constant=_reject_nonfinite_constant)
    if not isinstance(doc,dict):
        raise ValueError("Receipt/manifest must be a JSON object")
    return doc

def _is_sha(digest):
    return isinstance(digest,str) and len(digest)==64 and all(x in HEX for x in digest)

def _folder_identity(root):
    """Detect persistent root replacement or member changes during a verify pass.

    An ordinary pathname is not a transaction or immutable snapshot. Compare
    root identity/metadata at the start and end, and enumerate members twice.
    This narrows races but cannot defeat an adversary who swaps and restores
    everything between checks (R06 field acceptance still pending).
    """
    assert_no_links(root)
    info = root.lstat()
    if not stat.S_ISDIR(info.st_mode):
        raise ValueError("Customer delivery folder is not a real directory")
    return (info.st_dev, info.st_ino, info.st_mode,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def verify_customer_folder(destination):
    root=Path(destination)
    starting_identity=_folder_identity(root)
    items=list(root.iterdir())
    if len(items)!=3 or {p.name for p in items}!=EXPECTED:
        raise ValueError("Unexpected, missing, or duplicated delivery folder member")
    for path in items:
        assert_no_links(path)
        if not path.is_file():
            raise ValueError("Customer folder contains a non-file entry")

    html=read_bounded_source(root/"index.html",max_bytes=20_000_000)
    if not html.startswith(b"<!doctype html>") or len(html)>20_000_000:
        raise ValueError("Invalid or oversized local HTML")
    rbytes=read_bounded_source(root/"receipt.json",max_bytes=256_000)
    receipt=_load_json(rbytes)
    if (set(receipt)!=RECEIPT_FIELDS or
            receipt.get("contract")!="DATA2WEB_RECEIPT_V1" or
            receipt.get("status")!="INTEGRITY_RECEIPT_ONLY_NOT_CUSTOMER_OR_SALE_APPROVAL" or
            receipt.get("sale_approved") is not False or
            receipt.get("privacy_classification") not in
                ("NO_PERSONAL_DATA_REVIEWED","OWNER_APPROVED_LOCAL_ONLY")):
        raise ValueError("Incomplete or unapproved customer delivery receipt")
    if not _is_sha(receipt.get("source_sha256")) or not _is_sha(receipt.get("output_sha256")):
        raise ValueError("Invalid source/output digest format")
    if receipt["output_sha256"]!=hashlib.sha256(html).hexdigest():
        raise ValueError("On-disk HTML modified since owner receipt")

    verified=verify_zip(root/"delivery.zip")
    if not verified["verified"]:
        raise ValueError("Independent ZIP verification failed")
    zip_snapshot=read_bounded_source(root/"delivery.zip",max_bytes=MAX_ARCHIVE)
    if hashlib.sha256(zip_snapshot).hexdigest()!=verified["zip_sha256"]:
        raise ValueError("Delivery ZIP changed between independent checks")
    with ZipFile(BytesIO(zip_snapshot),"r") as z:
        if z.read("index.html")!=html:
            raise ValueError("Delivery HTML is not the exact ZIP member")
        manifest=_load_json(z.read("manifest.json"))
    expected_pairs=(
        ("source_sha256","source_sha256"),
        ("html_sha256","output_sha256"),
        ("rows","rows"),
        ("sheet","sheet"),
        ("header_row","header_row"),
        ("cached_formulas","cached_formulas"),
        ("source_receipts","source_receipts"),
    )
    for left,right in expected_pairs:
        if manifest.get(left)!=receipt.get(right):
            raise ValueError("Receipt fields do not match independently verified ZIP")
    if type(receipt["rows"]) is not int or receipt["rows"]<0:
        raise ValueError("Invalid row count")
    match=re.search(rb'<script type="application/json" id="dataset">([^<]+)</script>',html)
    if match is None:
        raise ValueError("Local HTML source table missing")
    embedded=_load_json(match.group(1),max_bytes=20_000_000)
    columns=embedded.get("columns")
    mapping=embedded.get("mapping")
    if (not isinstance(columns,list) or not all(isinstance(x,str) for x in columns)
            or receipt["columns"]!=columns or not isinstance(mapping,list) or len(mapping)!=3
            or not isinstance(receipt.get("mapping"),dict)
            or set(receipt["mapping"])!={"id","title","category"}
            or [receipt["mapping"][key] for key in ("id","title","category")]!=mapping):
        raise ValueError("Receipt columns or explicit field map do not match HTML")
    if (embedded.get("source_sha256")!=receipt["source_sha256"] or
            embedded.get("source_receipts")!=receipt["source_receipts"] or
            len(embedded.get("rows",[]))!=receipt["rows"]):
        raise ValueError("Embedded source evidence differs from customer receipt")
    # A new unexpected file inserted after the first enumeration must HOLD,
    # even if the HTML, ZIP and receipt all have matching checksums.
    if _folder_identity(root) != starting_identity:
        raise ValueError("Customer folder changed during verification")
    final_members=list(root.iterdir())
    if len(final_members)!=3 or {p.name for p in final_members}!=EXPECTED:
        raise ValueError("Customer folder members changed during verification")
    for member in final_members:
        assert_no_links(member)
        if not member.is_file():
            raise ValueError("Customer folder member became unsafe")
    # The directory may remain unchanged while a writer edits an existing
    # HTML, receipt or ZIP in-place after its earlier validated snapshot.
    # Re-read each bounded file by its identity-checked handle before success.
    # This narrows persistent byte-replacement races; no pathname API provides
    # a fully atomic snapshot against concurrent hostile writers.
    for name, snapshot, limit in (
        ("index.html", html, 20_000_000),
        ("receipt.json", rbytes, 256_000),
        ("delivery.zip", zip_snapshot, MAX_ARCHIVE),
    ):
        if read_bounded_source(root/name, max_bytes=limit) != snapshot:
            raise ValueError("Customer artifact changed during verification")
    if _folder_identity(root) != starting_identity:
        raise ValueError("Customer folder changed during final inventory")
    return {
        "verified":True,
        "contract":"DATA2WEB_CUSTOMER_FOLDER_V1",
        "status":"LOCAL_INTEGRITY_VERIFIED_RELEASE_HOLD_NOT_SALE_APPROVED",
        "rows":receipt["rows"],
        "html_sha256":receipt["output_sha256"],
        "zip_sha256":verified["zip_sha256"],
        "receipt_sha256":hashlib.sha256(rbytes).hexdigest(),
        "sale_approved":False,
    }

def diagnose_customer_folder(destination):
    """Read-only, redacted HOLD classification for a local customer folder.

    No filenames beyond the three fixed contract members, customer values,
    paths or exception messages leave this function. A complete folder must
    still pass the full independent verifier; this is not a recovery/write API.
    """
    root = Path(destination)
    base = {
        "verified": False,
        "status": "HOLD",
        "sale_approved": False,
    }
    try:
        assert_no_links(root, allow_missing_leaf=True)
        if not root.is_dir():
            return {**base, "reason_code": "MISSING_OR_UNSAFE_DIRECTORY"}
        starting_identity = _folder_identity(root)
        observed = {p.name for p in root.iterdir()}
        if observed != EXPECTED:
            if _folder_identity(root) != starting_identity:
                return {**base, "reason_code": "INTEGRITY_CHECK_FAILED"}
            return {
                **base,
                "reason_code": "INCOMPLETE_OR_UNEXPECTED_MEMBERS",
                "present": {name: name in observed for name in sorted(EXPECTED)},
                "unexpected_member_count": len(observed - EXPECTED),
            }
        verified = verify_customer_folder(root)
        return {
            "verified": True,
            "status": verified["status"],
            "sale_approved": False,
            "reason_code": "FULL_INTEGRITY_VERIFIED_NOT_SALE_APPROVED",
        }
    except (OSError, ValueError):
        # Do not include exception messages: they may contain customer paths.
        return {**base, "reason_code": "INTEGRITY_CHECK_FAILED"}
