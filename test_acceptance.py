"""Independent 50+ synthetic cases, security gates and REA Lite contract fixture."""
from __future__ import annotations
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from data2web import read_table, build
from delivery import package_html
from verify_delivery import verify_zip

GOLDEN_CSV = "식별자,이름,분류,비고\nA-01,콜드브루,커피,진한 맛\nA-02,딸기우유,음료,시원함\n"

class Acceptance(unittest.TestCase):
    def setUp(self):
        self.d=tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)
        self.root=Path(self.d.name)
        self.src=self.root/"input.csv"
        self.src.write_text(GOLDEN_CSV,encoding="utf-8")
        self.html=self.root/"out.html"
        self.kw={"id_column":"식별자","title_column":"이름","category_column":"분류","approved":True}

    def golden_build(self, **more):
        return build(self.src,self.html,**{**self.kw,**more})

    def test_upstream_golden_contract_fixture(self):
        # REA_Web/tests/test_lite_builder.py BASE, tests original 2 Korean records.
        fields,rows,digest=read_table(self.src)
        self.assertEqual(fields,["식별자","이름","분류","비고"])
        self.assertEqual(rows[0]["식별자"],"A-01")
        self.assertEqual(rows[1]["이름"],"딸기우유")
        result=self.golden_build(expected_sha256=digest)
        self.assertEqual(result["rows"],2)
        content=self.html.read_text(encoding="utf-8")
        self.assertIn('"콜드브루"',content)
        self.assertIn("connect-src 'none'",content)
        self.assertIn('id="sort"',content)
        self.assertIn('id="csv"',content)

    def test_owner_theme_and_escaped_title(self):
        for theme in ("office","cafe","inventory"):
            with self.subTest(theme=theme):
                target=self.root/(theme+".html")
                result=build(self.src,target,**self.kw,name="<DATA2WEB>",theme=theme)
                self.assertEqual(result["theme"],theme)
                s=target.read_text(encoding="utf-8")
                self.assertIn('data-theme="'+theme+'"',s)
                self.assertIn("&lt;DATA2WEB&gt;",s)
                self.assertEqual(result["mapping"]["id"],"식별자")
                self.assertFalse(result["sale_approved"])

    def test_expected_sha_rejected(self):
        with self.assertRaises(ValueError): self.golden_build(expected_sha256="0"*64)
        self.assertFalse(self.html.exists())

    def test_source_unchanged(self):
        before=self.src.read_bytes()
        self.golden_build(expected_sha256=hashlib.sha256(before).hexdigest())
        self.assertEqual(before,self.src.read_bytes())

    def test_inspect_cli_no_private_cell_leak(self):
        p=subprocess.run([sys.executable,"studio.py","inspect",str(self.src)],
                         cwd=Path(__file__).resolve().parent,text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn("source_sha256",p.stdout)
        self.assertNotIn("콜드브루",p.stdout)
        self.assertNotIn("딸기우유",p.stdout)

    def test_cli_build_zip_verify(self):
        digest=hashlib.sha256(self.src.read_bytes()).hexdigest()
        z=self.root/"delivery.zip"
        p=subprocess.run([sys.executable,"studio.py","build",str(self.src),str(self.html),
                          "--source-sha256",digest,"--id","식별자","--title","이름",
                          "--category","분류","--confirm","APPROVE","--ack-plaintext",
                          "--zip-path",str(z)],cwd=Path(__file__).resolve().parent,
                         text=True,capture_output=True,encoding="utf-8")
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertTrue(verify_zip(z)["verified"])
        v=subprocess.run([sys.executable,"verify_delivery.py",str(z)],
                          cwd=Path(__file__).resolve().parent,text=True,capture_output=True,
                          encoding="utf-8")
        self.assertEqual(v.returncode,0,v.stdout+v.stderr)
        self.assertTrue(json.loads(v.stdout)["verified"])
        self.assertNotIn("콜드브루",p.stdout)

    def test_cli_missing_ack_holds(self):
        digest=hashlib.sha256(self.src.read_bytes()).hexdigest()
        p=subprocess.run([sys.executable,"studio.py","build",str(self.src),str(self.html),
                          "--source-sha256",digest,"--id","식별자","--title","이름",
                          "--category","분류","--confirm","APPROVE"],
                         cwd=Path(__file__).resolve().parent,text=True,capture_output=True)
        self.assertNotEqual(p.returncode,0)
        self.assertFalse(self.html.exists())

    def test_package_repeatable(self):
        receipt=self.golden_build()
        a=self.root/"a.zip"; b=self.root/"b.zip"
        package_html(self.html,a,receipt)
        package_html(self.html,b,receipt)
        self.assertEqual(a.read_bytes(),b.read_bytes())

    def test_package_never_overwrite(self):
        receipt=self.golden_build()
        p=self.root/"existing.zip";p.write_bytes(b"KEEP")
        with self.assertRaises(ValueError): package_html(self.html,p,receipt)
        self.assertEqual(p.read_bytes(),b"KEEP")

    def test_zip_manifest_hash_tamper_detected(self):
        receipt=self.golden_build()
        z=self.root/"delivery.zip"
        package_html(self.html,z,receipt)
        corrupted=self.root/"corrupted.zip"
        with zipfile.ZipFile(z) as origin, zipfile.ZipFile(corrupted,"w") as output:
            for item in origin.infolist():
                data=origin.read(item.filename)
                if item.filename=="index.html": data=data.replace(b"DATA2WEB",b"BAD2WEB ",1)
                output.writestr(item,data)
        with self.assertRaises(ValueError): verify_zip(corrupted)

    def test_zip_slip_refused(self):
        z=self.root/"bad.zip"
        with zipfile.ZipFile(z,"w") as archive:
            for name in ("index.html","manifest.json","../secret"):
                archive.writestr(name,b"x")
        with self.assertRaises(ValueError): verify_zip(z)

    def test_zip_extra_refused(self):
        z=self.root/"bad.zip"
        with zipfile.ZipFile(z,"w") as archive:
            for name in ("index.html","manifest.json","README_KO.txt","other"):
                archive.writestr(name,b"x")
        with self.assertRaises(ValueError): verify_zip(z)

    def test_zip_compressed_refused(self):
        z=self.root/"bad.zip"
        with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as archive:
            for name in ("index.html","manifest.json","README_KO.txt"):
                archive.writestr(name,b"x"*1024)
        with self.assertRaises(ValueError): verify_zip(z)

    def test_zip_invalid_archive_refused(self):
        z=self.root/"bad.zip";z.write_bytes(b"not-a-zip")
        with self.assertRaises(ValueError): verify_zip(z)

    def test_html_not_symlink(self):
        target=self.root/"existing.html";target.write_text("KEEP")
        try:self.html.symlink_to(target)
        except (OSError,NotImplementedError):self.skipTest("symlink restricted")
        with self.assertRaises(FileExistsError):self.golden_build()
        self.assertEqual(target.read_text(),"KEEP")

    def test_source_symlink_blocked(self):
        other=self.root/"actual.csv";other.write_text(GOLDEN_CSV,encoding="utf-8")
        self.src.unlink()
        try:self.src.symlink_to(other)
        except (OSError,NotImplementedError):self.skipTest("symlink restricted")
        with self.assertRaises(ValueError):read_table(self.src)

    def test_duplicate_csv_headers(self):
        self.src.write_text("id,id,title,category\n1,2,a,x\n")
        with self.assertRaises(ValueError):read_table(self.src)

    def test_extra_csv_cells(self):
        self.src.write_text("id,title,category\n1,a,x,EXTRA\n")
        with self.assertRaises(ValueError):read_table(self.src)

    def test_empty_csv(self):
        self.src.write_text("",encoding="utf-8")
        with self.assertRaises(ValueError):read_table(self.src)

    def test_json_inconsistent_keys(self):
        self.src=self.root/"input.json"
        self.src.write_text('[{"id":"1","title":"ok","category":"x"},{"id":"2","title":"wrong"}]')
        with self.assertRaises(ValueError):read_table(self.src)

    def test_json_invalid_root(self):
        self.src=self.root/"input.json"
        self.src.write_text('{"rows":[{"id":"1"}]}')
        with self.assertRaises(ValueError):read_table(self.src)

    def test_json_duplicate_key_refused(self):
        self.src=self.root/"input.json"
        self.src.write_text('[{"id":"1","id":"2","title":"a","category":"x"}]')
        with self.assertRaises(ValueError):read_table(self.src)

    def test_injection_formula_is_text(self):
        self.src.write_text("식별자,이름,분류,비고\nA-01,=HYPERLINK(a),커피,@SUM(A1)\n",encoding="utf-8")
        self.golden_build()
        s=self.html.read_text(encoding="utf-8")
        self.assertIn("=HYPERLINK",s)
        self.assertIn("textContent",s)

    def test_html_escape_bad_script(self):
        self.src.write_text('식별자,이름,분류,비고\nA-01,"</script><img src=x onerror=alert(1)>",커피,x\n',encoding="utf-8")
        self.golden_build()
        s=self.html.read_text(encoding="utf-8")
        self.assertNotIn("</script><img",s)
        self.assertIn(r"\u003c/script\u003e",s)

    def test_csv_utf8_bom(self):
        self.src.write_bytes(b"\xef\xbb\xbf"+GOLDEN_CSV.encode("utf-8"))
        fields,rows,_=read_table(self.src)
        self.assertEqual(fields[0],"식별자")
        self.assertEqual(len(rows),2)

    def test_reject_missing_id(self):
        self.src.write_text("식별자,이름,분류\n,zero,x\n",encoding="utf-8")
        with self.assertRaises(ValueError):self.golden_build()

    def test_reject_duplicate_id(self):
        self.src.write_text("식별자,이름,분류\nA1,one,x\nA1,two,y\n",encoding="utf-8")
        with self.assertRaises(ValueError):self.golden_build()

    def test_json_nested_array_refused(self):
        self.src=self.root/"input.json"
        self.src.write_text('[{"id":"1","title":["a"],"category":"x"}]')
        with self.assertRaises(ValueError):read_table(self.src)

    def test_unapproved_output_refused(self):
        with self.assertRaises(ValueError):build(self.src,self.html,"식별자","이름","분류")
        self.assertFalse(self.html.exists())

# Parameterized fixture variants are independent unittest methods, not hidden pass counts.
def make_csv_test(index):
    def case(self):
        phrases=[
            "simple","한글","éclair","12,345",'quoted " twice',"line1\nline2",
            "</script><img onerror=alert(1)>","&amp;","=1+1","+1","@SUM(A1)",
            "-42","(123)"," path /tmp ","space  ","2026-11-13","00:03",
            "👀","＜tag＞","tab\tinside","brackets[]","ellipsis…","a'b",
            "leading-zero 001","line\rinside","https://example.invalid","$1,000",
            "NULL","💻🚀","backslash\\path",
        ]
        phrase=phrases[index]
        buf=io.StringIO(newline="")
        writer=csv.writer(buf,lineterminator="\r\n")
        writer.writerow(["id","title","category","memo"])
        writer.writerow([f"key-{index}",phrase,"A",phrase])
        self.src.write_bytes(buf.getvalue().encode("utf-8"))
        fields,rows,_=read_table(self.src)
        self.assertEqual(rows[0]["memo"],phrase)
        out=build(self.src,self.html,"id","title","category",True)
        self.assertEqual(out["rows"],1)
        html=self.html.read_text(encoding="utf-8")
        self.assertIn("DATA2WEB_HTML_V1",html)
        self.assertNotIn("</script><img",html)
    return case

def make_json_test(index):
    def case(self):
        vals=[
            0,1,-5,3.14159,True,False,None,"", "한글", "emoji 🎯",
            "line\nbreak", "quote \"", "apostrophe '", "</script>",
            "&", "002", "50%", "tab\tvalue","<svg onload=alert(1)>",
            "prototype", "abc", "2026-11-13", "£99", "micro µ",
            "\u2028", "\u2029", "end", "∑", "=-2", "a,b",
        ]
        v=vals[index]
        self.src=self.root/"input.json"
        self.src.write_text(json.dumps([{"id":str(index+1),"title":v,"category":"Group"}],ensure_ascii=False),encoding="utf-8")
        cols,rows,digest=read_table(self.src)
        self.assertEqual(rows[0]["title"],"" if v is None else str(v))
        self.assertEqual(build(self.src,self.html,"id","title","category",True,expected_sha256=digest)["rows"],1)
    return case

for i in range(30):
    setattr(Acceptance,f"test_csv_matrix_{i:02d}",make_csv_test(i))
    setattr(Acceptance,f"test_json_matrix_{i:02d}",make_json_test(i))

if __name__=="__main__":
    unittest.main()
