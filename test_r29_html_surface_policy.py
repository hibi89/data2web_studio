"""R29 passive HTML surface guard: canonical generator and adversarial markup.

High-owned tests; no real browser navigation or external network operation.
"""
from __future__ import annotations

import unittest

from data2web_web import render_html
from r29_html_surface_policy import assert_passive_offline_html_markup


def pristine_html():
    return render_html(
        ["id", "title", "category"],
        [{"id": "A1",
          "title": "</script><iframe src=https://invalid.example/a></iframe>",
          "category": "=HYPERLINK(\"https://invalid.example\",\"x\")"}],
        ["id", "title", "category"],
        "a" * 64,
    ).encode("utf-8")


class PassiveHTMLSurfacePolicy(unittest.TestCase):
    def setUp(self):
        self.original = pristine_html()

    def test_valid_generated_html_passes_without_certification(self):
        result = assert_passive_offline_html_markup(self.original)
        self.assertTrue(result["passive_template_surface_verified"])
        self.assertFalse(result["source_authenticity_verified"])
        self.assertFalse(result["independent_security_audit_completed"])
        self.assertFalse(result["commercial_release_approved"])

    def assert_unsafe(self, changed):
        self.assertNotEqual(changed, self.original)
        with self.assertRaises(ValueError):
            assert_passive_offline_html_markup(changed)

    def test_meta_refresh_inserted_before_head_close(self):
        self.assert_unsafe(self.original.replace(
            b"</head>",
            b'<meta http-equiv="refresh" content="0;url=https://invalid.example/">'
            + b"</head>", 1))

    def test_viewport_replaced_with_meta_refresh_without_changing_tag_count(self):
        self.assert_unsafe(self.original.replace(
            b'name="viewport" content="width=device-width,initial-scale=1"',
            b'http-equiv="refresh" content="0;url=https://invalid.example/"',
            1))

    def test_unapproved_navigation_resource_and_exec_elements(self):
        for payload in (
            b'<iframe src="https://invalid.example/"></iframe>',
            b'<link rel="stylesheet" href="https://invalid.example/x.css">',
            b'<form action="https://invalid.example/"></form>',
            b'<base href="https://invalid.example/">',
            b'<svg onload="evil()"></svg>',
            b'<script src="https://invalid.example/x.js"></script>',
        ):
            with self.subTest(payload=payload):
                self.assert_unsafe(self.original.replace(
                    b"</head>", payload + b"</head>", 1))

    def test_event_attribute_on_existing_element_rejected(self):
        self.assert_unsafe(self.original.replace(
            b"<main>", b'<main onclick="evil()">', 1))

    def test_html_tags_cannot_be_rearranged_or_duplicated(self):
        self.assert_unsafe(self.original.replace(
            b"</main>", b"</section>", 1))
        self.assert_unsafe(self.original.replace(
            b"<main>", b"<main><div></div>", 1))

    def test_invalid_markup_encoding_and_type_rejected(self):
        for bad in (b"", b"not html", b"\\xff", "not-bytes", None):
            with self.subTest(bad=repr(bad)), self.assertRaises(ValueError):
                assert_passive_offline_html_markup(bad)

    def test_unexpected_html_comment_rejected(self):
        self.assert_unsafe(self.original.replace(
            b"</head>", b"<!-- unexpected -->" + b"</head>", 1))


if __name__ == "__main__":
    unittest.main()
