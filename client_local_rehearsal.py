"""Private, stdlib-only local pre-delivery acceptance rehearsal.

No customer file is read; the only input is an internally generated synthetic
CSV. Tests owner-SHA-pin delivery + independent full folder verification,
optionally probes installed Chrome and Edge in disposable headless browser
profiles. Never reports customer-machine acceptance without actually running
on that device. No source or browser output is uploaded or retained.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from data2web_single import deliver_single
from verify_customer_folder import verify_customer_folder


def _browser_binary(which):
    names={"chrome":["chrome","chrome.exe"],"edge":["msedge","msedge.exe"]}
    for name in names[which]:
        candidate=shutil.which(name)
        if candidate:
            return Path(candidate)
    if os.name=="nt":
        roots=[os.environ.get("PROGRAMFILES"),os.environ.get("PROGRAMFILES(X86)"),
               os.environ.get("LOCALAPPDATA")]
        parts={"chrome":("Google","Chrome","Application","chrome.exe"),
               "edge":("Microsoft","Edge","Application","msedge.exe")}[which]
        for root in roots:
            if not root:
                continue
            candidate=Path(root).joinpath(*parts)
            if candidate.is_file():
                return candidate
    return None


def _headless_browser(binary, html, temp):
    profile=temp/("browser-"+binary.name.replace(".","-"))
    command=[str(binary),"--headless=new","--disable-gpu",
             "--disable-extensions","--disable-background-networking",
             "--no-first-run","--no-default-browser-check",
             "--disable-sync","--disable-features=Translate",
             "--user-data-dir="+str(profile),"--virtual-time-budget=3500",
             "--dump-dom",html.as_uri()]
    try:
        process=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                               timeout=22,check=False)
    except (OSError,subprocess.TimeoutExpired):
        return "HOLD_EXECUTION_FAILED"
    if process.returncode!=0:
        return "HOLD_NONZERO_EXIT"
    # The actual DATA2WEB HTML uses <p id="count" role="status">,
    # not a span. Verify live DOM text after executing inline JS.
    if not re.search(rb'<p\s+id="count"\s+role="status">2[^<]*</p>',process.stdout):
        return "HOLD_BROWSER_RENDER_NOT_CONFIRMED"
    if b"LOCAL-ITEM-1" not in process.stdout or b"LOCAL-ITEM-2" not in process.stdout:
        return "HOLD_BROWSER_CONTENT_NOT_VISIBLE"
    return "PASS_SYNTHETIC_LOCAL_FILE"


def self_check(*, with_browsers=False):
    with tempfile.TemporaryDirectory(prefix="data2web-self-check-") as scratch:
        root=Path(scratch)
        sample=root/"sample.csv"
        sample.write_text("id,title,category,amount\n"
                          "S1,LOCAL-ITEM-1,A,2\nS2,LOCAL-ITEM-2,B,3\n",encoding="utf-8")
        approved_sha=hashlib.sha256(sample.read_bytes()).hexdigest()
        delivered=root/"synthetic-delivery"
        receipt=deliver_single(sample,delivered,expected_sha256=approved_sha,
                id_column="id",title_column="title",category_column="category",
                confirm="APPROVE",ack_plaintext=True,
                privacy_classification="NO_PERSONAL_DATA_REVIEWED")
        verified=verify_customer_folder(delivered)
        assert verified["verified"] and receipt["rows"]==2
        results={}
        if with_browsers:
            for name in ("chrome","edge"):
                binary=_browser_binary(name)
                results[name]=(_headless_browser(binary,delivered/"index.html",root)
                               if binary is not None else "HOLD_BROWSER_NOT_INSTALLED")
        result={
            "contract":"DATA2WEB_LOCAL_REHEARSAL_V1",
            "status":"PASS_SYNTHETIC_ONLY" if (not with_browsers or
                all(v=="PASS_SYNTHETIC_LOCAL_FILE" for v in results.values())) else "PARTIAL_HOLD",
            "platform_family":platform.system(),
            "sample_type":"GENERATED_SYNTHETIC_NOT_CUSTOMER_INPUT",
            "local_folder_verified":True,
            "data_egress_required":False,
            "browser_check_requested":bool(with_browsers),
            "browser_results":results,
            "customer_source_inspected":False,
            "customer_rights_approved":False,
            "commercial_release_approved":False,
        }
        return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--browsers",action="store_true",
                        help="Try installed Chrome + Edge using throwaway headless profiles")
    args=parser.parse_args()
    result=self_check(with_browsers=args.browsers)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    return 0 if result["status"]=="PASS_SYNTHETIC_ONLY" else 2


if __name__=="__main__":
    raise SystemExit(main())
