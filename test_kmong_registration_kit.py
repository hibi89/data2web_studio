"""Offline, synthetic only, stdlib-only tests for registration kit packaging."""
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

from kmong_weekend_demo import build_demo, SOURCE
from kmong_registration_kit import create_registration_kit, verify_kit, SHOTS


def fake_fixture_png():
    # This is a valid all-white PNG UNIT-TEST fixture, not a browser screenshot.
    width, height = 1440, 900
    uncompressed = (b"\x00" + b"\xff\xff\xff" * width) * height
    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload +
                struct.pack(">I", zlib.crc32(tag + payload) & 0xffffffff))
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(uncompressed)) + chunk(b"IEND", b""))


class RegistrationKitTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.preview = self.root / "preview"
        build_demo(self.preview)
        self.zip = self.root / "new-kit.zip"

    def prepare_fake_capture(self):
        shots = self.preview / "screenshots"
        shots.mkdir()
        evidence = {"contract": "DATA2WEB_SYNTHETIC_BROWSER_SCREENSHOTS_V1",
                    "customer_data_used": False, "real_browser_chromium": True,
                    "offline_http_requests": 0, "js_errors": 0,
                    "sale_approved": False, "screenshots": []}
        for name in SHOTS:
            raw = fake_fixture_png()
            (shots / name).write_bytes(raw)
            evidence["screenshots"].append(
                {"filename": name, "bytes": len(raw),
                 "sha256": hashlib.sha256(raw).hexdigest()})
        (shots / "CAPTURE_EVIDENCE.json").write_text(json.dumps(evidence), "utf-8")
        return evidence

    def test_no_screenshot_evidence_fails_without_creating_output(self):
        with self.assertRaises(ValueError):
            create_registration_kit(self.zip, self.preview, source_sha="a"*40)
        self.assertFalse(self.zip.exists())

    def test_valid_synthetic_fixture_package_and_create_only(self):
        self.prepare_fake_capture()
        result = create_registration_kit(self.zip, self.preview, source_sha="a"*40)
        self.assertEqual(result["member_count"], 11)
        self.assertTrue(result["verified"])
        self.assertFalse(result["sale_approved"])
        self.assertFalse(result["customer_data_used"])
        data = self.zip.read_bytes()
        with self.assertRaises(FileExistsError):
            create_registration_kit(self.zip, self.preview, source_sha="a"*40)
        self.assertEqual(self.zip.read_bytes(), data)

    def test_screenshot_mutation_fails_before_output(self):
        self.prepare_fake_capture()
        with (self.preview / "screenshots" / SHOTS[0]).open("ab") as f:
            f.write(b"tampered")
        with self.assertRaises(ValueError):
            create_registration_kit(self.zip, self.preview, source_sha="a"*40)
        self.assertFalse(self.zip.exists())

    def test_client_source_substitution_fails_before_output(self):
        self.prepare_fake_capture()
        with (self.preview / SOURCE).open("ab") as f:
            f.write(b"PRIVATE")
        with self.assertRaises(ValueError):
            create_registration_kit(self.zip, self.preview, source_sha="a"*40)
        self.assertFalse(self.zip.exists())

    def test_missing_real_source_sha_refused(self):
        self.prepare_fake_capture()
        for invalid in (None, "main", "short", "z"*40):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    create_registration_kit(self.zip, self.preview, source_sha=invalid)
        self.assertFalse(self.zip.exists())

    def test_byte_identical_given_same_commit_and_fixture(self):
        self.prepare_fake_capture()
        first = self.root / "first.zip"
        second = self.root / "second.zip"
        a = create_registration_kit(first, self.preview, source_sha="a"*40)
        b = create_registration_kit(second, self.preview, source_sha="a"*40)
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
