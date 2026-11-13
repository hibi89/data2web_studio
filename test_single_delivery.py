"""R02, R24, R32: single-record JSON and actual single customer delivery contracts."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from data2web import read_table
from data2web_single import deliver_single
from package_portable import create_portable
from verify_delivery import verify_zip
from test_xlsx_fixtures import workbook_bytes

ROOT=Path(__file__).resolve().parent
class SingleDelivery(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.source=self.root/"source.csv"
        self.source.write_text("id,title,category,notes\nA-01,Sample English,A,First\nA-02,한글 상품,B,Second\n",encoding="utf-8")
        self.target=self.root/"new-customer"
    def options(self,**kw):
        params={"expected_sha256":hashlib.sha256(self.source.read_bytes()).hexdigest(),
                "id_column":"id","title_column":"title","category_column":"category",
                "confirm":"APPROVE","ack_plaintext":True,
                "privacy_classification":"NO_PERSONAL_DATA_REVIEWED"}
        params.update(kw)
        return params
    def make(self,**kwargs):return deliver_single(self.source,self.target,**self.options(**kwargs))

    def test_single_csv_full_customer_delivery(self):
        result=self.make()
        self.assertEqual(result["rows"],2)
        self.assertTrue(result["delivery_folder_created"])
        self.assertTrue((self.target/"index.html").exists())
        self.assertTrue((self.target/"delivery.zip").exists())
        self.assertTrue((self.target/"receipt.json").exists())
        self.assertTrue(verify_zip(self.target/"delivery.zip")["verified"])
        metadata=json.loads((self.target/"receipt.json").read_text(encoding="utf-8"))
        self.assertFalse(metadata["sale_approved"])
        self.assertEqual(metadata["privacy_classification"],"NO_PERSONAL_DATA_REVIEWED")
        self.assertNotIn("한글 상품",json.dumps(metadata,ensure_ascii=False))
    def test_cli_single_csv_delivery(self):
        digest=hashlib.sha256(self.source.read_bytes()).hexdigest()
        command=[sys.executable,"studio.py","deliver",str(self.source),str(self.target),
                 "--source-sha256",digest,"--id","id","--title","title","--category","category",
                 "--confirm","APPROVE","--ack-plaintext",
                 "--privacy-classification","OWNER_APPROVED_LOCAL_ONLY"]
        result=subprocess.run(command,cwd=ROOT,text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertNotIn("한글 상품",result.stdout)
        self.assertTrue(verify_zip(self.target/"delivery.zip")["verified"])
    def test_single_portable_zipapp_delivery(self):
        app=self.root/"tool.pyz"
        create_portable(app)
        digest=hashlib.sha256(self.source.read_bytes()).hexdigest()
        result=subprocess.run([sys.executable,str(app),"deliver",str(self.source),str(self.target),
              "--source-sha256",digest,"--id","id","--title","title","--category","category",
              "--confirm","APPROVE","--ack-plaintext",
              "--privacy-classification","NO_PERSONAL_DATA_REVIEWED"],
              text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue(verify_zip(self.target/"delivery.zip")["verified"])
    def test_single_xlsx_missing_sheet_creates_no_customer_folder(self):
        self.source=self.root/"workbook.xlsx"
        self.source.write_bytes(workbook_bytes())
        with self.assertRaises(ValueError):self.make()
        self.assertFalse(self.target.exists())

    def test_single_xlsx_owner_selected_sheet_and_zip(self):
        self.source=self.root/"workbook.xlsx"
        self.source.write_bytes(workbook_bytes())
        result=self.make(sheet="Inventory")
        self.assertEqual(result["rows"],2)
        self.assertEqual(result["sheet"],"Inventory")
        self.assertTrue(verify_zip(self.target/"delivery.zip")["verified"])

    def test_source_sha_changed_preflight_keeps_folder_absent(self):
        with self.assertRaises(ValueError):
            self.make(expected_sha256="f"*64)
        self.assertFalse(self.target.exists())
    def test_explicit_privacy_mode_required(self):
        for mode in (None,"","AUTOMATICALLY_SAFE","UNREVIEWED"):
            with self.subTest(mode=mode):
                with self.assertRaises(ValueError):self.make(privacy_classification=mode)
                self.assertFalse(self.target.exists())
    def test_rights_ack_denied(self):
        for config in ({"ack_plaintext":False},{"confirm":"DENY"}):
            with self.subTest(config=config):
                with self.assertRaises(ValueError):self.make(**config)
                self.assertFalse(self.target.exists())
    def test_wrong_mapping_preflight(self):
        with self.assertRaises(ValueError):self.make(title_column="category")
        self.assertFalse(self.target.exists())
    def test_duplicate_ids_preflight(self):
        self.source.write_text("id,title,category\n1,First,A\n1,Second,B\n",encoding="utf-8")
        with self.assertRaises(ValueError):self.make()
        self.assertFalse(self.target.exists())
    def test_existing_directory_never_overwritten(self):
        self.target.mkdir()
        keep=self.target/"keep.txt"
        keep.write_text("UNTOUCHED",encoding="utf-8")
        with self.assertRaises((FileExistsError,ValueError)):self.make()
        self.assertEqual(keep.read_text(encoding="utf-8"),"UNTOUCHED")
    def test_no_destructive_repeat(self):
        self.make()
        before=(self.target/"delivery.zip").read_bytes()
        with self.assertRaises((FileExistsError,ValueError)):self.make()
        self.assertEqual((self.target/"delivery.zip").read_bytes(),before)
    def test_output_is_deterministic_across_folders(self):
        one=self.make()
        second=self.root/"another"
        two=deliver_single(self.source,second,**self.options())
        self.assertEqual((self.target/"index.html").read_bytes(),(second/"index.html").read_bytes())
        self.assertEqual((self.target/"delivery.zip").read_bytes(),(second/"delivery.zip").read_bytes())
        self.assertEqual(one["source_sha256"],two["source_sha256"])
    def test_input_symlink_refused(self):
        backup=self.root/"true.csv"
        backup.write_bytes(self.source.read_bytes())
        self.source.unlink()
        try:self.source.symlink_to(backup)
        except (OSError,NotImplementedError):self.skipTest("OS symlinks unavailable")
        with self.assertRaises(ValueError):self.make()
        self.assertFalse(self.target.exists())
    def test_json_flat_object_one_row(self):
        file=self.root/"row.json"
        file.write_text('{"id":"single","title":"단독 JSON","category":"A","count":7}',encoding="utf-8")
        fields,rows,digest=read_table(file)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["count"],"7")
        self.assertEqual(len(digest),64)
    def test_json_flat_object_delivery(self):
        self.source=self.root/"single.json"
        self.source.write_text('{"id":"x1","title":"Object Record","category":"A"}',encoding="utf-8")
        result=self.make()
        self.assertEqual(result["rows"],1)
        self.assertTrue(verify_zip(self.target/"delivery.zip")["verified"])
    def test_json_root_object_nested_refused(self):
        self.source=self.root/"nested.json"
        self.source.write_text('{"id":"1","title":{"bad":"nested"},"category":"A"}',encoding="utf-8")
        with self.assertRaises(ValueError):self.make()
        self.assertFalse(self.target.exists())
    def test_json_root_object_records_key_not_implicitly_unwrapped(self):
        self.source=self.root/"nested.json"
        self.source.write_text('{"rows":[{"id":"a"}]}',encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.source)
    def test_json_nonfinite_constant_refused(self):
        self.source=self.root/"nan.json"
        self.source.write_text('[{"id":"1","title":NaN,"category":"A"}]',encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.source)
    def test_json_duplicate_keys_still_rejected(self):
        self.source=self.root/"duplicate.json"
        self.source.write_text('{"id":"1","id":"2","title":"x","category":"A"}',encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.source)

if __name__=="__main__":unittest.main()
