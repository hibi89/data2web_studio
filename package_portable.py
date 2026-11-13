"""Reproducible no-dependency, create-only Python zipapp for local customer delivery.

Zipapp requires a user-installed Python 3.11+. It is NOT a signed Windows EXE.
No network, caches or source/customer records are embedded in the archive.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
from path_policy import assert_no_links
from zipfile import ZIP_STORED, ZipFile, ZipInfo

RUNTIME=(
    "data2web.py","data2web_tabular.py","data2web_web.py",
    "data2web_profile.py","data2web_append.py",
    "receipt_utils.py","path_policy.py","data2web_single.py","studio.py","delivery.py","verify_delivery.py",
)
MAIN=b"from studio import main\nraise SystemExit(main())\n"

def create_portable(output, *, source_directory=None):
    root=Path(source_directory) if source_directory is not None else Path(__file__).resolve().parent
    output=Path(output)
    assert_no_links(output,allow_missing_leaf=True)
    if (output.suffix.lower()!=".pyz" or output.is_symlink() or output.exists() or
            not output.parent.is_dir() or output.parent.is_symlink()):
        raise FileExistsError("Portable output must be a new .pyz file")
    contents=[("__main__.py",MAIN)]
    for name in RUNTIME:
        file=root/name
        assert_no_links(file)
        if not file.is_file() or file.is_symlink() or file.stat().st_size>1_000_000:
            raise ValueError("Unsafe or missing portable source module")
        contents.append((name,file.read_bytes()))
    file_descriptor=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(file_descriptor,"wb") as file:
        with ZipFile(file,"w",compression=ZIP_STORED,allowZip64=False) as archive:
            for name,data in contents:
                member=ZipInfo(name,date_time=(1980,1,1,0,0,0))
                member.compress_type=ZIP_STORED
                member.external_attr=0o100600<<16
                archive.writestr(member,data)
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    return {"created":True,"sha256":digest,"requires":"Python 3.11+",
            "runtime_dependencies":[],"sale_approved":False}

def main():
    import argparse
    import json
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    print(json.dumps(create_portable(args.output),sort_keys=True))

if __name__=="__main__":
    main()
