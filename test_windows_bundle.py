"""R32 portable Windows launcher: actual cmd on hosted Windows, integrity on both OS."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from package_windows_bundle import create_windows_bundle, verify_windows_bundle

ROOT=Path(__file__).resolve().parent

class WindowsBundle(unittest.TestCase):
    def setUp(self):
        holder=tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.root=Path(holder.name)
        self.target=self.root/"new-windows-bundle"

    def make(self):
        return create_windows_bundle(self.target)

    def test_unsigned_bundle_creation_and_integrity(self):
        result=self.make()
        self.assertTrue(result["created"] and result["verified"])
        self.assertFalse(result["signed_executable"])
        self.assertFalse(result["sale_approved"])
        verified=verify_windows_bundle(self.target)
        self.assertTrue(verified["verified"])
        self.assertEqual(result["bundle_sha256"],verified["bundle_sha256"])
        actual=sorted(p.name for p in self.target.iterdir())
        self.assertEqual(actual,sorted(["DATA2WEB.pyz","RUN_DESKTOP.cmd",
                          "RUN_SELFCHECK.cmd","VERIFY_CUSTOMER.cmd",
                          "README_LOCAL_KO.txt","BUNDLE_MANIFEST.json"]))
        for name in ("RUN_DESKTOP.cmd","RUN_SELFCHECK.cmd","VERIFY_CUSTOMER.cmd"):
            data=(self.target/name).read_text(encoding="utf-8")
            self.assertIn("Python 3.11+",data)
            self.assertNotIn("http://",data)
            self.assertNotIn("https://",data)

    def test_identical_bundle_bytes_in_independent_folders(self):
        self.make()
        second=self.root/"second"
        create_windows_bundle(second)
        for member in self.target.iterdir():
            self.assertEqual(member.read_bytes(),(second/member.name).read_bytes())

    def test_existing_target_not_overwritten(self):
        self.target.mkdir()
        original=self.target/"user.txt"
        original.write_text("DO NOT TOUCH",encoding="utf-8")
        with self.assertRaises((FileExistsError,ValueError)):
            self.make()
        self.assertEqual(original.read_text(encoding="utf-8"),"DO NOT TOUCH")

    def test_byte_change_in_launch_script_rejected(self):
        self.make()
        cmd=self.target/"RUN_DESKTOP.cmd"
        cmd.write_bytes(cmd.read_bytes()+b"\nrem unexpected modification")
        with self.assertRaises(ValueError):
            verify_windows_bundle(self.target)

    def test_byte_change_in_python_runtime_rejected(self):
        self.make()
        p=self.target/"DATA2WEB.pyz"
        p.write_bytes(p.read_bytes()+b"corrupted")
        with self.assertRaises(ValueError):
            verify_windows_bundle(self.target)

    def test_unknown_file_rejected(self):
        self.make()
        (self.target/".extra").write_text("unknown",encoding="utf-8")
        with self.assertRaises(ValueError):
            verify_windows_bundle(self.target)

    def test_missing_file_rejected(self):
        self.make()
        (self.target/"RUN_SELFCHECK.cmd").unlink()
        with self.assertRaises(ValueError):
            verify_windows_bundle(self.target)

    def test_unapproved_sale_flag_rejected(self):
        self.make()
        p=self.target/"BUNDLE_MANIFEST.json"
        doc=json.loads(p.read_text(encoding="utf-8"))
        doc["sale_approved"]=True
        p.write_text(json.dumps(doc),encoding="utf-8")
        with self.assertRaises(ValueError):verify_windows_bundle(self.target)

    def test_manifest_duplicate_keys_rejected(self):
        self.make()
        p=self.target/"BUNDLE_MANIFEST.json"
        raw=p.read_text(encoding="utf-8")
        self.assertIn('"sale_approved":false',raw)
        p.write_text(raw.replace('"sale_approved":false',
                     '"sale_approved":false,"sale_approved":false',1),encoding="utf-8")
        with self.assertRaises(ValueError):verify_windows_bundle(self.target)

    def test_unsafe_link_rejected(self):
        self.make()
        original=self.root/"script.cmd"
        original.write_bytes((self.target/"RUN_DESKTOP.cmd").read_bytes())
        (self.target/"RUN_DESKTOP.cmd").unlink()
        try:(self.target/"RUN_DESKTOP.cmd").symlink_to(original)
        except (NotImplementedError,OSError):
            self.skipTest("OS symlink creation unavailable")
        with self.assertRaises(ValueError):verify_windows_bundle(self.target)

    def test_python_zipapp_inside_bundle_executes_offline_selfcheck(self):
        self.make()
        p=subprocess.run([sys.executable,str(self.target/"DATA2WEB.pyz"),"self-check"],
                         capture_output=True,encoding="utf-8",text=True,check=False)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        result=json.loads(p.stdout)
        self.assertTrue(result["local_folder_verified"])
        self.assertEqual(result["status"],"PASS_SYNTHETIC_ONLY")

    @unittest.skipUnless(os.name=="nt","Windows cmd.exe only")
    def test_real_hosted_windows_launcher_cmd_executes_browser_selfcheck(self):
        self.make()
        p=subprocess.run(["cmd.exe","/c",str(self.target/"RUN_SELFCHECK.cmd")],
                        capture_output=True,encoding="utf-8",text=True,check=False,
                        timeout=90)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        doc=json.loads(p.stdout.strip().splitlines()[-1])
        self.assertEqual(doc["status"],"PASS_SYNTHETIC_ONLY")
        self.assertEqual(doc["browser_results"],
            {"chrome":"PASS_SYNTHETIC_LOCAL_FILE","edge":"PASS_SYNTHETIC_LOCAL_FILE"})

if __name__=="__main__":
    unittest.main()
