"""Late in-place member writes must never pass the whole-folder success gate.

All mutations are synthetic fault injections after the earlier bounded reads;
no customer files, remote requests, or automatic repairs.
"""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import verify_customer_folder as verifier
from data2web_single import deliver_single


class LateMemberMutation(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.source=self.root/"source.csv"
        self.source.write_text(
            "id,title,category\nA,Sample Item,Group\n", encoding="utf-8"
        )
        self.original=self.source.read_bytes()
        self.folder=self.root/"delivery"
        deliver_single(
            self.source,self.folder,
            expected_sha256=hashlib.sha256(self.original).hexdigest(),
            id_column="id",title_column="title",category_column="category",
            confirm="APPROVE",ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )

    def test_html_changed_in_place_after_initial_read_is_hold(self):
        real=verifier.verify_zip

        def edit_html(path):
            evidence=real(path)
            target=self.folder/"index.html"
            before=target.read_bytes()
            after=before.replace(b"<!doctype html>",b"<!doctype htmm>",1)
            self.assertEqual(len(after),len(before))
            self.assertNotEqual(after,before)
            target.write_bytes(after)
            return evidence

        with patch.object(verifier,"verify_zip",side_effect=edit_html):
            with self.assertRaisesRegex(ValueError,"Customer artifact changed"):
                verifier.verify_customer_folder(self.folder)
        self.assertEqual(self.source.read_bytes(),self.original)
        self.assertFalse(verifier.diagnose_customer_folder(self.folder)["verified"])

    def test_receipt_changed_in_place_after_initial_read_is_hold(self):
        real=verifier.verify_zip

        def edit_receipt(path):
            evidence=real(path)
            target=self.folder/"receipt.json"
            before=target.read_bytes()
            after=before.replace(
                b"INTEGRITY_RECEIPT_ONLY_NOT_CUSTOMER_OR_SALE_APPROVAL",
                b"INTEGRITY_RECEIPT_ONLY_NOT_CUSTOMER_OR_SALE_APPROVAQ",1
            )
            self.assertEqual(len(after),len(before))
            self.assertNotEqual(after,before)
            target.write_bytes(after)
            return evidence

        with patch.object(verifier,"verify_zip",side_effect=edit_receipt):
            with self.assertRaisesRegex(ValueError,"Customer artifact changed"):
                verifier.verify_customer_folder(self.folder)
        self.assertEqual(self.source.read_bytes(),self.original)
        self.assertFalse(verifier.diagnose_customer_folder(self.folder)["verified"])

    def test_zip_changed_after_snapshot_parse_is_hold(self):
        original=verifier._load_json
        modified=[False]

        def edit_zip_at_manifest_parse(data,**kwargs):
            document=original(data,**kwargs)
            if document.get("contract")=="DATA2WEB_PACKAGE_V1" and not modified[0]:
                target=self.folder/"delivery.zip"
                with target.open("r+b") as stream:
                    stream.seek(-1,2)
                    stream.write(b"\x01")
                modified[0]=True
            return document

        with patch.object(verifier,"_load_json",side_effect=edit_zip_at_manifest_parse):
            with self.assertRaisesRegex(ValueError,"Customer artifact changed"):
                verifier.verify_customer_folder(self.folder)
        self.assertTrue(modified[0])
        self.assertEqual(self.source.read_bytes(),self.original)
        self.assertFalse(verifier.diagnose_customer_folder(self.folder)["verified"])

    def test_healthy_folder_still_independently_verified(self):
        result=verifier.verify_customer_folder(self.folder)
        self.assertTrue(result["verified"])
        self.assertFalse(result["sale_approved"])
        self.assertEqual(result["rows"],1)
        self.assertTrue(verifier.diagnose_customer_folder(self.folder)["verified"])

    def test_late_bounded_read_permission_denial_becomes_redacted_hold(self):
        original=verifier.read_bounded_source
        seen=[0]

        def deny_second_html_read(path,*,max_bytes):
            if Path(path).name=="index.html":
                seen[0]+=1
                if seen[0]==2:
                    raise PermissionError("SECRET_PRIVATE_SOURCE_PATH")
            return original(path,max_bytes=max_bytes)

        with patch.object(verifier,"read_bounded_source",side_effect=deny_second_html_read):
            result=verifier.diagnose_customer_folder(self.folder)
        self.assertGreaterEqual(seen[0],2)
        self.assertEqual(result["status"],"HOLD")
        self.assertEqual(result["reason_code"],"INTEGRITY_CHECK_FAILED")
        self.assertNotIn("SECRET",str(result))
        self.assertEqual(self.source.read_bytes(),self.original)


if __name__=="__main__":
    unittest.main()
