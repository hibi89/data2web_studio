"""Synthetic regression: customer folder inventory races and unsafe paths.

No customer content, network, automatic cleanup, or existing-output overwrite.
"""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import verify_customer_folder as verifier
from data2web_single import deliver_single


class CustomerFolderRootRace(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.input = self.base / "source.csv"
        self.input.write_text(
            "id,title,category\nA,Example,Group\n", encoding="utf-8"
        )
        self.raw = self.input.read_bytes()
        self.folder = self.base / "delivery"
        self.args = dict(
            expected_sha256=hashlib.sha256(self.raw).hexdigest(),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )
        self._delivered = False

    def make(self):
        if not self._delivered:
            deliver_single(self.input, self.folder, **self.args)
            self._delivered = True

    def test_unexpected_member_inserted_after_inventory_is_hold(self):
        self.make()
        real = verifier.verify_zip
        def insert_after_listing(path):
            (self.folder / "unexpected-after-inventory.txt").write_bytes(b"EXTRA")
            return real(path)
        with patch.object(verifier, "verify_zip", side_effect=insert_after_listing):
            with self.assertRaisesRegex(ValueError, "Customer folder changed"):
                verifier.verify_customer_folder(self.folder)
        self.assertEqual(self.input.read_bytes(), self.raw)
        self.assertTrue((self.folder / "unexpected-after-inventory.txt").is_file())
        self.assertFalse(verifier.diagnose_customer_folder(self.folder)["verified"])
        self.assertFalse((self.folder / "unexpected-after-inventory.txt").stat().st_size == 0)

    def test_directory_replaced_with_identical_contents_during_verify_is_hold(self):
        self.make()
        real = verifier.verify_zip
        archived = self.base / "archived_original"
        def replace_folder_after_listing(path):
            self.folder.rename(archived)
            shutil.copytree(archived, self.folder)
            return real(path)
        with patch.object(verifier, "verify_zip", side_effect=replace_folder_after_listing):
            with self.assertRaisesRegex(ValueError, "Customer folder changed"):
                verifier.verify_customer_folder(self.folder)
        self.assertTrue(archived.is_dir())
        self.assertTrue(self.folder.is_dir())
        for name in ("index.html", "delivery.zip", "receipt.json"):
            self.assertEqual((archived / name).read_bytes(), (self.folder / name).read_bytes())
        self.assertEqual(self.input.read_bytes(), self.raw)
        with self.assertRaises((FileExistsError, ValueError)):
            deliver_single(self.input, self.folder, **self.args)

    def test_symlink_to_healthy_folder_never_returns_verified(self):
        self.make()
        link = self.base / "linked_delivery"
        try:
            link.symlink_to(self.folder, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Directory symlink privilege unavailable on host")
        with self.assertRaises(ValueError):
            verifier.verify_customer_folder(link)
        report = verifier.diagnose_customer_folder(link)
        self.assertFalse(report["verified"])
        self.assertEqual(report["status"], "HOLD")
        self.assertFalse(report["sale_approved"])
        self.assertEqual(self.input.read_bytes(), self.raw)

    def test_permission_error_is_redacted_hold_and_no_writes(self):
        self.make()
        before = {p.name: p.read_bytes() for p in self.folder.iterdir()}
        with patch.object(Path, "iterdir", side_effect=PermissionError(
            "private/customer/SECRET_PERMISSION_DENIED"
        )):
            report = verifier.diagnose_customer_folder(self.folder)
        self.assertEqual(report["reason_code"], "INTEGRITY_CHECK_FAILED")
        self.assertFalse(report["verified"])
        self.assertNotIn("SECRET", json.dumps(report))
        self.assertEqual({p.name: p.read_bytes() for p in self.folder.iterdir()}, before)

    def test_normal_complete_folder_still_verifies(self):
        self.make()
        result = verifier.verify_customer_folder(self.folder)
        self.assertTrue(result["verified"])
        self.assertFalse(result["sale_approved"])
        report = verifier.diagnose_customer_folder(self.folder)
        self.assertTrue(report["verified"])
        self.assertEqual(report["reason_code"], "FULL_INTEGRITY_VERIFIED_NOT_SALE_APPROVED")


if __name__ == "__main__":
    unittest.main()
