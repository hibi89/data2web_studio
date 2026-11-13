"""P70 workbook/TSV parser regression, bad XLSX holdouts and end-to-end build."""
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from data2web import read_table, build
from data2web_tabular import list_xlsx_sheets
from delivery import package_html
from verify_delivery import verify_zip
from test_xlsx_fixtures import workbook_bytes

DIR=Path(__file__).resolve().parent

class P70XlsxTsv(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.xlsx=self.root/"sample.xlsx"
        self.html=self.root/"output.html"
        self.tsv=self.root/"sample.tsv"
        self.xlsx.write_bytes(workbook_bytes())

    def load_xlsx(self,raw=None,**kwargs):
        if raw is not None:self.xlsx.write_bytes(raw)
        return read_table(self.xlsx,**kwargs)

    def build_xlsx(self,**kwargs):
        digest=hashlib.sha256(self.xlsx.read_bytes()).hexdigest()
        return build(self.xlsx,self.html,"id","title","category",True,
                     expected_sha256=digest,sheet="Inventory",**kwargs)

    def test_valid_xlsx_rows(self):
        fields,rows,sha=self.load_xlsx(sheet="Inventory")
        self.assertEqual(fields,["id","title","category","amount"])
        self.assertEqual(rows[0]["title"],"한글 상품")
        self.assertEqual(rows[0]["amount"],"125")
        self.assertEqual(rows[1]["amount"],"0")
        self.assertEqual(len(sha),64)

    def test_xlsx_sheet_list(self):
        info=list_xlsx_sheets(self.xlsx.read_bytes())
        self.assertEqual(info,[{"name":"Inventory","state":"visible"}])

    def test_xlsx_multiple_sheets_select(self):
        data=workbook_bytes(sheets={
            "First":[["id","title","category"],["F1","First row","X"]],
            "Second":[["id","title","category"],["S1","Second row","Y"]],
        })
        self.assertRaises(ValueError,self.load_xlsx,data)
        cols,rows,_=self.load_xlsx(sheet="Second")
        self.assertEqual(cols,["id","title","category"])
        self.assertEqual(rows[0]["id"],"S1")

    def test_xlsx_wrong_sheet(self):
        with self.assertRaises(ValueError):self.load_xlsx(sheet="other")

    def test_xlsx_hidden_sheet(self):
        with self.assertRaises(ValueError):self.load_xlsx(workbook_bytes(hidden=True))
        with self.assertRaises(ValueError):self.load_xlsx(sheet="Inventory")

    def test_xlsx_header_row_three(self):
        data=workbook_bytes(header_row=3)
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")
        fields,rows,_=self.load_xlsx(sheet="Inventory",header_row=3)
        self.assertEqual(rows[0]["id"],"A-01")

    def test_xlsx_header_row_bounds(self):
        for n in (0,51,-1,1.5,True):
            with self.subTest(header_row=n):
                with self.assertRaises(ValueError):self.load_xlsx(sheet="Inventory",header_row=n)

    def test_xlsx_real_html_build(self):
        r=self.build_xlsx()
        self.assertEqual(r["rows"],2)
        self.assertEqual(r["sheet"],"Inventory")
        text=self.html.read_text(encoding="utf-8")
        self.assertIn('"source_sheet":"Inventory"',text)
        self.assertNotIn("</script><img",text)

    def test_xlsx_zip_verifier_bindings(self):
        r=self.build_xlsx()
        zip_path=self.root/"package.zip"
        package_html(self.html,zip_path,r)
        self.assertTrue(verify_zip(zip_path)["verified"])
        with zipfile.ZipFile(zip_path) as z:
            m=json.loads(z.read("manifest.json"))
            self.assertEqual(m["sheet"],"Inventory")
            self.assertEqual(m["header_row"],1)
            self.assertEqual(m["source_sha256"],r["source_sha256"])

    def test_xlsx_format_no_overwrite(self):
        self.html.write_text("KEEP",encoding="utf-8")
        with self.assertRaises(FileExistsError):self.build_xlsx()
        self.assertEqual(self.html.read_text(),"KEEP")

    def test_xlsx_sha_changed(self):
        with self.assertRaises(ValueError):
            build(self.xlsx,self.html,"id","title","category",True,
                  expected_sha256="a"*64,sheet="Inventory")
        self.assertFalse(self.html.exists())

    def test_xlsx_formula_default_hold(self):
        data=workbook_bytes(formula="1+2",cached=3)
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")
        self.assertFalse(self.html.exists())

    def test_xlsx_formula_cached_requires_approval(self):
        data=workbook_bytes(formula="1+2",cached=3)
        self.load_xlsx(data,sheet="Inventory",allow_cached_formulas=True)
        result=self.build_xlsx(allow_cached_formulas=True)
        self.assertTrue(result["cached_formulas"])
        self.assertEqual(result["rows"],2)
        self.assertIn('"cached_formulas":true',self.html.read_text(encoding="utf-8"))

    def test_xlsx_formula_missing_cache_hold(self):
        data=workbook_bytes(formula="=NOW()",cached=None)
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory",allow_cached_formulas=True)

    def test_xlsx_external_link_hold(self):
        data=workbook_bytes(external=True)
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_macro_part_hold(self):
        data=workbook_bytes(extra_part="xl/vbaProject.bin")
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_traversal_part_hold(self):
        data=workbook_bytes(extra_part="../attack.xml")
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_unknown_embedded_part_hold(self):
        data=workbook_bytes(extra_part="xl/embeddings/oleObject1.bin")
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_unsupported_xml_part_hold(self):
        data=workbook_bytes(extra_part="xl/externalLinks/externalLink1.xml")
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_merged_cells_hold(self):
        data=workbook_bytes(merged=True)
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_duplicate_headers_hold(self):
        data=workbook_bytes(sheets={"Inventory":[["id","title","title"],["a","b","c"]]})
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_unmapped_header_gap_hold(self):
        data=workbook_bytes(sheets={"Inventory":[["id",None,"category"],["a","b","c"]]})
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_reserved_header_hold(self):
        data=workbook_bytes(sheets={"Inventory":[["id","title","category","__proto__"],["a","b","c","d"]]})
        with self.assertRaises(ValueError):self.load_xlsx(data,sheet="Inventory")

    def test_xlsx_bad_signature_hold(self):
        with self.assertRaises(ValueError):self.load_xlsx(b"This is not ZIP",sheet="Inventory")

    def test_xlsx_truncated_zip_hold(self):
        with self.assertRaises(ValueError):self.load_xlsx(b"PK\x03\x04"+"junk".encode(),sheet="Inventory")

    def test_xlsx_duplicate_members_hold(self):
        original=workbook_bytes()
        out=io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(original)) as z,zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as w:
            for x in z.namelist():w.writestr(x,z.read(x))
            w.writestr("xl/workbook.xml",b"<unsafe/>")
        with self.assertRaises(ValueError):self.load_xlsx(out.getvalue(),sheet="Inventory")

    def test_xlsx_xml_entity_hold(self):
        base=workbook_bytes()
        out=io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(base)) as z,zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as w:
            for x in z.namelist():
                data=z.read(x)
                if x=="xl/workbook.xml":data=b'<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>'+data
                w.writestr(x,data)
        with self.assertRaises(ValueError):self.load_xlsx(out.getvalue(),sheet="Inventory")

    def test_xlsx_bad_xml_hold(self):
        base=workbook_bytes()
        out=io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(base)) as z,zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as w:
            for x in z.namelist():
                w.writestr(x,b"<invalid" if x=="xl/workbook.xml" else z.read(x))
        with self.assertRaises(ValueError):self.load_xlsx(out.getvalue(),sheet="Inventory")

    def test_xlsx_compression_bomb_hold(self):
        out=io.BytesIO()
        with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            z.writestr("[Content_Types].xml",b"x"*2_000_000)
            z.writestr("xl/workbook.xml",b"x")
            z.writestr("xl/_rels/workbook.xml.rels",b"x")
        with self.assertRaises(ValueError):self.load_xlsx(out.getvalue(),sheet="Inventory")

    def test_xlsx_extra_members_limit_hold(self):
        out=io.BytesIO()
        with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_STORED) as z:
            for n in range(130):z.writestr(f"xl/worksheets/sheet{n+1}.xml",b"a")
            z.writestr("[Content_Types].xml",b"x")
        with self.assertRaises(ValueError):self.load_xlsx(out.getvalue(),sheet="Inventory")

    def test_xlsx_size_limit_hold(self):
        self.xlsx.write_bytes(b"X"*8_000_001)
        with self.assertRaises(ValueError):read_table(self.xlsx,sheet="Inventory")

    def test_xlsx_shared_strings(self):
        data=workbook_bytes(shared=True)
        fields,rows,_=self.load_xlsx(data,sheet="Inventory")
        self.assertEqual(fields[0],"id")
        self.assertEqual(rows[0]["title"],"한글 상품")

    def test_xlsx_duplicate_ids_hold(self):
        data=workbook_bytes(sheets={"Inventory":[["id","title","category"],["A1","foo","X"],["A1","bar","Y"]]})
        self.xlsx.write_bytes(data)
        with self.assertRaises(ValueError):self.build_xlsx()

    def test_xlsx_no_personal_values_inspect(self):
        p=subprocess.run([sys.executable,"studio.py","inspect",str(self.xlsx)],
            cwd=DIR,text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,0,p.stderr)
        j=json.loads(p.stdout)
        self.assertEqual(j["status"],"XLSX_SHEETS_REQUIRE_EXPLICIT_SELECTION")
        self.assertEqual(j["sheets"][0]["name"],"Inventory")
        self.assertNotIn("한글 상품",p.stdout)

    def test_xlsx_selected_sheet_inspect(self):
        p=subprocess.run([sys.executable,"studio.py","inspect",str(self.xlsx),"--sheet","Inventory"],
            cwd=DIR,text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        j=json.loads(p.stdout)
        self.assertEqual(j["rows"],2)
        self.assertEqual(j["sheet"],"Inventory")
        self.assertNotIn("한글 상품",p.stdout)

    def test_xlsx_cli_build_with_zip(self):
        digest=hashlib.sha256(self.xlsx.read_bytes()).hexdigest()
        z=self.root/"delivery.zip"
        args=[sys.executable,"studio.py","build",str(self.xlsx),str(self.html),
            "--source-sha256",digest,"--id","id","--title","title","--category","category",
            "--sheet","Inventory","--confirm","APPROVE","--ack-plaintext","--zip-path",str(z)]
        p=subprocess.run(args,cwd=DIR,text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertTrue(verify_zip(z)["verified"])
        self.assertNotIn("한글 상품",p.stdout)

    def test_xlsx_cli_denies_wrong_sheet(self):
        digest=hashlib.sha256(self.xlsx.read_bytes()).hexdigest()
        p=subprocess.run([sys.executable,"studio.py","build",str(self.xlsx),str(self.html),
            "--source-sha256",digest,"--id","id","--title","title","--category","category",
            "--sheet","WRONG","--confirm","APPROVE","--ack-plaintext"],
            cwd=DIR,text=True,encoding="utf-8",capture_output=True)
        self.assertEqual(p.returncode,2)
        self.assertFalse(self.html.exists())

    def test_tsv_quotes_newline_and_bom(self):
        self.tsv.write_bytes(b"\xef\xbb\xbf"+'id\ttitle\tcategory\n1\t"hello\tworld"\tA\n2\t"line\nbreak"\tB\n'.encode("utf-8"))
        fields,rows,_=read_table(self.tsv)
        self.assertEqual(fields,["id","title","category"])
        self.assertEqual(rows[0]["title"],"hello\tworld")
        self.assertEqual(rows[1]["title"],"line\nbreak")

    def test_tsv_html_build(self):
        self.tsv.write_text('id\ttitle\tcategory\n1\t"safe title"\tA\n2\t"</script>"\tB\n',encoding="utf-8")
        r=build(self.tsv,self.html,"id","title","category",True)
        self.assertEqual(r["rows"],2)
        self.assertIn(r"\u003c/script\u003e",self.html.read_text(encoding="utf-8"))

    def test_tsv_duplicate_columns_hold(self):
        self.tsv.write_text('id\tid\tcategory\n1\tB\tX\n',encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.tsv)

    def test_tsv_ragged_hold(self):
        self.tsv.write_text('id\ttitle\tcategory\n1\tB\n',encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.tsv)

    def test_tsv_unclosed_quote_hold(self):
        self.tsv.write_text('id\ttitle\tcategory\n1\t"not closed\tX\n',encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.tsv)

    def test_tsv_oversize_cell_hold(self):
        self.tsv.write_text('id\ttitle\tcategory\n1\t'+'X'*16001+'\tC\n',encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.tsv)

    def test_tsv_invalid_encoding_hold(self):
        self.tsv.write_bytes(b"id\ttitle\tcategory\n1\t\xff\tX\n")
        with self.assertRaises(ValueError):read_table(self.tsv)

    def test_tsv_formula_as_inert_text(self):
        self.tsv.write_text('id\ttitle\tcategory\n1\t"=HYPERLINK(""evil"")"\tA\n',encoding="utf-8")
        r=build(self.tsv,self.html,"id","title","category",True)
        self.assertEqual(r["rows"],1)
        self.assertIn("textContent",self.html.read_text(encoding="utf-8"))

    def test_xlsx_sheet_individual_approval(self):
        multi=workbook_bytes(sheets={
            "A":[["id","title","category"],["1","Secret A","X"]],
            "B":[["id","title","category"],["2","Public B","Y"]],
        })
        self.xlsx.write_bytes(multi)
        h=hashlib.sha256(multi).hexdigest()
        result=build(self.xlsx,self.html,"id","title","category",True,
                     expected_sha256=h,sheet="B")
        text=self.html.read_text(encoding="utf-8")
        self.assertEqual(result["sheet"],"B")
        self.assertIn("Public B",text)
        self.assertNotIn("Secret A",text)

if __name__=="__main__":
    unittest.main()
