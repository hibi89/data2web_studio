"""Independent customer-folder verification and deliberate tampering regressions."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from data2web_single import deliver_single
from data2web_append import deliver_to_new_directory
from verify_customer_folder import verify_customer_folder
from package_portable import create_portable

class CustomerFolderContract(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.source=self.root/"one.csv"
        self.source.write_text("id,title,category\n1,One,A\n2,Two,B\n",encoding="utf-8")
        self.folder=self.root/"customer"

    def make(self):
        return deliver_single(self.source,self.folder,
                    expected_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),
                    id_column="id",title_column="title",category_column="category",
                    confirm="APPROVE",ack_plaintext=True,
                    privacy_classification="NO_PERSONAL_DATA_REVIEWED")

    def test_single_complete_folder_verified(self):
        self.make()
        result=verify_customer_folder(self.folder)
        self.assertTrue(result["verified"])
        self.assertFalse(result["sale_approved"])
        self.assertEqual(result["rows"],2)
        self.assertEqual(len(result["html_sha256"]),64)

    def test_source_file_not_required_for_offline_integrity_validation(self):
        self.make()
        self.source.unlink()
        self.assertTrue(verify_customer_folder(self.folder)["verified"])

    def test_mutated_on_disk_html_rejected(self):
        self.make()
        html=self.folder/"index.html"
        html.write_bytes(html.read_bytes()+b"\n<!--tamper-->")
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

    def test_mutated_receipt_sha_rejected(self):
        self.make()
        path=self.folder/"receipt.json"
        obj=json.loads(path.read_text(encoding="utf-8"))
        obj["output_sha256"]="f"*64
        path.write_text(json.dumps(obj),encoding="utf-8")
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

    def test_mutated_receipt_mapping_rejected(self):
        self.make()
        path=self.folder/"receipt.json"
        obj=json.loads(path.read_text(encoding="utf-8"))
        obj["mapping"]["id"]="category"
        path.write_text(json.dumps(obj),encoding="utf-8")
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

    def test_mutated_receipt_privacy_to_unreviewed_rejected(self):
        self.make()
        path=self.folder/"receipt.json"
        obj=json.loads(path.read_text(encoding="utf-8"))
        obj["privacy_classification"]="AUTOMATICALLY_APPROVED"
        path.write_text(json.dumps(obj),encoding="utf-8")
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

    def test_receipt_nonfinite_json_constant_rejected(self):
        self.make()
        from verify_customer_folder import _load_json
        for token in (b"NaN",b"Infinity",b"-Infinity"):
            with self.subTest(token=token):
                with self.assertRaises(ValueError):
                    _load_json(b'{"suspicious":'+token+b'}')
        path=self.folder/"receipt.json"
        obj=json.loads(path.read_text(encoding="utf-8"))
        obj["header_row"]=float("nan")
        path.write_text(json.dumps(obj,allow_nan=True),encoding="utf-8")
        with self.assertRaises(ValueError):
            verify_customer_folder(self.folder)

    def test_receipt_duplicate_json_key_rejected(self):
        self.make()
        path=self.folder/"receipt.json"
        payload=path.read_text(encoding="utf-8")
        payload=payload.replace('"sale_approved":false','"sale_approved":true,"sale_approved":false')
        path.write_text(payload,encoding="utf-8")
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

    def test_extra_hidden_file_rejected(self):
        self.make()
        (self.folder/".unexpected").write_text("EXTRA",encoding="utf-8")
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

    def test_missing_receipt_rejected_without_deleting_html(self):
        self.make()
        before=(self.folder/"index.html").read_bytes()
        (self.folder/"receipt.json").unlink()
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)
        self.assertEqual((self.folder/"index.html").read_bytes(),before)

    def test_swapped_zip_between_two_folders_rejected(self):
        self.make()
        other=self.root/"other"
        changed=self.root/"other.csv"
        changed.write_text("id,title,category\n10,Other,A\n",encoding="utf-8")
        deliver_single(changed,other,expected_sha256=hashlib.sha256(changed.read_bytes()).hexdigest(),
                       id_column="id",title_column="title",category_column="category",
                       confirm="APPROVE",ack_plaintext=True,
                       privacy_classification="NO_PERSONAL_DATA_REVIEWED")
        (self.folder/"delivery.zip").write_bytes((other/"delivery.zip").read_bytes())
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

    def test_multi_source_complete_folder_verified(self):
        two=self.root/"two.csv"
        two.write_text("id,title,category\n3,Third,C\n",encoding="utf-8")
        sources=[{"filename":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
                 for p in (self.source,two)]
        approved=self.root/"approved.json"
        approved.write_text(json.dumps({
           "contract":"DATA2WEB_INPUT_APPROVALS_V1","sources":sources,
           "mapping":{"id":"id","title":"title","category":"category"},
           "approval":{"rights_and_plaintext_ack":True,
                       "privacy_classification":"OWNER_APPROVED_LOCAL_ONLY"}
        }),encoding="utf-8")
        deliver_to_new_directory(approved,self.folder,confirm="APPROVE",ack_plaintext=True)
        result=verify_customer_folder(self.folder)
        self.assertTrue(result["verified"])
        self.assertEqual(result["rows"],3)

    def test_portable_zipapp_verifies_folder(self):
        self.make()
        app=self.root/"portable.pyz"
        create_portable(app)
        p=subprocess.run([sys.executable,str(app),"verify-customer",str(self.folder)],
                         text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        j=json.loads(p.stdout)
        self.assertTrue(j["verified"])

    def test_cli_verification_rejects_tampered_folder_without_source_cells(self):
        self.make()
        path=self.folder/"receipt.json"
        obj=json.loads(path.read_text(encoding="utf-8"))
        obj["source_sha256"]="f"*64
        path.write_text(json.dumps(obj),encoding="utf-8")
        p=subprocess.run([sys.executable,"studio.py","verify-customer",str(self.folder)],
                         text=True,encoding="utf-8",capture_output=True,
                         cwd=Path(__file__).resolve().parent)
        self.assertEqual(p.returncode,2)
        self.assertEqual(json.loads(p.stdout)["status"],"HOLD")
        self.assertNotIn("One",p.stdout)
        self.assertNotIn(str(self.source),p.stdout)

    def test_file_link_guard_refuses_symlink_receipt(self):
        self.make()
        original=self.root/"old_receipt.json"
        original.write_bytes((self.folder/"receipt.json").read_bytes())
        (self.folder/"receipt.json").unlink()
        try:(self.folder/"receipt.json").symlink_to(original)
        except (OSError,NotImplementedError):self.skipTest("File link creation unavailable")
        with self.assertRaises(ValueError):verify_customer_folder(self.folder)

if __name__=="__main__":
    unittest.main()
