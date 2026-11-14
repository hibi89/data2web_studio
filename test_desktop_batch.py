"""Real local backend multi-source controller regression, no customer data."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import unittest

from data2web_desktop import inspect_owner_batch, deliver_reviewed_batch
from test_xlsx_fixtures import workbook_bytes
from verify_customer_folder import verify_customer_folder


class BatchOwnerWorkflow(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(prefix="data2web-owner-batch-")
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.a=self.root/"a.csv"
        self.b=self.root/"b.tsv"
        self.a.write_text("id,title,category,amount\nA1,One,X,2\nA2,Two,Y,3\n",encoding="utf-8")
        self.b.write_text("id\ttitle\tcategory\tamount\nB1\tThree\tZ\t4\n",encoding="utf-8")
        self.dest=self.root/"new-customer"
        self.mapping={"id":"id","title":"title","category":"category"}

    def reviews(self):
        return inspect_owner_batch([self.a,self.b])

    def deliver(self,reviews=None,**overrides):
        opts={
            "owner_has_rights":True,"plaintext_ack":True,
            "privacy_classification":"NO_PERSONAL_DATA_REVIEWED",
            "name":"Synthetic batch","theme":"inventory",
        }
        opts.update(overrides)
        return deliver_reviewed_batch(self.reviews() if reviews is None else reviews,
                                      self.dest,self.mapping,**opts)

    def test_csv_tsv_two_sources_create_verified_folder_without_temp_manifest(self):
        original={p.name for p in self.root.iterdir()}
        reviewed=self.reviews()
        self.assertEqual(len(reviewed),2)
        self.assertEqual(sum(r.count for r in reviewed),3)
        result=self.deliver(reviewed)
        checked=verify_customer_folder(self.dest)
        self.assertTrue(checked["verified"])
        self.assertEqual(checked["rows"],3)
        self.assertEqual(result["source_receipts"][1]["kind"],"tsv")
        self.assertFalse(result["sale_approved"])
        self.assertEqual({p.name for p in self.root.iterdir()},original|{"new-customer"})
        self.assertFalse(any(p.suffix==".json" for p in self.root.iterdir() if p.is_file()))

    def test_csv_xlsx_explicit_sheet_and_receipt(self):
        self.b.unlink()
        self.b=self.root/"b.xlsx"
        self.b.write_bytes(workbook_bytes(sheets={"Inventory":[
            ["id","title","category","amount"],["B1","Excel", "Z", 4],
        ]}))
        with self.assertRaises(ValueError):
            inspect_owner_batch([self.a,self.b])
        reviews=inspect_owner_batch([self.a,self.b],
                options=[{},{"sheet":"Inventory","header_row":1}])
        self.assertEqual(reviews[1].sheet,"Inventory")
        result=self.deliver(reviews)
        self.assertEqual(result["source_receipts"][1]["sheet"],"Inventory")
        self.assertTrue(verify_customer_folder(self.dest)["verified"])

    def test_mutated_original_is_rejected_before_folder(self):
        reviewed=self.reviews()
        self.b.write_text("id\ttitle\tcategory\tamount\nB1\tModified\tZ\t900\n",encoding="utf-8")
        with self.assertRaises(ValueError):
            self.deliver(reviewed)
        self.assertFalse(self.dest.exists())

    def test_duplicate_ids_across_sources_are_rejected_before_folder(self):
        self.b.write_text("id\ttitle\tcategory\tamount\nA1\tCollision\tZ\t4\n",encoding="utf-8")
        reviewed=self.reviews()
        with self.assertRaises(ValueError):
            self.deliver(reviewed)
        self.assertFalse(self.dest.exists())

    def test_non_matching_column_order_is_rejected_during_review(self):
        self.b.write_text("title\tid\tcategory\tamount\nBad\tB1\tZ\t4\n",encoding="utf-8")
        with self.assertRaises(ValueError):
            self.reviews()

    def test_different_input_directories_refused(self):
        sub=self.root/"sub"
        sub.mkdir()
        other=sub/"b.tsv"
        other.write_bytes(self.b.read_bytes())
        with self.assertRaises(ValueError):
            inspect_owner_batch([self.a,other])

    def test_repeated_input_refused(self):
        with self.assertRaises(ValueError):
            inspect_owner_batch([self.a,self.a])

    def test_batch_size_requires_two_to_ten(self):
        for chosen in ([],[self.a],[self.a]*11):
            with self.subTest(length=len(chosen)):
                with self.assertRaises(ValueError):
                    inspect_owner_batch(chosen)

    def test_false_or_missing_owner_consent_refuses_before_folder(self):
        reviewed=self.reviews()
        for opts in ({"owner_has_rights":False},
                     {"plaintext_ack":False},
                     {"privacy_classification":""},
                     {"privacy_classification":"AUTO_APPROVED"}):
            with self.subTest(opts=opts):
                with self.assertRaises(ValueError):
                    self.deliver(reviewed,**opts)
                self.assertFalse(self.dest.exists())

    def test_bad_mapping_refuses_before_folder(self):
        reviewed=self.reviews()
        self.mapping={"id":"id","title":"id","category":"category"}
        with self.assertRaises(ValueError):
            self.deliver(reviewed)
        self.assertFalse(self.dest.exists())

    def test_existing_customer_folder_remains_untouched(self):
        self.dest.mkdir()
        old=self.dest/"keep.txt"
        old.write_text("PRESERVE",encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.deliver()
        self.assertEqual(old.read_text("utf-8"),"PRESERVE")
        self.assertEqual({p.name for p in self.dest.iterdir()},{"keep.txt"})

    def test_non_excel_cannot_claim_cached_formulas(self):
        with self.assertRaises(ValueError):
            inspect_owner_batch([self.a,self.b],
                                options=[{},{"allow_cached_formulas":True}])


if __name__=="__main__":
    unittest.main()
