"""Measured synthetic 10,000x20 spreadsheet web viewer performance acceptance.

Not a real-user benchmark or general Chrome/Edge guarantee. CI threshold is
generous to guard against pathological regressions, measured timings reported.
"""
import csv
import hashlib
import json
import tempfile
import time
import tracemalloc
from pathlib import Path

from playwright.sync_api import sync_playwright, expect
from data2web import build
from delivery import package_html
from verify_delivery import verify_zip

ROWS=10000
COLS=20
MAX_BUILD_SEC=20
MAX_INITIAL_SEC=15
MAX_SEARCH_SEC=12
MAX_SORT_SEC=12
MAX_PEAK_PYTHON_MIB=320
MAX_HTML_BYTES=20_000_000

def main():
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary)
        source=root/"large.csv"
        headers=["id","title","category"]+[f"metric{i}" for i in range(COLS-3)]
        with source.open("w",encoding="utf-8",newline="") as out:
            writer=csv.writer(out)
            writer.writerow(headers)
            for i in range(ROWS):
                writer.writerow([f"ITEM-{i:05}",f"Item {i}",f"group{i%20}"]+
                                [str((i*j)%10000) for j in range(1,COLS-2)])
        assert source.stat().st_size<=8_000_000,source.stat().st_size
        html=root/"report.html"
        start=time.perf_counter()
        tracemalloc.start()
        receipt=build(source,html,"id","title","category",True,
                      expected_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        _,memory=tracemalloc.get_traced_memory()
        tracemalloc.stop()
        build_time=time.perf_counter()-start
        assert receipt["rows"]==ROWS
        assert receipt["columns"]==headers
        assert html.stat().st_size<=MAX_HTML_BYTES
        z=root/"report.zip"
        package_html(html,z,receipt)
        assert verify_zip(z)["rows"]==ROWS
        assert build_time<MAX_BUILD_SEC, f"build {build_time:.2f}s over {MAX_BUILD_SEC}s"
        assert memory/1048576<MAX_PEAK_PYTHON_MIB,f"peak {memory/1048576:.1f} MiB"
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True)
            page=browser.new_page(viewport={"width":1360,"height":900})
            failures=[]
            external=[]
            page.on("pageerror",lambda e:failures.append(str(e)))
            page.on("request",lambda r:external.append(r.url) if r.url.startswith(("http:","https:")) else None)
            started=time.perf_counter()
            page.goto(html.as_uri())
            expect(page.locator("#count")).to_have_text("10000건",timeout=15000)
            init_time=time.perf_counter()-started
            assert page.locator("#body tr").count()==50
            assert page.locator("#chart-bars .chart-row").count()==10 # top9+other for 20 categories
            started=time.perf_counter()
            page.locator("#search").fill("ITEM-09999")
            expect(page.locator("#count")).to_have_text("1건",timeout=15000)
            search_time=time.perf_counter()-started
            started=time.perf_counter()
            page.locator("#search").fill("")
            page.locator("#sort").select_option("metric5")
            page.locator("#direction").click()
            expect(page.locator("#count")).to_have_text("10000건",timeout=15000)
            sort_time=time.perf_counter()-started
            assert page.locator("#body tr").count()==50
            assert not failures,failures
            assert not external,external
            browser.close()
        assert init_time<MAX_INITIAL_SEC, f"init {init_time:.2f}s exceeds {MAX_INITIAL_SEC}s"
        assert search_time<MAX_SEARCH_SEC, f"search {search_time:.2f}s exceeds {MAX_SEARCH_SEC}s"
        assert sort_time<MAX_SORT_SEC, f"sort {sort_time:.2f}s exceeds {MAX_SORT_SEC}s"
        print(json.dumps({
            "status":"P85_PERF_PASS_SYNTHETIC_ONLY",
            "rows":ROWS,"cols":COLS,
            "csv_bytes":source.stat().st_size,"html_bytes":html.stat().st_size,
            "build_sec":round(build_time,3),
            "peak_python_mib":round(memory/1048576,2),
            "browser_initial_sec":round(init_time,3),
            "browser_search_sec":round(search_time,3),
            "browser_sort_sec":round(sort_time,3),
            "external_requests":len(external),"page_errors":len(failures)
        },ensure_ascii=True))
if __name__=="__main__":
    main()
