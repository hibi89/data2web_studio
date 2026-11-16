"""Unsigned offline Windows launch bundle, built from deterministic DATA2WEB .pyz.

A customer must have Python 3.11+ installed. This is not a signed .exe and
does not approve sales or commercial redistribution of source/customer data.
The bundle includes no customer records, credentials or remote endpoints.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from package_portable import create_portable
from path_policy import assert_no_links, read_bounded_source
from secure_output import create_output_directory, create_output_file

FILE_NAMES={"DATA2WEB.pyz","RUN_DESKTOP.cmd","RUN_SELFCHECK.cmd","VERIFY_CUSTOMER.cmd",
            "README_LOCAL_KO.txt","BUNDLE_MANIFEST.json"}
MAX_FILE=2_000_000
STATUS="UNSIGNED_PYTHON_311_LOCAL_ONLY_RELEASE_HOLD"

def _launcher(action):
    if action not in ("desktop","self-check","verify-customer"):
        raise ValueError("Invalid local launcher action")
    extra=" --browsers" if action=="self-check" else ' "%~1"' if action=="verify-customer" else ""
    command=action+extra
    prelude=(
        "@echo off\r\n"
        "setlocal\r\n"
        "rem This local tool requires Python 3.11+; no automatic installation.\r\n"
        "where py >nul 2>&1\r\n"
        "if not errorlevel 1 (\r\n"
        '  py -3.11 -c "import sys;sys.exit(0 if sys.version_info >= (3,11) else 2)" >nul 2>&1\r\n'
        "  if not errorlevel 1 goto use_py\r\n"
        ")\r\n"
        "where python >nul 2>&1\r\n"
        "if errorlevel 1 goto no_python\r\n"
        'python -c "import sys;sys.exit(0 if sys.version_info >= (3,11) else 2)" >nul 2>&1\r\n'
        "if errorlevel 1 goto no_python\r\n"
    )
    if action=="verify-customer":
        prelude=prelude.replace(
            "where py >nul 2>&1\r\n",
            'if "%~1"=="" goto missing_folder\r\n'
            "where py >nul 2>&1\r\n",1)
    suffix=(
        f'python "%~dp0DATA2WEB.pyz" {command}\r\n'
        "exit /b %errorlevel%\r\n"
        ":use_py\r\n"
        f'py -3.11 "%~dp0DATA2WEB.pyz" {command}\r\n'
        "exit /b %errorlevel%\r\n"
        ":no_python\r\n"
        "echo DATA2WEB HOLD: Python 3.11+ required, no download or installation performed.\r\n"
        "exit /b 2\r\n"
    )
    if action=="verify-customer":
        suffix+=(":missing_folder\r\n"
                 "echo DATA2WEB HOLD: pass a local customer folder path as argument.\r\n"
                 "exit /b 2\r\n")
    return (prelude+suffix).encode("utf-8")


def _manifest(entries):
    return {
        "contract":"DATA2WEB_WINDOWS_BUNDLE_V1",
        "status":STATUS,
        "customer_data_included":False,
        "sale_approved":False,
        "signed_executable":False,
        "requires":"Python 3.11+ installed (with Tcl/Tk for desktop)",
        "files":{name:hashlib.sha256(data).hexdigest() for name,data in sorted(entries.items())},
    }


def create_windows_bundle(directory, *, source_directory=None):
    target=Path(directory)
    assert_no_links(target,allow_missing_leaf=True)
    if (target.exists() or target.is_symlink() or
        not target.parent.is_dir() or target.parent.is_symlink() or target.name in ("",".","..")):
        raise FileExistsError("Windows launcher bundle must be a new directory")
    with create_output_directory(target) as output_directory:
        # On error, leave incomplete directory in HOLD for inspection, never delete.
        result=create_portable(
            target/"DATA2WEB.pyz",source_directory=source_directory,
            _output_directory=output_directory
        )
        scripts={
            "RUN_DESKTOP.cmd":_launcher("desktop"),
            "RUN_SELFCHECK.cmd":_launcher("self-check"),
            "VERIFY_CUSTOMER.cmd":_launcher("verify-customer"),
            "README_LOCAL_KO.txt":(
                "DATA2WEB local testing bundle (UNSIGNED, RELEASE HOLD)\n"
                "Requires user-installed Python 3.11+ (Tk required for desktop UI).\n"
                "RUN_SELFCHECK.cmd generates only synthetic data and checks local Chrome + Edge.\n"
                "RUN_DESKTOP.cmd opens a user-reviewed local file dialog; user approves source rights.\n"
                "VERIFY_CUSTOMER.cmd takes an exact local customer folder path as first argument.\n"
                "The checks do not establish data rights, software license, sale approval or vendor signature.\n"
                "Files are never sent to a server. An incomplete or tampered bundle must be held.\n"
            ).encode("utf-8")
        }
        for name,content in scripts.items():
            with create_output_file(target/name,directory=output_directory) as stream:
                stream.write(content)
        entries={"DATA2WEB.pyz":read_bounded_source(target/"DATA2WEB.pyz",max_bytes=MAX_FILE),
                 **scripts}
        doc=_manifest(entries)
        encoded=(json.dumps(doc,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
        with create_output_file(target/"BUNDLE_MANIFEST.json",directory=output_directory) as stream:
            stream.write(encoded)
        verified=verify_windows_bundle(target)
        if not verified["verified"]:
            raise ValueError("Generated bundle failed independent integrity verification")
        return {"created":True,"verified":True,
                "bundle_sha256":hashlib.sha256(encoded).hexdigest(),
                "portable_sha256":result["sha256"],
                "signed_executable":False,"sale_approved":False}



def _reject_duplicates(pairs):
    out={}
    for k,v in pairs:
        if k in out:
            raise ValueError("Duplicate bundle manifest key")
        out[k]=v
    return out


def verify_windows_bundle(directory):
    target=Path(directory)
    assert_no_links(target)
    if not target.is_dir() or {x.name for x in target.iterdir()}!=FILE_NAMES:
        raise ValueError("Incomplete or unexpected bundle files")
    contents={}
    for name in sorted(FILE_NAMES):
        path=target/name
        assert_no_links(path)
        if not path.is_file():
            raise ValueError("Bundle contains a non-file member")
        contents[name]=read_bounded_source(path,max_bytes=MAX_FILE if name=="DATA2WEB.pyz" else 100_000)
    doc=json.loads(contents["BUNDLE_MANIFEST.json"].decode("utf-8"),
                   object_pairs_hook=_reject_duplicates)
    if (not isinstance(doc,dict) or doc.get("contract")!="DATA2WEB_WINDOWS_BUNDLE_V1"
            or doc.get("status")!=STATUS or doc.get("customer_data_included") is not False
            or doc.get("signed_executable") is not False or doc.get("sale_approved") is not False):
        raise ValueError("Unapproved or malformed local Windows bundle manifest")
    source={name:data for name,data in contents.items() if name!="BUNDLE_MANIFEST.json"}
    if doc.get("files")!=_manifest(source)["files"]:
        raise ValueError("Portable runtime or launcher bundle bytes changed")
    return {"verified":True,"status":STATUS,
            "bundle_sha256":hashlib.sha256(contents["BUNDLE_MANIFEST.json"]).hexdigest(),
            "sale_approved":False,"signed_executable":False}


def main():
    import argparse
    p=argparse.ArgumentParser(description="Create/verify unsigned offline Python Windows launcher bundle")
    p.add_argument("action",choices=["create","verify"])
    p.add_argument("directory",type=Path)
    a=p.parse_args()
    result=create_windows_bundle(a.directory) if a.action=="create" else verify_windows_bundle(a.directory)
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":
    main()
