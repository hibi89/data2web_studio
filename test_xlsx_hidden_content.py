"""Regression: hidden Excel values must never enter an offline HTML without review.

These are fictional OOXML workbooks; no customer material or network access.
"""
import hashlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from data2web import build
from data2web_tabular import parse_xlsx
from test_xlsx_fixtures import workbook_bytes, X


def worksheet_variant(kind):
    source = workbook_bytes()
    with zipfile.ZipFile(io.BytesIO(source)) as archive:
        entries = [(item.filename, archive.read(item)) for item in archive.infolist()]
    result = io.BytesIO()
    part = "xl/worksheets/sheet1.xml"
    ns = "{" + X + "}"
    with zipfile.ZipFile(result, "w", zipfile.ZIP_DEFLATED) as output:
        for name, raw in entries:
            if name == part:
                root = ET.fromstring(raw)
                data = root.find(ns + "sheetData")
                if kind == "hidden-row":
                    data.findall(ns + "row")[1].set("hidden", "1")
                elif kind == "hidden-header":
                    data.findall(ns + "row")[0].set("hidden", "true")
                elif kind == "hidden-column":
                    cols = ET.Element(ns + "cols")
                    ET.SubElement(cols, ns + "col", {
                        "min": "2", "max": "2", "width": "10", "hidden": "1"
                    })
                    root.insert(list(root).index(data), cols)
                elif kind == "zero-height":
                    root.insert(0, ET.Element(ns + "sheetFormatPr", {"zeroHeight": "1"}))
                elif kind == "visible-flags":
                    data.findall(ns + "row")[1].set("hidden", "false")
                    cols = ET.Element(ns + "cols")
                    ET.SubElement(cols, ns + "col", {
                        "min": "2", "max": "2", "width": "10", "hidden": "0"
                    })
                    root.insert(list(root).index(data), cols)
                else:
                    raise ValueError("unsupported test variant")
                raw = ET.tostring(root, encoding="utf-8")
            output.writestr(name, raw)
    return result.getvalue()


class HiddenXlsxPublicationGate(unittest.TestCase):
    def test_hidden_rows_and_columns_require_visible_source_reapproval(self):
        for variant in ("hidden-row", "hidden-header", "hidden-column", "zero-height"):
            with self.subTest(variant=variant):
                workbook = worksheet_variant(variant)
                with self.assertRaisesRegex(ValueError, "Hidden XLSX"):
                    parse_xlsx(workbook, sheet="Inventory")
                with tempfile.TemporaryDirectory() as folder:
                    src = Path(folder) / "synthetic.xlsx"
                    out = Path(folder) / "offline.html"
                    src.write_bytes(workbook)
                    with self.assertRaisesRegex(ValueError, "Hidden XLSX"):
                        build(src, out, "id", "title", "category", True,
                              expected_sha256=hashlib.sha256(workbook).hexdigest(),
                              sheet="Inventory")
                    self.assertFalse(out.exists())

    def test_explicitly_visible_rows_and_columns_stay_compatible(self):
        cols, rows, sheet = parse_xlsx(worksheet_variant("visible-flags"), sheet="Inventory")
        self.assertEqual(sheet, "Inventory")
        self.assertEqual(cols, ["id", "title", "category", "amount"])
        self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
