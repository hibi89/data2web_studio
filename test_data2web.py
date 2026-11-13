import json
import tempfile
import unittest
from pathlib import Path
from data2web import build, read_table

class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root / "sample.csv"
        self.src.write_text('id,title,category\n1,"Hello, world",A\n2,<script>alert(1)</script>,B\n', encoding="utf-8")
        self.out = self.root / "out.html"

    def test_build(self):
        result = build(self.src,self.out,"id","title","category",True)
        self.assertEqual(result["rows"],2)
        self.assertIn("DATA2WEB",self.out.read_text())
        self.assertNotIn("<script>alert(1)</script>",self.out.read_text())

    def test_requires_approval(self):
        with self.assertRaises(ValueError): build(self.src,self.out,"id","title","category")

    def test_no_overwrite(self):
        self.out.write_text("original")
        with self.assertRaises(FileExistsError): build(self.src,self.out,"id","title","category",True)
        self.assertEqual(self.out.read_text(),"original")

    def test_duplicate_ids(self):
        self.src.write_text("id,title,category\n1,a,x\n1,b,y\n")
        with self.assertRaises(ValueError): build(self.src,self.out,"id","title","category",True)

    def test_json(self):
        self.src = self.root / "sample.json"
        self.src.write_text(json.dumps([{"id":"1","title":"a","category":"x"}]))
        self.assertEqual(build(self.src,self.out,"id","title","category",True)["rows"],1)

    def test_duplicate_json_keys(self):
        self.src = self.root / "sample.json"
        self.src.write_text('[{"id":"1","id":"2","title":"a","category":"x"}]')
        with self.assertRaises(ValueError): read_table(self.src)

    def test_nested_json(self):
        self.src = self.root / "sample.json"
        self.src.write_text('[{"id":"1","title":{"bad":1},"category":"x"}]')
        with self.assertRaises(ValueError): read_table(self.src)

    def test_invalid_mapping(self):
        with self.assertRaises(ValueError): build(self.src,self.out,"id","id","category",True)

if __name__ == "__main__": unittest.main()
