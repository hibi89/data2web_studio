"""Fault-injection proof: a customer folder must be independently verified
AFTER the receipt is written, before the delivery operation returns success.

Synthetic source and tampering only. Failed folders remain unchanged and HOLD.
"""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data2web_append
import data2web_single
from data2web_append import deliver_to_new_directory
from data2web_single import deliver_single
from verify_customer_folder import verify_customer_folder


class CustomerDeliveryFinalVerification(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.source = self.root / "source.csv"
        self.source.write_text(
            "id,title,category\nA1,Valid One,Group1\nA2,Valid Two,Group2\n",
            encoding="utf-8",
        )
        self.destination = self.root / "delivery"
        self.original_source = self.source.read_bytes()

    def single(self):
        return deliver_single(
            self.source, self.destination,
            expected_sha256=hashlib.sha256(self.original_source).hexdigest(),
            id_column="id", title_column="title", category_column="category",
            confirm="APPROVE", ack_plaintext=True,
            privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        )

    def append(self):
        source2 = self.root / "second.csv"
        source2.write_text(
            "id,title,category\nB1,Another One,Group3\n", encoding="utf-8"
        )
        manifest = self.root / "approval.json"
        manifest.write_text(json.dumps({
            "contract": "DATA2WEB_INPUT_APPROVALS_V1",
            "sources": [
                {"filename": src.name, "sha256": hashlib.sha256(src.read_bytes()).hexdigest()}
                for src in (self.source, source2)
            ],
            "mapping": {"id": "id", "title": "title", "category": "category"},
            "approval": {
                "rights_and_plaintext_ack": True,
                "privacy_classification": "NO_PERSONAL_DATA_REVIEWED",
            },
        }), encoding="utf-8")
        return deliver_to_new_directory(
            manifest, self.destination, confirm="APPROVE", ack_plaintext=True
        )

    @staticmethod
    def altered_receipt(real_writer):
        def write(path, receipt):
            result = real_writer(path, receipt)
            target = Path(path)
            doc = json.loads(target.read_text(encoding="utf-8"))
            doc["output_sha256"] = "f" * 64
            target.write_text(json.dumps(doc), encoding="utf-8")
            return result
        return write

    @staticmethod
    def altered_zip(real_writer):
        def write(path, receipt):
            result = real_writer(path, receipt)
            target = Path(path).parent / "delivery.zip"
            with target.open("ab") as stream:
                stream.write(b"TAMPER_AFTER_ZIP_VERIFICATION")
            return result
        return write

    def assert_existing_failure_is_hold(self):
        self.assertEqual(self.source.read_bytes(), self.original_source)
        self.assertTrue(self.destination.is_dir())
        with self.assertRaises(ValueError):
            verify_customer_folder(self.destination)
        before = {f.name: f.read_bytes() for f in self.destination.iterdir()}
        with self.assertRaises((ValueError, FileExistsError)):
            self.single()
        self.assertEqual(
            {f.name: f.read_bytes() for f in self.destination.iterdir()}, before
        )

    def test_successful_single_path_is_verified_after_final_receipt(self):
        result = self.single()
        self.assertTrue(result["delivery_folder_created"])
        self.assertTrue(verify_customer_folder(self.destination)["verified"])

    def test_successful_append_path_is_verified_after_final_receipt(self):
        result = self.append()
        self.assertTrue(result["delivery_folder_created"])
        self.assertTrue(verify_customer_folder(self.destination)["verified"])

    def test_single_tampered_receipt_after_write_fails_closed(self):
        with patch.object(data2web_single, "write_receipt",
                          side_effect=self.altered_receipt(data2web_single.write_receipt)):
            with self.assertRaises(ValueError):
                self.single()
        self.assert_existing_failure_is_hold()

    def test_single_zip_modified_after_package_verification_fails_closed(self):
        with patch.object(data2web_single, "write_receipt",
                          side_effect=self.altered_zip(data2web_single.write_receipt)):
            with self.assertRaises(ValueError):
                self.single()
        self.assert_existing_failure_is_hold()

    def test_append_tampered_receipt_after_write_fails_closed(self):
        with patch.object(data2web_append, "write_receipt",
                          side_effect=self.altered_receipt(data2web_append.write_receipt)):
            with self.assertRaises(ValueError):
                self.append()
        self.assert_existing_failure_is_hold()

    def test_append_zip_modified_after_package_verification_fails_closed(self):
        with patch.object(data2web_append, "write_receipt",
                          side_effect=self.altered_zip(data2web_append.write_receipt)):
            with self.assertRaises(ValueError):
                self.append()
        self.assert_existing_failure_is_hold()

    def test_interrupted_receipt_write_preserves_partial_and_blocks_retry(self):
        def write_partial(path, receipt):
            Path(path).write_bytes(b'{"contract":')
            raise OSError("SIMULATED_RECEIPT_INTERRUPTION")
        with patch.object(data2web_single, "write_receipt", side_effect=write_partial):
            with self.assertRaisesRegex(OSError, "SIMULATED_RECEIPT_INTERRUPTION"):
                self.single()
        self.assert_existing_failure_is_hold()


if __name__ == "__main__":
    unittest.main()
