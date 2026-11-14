"""Headless Tcl regression of consent invalidation (no desktop display required)."""
import ast
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent

class ConsentResetBindingTests(unittest.TestCase):
    def test_desktop_module_parses(self):
        ast.parse((ROOT/"data2web_desktop.py").read_text(encoding="utf-8"))

    def test_single_and_batch_reset_on_every_mapping_or_destination_change(self):
        try:
            import tkinter as tk
        except ImportError:
            self.skipTest("Tkinter unavailable; Windows GUI acceptance still pending")
        from data2web_desktop import bind_consent_reset
        for names in (
            ("id_key","title_key","category_key","parent","folder"),
            ("batch_id","batch_title","batch_category","batch_parent","batch_leaf"),
        ):
            with self.subTest(scope=names[0]):
                interpreter=tk.Tcl()  # No window, no display server.
                variables={name:tk.StringVar(master=interpreter) for name in names}
                rights=tk.BooleanVar(master=interpreter)
                plaintext=tk.BooleanVar(master=interpreter)
                privacy=tk.StringVar(master=interpreter)
                callback=bind_consent_reset(tuple(variables.values()),rights,plaintext,privacy)
                self.assertTrue(callable(callback))
                for name,var in variables.items():
                    with self.subTest(variable=name):
                        rights.set(True)
                        plaintext.set(True)
                        privacy.set("OWNER_APPROVED_LOCAL_ONLY")
                        var.set(name+"-changed")
                        self.assertFalse(rights.get())
                        self.assertFalse(plaintext.get())
                        self.assertEqual(privacy.get(),"")

    def test_unrelated_display_option_does_not_clear_consent(self):
        try:
            import tkinter as tk
        except ImportError:
            self.skipTest("Tkinter unavailable")
        from data2web_desktop import bind_consent_reset
        interpreter=tk.Tcl()
        mapping=tk.StringVar(master=interpreter)
        theme=tk.StringVar(master=interpreter)
        rights=tk.BooleanVar(master=interpreter,value=True)
        plaintext=tk.BooleanVar(master=interpreter,value=True)
        privacy=tk.StringVar(master=interpreter,value="NO_PERSONAL_DATA_REVIEWED")
        callback=bind_consent_reset((mapping,),rights,plaintext,privacy)
        self.assertTrue(callable(callback))
        theme.set("cafe")
        self.assertTrue(rights.get())
        self.assertTrue(plaintext.get())
        self.assertEqual(privacy.get(),"NO_PERSONAL_DATA_REVIEWED")

if __name__=="__main__":
    unittest.main()
