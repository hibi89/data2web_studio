"""Portable stdlib distribution exact-byte and execution regression."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from package_portable import create_portable
from verify_delivery import verify_zip

ROOT=Path(__file__).resolve().parent

class PortableDelivery(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.archive=self.root/"app.pyz"
        self.csv=self.root/"data.csv"
        self.csv.write_text("id,title,category\nA1,Local sample,X\n",encoding="utf-8")

    def test_deterministic_archive_bytes(self):
        a=create_portable(self.archive)
        second=self.root/"second.pyz"
        b=create_portable(second)
        self.assertEqual(a["sha256"],b["sha256"])
        self.assertEqual(self.archive.read_bytes(),second.read_bytes())
        self.assertFalse(a["sale_approved"])

    def test_create_only_no_overwrite(self):
        self.archive.write_bytes(b"KEEP")
        with self.assertRaises(FileExistsError):create_portable(self.archive)
        self.assertEqual(self.archive.read_bytes(),b"KEEP")

    def test_python_zipapp_inspect(self):
        create_portable(self.archive)
        p=subprocess.run([sys.executable,str(self.archive),"inspect",str(self.csv)],
                         text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        o=json.loads(p.stdout)
        self.assertEqual(o["profile"]["row_count"],1)
        self.assertNotIn("Local sample",p.stdout)

    def test_python_zipapp_append_and_customer_folder(self):
        create_portable(self.archive)
        second=self.root/"second.csv"
        second.write_text("id,title,category\nB1,Second sample,Y\n",encoding="utf-8")
        doc={"contract":"DATA2WEB_INPUT_APPROVALS_V1","sources":[
          {"filename":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
          for p in (self.csv,second)],
          "mapping":{"id":"id","title":"title","category":"category"},
          "approval":{"rights_and_plaintext_ack":True,"privacy_classification":"NO_PERSONAL_DATA_REVIEWED"}}
        src=self.root/"approved.json"
        src.write_text(json.dumps(doc),encoding="utf-8")
        dest=self.root/"new-customer-folder"
        p=subprocess.run([sys.executable,str(self.archive),"deliver-append",str(src),str(dest),
                          "--confirm","APPROVE","--ack-plaintext"],
                          text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertEqual(json.loads(p.stdout)["rows"],2)
        self.assertTrue(verify_zip(dest/"delivery.zip")["verified"])

    def test_python_zipapp_build_zip_verify(self):
        create_portable(self.archive)
        sha=hashlib.sha256(self.csv.read_bytes()).hexdigest()
        html=self.root/"generated.html"
        zipped=self.root/"customer.zip"
        r=subprocess.run([sys.executable,str(self.archive),"build",str(self.csv),str(html),
                "--source-sha256",sha,"--id","id","--title","title","--category","category",
                "--confirm","APPROVE","--ack-plaintext","--zip-path",str(zipped)],
                text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertTrue(verify_zip(zipped)["verified"])
        self.assertEqual(json.loads(r.stdout)["rows"],1)

if __name__=="__main__":unittest.main()
