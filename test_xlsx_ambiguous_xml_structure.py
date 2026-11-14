"""Fail-closed OOXML: duplicate structured data must not be ignored.

Fixtures are fully synthetic and never include customer documents.
"""
import copy
import hashlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from data2web import build, read_table
from test_xlsx_fixtures import workbook_bytes

X = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SHEET = "xl/worksheets/sheet1.xml"
BOOK = "xl/workbook.xml"


class XlsxAmbiguousXmlStructure(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / "ambiguous.xlsx"
        self.output = self.root / "should-not-exist.html"

    def mutate(self, filename, transform):
        original = workbook_bytes()
        destination = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(original)) as z, zipfile.ZipFile(
            destination, "w", compression=zipfile.ZIP_DEFLATED
        ) as output:
            for info in z.infolist():
                content = z.read(info.filename)
                if info.filename == filename:
                    root = ET.fromstring(content)
                    transform(root)
                    content = ET.tostring(root, encoding="utf-8")
                output.writestr(info, content)
        self.source.write_bytes(destination.getvalue())
        return hashlib.sha256(destination.getvalue()).hexdigest()

    def assert_hold(self, phrase):
        with self.assertRaisesRegex(ValueError, phrase):
            read_table(self.source, sheet="Inventory")

    def test_duplicate_sheetdata_does_not_silently_disappear(self):
        def poison(root):
            data = root.find(X + "sheetData")
            root.append(copy.deepcopy(data))
        self.mutate(SHEET, poison)
        self.assert_hold("worksheet structure")

    def test_duplicate_workbook_sheet_list_is_rejected(self):
        def poison(root):
            root.append(copy.deepcopy(root.find(X + "sheets")))
        self.mutate(BOOK, poison)
        self.assert_hold("sheet list")

    def test_duplicate_sheetformat_hidden_override_is_rejected(self):
        def poison(root):
            root.insert(0, ET.Element(X + "sheetFormatPr", {"zeroHeight": "0"}))
            root.append(ET.Element(X + "sheetFormatPr", {"zeroHeight": "1"}))
        self.mutate(SHEET, poison)
        self.assert_hold("worksheet structure")

    def test_duplicate_column_layout_hidden_override_is_rejected(self):
        def poison(root):
            a = ET.SubElement(root, X + "cols")
            ET.SubElement(a, X + "col", {"min": "1", "max": "1", "hidden": "0"})
            b = ET.SubElement(root, X + "cols")
            ET.SubElement(b, X + "col", {"min": "1", "max": "1", "hidden": "1"})
        self.mutate(SHEET, poison)
        self.assert_hold("worksheet structure")

    def test_duplicate_numeric_cache_is_rejected(self):
        def poison(root):
            row = root.find(X + "sheetData").findall(X + "row")[1]
            cell = next(c for c in row.findall(X + "c") if c.get("r") == "D2")
            ET.SubElement(cell, X + "v").text = "999999"
        self.mutate(SHEET, poison)
        self.assert_hold("Duplicate XLSX cell payload")

    def test_duplicate_inline_string_is_rejected(self):
        def poison(root):
            row = root.find(X + "sheetData").findall(X + "row")[1]
            cell = next(c for c in row.findall(X + "c") if c.get("r") == "A2")
            ET.SubElement(ET.SubElement(cell, X + "is"), X + "t").text = "hidden-id"
        self.mutate(SHEET, poison)
        self.assert_hold("Duplicate XLSX cell payload")

    def test_inline_string_with_unreviewed_numeric_cache_is_rejected(self):
        def poison(root):
            row = root.find(X + "sheetData").findall(X + "row")[1]
            cell = next(c for c in row.findall(X + "c") if c.get("r") == "A2")
            ET.SubElement(cell, X + "v").text = "123"
        self.mutate(SHEET, poison)
        self.assert_hold("Ambiguous XLSX inline cell payload")

    def test_invalid_workbook_does_not_publish_html(self):
        def poison(root):
            root.append(copy.deepcopy(root.find(X + "sheetData")))
        source_sha = self.mutate(SHEET, poison)
        with self.assertRaisesRegex(ValueError, "worksheet structure"):
            build(
                self.source, self.output, "id", "title", "category",
                approved=True, expected_sha256=source_sha, sheet="Inventory"
            )
        self.assertFalse(self.output.exists())

    def test_unmodified_workbook_remains_compatible(self):
        self.source.write_bytes(workbook_bytes())
        columns, rows, _ = read_table(self.source, sheet="Inventory")
        self.assertEqual(columns, ["id", "title", "category", "amount"])
        self.assertEqual([row["id"] for row in rows], ["A-01", "A-02"])


if __name__ == "__main__":
    unittest.main()
