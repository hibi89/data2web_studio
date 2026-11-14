"""Capture only the verified synthetic DATA2WEB HTML using real Chromium.

No customer input, remote API, credential, personal data, or production deployment.
Playwright is a test-only dependency installed by the free public GitHub workflow.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path

from kmong_weekend_demo import LEAF, REPORT, SOURCE, sample_csv_bytes
from path_policy import assert_no_links
from secure_output import create_output_directory, create_output_file
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
    from playwright.sync_api import sync_playwright, expect
    errors = []
    remote_requests = []
    captures = []
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
            one_bytes = page.screenshot(full_page=False)
            captures.append((one.name, one_bytes))
            page.locator("#search").fill("가상 노트")
            expect(page.locator("#count")).to_have_text("1건")
            two = screenshots / "02-search-filter.png"
            two_bytes = page.screenshot(full_page=False)
            captures.append((two.name, two_bytes))
            # Official Kmong 4:3 cover at 652x488, all authored from the
            # proven synthetic local screenshot. No third-party graphic or
            # external request, no price or unverified ranking on the cover.
            preview_data = base64.b64encode(one_bytes).decode("ascii")
            cover_html = ("""<!doctype html><html lang="ko"><meta charset="utf-8">
            <style>
              *{box-sizing:border-box}
              html,body{margin:0;width:652px;height:488px;overflow:hidden}
              body{font-family:'Noto Sans CJK KR','NanumGothic',sans-serif;
                   color:#f7f9fd;background:linear-gradient(120deg,#0a213a,#143b60)}
              .shell{position:absolute;inset:0;padding:51px 52px;
                     background:radial-gradient(circle at 93% 8%,#1e5981 0,transparent 48%)}
              .eyebrow{font-size:14px;letter-spacing:1px;font-weight:700;color:#84d9e3}
              #headline{font-size:32px;line-height:1.32;font-weight:800;
                        margin:12px 0 10px;letter-spacing:-0.6px}
              .desc{font-size:16px;line-height:1.4;color:#c2dcea}
              .screen{margin-top:20px;height:199px;border:2px solid #779cb9;
                      border-radius:14px;overflow:hidden;background:#f5f7fa;
                      box-shadow:0 10px 35px #03132199}
              .screen img{width:100%;height:100%;object-fit:cover;object-position:top left}
              .note{position:absolute;right:53px;bottom:52px;font-size:11px;
                    background:#0d2439db;border-radius:5px;padding:5px 9px}
            </style><body><main class="shell">
              <div class="eyebrow">DATA2WEB · CUSTOM DASHBOARD</div>
              <h1 id="headline">엑셀·CSV를<br>오프라인 웹 대시보드로</h1>
              <div class="desc">검색 · 분류 · 정렬 · 요약</div>
              <div class="screen"><img alt="가상 데이터 대시보드" src="data:image/png;base64,"""+
              preview_data+""""></div><div class="note">합성 데이터 시연</div>
              </main></body></html>""")
            cover = browser.new_page(viewport={"width": 652, "height": 488},
                                     device_scale_factor=1)
            try:
                cover.on("pageerror", lambda err: errors.append(str(err)))
                cover.on("request", lambda req: remote_requests.append(req.url)
                         if req.url.startswith(("http://", "https://")) else None)
                cover.set_content(cover_html, wait_until="load")
                expect(cover.locator("#headline")).to_contain_text("오프라인 웹 대시보드로")
                three = screenshots / "03-kmong-main-652x488.png"
                three_bytes = cover.screenshot(full_page=False)
                captures.append((three.name, three_bytes))
            finally:
                cover.close()
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
    for name, raw in captures:
        if not raw.startswith(b"\x89PNG\r\n\x1a\n") or not 1000 <= len(raw) <= 8_000_000:
            raise ValueError("Screenshot missing, malformed or too large")
        manifest["screenshots"].append({
            "filename": name,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        })
    output_directory = create_output_directory(screenshots)
    try:
        for name, raw in captures:
            target = output_directory.path / name
            with create_output_file(target, directory=output_directory) as stream:
                stream.write(raw)
        raw_manifest = (
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        with create_output_file(
                output_directory.path / "CAPTURE_EVIDENCE.json",
                directory=output_directory) as stream:
            stream.write(raw_manifest)
    finally:
        output_directory.close()
    return manifest


def main():
    p = argparse.ArgumentParser(description="Render only vetted synthetic HTML")
    p.add_argument("--root", required=True, type=Path)
    print(json.dumps(capture(p.parse_args().root), ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
