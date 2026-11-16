"""Same-byte artifact replacement fault injection for local delivery verifier.

Only synthetic customer folders; no remote data, permissions, or cleanup.
The directory metadata gate is frozen in race simulations to isolate the
member identity gate and model filesystems that miss parent metadata changes.
"""
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import verify_customer_folder as verifier
from data2web_single import deliver_single


class IdenticalByteMemberReplacement(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.source=self.root/"synthetic.csv"
        self.source.write_text("id,title,category\nS1,Sample,Group\n",encoding="utf-8")
        self.source_bytes=self.source.read_bytes()
        self.folder=self.root/"customer"
        deliver_single(
            self.source,self.folder,
            expected_sha256=hashlib.sha256(self.source_bytes).hexdigest(),
            id_column="id",title_column="title",category_column="category",
            confirm="APPROVE",ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )
        self.archived=[]

    def replace_identical(self,name):
        target=self.folder/name
        before=target.read_bytes()
        before_identity=verifier._member_identity(target)
        state=target.stat()
        old=self.root/("archived_"+name)
        target.rename(old)
        target.write_bytes(before)
        os.utime(target,ns=(state.st_atime_ns,state.st_mtime_ns))
        self.archived.append(old)
        self.assertEqual(target.read_bytes(),before)
        # Some unusual filesystems return a constant inode; skip only there.
        if verifier._member_identity(target)==before_identity:
            self.skipTest("Filesystem provides no distinct replacement identity")
        return old

    def check_replacement(self,name):
        actual_zip=verifier.verify_zip
        anchored=verifier._folder_identity(self.folder)
        fired=[False]

        def inject_zip_check(path):
            result=actual_zip(path)
            self.replace_identical(name)
            fired[0]=True
            return result

        # Freeze root checkpoint *only* in this fault injection. Even if the
        # root metadata does not report a mutation, the member must HOLD.
        with patch.object(verifier,"_folder_identity",return_value=anchored):
            with patch.object(verifier,"verify_zip",side_effect=inject_zip_check):
                with self.assertRaisesRegex(
                    ValueError,"Customer artifact identity changed"
                ):
                    verifier.verify_customer_folder(self.folder)
        self.assertTrue(fired[0])
        self.assertEqual(self.source.read_bytes(),self.source_bytes)
        self.assertTrue(self.archived[-1].is_file())
        self.assertFalse(verifier.diagnose_customer_folder(self.folder)["sale_approved"])

    def test_identical_html_replacement_is_hold(self):
        self.check_replacement("index.html")

    def test_identical_receipt_replacement_is_hold(self):
        self.check_replacement("receipt.json")

    def test_identical_zip_replacement_is_hold(self):
        self.check_replacement("delivery.zip")

    def test_normal_existing_delivery_still_verifies(self):
        result=verifier.verify_customer_folder(self.folder)
        self.assertTrue(result["verified"])
        self.assertFalse(result["sale_approved"])
        self.assertTrue(verifier.diagnose_customer_folder(self.folder)["verified"])


if __name__=="__main__":
    unittest.main()
