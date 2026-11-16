"""Create-only SHA receipt; do not write customer values or expose private paths."""
from __future__ import annotations
import json
from pathlib import Path
from path_policy import assert_no_links
from secure_output import create_output_file, open_output_directory

def assert_receipt_path_available(path):
    if path is None:
        return
    p=Path(path)
    assert_no_links(p,allow_missing_leaf=True)
    if p.suffix.lower() != ".json" or p.is_symlink() or p.exists() or not p.parent.is_dir() or p.parent.is_symlink():
        raise FileExistsError("Receipt target must be a fresh .json file in an existing real directory")

def write_receipt(path, receipt, *, _output_directory=None):
    if path is None:
        return None
    assert_receipt_path_available(path)
    p=Path(path)
    owns_output_directory=_output_directory is None
    if owns_output_directory:
        parent_info=p.parent.lstat()
        _output_directory=open_output_directory(
            p.parent,expected_identity=(parent_info.st_dev,parent_info.st_ino)
        )
    elif p.parent.absolute() != _output_directory.path:
        raise ValueError("Output directory handle does not match receipt parent")
    try:
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
        with create_output_file(p,directory=_output_directory) as out:
            out.write(data)
        return {"receipt_created":True,"contract":approved["contract"]}
    finally:
        if owns_output_directory:
            _output_directory.close()
