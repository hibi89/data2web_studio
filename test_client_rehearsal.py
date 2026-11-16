"""Customer local rehearsal is fully synthetic, privacy-redacted and fail-closed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import client_local_rehearsal as rehearsal
from package_portable import create_portable

ROOT=Path(__file__).resolve().parent

class LocalRehearsal(unittest.TestCase):
    def test_direct_private_synthetic_rehearsal(self):
        result=rehearsal.self_check(with_browsers=False)
        self.assertEqual(result["status"],"PASS_SYNTHETIC_ONLY")
        self.assertEqual(result["sample_type"],"GENERATED_SYNTHETIC_NOT_CUSTOMER_INPUT")
        self.assertTrue(result["local_folder_verified"])
        self.assertFalse(result["customer_rights_approved"])
        self.assertFalse(result["commercial_release_approved"])
        self.assertFalse(result["customer_source_inspected"])
        self.assertNotIn("LOCAL-ITEM-1",json.dumps(result))

    def test_evidence_is_local_create_only_and_not_customer_approval(self):
        with tempfile.TemporaryDirectory() as holder:
            report=Path(holder)/"synthetic-evidence.json"
            outcome=rehearsal.save_rehearsal_evidence(report,with_browsers=False)
            raw=report.read_bytes()
            doc=json.loads(raw)
            self.assertEqual(outcome["status"],"PASS_SYNTHETIC_ONLY")
            self.assertEqual(doc["contract"],"DATA2WEB_LOCAL_DEVICE_EVIDENCE_V1")
            self.assertEqual(doc["results"]["status"],"PASS_SYNTHETIC_ONLY")
            self.assertFalse(doc["actual_customer_acceptance"])
            self.assertFalse(doc["customer_rights_verified"])
            self.assertFalse(doc["commercial_distribution_approved"])
            self.assertFalse(doc["network_upload_performed"])
            self.assertNotIn("LOCAL-ITEM-1",raw.decode("utf-8"))
            self.assertNotIn(str(report),raw.decode("utf-8"))
            import hashlib
            self.assertEqual(outcome["evidence_sha256"],hashlib.sha256(raw).hexdigest())
            with self.assertRaises((FileExistsError,ValueError)):
                rehearsal.save_rehearsal_evidence(report,with_browsers=False)
            self.assertEqual(report.read_bytes(),raw)

    def test_evidence_missing_native_browser_remains_partial(self):
        with tempfile.TemporaryDirectory() as holder:
            with patch.object(rehearsal,"_browser_binary",return_value=None):
                result=rehearsal.save_rehearsal_evidence(
                    Path(holder)/"hold.json",with_browsers=True)
            self.assertEqual(result["status"],"PARTIAL_HOLD")
            self.assertFalse(result["actual_customer_acceptance"])

    def test_cli_self_check_create_only_evidence(self):
        with tempfile.TemporaryDirectory() as holder:
            path=Path(holder)/"report.json"
            command=[sys.executable,"studio.py","self-check",
                     "--evidence-output",str(path)]
            first=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,
                                 encoding="utf-8",check=False)
            self.assertEqual(first.returncode,0,first.stderr)
            report=json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(report["scope"],"SYNTHETIC_LOCAL_DEVICE_CHECK_ONLY")
            before=path.read_bytes()
            again=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,
                                 encoding="utf-8",check=False)
            self.assertEqual(again.returncode,2,again.stdout+again.stderr)
            self.assertEqual(json.loads(again.stdout)["status"],"HOLD")
            self.assertEqual(path.read_bytes(),before)

    def test_absent_customer_browser_fails_closed(self):
        with patch.object(rehearsal,"_browser_binary",return_value=None):
            result=rehearsal.self_check(with_browsers=True)
        self.assertEqual(result["status"],"PARTIAL_HOLD")
        self.assertEqual(result["browser_results"]["chrome"],"HOLD_BROWSER_NOT_INSTALLED")
        self.assertEqual(result["browser_results"]["edge"],"HOLD_BROWSER_NOT_INSTALLED")

    def test_failed_render_fails_closed(self):
        with patch.object(rehearsal,"_browser_binary",return_value=Path("fake-browser")):
            with patch.object(rehearsal,"_headless_browser",return_value="HOLD_BROWSER_RENDER_NOT_CONFIRMED"):
                result=rehearsal.self_check(with_browsers=True)
        self.assertEqual(result["status"],"PARTIAL_HOLD")

    def test_native_browser_result_matches_real_p_count_role(self):
        from types import SimpleNamespace
        fake=SimpleNamespace(returncode=0,stdout=(
           b'<p id="count" role="status">2\xea\xb1\xb4</p>LOCAL-ITEM-1 LOCAL-ITEM-2'),
           stderr=b"")
        with patch.object(rehearsal.subprocess,"run",return_value=fake):
            with tempfile.TemporaryDirectory() as folder:
                result=rehearsal._headless_browser(Path("chrome.exe"),
                         Path(folder)/"index.html",Path(folder))
        self.assertEqual(result,"PASS_SYNTHETIC_LOCAL_FILE")

    def test_native_browser_does_not_accept_unrendered_placeholder(self):
        from types import SimpleNamespace
        fake=SimpleNamespace(returncode=0,
            stdout=b'<p id="count" role="status"></p>LOCAL-ITEM-1 LOCAL-ITEM-2',stderr=b"")
        with patch.object(rehearsal.subprocess,"run",return_value=fake):
            with tempfile.TemporaryDirectory() as folder:
                result=rehearsal._headless_browser(Path("msedge.exe"),
                         Path(folder)/"index.html",Path(folder))
        self.assertEqual(result,"HOLD_BROWSER_RENDER_NOT_CONFIRMED")

    def test_cli_self_check_outputs_only_redacted_json(self):
        process=subprocess.run([sys.executable,"studio.py","self-check"],cwd=ROOT,
                capture_output=True,text=True,encoding="utf-8",check=False)
        self.assertEqual(process.returncode,0,process.stdout+process.stderr)
        result=json.loads(process.stdout)
        self.assertEqual(result["status"],"PASS_SYNTHETIC_ONLY")
        self.assertNotIn("LOCAL-ITEM-",process.stdout)

    def test_portable_zipapp_self_check(self):
        with tempfile.TemporaryDirectory() as directory:
            archive=Path(directory)/"customer-tool.pyz"
            create_portable(archive)
            process=subprocess.run([sys.executable,str(archive),"self-check"],
                 capture_output=True,text=True,encoding="utf-8",check=False)
            self.assertEqual(process.returncode,0,process.stdout+process.stderr)
            self.assertTrue(json.loads(process.stdout)["local_folder_verified"])

if __name__=="__main__":
    unittest.main()
