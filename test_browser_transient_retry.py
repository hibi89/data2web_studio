"""Browser retry is narrowly scoped to launch failures, never data failures."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import subprocess
import tempfile
import unittest

import client_local_rehearsal as rehearsal


GOOD = SimpleNamespace(
    returncode=0,
    stdout=(b'<p id="count" role="status">2 items</p>'
            b'LOCAL-ITEM-1 LOCAL-ITEM-2'),
    stderr=b"",
)


class NativeBrowserTransientRecovery(unittest.TestCase):
    def _run(self, outcomes):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(rehearsal.subprocess, "run", side_effect=outcomes) as process:
                result = rehearsal._headless_browser(
                    Path("chrome.exe"), Path(temp)/"index.html", Path(temp))
                calls = process.call_args_list
        return result, calls

    def test_single_timeout_then_real_dom_passes_with_new_profile(self):
        result, calls = self._run([
            subprocess.TimeoutExpired(cmd="chrome.exe", timeout=22),
            GOOD,
        ])
        self.assertEqual(result, "PASS_SYNTHETIC_LOCAL_FILE")
        self.assertEqual(len(calls), 2)
        command0 = calls[0].args[0]
        command1 = calls[1].args[0]
        profile0 = [x for x in command0 if x.startswith("--user-data-dir=")]
        profile1 = [x for x in command1 if x.startswith("--user-data-dir=")]
        self.assertEqual(len(profile0), 1)
        self.assertEqual(len(profile1), 1)
        self.assertNotEqual(profile0[0], profile1[0])
        self.assertEqual(calls[0].kwargs["timeout"], 22)
        self.assertEqual(calls[1].kwargs["timeout"], 22)

    def test_one_oserror_then_pass(self):
        result, calls = self._run([OSError("synthetic startup failed"), GOOD])
        self.assertEqual(result, "PASS_SYNTHETIC_LOCAL_FILE")
        self.assertEqual(len(calls), 2)

    def test_two_timeouts_stay_hold(self):
        error = subprocess.TimeoutExpired(cmd="chrome.exe", timeout=22)
        result, calls = self._run([error, error])
        self.assertEqual(result, "HOLD_EXECUTION_FAILED")
        self.assertEqual(len(calls), 2)

    def test_nonzero_twice_stays_hold(self):
        result, calls = self._run([
            SimpleNamespace(returncode=3,stdout=b"",stderr=b""),
            SimpleNamespace(returncode=3,stdout=b"",stderr=b""),
        ])
        self.assertEqual(result, "HOLD_NONZERO_EXIT")
        self.assertEqual(len(calls), 2)

    def test_unrendered_dom_does_not_get_retry_or_pass(self):
        bad = SimpleNamespace(returncode=0,stdout=b'<p id="count" role="status"></p>',
                              stderr=b"")
        result, calls = self._run([bad])
        self.assertEqual(result, "HOLD_BROWSER_RENDER_NOT_CONFIRMED")
        self.assertEqual(len(calls), 1)

    def test_missing_rows_does_not_get_retry_or_pass(self):
        bad = SimpleNamespace(returncode=0,
                              stdout=b'<p id="count" role="status">2 items</p>',
                              stderr=b"")
        result, calls = self._run([bad])
        self.assertEqual(result, "HOLD_BROWSER_CONTENT_NOT_VISIBLE")
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
