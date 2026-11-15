"""R29 strict verifier: canonical packages remain usable; rehash attacks HOLD.

Synthetic local files only. This is not a substitute for an external auditor
or authentication of the publisher/customer source.
"""
import base64
import contextlib
import hashlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZIP_STORED, ZipFile, ZipInfo

from data2web_single import deliver_single
from r29_strict_zip_verifier import main, verify_zip_r29_strict
from verify_delivery import verify_zip


class StrictR29ZipVerification(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix="data2web-r29-strict-")
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        source = self.root / "synthetic.csv"
        original = b"id,title,category\n1,Synthetic,A\n"
        source.write_bytes(original)
        output = self.root / "new-folder"
        deliver_single(
            source, output, expected_sha256=hashlib.sha256(original).hexdigest(),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )
        self.archive = output / "delivery.zip"
        with ZipFile(self.archive, "r") as zip_in:
            self.members = {n: zip_in.read(n) for n in zip_in.namelist()}

    def _modified(self, html):
        members = dict(self.members)
        members["index.html"] = html
        manifest = json.loads(members["manifest.json"])
        manifest["html_sha256"] = hashlib.sha256(html).hexdigest()
        members["manifest.json"] = (
            json.dumps(manifest, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + chr(10)
        ).encode("utf-8")
        target = self.root / ("altered-%d.zip" % len(list(self.root.glob("altered-*.zip"))))
        with ZipFile(target, "w", compression=ZIP_STORED, allowZip64=False) as out:
            for name in ("index.html", "manifest.json", "README_KO.txt"):
                entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = ZIP_STORED
                entry.external_attr = 0o100600 << 16
                out.writestr(entry, members[name])
        return target

    def _assert_guard_blocks_but_legacy_accepts(self, html):
        self.assertNotEqual(html, self.members["index.html"])
        target = self._modified(html)
        self.assertTrue(verify_zip(target)["verified"])
        with self.assertRaises(ValueError):
            verify_zip_r29_strict(target)

    def test_unmodified_synthetic_zip_strict_verifies_without_sale(self):
        original = self.archive.read_bytes()
        result = verify_zip_r29_strict(self.archive)
        self.assertTrue(result["verified"])
        self.assertTrue(result["strict_passive_html_verified"])
        self.assertFalse(result["source_authenticity_verified"])
        self.assertFalse(result["independent_security_audit_completed"])
        self.assertFalse(result["commercial_release_approved"])
        self.assertEqual(result["score_addition"], 0)
        self.assertEqual(result["production_status"], "RELEASE_HOLD_SALE_NO_GO")
        self.assertEqual(self.archive.read_bytes(), original)

    def test_rehashed_meta_refresh_is_rejected_though_legacy_accepts(self):
        html = self.members["index.html"].replace(
            b"</head>",
            b'<meta http-equiv="refresh" content="0;url=https://invalid.example/">'
            + b"</head>", 1,
        )
        self._assert_guard_blocks_but_legacy_accepts(html)

    def test_self_rehashed_executable_js_is_rejected(self):
        original = self.members["index.html"]
        match = re.search(rb"<script>(.*?)</script>", original, re.DOTALL)
        self.assertIsNotNone(match)
        old_script = match.group(1)
        evil_script = old_script + b"window.R29_SYNTHETIC=1;"
        html = original.replace(
            b"<script>" + old_script + b"</script>",
            b"<script>" + evil_script + b"</script>", 1,
        )
        old_hash = base64.b64encode(hashlib.sha256(old_script).digest())
        new_hash = base64.b64encode(hashlib.sha256(evil_script).digest())
        html = html.replace(old_hash, new_hash, 1)
        self._assert_guard_blocks_but_legacy_accepts(html)

    def test_rehashed_css_style_mutation_is_rejected(self):
        original = self.members["index.html"]
        self._assert_guard_blocks_but_legacy_accepts(original.replace(
            b"</style>", b"body{display:none}</style>", 1,
        ))

    def test_rehashed_shadow_dataset_div_is_rejected_by_strict_verifier(self):
        # Inject an early shadow for document.getElementById("dataset")
        # without modifying the actual approved JSON script contents.
        original = self.members["index.html"]
        data_match = re.search(
            rb'<script type="application/json" id="dataset">(.*?)</script>',
            original, re.DOTALL,
        )
        self.assertIsNotNone(data_match)
        forged = json.loads(data_match.group(1))
        forged["rows"][0]["title"] = "SYNTHETIC_UNVERIFIED_DISPLAY"
        injected = (b'<div id="dataset">'
                    + json.dumps(forged, ensure_ascii=True,
                                 separators=(",", ":")).encode("utf-8")
                    + b"</div>")
        modified = original.replace(
            b"</main>", injected + b"</main>", 1
        )
        # Old package checks can still read the original dataset script
        # and accept the rehashed modified HTML container. The browser
        # would select the earlier injected identity, not the signed data.
        self._assert_guard_blocks_but_legacy_accepts(modified)

    def test_source_bytes_changed_during_strict_verification_hold(self):
        snapshot = self.archive.read_bytes()
        with patch("r29_strict_zip_verifier.read_bounded_source",
                   side_effect=(snapshot, snapshot + b"changed")):
            with self.assertRaisesRegex(ValueError, "changed during"):
                verify_zip_r29_strict(self.archive)

    def test_cli_failure_is_redacted_and_has_nonzero_exit(self):
        missing = self.root / "private-customer-path.zip"
        output = io.StringIO()
        with patch("sys.argv", ["r29_strict_zip_verifier.py", str(missing)]):
            with contextlib.redirect_stdout(output):
                code = main()
        self.assertEqual(code, 1)
        result = json.loads(output.getvalue())
        self.assertFalse(result["verified"])
        self.assertFalse(result["commercial_release_approved"])
        self.assertNotIn(str(missing), output.getvalue())


if __name__ == "__main__":
    unittest.main()
