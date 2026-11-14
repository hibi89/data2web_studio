"""Create a redacted, offline, create-only R29 *internal* pre-audit report.

The report is an evidence handoff to a future *independent* auditor, never a
security certification or permission to redistribute the repository. All data
probed is synthetic and ephemeral. No customer input path is accepted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from html.parser import HTMLParser
import tempfile
from zipfile import ZipFile, ZIP_STORED

from data2web_single import deliver_single
from path_policy import assert_no_links
from secure_output import create_output_file
from verify_customer_folder import verify_customer_folder
from verify_delivery import verify_zip

CONTRACT = "DATA2WEB_R29_INTERNAL_PREAUDIT_V1"
SCOPE = ("XSS_SCRIPT_END_TAG", "CSV_FORMULA_TEXT", "ORIGINAL_BYTES_PRESERVED",
         "ZIP_STATUS_FORGERY_BLOCKED", "CUSTOMER_FOLDER_TAMPER_BLOCKED",
         "EXISTING_DESTINATION_NOT_OVERWRITTEN", "OFFLINE_LOCAL_DELIVERY")


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
        try:
            verify_zip(altered)
        except ValueError:
            checks["ZIP_STATUS_FORGERY_BLOCKED"] = True
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
