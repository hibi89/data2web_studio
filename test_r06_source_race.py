"""R06 synthetic fail-closed regressions: hardlinks, FIFO races and path swaps.

No customer source, credentials or external transfers; tests use isolated temp.
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import path_policy


class SourceHandleRaceRegressions(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="r06-source-race-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "owner-reviewed.csv"
        self.original = b"id,title,category\\nA1,Synthetic,A\\n".replace(b"\\n", bytes([10]))
        self.source.write_bytes(self.original)

    def test_normal_bounded_source_unchanged(self):
        self.assertEqual(path_policy.read_bounded_source(self.source), self.original)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_hardlinked_source_is_not_accepted(self):
        alias = self.root / "other-name.csv"
        try:
            os.link(self.source, alias)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Hardlinks unavailable on this volume: {exc}")
        with self.assertRaisesRegex(ValueError, "single-link"):
            path_policy.read_bounded_source(self.source)
        self.assertEqual(alias.read_bytes(), self.original)

    def test_hardlink_added_after_precheck_is_rejected(self):
        alias = self.root / "late-link.csv"
        real_open = path_policy._open_source_readonly

        def add_link_then_open(path, flags):
            try:
                os.link(self.source, alias)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"Hardlinks unavailable on this volume: {exc}")
            return real_open(path, flags)

        with patch.object(path_policy, "_open_source_readonly", add_link_then_open):
            with self.assertRaisesRegex(ValueError, "link count"):
                path_policy.read_bounded_source(self.source)
        self.assertEqual(self.source.read_bytes(), self.original)

    @unittest.skipUnless(os.name == "posix" and hasattr(os, "mkfifo"),
                         "POSIX FIFO race only")
    def test_regular_source_swapped_to_fifo_cannot_block_open(self):
        held = self.root / "held-original.csv"
        real_open = path_policy._open_source_readonly

        def fifo_swap(path, flags):
            os.replace(self.source, held)
            os.mkfifo(self.source)
            # Without O_NONBLOCK, opening this FIFO would hang the CI process.
            return real_open(path, flags)

        with patch.object(path_policy, "_open_source_readonly", fifo_swap):
            with self.assertRaisesRegex(ValueError, "changed type"):
                path_policy.read_bounded_source(self.source)
        self.assertEqual(held.read_bytes(), self.original)

    @unittest.skipUnless(os.name == "posix", "POSIX replace-on-read race")
    def test_same_length_atomic_replacement_during_read_is_rejected(self):
        substitute = self.root / "substitute.csv"
        substitute.write_bytes(self.original.replace(b"Synthetic", b"Malicious"))
        held = self.root / "old-inode.csv"
        real_read = os.read
        switched = False

        def replace_on_read(fd, count):
            nonlocal switched
            chunk = real_read(fd, count)
            if chunk and not switched:
                switched = True
                os.replace(self.source, held)
                os.replace(substitute, self.source)
            return chunk

        with patch("os.read", side_effect=replace_on_read):
            with self.assertRaisesRegex(ValueError, "Source changed"):
                path_policy.read_bounded_source(self.source)
        self.assertTrue(switched)
        self.assertEqual(held.read_bytes(), self.original)


if __name__ == "__main__":
    unittest.main()
