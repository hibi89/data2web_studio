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
import tempfile
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from data2web_single import deliver_single
from r29_html_surface_policy import assert_passive_offline_html_markup


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
            checked = assert_passive_offline_html_markup(raw)
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
            browser.close()
        if original.read_bytes() != original_bytes:
            raise AssertionError("Original approved source changed")
        print("R29_ACTUAL_BROWSER_SAVED_DOM_PASS channel=" + args.channel +
              " rows=76 categories=12 rendered=50 chart=10" +
              " guard=PASS source_unchanged=true network0=true" +
              " browser_reopen=true sale_approved=false")


if __name__ == "__main__":
    main()
