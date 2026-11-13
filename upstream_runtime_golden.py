"""Read-only live upstream REA_Web Lite runtime golden comparison.

The upstream PUBLIC repository is checked out by GitHub Actions into a disposable
test directory at its exact pinned commit. Nothing is copied into DATA2WEB git,
and no customer file leaves the runner. No golden is inferred from screenshots.
The comparison covers the shared CSV/JSON input and core local browsing contract;
new product-specific features and pixel equality are intentionally excluded.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright, expect

PINNED_UPSTREAM="7b6b68111efd906f9d929b5e2f577699b26399ee"
SOURCE_ROOT=Path(__file__).resolve().parent
UPSTREAM=SOURCE_ROOT/".upstream-rea-golden"

def run_process(command, *, upstream=False):
    env=os.environ.copy()
    cwd=UPSTREAM if upstream else SOURCE_ROOT
    if upstream:env["PYTHONPATH"]=str(UPSTREAM)
    return subprocess.run(command,cwd=cwd,env=env,capture_output=True,
                          encoding="utf-8",text=True,check=False)

def snapshot_sha():
    if not (UPSTREAM/"rea"/"lite_builder.py").is_file():
        raise RuntimeError("Read-only actual upstream checkout is missing")
    result=run_process(["git","rev-parse","HEAD"],upstream=True)
    if result.returncode!=0 or result.stdout.strip()!=PINNED_UPSTREAM:
        raise RuntimeError("Upstream checkout must match pinned commit exactly")
    return result.stdout.strip()

def script_payload(html,ident):
    expression=r'<script type="application/json" id="'+re.escape(ident)+r'">([^<]+)</script>'
    match=re.search(expression,html)
    if not match:raise AssertionError(f"Embedded data script not found: {ident}")
    return json.loads(match.group(1))

def normalize_new(payload,mapping):
    source=payload["columns"]
    extras=[c for c in source if c not in set(mapping.values())]
    target=["id","title","category"]+extras
    records=[{**{field:row[mapping[field]] for field in ("id","title","category")},
              **{col:row[col] for col in extras}} for row in payload["rows"]]
    return target,records

def build_pair(path,name,mapping,tag,root,*,sha=None):
    old_html=root/(tag+"-old.html")
    new_html=root/(tag+"-new.html")
    source_digest=sha or hashlib.sha256(path.read_bytes()).hexdigest()
    old=run_process([sys.executable,"-m","rea.lite_builder","--source",str(path),
        "--out",str(old_html),"--source-sha256",source_digest,
        "--id-field",mapping["id"],"--title-field",mapping["title"],
        "--category-field",mapping["category"],"--confirm","APPROVE","--name",name],
        upstream=True)
    new=run_process([sys.executable,"studio.py","build",str(path),str(new_html),
        "--source-sha256",source_digest,"--id",mapping["id"],"--title",mapping["title"],
        "--category",mapping["category"],"--confirm","APPROVE","--ack-plaintext",
        "--name",name])
    return old,new,old_html,new_html

def expected_equal(old,new,old_html,new_html,mapping):
    assert old.returncode==0,("upstream execution failed",old.stderr[-500:],old.stdout[-500:])
    assert new.returncode==0,("new standalone build failed",new.stderr[-500:],new.stdout[-500:])
    old_receipt=json.loads(old.stdout)
    new_receipt=json.loads(new.stdout)
    assert old_receipt["rows"]==new_receipt["rows"]
    assert old_receipt["source_sha256"]==new_receipt["source_sha256"]
    assert old_receipt["customer_sale_approved"] is False
    assert new_receipt["sale_approved"] is False
    oh=old_html.read_text(encoding="utf-8")
    nh=new_html.read_text(encoding="utf-8")
    before=script_payload(oh,"rea-dataset")
    after=script_payload(nh,"dataset")
    cols,rows=normalize_new(after,mapping)
    assert before["fields"]==cols,(before["fields"],cols)
    assert before["rows"]==rows,("Row-by-row canonical behavior differs",before["rows"][:1],rows[:1])
    assert "connect-src 'none'" in oh and "connect-src 'none'" in nh
    assert "<script>alert(1)</script>" not in nh
    return len(rows)

def compare_browser(upstream_html,new_html,query,expected_count):
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        context=browser.new_context()
        old=context.new_page()
        new=context.new_page()
        errors=[]
        remote=[]
        for page in (old,new):
            page.on("pageerror",lambda error:errors.append(str(error)))
            page.on("request",lambda request:remote.append(request.url)
                    if request.url.startswith(("http:","https:")) else None)
        old.goto(upstream_html.as_uri())
        new.goto(new_html.as_uri())
        expect(old.locator("#items tr")).to_have_count(min(expected_count,60))
        expect(new.locator("#body tr")).to_have_count(min(expected_count,50))
        old.locator("#search").fill(query)
        new.locator("#search").fill(query)
        assert old.locator("#items tr").count()==new.locator("#body tr").count()
        old.locator("#search").fill("")
        new.locator("#search").fill("")
        old.locator("#category").select_option("A")
        new.locator("#category").select_option("A")
        assert old.locator("#items tr").count()==new.locator("#body tr").count()
        assert not errors,errors
        assert not remote,remote
        browser.close()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--no-browser",action="store_true")
    args=parser.parse_args()
    upstream_sha=snapshot_sha()
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary)
        mapping={"id":"식별자","title":"이름","category":"분류"}
        original=root/"korean.csv"
        with original.open("w",encoding="utf-8",newline="") as stream:
            writer=csv.writer(stream)
            writer.writerow(["식별자","이름","분류","비고"])
            for n in range(75):
                writer.writerow([f"R-{n:03}",("골든 "+str(n) if n!=3 else '</script><img src=x onerror=alert(1)>'),
                                 "A" if n%2==0 else "B",f"메모-{n}"])
        old,new,oh,nh=build_pair(original,"원본 Lite 기준",mapping,"csv",root)
        assert expected_equal(old,new,oh,nh,mapping)==75
        if not args.no_browser:
            compare_browser(oh,nh,"골든 10",75)
        data=root/"korean.json"
        data.write_text(json.dumps([{"식별자":"JSON-1","이름":"콜드브루","분류":"A","비고":"테스트"},
                                    {"식별자":"JSON-2","이름":"딸기우유","분류":"B","비고":"추가"}],
                                   ensure_ascii=False),encoding="utf-8")
        old,new,oh,nh=build_pair(data,"원본 JSON 기준",mapping,"json",root)
        assert expected_equal(old,new,oh,nh,mapping)==2
        if not args.no_browser:compare_browser(oh,nh,"콜드브루",2)
        failcases=[]
        bad=root/"duplicate.csv"
        bad.write_text("식별자,이름,분류\nA1,One,A\nA1,Two,B\n",encoding="utf-8")
        failcases.append((bad,mapping,"duplicate_id"))
        bad_json=root/"duplicate.json"
        bad_json.write_text('[{"식별자":"J1","이름":"One","분류":"A"},{"식별자":"J1","이름":"Two","분류":"B"}]',encoding="utf-8")
        failcases.append((bad_json,mapping,"duplicate_json_id"))
        wrong_mapping={"id":"식별자","title":"이름","category":"이름"}
        failcases.append((original,wrong_mapping,"invalid_mapping"))
        for source,m,key in failcases:
            op,np,old_dest,new_dest=build_pair(source,"검수",m,key,root)
            assert op.returncode!=0,(key,"upstream unexpectedly passed",op.stdout)
            assert np.returncode!=0,(key,"new implementation unexpectedly passed",np.stdout)
            assert not old_dest.exists() and not new_dest.exists()
        stale="0"*64
        op,np,old_dest,new_dest=build_pair(original,"검수",mapping,"stale",root,sha=stale)
        assert op.returncode!=0 and np.returncode!=0
        assert not old_dest.exists() and not new_dest.exists()
    print("UPSTREAM_LITE_ACTUAL_RUNTIME_GOLDEN_PASS original_commit="+upstream_sha+
          " shared CSV/JSON data/semantic mapping, actual file browser query/category, rejected bad inputs,"
          " source SHA and no-clobber; new HTML implementation/pixels are independent")
if __name__=="__main__":main()
