"""R29 standalone HTML passive-markup policy, independent of the renderer.

The approved DATA2WEB V1 offline template has a fixed tag/attribute surface.
This check is a defense-in-depth component; it is NOT proof of origin, signing,
data rights, or an external independent audit. All errors are redacted.
"""
from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser

# Fixed structure from the reviewed DATA2WEB_HTML_V1 source template.
# Do not derive this whitelist from the untrusted ZIP's HTML or from live
# generator source while validating a customer package.
EXPECTED_TAGS = {
    "html": 1, "head": 1, "meta": 3, "title": 1, "style": 1,
    "body": 1, "main": 1, "header": 1, "small": 6, "h1": 1,
    "p": 10, "section": 5, "div": 7, "span": 5, "strong": 3,
    "label": 6, "input": 3, "select": 3, "option": 2,
    "button": 5, "table": 1, "thead": 1, "tbody": 1,
    "nav": 1, "h2": 3, "pre": 1, "footer": 1, "script": 2,
}
ALLOWED_ATTRS = {
    "html": {"lang", "data-theme"},
    "meta": {"charset", "name", "content", "http-equiv"},
    "small": {"id", "class"},
    "p": {"id", "class", "aria-live", "role"},
    "section": {"class", "aria-label", "id"},
    "div": {"class", "id", "role", "aria-label"},
    "span": {"class", "id"},
    "strong": {"id"},
    "input": {"id", "type", "placeholder", "accept"},
    "select": {"id", "size", "aria-label"},
    "option": {"value"},
    "button": {"id", "type"},
    "table": {"aria-label"},
    "thead": {"id"},
    "tbody": {"id"},
    "nav": {"class", "aria-label"},
    "pre": {"id", "aria-live"},
    "script": {"type", "id"},
}
VOID_TAGS = {"meta", "input"}
THEMES = {"office", "cafe", "inventory"}


class _HTMLSurfaceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = Counter()
        self.stack = []
        self.metas = set()
        self.scripts = set()
        self.declaration_count = 0

    def handle_decl(self, decl):
        if decl.lower().strip() != "doctype html":
            raise ValueError("Unapproved document declaration")
        self.declaration_count += 1

    def unknown_decl(self, data):
        raise ValueError("Unknown document declaration")

    def handle_pi(self, data):
        raise ValueError("Processing instruction forbidden")

    def handle_comment(self, data):
        # The shipped HTML template uses no comments outside script/style
        # CDATA. Do not make exclusions by parsing untrusted comment content.
        raise ValueError("Unexpected HTML comment")

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def _start(self, tag, attrs):
        if tag not in EXPECTED_TAGS:
            raise ValueError("Unapproved HTML element")
        self.tags[tag] += 1
        if self.tags[tag] > EXPECTED_TAGS[tag]:
            raise ValueError("HTML element count exceeded")
        if any((name is None or name not in ALLOWED_ATTRS.get(tag, set())
                or value is None) for name, value in attrs):
            raise ValueError("Unapproved HTML attribute")
        names = [name for name, _ in attrs]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate HTML attribute")
        attributes = dict(attrs)
        if tag == "html" and (
            attributes != {"lang": "ko", "data-theme": attributes.get("data-theme")}
            or attributes.get("data-theme") not in THEMES
        ):
            raise ValueError("Unapproved HTML root")
        if tag == "meta":
            if attributes == {"charset": "utf-8"}:
                meta_kind = "charset"
            elif attributes == {
                "name": "viewport", "content": "width=device-width,initial-scale=1"
            }:
                meta_kind = "viewport"
            elif (set(attributes) == {"http-equiv", "content"}
                  and attributes["http-equiv"].lower() == "content-security-policy"
                  and attributes["content"].startswith(
                      "default-src 'none'; script-src 'sha256-")
                  and "connect-src 'none'" in attributes["content"]):
                # Exact fixed policy + executable-script SHA remains a separate
                # mandatory check in the CODEX-owned verify_delivery verifier.
                meta_kind = "csp"
            else:
                raise ValueError("Unapproved HTML meta instruction")
            if meta_kind in self.metas:
                raise ValueError("Duplicate HTML metadata")
            self.metas.add(meta_kind)
        if tag == "script":
            if attributes == {"type": "application/json", "id": "dataset"}:
                kind = "data"
            elif not attributes:
                kind = "static"
            else:
                raise ValueError("Unexpected script attributes")
            if kind in self.scripts:
                raise ValueError("Duplicate HTML script")
            self.scripts.add(kind)
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag not in EXPECTED_TAGS or tag in VOID_TAGS:
            raise ValueError("Unexpected HTML closing element")
        if not self.stack or self.stack.pop() != tag:
            raise ValueError("Malformed HTML nesting")


def assert_passive_offline_html_markup(html_bytes):
    """Accept only the reviewed passive DATA2WEB V1 tag surface.

    Raises ValueError with a generic message on unsafe structure. Never
    returns authority to sell, customer ownership or security certification.
    """
    if not isinstance(html_bytes, bytes) or len(html_bytes) > 20_000_000:
        raise ValueError("Invalid or oversized HTML snapshot")
    try:
        source = html_bytes.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ValueError("Invalid HTML text encoding") from exc
    parser = _HTMLSurfaceParser()
    parser.feed(source)
    parser.close()
    if (parser.declaration_count != 1
        or parser.tags != Counter(EXPECTED_TAGS)
        or parser.stack
        or parser.metas != {"charset", "viewport", "csp"}
        or parser.scripts != {"data", "static"}):
        raise ValueError("HTML does not match approved passive surface")
    return {"passive_template_surface_verified": True,
            "source_authenticity_verified": False,
            "independent_security_audit_completed": False,
            "commercial_release_approved": False}
