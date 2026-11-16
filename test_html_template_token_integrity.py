"""Regression: reserved HTML template tokens must remain literal user data."""
import base64
import hashlib
import json
import re
import unittest

from data2web_web import render_html


class HtmlTemplateTokenIntegrityTests(unittest.TestCase):
    def test_reserved_tokens_preserved_in_title_headers_and_cells(self):
        headers = ["id", "title", "category", "notes__SCRIPT_HASH__"]
        original = {
            "id": "item-1",
            "title": "A __SCRIPT_HASH__ record",
            "category": "C __PAYLOAD__",
            "notes__SCRIPT_HASH__": "literal __SCRIPT_HASH__ __PAYLOAD__ __TITLE__ <script> &"
        }
        page = render_html(
            headers, [original], ["id", "title", "category"],
            "a" * 64, name="Studio __SCRIPT_HASH__ __PAYLOAD__"
        )
        match = re.search(
            r'<script type="application/json" id="dataset">(.*?)</script>',
            page, flags=re.S
        )
        self.assertIsNotNone(match)
        data = json.loads(match.group(1))
        self.assertEqual(data["columns"], headers)
        self.assertEqual(data["rows"], [original])
        self.assertIn("<h1>Studio __SCRIPT_HASH__ __PAYLOAD__</h1>", page)
        self.assertIn("<title>Studio __SCRIPT_HASH__ __PAYLOAD__ · DATA2WEB</title>", page)

    def test_static_script_hash_csp_remains_exact(self):
        page = render_html(
            ["id", "title", "category"],
            [{"id": "1", "title": "__SCRIPT_HASH__", "category": "A"}],
            ["id", "title", "category"], "b" * 64
        )
        script = page.rsplit("<script>", 1)[1].split("</script>", 1)[0]
        digest = base64.b64encode(
            hashlib.sha256(script.encode("utf-8")).digest()
        ).decode("ascii")
        self.assertIn("script-src 'sha256-" + digest + "'", page)
        self.assertEqual(page.count("script-src 'sha256-"), 1)


if __name__ == "__main__":
    unittest.main()
