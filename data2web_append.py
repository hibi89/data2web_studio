"""Explicit per-source approved same-schema *append*, never JOIN.

Manifest is local owner input; individual hashes and sheet choices are checked
again immediately before and after output generation. No cloud upload or
source deletion. The manifest is not a digital signature or commercial approval.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from data2web import read_table, MAX_ROWS, MAX_COLS, MAX_BYTES
from data2web_web import render_html
from delivery import package_html
from receipt_utils import write_receipt, assert_receipt_path_available
from path_policy import assert_no_links, read_bounded_source
from secure_output import create_output_directory, create_output_file

CONTRACT="DATA2WEB_INPUT_APPROVALS_V1"
COMBINED="DATA2WEB_APPENDED_SOURCE_V1"
MAX_INPUTS=10
MAX_OUTPUT=20_000_000

def unique_keys(pairs):
    obj={}
    for key,value in pairs:
        if key in obj:
            raise ValueError("Duplicate approval manifest key")
        obj[key]=value
    return obj

def read_approval_manifest(path):
    p=Path(path)
    assert_no_links(p)
    if p.is_symlink() or not p.is_file() or p.suffix.lower() != ".json" or p.stat().st_size>64000:
        raise ValueError("Unsafe approval manifest")
    raw=read_bounded_source(p,max_bytes=64000)
    doc=json.loads(raw.decode("utf-8-sig"),object_pairs_hook=unique_keys)
    return validate_approval_doc(doc)

def validate_approval_doc(doc):
    if not isinstance(doc,dict) or doc.get("contract") != CONTRACT:
        raise ValueError("Invalid approval manifest contract")
    sources=doc.get("sources")
    if not isinstance(sources,list) or not 2<=len(sources)<=MAX_INPUTS:
        raise ValueError("Append requires two to ten individually inspected sources")
    mapping=doc.get("mapping")
    if (not isinstance(mapping,dict) or set(mapping)!={"id","title","category"} or
            not all(isinstance(v,str) and v for v in mapping.values()) or
            len(set(mapping.values()))!=3):
        raise ValueError("Three distinct explicit column mappings required")
    approval=doc.get("approval")
    if (not isinstance(approval,dict) or
            approval.get("rights_and_plaintext_ack") is not True or
            approval.get("privacy_classification") not in ("NO_PERSONAL_DATA_REVIEWED","OWNER_APPROVED_LOCAL_ONLY")):
        raise ValueError("Owner data-rights/privacy review has not been approved")
    return doc


def source_path(manifest_path, filename):
    if (not isinstance(filename,str) or not filename or len(filename)>180 or
            filename in (".","..") or
            Path(filename).name!=filename or
            "/" in filename or "\\" in filename or
            any(ord(c)<32 or ord(c)==127 for c in filename)):
        raise ValueError("Source filenames must be simple local basenames")
    base=Path(manifest_path).parent
    if base.is_symlink():
        raise ValueError("Manifest parent symlink not allowed")
    file=base/filename
    assert_no_links(file)
    if file.is_symlink() or not file.is_file():
        raise ValueError("Missing or linked append input")
    return file

def approved_sources(manifest_path, doc):
    columns=None
    joined=[]
    provenance=[]
    files=[]
    unique_ids=set()
    mapping=doc["mapping"]
    seen_files=set()
    for index,entry in enumerate(doc["sources"]):
        if not isinstance(entry,dict):
            raise ValueError("Invalid per-file approval")
        filename=entry.get("filename")
        path=source_path(manifest_path,filename)
        if path.name.casefold() in seen_files:
            raise ValueError("Same source cannot be appended twice")
        seen_files.add(path.name.casefold())
        expected=entry.get("sha256")
        if not isinstance(expected,str) or len(expected)!=64 or any(c not in "0123456789abcdef" for c in expected):
            raise ValueError("Source requires exact lowercase SHA256")
        sheet=entry.get("sheet")
        header=entry.get("header_row",1)
        allow_cache=entry.get("allow_cached_formulas",False)
        if (sheet is not None and (not isinstance(sheet,str) or not sheet) or
                type(header) is not int or not 1<=header<=50 or type(allow_cache) is not bool):
            raise ValueError("Invalid source sheet/header/cache settings")
        if path.suffix.lower()==".xlsx" and not sheet:
            raise ValueError("Explicit worksheet choice required per XLSX")
        if path.suffix.lower()!=".xlsx" and (sheet is not None or header!=1 or allow_cache):
            raise ValueError("Non-XLSX source cannot use spreadsheet-only options")
        actual=hashlib.sha256(read_bounded_source(path,max_bytes=MAX_BYTES)).hexdigest()
        if actual!=expected:
            raise ValueError("Source SHA changed since approval")
        names,rows,digest=read_table(path,sheet=sheet,header_row=header,
                                    allow_cached_formulas=allow_cache)
        if digest!=expected:
            raise ValueError("Source hash changed during parse")
        if columns is None:
            columns=names
            if len(columns)>MAX_COLS or not all(m in columns for m in mapping.values()):
                raise ValueError("Mapped columns missing from approved schema")
        elif names!=columns:
            raise ValueError("Append requires exactly identical ordered columns")
        for record in rows:
            identity=record[mapping["id"]]
            if not identity or identity in unique_ids:
                raise ValueError("Duplicate or missing primary IDs across all files")
            unique_ids.add(identity)
        joined.extend(rows)
        if len(joined)>MAX_ROWS:
            raise ValueError("Combined row limit exceeded")
        provenance.append({
            "position":index+1,"sha256":digest,"rows":len(rows),
            "kind":path.suffix.lower()[1:],"sheet":sheet,
            "header_row":header,"cached_formulas":allow_cache,
        })
        files.append((path,digest))
    return columns,joined,provenance,files

def provenance_sha(sources):
    raw=json.dumps({"contract":COMBINED,"sources":sources},ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def build_approved_append(approval_manifest,html_path,*,confirm,ack_plaintext,zip_path=None,receipt_path=None):
    if confirm!="APPROVE" or ack_plaintext is not True:
        raise ValueError("Explicit owner append approval is required")
    doc=read_approval_manifest(approval_manifest)
    return _build_approved_append_doc(doc,approval_manifest,html_path,
             confirm=confirm,ack_plaintext=ack_plaintext,
             zip_path=zip_path,receipt_path=receipt_path)

def _build_approved_append_doc(doc,approval_manifest,html_path,*,
                                confirm,ack_plaintext,zip_path=None,receipt_path=None,
                                _output_directory=None):
    if confirm!="APPROVE" or ack_plaintext is not True:
        raise ValueError("Explicit owner append approval is required")
    validate_approval_doc(doc)
    columns,rows,sources,files=approved_sources(approval_manifest,doc)
    mapping=doc["mapping"]
    identity=provenance_sha(sources)
    html_path=Path(html_path)
    if html_path.is_symlink() or html_path.exists():
        raise FileExistsError("Append output already exists")
    assert_no_links(html_path,allow_missing_leaf=True)
    if (html_path.suffix.lower()!=".html" or html_path.is_symlink() or html_path.exists() or
            not html_path.parent.is_dir() or html_path.parent.is_symlink()):
        raise FileExistsError("Append output must be new .html in an existing real directory")
    if zip_path is not None:
        z=Path(zip_path)
        assert_no_links(z,allow_missing_leaf=True)
        if (z.suffix.lower()!=".zip" or z.exists() or z.is_symlink() or
                not z.parent.is_dir() or z.parent.is_symlink()):
            raise FileExistsError("Append ZIP output must be new")
    assert_receipt_path_available(receipt_path)
    markup=render_html(columns,rows,[mapping["id"],mapping["title"],mapping["category"]],
                       identity,name=doc.get("name","DATA2WEB"),theme=doc.get("theme","office"),
                       source_receipts=sources)
    raw=markup.encode("utf-8")
    if len(raw)>MAX_OUTPUT:
        raise ValueError("HTML output exceeds offline delivery limit")
    for path,sha in files:
        if hashlib.sha256(read_bounded_source(path,max_bytes=MAX_BYTES)).hexdigest()!=sha:
            raise ValueError("Input mutated before publish")
    with create_output_file(html_path,directory=_output_directory) as output:
        output.write(raw)
    for path,sha in files:
        if hashlib.sha256(read_bounded_source(path,max_bytes=MAX_BYTES)).hexdigest()!=sha:
            raise ValueError("Input mutated after publish; output HOLD")
    outsha=hashlib.sha256(read_bounded_source(html_path,max_bytes=MAX_OUTPUT)).hexdigest()
    if outsha!=hashlib.sha256(raw).hexdigest():
        raise ValueError("Output differs from generated HTML")
    receipt={
        "source_sha256":identity,"output_sha256":outsha,
        "rows":len(rows),"columns":columns,"mapping":mapping,
        "sheet":None,"header_row":1,"cached_formulas":False,
        "source_receipts":sources,
        "privacy_classification":doc["approval"]["privacy_classification"],
        "sale_approved":False,
        "status":"OWNER_APPROVED_APPEND_LOCAL_ONLY_RELEASE_HOLD",
    }
    if zip_path is not None:
        receipt["package"]=package_html(html_path,zip_path,receipt,
                                         _output_directory=_output_directory)
        # The pre-write checks are not sufficient when packaging races a
        # source edit. The receipt is issued only after the post-ZIP hashes.
        for path,sha in files:
            if hashlib.sha256(read_bounded_source(path,max_bytes=MAX_BYTES)).hexdigest()!=sha:
                raise ValueError("Approved source modified during ZIP packaging; output HOLD")
    if receipt_path is not None:
        receipt["receipt_file"]=write_receipt(receipt_path,receipt,
                                               _output_directory=_output_directory)
    return receipt

def deliver_to_new_directory(approval_manifest, destination, *, confirm, ack_plaintext):
    """Existing manifest-driven CLI API; preserves all v1 semantics."""
    if confirm!="APPROVE" or ack_plaintext is not True:
        raise ValueError("Explicit approval is required for delivery")
    doc=read_approval_manifest(approval_manifest)
    return _deliver_approved_append_doc(doc,approval_manifest,destination,
                  confirm=confirm,ack_plaintext=ack_plaintext)

def deliver_reviewed_sources(doc, source_directory, destination, *, confirm, ack_plaintext):
    """GUI entrypoint: in-memory owner approvals, no temp manifest on disk.

    All source paths are resolved relative to one real source directory.
    Existing append core re-reads SHA/headers/IDs before creating new output.
    """
    if confirm!="APPROVE" or ack_plaintext is not True:
        raise ValueError("Explicit approval required")
    base=Path(source_directory)
    assert_no_links(base)
    if not base.is_dir():
        raise ValueError("Real source directory required")
    validate_approval_doc(doc)
    # The reference is never opened or created. Only its .parent is used by
    # source_path(), so no extra approval JSON enters customer source folders.
    reference=base/".DATA2WEB-IN-MEMORY-APPROVAL-NOT-A-FILE.json"
    return _deliver_approved_append_doc(doc,reference,destination,
                   confirm=confirm,ack_plaintext=ack_plaintext)

def _deliver_approved_append_doc(doc, approval_manifest, destination, *,
                                 confirm, ack_plaintext):
    """Create-only full customer folder with the same validated append engine."""
    if confirm!="APPROVE" or ack_plaintext is not True:
        raise ValueError("Explicit approval is required for delivery")
    validate_approval_doc(doc)
    approved_sources(approval_manifest,doc)  # fail before creating the folder
    path=Path(destination)
    assert_no_links(path,allow_missing_leaf=True)
    if (path.exists() or path.is_symlink() or
            not path.parent.is_dir() or path.parent.is_symlink() or
            path.name in ("", ".", "..")):
        raise FileExistsError("Delivery destination must be a new folder")
    with create_output_directory(path) as output_directory:
        result=_build_approved_append_doc(doc,approval_manifest,path/"index.html",
                  confirm=confirm,ack_plaintext=ack_plaintext,
                  zip_path=path/"delivery.zip",receipt_path=path/"receipt.json",
                  _output_directory=output_directory)
        # Do not advertise an approved customer folder until the independently
        # checked HTML, ZIP and *final* receipt agree on disk.
        from verify_customer_folder import verify_customer_folder
        verify_customer_folder(path)
        result["delivery_folder_created"]=True
        result["status"]="DELIVERY_FOLDER_CREATED_RELEASE_HOLD_NOT_SALE_APPROVED"
        return result
