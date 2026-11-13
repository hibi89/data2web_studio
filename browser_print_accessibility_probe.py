"""R15/R16: real standalone file:// print-to-PDF and keyboard acceptance.

Runs in test-only Chromium, installed Chrome and Edge. pypdf is test-only,
not shipped in the customer ZIP or Python zipapp. Synthetic data only.
"""
import argparse
import hashlib
import io
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import expect, sync_playwright
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--channel",choices=["chromium","chrome","msedge"],required=True)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory() as root_str:
        root=Path(root_str)
        csv_file=root/"print-sample.csv"
        csv_file.write_text(
            "id,title,category,amount\n"+
            "".join(f"{i},Product-{i:03d},{'ABC'[i%3]},{i%10+1}\n" for i in range(131)),
            encoding="utf-8")
        html_file=root/"print-approved.html"
        command=[sys.executable,"studio.py","build",str(csv_file),str(html_file),
                 "--source-sha256",hashlib.sha256(csv_file.read_bytes()).hexdigest(),
                 "--id","id","--title","title","--category","category",
                 "--name","Print sample","--theme","office",
                 "--confirm","APPROVE","--ack-plaintext"]
        done=subprocess.run(command,cwd=ROOT,text=True,encoding="utf-8",
                            capture_output=True)
        assert done.returncode==0,(done.stdout+done.stderr)
        with sync_playwright() as p:
            browser=(p.chromium.launch(headless=True) if args.channel=="chromium"
                     else p.chromium.launch(channel=args.channel,headless=True))
            context=browser.new_context(viewport={"width":1250,"height":860})
            page=context.new_page()
            pageerrors=[]
            remote=[]
            page.on("pageerror",lambda error:pageerrors.append(str(error)))
            page.on("request",lambda request:remote.append(request.url) if
                request.url.startswith(("http:","https:")) else None)
            page.goto(html_file.as_uri())
            expect(page.locator("#count")).to_have_text("131건")
            expect(page.locator("#print-scope")).to_contain_text("1/3페이지")
            expect(page.locator("#body tr")).to_have_count(50)
            first=page.locator("#body tr").first
            first.focus()
            first.press("Space")
            expect(page.locator("#details")).to_contain_text("Product-000")
            assert first.get_attribute("aria-label")=="상세 보기: Product-000"
            page.emulate_media(media="print")
            css=page.evaluate("""() => ({
                tableLayout:getComputedStyle(document.querySelector("table")).tableLayout,
                controls:getComputedStyle(document.querySelector(".controls")).display,
                overflow:getComputedStyle(document.querySelector(".table-scroll")).overflowX,
                scope:getComputedStyle(document.querySelector("#print-scope")).display,
                rows:document.querySelectorAll("#body tr").length
            })""")
            assert css["controls"]=="none",css
            assert css["tableLayout"]=="fixed",css
            assert css["overflow"]=="visible",css
            assert css["scope"]!="none" and css["rows"]==50,css
            def pdf_check():
                data=page.pdf(format="A4",prefer_css_page_size=True,
                              print_background=True)
                assert data.startswith(b"%PDF-") and len(data)>4000
                reader=PdfReader(io.BytesIO(data))
                assert 1<=len(reader.pages)<=30
                first_page=reader.pages[0]
                assert abs(float(first_page.mediabox.width)-595.28)<2
                assert abs(float(first_page.mediabox.height)-841.89)<2
                text="\n".join(x.extract_text() or "" for x in reader.pages)
                assert "DATA2WEB" in text
                return reader,text
            reader,one=pdf_check()
            assert "Product-000" in one,one[:600]
            assert "Product-050" not in one,one[-300:]
            page.emulate_media(media="screen")
            page.locator("#next").click()
            expect(page.locator("#print-scope")).to_contain_text("2/3페이지")
            expect(page.locator("#body tr")).to_have_count(50)
            page.emulate_media(media="print")
            _,two=pdf_check()
            assert "Product-050" in two
            assert "Product-000" not in two
            # Explicit page-scoped print (not a false claim of printing all 131 rows).
            assert "Product-100" not in two
            assert not remote,remote
            assert not pageerrors,pageerrors
            browser.close()
        print("R16_PRINT_KEYBOARD_PASS channel="+args.channel+
              " A4_PDF_pypdf_extraction + 2_page_scopes + keyboard_Space + file_no_network")

if __name__=="__main__":
    main()
