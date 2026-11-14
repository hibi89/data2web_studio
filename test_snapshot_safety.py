"""Source file-handle identity, bounded snapshot and race-guard regressions."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data2web
import path_policy
from path_policy import read_bounded_source


class SnapshotSafety(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.source=self.root/"owner.csv"
        self.source.write_text("id,title,category\n1,Original,A\n",encoding="utf-8")

    def test_source_snapshot_exact_bytes(self):
        self.assertEqual(read_bounded_source(self.source),self.source.read_bytes())

    def test_bounded_read_rejects_oversize(self):
        with self.assertRaises(ValueError):
            read_bounded_source(self.source,max_bytes=4)

    def test_source_symlink_rejected(self):
        alias=self.root/"alias.csv"
        try:alias.symlink_to(self.source)
        except (OSError,NotImplementedError):self.skipTest("OS symlinks unavailable")
        with self.assertRaises(ValueError):
            read_bounded_source(alias)

    def test_simulated_path_swap_before_open_detected(self):
        replacement=self.root/"replacement.csv"
        replacement.write_bytes(self.source.read_bytes())
        original_open=path_policy._open_source_readonly
        called=[False]

        def swap_and_open(path,flags):
            if Path(path)==self.source.absolute() and not called[0]:
                called[0]=True
                os.replace(replacement,self.source)
            return original_open(path,flags)

        with patch("path_policy._open_source_readonly",side_effect=swap_and_open):
            with self.assertRaises(ValueError):
                read_bounded_source(self.source)
        self.assertTrue(called[0])

    def test_hardlink_alias_mutation_during_bounded_read_is_rejected(self):
        alias=self.root/"hardlink.csv"
        try:
            os.link(self.source,alias)
        except (OSError,NotImplementedError) as error:
            self.skipTest(f"Hard link unavailable: {type(error).__name__}")
        self.assertTrue(self.source.samefile(alias))
        original_bytes=self.source.read_bytes()
        initial_mtime_ns=alias.stat().st_mtime_ns
        original_read=os.read
        mutated=[False]
        write_denied=[]

        def mutate_through_alias(fd,size):
            data=original_read(fd,size)
            if not mutated[0]:
                mutated[0]=True
                try:
                    with alias.open("r+b") as stream:
                        stream.write(b"X")
                except PermissionError as error:
                    write_denied.append(error)
                else:
                    changed=alias.stat()
                    # POSIX has no mandatory share-deny lock. Pin a distinct
                    # mtime so the metadata-change path is deterministic.
                    os.utime(
                        alias,
                        ns=(changed.st_atime_ns,initial_mtime_ns+10_000_000_000),
                    )
            return data

        with patch("os.read",side_effect=mutate_through_alias):
            if os.name=="nt":
                snapshot=read_bounded_source(self.source)
            else:
                with self.assertRaisesRegex(
                    ValueError,"Source changed during bounded file-handle read"
                ):
                    read_bounded_source(self.source)
        self.assertTrue(mutated[0])
        if os.name=="nt":
            self.assertEqual(len(write_denied),1)
            self.assertEqual(snapshot,original_bytes)
            self.assertEqual(self.source.read_bytes(),original_bytes)
        else:
            self.assertFalse(write_denied)
            self.assertNotEqual(alias.read_bytes(),original_bytes)
            self.assertNotEqual(alias.stat().st_mtime_ns,initial_mtime_ns)

    def test_read_table_rejects_source_mutated_during_parse(self):
        original=self.source.read_bytes()
        mutated=original.replace(b"Original",b"Changed!")
        with patch.object(data2web,"read_bounded_source",side_effect=(original,mutated)):
            with self.assertRaisesRegex(ValueError,"Input changed during parsing"):
                data2web.read_table(self.source)

    def test_build_preflight_sha_unchanged(self):
        actual=self.source.read_bytes()
        import hashlib
        sha=hashlib.sha256(actual).hexdigest()
        path=self.root/"result.html"
        receipt=data2web.build(self.source,path,"id","title","category",True,
                               expected_sha256=sha)
        self.assertEqual(receipt["source_sha256"],sha)
        self.assertTrue(path.exists())

    def test_read_table_fails_if_file_is_replaced_with_different_same_size_bytes(self):
        original=self.source.read_bytes()
        data=self.source.read_bytes().replace(b"Original",b"Alternate")
        with patch.object(data2web,"read_bounded_source",side_effect=(original,data)):
            with self.assertRaises(ValueError):
                data2web.read_table(self.source)

if __name__=="__main__":
    unittest.main()
