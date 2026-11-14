"""Actual vendor browser acceptance: CLI -> ZIP verifier -> file:// chart and export.

Runs on Windows Chrome/Edge and Linux Chromium. Synthetic values only.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright, expect

from verify_delivery import verify_zip

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--channel",choices=["chromium","chrome","msedge"],required=True)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)
        original=root/"source.csv"
        records=["id,title,category,amount,notes"]
        for n in range(240):
            records.append(f"{n},Product-{n},{'ABC'[n%3]},{n%5+1},row-{n}")
        records.append('XSS,Injection,"<img onerror=alert(1)>",4,untrusted')
        original.write_text("\n".join(records)+"\n",encoding="utf-8")
        html=root/"approved.html"
        z=root/"delivery.zip"
        sha=hashlib.sha256(original.read_bytes()).hexdigest()
        cmd=[sys.executable,"studio.py","build",str(original),str(html),
             "--source-sha256",sha,"--id","id","--title","title",
             "--category","category","--confirm","APPROVE","--ack-plaintext",
             "--zip-path",str(z)]
        output=subprocess.run(cmd,cwd=Path(__file__).parent,encoding="utf-8",capture_output=True,text=True)
        assert output.returncode==0,output.stdout+output.stderr
        result=json.loads(output.stdout)
        assert result["rows"]==241
        assert verify_zip(z)["verified"]
        changed=root/"changed.csv"
        # Physical blank CSV lines are legal and ignored by the backend.
        changed.write_text('\nid,title,category,amount,notes\nX1,"Updated row",A,7,ok\n\nX2,"<script>alert(1)</script>",B,11,safe\n\n',encoding="utf-8")
        uncategorized=root/"uncategorized.csv"
        uncategorized.write_text('id,title,category,amount,notes\\nZ1,Uncategorized,,5,blank\\nZ2,Classified,B,7,ok\\n',encoding="utf-8")
        with sync_playwright() as p:
            browser=(p.chromium.launch(headless=True) if args.channel=="chromium"
                     else p.chromium.launch(channel=args.channel,headless=True))
            context=browser.new_context(accept_downloads=True,viewport={"width":1365,"height":900})
            page=context.new_page()
            errors=[]
            remote=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.on("request",lambda r:remote.append(r.url) if r.url.startswith(("https:","http:")) else None)
            page.goto(html.as_uri())
            expect(page.locator("#count")).to_have_text("241건")
            expect(page.locator("#total-rows")).to_have_text("241")
            expect(page.locator("#filtered-rows")).to_have_text("241")
            expect(page.locator("#category-total")).to_have_text("4")
            assert page.locator("#chart-bars .chart-row").count()==4
            assert page.locator("#chart-bars img").count()==0
            page.locator("#metric").select_option("amount")
            expect(page.locator("#chart-summary")).to_contain_text("724")
            page.locator("#category").select_option(["A","B"])
            expect(page.locator("#count")).to_have_text("160건")
            page.locator("#category").select_option("B")
            expect(page.locator("#count")).to_have_text("80건")
            expect(page.locator("#filtered-rows")).to_have_text("80")
            expect(page.locator("#chart-summary")).to_contain_text("240")
            page.locator("#category").select_option("")
            page.locator("#search").fill("Product-239")
            expect(page.locator("#count")).to_have_text("1건")
            page.locator("#search").fill("")
            page.locator("#sort").select_option("id")
            page.locator("#direction").click()
            page.locator("#body tr").first.press("Enter")
            expect(page.locator("#details")).to_contain_text("XSS")
            page.locator("#category").select_option("")
            # Stale detailed content from a different source must never be
            # included in the downloaded replacement HTML.
            page.locator("#body tr").first.click()
            expect(page.locator("#details")).to_contain_text("Injection")
            page.locator("#csv").set_input_files(str(changed))
            page.locator("#replace").click()
            expect(page.locator("#notice")).to_contain_text("HOLD")
            page.locator("#ack").check()
            page.locator("#replace").click()
            expect(page.locator("#count")).to_have_text("2건")
            expect(page.locator("#details")).to_have_text("항목을 선택하세요.")
            expect(page.locator("#import-warning")).to_be_visible()
            expect(page.locator("#metric")).to_have_value("amount")
            expect(page.locator("#chart-summary")).to_contain_text("18")
            with page.expect_download() as download:
                page.locator("#save").click()
            downloaded=root/"saved.html"
            download.value.save_as(str(downloaded))
            assert downloaded.exists()
            assert "row-239" not in downloaded.read_text(encoding="utf-8"), "Stale prior detail leaked into replacement HTML"
            assert "Injection" not in downloaded.read_text(encoding="utf-8"), "Old source detail leaked into replacement"
            secondary=context.new_page()
            secondary.on("pageerror",lambda e:errors.append(str(e)))
            secondary.on("request",lambda r:remote.append(r.url) if r.url.startswith(("https:","http:")) else None)
            secondary.goto(downloaded.as_uri())
            expect(secondary.locator("#count")).to_have_text("2건")
            expect(secondary.locator("#import-warning")).to_be_visible()
            assert '"source_sha256":null' in secondary.locator("#dataset").text_content()
            assert '"source_sheet":null' in secondary.locator("#dataset").text_content()
            assert '"cached_formulas":false' in secondary.locator("#dataset").text_content()
            expect(secondary.locator("#chart-summary")).to_contain_text("표시된 행 2")
            secondary.locator("#metric").select_option("amount")
            expect(secondary.locator("#chart-summary")).to_contain_text("18")
            # A category selected from an earlier source is never silently
            # carried over to a newly reviewed CSV, even when names match.
            secondary.locator("#category").select_option("B")
            expect(secondary.locator("#count")).to_have_text("1건")
            secondary.locator("#csv").set_input_files(str(changed))
            secondary.locator("#ack").check()
            secondary.locator("#replace").click()
            expect(secondary.locator("#count")).to_have_text("2건")
            expect(secondary.locator("#category")).to_have_values([""])
            # Explicit quoted empty at EOF is not a blank physical line.
            # It must HOLD without losing the previously accepted rows.
            invalid=root/"explicit_empty_id.csv"
            invalid.write_text('id,title,category,amount,notes\n""',encoding="utf-8")
            secondary.locator("#csv").set_input_files(str(invalid))
            secondary.locator("#ack").check()
            secondary.locator("#replace").click()
            expect(secondary.locator("#notice")).to_contain_text("HOLD")
            expect(secondary.locator("#count")).to_have_text("2건")
            # Empty category is a valid source value distinct from 'All'.
            secondary.locator("#csv").set_input_files(str(uncategorized))
            secondary.locator("#ack").check()
            secondary.locator("#replace").click()
            expect(secondary.locator("#count")).to_have_text("2건")
            secondary.locator("#category").select_option(label="— 분류 없음 —")
            expect(secondary.locator("#count")).to_have_text("1건")
            expect(secondary.locator("#body tr")).to_have_count(1)
            expect(secondary.locator("#body tr").first).to_contain_text("Z1")
            secondary.locator("#category").select_option("")
            expect(secondary.locator("#count")).to_have_text("2건")
            assert secondary.locator("img").count()==0
            mobile=browser.new_context(viewport={"width":390,"height":844},device_scale_factor=1,is_mobile=False)
            mob=mobile.new_page()
            mob.on("pageerror",lambda e:errors.append(str(e)))
            mob.on("request",lambda r:remote.append(r.url) if r.url.startswith(("https:","http:")) else None)
            mob.goto(html.as_uri())
            expect(mob.locator("#count")).to_have_text("241건")
            # table scroll is inside its container; the document should not overflow horizontally
            scroll_width=mob.evaluate("document.documentElement.scrollWidth")
            assert scroll_width<=391, f"Mobile viewport overflows: {scroll_width}"
            # Print stylesheet has no browser-only external dependencies.
            mob.emulate_media(media="print")
            assert mob.locator(".surface").count()>=3
            assert not errors,errors
            assert not remote,remote
            browser.close()
        print(f"P85_CROSS_BROWSER_PASS channel={args.channel} pages/metrics/safety/import/zip/reopen/mobile/print network0")

if __name__=="__main__":
    main()
