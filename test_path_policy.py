"""Path ancestry, junction-equivalent and no-clobber regressions."""
import tempfile
import unittest
from pathlib import Path

from data2web import read_table, build
from path_policy import assert_no_links

class LinkedAncestors(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.real=self.root/"safe"
        self.real.mkdir()
        self.source=self.real/"source.csv"
        self.source.write_text("id,title,category\nA1,Real input,A\n",encoding="utf-8")

    def test_simple_safe_source_accepted(self):
        self.assertEqual(assert_no_links(self.source),self.source.absolute())
        fields,rows,_=read_table(self.source)
        self.assertEqual(len(rows),1)

    def test_parent_directory_alias_rejected(self):
        path=self.real/".."/"safe"/"source.csv"
        with self.assertRaises(ValueError):assert_no_links(path)

    def test_source_symlink_directory_rejected(self):
        alias=self.root/"linkdir"
        try:alias.symlink_to(self.real,target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest("Symlink unavailable")
        with self.assertRaises(ValueError):read_table(alias/"source.csv")

    def test_output_parent_directory_symlink_rejected(self):
        alias=self.root/"linkdir"
        try:alias.symlink_to(self.real,target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest("Symlink unavailable")
        with self.assertRaises(ValueError):
            build(self.source,alias/"new.html","id","title","category",True)
        self.assertFalse((self.real/"new.html").exists())

    def test_existing_output_never_overwritten(self):
        output=self.real/"generated.html"
        output.write_text("KEEP",encoding="utf-8")
        with self.assertRaises(FileExistsError):
            build(self.source,output,"id","title","category",True)
        self.assertEqual(output.read_text(encoding="utf-8"),"KEEP")

if __name__=="__main__":unittest.main()
