"""Create-only SHA receipt; do not write customer values or expose private paths."""
from __future__ import annotations
import json
import os
from pathlib import Path

def assert_receipt_path_available(path):
    if path is None:
        return
    p=Path(path)
    if p.suffix.lower() != ".json" or p.is_symlink() or p.exists() or not p.parent.is_dir() or p.parent.is_symlink():
        raise FileExistsError("Receipt target must be a fresh .json file in an existing real directory")

def write_receipt(path, receipt):
    if path is None:
        return None
    assert_receipt_path_available(path)
    approved={
        "contract":"DATA2WEB_RECEIPT_V1",
        "status":"INTEGRITY_RECEIPT_ONLY_NOT_CUSTOMER_OR_SALE_APPROVAL",
        "source_sha256":receipt["source_sha256"],
        "output_sha256":receipt["output_sha256"],
        "rows":receipt["rows"],
        "columns":receipt["columns"],
        "mapping":receipt["mapping"],
        "sheet":receipt.get("sheet"),
        "header_row":receipt.get("header_row",1),
        "cached_formulas":receipt.get("cached_formulas",False),
        "source_receipts":receipt.get("source_receipts"),
        "privacy_classification":receipt.get("privacy_classification","UNREVIEWED"),
        "sale_approved":False,
    }
    data=(json.dumps(approved,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
    p=Path(path)
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,"wb") as out:
        out.write(data)
    return {"receipt_created":True,"contract":approved["contract"]}
