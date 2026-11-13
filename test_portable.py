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
