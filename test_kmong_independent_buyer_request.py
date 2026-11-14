"""A requested human buyer test remains NOT RUN until a person performs it."""
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from kmong_independent_buyer_request import create_request, verify_request
from kmong_weekend_demo import build_demo, SOURCE, REPORT


class BuyerRequestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.preview = self.root / "preview"
        build_demo(self.preview)
        self.out = self.root / "independent-request.zip"
        self.sha = "a" * 40

    def test_request_contains_real_synthetic_html_and_unrun_form(self):
        result = create_request(self.out, self.preview, source_sha=self.sha)
        self.assertTrue(result["request_prepared"])
        self.assertEqual(result["members"], 7)
        self.assertFalse(result["human_test_completed"])
        self.assertFalse(result["sale_approved"])
        with ZipFile(self.out) as z:
            form = json.loads(z.read("REVIEW_FORM_BLANK.json"))
            self.assertEqual(form["observed_result"], "NOT_RUN")
            self.assertFalse(form["buyer_acceptance_verified"])
            self.assertTrue(z.read("index.html").startswith(b"<!doctype html>"))
            self.assertEqual(z.read(SOURCE), (self.preview / SOURCE).read_bytes())

    def test_create_only_does_not_modify_existing_request(self):
        create_request(self.out, self.preview, source_sha=self.sha)
        old = self.out.read_bytes()
        with self.assertRaises(FileExistsError):
            create_request(self.out, self.preview, source_sha=self.sha)
        self.assertEqual(self.out.read_bytes(), old)

    def test_reproducible_exact_bytes(self):
        one = self.root / "one.zip"
        two = self.root / "two.zip"
        a = create_request(one, self.preview, source_sha=self.sha)
        b = create_request(two, self.preview, source_sha=self.sha)
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertEqual(one.read_bytes(), two.read_bytes())

    def test_substituted_source_fails_before_creation(self):
        with (self.preview / SOURCE).open("ab") as f:
            f.write(b"\nPRIVATE INFORMATION")
        with self.assertRaises(ValueError):
            create_request(self.out, self.preview, source_sha=self.sha)
        self.assertFalse(self.out.exists())

    def test_forced_sale_flag_in_demo_fails_closed(self):
        path = self.preview / REPORT
        doc = json.loads(path.read_text("utf-8"))
        doc["sale_approved"] = True
        path.write_text(json.dumps(doc), "utf-8")
        with self.assertRaises(ValueError):
            create_request(self.out, self.preview, source_sha=self.sha)
        self.assertFalse(self.out.exists())

    def test_invalid_sha_and_preapproved_form_rejected(self):
        for invalid in ("unknown", "x"*40, "", None):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    create_request(self.out, self.preview, source_sha=invalid)
                self.assertFalse(self.out.exists())
        create_request(self.out, self.preview, source_sha=self.sha)
        raw = self.out.read_bytes()
        from zipfile import ZIP_STORED
        with ZipFile(io.BytesIO(raw)) as z:
            members = {n: z.read(n) for n in z.namelist()}
        form = json.loads(members["REVIEW_FORM_BLANK.json"])
        form["buyer_acceptance_verified"] = True
        members["REVIEW_FORM_BLANK.json"] = json.dumps(form).encode()
        man = json.loads(members["REQUEST_MANIFEST.json"])
        man["files_sha256"]["REVIEW_FORM_BLANK.json"] = hashlib.sha256(
            members["REVIEW_FORM_BLANK.json"]
        ).hexdigest()
        members["REQUEST_MANIFEST.json"] = json.dumps(man).encode()
        tampered = self.root / "tampered.zip"
        with ZipFile(tampered, "w", compression=ZIP_STORED) as z:
            for name, data in members.items():
                z.writestr(name, data)
        with self.assertRaises(ValueError):
            verify_request(tampered)


if __name__ == "__main__":
    unittest.main()
