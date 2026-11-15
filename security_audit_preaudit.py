"""Create a redacted, offline, create-only R29 *internal* pre-audit report.

The report is an evidence handoff to a future *independent* auditor, never a
security certification or permission to redistribute the repository. All data
probed is synthetic and ephemeral. No customer input path is accepted.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import re
from pathlib import Path
from html.parser import HTMLParser
import tempfile
from zipfile import ZipFile, ZipInfo, ZIP_STORED, ZIP_DEFLATED

from data2web_single import deliver_single
from data2web_tabular import list_xlsx_sheets
from path_policy import assert_no_links
from secure_output import create_output_file
from verify_customer_folder import verify_customer_folder
from verify_delivery import verify_zip

CONTRACT = "DATA2WEB_R29_INTERNAL_PREAUDIT_V1"
SCOPE = ("XSS_SCRIPT_END_TAG", "CSV_FORMULA_TEXT", "ORIGINAL_BYTES_PRESERVED",
         "ZIP_STATUS_FORGERY_BLOCKED", "CUSTOMER_FOLDER_TAMPER_BLOCKED",
         "EXISTING_DESTINATION_NOT_OVERWRITTEN", "OFFLINE_LOCAL_DELIVERY",
         "STATIC_SCRIPT_HASH_MATCHED", "NETWORK_MARKUP_ABSENT",
         "ZIP_SLIP_BLOCKED", "ZIP_SYMLINK_BLOCKED",
         "XLSX_EXTERNAL_REL_BLOCKED", "XLSX_ZIP_BOMB_BLOCKED",
         "XLSX_MACRO_MEMBER_BLOCKED")


class _OutputMarkupAudit(HTMLParser):
    """Collect parsed output elements while treating JSON script data as text."""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.elements = []
        self.dataset_parts = []
        self.in_dataset = False

    def handle_starttag(self, tag, attrs):
        normalized = {str(key).lower(): value for key, value in attrs}
        self.elements.append((tag.lower(), normalized))
        self.in_dataset = tag.lower() == "script" and normalized.get("id") == "dataset"

    def handle_endtag(self, tag):
        if tag.lower() == "script":
            self.in_dataset = False

    def handle_data(self, data):
        if self.in_dataset:
            self.dataset_parts.append(data)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _tamper_zip(archive, target):
    with ZipFile(archive, "r") as old:
        members = {name: old.read(name) for name in old.namelist()}
    manifest = json.loads(members["manifest.json"])
    manifest["status"] = "APPROVED_FOR_SALE"
    members["manifest.json"] = json.dumps(manifest, sort_keys=True).encode("utf-8")
    with ZipFile(target, "w", compression=ZIP_STORED) as new:
        for name, data in members.items():
            new.writestr(name, data)


def _adversarial_zip(legitimate, target, *, extra_name=None, symlink=False):
    """Create an intentionally invalid synthetic ZIP, never extract it."""
    with ZipFile(legitimate, "r") as original:
        entries = {name: original.read(name) for name in original.namelist()}
    with ZipFile(target, "w", compression=ZIP_STORED, allowZip64=False) as z:
        for name, data in entries.items():
            item = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            item.compress_type = ZIP_STORED
            item.external_attr = (0o120777 if symlink and name == "index.html"
                                  else 0o100600) << 16
            z.writestr(item, data)
        if extra_name is not None:
            z.writestr(extra_name, b"synthetic-no-extraction")


def _adversarial_xlsx(*, external=False, compress_bomb=False, macro=False):
    """Bounded in-memory OOXML negatives, without filesystem extraction."""
    rel = (b'<Relationships xmlns="http://schemas.openxmlformats.org/'
           b'package/2006/relationships"><Relationship Id="rId1" '
           b'Type="http://schemas.openxmlformats.org/officeDocument/'
           b'2006/relationships/worksheet" '
           + (b'TargetMode="External" Target="https://invalid.example/private"'
              if external else b'Target="worksheets/sheet1.xml"')
           + b'/></Relationships>')
    workbook = (b'<workbook xmlns="http://schemas.openxmlformats.org/'
                b'spreadsheetml/2006/main"><sheets/></workbook>')
    if compress_bomb:
        workbook = b"A" * 200_000  # High compression ratio, tiny ZIP input.
    parts = {
        "[Content_Types].xml": b"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml",
        "xl/_rels/workbook.xml.rels": rel,
        "xl/workbook.xml": workbook,
    }
    if macro:
        parts["xl/vbaProject.bin"] = b"not-real-macro"
    stream = io.BytesIO()
    with ZipFile(stream, "w", compression=ZIP_DEFLATED, allowZip64=False) as z:
        for name, contents in parts.items():
            z.writestr(name, contents)
    return stream.getvalue()


def _rejected_xlsx(raw):
    try:
        list_xlsx_sheets(raw)
    except ValueError:
        return True
    return False


def _rejected_zip(path):
    try:
        verify_zip(path)
    except ValueError:
        return True
    return False


def internal_synthetic_probes():
    checks = {name: False for name in SCOPE}
    with tempfile.TemporaryDirectory(prefix="data2web-r29-synthetic-") as scratch:
        root = Path(scratch)
        source = root / "generated-synthetic.csv"
        buf = io.StringIO(newline="")
        writer = csv.writer(buf)
        writer.writerow(("id", "title", "category"))
        writer.writerow(("S1", "</script><script>window.XSS_PROBE=1</script>", "B"))
        formula_probe = '=HYPERLINK("https://invalid.example","probe")'
        writer.writerow(("S2", formula_probe, "A"))
        before = buf.getvalue().encode("utf-8")
        source.write_bytes(before)
        dest = root / "new-customer-folder"
        delivered = deliver_single(
            source, dest, expected_sha256=_sha(before),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )
        if not delivered["rows"] == 2:
            raise AssertionError("Synthetic data row count mismatch")
        verified = verify_customer_folder(dest)
        if verified["verified"] is not True or verified["sale_approved"] is not False:
            raise AssertionError("Synthetic delivery did not independently verify")
        html = (dest / "index.html").read_bytes()
        checks["XSS_SCRIPT_END_TAG"] = (
            b"window.XSS_PROBE=1" in html
            and b"</script><script>window.XSS_PROBE=1" not in html
            and b"\\u003c/script\\u003e" in html
        )
        markup = _OutputMarkupAudit()
        markup.feed(html.decode("utf-8"))
        markup.close()
        try:
            embedded_rows = (
                json.loads("".join(markup.dataset_parts))["rows"]
                if len(markup.dataset_parts) == 1 else []
            )
        except (KeyError, TypeError, ValueError):
            embedded_rows = []
        active_tags = {"a", "iframe", "object", "embed", "form"}
        uri_attributes = {"href", "src", "action", "formaction", "xlink:href"}
        scripts = re.findall(rb"<script>(.*?)</script>", html, flags=re.DOTALL)
        script_digest = (base64.b64encode(hashlib.sha256(scripts[0]).digest())
                         if len(scripts) == 1 else b"")
        checks["STATIC_SCRIPT_HASH_MATCHED"] = (
            len(scripts) == 1
            and len([tag for tag, _ in markup.elements if tag == "script"]) == 2
            and b"script-src 'sha256-" + script_digest + b"'" in html
            and len(re.findall(rb"Content-Security-Policy", html, re.I)) == 1
        )
        blocked_tags = {"a", "iframe", "object", "embed", "form", "img",
                        "video", "audio", "link", "base"}
        uri_attributes = {"href", "src", "action", "formaction", "xlink:href"}
        checks["NETWORK_MARKUP_ABSENT"] = (
            not any(tag in blocked_tags for tag, _ in markup.elements)
            and not any(tag == "meta" and
                        (attrs.get("http-equiv") or "").lower() == "refresh"
                        for tag, attrs in markup.elements)
            and not any(name.startswith("on") or name in uri_attributes
                        for _, attrs in markup.elements for name in attrs)
        )
        checks["CSV_FORMULA_TEXT"] = (
            len(embedded_rows) > 1
            and isinstance(embedded_rows[1], dict)
            and embedded_rows[1].get("title") == formula_probe
            and not any(tag in active_tags for tag, _ in markup.elements)
            and not any(
                name.lower().startswith("on") or name.lower() in uri_attributes
                for _, attrs in markup.elements for name in attrs
            )
        )
        checks["ORIGINAL_BYTES_PRESERVED"] = source.read_bytes() == before
        checks["OFFLINE_LOCAL_DELIVERY"] = (
            verified["status"] ==
            "LOCAL_INTEGRITY_VERIFIED_RELEASE_HOLD_NOT_SALE_APPROVED"
            and b"connect-src 'none'" in html
        )
        try:
            deliver_single(
                source, dest, expected_sha256=_sha(before),
                id_column="id", title_column="title", category_column="category",
                confirm="APPROVE", ack_plaintext=True,
                privacy_classification="NO_PERSONAL_DATA_REVIEWED",
            )
        except FileExistsError:
            checks["EXISTING_DESTINATION_NOT_OVERWRITTEN"] = (
                verify_customer_folder(dest)["verified"] is True
            )
        altered = root / "synthetic-unauthorized.zip"
        _tamper_zip(dest / "delivery.zip", altered)
        checks["ZIP_STATUS_FORGERY_BLOCKED"] = _rejected_zip(altered)

        traversal = root / "synthetic-zip-slip.zip"
        _adversarial_zip(dest / "delivery.zip", traversal,
                         extra_name="../outside.txt")
        checks["ZIP_SLIP_BLOCKED"] = _rejected_zip(traversal)

        link = root / "synthetic-zip-link.zip"
        _adversarial_zip(dest / "delivery.zip", link, symlink=True)
        checks["ZIP_SYMLINK_BLOCKED"] = _rejected_zip(link)

        checks["XLSX_EXTERNAL_REL_BLOCKED"] = _rejected_xlsx(
            _adversarial_xlsx(external=True))
        checks["XLSX_ZIP_BOMB_BLOCKED"] = _rejected_xlsx(
            _adversarial_xlsx(compress_bomb=True))
        checks["XLSX_MACRO_MEMBER_BLOCKED"] = _rejected_xlsx(
            _adversarial_xlsx(macro=True))
        altered_html = dest / "index.html"
        with altered_html.open("ab") as f:
            f.write(b"<!-- tampered synthetic only -->")
        try:
            verify_customer_folder(dest)
        except ValueError:
            checks["CUSTOMER_FOLDER_TAMPER_BLOCKED"] = True
    return checks


def report():
    checks = internal_synthetic_probes()
    if not all(checks.values()):
        raise AssertionError("Internal synthetic threat probes not all passing")
    # Only bounded enumerated check names/results, no source rows, device paths,
    # machine ID, environment variables, tokens, logs or external audit claims.
    return {
        "contract": CONTRACT,
        "status": "INTERNAL_SYNTHETIC_ONLY_EXTERNAL_AUDIT_PENDING",
        "scope": "A_OFFLINE_HTML_ZIP_RECEIPT",
        "checks": checks,
        "check_count": len(checks),
        "internal_synthetic_checks_passed": True,
        "independent_security_audit_completed": False,
        "customer_source_inspected": False,
        "owner_rights_attested": False,
        "commercial_release_approved": False,
        "external_transfer_performed": False,
        "production_status": "RELEASE_HOLD_SALE_NO_GO",
        "score_addition": 0,
        "auditor_requirements": {
            "independent_party": True,
            "replay_exact_source_sha": True,
            "real_os_toctou_required": True,
            "privacy_and_license_are_separate_owner_gates": True,
            "remediation_recheck_required_if_findings": True,
        },
    }


def write_report(target):
    """No upload, no overwrite, no user data. Target path explicitly supplied."""
    result = report()
    path = assert_no_links(target, allow_missing_leaf=True)
    if path.exists() or path.is_symlink() or not path.parent.is_dir():
        raise FileExistsError("New report path within an existing safe directory required")
    blob = (json.dumps(result, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")
    with create_output_file(path) as out:
        out.write(blob)
    return {"status": result["status"], "report_sha256": _sha(blob),
            "independent_security_audit_completed": False, "score_addition": 0}


def main():
    parser = argparse.ArgumentParser(description="R29 synthetic-only self-audit")
    parser.add_argument("--output", help="Create-only local JSON report; no upload")
    args = parser.parse_args()
    result = write_report(args.output) if args.output else report()
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
