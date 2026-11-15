"""R29 standalone HTML passive-markup policy, independent of the renderer.

The approved DATA2WEB V1 offline template has a fixed tag/attribute surface.
This check is a defense-in-depth component; it is NOT proof of origin, signing,
data rights, or an external independent audit. All errors are redacted.
"""
from __future__ import annotations

from collections import Counter
import base64
import hashlib
from html.parser import HTMLParser
import re

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
# Browser "Save local HTML" serializes the DOM after rendering extra table,
# category and chart elements. Static control counts remain fixed.
DYNAMIC_COUNTS = {
    "div": (7, 60), "span": (5, 60),
    "option": (2, 10_100), "tr": (0, 55),
    "th": (0, 40), "td": (0, 2_000),
}
# Independent reviewed V1 CSS and executable JavaScript byte hashes.
# Manifest SHA and CSP hash inside a ZIP are attacker-rehashable.
APPROVED_SCRIPT_SHA256 = "88eb85f18024b12dee9b0a80b5df63c5fe62657cf3fa207c18dff57178dd3a14"
APPROVED_STYLE_SHA256 = "4cd3dc81e7efb0fc1fe60b072f5fa0e81ed40f8cfc22c0aea863e42f49a1f597"
APPROVED_CSP = (
    "default-src 'none'; script-src 'sha256-" +
    base64.b64encode(bytes.fromhex(APPROVED_SCRIPT_SHA256)).decode("ascii") +
    "'; style-src 'unsafe-inline'; img-src 'none'; connect-src 'none'; " +
    "form-action 'none'; base-uri 'none'"
)
# IDs are executable JS lookup keys (getElementById). A duplicated or
# shadowed dataset ID can redirect display to unverified rows even when the
# original dataset script and ZIP receipt remain unchanged.
# This map is reviewed independently of an untrusted package's HTML.
APPROVED_FIXED_IDS = {
    "sheet-warning": "p",
    "formula-warning": "p",
    "import-warning": "p",
    "source-line": "p",
    "total-rows": "strong",
    "filtered-rows": "strong",
    "category-total": "strong",
    "search": "input",
    "category": "select",
    "sort": "select",
    "direction": "button",
    "count": "p",
    "print-scope": "p",
    "head": "thead",
    "body": "tbody",
    "prev": "button",
    "page": "span",
    "next": "button",
    "metric": "select",
    "chart-note": "small",
    "chart-bars": "div",
    "chart-summary": "p",
    "detail-panel": "section",
    "details": "pre",
    "csv": "input",
    "ack": "input",
    "replace": "button",
    "save": "button",
    "notice": "p",
    "dataset": "script",
}

ALLOWED_ATTRS = {
    "html": {"lang", "data-theme"},
    "meta": {"charset", "name", "content", "http-equiv"},
    "small": {"id", "class"},
    "p": {"id", "class", "aria-live", "role", "hidden"},
    "section": {"class", "aria-label", "id"},
    "div": {"class", "id", "role", "aria-label", "style"},
    "span": {"class", "id"},
    "strong": {"id"},
    "input": {"id", "type", "placeholder", "accept"},
    "select": {"id", "size", "aria-label", "multiple"},
    "option": {"value", "selected", "data-all"},
    "button": {"id", "type", "disabled"},
    "table": {"aria-label"},
    "thead": {"id"},
    "tbody": {"id"},
    "nav": {"class", "aria-label"},
    "pre": {"id", "aria-live"},
    "tr": {"tabindex", "aria-label"},
    "script": {"type", "id"},
}
VOID_TAGS = {"meta", "input"}
BOOLEAN_ATTRS = {"p": {"hidden"}, "select": {"multiple"},
                 "option": {"selected"}, "button": {"disabled"}}
THEMES = {"office", "cafe", "inventory"}
# Reviewer-pinned obligations. Never derive them from the package under test.
APPROVED_STATIC_NOTICES = {
    "sheet-warning": "이 자료는 Excel 셀의 원시/캐시 값을 문자로 표시합니다. 날짜·숫자 표시형식·수식 재계산은 재현하지 않으므로 원본과 대조하십시오.",
    "formula-warning": "수식 셀이 발견되어 명시적으로 승인한 캐시값만 읽었습니다. 수식은 계산되지 않았고 캐시가 올바른지는 보장하지 않습니다.",
    "import-warning": "현재 데이터는 브라우저에서 교체한 로컬 CSV입니다. 원본 SHA·이전 납품 ZIP 무결성 증거가 새 데이터에 적용되지 않습니다. 배포 전 판매자 재검증이 필요합니다.",
    "print-scope": "인쇄는 현재 화면의 최대 50행만 포함합니다. 전체 자료는 오프라인 HTML에서 확인하세요.",
}
APPROVED_FIXED_INPUTS = {
    "ack": {"id": "ack", "type": "checkbox"},
    "csv": {"id": "csv", "type": "file", "accept": ".csv,text/csv"},
    "search": {"id": "search", "type": "search", "placeholder": "모든 열에서 검색"},
}


def _approved_print_scope(value):
    # The source template is static, but the reviewed runtime updates this
    # sentence on every filter/pagination event before HTML download.
    # Accept only the exact reviewed syntax and internally consistent pages.
    if value == APPROVED_STATIC_NOTICES["print-scope"]:
        return True
    match = re.fullmatch(
        r"인쇄 범위: (\d{1,5})건 중 화면 ([1-9]\d{0,2})/([1-9]\d{0,2})"
        r"페이지의 최대 50행\. 전체 데이터는 오프라인 HTML을 이용하세요\.",
        value,
    )
    if not match:
        return False
    total, page, pages = (int(part) for part in match.groups())
    return (total <= 10_000 and pages == max(1, (total + 49) // 50)
            and page <= pages)


class _HTMLSurfaceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = Counter()
        self.stack = []
        self.metas = set()
        self.scripts = set()
        self.declaration_count = 0
        self.total_tags = 0
        self.seen_fixed_ids = set()
        self.head_closed = False
        self.main_closed = False
        self.active_notice = None
        self.notice_parts = {}

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

    def handle_data(self, data):
        if self.active_notice is not None:
            self.notice_parts[self.active_notice].append(data)

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def _start(self, tag, attrs):
        if tag not in EXPECTED_TAGS and tag not in DYNAMIC_COUNTS:
            raise ValueError("Unapproved HTML element")
        self.total_tags += 1
        if self.total_tags > 15_000:
            raise ValueError("HTML element count exceeded")
        self.tags[tag] += 1
        if self.active_notice is not None:
            raise ValueError("Static disclosure cannot contain child markup")
        # Counts alone do not prove a CSP meta is in HEAD or that runtime
        # JavaScript executes only after its controls have been parsed.
        parent = tuple(self.stack)
        if tag == "html":
            if parent:
                raise ValueError("Unapproved document structure")
        elif tag == "head":
            if parent != ("html",) or self.head_closed:
                raise ValueError("Unapproved head position")
        elif tag == "body":
            if parent != ("html",) or not self.head_closed:
                raise ValueError("Unapproved body position")
        elif tag in {"meta", "title", "style"}:
            if parent != ("html", "head"):
                raise ValueError("Unapproved head element position")
        elif tag == "main":
            if parent != ("html", "body") or self.main_closed:
                raise ValueError("Unapproved main position")
        elif tag == "script":
            if parent != ("html", "body") or not self.main_closed:
                raise ValueError("Unapproved script position")
        elif "main" not in parent:
            raise ValueError("Unapproved body element position")
        if tag in DYNAMIC_COUNTS:
            if self.tags[tag] > DYNAMIC_COUNTS[tag][1]:
                raise ValueError("Dynamic HTML element count exceeded")
        elif self.tags[tag] > EXPECTED_TAGS[tag]:
            raise ValueError("HTML element count exceeded")
        for name, value in attrs:
            if (name is None or name not in ALLOWED_ATTRS.get(tag, set())
                or (value is None and
                    name not in BOOLEAN_ATTRS.get(tag, set())) or
                (value not in (None, "") and
                 name in BOOLEAN_ATTRS.get(tag, set()))):
                raise ValueError("Unapproved HTML attribute")
        names = [name for name, _ in attrs]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate HTML attribute")
        attributes = dict(attrs)
        if "id" in attributes:
            fixed_id = attributes["id"]
            if (fixed_id not in APPROVED_FIXED_IDS or
                APPROVED_FIXED_IDS[fixed_id] != tag or
                fixed_id in self.seen_fixed_ids):
                raise ValueError("Unapproved, misplaced or duplicate HTML identity")
            self.seen_fixed_ids.add(fixed_id)
            if (fixed_id in APPROVED_FIXED_INPUTS
                    and attributes != APPROVED_FIXED_INPUTS[fixed_id]):
                raise ValueError("Critical input semantics changed")
            if fixed_id in APPROVED_STATIC_NOTICES:
                self.active_notice = fixed_id
                self.notice_parts[fixed_id] = []
        if tag == "option" and "data-all" in attributes and attributes["data-all"] != "true":
            raise ValueError("Unexpected dynamic option metadata")
        if tag == "tr" and "tabindex" in attributes and attributes["tabindex"] != "0":
            raise ValueError("Unexpected table-row accessibility metadata")
        if "style" in attributes:
            styling = attributes["style"]
            width = re.fullmatch(
                r"\s*width:\s*(\d+(?:\.\d+)?(?:e-?\d+)?)%\s*;?\s*",
                styling, flags=re.I,
            ) if styling is not None else None
            # Aggregated "other" categories may exceed the largest
            # individual category, e.g. 257.143%; the approved stylesheet
            # separately sets max-width:100% on chart bars. The importer
            # bounds rows at 10,000, so even an extreme valid aggregation
            # has a finite <= 1,000,000% computed style. Never allow other
            # CSS properties, URLs, units, infinities or negative widths.
            if (tag != "div" or attributes.get("class") != "bar-fill"
                    or "id" in attributes or not width or
                    not 0 <= float(width.group(1)) <= 1_000_000):
                raise ValueError("Inline HTML styles outside the chart contract")
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
                  and attributes["content"] == APPROVED_CSP):
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
            if kind == "static" and "data" not in self.scripts:
                raise ValueError("Executable HTML script precedes approved data")
            if kind in self.scripts:
                raise ValueError("Duplicate HTML script")
            self.scripts.add(kind)
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if (tag not in EXPECTED_TAGS and tag not in DYNAMIC_COUNTS
                or tag in VOID_TAGS):
            raise ValueError("Unexpected HTML closing element")
        if not self.stack or self.stack.pop() != tag:
            raise ValueError("Malformed HTML nesting")
        if tag == "p" and self.active_notice is not None:
            self.active_notice = None
        if tag == "head":
            self.head_closed = True
        elif tag == "main":
            self.main_closed = True


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
    for tag, baseline in EXPECTED_TAGS.items():
        actual = parser.tags[tag]
        if tag in DYNAMIC_COUNTS:
            if not DYNAMIC_COUNTS[tag][0] <= actual <= DYNAMIC_COUNTS[tag][1]:
                raise ValueError("Dynamic HTML is outside reviewed limits")
        elif actual != baseline:
            raise ValueError("HTML does not match static element counts")
    if (parser.declaration_count != 1
        or parser.stack
        or parser.metas != {"charset", "viewport", "csp"}
        or parser.scripts != {"data", "static"}
        or parser.seen_fixed_ids != set(APPROVED_FIXED_IDS)
        or parser.active_notice is not None
        or set(parser.notice_parts) != set(APPROVED_STATIC_NOTICES)
        or any("".join(parser.notice_parts[k]) != expected
               for k, expected in APPROVED_STATIC_NOTICES.items()
               if k != "print-scope")
        or not _approved_print_scope(
            "".join(parser.notice_parts["print-scope"]))):

        raise ValueError("HTML does not match approved passive surface")
    # Static JS and CSS must match REVIEWED bytes, not attacker-controlled ZIP
    # manifest or dynamic CSP text. The JSON data may change after local CSV.
    js = re.findall(rb"<script>(.*?)</script>", html_bytes,
                    flags=re.DOTALL | re.IGNORECASE)
    css = re.findall(rb"<style>(.*?)</style>", html_bytes,
                     flags=re.DOTALL | re.IGNORECASE)
    if (len(js) != 1 or len(css) != 1
        or hashlib.sha256(js[0]).hexdigest() != APPROVED_SCRIPT_SHA256
        or hashlib.sha256(css[0]).hexdigest() != APPROVED_STYLE_SHA256):
        raise ValueError("Approved executable/style bytes changed")
    return {"passive_template_surface_verified": True,
            "source_authenticity_verified": False,
            "independent_security_audit_completed": False,
            "commercial_release_approved": False}
