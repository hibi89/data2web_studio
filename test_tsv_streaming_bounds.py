"""Bounded TSV importer: stop at approved limits without accepting ragged rows."""
from __future__ import annotations

import unittest

from data2web_tabular import MAX_ROWS, parse_tsv


class TsvStreamingBoundedTests(unittest.TestCase):
    def test_explicit_trailing_tab_is_a_valid_empty_field(self):
        fields, rows = parse_tsv(b"id\ttitle\tcategory\nA\tAlpha\t\n")
        self.assertEqual(fields, ["id", "title", "category"])
        self.assertEqual(rows, [{"id": "A", "title": "Alpha", "category": ""}])

    def test_short_record_rejected(self):
        with self.assertRaisesRegex(ValueError, "inconsistent column count"):
            parse_tsv(b"id\ttitle\tcategory\nA\tAlpha\n")

    def test_csv_style_multiline_quoted_tsv_supported(self):
        columns, rows = parse_tsv(
            b'id\ttitle\tcategory\nA\t"Line one\nLine two"\tBlue\n'
        )
        self.assertEqual(columns, ["id", "title", "category"])
        self.assertEqual(rows[0]["title"], "Line one\nLine two")

    def test_exact_limit_accepted(self):
        raw = b"id\ttitle\tcategory\n" + b"X\tSample\tA\n" * MAX_ROWS
        fields, rows = parse_tsv(raw)
        self.assertEqual(len(rows), MAX_ROWS)
        self.assertEqual(fields[0], "id")

    def test_limit_plus_one_rejected(self):
        raw = b"id\ttitle\tcategory\n" + b"X\tSample\tA\n" * (MAX_ROWS + 1)
        with self.assertRaisesRegex(ValueError, "TSV row count limit"):
            parse_tsv(raw)

    def test_extra_field_rejected(self):
        with self.assertRaisesRegex(ValueError, "inconsistent column count"):
            parse_tsv(b"id\ttitle\tcategory\nA\tAlpha\tBlue\textra\n")


if __name__ == "__main__":
    unittest.main()
