"""R29 real browser-local HTML save -> independent passive surface regression.

All data are synthetic in a temporary folder. No external requests, service
deployment, customer originals, or third-party transfer. This is hosted
browser evidence only, not a customer's Windows10/11 acceptance or external
human security audit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import re
import tempfile
from pathlib import Path
from html.parser import HTMLParser

from playwright.sync_api import expect, sync_playwright

from data2web_single import deliver_single
from r29_html_surface_policy import (
    APPROVED_FIXED_INPUTS, APPROVED_STATIC_NOTICES,
    assert_passive_offline_html_markup,
)


def _redacted_synthetic_surface_diagnostic(raw):
    # Test-only troubleshooting: print fixed contract IDs, never content.
    class Audit(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.inputs = {}
            self.notices = {}
            self.active = None

        def handle_starttag(self, tag, attrs):
            attr = dict(attrs)
            identity = attr.get("id")
            if tag == "input" and identity in APPROVED_FIXED_INPUTS:
                self.inputs[identity] = attr
            if tag == "p" and identity in APPROVED_STATIC_NOTICES:
                self.active = identity
                self.notices[identity] = []

        def handle_data(self, data):
            if self.active is not None:
                self.notices[self.active].append(data)

        def handle_endtag(self, tag):
            if tag == "p":
                self.active = None

    probe = Audit()
    probe.feed(raw.decode("utf-8", errors="strict"))
    probe.close()
    altered_inputs = sorted(k for k, v in APPROVED_FIXED_INPUTS.items()
                            if probe.inputs.get(k) != v)
    altered_notices = sorted(k for k, v in APPROVED_STATIC_NOTICES.items()
                             if "".join(probe.notices.get(k, [])) != v)
    print("R29_SYNTHETIC_SAVED_CONTROL_MISMATCH_IDS=" +
          json.dumps(altered_inputs))
    print("R29_SYNTHETIC_SAVED_NOTICE_MISMATCH_IDS=" +
          json.dumps(altered_notices))


def _synthetic_csv(rows):
    text = io.StringIO(newline="")
    writer = csv.writer(text)
    writer.writerow(["id", "title", "category", "amount"])
    for i in range(rows):
        writer.writerow([
            f"ID-{i:03}", "</script><svg onload=alert(1)>" if i == 5
            else f"Synthetic record {i:03}", f"CAT-{i % 12:02}", str(i + 1)
        ])
    return text.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description="Local-only R29 browser-saved HTML")
    parser.add_argument("--channel", choices=("chromium", "chrome", "msedge"),
                        default="chromium")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="r29-saved-dom-") as scratch:
        root = Path(scratch)
        original = root / "approved.csv"
        original_bytes = _synthetic_csv(3)
        original.write_bytes(original_bytes)
        target = root / "delivery-new"
        deliver_single(
            original, target,
            expected_sha256=hashlib.sha256(original_bytes).hexdigest(),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )
        index = target / "index.html"
        assert_passive_offline_html_markup(index.read_bytes())
        replacement = root / "replacement-synthetic.csv"
        replacement.write_bytes(_synthetic_csv(76))
        with sync_playwright() as pw:
            browser = (pw.chromium.launch(headless=True)
                       if args.channel == "chromium" else
                       pw.chromium.launch(channel=args.channel, headless=True))
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()
            errors, remote = [], []
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.on("request", lambda req:
                    remote.append(req.url) if req.url.startswith(
                        ("http:", "https:")) else None)
            page.goto(index.as_uri())
            expect(page.locator("#count")).to_have_text("3건")
            page.locator("#csv").set_input_files(str(replacement))
            page.locator("#ack").check()
            page.locator("#replace").click()
            expect(page.locator("#count")).to_have_text("76건")
            expect(page.locator("#import-warning")).to_be_visible()
            # More than 10 categories forces the aggregation/extra chart
            # row and 76 records require a 50-row paginated DOM.
            if page.locator("#body tr").count() != 50:
                raise AssertionError("Page limit or rendered row count changed")
            if page.locator("#chart-bars .chart-row").count() != 10:
                raise AssertionError("Top-category chart structure changed")
            with page.expect_download() as downloaded:
                page.locator("#save").click()
            saved = root / "browser-saved.html"
            downloaded.value.save_as(str(saved))
            raw = saved.read_bytes()
            # This tool only ever handles generated synthetic records.
            # Redact all source values; print bounded *style attributes*
            # to diagnose browser serializer compatibility, never paths.
            class _SyntheticStyleAudit(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.styles = []

                def handle_starttag(self, tag, attrs):
                    for name, value in attrs:
                        if name == "style":
                            self.styles.append((tag, (value or "")[:100]))
            debug = _SyntheticStyleAudit()
            debug.feed(raw.decode("utf-8"))
            print("R29_SYNTHETIC_BROWSER_INLINE_STYLES=" +
                  json.dumps(debug.styles[:20]))
            try:
                checked = assert_passive_offline_html_markup(raw)
            except ValueError:
                _redacted_synthetic_surface_diagnostic(raw)
                raise
            if checked.get("passive_template_surface_verified") is not True:
                raise AssertionError("Saved HTML guard returned an invalid result")
            if checked.get("commercial_release_approved") is not False:
                raise AssertionError("Browser save cannot authorize sale")
            second = context.new_page()
            second.on("pageerror", lambda err: errors.append(str(err)))
            second.on("request", lambda req:
                      remote.append(req.url) if req.url.startswith(
                          ("http:", "https:")) else None)
            second.goto(saved.as_uri())
            expect(second.locator("#count")).to_have_text("76건")
            expect(second.locator("#import-warning")).to_be_visible()
            dataset = json.loads(second.locator("#dataset").text_content())
            if (dataset["import_status"] !=
                "USER_LOCAL_CSV_REPLACEMENT_NOT_VERIFIED"):
                raise AssertionError("Locally replaced provenance was upgraded")
            if len(dataset["rows"]) != 76:
                raise AssertionError("Local browser output lost rows")
            if errors or remote:
                raise AssertionError("Browser errors or unexpected network attempts")

            # R29-ID-001: synthetic real-browser identity spoof. The static JS
            # calls getElementById("dataset"); untrusted extra div must not
            # be able to shadow the original approved JSON script.
            pristine = index.read_bytes()
            m = re.search(
                rb'<script type="application/json" id="dataset">(.*?)</script>',
                pristine, re.DOTALL,
            )
            if m is None:
                raise AssertionError("Expected approved dataset missing")
            forged = json.loads(m.group(1))
            forged["rows"] = [dict(forged["rows"][0])]
            forged["rows"][0]["title"] = "SYNTHETIC_UNVERIFIED_DISPLAY"
            injected = (
                b'<div id="dataset">'
                + json.dumps(forged, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
                + b"</div>"
            )
            attack_html = pristine.replace(
                b"</main>", injected + b"</main>", 1
            )
            if attack_html == pristine:
                raise AssertionError("Synthetic fixed-id mutation missing")
            try:
                assert_passive_offline_html_markup(attack_html)
            except ValueError:
                guard_rejected = True
            else:
                guard_rejected = False
            if not guard_rejected:
                raise AssertionError("High guard accepted shadowed dataset identity")

            attack_file = root / "synthetic-unverified-shadow.html"
            attack_file.write_bytes(attack_html)
            probe = context.new_page()
            probe.on("pageerror", lambda err: errors.append(str(err)))
            probe.on("request", lambda req:
                     remote.append(req.url) if req.url.startswith(
                         ("http:", "https:")) else None)
            probe.goto(attack_file.as_uri())
            expect(probe.locator("#count")).to_have_text("1건")
            expect(probe.locator("#body tr")).to_contain_text(
                "SYNTHETIC_UNVERIFIED_DISPLAY")
            # The real JS was unmodified, but chose the forged DOM id.
            if errors or remote:
                raise AssertionError("Synthetic spoof browser errors/network attempt")
            print("R29_ACTUAL_BROWSER_DOM_ID_SHADOW_REPRODUCED channel=" + args.channel +
                  " unverified_display=true guard_rejected=true network0=true")
            browser.close()
        if original.read_bytes() != original_bytes:
            raise AssertionError("Original approved source changed")
        print("R29_ACTUAL_BROWSER_SAVED_DOM_PASS channel=" + args.channel +
              " rows=76 categories=12 rendered=50 chart=10" +
              " guard=PASS source_unchanged=true network0=true" +
              " browser_reopen=true sale_approved=false")


if __name__ == "__main__":
    main()
