"""DATA2WEB offline owner CLI: inspect -> explicit approval -> build -> verify."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from data2web import read_table, build
from delivery import package_html
from verify_delivery import verify_zip

def main(argv=None):
    p=argparse.ArgumentParser(description="DATA2WEB local-only CSV/JSON HTML creator")
    sub=p.add_subparsers(dest="action",required=True)
    pi=sub.add_parser("inspect");pi.add_argument("source",type=Path)
    pb=sub.add_parser("build")
    pb.add_argument("source",type=Path);pb.add_argument("output",type=Path)
    pb.add_argument("--source-sha256",required=True)
    pb.add_argument("--id",required=True);pb.add_argument("--title",required=True)
    pb.add_argument("--category",required=True)
    pb.add_argument("--confirm",choices=["APPROVE"],required=True)
    pb.add_argument("--ack-plaintext",action="store_true",required=True)
    pb.add_argument("--zip-path",type=Path)
    pb.add_argument("--name",default="DATA2WEB")
    pb.add_argument("--theme",choices=["office","cafe","inventory"],default="office")
    pv=sub.add_parser("verify");pv.add_argument("zip_path",type=Path)
    args=p.parse_args(argv)
    try:
        if args.action=="inspect":
            cols,rows,digest=read_table(args.source)
            result={"status":"LOCAL_INSPECT_NOT_APPROVED","source_sha256":digest,
                    "columns":cols,"rows":len(rows),
                    "plaintext_warning":True,"source_modified":False}
        elif args.action=="build":
            if not args.ack_plaintext:
                raise ValueError("Explicit plaintext acknowledgment required")
            result=build(args.source,args.output,args.id,args.title,args.category,
                         approved=True,expected_sha256=args.source_sha256,
                         name=args.name,theme=args.theme)
            result["status"]="LOCAL_HTML_BUILT_NOT_RELEASE_APPROVED"
            if args.zip_path: result["package"]=package_html(args.output,args.zip_path,result)
        else:
            result=verify_zip(args.zip_path)
        print(json.dumps(result,ensure_ascii=True,sort_keys=True))
        return 0
    except (OSError,ValueError,FileExistsError) as e:
        # Never print row contents or customer paths into logs.
        print(json.dumps({"status":"HOLD","reason_type":type(e).__name__},sort_keys=True))
        return 2
if __name__=="__main__":
    raise SystemExit(main())
