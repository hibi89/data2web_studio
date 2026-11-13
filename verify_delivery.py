"""Independent stdlib package verifier: no import from the builder."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED, BadZipFile

ALLOWED = {"index.html", "manifest.json", "README_KO.txt"}
MAX_ARCHIVE = 24_000_000
MAX_HTML = 20_000_000

def verify_zip(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_ARCHIVE:
        raise ValueError("Missing, linked, or oversized package")
    try:
        with ZipFile(path, "r") as archive:
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
            manifest = json.loads(archive.read("manifest.json"))
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
            return {"verified": True, "status": "INTEGRITY_VERIFIED_NOT_SALE_APPROVED",
                    "rows": manifest["rows"], "source_sha256": manifest["source_sha256"],
                    "zip_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    except (BadZipFile, KeyError, UnicodeError, json.JSONDecodeError) as e:
        raise ValueError("Invalid package structure") from e

def main():
    p=argparse.ArgumentParser(description="Independently verify DATA2WEB delivery ZIP")
    p.add_argument("zip_path")
    a=p.parse_args()
    print(json.dumps(verify_zip(a.zip_path),sort_keys=True))

if __name__=="__main__":
    main()
