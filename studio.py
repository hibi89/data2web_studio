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
    ps=sub.add_parser("deliver")
    ps.add_argument("source",type=Path)
    ps.add_argument("new_directory",type=Path)
    ps.add_argument("--source-sha256",required=True)
    ps.add_argument("--id",required=True);ps.add_argument("--title",required=True)
    ps.add_argument("--category",required=True)
    ps.add_argument("--confirm",choices=["APPROVE"],required=True)
    ps.add_argument("--ack-plaintext",action="store_true",required=True)
    ps.add_argument("--privacy-classification",
          choices=["NO_PERSONAL_DATA_REVIEWED","OWNER_APPROVED_LOCAL_ONLY"],required=True)
    ps.add_argument("--sheet");ps.add_argument("--header-row",type=int,default=1)
    ps.add_argument("--allow-cached-formulas",action="store_true")
    ps.add_argument("--theme",choices=["office","cafe","inventory"],default="office")
    ps.add_argument("--name",default="DATA2WEB")
    sub.add_parser("desktop",help="Open optional local Tkinter owner-review UI (no server)")
    selfcheck=sub.add_parser("self-check",help="Run redacted local synthetic acceptance checks")
    selfcheck.add_argument("--browsers",action="store_true")
    selfcheck.add_argument("--evidence-output",type=Path,
        help="Create-only local unsigned synthetic device report; never uploads customer data")
    pc=sub.add_parser("verify-customer",help="Independently verify a full local customer folder")
    pc.add_argument("directory",type=Path)
    pv=sub.add_parser("verify");pv.add_argument("zip_path",type=Path)
    args=p.parse_args(argv)
    try:
        if args.action=="self-check":
            from client_local_rehearsal import self_check, save_rehearsal_evidence
            result=(save_rehearsal_evidence(args.evidence_output,with_browsers=args.browsers)
                    if args.evidence_output is not None else self_check(with_browsers=args.browsers))
            print(json.dumps(result,ensure_ascii=True,sort_keys=True))
            return 0 if result["status"]=="PASS_SYNTHETIC_ONLY" else 2
        if args.action=="desktop":
            from data2web_desktop import desktop_main
            try:
                desktop_main()
            except KeyboardInterrupt:
                # Console interruption while Tk is running must not turn into a
                # PyInstaller traceback. Preserve all existing input/output and
                # report the interruption (not an acceptance or sale approval).
                print(json.dumps({"status":"INTERRUPTED","action":"desktop",
                                  "sale_approved":False},sort_keys=True))
                return 130
            return 0
        elif args.action=="inspect":
            if args.source.suffix.lower()==".xlsx" and args.sheet is None:
                import hashlib
                from data2web_tabular import list_xlsx_sheets
                from path_policy import read_bounded_source
                # A single identity-checked bounded FD snapshot.
                # Avoid path.stat() -> read_bytes() TOCTOU and unbounded reads.
                raw=read_bounded_source(args.source,max_bytes=8_000_000)
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
        elif args.action=="deliver":
            from data2web_single import deliver_single
            result=deliver_single(args.source,args.new_directory,
                    expected_sha256=args.source_sha256,
                    id_column=args.id,title_column=args.title,category_column=args.category,
                    confirm=args.confirm,ack_plaintext=args.ack_plaintext,
                    privacy_classification=args.privacy_classification,
                    sheet=args.sheet,header_row=args.header_row,
                    allow_cached_formulas=args.allow_cached_formulas,
                    name=args.name,theme=args.theme)
        elif args.action=="verify-customer":
            from verify_customer_folder import verify_customer_folder
            result=verify_customer_folder(args.directory)
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
