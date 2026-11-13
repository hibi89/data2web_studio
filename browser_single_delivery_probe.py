"""Actual local single-owner-file delivery acceptance in installed browsers."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright, expect
from verify_delivery import verify_zip

ROOT=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--channel",choices=["chromium","chrome","msedge"],default="chromium")
    args=parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)
        source=root/"single.csv"
        source.write_text('id,title,category,amount\n1,First product,A,1\n2,Second product,B,2\n3,"</script><img onerror=alert(1)>",C,3\n',encoding="utf-8")
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        destination=root/"brand-new-customer-folder"
        command=[sys.executable,"studio.py","deliver",str(source),str(destination),
                 "--source-sha256",digest,"--id","id","--title","title","--category","category",
                 "--confirm","APPROVE","--ack-plaintext",
                 "--privacy-classification","NO_PERSONAL_DATA_REVIEWED"]
        result=subprocess.run(command,cwd=ROOT,text=True,encoding="utf-8",capture_output=True)
        assert result.returncode==0,(result.stdout+result.stderr)
        metadata=json.loads(result.stdout)
        assert metadata["rows"]==3
        assert not metadata["sale_approved"]
        assert verify_zip(destination/"delivery.zip")["rows"]==3
        receipt=json.loads((destination/"receipt.json").read_text(encoding="utf-8"))
        assert receipt["source_sha256"]==digest
        again=subprocess.run(command,cwd=ROOT,text=True,encoding="utf-8",capture_output=True)
        assert again.returncode!=0
        assert verify_zip(destination/"delivery.zip")["verified"]
        with sync_playwright() as p:
            browser=(p.chromium.launch(headless=True) if args.channel=="chromium"
                     else p.chromium.launch(channel=args.channel,headless=True))
            context=browser.new_context(accept_downloads=True)
            page=context.new_page()
            errors=[]
            remote=[]
            page.on("pageerror",lambda err:errors.append(str(err)))
            page.on("request",lambda r:remote.append(r.url) if r.url.startswith(("http:","https:")) else None)
            page.goto((destination/"index.html").as_uri())
            expect(page.locator("#count")).to_have_text("3건")
            expect(page.locator("#category-total")).to_have_text("3")
            expect(page.locator("#source-line")).to_contain_text(digest[:20])
            assert page.locator("img").count()==0
            page.locator("#category").select_option(["A","C"])
            expect(page.locator("#count")).to_have_text("2건")
            page.locator("#search").fill("First")
            expect(page.locator("#count")).to_have_text("1건")
            page.locator("#search").fill("")
            page.locator("#category").select_option("")
            page.locator("#metric").select_option("amount")
            expect(page.locator("#chart-summary")).to_contain_text("6")
            assert not errors,errors
            assert not remote,remote
            browser.close()
        print("OWNER_SINGLE_BROWSER_PASS channel="+args.channel+
              " owner_SHA+privacy, new folder, HTML+ZIP+receipt, chart/filter/XSS, repeat HOLD, network0")

if __name__=="__main__":main()
