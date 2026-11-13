"""DATA2WEB offline owner CLI: inspect -> explicit approval -> build -> verify."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from data2web import read_table, build
from delivery import package_html
from verify_delivery import verify_zip

def main(argv=None):
    p=argparse.ArgumentParser(description="DATA2WEB local-only CSV/JSON/TSV/XLSX HTML creator")
    sub=p.add_subparsers(dest="action",required=True)
    pi=sub.add_parser("inspect");pi.add_argument("source",type=Path)
    pi.add_argument("--sheet");pi.add_argument("--header-row",type=int,default=1)
    pi.add_argument("--allow-cached-formulas",action="store_true")
    pb=sub.add_parser("build")
    pb.add_argument("source",type=Path);pb.add_argument("output",type=Path)
    pb.add_argument("--source-sha256",required=True)
    pb.add_argument("--sheet")
    pb.add_argument("--header-row",type=int,default=1)
    pb.add_argument("--allow-cached-formulas",action="store_true")
    pb.add_argument("--id",required=True);pb.add_argument("--title",required=True)
    pb.add_argument("--category",required=True)
    pb.add_argument("--confirm",choices=["APPROVE"],required=True)
    pb.add_argument("--ack-plaintext",action="store_true",required=True)
    pb.add_argument("--zip-path",type=Path)
    pb.add_argument("--receipt-path",type=Path)
    pb.add_argument("--name",default="DATA2WEB")
    pb.add_argument("--theme",choices=["office","cafe","inventory"],default="office")
    pa=sub.add_parser("append")
    pa.add_argument("approval_manifest",type=Path)
    pa.add_argument("output",type=Path)
    pa.add_argument("--confirm",choices=["APPROVE"],required=True)
    pa.add_argument("--ack-plaintext",action="store_true",required=True)
    pa.add_argument("--zip-path",type=Path)
    pa.add_argument("--receipt-path",type=Path)
    pd=sub.add_parser("deliver-append")
    pd.add_argument("approval_manifest",type=Path)
    pd.add_argument("new_directory",type=Path)
    pd.add_argument("--confirm",choices=["APPROVE"],required=True)
    pd.add_argument("--ack-plaintext",action="store_true",required=True)
    pv=sub.add_parser("verify");pv.add_argument("zip_path",type=Path)
    args=p.parse_args(argv)
    try:
        if args.action=="inspect":
            if args.source.suffix.lower()==".xlsx" and args.sheet is None:
                import hashlib
                from data2web_tabular import list_xlsx_sheets
                if (args.source.is_symlink() or not args.source.is_file()
                        or args.source.stat().st_size>8_000_000):
                    raise ValueError("Unsafe XLSX source")
                raw=args.source.read_bytes()
                if len(raw)>8_000_000: raise ValueError("Unsafe XLSX size")
                result={"status":"XLSX_SHEETS_REQUIRE_EXPLICIT_SELECTION",
                        "source_sha256":hashlib.sha256(raw).hexdigest(),
                        "sheets":list_xlsx_sheets(raw),"plaintext_warning":True}
            else:
                cols,rows,digest=read_table(args.source,sheet=args.sheet,
                    header_row=args.header_row,allow_cached_formulas=args.allow_cached_formulas)
                from data2web_profile import profile_table
                result={"status":"LOCAL_INSPECT_NOT_APPROVED","source_sha256":digest,
                        "columns":cols,"rows":len(rows),"sheet":args.sheet,
                        "header_row":args.header_row,"cached_formulas":args.allow_cached_formulas,
                        "profile":profile_table(cols,rows),
                        "plaintext_warning":True,"source_modified":False}
        elif args.action=="build":
            if not args.ack_plaintext:
                raise ValueError("Explicit plaintext acknowledgment required")
            result=build(args.source,args.output,args.id,args.title,args.category,
                         approved=True,expected_sha256=args.source_sha256,
                         name=args.name,theme=args.theme,sheet=args.sheet,
                         header_row=args.header_row,allow_cached_formulas=args.allow_cached_formulas)
            result["status"]="LOCAL_HTML_BUILT_NOT_RELEASE_APPROVED"
            if args.zip_path: result["package"]=package_html(args.output,args.zip_path,result)
            if args.receipt_path:
                from receipt_utils import write_receipt
                result["receipt_file"]=write_receipt(args.receipt_path,result)
        elif args.action=="append":
            from data2web_append import build_approved_append
            result=build_approved_append(args.approval_manifest,args.output,
                        confirm=args.confirm,ack_plaintext=args.ack_plaintext,
                        zip_path=args.zip_path,receipt_path=args.receipt_path)
        elif args.action=="deliver-append":
            from data2web_append import deliver_to_new_directory
            result=deliver_to_new_directory(args.approval_manifest,args.new_directory,
                                             confirm=args.confirm,ack_plaintext=args.ack_plaintext)
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
