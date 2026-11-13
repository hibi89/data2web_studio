"""Actual Tk form button interaction in hosted Windows (CSV and XLSX).

Selects a synthetic input, inspects, chooses optional worksheet, checks privacy
and rights, chooses a fresh folder, generates and independently verifies all
artifacts. No customer data, external network, storage outside CI temp, or GUI
display sharing. This does not replace real Win10/11 customer acceptance.
"""
from __future__ import annotations
import tempfile
from pathlib import Path
from unittest.mock import patch
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from data2web_desktop import desktop_main
from test_xlsx_fixtures import workbook_bytes
from verify_customer_folder import verify_customer_folder

def test_case(source_kind):
    with tempfile.TemporaryDirectory() as directory:
        root_dir=Path(directory)
        source=root_dir/("sample.xlsx" if source_kind=="xlsx" else "sample.csv")
        if source_kind=="xlsx":
            source.write_bytes(workbook_bytes())
            expected_count=2
        else:
            source.write_text("id,title,category,amount\nA1,First,A,4\nA2,Second,B,5\n",encoding="utf-8")
            expected_count=2
        expected_dir=root_dir/"DATA2WEB-customer"
        real_tk=tk.Tk
        evidence={"ran":False,"ui_error":None,"approved":False}

        def synthetic_owner_uses_form(root):
            try:
                visited=[]
                def walk(parent):
                    for child in parent.winfo_children():
                        visited.append(child)
                        walk(child)
                walk(root)
                buttons={}
                for widget in visited:
                    if isinstance(widget,ttk.Button):
                        buttons[widget.cget("text")]=widget
                for needed in ("파일 선택","SHA·열·중복 검수","상위 폴더 선택",
                               "새 고객 폴더 생성·독립 검증"):
                    assert needed in buttons,f"Missing actual desktop button: {needed}"
                buttons["파일 선택"].invoke()
                if source_kind=="xlsx":
                    visible=[widget for widget in visited
                             if isinstance(widget,ttk.Combobox) and "Inventory" in widget.cget("values")]
                    assert len(visible)==1,"XLSX sheet combobox not populated"
                    visible[0].set("Inventory")
                buttons["SHA·열·중복 검수"].invoke()
                approval_boxes=[widget for widget in visited if isinstance(widget,ttk.Checkbutton)]
                assert len(approval_boxes)>=3
                for check in approval_boxes:
                    if check.cget("text").startswith(("이 자료를 사용할 권리","결과 HTML·ZIP")):
                        check.invoke()
                privacy=[widget for widget in visited
                         if isinstance(widget,ttk.Combobox)
                         and "NO_PERSONAL_DATA_REVIEWED" in widget.cget("values")]
                assert len(privacy)==1
                privacy[0].set("NO_PERSONAL_DATA_REVIEWED")
                buttons["상위 폴더 선택"].invoke()
                buttons["새 고객 폴더 생성·독립 검증"].invoke()
                assert expected_dir.is_dir(), "GUI did not actually create the folder"
                assert verify_customer_folder(expected_dir)["rows"]==expected_count
                evidence["approved"]=True
                evidence["ran"]=True
            except Exception as error:
                evidence["ui_error"]=repr(error)
            finally:
                root.destroy()

        def new_root(*args,**kwargs):
            win=real_tk(*args,**kwargs)
            win.after(200,lambda:synthetic_owner_uses_form(win))
            win.after(10000,lambda:win.destroy() if win.winfo_exists() else None)
            return win
        with (patch.object(tk,"Tk",new=new_root),
              patch.object(filedialog,"askopenfilename",return_value=str(source)),
              patch.object(filedialog,"askdirectory",return_value=str(root_dir)),
              patch.object(messagebox,"askyesno",return_value=True),
              patch.object(messagebox,"showinfo",return_value=None)):
            desktop_main()
        assert evidence["ui_error"] is None,evidence["ui_error"]
        assert evidence["approved"] and evidence["ran"],"Desktop interaction not completed"
        return source_kind

def main():
    assert test_case("csv")=="csv"
    assert test_case("xlsx")=="xlsx"
    print("HOSTED_WINDOWS_TK_OWNER_ACTUAL_BUTTON_FLOW_PASS csv+xlsx file-sheet-SHA-mapping-rights/privacy-new_folder-whole_folder_verification; not physical Win10/11 owner signoff")

if __name__=="__main__":
    main()
