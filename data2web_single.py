"""Owner-approved single-file create-only customer delivery.

This is a local build operation, not an authorization to sell or redistribute.
The caller supplies one reviewed exact SHA, mapping, and privacy assertion.
All generated artifacts stay inside a newly created directory.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
from data2web import build, read_table
from data2web_web import render_html
from delivery import package_html
from receipt_utils import write_receipt
from path_policy import assert_no_links

PRIVACY_MODES=("NO_PERSONAL_DATA_REVIEWED","OWNER_APPROVED_LOCAL_ONLY")

def deliver_single(source, new_directory, *,
                   expected_sha256, id_column, title_column, category_column,
                   confirm, ack_plaintext, privacy_classification,
                   sheet=None, header_row=1, allow_cached_formulas=False,
                   name="DATA2WEB", theme="office"):
    if confirm!="APPROVE" or ack_plaintext is not True:
        raise ValueError("Explicit rights and plaintext approval required")
    if privacy_classification not in PRIVACY_MODES:
        raise ValueError("Owner privacy classification must be explicitly reviewed")
    if (not isinstance(expected_sha256,str) or len(expected_sha256)!=64 or
            any(c not in "0123456789abcdef" for c in expected_sha256)):
        raise ValueError("Exact lowercase source SHA256 required")
    source=Path(source)
    if source.suffix.lower()==".xlsx" and not sheet:
        raise ValueError("XLSX delivery requires owner-selected worksheet")
    assert_no_links(source)
    # Preflight all content/mapping/size and current source before making a folder.
    columns,records,digest=read_table(source,sheet=sheet,header_row=header_row,
                                      allow_cached_formulas=allow_cached_formulas)
    if digest!=expected_sha256:
        raise ValueError("Source changed since owner inspection")
    mapping=[id_column,title_column,category_column]
    if len(set(mapping))!=3 or not all(c in columns for c in mapping):
        raise ValueError("Three distinct mapped columns required")
    keys=[r[id_column] for r in records]
    if any(not key for key in keys) or len(set(keys))!=len(keys):
        raise ValueError("Source has missing or duplicate IDs")
    # Validate final standalone HTML and output budget before touching disk.
    artifact=render_html(columns,records,mapping,digest,name=name,theme=theme,
                         source_sheet=sheet,source_header_row=header_row,
                         cached_formulas=allow_cached_formulas)
    if len(artifact.encode("utf-8"))>20_000_000:
        raise ValueError("Output HTML would exceed delivery limit")
    destination=Path(new_directory)
    assert_no_links(destination,allow_missing_leaf=True)
    if (destination.is_symlink() or destination.exists() or
            not destination.parent.is_dir() or destination.parent.is_symlink() or
            destination.name in ("", ".", "..")):
        raise FileExistsError("New customer delivery folder required")
    # No recursive automatic cleanup: failed delivery folder remains HOLD
    # for human investigation, never overwritten on retry.
    destination.mkdir(mode=0o700,exist_ok=False)
    receipt=build(source,destination/"index.html",id_column,title_column,category_column,
                  approved=True,expected_sha256=expected_sha256,
                  name=name,theme=theme,sheet=sheet,header_row=header_row,
                  allow_cached_formulas=allow_cached_formulas)
    receipt["privacy_classification"]=privacy_classification
    receipt["status"]="SINGLE_OWNER_APPROVED_LOCAL_DELIVERY_RELEASE_HOLD"
    receipt["package"]=package_html(destination/"index.html",destination/"delivery.zip",receipt)
    receipt["receipt_file"]=write_receipt(destination/"receipt.json",receipt)
    receipt["delivery_folder_created"]=True
    receipt["sale_approved"]=False
    return receipt
