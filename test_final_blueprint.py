"""R08 R13 R24 R26 R32 final blueprint execution and adversarial regressions."""
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from data2web import read_table
from data2web_append import build_approved_append, provenance_sha
from data2web_profile import profile_table
from receipt_utils import write_receipt
from verify_delivery import verify_zip
from test_xlsx_fixtures import workbook_bytes

ROOT=Path(__file__).resolve().parent

class FinalBlueprint(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.one=self.root/"one.csv"
        self.two=self.root/"two.csv"
        self.one.write_text("id,title,category,amount\nA-1,SecretMarker-DO-NOT-LOG,alpha,2\nA-2,Second,beta,3\n",encoding="utf-8")
        self.two.write_text("id,title,category,amount\nB-1,Third,alpha,4\n",encoding="utf-8")
        self.manifest=self.root/"approved.json"
        self.out=self.root/"joined.html"
        self.zip=self.root/"joined.zip"
        self.receipt=self.root/"receipt.json"
        self.configure()

    def configure(self):
        self.doc={
            "contract":"DATA2WEB_INPUT_APPROVALS_V1",
            "sources":[
                {"filename":f.name,"sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
                for f in (self.one,self.two)
            ],
            "mapping":{"id":"id","title":"title","category":"category"},
            "approval":{"rights_and_plaintext_ack":True,
                        "privacy_classification":"OWNER_APPROVED_LOCAL_ONLY"},
            "name":"Synthetic seller test","theme":"office",
        }
        self.save()

    def save(self):
        self.manifest.write_text(json.dumps(self.doc,ensure_ascii=False),encoding="utf-8")

    def build(self, **kw):
        return build_approved_append(self.manifest,self.out,confirm="APPROVE",
                    ack_plaintext=True,**kw)

    def test_profile_no_customer_cell_values(self):
        cols,rows,_=read_table(self.one)
        preview=profile_table(cols,rows)
        text=json.dumps(preview)
        self.assertNotIn("SecretMarker-DO-NOT-LOG",text)
        self.assertEqual(preview["row_count"],2)
        self.assertEqual(preview["columns"][-1]["kind_hint"],"number_text")
        self.assertFalse(preview["values_revealed"])

    def test_profile_blank_and_duplicate_count(self):
        cols=["id","title","category"]
        rows=[{"id":"1","title":"","category":"A"},
              {"id":"1","title":"","category":"A"}]
        result=profile_table(cols,rows)
        self.assertEqual(result["duplicate_full_rows"],1)
        self.assertEqual(result["columns"][1]["blank_cells"],2)
        self.assertEqual(result["columns"][0]["duplicate_nonblank"],1)

    def test_cli_inspect_profile_does_not_leak_values(self):
        x=subprocess.run([sys.executable,"studio.py","inspect",str(self.one)],
                         cwd=ROOT,encoding="utf-8",capture_output=True,text=True)
        self.assertEqual(x.returncode,0,x.stdout+x.stderr)
        j=json.loads(x.stdout)
        self.assertIn("profile",j)
        self.assertEqual(j["profile"]["column_count"],4)
        self.assertNotIn("SecretMarker-DO-NOT-LOG",x.stdout)

    def test_two_file_append_zip_and_receipt_end_to_end(self):
        receipt=self.build(zip_path=self.zip,receipt_path=self.receipt)
        self.assertEqual(receipt["rows"],3)
        self.assertEqual(len(receipt["source_receipts"]),2)
        self.assertEqual(receipt["status"],"OWNER_APPROVED_APPEND_LOCAL_ONLY_RELEASE_HOLD")
        self.assertTrue(verify_zip(self.zip)["verified"])
        obj=json.loads(self.receipt.read_text(encoding="utf-8"))
        self.assertEqual(obj["contract"],"DATA2WEB_RECEIPT_V1")
        self.assertEqual(obj["rows"],3)
        self.assertFalse(obj["sale_approved"])
        self.assertNotIn("SecretMarker-DO-NOT-LOG",self.receipt.read_text(encoding="utf-8"))
        self.assertEqual(obj["source_sha256"],provenance_sha(receipt["source_receipts"]))

    def test_cli_append_end_to_end_no_customer_cell_leak(self):
        process=subprocess.run([sys.executable,"studio.py","append",str(self.manifest),str(self.out),
               "--confirm","APPROVE","--ack-plaintext","--zip-path",str(self.zip),
               "--receipt-path",str(self.receipt)],cwd=ROOT,encoding="utf-8",text=True,capture_output=True)
        self.assertEqual(process.returncode,0,process.stdout+process.stderr)
        self.assertNotIn("SecretMarker-DO-NOT-LOG",process.stdout)
        self.assertEqual(json.loads(process.stdout)["rows"],3)
        self.assertTrue(verify_zip(self.zip)["verified"])

    def test_append_never_overwrites_any_customer_artifacts(self):
        self.out.write_text("KEEP",encoding="utf-8")
        with self.assertRaises(FileExistsError):self.build(zip_path=self.zip)
        self.assertEqual(self.out.read_text(encoding="utf-8"),"KEEP")
        self.assertFalse(self.zip.exists())

    def test_append_refuses_existing_zip(self):
        self.zip.write_bytes(b"KEEP")
        with self.assertRaises(FileExistsError):self.build(zip_path=self.zip)
        self.assertEqual(self.zip.read_bytes(),b"KEEP")
        self.assertFalse(self.out.exists())

    def test_append_refuses_existing_receipt(self):
        self.receipt.write_text("KEEP",encoding="utf-8")
        with self.assertRaises(FileExistsError):self.build(receipt_path=self.receipt)
        self.assertEqual(self.receipt.read_text(encoding="utf-8"),"KEEP")
        self.assertFalse(self.out.exists())

    def test_append_id_collision_fail_closed(self):
        self.two.write_text("id,title,category,amount\nA-1,Collision,b,5\n",encoding="utf-8")
        self.configure()
        with self.assertRaises(ValueError):self.build()
        self.assertFalse(self.out.exists())

    def test_append_schema_change_fail_closed(self):
        self.two.write_text("id,category,title,amount\nB-1,b,Changed,5\n",encoding="utf-8")
        self.configure()
        with self.assertRaises(ValueError):self.build()

    def test_append_changed_source_hash_fail_closed(self):
        self.two.write_text("id,title,category,amount\nB-1,Modified,alpha,999\n",encoding="utf-8")
        with self.assertRaises(ValueError):self.build()
        self.assertFalse(self.out.exists())

    def test_append_false_rights_ack_hold(self):
        self.doc["approval"]["rights_and_plaintext_ack"]=False
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_missing_privacy_classification_hold(self):
        self.doc["approval"].pop("privacy_classification")
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_invalid_approval_classification_hold(self):
        self.doc["approval"]["privacy_classification"]="AUTO_CLEARED"
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_missing_cli_plaintext_ack_hold(self):
        with self.assertRaises(ValueError):
            build_approved_append(self.manifest,self.out,confirm="APPROVE",ack_plaintext=False)
        self.assertFalse(self.out.exists())

    def test_append_missing_confirm_hold(self):
        with self.assertRaises(ValueError):
            build_approved_append(self.manifest,self.out,confirm="NO",ack_plaintext=True)
        self.assertFalse(self.out.exists())

    def test_append_duplicate_manifest_json_key_hold(self):
        self.manifest.write_text('{"contract":"DATA2WEB_INPUT_APPROVALS_V1","contract":"OVERWRITE"}',encoding="utf-8")
        with self.assertRaises(ValueError):self.build()

    def test_append_bad_filename_traversal_hold(self):
        self.doc["sources"][1]["filename"]="../two.csv"
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_abs_filename_hold(self):
        self.doc["sources"][1]["filename"]=str(self.two)
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_duplicate_source_file_hold(self):
        self.doc["sources"][1]=self.doc["sources"][0].copy()
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_not_enough_sources_hold(self):
        self.doc["sources"]=self.doc["sources"][:1]
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_extra_nonapproved_mapping_hold(self):
        self.doc["mapping"]["unknown"]="extra"
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_bad_sha_hold(self):
        self.doc["sources"][0]["sha256"]="f"*64
        self.save()
        with self.assertRaises(ValueError):self.build()

    def test_append_xlsx_requires_sheet_per_source(self):
        self.two.unlink()
        self.two=self.root/"book.xlsx"
        self.two.write_bytes(workbook_bytes(sheets={"Inventory":[
            ["id","title","category","amount"],["C-1","XLSX row","alpha",6]
        ]}))
        self.configure()
        with self.assertRaises(ValueError):self.build()
        self.doc["sources"][1]["sheet"]="Inventory"
        self.save()
        out=self.build()
        self.assertEqual(out["rows"],3)
        self.assertEqual(out["source_receipts"][1]["kind"],"xlsx")
        self.assertIn("XLSX row",self.out.read_text(encoding="utf-8"))

    def test_append_csv_tsv_same_schema(self):
        self.two.unlink()
        self.two=self.root/"two.tsv"
        self.two.write_text("id\ttitle\tcategory\tamount\nB-1\tTSV Title\talpha\t8\n",encoding="utf-8")
        self.configure()
        r=self.build(zip_path=self.zip)
        self.assertEqual(r["source_receipts"][1]["kind"],"tsv")
        self.assertEqual(verify_zip(self.zip)["rows"],3)

    def test_append_rejects_over_10k_total_rows(self):
        self.one.write_text("id,title,category,amount\n"+"\n".join(
            f"{i},Item-{i},A,1" for i in range(10000))+"\n",encoding="utf-8")
        self.configure()
        with self.assertRaises(ValueError):self.build()

    def test_append_deterministic_output_and_zip_across_paths(self):
        r1=self.build(zip_path=self.zip)
        z2=self.root/"another.zip"
        h2=self.root/"another.html"
        build_approved_append(self.manifest,h2,confirm="APPROVE",ack_plaintext=True,zip_path=z2)
        self.assertEqual(self.out.read_bytes(),h2.read_bytes())
        self.assertEqual(self.zip.read_bytes(),z2.read_bytes())

    def test_append_manifest_embedded_provenance_tamper_hold(self):
        self.build(zip_path=self.zip)
        altered=self.root/"altered.zip"
        with zipfile.ZipFile(self.zip) as a,zipfile.ZipFile(altered,"w") as b:
            for n in a.namelist():
                raw=a.read(n)
                if n=="manifest.json":
                    d=json.loads(raw)
                    d["source_receipts"][0]["rows"]=999
                    d["rows"]=1001
                    raw=json.dumps(d).encode("utf-8")
                b.writestr(n,raw)
        with self.assertRaises(ValueError):verify_zip(altered)

    def test_append_symlink_source_hold(self):
        original=self.one.read_bytes()
        actual=self.root/"private.csv"
        actual.write_bytes(original)
        self.one.unlink()
        try:self.one.symlink_to(actual)
        except (OSError,NotImplementedError):self.skipTest("Symlink requires OS privileges")
        with self.assertRaises(ValueError):self.build()

    def test_receipt_createonly_second_write_hold(self):
        fields,rows,sha=read_table(self.one)
        data={"source_sha256":sha,"output_sha256":"0"*64,"rows":len(rows),
              "columns":fields,"mapping":{"id":"id","title":"title","category":"category"}}
        write_receipt(self.receipt,data)
        before=self.receipt.read_bytes()
        with self.assertRaises(FileExistsError):write_receipt(self.receipt,data)
        self.assertEqual(before,self.receipt.read_bytes())

    def test_profile_does_not_treat_automatic_heuristics_as_privacy_approval(self):
        cols,rows,_=read_table(self.one)
        p=profile_table(cols,rows)
        self.assertEqual(p["personal_data_status"],"OWNER_REVIEW_REQUIRED_NOT_AUTOMATICALLY_CLEARED")
        self.assertNotIn("SecretMarker-DO-NOT-LOG",json.dumps(p,ensure_ascii=False))

if __name__=="__main__":
    unittest.main()
