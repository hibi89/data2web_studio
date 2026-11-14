"""Synthetic output-parent replacement regressions for anchored creates."""
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data2web
from secure_output import open_output_directory


class OutputPathRace(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.selected = self.root / "selected"
        self.alternate = self.root / "alternate"
        self.held = self.root / "selected-original"
        self.selected.mkdir()
        self.alternate.mkdir()
        self.source = self.root / "source.csv"
        self.source.write_text(
            "id,title,category\nA1,Synthetic title,A\n", encoding="utf-8"
        )

    def _make_link(self):
        if os.name == "nt":
            result = subprocess.run(
                [os.environ.get("COMSPEC", "cmd.exe"), "/c", "mklink", "/J",
                 str(self.selected), str(self.alternate)],
                capture_output=True, text=True, errors="replace", timeout=15,
            )
            if result.returncode:
                self.fail("mklink /J failed: " + result.stdout + result.stderr)
            self.addCleanup(self._remove_junction)
            attributes = getattr(self.selected.lstat(), "st_file_attributes", 0)
            self.assertTrue(
                attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
            )
        else:
            self.selected.symlink_to(self.alternate, target_is_directory=True)
            self.addCleanup(self.selected.unlink)

    def _remove_junction(self):
        try:
            os.rmdir(self.selected)
        except FileNotFoundError:
            pass

    def test_parent_replacement_after_anchor_does_not_redirect_build(self):
        real_create = data2web.create_output_file
        swapped = False

        def replace_then_create(path, *, directory=None, mode=0o600):
            nonlocal swapped
            if not swapped:
                parent = open_output_directory(Path(path).parent)
                os.replace(self.selected, self.held)
                self._make_link()
                swapped = True
                try:
                    return parent.create_file(Path(path).name, mode)
                finally:
                    parent.close()
            return real_create(path, directory=directory, mode=mode)

        target = self.selected / "generated.html"
        with patch.object(data2web, "create_output_file", replace_then_create):
            with self.assertRaises(ValueError):
                data2web.build(
                    self.source, target, "id", "title", "category", approved=True
                )
        self.assertTrue(swapped)
        self.assertTrue((self.held / "generated.html").is_file())
        self.assertFalse((self.alternate / "generated.html").exists())
        self.assertIn("Synthetic title", (self.held / "generated.html").read_text(
            encoding="utf-8"
        ))

    def test_child_create_is_relative_to_pinned_directory(self):
        with open_output_directory(self.selected) as parent:
            os.replace(self.selected, self.held)
            self._make_link()
            with parent.create_file("receipt.json") as stream:
                stream.write(b'{"synthetic":true}\n')
        self.assertEqual(
            (self.held / "receipt.json").read_bytes(),
            b'{"synthetic":true}\n',
        )
        self.assertFalse((self.alternate / "receipt.json").exists())


if __name__ == "__main__":
    unittest.main()
