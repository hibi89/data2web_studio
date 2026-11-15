"""R29 probe specificity: valid synthetic controls and targeted failure causes.

These tests must not pass merely because the attack sample itself was malformed
before the intended security boundary. All bytes are generated in temporary folders.
"""
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

import security_audit_preaudit as audit
from data2web_single import deliver_single
from data2web_tabular import list_xlsx_sheets
from verify_delivery import verify_zip


class R29ProbeSpecificity(unittest.TestCase):
    def test_control_xlsx_is_real_accepted_ooxml(self):
        control = audit._adversarial_xlsx()
        self.assertEqual(list_xlsx_sheets(control), [
            {"name": "Inventory", "state": "visible"}
        ])

    def test_xlsx_rejection_cause_is_attack_specific(self):
        cases = (
            ({"external": True}, "External workbook relationship rejected"),
            ({"compress_bomb": True}, "XLSX decompression safety limit"),
            ({"macro": True}, "Unsupported or unsafe XLSX ZIP member"),
        )
        for opts, cause in cases:
            with self.subTest(cause=cause):
                mutated = audit._adversarial_xlsx(**opts)
                with self.assertRaisesRegex(ValueError, cause):
                    list_xlsx_sheets(mutated)
                self.assertTrue(audit._rejected_xlsx(mutated, cause))
        bomb = audit._adversarial_xlsx(compress_bomb=True)
        with ZipFile(io.BytesIO(bomb)) as archive:
            worksheet = archive.getinfo("xl/worksheets/sheet1.xml")
            self.assertGreater(
                worksheet.file_size / max(1, worksheet.compress_size), 180
            )

    def test_zip_attack_changes_one_canonical_member(self):
        with tempfile.TemporaryDirectory(prefix="r29-specificity-") as temp:
            root = Path(temp)
            source = root / "synthetic.csv"
            data = ("id,title,category" + chr(10)
                    + "1,Synthetic,A" + chr(10)).encode("utf-8")
            source.write_bytes(data)
            destination = root / "delivery"
            deliver_single(
                source, destination, expected_sha256=hashlib.sha256(data).hexdigest(),
                id_column="id", title_column="title", category_column="category",
                confirm="APPROVE", ack_plaintext=True,
                privacy_classification="NO_PERSONAL_DATA_REVIEWED"
            )
            original = destination / "delivery.zip"
            self.assertTrue(verify_zip(original)["verified"])
            cases = (
                ("forged-status.zip", lambda dst: audit._tamper_zip(original, dst),
                 "Invalid or unauthorized package manifest"),
                ("traversal.zip", lambda dst: audit._adversarial_zip(
                    original, dst, extra_name="../outside.txt"),
                 "Unexpected, duplicated, or unsafe ZIP members"),
                ("symlink.zip", lambda dst: audit._adversarial_zip(
                    original, dst, symlink=True), "Linked ZIP entry"),
            )
            for name, mutate, cause in cases:
                with self.subTest(name=name):
                    altered = root / name
                    mutate(altered)
                    with ZipFile(altered) as archive:
                        self.assertEqual(len(archive.infolist()), 3)
                        self.assertFalse(archive.comment)
                        self.assertEqual(archive.infolist()[0].header_offset, 0)
                    with self.assertRaisesRegex(ValueError, cause):
                        verify_zip(altered)
                    self.assertTrue(audit._rejected_zip(altered, cause))
            self.assertFalse((root / "outside.txt").exists())
            self.assertTrue(verify_zip(original)["verified"])

    def test_unrelated_verifier_error_is_not_a_security_probe_pass(self):
        with patch.object(audit, "list_xlsx_sheets",
                          side_effect=ValueError("wrong boundary")):
            self.assertFalse(audit._rejected_xlsx(
                b"some bytes", "External workbook relationship rejected"
            ))
        with patch.object(audit, "verify_zip",
                          side_effect=ValueError("wrong boundary")):
            self.assertFalse(audit._rejected_zip(
                Path("not-read.zip"), "Linked ZIP entry"
            ))


if __name__ == "__main__":
    unittest.main()
