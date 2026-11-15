"""R29 passive HTML surface guard: canonical generator and adversarial markup.

High-owned tests; no real browser navigation or external network operation.
"""
from __future__ import annotations

import unittest
import base64
import hashlib
import re

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
            b"<main>", b"<main><header></header>", 1))

    def test_browser_saved_dynamic_table_options_and_chart_are_accepted(self):
        # The runtime saves the *rendered* DOM, not just the initial template.
        html = self.original.replace(
            b'<tbody id="body"></tbody>',
            b'<tbody id="body"><tr tabindex="0" aria-label="Synthetic">'
            b'<td>synthetic</td><td>&lt;/script&gt;</td></tr></tbody>', 1)
        # Add a passive chart row to the data-browser body, no navigation.
        chart = (b'<div class="chart-row"><span class="chart-key">A</span>'
                 b'<div class="bar-track"><div class="bar-fill" '
                 b'style="width: 25%;"></div></div>'
                 b'<span class="chart-value">1</span></div>')
        # Insert into chart container after its opening tag using a safe
        # regular expression; the container is present in the real template.
        html, n = re.subn(
            rb'(<div id="chart-bars"[^>]*>)', lambda m: m.group(1) + chart,
            html, count=1,
        )
        self.assertEqual(n, 1)
        html = html.replace(
            b'</select>',
            b'<option data-all="true" value="" selected="">All</option></select>',
            1,
        )
        html = html.replace(
            b'<button id="prev" type="button">',
            b'<button id="prev" type="button" disabled="">', 1,
        )
        html = html.replace(
            b'class="warning" hidden>',
            b'class="warning" hidden="">', 1,
        )
        result = assert_passive_offline_html_markup(html)
        self.assertTrue(result["passive_template_surface_verified"])

    def test_aggregated_chart_width_above_100_percent_stays_numeric_only(self):
        # Real CSSOM emits >100% when grouped remaining categories outrank
        # the largest individual category; max-width:100% caps drawing.
        html, n = re.subn(
            rb'(<div id="chart-bars"[^>]*>)',
            lambda m: m.group(1) +
                b'<div class="chart-row"><div class="bar-fill" '
                b'style="width: 257.143%;"></div></div>',
            self.original, count=1,
        )
        self.assertEqual(n, 1)
        self.assertTrue(
            assert_passive_offline_html_markup(html)[
                "passive_template_surface_verified"]
        )
        for forbidden in (
            b'width: -1%;',
            b'width: 1000001%;',
            b'width: inf%;',
            b'width: 257%; background:url(https://invalid.example/x);',
            b'width: calc(99% + 1px);',
        ):
            with self.subTest(unsafe=forbidden):
                self.assert_unsafe(html.replace(b'width: 257.143%;', forbidden, 1))

    def test_self_rehashed_script_and_css_mutations_are_still_rejected(self):
        original = self.original
        script = re.findall(rb"<script>(.*?)</script>", original, re.DOTALL)[0]
        mutated_script = script + b"window.EVIL_SYNTHETIC=1;"
        old_hash = base64.b64encode(hashlib.sha256(script).digest())
        new_hash = base64.b64encode(hashlib.sha256(mutated_script).digest())
        payload = original.replace(b"<script>" + script + b"</script>",
                                   b"<script>" + mutated_script + b"</script>", 1)
        payload = payload.replace(old_hash, new_hash, 1)
        self.assert_unsafe(payload)
        css = re.findall(rb"<style>(.*?)</style>", original, re.DOTALL)[0]
        self.assert_unsafe(original.replace(
            b"<style>" + css + b"</style>",
            b"<style>" + css + b"body{display:none}" + b"</style>", 1))

    def test_active_attribute_in_dynamic_table_rejected(self):
        self.assert_unsafe(self.original.replace(
            b'<tbody id="body"></tbody>',
            b'<tbody id="body"><tr onclick="evil()">'
            b'<td>A</td></tr></tbody>', 1))
        self.assert_unsafe(self.original.replace(
            b'<div id="chart-bars"',
            b'<div id="chart-bars" style="background:url(https://invalid.example/a)"',
            1))

    def test_fixed_id_shadowing_is_not_permitted_in_passive_dynamic_dom(self):
        base = self.original
        for mutation in (
            b'<div id="dataset">{"rows":[]}</div>',
            b'<div id="search">text</div>',
            b'<div id="unreviewed">text</div>',
            b'<span id="category">shadow</span>',
            b'<div id="dataset"></div><div id="dataset"></div>',
        ):
            with self.subTest(id_injection=mutation):
                self.assert_unsafe(base.replace(
                    b"</main>", mutation + b"</main>", 1))
        self.assert_unsafe(base.replace(
            b'<div id="chart-bars"', b'<div class="untrusted"', 1))

    def test_csp_meta_moved_into_body_is_rejected(self):
        meta = re.search(rb'<meta http-equiv="Content-Security-Policy"[^>]*>',
                         self.original)
        self.assertIsNotNone(meta)
        altered = self.original.replace(meta.group(), b"", 1).replace(
            b"<body><main>", b"<body>" + meta.group() + b"<main>", 1)
        self.assert_unsafe(altered)

    def test_executable_js_cannot_precede_body_controls(self):
        start = self.original.index(b"<script>")
        end = self.original.index(b"</script>", start) + len(b"</script>")
        script = self.original[start:end]
        altered = self.original.replace(script, b"", 1).replace(
            b"<body><main>", b"<body>" + script + b"<main>", 1)
        self.assert_unsafe(altered)

    def test_chart_inline_style_cannot_target_fixed_id(self):
        altered = self.original.replace(
            b'<div id="chart-bars" role="img"',
            b'<div id="chart-bars" class="bar-fill" style="width: 0%;" role="img"', 1)
        self.assert_unsafe(altered)

    def test_invalid_markup_encoding_and_type_rejected(self):
        for bad in (b"", b"not html", b"\\xff", "not-bytes", None):
            with self.subTest(bad=repr(bad)), self.assertRaises(ValueError):
                assert_passive_offline_html_markup(bad)

    def test_unexpected_html_comment_rejected(self):
        self.assert_unsafe(self.original.replace(
            b"</head>", b"<!-- unexpected -->" + b"</head>", 1))


if __name__ == "__main__":
    unittest.main()
