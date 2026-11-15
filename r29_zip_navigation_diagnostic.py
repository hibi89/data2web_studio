"""Synthetic-only diagnostic: does rehashed active markup pass the ZIP verifier?

This is an evidence generator, not an audit pass/fail test or browser exploit.
No external URL is fetched. The result must always retain RELEASE HOLD.
CODEX owns the verifier implementation and its security corrections.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

from data2web_single import deliver_single
from verify_delivery import verify_zip

CONTRACT = "DATA2WEB_R29_REHASHED_NAVIGATION_DIAGNOSTIC_V1"


def assess_rehashed_navigation():
    with tempfile.TemporaryDirectory(prefix="r29-rehash-navigation-") as temp:
        root = Path(temp)
        source = root / "synthetic.csv"
        source_bytes = (
            "id,title,category" + chr(10)
            + "A1,Only Synthetic,Test" + chr(10)
        ).encode("utf-8")
        source.write_bytes(source_bytes)
        output = root / "new-delivery"
        deliver_single(
            source, output, expected_sha256=hashlib.sha256(source_bytes).hexdigest(),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )
        original_zip = output / "delivery.zip"
        if verify_zip(original_zip).get("verified") is not True:
            raise AssertionError("Valid synthetic control did not verify")
        with ZipFile(original_zip, "r") as z:
            members = {name: z.read(name) for name in z.namelist()}
        marker = b"</head>"
        original_html = members["index.html"]
        if original_html.count(marker) != 1:
            raise AssertionError("Unexpected generated HTML head structure")
        navigation = (
            b'<meta http-equiv="refresh" '
            b'content="0;url=https://invalid.example/synthetic-only">'
        )
        modified_html = original_html.replace(marker, navigation + marker, 1)
        if modified_html == original_html:
            raise AssertionError("Synthetic navigation mutation not applied")
        members["index.html"] = modified_html
        manifest = json.loads(members["manifest.json"])
        manifest["html_sha256"] = hashlib.sha256(modified_html).hexdigest()
        members["manifest.json"] = (
            json.dumps(manifest, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + chr(10)
        ).encode("utf-8")
        altered = root / "synthetic-rehashed-navigation.zip"
        with ZipFile(altered, "w", compression=ZIP_STORED, allowZip64=False) as z:
            for name in ("index.html", "manifest.json", "README_KO.txt"):
                item = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                item.compress_type = ZIP_STORED
                item.external_attr = 0o100600 << 16
                z.writestr(item, members[name])
        with ZipFile(altered) as z:
            names = z.namelist()
        if names != ["index.html", "manifest.json", "README_KO.txt"]:
            raise AssertionError("Adversarial package is not three-member canonical")
        try:
            verified = verify_zip(altered)
        except ValueError:
            accepted = False
        else:
            accepted = verified.get("verified") is True
        return {
            "contract": CONTRACT,
            "status": ("SECURITY_HOLD_CANDIDATE_CONFIRMED" if accepted
                       else "MODIFIED_NAVIGATION_REJECTED_BY_VERIFIER"),
            "verifier_accepted_rehashed_navigation": accepted,
            "synthetic_control_verified": True,
            "zip_member_count": len(names),
            "external_network_request_performed": False,
            "actual_browser_navigation_tested": False,
            "independent_security_audit_completed": False,
            "commercial_release_approved": False,
            "score_addition": 0,
        }


if __name__ == "__main__":
    print(json.dumps(assess_rehashed_navigation(), sort_keys=True))
