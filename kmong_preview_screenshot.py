"""Capture only the verified synthetic DATA2WEB HTML using real Chromium.

No customer input, remote API, credential, personal data, or production deployment.
Playwright is a test-only dependency installed by the free public GitHub workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from kmong_weekend_demo import LEAF, REPORT, SOURCE, sample_csv_bytes
from path_policy import assert_no_links
from verify_customer_folder import verify_customer_folder


def capture(root):
    root = Path(root)
    assert_no_links(root)
    if not root.is_dir():
        raise ValueError("Existing real synthetic demo root required")
    source = root / SOURCE
    assert_no_links(source)
    if source.read_bytes() != sample_csv_bytes():
        raise ValueError("Only exact synthetic inventory is permitted")
    report = json.loads((root / REPORT).read_text(encoding="utf-8"))
    if (report.get("contract") != "DATA2WEB_KMONG_SYNTHETIC_DEMO_V1"
            or report.get("sample_only") is not True
            or report.get("customer_data_used") is not False
            or report.get("sale_approved") is not False
            or report.get("rows") != 8):
        raise ValueError("Refuse non-synthetic or falsely approved output")
    demo = root / LEAF
    verified = verify_customer_folder(demo)
    if not verified["verified"] or verified["sale_approved"] is not False:
        raise ValueError("Unverified synthetic HTML delivery")
    screenshots = root / "screenshots"
    assert_no_links(screenshots, allow_missing_leaf=True)
    if screenshots.is_symlink() or screenshots.exists():
        raise FileExistsError("Screenshots are create-only")
    screenshots.mkdir(mode=0o700, exist_ok=False)

    from playwright.sync_api import sync_playwright, expect
    errors = []
    remote_requests = []
    paths = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.on("request", lambda req: remote_requests.append(req.url)
                    if req.url.startswith(("http://", "https://")) else None)
            page.goto((demo / "index.html").absolute().as_uri())
            expect(page.locator("#count")).to_have_text("8건")
            expect(page.locator("#category-total")).to_have_text("3")
            one = screenshots / "01-dashboard.png"
            page.screenshot(path=str(one), full_page=False)
            paths.append(one)
            page.locator("#search").fill("가상 노트")
            expect(page.locator("#count")).to_have_text("1건")
            two = screenshots / "02-search-filter.png"
            page.screenshot(path=str(two), full_page=False)
            paths.append(two)
        finally:
            browser.close()
    if errors or remote_requests:
        raise RuntimeError("Unexpected script errors or remote requests in offline preview")
    manifest = {
        "contract": "DATA2WEB_SYNTHETIC_BROWSER_SCREENSHOTS_V1",
        "customer_data_used": False,
        "real_browser_chromium": True,
        "offline_http_requests": 0,
        "js_errors": 0,
        "sale_approved": False,
        "screenshots": [],
    }
    for file in paths:
        raw = file.read_bytes()
        if not raw.startswith(b"\x89PNG\r\n\x1a\n") or not 1000 <= len(raw) <= 8_000_000:
            raise ValueError("Screenshot missing, malformed or too large")
        manifest["screenshots"].append({
            "filename": file.name,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        })
    with (screenshots / "CAPTURE_EVIDENCE.json").open("x", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")
    return manifest


def main():
    p = argparse.ArgumentParser(description="Render only vetted synthetic HTML")
    p.add_argument("--root", required=True, type=Path)
    print(json.dumps(capture(p.parse_args().root), ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
