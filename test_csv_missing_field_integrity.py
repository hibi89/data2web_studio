"""CSV row-shape integrity: omissions are not explicit empty values."""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from data2web import read_table
from data2web_single import deliver_single


class CsvMissingFieldIntegrityTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.source = self.root / "synthetic.csv"

    def _write(self, content):
        self.source.write_text(content, encoding="utf-8")
        return self.source

    def test_explicit_trailing_comma_preserves_intentionally_empty_cell(self):
        fields, rows, _ = read_table(self._write("id,title,category\nA,Alpha,\n"))
        self.assertEqual(fields, ["id", "title", "category"])
        self.assertEqual(rows, [{"id": "A", "title": "Alpha", "category": ""}])

    def test_explicit_quoted_empty_preserves_cell(self):
        _, rows, _ = read_table(self._write('id,title,category\nA,Alpha,""\n'))
        self.assertEqual(rows[0]["category"], "")

    def test_physically_blank_lines_still_ignored(self):
        _, rows, _ = read_table(
            self._write("id,title,category\n\nA,Alpha,Blue\n\n")
        )
        self.assertEqual(len(rows), 1)

    def test_missing_trailing_delimiter_rejected(self):
        self._write("id,title,category\nA,Alpha\n")
        with self.assertRaisesRegex(ValueError, "missing a required field delimiter"):
            read_table(self.source)

    def test_missing_unmapped_column_rejected(self):
        self._write("id,title,category,notes\nA,Alpha,Blue\n")
        with self.assertRaisesRegex(ValueError, "missing a required field delimiter"):
            read_table(self.source)

    def test_csv_row_count_is_rejected_at_bounded_limit(self):
        self._write(
            "id,title,category\n" +
            "".join(f"{n},Sample{n},A\n" for n in range(10001))
        )
        with self.assertRaisesRegex(ValueError, "CSV row count limit"):
            read_table(self.source)

    def test_csv_excess_columns_rejected_before_reading_records(self):
        columns = ["id", "title", "category"] + [f"extra{i}" for i in range(38)]
        self._write(",".join(columns) + "\n")
        with self.assertRaisesRegex(ValueError, "CSV column count limit"):
            read_table(self.source)

    def test_invalid_row_cannot_create_single_delivery_directory(self):
        content = "id,title,category\nA,Alpha\n"
        self._write(content)
        dest = self.root / "should-not-exist"
        with self.assertRaisesRegex(ValueError, "missing a required field delimiter"):
            deliver_single(
                self.source, dest,
                expected_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),
                id_column="id", title_column="title", category_column="category",
                confirm="APPROVE", ack_plaintext=True,
                privacy_classification="NO_PERSONAL_DATA_REVIEWED"
            )
        self.assertFalse(dest.exists())
        self.assertEqual(self.source.read_text(encoding="utf-8"), content)


if __name__ == "__main__":
    unittest.main()
