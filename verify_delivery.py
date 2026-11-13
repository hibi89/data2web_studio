"""Independent stdlib package verifier: no import from the builder."""
from __future__ import annotations
import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path
from path_policy import assert_no_links, read_bounded_source
from zipfile import ZipFile, ZIP_STORED, BadZipFile

ALLOWED = {"index.html", "manifest.json", "README_KO.txt"}
def _object_no_duplicate_keys(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError("Duplicate ZIP manifest or embedded dataset JSON key")
        result[key]=value
    return result

def _reject_nonfinite_constant(value):
    raise ValueError("Nonfinite JSON values forbidden: "+value)
MAX_ARCHIVE = 24_000_000
MAX_HTML = 20_000_000

def verify_zip(path):
    path = Path(path)
    assert_no_links(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_ARCHIVE:
        raise ValueError("Missing, linked, or oversized package")
    # One verified, bounded file-descriptor snapshot. Never validate one ZIP and
    # hash a separately re-opened version of the same untrusted path.
    raw=read_bounded_source(path,max_bytes=MAX_ARCHIVE)
    try:
        with ZipFile(BytesIO(raw), "r") as archive:
            info = archive.infolist()
            names = [x.filename for x in info]
            if len(info) != 3 or set(names) != ALLOWED or len(set(names)) != 3:
                raise ValueError("Unexpected, duplicated, or unsafe ZIP members")
            for part in info:
                if part.is_dir() or part.compress_type != ZIP_STORED or part.flag_bits & 0x1:
                    raise ValueError("Directory, compression or encryption forbidden")
                limit = MAX_HTML if part.filename == "index.html" else 256_000
                if part.file_size > limit or part.compress_size > limit:
                    raise ValueError("Oversized ZIP member")
                if part.external_attr >> 16 & 0o170000 == 0o120000:
                    raise ValueError("Linked ZIP entry")
            if archive.testzip() is not None:
                raise ValueError("ZIP CRC failure")
            manifest = json.loads(archive.read("manifest.json"),object_pairs_hook=_object_no_duplicate_keys,parse_constant=_reject_nonfinite_constant)
            html = archive.read("index.html")
            guide = archive.read("README_KO.txt")
            if (manifest.get("contract") != "DATA2WEB_PACKAGE_V1"
                    or manifest.get("sale_approved") is not False
                    or manifest.get("plaintext_ack") is not True):
                raise ValueError("Invalid manifest contract")
            for key, content in (("html_sha256", html), ("guide_sha256", guide)):
                if manifest.get(key) != hashlib.sha256(content).hexdigest():
                    raise ValueError("Member integrity mismatch")
            if not html.startswith(b"<!doctype html>") or b"DATA2WEB" not in html:
                raise ValueError("Invalid standalone HTML")
            if not isinstance(manifest.get("rows"), int) or manifest["rows"] < 0:
                raise ValueError("Invalid manifest row count")
            if manifest.get("sheet") is not None and not isinstance(manifest["sheet"], str):
                raise ValueError("Invalid sheet identity")
            if not isinstance(manifest.get("header_row"), int) or not 1 <= manifest["header_row"] <= 50:
                raise ValueError("Invalid header row")
            if not isinstance(manifest.get("cached_formulas"), bool):
                raise ValueError("Invalid formula approval flag")
            import re
            match = re.search(rb'<script type="application/json" id="dataset">([^<]+)</script>', html)
            if not match:
                raise ValueError("Embedded source metadata missing")
            embedded = json.loads(match.group(1),object_pairs_hook=_object_no_duplicate_keys,parse_constant=_reject_nonfinite_constant)
            if (embedded.get("contract") != "DATA2WEB_HTML_V1" or
                    embedded.get("source_sha256") != manifest["source_sha256"] or
                    embedded.get("source_sheet") != manifest["sheet"] or
                    embedded.get("source_header_row") != manifest["header_row"] or
                    embedded.get("cached_formulas") != manifest["cached_formulas"] or
                    len(embedded.get("rows",[])) != manifest["rows"] or
                    embedded.get("source_receipts") != manifest.get("source_receipts")):
                raise ValueError("Embedded data and manifest disagree")
            sources=manifest.get("source_receipts")
            if sources is not None:
                if (not isinstance(sources,list) or not 2<=len(sources)<=10 or
                        not all(isinstance(x,dict) and x.get("position")==i+1 and
                                isinstance(x.get("sha256"),str) and
                                len(x["sha256"])==64 and
                                isinstance(x.get("rows"),int) and x["rows"]>=0
                                for i,x in enumerate(sources))):
                    raise ValueError("Invalid append provenance")
                if sum(x["rows"] for x in sources)!=manifest["rows"]:
                    raise ValueError("Append row count disagrees with sources")
                derivation=json.dumps({"contract":"DATA2WEB_APPENDED_SOURCE_V1","sources":sources},
                                      ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
                if hashlib.sha256(derivation).hexdigest()!=manifest["source_sha256"]:
                    raise ValueError("Append provenance digest mismatch")
            return {"verified": True, "status": "INTEGRITY_VERIFIED_NOT_SALE_APPROVED",
                    "rows": manifest["rows"], "source_sha256": manifest["source_sha256"],
                    "zip_sha256": hashlib.sha256(raw).hexdigest()}
    except (BadZipFile, KeyError, UnicodeError, json.JSONDecodeError) as e:
        raise ValueError("Invalid package structure") from e

def main():
    p=argparse.ArgumentParser(description="Independently verify DATA2WEB delivery ZIP")
    p.add_argument("zip_path")
    a=p.parse_args()
    print(json.dumps(verify_zip(a.zip_path),sort_keys=True))

if __name__=="__main__":
    main()
