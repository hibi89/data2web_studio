"""Regression: pressing Ctrl+C during the optional Tk window is not a crash.

Mock only the Tk entrypoint. Never load customer files, windows or network.
"""
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import studio


class DesktopInterruptContract(unittest.TestCase):
    def test_console_interrupt_is_explicit_redacted_nonzero(self):
        out=io.StringIO()
        with patch("data2web_desktop.desktop_main",
                   side_effect=KeyboardInterrupt("SENSITIVE_USER_PATH")) as launcher:
            with redirect_stdout(out):
                code=studio.main(["desktop"])
        launcher.assert_called_once_with()
        self.assertEqual(code,130)
        receipt=json.loads(out.getvalue())
        self.assertEqual(receipt,{"action":"desktop",
                                  "sale_approved":False,"status":"INTERRUPTED"})
        self.assertNotIn("SENSITIVE_USER_PATH",out.getvalue())
        self.assertNotIn("Traceback",out.getvalue())

    def test_normal_window_close_keeps_zero_exit_without_output(self):
        out=io.StringIO()
        with patch("data2web_desktop.desktop_main",return_value=None) as launcher:
            with redirect_stdout(out):
                code=studio.main(["desktop"])
        launcher.assert_called_once_with()
        self.assertEqual(code,0)
        self.assertEqual(out.getvalue(),"")

    def test_keyboard_interrupt_does_not_mark_release_approved(self):
        out=io.StringIO()
        with patch("data2web_desktop.desktop_main",
                   side_effect=KeyboardInterrupt):
            with redirect_stdout(out):
                code=studio.main(["desktop"])
        self.assertEqual(code,130)
        self.assertFalse(json.loads(out.getvalue())["sale_approved"])


if __name__=="__main__":
    unittest.main()
