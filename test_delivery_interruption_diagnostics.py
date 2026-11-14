"""Crash interruption and read-only redacted HOLD diagnostics (synthetic only)."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import data2web
import data2web_append
import delivery
from data2web_single import deliver_single
from data2web_append import deliver_to_new_directory
from package_portable import create_portable
from verify_customer_folder import diagnose_customer_folder, verify_customer_folder


class InterruptedCustomerDelivery(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.source = self.root / "one.csv"
        self.source.write_text(
            "id,title,category\nA1,Sample One,A\nA2,Sample Two,B\n",
            encoding="utf-8",
        )
        self.second = self.root / "two.csv"
        self.second.write_text(
            "id,title,category\nB1,Sample Three,C\n", encoding="utf-8"
        )
        self.originals = {p: p.read_bytes() for p in (self.source, self.second)}
        self.destination = self.root / "customer"
        manifest = {
            "contract": "DATA2WEB_INPUT_APPROVALS_V1",
            "sources": [
                {"filename": p.name, "sha256": hashlib.sha256(raw).hexdigest()}
                for p, raw in self.originals.items()
            ],
            "mapping": {"id": "id", "title": "title", "category": "category"},
            "approval": {
                "rights_and_plaintext_ack": True,
                "privacy_classification": "NO_PERSONAL_DATA_REVIEWED",
            },
        }
        self.manifest = self.root / "approval.json"
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")

    def deliver(self, *, append=False):
        if append:
            return deliver_to_new_directory(
                self.manifest, self.destination, confirm="APPROVE",
                ack_plaintext=True,
            )
        return deliver_single(
            self.source, self.destination,
            expected_sha256=hashlib.sha256(self.originals[self.source]).hexdigest(),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )

    @staticmethod
    def interrupted_fdopen(real_fdopen):
        def open_partial(fd, mode):
            stream = real_fdopen(fd, mode)

            class PartialWriter:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    stream.close()

                def write(self, data):
                    stream.write(data[:40])
                    stream.flush()
                    raise OSError("INJECTED_HTML_DISK_INTERRUPTION")
            return PartialWriter()
        return open_partial

    def assert_failed_folder_held(self, *, html, zip_file, receipt):
        for source, before in self.originals.items():
            self.assertEqual(source.read_bytes(), before)
        self.assertTrue(self.destination.is_dir())
        present = {"index.html": html, "delivery.zip": zip_file,
                   "receipt.json": receipt}
        self.assertEqual(
            {p.name for p in self.destination.iterdir()},
            {name for name, exists in present.items() if exists},
        )
        diagnosis = diagnose_customer_folder(self.destination)
        self.assertFalse(diagnosis["verified"])
        self.assertEqual(diagnosis["status"], "HOLD")
        self.assertFalse(diagnosis["sale_approved"])
        self.assertEqual(diagnosis["reason_code"], "INCOMPLETE_OR_UNEXPECTED_MEMBERS")
        self.assertEqual(diagnosis["present"], present)
        with self.assertRaises(ValueError):
            verify_customer_folder(self.destination)
        snapshot = {p.name: p.read_bytes() for p in self.destination.iterdir()}
        with self.assertRaises((FileExistsError, ValueError)):
            self.deliver()
        self.assertEqual(
            {p.name: p.read_bytes() for p in self.destination.iterdir()}, snapshot
        )
        return diagnosis

    def test_single_interrupted_html_write_is_hold(self):
        with patch.object(data2web.os, "fdopen",
                          new=self.interrupted_fdopen(os.fdopen)):
            with self.assertRaisesRegex(OSError, "INJECTED_HTML_DISK_INTERRUPTION"):
                self.deliver()
        self.assert_failed_folder_held(html=True, zip_file=False, receipt=False)

    def test_append_interrupted_html_write_is_hold(self):
        with patch.object(data2web_append.os, "fdopen",
                          new=self.interrupted_fdopen(os.fdopen)):
            with self.assertRaisesRegex(OSError, "INJECTED_HTML_DISK_INTERRUPTION"):
                self.deliver(append=True)
        self.assert_failed_folder_held(html=True, zip_file=False, receipt=False)

    def zip_interruption(self, *, append=False):
        original = delivery.ZipFile.writestr

        def fail_after_first_member(archive, name, data, *args, **kwargs):
            original(archive, name, data, *args, **kwargs)
            raise OSError("INJECTED_ZIP_DISK_INTERRUPTION")

        with patch.object(delivery.ZipFile, "writestr", new=fail_after_first_member):
            with self.assertRaisesRegex(OSError, "INJECTED_ZIP_DISK_INTERRUPTION"):
                self.deliver(append=append)
        self.assert_failed_folder_held(html=True, zip_file=True, receipt=False)

    def test_single_interrupted_zip_write_is_hold(self):
        self.zip_interruption()

    def test_append_interrupted_zip_write_is_hold(self):
        self.zip_interruption(append=True)

    def test_complete_folder_diagnosis_requires_full_integrity(self):
        self.deliver()
        diagnosis = diagnose_customer_folder(self.destination)
        self.assertTrue(diagnosis["verified"])
        self.assertFalse(diagnosis["sale_approved"])
        self.assertEqual(
            diagnosis["reason_code"], "FULL_INTEGRITY_VERIFIED_NOT_SALE_APPROVED"
        )
        (self.destination / "delivery.zip").write_bytes(b"PK\x03\x04PARTIAL")
        diagnosis = diagnose_customer_folder(self.destination)
        self.assertEqual(diagnosis["reason_code"], "INTEGRITY_CHECK_FAILED")
        self.assertFalse(diagnosis["verified"])

    def test_missing_folder_diagnosis_is_read_only(self):
        result = diagnose_customer_folder(self.destination)
        self.assertEqual(result["reason_code"], "MISSING_OR_UNSAFE_DIRECTORY")
        self.assertFalse(self.destination.exists())

    def test_cli_diagnosis_is_redacted_and_returns_hold_exit_code(self):
        self.destination.mkdir()
        (self.destination / "index.html").write_bytes(b"partial")
        result = subprocess.run(
            [sys.executable, "studio.py", "diagnose-customer", str(self.destination)],
            cwd=Path(__file__).resolve().parent,
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "HOLD")
        self.assertNotIn(str(self.destination), result.stdout)
        self.assertNotIn(str(self.source), result.stdout)
        self.assertNotIn("Sample One", result.stdout)
        self.assertEqual((self.destination / "index.html").read_bytes(), b"partial")

    def test_portable_diagnosis_is_read_only(self):
        app = self.root / "portable.pyz"
        create_portable(app)
        self.destination.mkdir()
        (self.destination / "index.html").write_bytes(b"partial")
        result = subprocess.run(
            [sys.executable, str(app), "diagnose-customer", str(self.destination)],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "HOLD")
        self.assertEqual((self.destination / "index.html").read_bytes(), b"partial")


if __name__ == "__main__":
    unittest.main()
