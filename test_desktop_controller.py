"""Headless GUI-controller tests. Tk widgets are not instantiated in CI.

The same controller is called by real Tkinter actions, and all output still
goes through existing SHA-pinned fail-close delivery. Physical Windows desktop
rendering remains a separate buyer-side acceptance condition.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from data2web_desktop import inspect_owner_input,inspect_sheets,deliver_reviewed,ReviewedInput
from test_xlsx_fixtures import workbook_bytes
from verify_delivery import verify_zip
from package_portable import create_portable

ROOT=Path(__file__).resolve().parent

class DesktopController(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.source=self.root/"input.csv"
        self.source.write_text("id,title,category,notes\nA,Test A,X,Visible only locally\nB,Test B,Y,Also local\n",encoding="utf-8")
        self.destination=self.root/"new-customer"
        self.mapping={"id":"id","title":"title","category":"category"}
        self.review=inspect_owner_input(self.source)

    def deliver(self,**opts):
        args={"owner_has_rights":True,"plaintext_ack":True,
              "privacy_classification":"NO_PERSONAL_DATA_REVIEWED",
              "name":"Local customer app","theme":"office"}
        args.update(opts)
        return deliver_reviewed(self.review,self.destination,self.mapping,**args)

    def test_inspect_no_values_leaked_and_sha_preserved(self):
        self.assertIsInstance(self.review,ReviewedInput)
        self.assertEqual(self.review.count,2)
        self.assertEqual(self.review.sha256,hashlib.sha256(self.source.read_bytes()).hexdigest())
        payload=json.dumps(self.review.profile,ensure_ascii=False)
        self.assertNotIn("Visible only locally",payload)
        self.assertNotIn("Also local",payload)

    def test_owner_delivery_stays_local_and_verified(self):
        receipt=self.deliver()
        self.assertTrue(receipt["delivery_folder_created"])
        self.assertTrue(verify_zip(self.destination/"delivery.zip")["verified"])
        self.assertTrue((self.destination/"receipt.json").exists())
        self.assertEqual(receipt["rows"],2)

    def test_rights_explicit_acknowledgement_is_required(self):
        for opts in ({"owner_has_rights":False},{"plaintext_ack":False},
                     {"privacy_classification":""},{"privacy_classification":"AUTOMATED_PASS"}):
            with self.subTest(opts=opts):
                with self.assertRaises(ValueError):self.deliver(**opts)
                self.assertFalse(self.destination.exists())

    def test_exact_mapping_must_be_approved(self):
        for mapping in ({"id":"id","title":"title"}, {"id":"id","title":"id","category":"category"},
                        {"id":"id","title":"unknown","category":"category"}):
            with self.subTest(mapping=mapping):
                with self.assertRaises(ValueError):deliver_reviewed(self.review,self.destination,mapping,
                       owner_has_rights=True,plaintext_ack=True,
                       privacy_classification="NO_PERSONAL_DATA_REVIEWED")
                self.assertFalse(self.destination.exists())

    def test_source_changed_after_preview_hold(self):
        self.source.write_text("id,title,category,notes\nA,Changed,X,New\n",encoding="utf-8")
        with self.assertRaises(ValueError):self.deliver()
        self.assertFalse(self.destination.exists())

    def test_second_delivery_refused_without_overwrite(self):
        self.deliver()
        before=(self.destination/"delivery.zip").read_bytes()
        with self.assertRaises((FileExistsError,ValueError)):self.deliver()
        self.assertEqual((self.destination/"delivery.zip").read_bytes(),before)

    def test_review_is_immutable(self):
        from dataclasses import FrozenInstanceError
        with self.assertRaises(FrozenInstanceError):
            self.review.sha256="0"*64

    def test_xlsx_sheet_name_explicit_and_inspect(self):
        source=self.root/"workbook.xlsx"
        source.write_bytes(workbook_bytes())
        self.assertEqual(inspect_sheets(source),["Inventory"])
        with self.assertRaises(ValueError):inspect_owner_input(source)
        review=inspect_owner_input(source,sheet="Inventory")
        self.assertEqual(review.sheet,"Inventory")
        self.assertEqual(review.count,2)
        receipt=deliver_reviewed(review,self.destination,self.mapping,
                       owner_has_rights=True,plaintext_ack=True,
                       privacy_classification="OWNER_APPROVED_LOCAL_ONLY")
        self.assertTrue(verify_zip(self.destination/"delivery.zip")["verified"])
        self.assertEqual(receipt["sheet"],"Inventory")

    def test_xlsx_hidden_sheet_not_listed(self):
        source=self.root/"workbook.xlsx"
        source.write_bytes(workbook_bytes(hidden=True))
        self.assertEqual(inspect_sheets(source),[])
        with self.assertRaises(ValueError):inspect_owner_input(source,sheet="Inventory")

    def test_xlsx_workbook_changed_after_review_hold(self):
        source=self.root/"workbook.xlsx"
        source.write_bytes(workbook_bytes())
        review=inspect_owner_input(source,sheet="Inventory")
        source.write_bytes(workbook_bytes(sheets={"Inventory":[
            ["id","title","category","amount"],
            ["CHANGED-1","변경한 상품","상품",999]
        ]}))
        with self.assertRaises(ValueError):
            deliver_reviewed(review,self.destination,self.mapping,
                        owner_has_rights=True,plaintext_ack=True,
                        privacy_classification="NO_PERSONAL_DATA_REVIEWED")
        self.assertFalse(self.destination.exists())

    def test_portable_contains_gui_controller_but_no_auto_open(self):
        packed=self.root/"tool.pyz"
        create_portable(packed)
        from zipfile import ZipFile
        with ZipFile(packed) as archive:
            self.assertIn("data2web_desktop.py",archive.namelist())
        # --help never attempts to create Tk root
        p=subprocess.run([sys.executable,str(packed),"--help"],text=True,
                         encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn("desktop",p.stdout)

if __name__=="__main__":
    unittest.main()
