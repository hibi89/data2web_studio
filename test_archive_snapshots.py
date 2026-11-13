"""R06/R22/R29: single-snapshot ZIP/receipt and bounded approval race tests.

All samples are generated in disposable directories; never use customer data.
"""
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile, ZIP_STORED

import verify_delivery as verifier
import verify_customer_folder as folder_verifier
from data2web_append import read_approval_manifest
from data2web_single import deliver_single


class ArchiveSnapshotSafety(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.src=self.base/"approved.csv"
        self.src.write_text("id,title,category\n1,One,A\n2,Two,B\n",encoding="utf-8")
        self.out=self.base/"customer"
        deliver_single(self.src,self.out,
            expected_sha256=hashlib.sha256(self.src.read_bytes()).hexdigest(),
            id_column="id",title_column="title",category_column="category",
            confirm="APPROVE",ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED")
        self.archive=self.out/"delivery.zip"

    def _forge(self, update):
        target=self.base/("forged-"+str(len(list(self.base.glob("forged-*"))))+".zip")
        with ZipFile(self.archive,"r") as source:
            data={name:source.read(name) for name in source.namelist()}
        update(data)
        with ZipFile(target,"w",compression=ZIP_STORED) as out:
            for name,content in data.items():
                out.writestr(name,content)
        return target

    def test_verify_zip_hashes_once_from_same_snapshot(self):
        expected=self.archive.read_bytes()
        with patch.object(verifier,"read_bounded_source",return_value=expected) as read:
            receipt=verifier.verify_zip(self.archive)
        read.assert_called_once()
        self.assertEqual(receipt["zip_sha256"],hashlib.sha256(expected).hexdigest())

    def test_archive_manifest_duplicate_key_with_valid_crc_is_rejected(self):
        def mutation(data):
            old=data["manifest.json"]
            self.assertIn(b'"rows":2',old)
            data["manifest.json"]=old.replace(b'"rows":2',b'"rows":2,"rows":2',1)
        tampered=self._forge(mutation)
        with self.assertRaisesRegex(ValueError,"Duplicate ZIP manifest"):
            verifier.verify_zip(tampered)

    def test_archive_manifest_nonfinite_with_valid_crc_is_rejected(self):
        def mutation(data):
            data["manifest.json"]=data["manifest.json"].replace(
                b'"rows":2',b'"rows":NaN',1)
        tampered=self._forge(mutation)
        with self.assertRaisesRegex(ValueError,"Nonfinite JSON"):
            verifier.verify_zip(tampered)

    def test_embedded_dataset_duplicate_json_key_even_if_manifest_rehashed(self):
        def mutation(data):
            html=data["index.html"].replace(
                b'"contract":"DATA2WEB_HTML_V1"',
                b'"contract":"DATA2WEB_HTML_V1","contract":"DATA2WEB_HTML_V1"',1)
            self.assertNotEqual(html,data["index.html"])
            data["index.html"]=html
            manifest=json.loads(data["manifest.json"])
            manifest["html_sha256"]=hashlib.sha256(html).hexdigest()
            data["manifest.json"]=json.dumps(manifest,ensure_ascii=False,
                   sort_keys=True,separators=(",",":")).encode("utf-8")
        tampered=self._forge(mutation)
        with self.assertRaisesRegex(ValueError,"Duplicate ZIP manifest"):
            verifier.verify_zip(tampered)

    def test_independent_full_folder_refuses_second_zip_identity(self):
        other=self.base/"other.zip"
        other.write_bytes(self.archive.read_bytes()+b"forged")
        original=folder_verifier.read_bounded_source
        def changed(path,*,max_bytes):
            if Path(path).name=="delivery.zip":
                return other.read_bytes()
            return original(path,max_bytes=max_bytes)
        with patch.object(folder_verifier,"read_bounded_source",side_effect=changed):
            with self.assertRaisesRegex(ValueError,"ZIP changed between independent checks"):
                folder_verifier.verify_customer_folder(self.out)
        # The verifier did not modify the actual owned package.
        self.assertTrue(verifier.verify_zip(self.archive)["verified"])

    def test_customer_receipt_extra_unknown_member_refused(self):
        with open(self.out/"unexpected.txt","w",encoding="utf-8") as f:
            f.write("not a customer artifact")
        with self.assertRaises(ValueError):
            folder_verifier.verify_customer_folder(self.out)

    def test_bounded_approval_manifest_reread_not_plain_readbytes(self):
        approval=self.base/"approval.json"
        approval.write_text(json.dumps({
           "contract":"DATA2WEB_INPUT_APPROVALS_V1",
           "sources":[{"filename":"a.csv"},{"filename":"b.csv"}],
           "mapping":{"id":"id","title":"title","category":"category"},
           "approval":{"rights_and_plaintext_ack":True,
                       "privacy_classification":"NO_PERSONAL_DATA_REVIEWED"}
        }),encoding="utf-8")
        import data2web_append as append
        with patch.object(append,"read_bounded_source",wraps=append.read_bounded_source) as fn:
            doc=read_approval_manifest(approval)
        self.assertEqual(doc["contract"],"DATA2WEB_INPUT_APPROVALS_V1")
        fn.assert_called_once()
        self.assertEqual(fn.call_args.kwargs,{"max_bytes":64000})

    def test_approval_link_rejected(self):
        alias=self.base/"alias.json"
        source=self.base/"a.json"
        source.write_text('{"contract":"DATA2WEB_INPUT_APPROVALS_V1"}',encoding="utf-8")
        try:alias.symlink_to(source)
        except (NotImplementedError,OSError):self.skipTest("Symlink unavailable")
        with self.assertRaises(ValueError):read_approval_manifest(alias)

if __name__=="__main__":
    unittest.main()
