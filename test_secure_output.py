"""Synthetic regressions for safe, anchored output creation."""
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data2web
from secure_output import create_output_file, open_output_directory


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

    def test_build_rejects_parent_link_inserted_before_open(self):
        real_open = data2web.open_output_directory
        swapped = False

        def replace_then_open(path, *, expected_identity=None):
            nonlocal swapped
            os.replace(self.selected, self.held)
            self._make_link()
            swapped = True
            return real_open(path, expected_identity=expected_identity)

        target = self.selected / "generated.html"
        with patch.object(data2web, "open_output_directory", replace_then_open):
            with self.assertRaisesRegex(ValueError, "reparse point forbidden"):
                data2web.build(
                    self.source, target, "id", "title", "category", approved=True
                )
        self.assertTrue(swapped)
        self.assertFalse((self.held / "generated.html").exists())
        self.assertFalse((self.alternate / "generated.html").exists())

    def test_create_file_is_relative_to_verified_directory(self):
        with open_output_directory(self.selected) as parent:
            with create_output_file(self.selected / "receipt.json", directory=parent) as stream:
                stream.write(b'{"synthetic":true}\n')
        self.assertEqual(
            (self.selected / "receipt.json").read_bytes(),
            b'{"synthetic":true}\n',
        )

    def test_posix_rejects_other_user_writable_ancestry(self):
        if os.name == "nt":
            self.skipTest("POSIX ancestry mode checks")
        self.selected.chmod(0o777)
        try:
            with self.assertRaisesRegex(ValueError, "writable by other users"):
                open_output_directory(self.selected)
        finally:
            self.selected.chmod(0o700)

    def test_windows_handle_prevents_ancestor_rename(self):
        if os.name != "nt":
            self.skipTest("Windows directory share semantics")
        with open_output_directory(self.selected):
            with self.assertRaises(OSError):
                os.replace(self.selected, self.held)
        self.assertTrue(self.selected.is_dir())
        self.assertFalse(self.held.exists())


if __name__ == "__main__":
    unittest.main()
