"""Independent stdlib package verifier: no import from the builder."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
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
PACKAGE_KEYS = {"contract", "source_sha256", "html_sha256", "guide_sha256",
                "rows", "sheet", "header_row", "cached_formulas",
                "source_receipts", "plaintext_ack", "sale_approved", "status"}
_HEX = set("0123456789abcdef")

def _is_sha256(value):
    return (isinstance(value, str) and len(value) == 64
            and all(char in _HEX for char in value))

def _validate_offline_html_csp(html):
    """Validate the HTML's single-static-script CSP safety contract.

    This is a *structural* security check, not a publisher signature.
    An attacker who can rewrite the ZIP AND recompute every SHA256 may
    replace both script and matching CSP hash. Source authenticity and
    reviewer trust still require separate out-of-band evidence.
    """
    # Only the generator's data JSON script and one static executable script
    # may be present; injection or duplicate policy tags are rejected.
    meta = re.findall(
        rb'<meta http-equiv="Content-Security-Policy" content="([^"]+)">',
        html
    )
    scripts = re.findall(rb"<script>(.*?)</script>", html, flags=re.DOTALL)
    if (len(meta) != 1 or len(scripts) != 1
            or len(re.findall(rb"<script\b", html, flags=re.IGNORECASE)) != 2
            or len(re.findall(rb"</script\s*>", html, flags=re.IGNORECASE)) != 2
            or len(re.findall(rb'http-equiv\s*=\s*["\']content-security-policy["\']',
                              html, flags=re.IGNORECASE)) != 1):
        raise ValueError("Standalone HTML script or CSP structure changed")
    digest = base64.b64encode(hashlib.sha256(scripts[0]).digest())
    approved = (
        b"default-src 'none'; script-src 'sha256-" + digest +
        b"'; style-src 'unsafe-inline'; img-src 'none'; connect-src 'none'; "
        b"form-action 'none'; base-uri 'none'"
    )
    if meta[0] != approved:
        raise ValueError("Offline CSP does not match fixed script and network policy")


def verify_zip(path):
    path = Path(path)
    assert_no_links(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_ARCHIVE:
        raise ValueError("Missing, linked, or oversized package")
    # One verified, bounded file-descriptor snapshot. Never validate one ZIP and
    # hash a separately re-opened version of the same untrusted path.
    raw=read_bounded_source(path,max_bytes=MAX_ARCHIVE)
    # The builder emits a plain ZIP, never a self-extracting/polyglot prefix,
    # trailing payload or archive comment. Do not endorse altered containers.
    if (len(raw) < 22 or not raw.startswith(b"PK\x03\x04")
            or raw[-22:-18] != b"PK\x05\x06" or raw[-2:] != b"\x00\x00"):
        raise ValueError("Non-canonical ZIP envelope")
    try:
        with ZipFile(BytesIO(raw), "r") as archive:
            info = archive.infolist()
            names = [x.filename for x in info]
            if archive.comment or not info or info[0].header_offset != 0:
                raise ValueError("ZIP prefix or comment forbidden")
            expected_offset = 0
            for member in info:
                if (member.header_offset != expected_offset or member.extra
                        or member.comment or member.flag_bits != 0):
                    raise ValueError("Non-canonical ZIP member metadata")
                expected_offset += 30 + len(member.filename.encode("ascii")) + member.compress_size
            if expected_offset != archive.start_dir:
                raise ValueError("Unexpected hidden ZIP payload")
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
            if (not isinstance(manifest, dict) or set(manifest) != PACKAGE_KEYS
                    or manifest.get("contract") != "DATA2WEB_PACKAGE_V1"
                    or manifest.get("status") != "RELEASE_HOLD"
                    or manifest.get("sale_approved") is not False
                    or manifest.get("plaintext_ack") is not True
                    or not _is_sha256(manifest.get("source_sha256"))):
                raise ValueError("Invalid or unauthorized package manifest")
            for key, content in (("html_sha256", html), ("guide_sha256", guide)):
                if manifest.get(key) != hashlib.sha256(content).hexdigest():
                    raise ValueError("Member integrity mismatch")
            if not html.startswith(b"<!doctype html>") or b"DATA2WEB" not in html:
                raise ValueError("Invalid standalone HTML")
            _validate_offline_html_csp(html)
            if type(manifest.get("rows")) is not int or manifest["rows"] < 0:
                raise ValueError("Invalid manifest row count")
            if manifest.get("sheet") is not None and not isinstance(manifest["sheet"], str):
                raise ValueError("Invalid sheet identity")
            if type(manifest.get("header_row")) is not int or not 1 <= manifest["header_row"] <= 50:
                raise ValueError("Invalid header row")
            if not isinstance(manifest.get("cached_formulas"), bool):
                raise ValueError("Invalid formula approval flag")
            import re
            match = re.search(rb'<script type="application/json" id="dataset">([^<]+)</script>', html)
            if not match:
                raise ValueError("Embedded source metadata missing")
            embedded = json.loads(match.group(1),object_pairs_hook=_object_no_duplicate_keys,parse_constant=_reject_nonfinite_constant)
            if not isinstance(embedded, dict) or not isinstance(embedded.get("rows"), list):
                raise ValueError("Embedded dataset must be a table object")
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
                                _is_sha256(x.get("sha256")) and
                                type(x.get("rows")) is int and x["rows"]>=0
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
