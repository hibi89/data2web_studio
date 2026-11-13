"""Real file:// multi-owner-source append -> inspect -> ZIP -> re-import E2E."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

from verify_delivery import verify_zip
from test_xlsx_fixtures import workbook_bytes

ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--channel",choices=["chromium","chrome","msedge"],default="chromium")
    channel=parser.parse_args().channel
    with tempfile.TemporaryDirectory() as td:
        directory=Path(td)
        one=directory/"one.csv"
        two=directory/"two.tsv"
        three=directory/"three.xlsx"
        one.write_text("id,title,category,amount\nA-1,CSV first,A,2\nA-2,CSV second,B,3\n",encoding="utf-8")
        two.write_text("id\ttitle\tcategory\tamount\nB-1\tTSV item\tA\t4\n",encoding="utf-8")
        three.write_bytes(workbook_bytes(sheets={"Approved":[["id","title","category","amount"],
                                                   ["C-1","XLSX item","C",5]]}))
        sources=[
            {"filename":"one.csv","sha256":hashlib.sha256(one.read_bytes()).hexdigest()},
            {"filename":"two.tsv","sha256":hashlib.sha256(two.read_bytes()).hexdigest()},
            {"filename":"three.xlsx","sha256":hashlib.sha256(three.read_bytes()).hexdigest(),
             "sheet":"Approved"},
        ]
        approval={
            "contract":"DATA2WEB_INPUT_APPROVALS_V1",
            "sources":sources,
            "mapping":{"id":"id","title":"title","category":"category"},
            "approval":{"rights_and_plaintext_ack":True,
                        "privacy_classification":"NO_PERSONAL_DATA_REVIEWED"},
            "name":"Offline approved append",
            "theme":"inventory",
        }
        manifest=directory/"approval.json"
        manifest.write_text(json.dumps(approval),encoding="utf-8")
        out=directory/"combined.html"
        zipped=directory/"combined.zip"
        receipt=directory/"receipt.json"
        process=subprocess.run([sys.executable,"studio.py","append",str(manifest),str(out),
          "--confirm","APPROVE","--ack-plaintext","--zip-path",str(zipped),
          "--receipt-path",str(receipt)],cwd=ROOT,encoding="utf-8",text=True,capture_output=True)
        assert process.returncode==0,process.stdout+process.stderr
        assert json.loads(process.stdout)["rows"]==4
        assert verify_zip(zipped)["rows"]==4
        # Individual new package files do not form a full customer folder here.
        # The complete folder verifier is covered by deliver-append CI unit tests.
        assert json.loads(receipt.read_text(encoding="utf-8"))["source_receipts"][2]["sheet"]=="Approved"
        changed=directory/"changed.csv"
        changed.write_text('id,title,category,amount\nR-1,"Replaced local CSV",Z,11\n',encoding="utf-8")
        with sync_playwright() as playwright:
            browser=(playwright.chromium.launch(headless=True) if channel=="chromium"
                     else playwright.chromium.launch(channel=channel,headless=True))
            context=browser.new_context(accept_downloads=True)
            page=context.new_page()
            errors=[]
            requests=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.on("request",lambda r:requests.append(r.url) if r.url.startswith(("https:","http:")) else None)
            page.goto(out.as_uri())
            expect(page.locator("#count")).to_have_text("4건")
            expect(page.locator("#source-line")).to_contain_text("다중 원본 종합 SHA256")
            assert page.locator("#chart-bars .chart-row").count()==3
            payload=json.loads(page.locator("#dataset").text_content())
            assert len(payload["source_receipts"])==3
            assert payload["source_sha256"]==json.loads(receipt.read_text(encoding="utf-8"))["source_sha256"]
            page.locator("#metric").select_option("amount")
            expect(page.locator("#chart-summary")).to_contain_text("14")
            page.locator("#category").select_option("C")
            expect(page.locator("#count")).to_have_text("1건")
            page.locator("#category").select_option("")
            page.locator("#search").fill("TSV item")
            expect(page.locator("#count")).to_have_text("1건")
            page.locator("#search").fill("")
            page.locator("#csv").set_input_files(str(changed))
            page.locator("#replace").click()
            expect(page.locator("#notice")).to_contain_text("HOLD")
            page.locator("#ack").check()
            page.locator("#replace").click()
            expect(page.locator("#count")).to_have_text("1건")
            expect(page.locator("#import-warning")).to_be_visible()
            with page.expect_download() as downloaded:
                page.locator("#save").click()
            saved=directory/"saved-replaced.html"
            downloaded.value.save_as(str(saved))
            second=context.new_page()
            second.on("pageerror",lambda e:errors.append(str(e)))
            second.on("request",lambda r:requests.append(r.url) if r.url.startswith(("https:","http:")) else None)
            second.goto(saved.as_uri())
            expect(second.locator("#count")).to_have_text("1건")
            expect(second.locator("#import-warning")).to_be_visible()
            newpayload=json.loads(second.locator("#dataset").text_content())
            assert newpayload["source_receipts"] is None
            assert newpayload["source_sha256"] is None
            assert newpayload["import_status"]=="USER_LOCAL_CSV_REPLACEMENT_NOT_VERIFIED"
            assert not requests,requests
            assert not errors,errors
            browser.close()
    print("FINAL_BLUEPRINT_APPEND_BROWSER_PASS channel="+channel+
          " csv/tsv/xlsx per-file SHA, integrity ZIP, chart, replace, re-open, provenance reset, network0")
if __name__=="__main__":main()
