"""CSP hash regressions for the exact offline script, not an external audit."""
import base64
import hashlib
import re
import unittest
from data2web_web import TEMPLATE, render_html
import verify_delivery

SCRIPT = re.compile(r"<script>(.*?)</script>", re.DOTALL | re.IGNORECASE)
POLICY = re.compile(r"script-src 'sha256-([^']+)'")

def sample(title="synthetic"):
    return render_html(["id", "title", "category"],
                       [{"id": "S1", "title": title, "category": "A"}],
                       ["id", "title", "category"], "0" * 64)

class ScriptHashPolicy(unittest.TestCase):
    def test_unsafe_inline_script_forbidden(self):
        page = sample()
        self.assertIn("connect-src 'none'", page)
        self.assertNotIn("script-src 'unsafe-inline'", page)
        self.assertNotIn("__SCRIPT_HASH__", page)
        self.assertEqual(page.count("script-src 'sha256-"), 1)

    def test_hash_is_exact_static_script(self):
        page = sample()
        script = SCRIPT.search(page).group(1)
        digest = base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii")
        self.assertEqual(POLICY.search(page).group(1), digest)
        self.assertEqual(SCRIPT.findall(page), [script])
        self.assertEqual(script, TEMPLATE.split("<script>", 1)[1].split("</script>", 1)[0])

    def test_injected_script_changes_hash(self):
        page = sample()
        script = SCRIPT.search(page).group(1)
        rogue = base64.b64encode(hashlib.sha256((script+"\nwindow.UNAPPROVED=1;").encode()).digest()).decode()
        self.assertNotEqual(POLICY.search(page).group(1), rogue)

    def test_script_ending_payload_is_escaped_case_insensitively(self):
        standard = sample()
        for payload in (
            "</script><script>alert('x')</script>",
            "</SCRIPT><SCRIPT>window.XSS_PROBE=1</SCRIPT>",
        ):
            with self.subTest(payload=payload):
                adversarial = sample(payload)
                self.assertEqual(POLICY.search(standard).group(1),
                                 POLICY.search(adversarial).group(1))
                self.assertIn(r"\u003c", adversarial)
                self.assertIsNone(re.search(
                    r"</script\s*>\s*<script\b", adversarial, re.IGNORECASE))
                verify_delivery._validate_offline_html_csp(
                    adversarial.encode("utf-8"))

    def test_csp_verifier_recognizes_uppercase_static_script_tags(self):
        page = sample()
        uppercase = page.replace("<script>", "<SCRIPT>")
        closing = uppercase.rfind("</script>")
        self.assertGreaterEqual(closing, 0)
        uppercase = (uppercase[:closing] + "</SCRIPT>" +
                     uppercase[closing + len("</script>"):])
        verify_delivery._validate_offline_html_csp(uppercase.encode("utf-8"))

    def test_csp_verifier_rejects_extra_uppercase_executable_script(self):
        page = sample().replace(
            "</body>", "<SCRIPT>window.UNAPPROVED=1</SCRIPT></body>")
        with self.assertRaises(ValueError):
            verify_delivery._validate_offline_html_csp(page.encode("utf-8"))

    def test_different_user_data_uses_same_approved_script(self):
        for title in ("테스트", "<b>HTML</b>", "=1+1", "&quot;"):
            self.assertEqual(POLICY.search(sample(title)).group(1),
                             POLICY.search(sample()).group(1))

    def test_html_has_no_inline_event_handler_attributes(self):
        self.assertIsNone(re.search(
            r"<[a-z][^>]*\s(?:onclick|onerror|onload|onchange)=", sample(), re.I))

if __name__ == "__main__":
    unittest.main()
