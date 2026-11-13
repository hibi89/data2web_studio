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
