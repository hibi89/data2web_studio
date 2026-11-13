"""Synthetic *actual OOXML XLSX* test fixture generator, no customer files.

The workbook has real workbook relationships, XML worksheets and valid ZIP parts.
Optional mutations generate bad XLSX files for fail-closed contract testing.
"""
import io
import zipfile
from xml.etree import ElementTree as E

X = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
E.register_namespace("", X)
E.register_namespace("r", R)

def col(i):
    s = ""
    i += 1
    while i:
        i, rem = divmod(i - 1, 26)
        s = chr(65 + rem) + s
    return s

def workbook_bytes(*, sheets=None, formula=None, cached=None, external=False,
                   merged=False, shared=False, hidden=False, extra_part=None,
                   header_row=1):
    if sheets is None:
        sheets = {"Inventory": [
            ["id", "title", "category", "amount"],
            ["A-01", "한글 상품", "상품", 125],
            ["A-02", "</script><img onerror=alert(1)>", "기타", 0],
        ]}
    shared_values = list(dict.fromkeys(v for rows in sheets.values() for row in rows for v in row if isinstance(v,str)))
    out = io.BytesIO()
    content = E.Element("{%s}Types" % CT)
    E.SubElement(content, "{%s}Default" % CT, {"Extension":"rels","ContentType":"application/vnd.openxmlformats-package.relationships+xml"})
    E.SubElement(content, "{%s}Default" % CT, {"Extension":"xml","ContentType":"application/xml"})
    E.SubElement(content, "{%s}Override" % CT, {"PartName":"/xl/workbook.xml",
        "ContentType":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"})
    book = E.Element("{%s}workbook"%X)
    bs = E.SubElement(book,"{%s}sheets"%X)
    relationships=E.Element("{%s}Relationships"%PKG)
    for num,(name,rows) in enumerate(sheets.items(),1):
        attrs={"name":name,"sheetId":str(num),"{%s}id"%R:"rId"+str(num)}
        if hidden and num==1:attrs["state"]="veryHidden"
        E.SubElement(bs,"{%s}sheet"%X,attrs)
        E.SubElement(relationships,"{%s}Relationship"%PKG,{
            "Id":"rId"+str(num),
            "Type":"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet",
            "Target":"worksheets/sheet"+str(num)+".xml"})
    if external:
        E.SubElement(relationships,"{%s}Relationship"%PKG,{"Id":"rIdEX",
            "Type":"http://schemas.openxmlformats.org/officeDocument/2006/relationships/externalLink",
            "Target":"https://example.invalid/evil.xlsx","TargetMode":"External"})
    pkg_rel=E.Element("{%s}Relationships"%PKG)
    E.SubElement(pkg_rel,"{%s}Relationship"%PKG,{"Id":"p1","Type":
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument",
        "Target":"xl/workbook.xml"})
    with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",E.tostring(content))
        z.writestr("_rels/.rels",E.tostring(pkg_rel))
        z.writestr("xl/workbook.xml",E.tostring(book))
        z.writestr("xl/_rels/workbook.xml.rels",E.tostring(relationships))
        for n,(_,rows) in enumerate(sheets.items(),1):
            worksheet=E.Element("{%s}worksheet"%X)
            data=E.SubElement(worksheet,"{%s}sheetData"%X)
            for rowidx,values in enumerate(rows,header_row):
                row=E.SubElement(data,"{%s}row"%X,{"r":str(rowidx)})
                for idx,v in enumerate(values):
                    if v is None:continue
                    cell=E.SubElement(row,"{%s}c"%X,{"r":col(idx)+str(rowidx)})
                    if formula is not None and rowidx == header_row+1 and idx == 3:
                        E.SubElement(cell,"{%s}f"%X).text=formula
                        if cached is not None:E.SubElement(cell,"{%s}v"%X).text=str(cached)
                    elif isinstance(v,(float,int)) and not isinstance(v,bool):
                        E.SubElement(cell,"{%s}v"%X).text=str(v)
                    elif isinstance(v,bool):
                        cell.set("t","b");E.SubElement(cell,"{%s}v"%X).text="1" if v else "0"
                    elif shared:
                        cell.set("t","s")
                        # generated compact sharedStrings table below is based on all strings
                        E.SubElement(cell,"{%s}v"%X).text=str(shared_values.index(v))
                    else:
                        cell.set("t","inlineStr")
                        inner=E.SubElement(cell,"{%s}is"%X)
                        E.SubElement(inner,"{%s}t"%X).text=v
            if merged:E.SubElement(worksheet,"{%s}mergeCells"%X,{"count":"1"})
            z.writestr("xl/worksheets/sheet"+str(n)+".xml",E.tostring(worksheet,encoding="utf-8"))
        if shared:
            strings=E.Element("{%s}sst"%X)
            for v in shared_values:
                si=E.SubElement(strings,"{%s}si"%X)
                E.SubElement(si,"{%s}t"%X).text=v
            z.writestr("xl/sharedStrings.xml",E.tostring(strings))
        if extra_part is not None:
            z.writestr(extra_part,b"unsafe")
    return out.getvalue()
