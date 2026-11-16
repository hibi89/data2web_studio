"""Real Chromium file:// E2E for OOXML workbook and TSV generated local HTML."""
import hashlib
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

from data2web import build
from delivery import package_html
from verify_delivery import verify_zip
from test_xlsx_fixtures import workbook_bytes

def main():
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)
        xlsx=root/"workbook.xlsx"
        workbook=workbook_bytes(sheets={
            "Unapproved":[["id","title","category"],["bad","Private not selected","A"]],
            "Approved":[
                ["id","title","category"],
                ["p-1","<script>alert(1)</script>","A"],
                ["p-2","합법 데이터","B"],
            ],
        })
        xlsx.write_bytes(workbook)
        tsv=root/"rows.tsv"
        tsv.write_text('id\ttitle\tcategory\n1\t"TSV\tquoted"\tA\n2\t"TSV result"\tB\n',encoding="utf-8")
        paths=[]
        for inp,tag,kw in (
            (xlsx,"xlsx",{"sheet":"Approved"}),
            (tsv,"tsv",{}),
        ):
            result=build(inp,root/(tag+".html"),"id","title","category",True,
                         expected_sha256=hashlib.sha256(inp.read_bytes()).hexdigest(),**kw)
            package=root/(tag+".zip")
            verified=package_html(root/(tag+".html"),package,result)
            assert verified["verified"]
            assert verify_zip(package)["rows"]==2
            paths.append((root/(tag+".html"),tag))
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            context=browser.new_context()
            for html,tag in paths:
                page=context.new_page()
                faults=[]
                remote=[]
                page.on("pageerror",lambda err:faults.append(str(err)))
                page.on("request",lambda req:remote.append(req.url) if req.url.startswith(("http:","https:")) else None)
                page.goto(html.as_uri())
                expect(page.locator("#count")).to_have_text("2건")
                page.locator("#sort").select_option("title")
                page.locator("#search").fill("p-1" if tag=="xlsx" else "TSV")
                expect(page.locator("#count")).to_have_text("1건" if tag=="xlsx" else "2건")
                if tag=="xlsx":
                    page.locator("#search").fill("")
                    page.locator("#category").select_option("B")
                    expect(page.locator("#count")).to_have_text("1건")
                    assert page.locator("script[src],img").count()==0
                    payload=page.locator("#dataset").text_content()
                    assert '"source_sheet":"Approved"' in payload
                    assert "Private not selected" not in page.content()
                    assert page.locator("#body").inner_text().find("Private not selected")<0
                assert not faults, faults
                assert not remote, remote
                page.close()
            browser.close()
    print("P70_BROWSER_PASS true XLSX+TSV file://, selected sheet, XSS, filter/search, ZIP verified, network0")

if __name__=="__main__":main()
