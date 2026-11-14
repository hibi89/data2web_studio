"""Fail-closed Git blob provenance pinning of R21 source producers.

Pinning source bytes is an engineering origin record, not copyright consent,
proof of legal distribution rights, an independent audit, or a release gate GO.
Never scans or logs actual customer input files.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PINS=ROOT/"data"/"r21_source_provenance_v1.json"
CONTRACT="DATA2WEB_R21_SOURCE_PROVENANCE_PINS_V1"
ROLES={
    "data2web_web.py":"GENERATES_CUSTOMER_HTML_CSS_JS",
    "delivery.py":"GENERATES_ZIP_MANIFEST_GUIDE",
    "receipt_utils.py":"GENERATES_LOCAL_RECEIPT",
    "data2web_single.py":"OWNER_ONLY_DELIVERY_PRODUCER",
    "data2web_append.py":"OWNER_ONLY_APPEND_PRODUCER",
    "data2web_tabular.py":"OWNER_ONLY_TABULAR_PARSER",
}
HOLD_FLAGS=(
    "rights_evidence_complete",
    "third_party_notice_approved",
    "commercial_release_approved",
    "independent_security_audit_completed",
)
KEYS={"contract","source_snapshot_commit","source_files","score_addition",*HOLD_FLAGS}
HEX=set("0123456789abcdef")


def git_blob_oid(data):
    """Compute Git SHA-1 blob OID (revision identity, not a signature)."""
    if type(data) is not bytes:
        raise TypeError("Git blob content must be bytes")
    return hashlib.sha1(
        b"blob "+str(len(data)).encode("ascii")+b"\x00"+data
    ).hexdigest()


def _unique(pairs):
    result={}
    for k,v in pairs:
        if k in result:
            raise ValueError("Duplicate provenance key")
        result[k]=v
    return result


def validate_pins(manifest):
    if type(manifest) is not dict or set(manifest)!=KEYS:
        raise ValueError("Unknown or incomplete R21 source provenance fields")
    if manifest["contract"]!=CONTRACT:
        raise ValueError("Unknown provenance contract")
    sha=manifest["source_snapshot_commit"]
    if type(sha) is not str or len(sha)!=40 or any(c not in HEX for c in sha):
        raise ValueError("Source snapshot commit must be a fixed Git SHA")
    if type(manifest["score_addition"]) is not int or manifest["score_addition"]!=0:
        raise ValueError("Source provenance cannot change final score")
    for flag in HOLD_FLAGS:
        if manifest[flag] is not False:
            raise ValueError("Source origin is not a license or sale approval")
    rows=manifest["source_files"]
    if type(rows) is not list or len(rows)!=len(ROLES):
        raise ValueError("Source provenance must enumerate all producer files")
    seen=set()
    for item in rows:
        if type(item) is not dict or set(item)!={"path","git_blob_sha1","role"}:
            raise ValueError("Source provenance row shape invalid")
        path=item["path"]
        if type(path) is not str or path not in ROLES or path in seen:
            raise ValueError("Unlisted, duplicate, or unsafe source file")
        seen.add(path)
        if item["role"]!=ROLES[path]:
            raise ValueError("Producer role changed without origin review")
        sha=item["git_blob_sha1"]
        if type(sha) is not str or len(sha)!=40 or any(c not in HEX for c in sha):
            raise ValueError("Invalid producer blob digest")
    if seen!=set(ROLES):
        raise ValueError("Missing producer source identity")
    return manifest


def read_pins(path=PINS):
    # Registry only. Never follow a user-supplied customer file or path.
    blob=Path(path).read_bytes()
    if len(blob)>8192:
        raise ValueError("Provenance registry oversized")
    return validate_pins(json.loads(
        blob.decode("utf-8"),object_pairs_hook=_unique,
        parse_constant=lambda _: (_ for _ in ()).throw(
            ValueError("Nonfinite registry data forbidden"))
    ))


def check_source_provenance(*,root=ROOT,manifest=None):
    """Check pinned source bytes; reject drift before synthetic shipping test."""
    doc=read_pins() if manifest is None else validate_pins(manifest)
    root=Path(root)
    # The paths are a closed internal whitelist, not customer-supplied.
    for item in doc["source_files"]:
        source=root/item["path"]
        from path_policy import read_bounded_source
        raw=read_bounded_source(source,max_bytes=200_000)
        if git_blob_oid(raw)!=item["git_blob_sha1"]:
            raise ValueError("Shipping producer source drift requires R21 review")
    return {
        "contract":CONTRACT,
        "status":"SOURCE_BLOBS_PINNED_RIGHTS_PENDING",
        "source_files_verified":len(ROLES),
        "source_commit_snapshot":doc["source_snapshot_commit"],
        "rights_evidence_complete":False,
        "third_party_notice_approved":False,
        "commercial_release_approved":False,
        "independent_security_audit_completed":False,
        "score_addition":0,
    }


if __name__=="__main__":
    print(json.dumps(check_source_provenance(),sort_keys=True))
