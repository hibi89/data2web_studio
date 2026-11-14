"""R11: explicitly materialized XLSX cells beyond approved headers must HOLD.

Synthetic OOXML only; formatted-but-empty cells are not extra data.
"""
from __future__ import annotations

import hashlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from data2web import build, read_table
from test_xlsx_fixtures import workbook_bytes

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


class XlsxExtraColumnIntegrity(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.source = self.root / "source.xlsx"
        self.html = self.root / "result.html"

    def make_extra(self, kind):
        base = workbook_bytes(sheets={
            "Inventory": [["id", "title", "category"], ["A1", "Item", "Blue"]]
        })
        output = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(base)) as original, zipfile.ZipFile(
            output, "w", compression=zipfile.ZIP_DEFLATED
        ) as target:
            for item in original.infolist():
                raw = original.read(item.filename)
                if item.filename == "xl/worksheets/sheet1.xml":
                    root = ET.fromstring(raw)
                    data = root.find(NS + "sheetData")
                    row = next(x for x in data.findall(NS + "row") if x.get("r") == "2")
                    cell = ET.SubElement(row, NS + "c", {"r": "D2"})
                    if kind in ("inline-empty", "inline-text"):
                        cell.set("t", "inlineStr")
                        inside = ET.SubElement(cell, NS + "is")
                        ET.SubElement(inside, NS + "t").text = (
                            "" if kind == "inline-empty" else "out-of-schema"
                        )
                    elif kind == "cached-empty":
                        ET.SubElement(cell, NS + "v")
                    elif kind == "styled-empty":
                        cell.set("s", "1")
                    else:
                        raise AssertionError(kind)
                    raw = ET.tostring(root, encoding="utf-8")
                target.writestr(item, raw)
        self.source.write_bytes(output.getvalue())
        return hashlib.sha256(output.getvalue()).hexdigest()

    def test_explicit_empty_inline_value_outside_headers_holds(self):
        self.make_extra("inline-empty")
        with self.assertRaisesRegex(ValueError, "Data extends beyond approved headers"):
            read_table(self.source, sheet="Inventory")

    def test_explicit_empty_cached_value_outside_headers_holds(self):
        self.make_extra("cached-empty")
        with self.assertRaisesRegex(ValueError, "Data extends beyond approved headers"):
            read_table(self.source, sheet="Inventory")

    def test_formatting_only_outside_headers_is_not_customer_data(self):
        self.make_extra("styled-empty")
        columns, rows, _ = read_table(self.source, sheet="Inventory")
        self.assertEqual(columns, ["id", "title", "category"])
        self.assertEqual(rows, [{"id": "A1", "title": "Item", "category": "Blue"}])

    def test_nonempty_extra_value_remains_rejected(self):
        self.make_extra("inline-text")
        with self.assertRaisesRegex(ValueError, "Data extends beyond approved headers"):
            read_table(self.source, sheet="Inventory")

    def test_invalid_extra_cell_cannot_create_html(self):
        sha = self.make_extra("inline-empty")
        with self.assertRaisesRegex(ValueError, "Data extends beyond approved headers"):
            build(
                self.source, self.html, "id", "title", "category",
                approved=True, expected_sha256=sha, sheet="Inventory",
            )
        self.assertFalse(self.html.exists())


if __name__ == "__main__":
    unittest.main()
