"""Offline desktop owner-review wizard (Tkinter; no SaaS and no customer upload).

This UI is an optional convenience for customers with Python 3.11 + Tcl/Tk.
All source handling uses the same reviewed CLI core and fail-closed SHA gates.
Importing this module does NOT open a window or require a display.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from data2web import MAX_BYTES, read_table
from data2web_profile import profile_table
from data2web_single import deliver_single
from path_policy import assert_no_links, read_bounded_source

PRIVACY_CHOICES=("NO_PERSONAL_DATA_REVIEWED","OWNER_APPROVED_LOCAL_ONLY")
THEMES=("office","cafe","inventory")


@dataclass(frozen=True)
class ReviewedInput:
    source: Path
    sha256: str
    columns: tuple[str, ...]
    count: int
    sheet: str | None
    header_row: int
    allow_cached_formulas: bool
    profile: dict


def inspect_sheets(path):
    p=Path(path)
    assert_no_links(p)
    if p.suffix.lower()!=".xlsx" or not p.is_file():
        raise ValueError("A regular, bounded XLSX file is required")
    from data2web_tabular import list_xlsx_sheets
    data=read_bounded_source(p,max_bytes=MAX_BYTES)
    return [s["name"] for s in list_xlsx_sheets(data) if s["state"]=="visible"]


def inspect_owner_input(path, *, sheet=None, header_row=1, allow_cached_formulas=False):
    p=Path(path)
    if p.suffix.lower()==".xlsx" and not sheet:
        raise ValueError("Select the exact visible worksheet before inspection")
    columns,rows,digest=read_table(p,sheet=sheet,header_row=header_row,
                                   allow_cached_formulas=allow_cached_formulas)
    return ReviewedInput(source=p,sha256=digest,columns=tuple(columns),
                         count=len(rows),sheet=sheet,header_row=header_row,
                         allow_cached_formulas=allow_cached_formulas,
                         profile=profile_table(columns,rows))


def deliver_reviewed(review, destination, mapping, *, owner_has_rights,
                     plaintext_ack, privacy_classification, name="DATA2WEB",
                     theme="office"):
    if not isinstance(review,ReviewedInput):
        raise ValueError("Input was not independently inspected")
    if owner_has_rights is not True or plaintext_ack is not True:
        raise ValueError("Owner must explicitly review rights and plaintext copying")
    if privacy_classification not in PRIVACY_CHOICES or theme not in THEMES:
        raise ValueError("Privacy review and valid theme must be selected")
    if not isinstance(mapping,dict) or set(mapping)!={"id","title","category"} or (
            len(set(mapping.values()))!=3) or not all(value in review.columns for value in mapping.values()):
        raise ValueError("Confirm three distinct existing ID/title/category columns")
    # Same SHA, worksheet, header position and cache policy reviewed before build.
    return deliver_single(review.source,destination,
         expected_sha256=review.sha256,
         id_column=mapping["id"],title_column=mapping["title"],
         category_column=mapping["category"],
         confirm="APPROVE",ack_plaintext=True,
         privacy_classification=privacy_classification,sheet=review.sheet,
         header_row=review.header_row,
         allow_cached_formulas=review.allow_cached_formulas,
         name=name,theme=theme)


def inspect_owner_batch(sources, *, options=None):
    """Review 2-10 same-directory files without creating a manifest on disk.

    Every input is parsed independently; all must share the exact ordered
    header schema. The unchanged SHA and per-XLSX sheet/cache preferences
    are carried into the final checked append core.
    """
    paths=tuple(Path(source) for source in sources)
    if not 2<=len(paths)<=10:
        raise ValueError("Select two to ten sources for the batch")
    configurations=tuple(options) if options is not None else tuple({} for _ in paths)
    if len(configurations)!=len(paths):
        raise ValueError("A separate configuration is required per source")
    origin=paths[0].absolute().parent
    assert_no_links(origin)
    keys=set()
    reviewed=[]
    total=0
    original_columns=None
    for path,settings in zip(paths,configurations):
        assert_no_links(path)
        if path.absolute().parent!=origin or path.name.casefold() in keys:
            raise ValueError("Batch files must have distinct names in one real folder")
        keys.add(path.name.casefold())
        if not isinstance(settings,dict) or set(settings)-{
                "sheet","header_row","allow_cached_formulas"}:
            raise ValueError("Only XLSX sheet/header/cache settings are permitted")
        if path.suffix.lower()!=".xlsx" and (
                settings.get("sheet") is not None or
                settings.get("header_row",1)!=1 or
                settings.get("allow_cached_formulas",False) is not False):
            raise ValueError("Non-XLSX file cannot use workbook-specific settings")
        review=inspect_owner_input(path,**settings)
        if original_columns is None:
            original_columns=review.columns
        elif review.columns!=original_columns:
            raise ValueError("All batch sources need identical ordered headers")
        total+=review.count
        from data2web import MAX_ROWS
        if total>MAX_ROWS:
            raise ValueError("Combined row limit exceeded")
        reviewed.append(review)
    return tuple(reviewed)


def deliver_reviewed_batch(reviews,destination,mapping,*,
                           owner_has_rights,plaintext_ack,
                           privacy_classification,name="DATA2WEB",theme="office"):
    """Build a single delivery folder from explicitly reviewed multiple files.

    Source SHA, ordered headers and cross-source duplicate IDs are rechecked by
    the existing append engine; this is not a commercial rights certificate.
    """
    items=tuple(reviews)
    if not 2<=len(items)<=10 or any(not isinstance(r,ReviewedInput) for r in items):
        raise ValueError("Batch delivery requires two to ten inspected records")
    if owner_has_rights is not True or plaintext_ack is not True:
        raise ValueError("Explicit batch source rights and plaintext review required")
    if privacy_classification not in PRIVACY_CHOICES or theme not in THEMES:
        raise ValueError("Privacy classification and theme required")
    if (not isinstance(mapping,dict) or set(mapping)!={"id","title","category"}
            or not all(isinstance(x,str) and x for x in mapping.values())
            or len(set(mapping.values()))!=3
            or not all(value in items[0].columns for value in mapping.values())):
        raise ValueError("Three distinct approved batch field mappings required")
    source_dir=items[0].source.absolute().parent
    if any(r.source.absolute().parent!=source_dir or r.columns!=items[0].columns
           for r in items):
        raise ValueError("Batch reviews must describe same-folder identical columns")
    doc={
        "contract":"DATA2WEB_INPUT_APPROVALS_V1",
        "sources":[{
            "filename":r.source.name,"sha256":r.sha256,"sheet":r.sheet,
            "header_row":r.header_row,
            "allow_cached_formulas":r.allow_cached_formulas,
        } for r in items],
        "mapping":dict(mapping),
        "approval":{"rights_and_plaintext_ack":True,
                    "privacy_classification":privacy_classification},
        "name":name,"theme":theme,
    }
    from data2web_append import deliver_reviewed_sources
    return deliver_reviewed_sources(doc,source_dir,destination,
                    confirm="APPROVE",ack_plaintext=True)


def desktop_main():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except ImportError as error:
        raise RuntimeError("Tkinter/Tcl/Tk is required for the optional local desktop UI") from error

    root=tk.Tk()
    root.title("DATA2WEB Studio — 로컬 데이터 검수")
    root.minsize(850,690)
    root.geometry("980x780")
    root.configure(bg="#eff3f7")
    font=("Malgun Gothic",10)
    style=ttk.Style(root)
    for variant in ("clam","vista"):
        if variant in style.theme_names():
            style.theme_use(variant)
            break
    style.configure("TLabel",font=font)
    style.configure("TButton",font=font,padding=6)
    style.configure("TCheckbutton",font=font)
    style.configure("TCombobox",font=font)
    frame=ttk.Frame(root,padding=18)
    frame.pack(fill="both",expand=True)
    frame.columnconfigure(1,weight=1)

    source=tk.StringVar()
    sheet=tk.StringVar()
    header=tk.IntVar(value=1)
    cached=tk.BooleanVar(value=False)
    id_key=tk.StringVar()
    title_key=tk.StringVar()
    category_key=tk.StringVar()
    title=tk.StringVar(value="DATA2WEB")
    theme=tk.StringVar(value="office")
    parent=tk.StringVar()
    folder=tk.StringVar(value="DATA2WEB-customer")
    rights=tk.BooleanVar(value=False)
    plaintext=tk.BooleanVar(value=False)
    privacy=tk.StringVar(value="")
    message=tk.StringVar(value="1. 원본을 선택하세요. 이 프로그램은 파일을 서버로 전송하지 않습니다.")
    reviewed=[None]

    def label(row,text):
        ttk.Label(frame,text=text).grid(row=row,column=0,sticky="w",padx=(0,12),pady=6)

    label(0,"원본 파일")
    ttk.Entry(frame,textvariable=source,state="readonly").grid(row=0,column=1,sticky="ew",pady=6)
    label(1,"XLSX 시트")
    sheets=ttk.Combobox(frame,textvariable=sheet,state="readonly")
    sheets.grid(row=1,column=1,sticky="ew",pady=5)
    label(2,"헤더 행 / 수식 캐시")
    row2=ttk.Frame(frame);row2.grid(row=2,column=1,sticky="w")
    ttk.Spinbox(row2,from_=1,to=50,textvariable=header,width=6).pack(side="left")
    ttk.Checkbutton(row2,text="Excel 수식의 미재계산 캐시 사용을 승인",variable=cached).pack(side="left",padx=14)

    label(3,"데이터 검수 정보")
    sha=tk.StringVar(value="검수 전")
    ttk.Label(frame,textvariable=sha,wraplength=650).grid(row=3,column=1,sticky="w")
    table=ttk.Treeview(frame,columns=("name","kind","blank","duplicate"),show="headings",height=9)
    for key,value,width in (("name","컬럼",260),("kind","자료형 힌트",160),
                            ("blank","빈 셀",75),("duplicate","중복 비어있지 않은 셀",175)):
        table.heading(key,text=value)
        table.column(key,width=width)
    table.grid(row=4,column=0,columnspan=3,sticky="nsew",pady=8)
    frame.rowconfigure(4,weight=1)

    label(5,"ID / 제목 / 분류 컬럼")
    mapping_frame=ttk.Frame(frame);mapping_frame.grid(row=5,column=1,sticky="ew")
    fields=[]
    for descriptor,value in (("ID",id_key),("제목",title_key),("분류",category_key)):
        ttk.Label(mapping_frame,text=descriptor).pack(side="left",padx=(0,4))
        box=ttk.Combobox(mapping_frame,textvariable=value,state="readonly",width=17)
        box.pack(side="left",padx=(0,12))
        fields.append(box)
    label(6,"앱 제목 / 테마")
    options=ttk.Frame(frame);options.grid(row=6,column=1,sticky="ew")
    ttk.Entry(options,textvariable=title,width=34).pack(side="left",padx=(0,10))
    ttk.Combobox(options,textvariable=theme,values=THEMES,state="readonly",width=15).pack(side="left")

    label(7,"새 고객 폴더 위치")
    location=ttk.Frame(frame);location.grid(row=7,column=1,sticky="ew")
    location.columnconfigure(0,weight=1)
    ttk.Entry(location,textvariable=parent,state="readonly").grid(row=0,column=0,sticky="ew")
    ttk.Button(location,text="상위 폴더 선택",command=lambda:parent.set(
        filedialog.askdirectory(parent=root,title="새 고객 폴더를 만들 위치") or parent.get())).grid(row=0,column=1,padx=6)
    ttk.Entry(location,textvariable=folder).grid(row=1,column=0,sticky="ew",pady=6)
    ttk.Label(location,text="기존 폴더명 사용 금지; 새 디렉터리만 생성").grid(row=1,column=1)
    label(8,"필수 권리·개인정보 검수")
    checks=ttk.Frame(frame);checks.grid(row=8,column=1,sticky="w")
    ttk.Checkbutton(checks,text="이 자료를 사용할 권리를 직접 확인했습니다",variable=rights).pack(anchor="w")
    ttk.Checkbutton(checks,text="결과 HTML·ZIP에 자료가 평문으로 포함되는 것을 이해합니다",variable=plaintext).pack(anchor="w")
    ttk.Label(checks,text="개인정보 검수 상태 (자동 법적 승인 아님)").pack(anchor="w",pady=(5,0))
    ttk.Combobox(checks,textvariable=privacy,values=PRIVACY_CHOICES,state="readonly",width=38).pack(anchor="w")

    def reset_consent(*_):
        # Rights/PII/plaintext acknowledgement belongs to this exact reviewed
        # dataset AND its ID/title/category mapping, never to a previous file.
        rights.set(False)
        plaintext.set(False)
        privacy.set("")

    def reset_review():
        reviewed[0]=None
        reset_consent()
        sha.set("검수 전 — 변경된 설정은 반드시 다시 검수하세요")
        for box in fields:
            box["values"]=()
        for mapped in (id_key,title_key,category_key):
            mapped.set("")
        for child in table.get_children():
            table.delete(child)

    for var in (source,sheet,header,cached):
        var.trace_add("write",lambda *_:reset_review())
    for var in (id_key,title_key,category_key,parent,folder):
        # Destination changes may change the recipient or delivery scope.
        var.trace_add("write",reset_consent)

    def choose_source():
        chosen=filedialog.askopenfilename(parent=root,title="고객 소유 표 데이터",
                 filetypes=[("표 데이터","*.csv *.json *.tsv *.xlsx"),("모든 파일","*.*")])
        if not chosen:return
        reset_review()
        source.set(chosen)
        sheet.set("")
        sheets["values"]=()
        if Path(chosen).suffix.lower()==".xlsx":
            try:
                visible=inspect_sheets(chosen)
                sheets["values"]=visible
                message.set("XLSX의 검토할 시트를 선택하고 검수하세요 (자동 선택하지 않음).")
            except (ValueError,OSError) as error:
                message.set("HOLD: 안전한 XLSX 시트 목록을 읽지 못했습니다.")
        else:
            message.set("원본 선택 완료. 컬럼 검수를 실행하세요.")
    ttk.Button(frame,text="파일 선택",command=choose_source).grid(row=0,column=2,padx=6,pady=6)

    def inspect():
        try:
            data=inspect_owner_input(source.get(),sheet=sheet.get() or None,
                      header_row=header.get(),allow_cached_formulas=cached.get())
            reviewed[0]=data
            for item in table.get_children():table.delete(item)
            for col in data.profile["columns"]:
                table.insert("",tk.END,values=(col["name"],col["kind_hint"],
                                     col["blank_cells"],col["duplicate_nonblank"]))
            for box in fields:box["values"]=data.columns
            for v,guess in ((id_key,"id"),(title_key,"title"),(category_key,"category")):
                v.set(guess if guess in data.columns else "")
            sha.set(f"SHA256: {data.sha256} | {data.count}행 / {len(data.columns)}열. 셀 값 표시·전송 없음.")
            message.set("검수 완료. 컬럼·사용권·개인정보를 확인하고 새 고객 폴더를 지정하세요.")
        except (ValueError,OSError,UnicodeError) as error:
            reset_review()
            message.set("HOLD: 읽기 오류·시트/헤더 불일치·원본 제한에 걸렸습니다.")
    ttk.Button(frame,text="SHA·열·중복 검수",command=inspect).grid(row=3,column=2,padx=6)

    def deliver():
        current=reviewed[0]
        if current is None:
            message.set("HOLD: 원본 SHA·컬럼을 먼저 검수하세요.");return
        if not parent.get() or not folder.get().strip() or Path(folder.get()).name!=folder.get().strip() or (
                "/" in folder.get() or "\\" in folder.get() or folder.get() in (".","..")):
            message.set("HOLD: 상위 폴더와 새로운 단순 폴더명을 지정하세요.");return
        destination=Path(parent.get())/folder.get()
        if not messagebox.askyesno("DATA2WEB 출력 전 최종 확인",
             f"검수 SHA256: {current.sha256}\\n파일: {current.source.name}\\n"
             f"행: {current.count} · 시트: {current.sheet or '해당 없음'}\\n"
             "출력에 원본 값이 평문으로 포함됩니다. 판매/사용권 최종 승인과 별개입니다.\\n"
             "새 폴더에 HTML·ZIP·영수증을 생성하시겠습니까?",parent=root):
            message.set("승인 취소: 기존 파일 변경 없음");return
        try:
            receipt=deliver_reviewed(current,destination,
                 {"id":id_key.get(),"title":title_key.get(),"category":category_key.get()},
                 owner_has_rights=rights.get(),plaintext_ack=plaintext.get(),
                 privacy_classification=privacy.get(),
                 name=title.get(),theme=theme.get())
            from verify_customer_folder import verify_customer_folder
            passed=verify_customer_folder(destination)
            if not passed["verified"] or receipt["rows"]!=current.count:
                raise ValueError("Independent ZIP verification mismatch")
            message.set("로컬 생성·독립 검증 PASS · 고객 상업 납품은 RELEASE HOLD. 폴더를 수동 검수하세요.")
            messagebox.showinfo("생성 검증",f"생성·독립 ZIP 검사 완료\\n{destination}\\n"
               "상업적 납품은 별도 권리·계약·고객 승인 전 HOLD입니다.",parent=root)
        except (ValueError,FileExistsError,OSError) as error:
            message.set("HOLD: 무덮어쓰기·원본 SHA/매핑·권리 승인·출력 한도를 확인하세요. 기존 자료는 삭제하지 않았습니다.")
    def open_batch_window():
        """Second owner-only wizard: 2-10 exact-order files, same safe folder."""
        from tkinter import simpledialog
        win=tk.Toplevel(root)
        win.title("DATA2WEB — 다중 원본 검수·납품")
        win.geometry("900x680")
        win.minsize(760,610)
        content=ttk.Frame(win,padding=16)
        content.pack(fill="both",expand=True)
        content.columnconfigure(1,weight=1)
        chosen=[()]
        options=[()]
        batch_reviews=[None]
        files_label=tk.StringVar(value="2~10개 표 파일을 동일 폴더에서 선택하세요.")
        batch_message=tk.StringVar(value="검수 전 · 서버 전송 없음 · 실제 데이터 값은 표시하지 않음")
        batch_id=tk.StringVar()
        batch_title=tk.StringVar()
        batch_category=tk.StringVar()
        batch_name=tk.StringVar(value="DATA2WEB")
        batch_theme=tk.StringVar(value="office")
        batch_parent=tk.StringVar()
        batch_leaf=tk.StringVar(value="DATA2WEB-batch")
        batch_rights=tk.BooleanVar(value=False)
        batch_plaintext=tk.BooleanVar(value=False)
        batch_privacy=tk.StringVar(value="")

        def clear_batch_consent(*_):
            batch_rights.set(False)
            batch_plaintext.set(False)
            batch_privacy.set("")

        for variable in (batch_id,batch_title,batch_category,batch_parent,batch_leaf):
            # Never carry a previous recipient/scope approval to a new folder.
            variable.trace_add("write",clear_batch_consent)

        def clear_batch_review():
            batch_reviews[0]=None
            clear_batch_consent()
            for variable in (batch_id,batch_title,batch_category):
                variable.set("")
            for field in combos:
                field["values"]=()

        def select_batch_sources():
            names=filedialog.askopenfilenames(
                parent=win,title="같은 폴더의 표 자료 2~10개 선택",
                filetypes=[("표 데이터","*.csv *.tsv *.json *.xlsx"),("모든 파일","*.*")]
            )
            if not names:return
            clear_batch_review()
            try:
                if not 2<=len(names)<=10:
                    raise ValueError("2~10개 원본만 선택")
                selected=tuple(Path(value) for value in names)
                specs=[]
                for src in selected:
                    if src.suffix.lower()==".xlsx":
                        visible=inspect_sheets(src)
                        if not visible:
                            raise ValueError("Visible XLSX sheet is required")
                        selection=simpledialog.askstring(
                            "XLSX 시트 명시 선택",
                            src.name+"\n사용 가능한 시트:\n"+"\n".join(visible),
                            initialvalue=visible[0],parent=win)
                        if selection not in visible:
                            raise ValueError("XLSX 시트를 명시 선택해야 합니다")
                        header_row=simpledialog.askinteger(
                            "XLSX 헤더행","검수할 헤더행 (1~50)",
                            initialvalue=1,minvalue=1,maxvalue=50,parent=win)
                        if header_row is None:
                            raise ValueError("XLSX 헤더행 선택을 취소했습니다")
                        cached=messagebox.askyesno(
                            "수식 캐시 정책",
                            "Excel 수식이 포함됐다면 저장된 캐시값만 사용합니다."
                            "\n실제 수식 계산이 아닌 캐시 사용을 승인합니까?",
                            parent=win)
                        specs.append({"sheet":selection,
                                      "header_row":header_row,
                                      "allow_cached_formulas":cached})
                    else:
                        specs.append({})
                chosen[0]=selected
                options[0]=tuple(specs)
                files_label.set(str(len(selected))+"개 선택 · 헤더와 원본 SHA 검수 필요")
                batch_message.set("검수 전 · 권리/개인정보 동의는 초기화됨")
            except (OSError,ValueError,UnicodeError):
                chosen[0]=()
                options[0]=()
                files_label.set("HOLD: 원본/시트/헤더 선택이 유효하지 않습니다.")
                batch_message.set("HOLD: 다시 파일을 선택하세요. 기존 자료는 변경하지 않았습니다.")

        def inspect_batch_selection():
            clear_batch_review()
            try:
                values=inspect_owner_batch(chosen[0],options=options[0])
                batch_reviews[0]=values
                for field in combos:
                    field["values"]=values[0].columns
                for variable,guess in ((batch_id,"id"),(batch_title,"title"),
                                       (batch_category,"category")):
                    variable.set(guess if guess in values[0].columns else "")
                files_label.set(str(len(values))+"개 SHA 검수 완료 / 총 "+
                                str(sum(v.count for v in values))+"행 / "+
                                str(len(values[0].columns))+"열")
                batch_message.set("다중 검수 완료 · 서로 다른 세 컬럼·자료 권리·평문 동의 필요")
            except (ValueError,OSError,UnicodeError):
                batch_message.set("HOLD: 파일별 SHA·시트·헤더·열순서/행수 확인 실패.")

        ttk.Button(content,text="여러 원본 파일 선택",command=select_batch_sources).grid(
            row=0,column=0,sticky="ew",pady=5)
        ttk.Label(content,textvariable=files_label,wraplength=650).grid(
            row=0,column=1,sticky="w")
        ttk.Button(content,text="2~10개 SHA·열 검수",command=inspect_batch_selection).grid(
            row=1,column=0,sticky="ew",pady=5)
        ttk.Label(content,text="여러 파일은 순서가 동일한 컬럼만 행 결합; JOIN 없음").grid(
            row=1,column=1,sticky="w")
        ttk.Label(content,text="ID / 제목 / 분류").grid(row=2,column=0,sticky="w",pady=6)
        mapping_frame=ttk.Frame(content)
        mapping_frame.grid(row=2,column=1,sticky="w")
        combos=[]
        for caption,var in (("ID",batch_id),("제목",batch_title),("분류",batch_category)):
            ttk.Label(mapping_frame,text=caption).pack(side="left",padx=3)
            combo=ttk.Combobox(mapping_frame,textvariable=var,state="readonly",width=16)
            combo.pack(side="left",padx=5)
            combos.append(combo)
        ttk.Label(content,text="앱 이름 / 테마").grid(row=3,column=0,sticky="w")
        opts=ttk.Frame(content)
        opts.grid(row=3,column=1,sticky="w")
        ttk.Entry(opts,textvariable=batch_name,width=34).pack(side="left",padx=4)
        ttk.Combobox(opts,textvariable=batch_theme,values=THEMES,
                     state="readonly",width=16).pack(side="left",padx=4)
        ttk.Label(content,text="새 폴더 생성 위치").grid(row=4,column=0,sticky="w",pady=6)
        location=ttk.Frame(content)
        location.grid(row=4,column=1,sticky="ew")
        location.columnconfigure(0,weight=1)
        ttk.Entry(location,textvariable=batch_parent,state="readonly").grid(
            row=0,column=0,sticky="ew")
        ttk.Button(location,text="상위 폴더 선택",command=lambda:batch_parent.set(
            filedialog.askdirectory(parent=win,title="새 다중 납품 폴더 위치") or
            batch_parent.get())).grid(row=0,column=1,padx=5)
        ttk.Entry(location,textvariable=batch_leaf).grid(row=1,column=0,sticky="ew",pady=5)
        ttk.Label(location,text="기존 폴더 덮어쓰기 불가").grid(row=1,column=1)
        ttk.Label(content,text="권리·평문·개인정보").grid(row=5,column=0,sticky="nw")
        privacy_frame=ttk.Frame(content)
        privacy_frame.grid(row=5,column=1,sticky="w")
        ttk.Checkbutton(privacy_frame,text="모든 원본에 대한 사용 권리를 확인했습니다",
                        variable=batch_rights).pack(anchor="w")
        ttk.Checkbutton(privacy_frame,text="결과 HTML·ZIP에 모든 원본 값이 평문 포함됨을 이해합니다",
                        variable=batch_plaintext).pack(anchor="w")
        ttk.Combobox(privacy_frame,textvariable=batch_privacy,
                     values=PRIVACY_CHOICES,state="readonly",width=40).pack(anchor="w",pady=6)

        def deliver_batch_selection():
            current=batch_reviews[0]
            leaf=batch_leaf.get()
            if current is None or not batch_parent.get() or not leaf.strip() or (
                    Path(leaf).name!=leaf or "/" in leaf or "\\" in leaf or
                    leaf in (".","..")):
                batch_message.set("HOLD: 새 폴더명/상위 폴더 및 SHA 검수를 먼저 확인하세요")
                return
            if not batch_rights.get() or not batch_plaintext.get() or (
                    batch_privacy.get() not in PRIVACY_CHOICES):
                batch_message.set("HOLD: 전체 파일 권리·평문·개인정보 검수가 필요합니다")
                return
            destination=Path(batch_parent.get())/leaf
            if not messagebox.askyesno(
                    "다중 데이터 오프라인 납품 확인",
                    str(len(current))+"개 SHA 검수·총 "+
                    str(sum(r.count for r in current))+"행을 새 폴더로 생성합니다."
                    "\n데이터 값은 평문으로 저장됩니다. 법적 판매 승인은 별도입니다.",
                    parent=win):
                batch_message.set("승인 취소 · 기존 원본/출력 불변")
                return
            try:
                result=deliver_reviewed_batch(
                    current,destination,
                    {"id":batch_id.get(),"title":batch_title.get(),
                     "category":batch_category.get()},
                    owner_has_rights=batch_rights.get(),
                    plaintext_ack=batch_plaintext.get(),
                    privacy_classification=batch_privacy.get(),
                    name=batch_name.get(),theme=batch_theme.get())
                from verify_customer_folder import verify_customer_folder
                checked=verify_customer_folder(destination)
                if not checked["verified"] or result["rows"]!=sum(r.count for r in current):
                    raise ValueError("Independent multi-source delivery failed")
                batch_message.set("다중 납품 로컬 생성·독립 검증 PASS · 판매/고객 전달은 RELEASE HOLD")
                messagebox.showinfo(
                    "다중 납품 기술 검증","HTML·ZIP·영수증 검증 PASS\n"+
                    str(destination)+"\n상업용 판매/외부 검수는 별도 승인 전 HOLD",parent=win)
            except (ValueError,OSError,FileExistsError):
                batch_message.set("HOLD: SHA/열순서/중복ID/사용권/무덮어쓰기 제한. 기존 자료 자동 삭제 없음.")

        ttk.Button(content,text="새 다중 고객 폴더 생성·검증",
                   command=deliver_batch_selection).grid(
            row=6,column=0,columnspan=2,sticky="ew",pady=14)
        ttk.Label(content,textvariable=batch_message,
                  foreground="#9d271d",wraplength=800).grid(
            row=7,column=0,columnspan=2,sticky="w")
        ttk.Label(content,
                  text="오프라인 · 2~10 동일 헤더 파일 · 최대 10,000행 · "
                       "승인 없는 고객 자료 처리/판매 불가",
                  wraplength=800).grid(row=8,column=0,columnspan=2,sticky="w",pady=8)

    ttk.Button(frame,text="새 고객 폴더 생성·독립 검증",command=deliver).grid(
        row=9,column=0,columnspan=3,sticky="ew",pady=15)
    ttk.Button(frame,text="다중 파일(2~10) 검수·납품",command=open_batch_window).grid(
        row=10,column=0,columnspan=3,sticky="ew",pady=7)
    ttk.Label(frame,textvariable=message,wraplength=880,
              foreground="#9d271d").grid(row=11,column=0,columnspan=3,sticky="w")
    ttk.Label(frame,text="오프라인 · 원본 읽기 전용 · 프로그램의 SHA는 법적 사용권/개인정보 적합성 인증이 아닙니다.",
              wraplength=900).grid(row=12,column=0,columnspan=3,sticky="w",pady=6)
    root.mainloop()


if __name__=="__main__":
    desktop_main()
