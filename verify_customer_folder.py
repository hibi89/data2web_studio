"""Independent local customer-folder verifier.

Cross-checks the on-disk HTML, exact deterministic ZIP, and the create-only
JSON receipt. Does not read or upload customer source files, never deletes or
modifies any artifact, and cannot prove its commercial rights/signature.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile

from path_policy import assert_no_links
from verify_delivery import verify_zip

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

def _load_json(data):
    if len(data)>256_000:
        raise ValueError("Receipt/manifest exceeds safe size")
    doc=json.loads(data.decode("utf-8"),object_pairs_hook=_unique_pairs)
    if not isinstance(doc,dict):
        raise ValueError("Receipt/manifest must be a JSON object")
    return doc

def _is_sha(digest):
    return isinstance(digest,str) and len(digest)==64 and all(x in HEX for x in digest)

def verify_customer_folder(destination):
    root=Path(destination)
    assert_no_links(root)
    if not root.is_dir():
        raise ValueError("Customer delivery folder is not a real directory")
    items=list(root.iterdir())
    if len(items)!=3 or {p.name for p in items}!=EXPECTED:
        raise ValueError("Unexpected, missing, or duplicated delivery folder member")
    for path in items:
        assert_no_links(path)
        if not path.is_file():
            raise ValueError("Customer folder contains a non-file entry")

    html=(root/"index.html").read_bytes()
    if not html.startswith(b"<!doctype html>") or len(html)>20_000_000:
        raise ValueError("Invalid or oversized local HTML")
    rbytes=(root/"receipt.json").read_bytes()
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
    with ZipFile(root/"delivery.zip","r") as z:
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
    embedded=_load_json(match.group(1))
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
