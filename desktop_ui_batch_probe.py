"""Real Windows Tk batch wizard acceptance with 2 synthetic source files.

No real customer data, network, credential, seller account or human release.
Tests actual Toplevel buttons and owner re-consent after mapping changes.
"""
from __future__ import annotations

from pathlib import Path
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from unittest.mock import patch

from data2web_desktop import desktop_main
from test_xlsx_fixtures import workbook_bytes
from verify_customer_folder import verify_customer_folder


def run_case(kind):
    with tempfile.TemporaryDirectory(prefix="data2web-batch-gui-") as td:
        rootdir=Path(td)
        a=rootdir/"input.csv"
        a.write_text("id,title,category,amount\nA1,First,X,2\n",encoding="utf-8")
        b=rootdir/("second.xlsx" if kind=="xlsx" else "second.tsv")
        if kind=="xlsx":
            b.write_bytes(workbook_bytes())
        else:
            b.write_text("id\ttitle\tcategory\tamount\nB1\tSecond\tY\t3\n",encoding="utf-8")
        before=(a.read_bytes(),b.read_bytes())
        output=rootdir/"DATA2WEB-batch"
        evidence={"ok":False,"error":None}
        actual_tk=tk.Tk

        def children(window):
            output=[]
            for child in window.winfo_children():
                output.append(child)
                output.extend(children(child))
            return output

        def operate(root):
            try:
                main_buttons={x.cget("text"):x for x in children(root)
                              if isinstance(x,ttk.Button)}
                main_buttons["다중 파일(2~10) 검수·납품"].invoke()
                dialogs=[x for x in root.winfo_children() if isinstance(x,tk.Toplevel)]
                assert len(dialogs)==1, "Multi-source Toplevel did not open"
                dialog=dialogs[0]
                widgets=children(dialog)
                buttons={x.cget("text"):x for x in widgets if isinstance(x,ttk.Button)}
                for caption in ("여러 원본 파일 선택","2~10개 SHA·열 검수",
                                "상위 폴더 선택","새 다중 고객 폴더 생성·검증"):
                    assert caption in buttons, "Missing real batch UI button"
                buttons["여러 원본 파일 선택"].invoke()
                buttons["2~10개 SHA·열 검수"].invoke()
                checks=[x for x in widgets if isinstance(x,ttk.Checkbutton)]
                assert len(checks)==2
                for checkbox in checks:
                    checkbox.invoke()
                    assert checkbox.instate(["selected"])
                privacy=[x for x in widgets if isinstance(x,ttk.Combobox)
                         and "NO_PERSONAL_DATA_REVIEWED" in x.cget("values")]
                assert len(privacy)==1
                privacy[0].set("NO_PERSONAL_DATA_REVIEWED")
                mapping=[x for x in widgets if isinstance(x,ttk.Combobox)
                         and ("id" in x.cget("values")) and
                         ("title" in x.cget("values"))]
                assert len(mapping)==3
                # Change a real field mapping -> all owner approvals are reset.
                mapping[2].set("amount")
                assert all(not x.instate(["selected"]) for x in checks)
                assert privacy[0].get()==""
                mapping[2].set("category")
                # Destination changes invalidate consent just like mapping
                # changes; select it before granting the final scope.
                buttons["상위 폴더 선택"].invoke()
                assert all(not x.instate(["selected"]) for x in checks)
                assert privacy[0].get()==""
                for checkbox in checks:checkbox.invoke()
                privacy[0].set("NO_PERSONAL_DATA_REVIEWED")
                buttons["새 다중 고객 폴더 생성·검증"].invoke()
                assert output.is_dir(), "Batch wizard did not create customer folder"
                result=verify_customer_folder(output)
                assert result["verified"] and result["sale_approved"] is False
                assert result["rows"] == (3 if kind=="xlsx" else 2)
                assert (a.read_bytes(),b.read_bytes())==before
                assert not any(p.suffix==".json" for p in rootdir.iterdir() if p.is_file())
                evidence["ok"]=True
            except Exception as exc:
                evidence["error"]=repr(exc)
            finally:
                root.destroy()

        def start(*args,**kwargs):
            win=actual_tk(*args,**kwargs)
            win.after(180,lambda:operate(win))
            win.after(12000,lambda:win.destroy() if win.winfo_exists() else None)
            return win

        with (patch.object(tk,"Tk",new=start),
              patch.object(filedialog,"askopenfilenames",return_value=(str(a),str(b))),
              patch.object(filedialog,"askdirectory",return_value=str(rootdir)),
              patch.object(simpledialog,"askstring",return_value="Inventory"),
              patch.object(simpledialog,"askinteger",return_value=1),
              patch.object(messagebox,"askyesno",return_value=True),
              patch.object(messagebox,"showinfo",return_value=None)):
            desktop_main()
        assert evidence["ok"] and not evidence["error"],evidence


def main():
    run_case("tsv")
    run_case("xlsx")
    print("HOSTED_WINDOWS_REAL_TK_MULTI_SOURCE_GUI_PASS CSV+TSV CSV+XLSX source-SHA-mapping-reconsent-create-only-ZIP-receipt; NOT buyer OS signoff")


if __name__=="__main__":
    main()
