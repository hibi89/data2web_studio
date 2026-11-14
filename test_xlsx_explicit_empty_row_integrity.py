"""R11: explicit XLSX empty values must not disappear during parsing.

Only synthetic OOXML fixtures. No real customer files or network access.
"""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from data2web import build, read_table
from test_xlsx_fixtures import workbook_bytes


class XlsxExplicitEmptyRowIntegrity(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.source = self.root / "synthetic.xlsx"
        self.output = self.root / "output.html"

    def make_sheet(self, records):
        raw = workbook_bytes(sheets={"Inventory": [
            ["id", "title", "category"], *records
        ]})
        self.source.write_bytes(raw)
        return raw

    def test_explicit_empty_row_is_not_silently_dropped(self):
        self.make_sheet([["A1", "Safe", "Blue"], ["", "", ""]])
        fields, rows, _ = read_table(self.source, sheet="Inventory")
        self.assertEqual(fields, ["id", "title", "category"])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1], {"id": "", "title": "", "category": ""})

    def test_structurally_blank_row_without_cells_is_skipped(self):
        self.make_sheet([["A1", "Safe", "Blue"], [None, None, None]])
        _, rows, _ = read_table(self.source, sheet="Inventory")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "A1")

    def test_explicit_empty_between_valid_rows_cannot_be_hidden(self):
        self.make_sheet([
            ["A1", "First", "Blue"], ["", "", ""], ["A2", "Second", "Red"]
        ])
        _, rows, _ = read_table(self.source, sheet="Inventory")
        self.assertEqual([r["id"] for r in rows], ["A1", "", "A2"])

    def test_delivery_holds_on_explicit_empty_id_without_creating_html(self):
        raw = self.make_sheet([["A1", "Safe", "Blue"], ["", "", ""]])
        with self.assertRaisesRegex(ValueError, "Missing or duplicate IDs"):
            build(
                self.source, self.output,
                "id", "title", "category",
                approved=True,
                expected_sha256=hashlib.sha256(raw).hexdigest(),
                sheet="Inventory",
            )
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
