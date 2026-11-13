"""Actual local file:// Chromium acceptance, run after playwright browser install."""
import hashlib
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from data2web import build

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        source=root/"source.csv"
        source.write_text("id,title,category\n"+"\n".join(
            f"{i},Product-{i},{'A' if i%2==0 else 'B'}" for i in range(115))+"\n",encoding="utf-8")
        target=root/"app.html"
        result=build(source,target,"id","title","category",True,
                     expected_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        assert result["rows"]==115
        changed=root/"changed.csv"
        changed.write_text('id,title,category\nN1,"Changed, title",A\nN2,"</script><img onerror=alert(1)>",B\n',encoding="utf-8")
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True)
            context=browser.new_context(accept_downloads=True)
            page=context.new_page()
            faults=[]
            requests=[]
            page.on("pageerror",lambda e:faults.append(str(e)))
            page.on("request",lambda r:requests.append(r.url) if r.url.startswith(("https:","http:")) else None)
            page.goto(target.as_uri())
            expect(page.locator("#count")).to_have_text("115건")
            assert page.locator("#count").inner_text()=="115건"
            assert page.locator("#page").inner_text()=="1 / 3"
            page.locator("#next").click()
            assert page.locator("#page").inner_text()=="2 / 3"
            page.locator("#search").fill("Product-114")
            assert page.locator("#count").inner_text()=="1건"
            page.locator("#search").fill("")
            page.locator("#category").select_option("B")
            assert page.locator("#count").inner_text()=="57건"
            page.locator("#category").select_option("")
            page.locator("#sort").select_option("id")
            page.locator("#direction").click()
            page.locator("#body tr").first.click()
            assert "114" in page.locator("#details").inner_text()
            page.locator("#csv").set_input_files(str(changed))
            page.locator("#replace").click()
            assert "HOLD" in page.locator("#notice").inner_text()
            assert page.locator("#count").inner_text()=="115건"
            page.locator("#ack").check()
            page.locator("#replace").click()
            expect(page.locator("#count")).to_have_text("2건", timeout=10000)
            assert page.locator("img").count()==0
            with page.expect_download() as started:
                page.locator("#save").click()
            downloaded=started.value
            saved=Path(downloaded.path())
            assert saved.exists()
            reopened=context.new_page()
            reopened.on("pageerror",lambda e:faults.append(str(e)))
            reopened.on("request",lambda r:requests.append(r.url) if r.url.startswith(("https:","http:")) else None)
            reopened.goto(saved.as_uri())
            expect(reopened.locator("#count")).to_have_text("2건")
            assert reopened.locator("#count").inner_text()=="2건"
            reopened.locator("#search").fill("Changed")
            assert reopened.locator("#count").inner_text()=="1건"
            assert reopened.locator("img").count()==0
            assert not faults,f"Browser JavaScript errors: {faults}"
            assert not requests,f"Unexpected remote requests: {requests}"
            browser.close()
    print("BROWSER_PASS file:// search/category/sort/detail/page, owner CSV ACK, export/reopen, XSS, no egress")

if __name__=="__main__":
    main()
