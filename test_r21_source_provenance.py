"""R21 source blob checks: exact source revision, no fake legal clearance."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from r21_source_provenance import (
    ROOT, ROLES, check_source_provenance, git_blob_oid,
    read_pins, validate_pins, _unique
)
from shipping_rights_preflight import synthetic_shipping_preflight


class SourceProvenanceGate(unittest.TestCase):
    def test_all_real_sources_pinned_and_still_hold(self):
        result=check_source_provenance()
        self.assertEqual(result["source_files_verified"],6)
        self.assertEqual(result["status"],"SOURCE_BLOBS_PINNED_RIGHTS_PENDING")
        self.assertFalse(result["commercial_release_approved"])
        self.assertEqual(result["score_addition"],0)

    def test_windows_crlf_checkout_is_same_git_blob(self):
        # Git checkout autocrlf modifies the WORKTREE representation only.
        from r21_source_provenance import source_checkout_matches_git_blob
        before=b"first line\nsecond line\n"
        expected=git_blob_oid(before)
        checked_out=before.replace(b"\n",b"\r\n")
        self.assertTrue(source_checkout_matches_git_blob(checked_out,expected))
        self.assertFalse(source_checkout_matches_git_blob(
            checked_out+b"unexpected\r\n",expected
        ))
        self.assertFalse(source_checkout_matches_git_blob(
            checked_out.replace(b"second",b"altered"),expected
        ))
        self.assertFalse(source_checkout_matches_git_blob(
            b"first line\rsecond line\n",expected
        ))

    def test_source_pins_survive_windows_style_worktree_line_endings(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)
            for filename in ROLES:
                raw=(ROOT/filename).read_bytes()
                # Normalize Git's text checkout LF/CRLF on any runner before
                # simulating a Windows-style worktree in this temporary copy.
                canonical=raw.replace(b"\r\n",b"\n")
                (dest/filename).write_bytes(canonical.replace(b"\n",b"\r\n"))
            self.assertEqual(check_source_provenance(root=dest)["source_files_verified"],6)

    def test_git_blob_oid_against_known_reference(self):
        self.assertEqual(git_blob_oid(b"hello\n"),
                         "ce013625030ba8dba906f756967f9e9ca394464a")
        with self.assertRaises(TypeError):
            git_blob_oid("hello")

    def test_one_byte_source_drift_is_hold_without_touching_repo(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)
            for filename in ROLES:
                shutil.copyfile(ROOT/filename,dest/filename)
            target=dest/"data2web_web.py"
            target.write_bytes(target.read_bytes()+b"\n# SYNTHETIC CHANGE\n")
            with self.assertRaisesRegex(ValueError,"source drift"):
                check_source_provenance(root=dest)
        self.assertEqual(check_source_provenance()["source_files_verified"],6)

    def test_missing_source_refuses_to_certify(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                check_source_provenance(root=Path(temp))

    def test_forged_rights_independence_and_score_refused(self):
        for field,value in (
            ("rights_evidence_complete",True),
            ("third_party_notice_approved",True),
            ("commercial_release_approved",True),
            ("independent_security_audit_completed",True),
            ("score_addition",4),
        ):
            with self.subTest(field=field):
                doc=copy.deepcopy(read_pins())
                doc[field]=value
                with self.assertRaises(ValueError):
                    validate_pins(doc)

    def test_filename_role_digest_and_extra_personal_data_refused(self):
        for mode in ("unsafe_path","new_key","repeated_file","wrong_role","bad_sha"):
            with self.subTest(mode=mode):
                doc=copy.deepcopy(read_pins())
                if mode=="unsafe_path":
                    doc["source_files"][0]["path"]="../customer-source.csv"
                if mode=="new_key":
                    doc["customer_email"]="private@example.invalid"
                if mode=="repeated_file":
                    doc["source_files"][1]=copy.deepcopy(doc["source_files"][0])
                if mode=="wrong_role":
                    doc["source_files"][0]["role"]="LICENSE_APPROVED"
                if mode=="bad_sha":
                    doc["source_files"][0]["git_blob_sha1"]="f"*39
                with self.assertRaises(ValueError):
                    validate_pins(doc)

    def test_duplicate_key_and_nonfinite_refused(self):
        with self.assertRaises(ValueError):
            json.loads('{"source_files":[],"source_files":[]}',
                       object_pairs_hook=_unique)
        doc=copy.deepcopy(read_pins())
        doc["source_snapshot_commit"]="a"*39
        with self.assertRaises(ValueError):
            validate_pins(doc)

    def test_actual_synthetic_shipping_stays_unapproved(self):
        report=synthetic_shipping_preflight()
        self.assertEqual(report["status"],"HOLD_OWNER_IP_NOTICE_EXTERNAL_AUDIT")
        self.assertFalse(report["commercial_release_approved"])
        self.assertEqual(report["score_addition"],0)

    def test_command_line_reports_only_source_metadata(self):
        p=subprocess.run(
            [sys.executable,"r21_source_provenance.py"],
            cwd=ROOT,capture_output=True,text=True,timeout=30
        )
        self.assertEqual(p.returncode,0,p.stderr)
        obj=json.loads(p.stdout)
        self.assertEqual(obj["source_files_verified"],6)
        self.assertFalse(obj["rights_evidence_complete"])
        self.assertNotIn("customer_email",p.stdout)


if __name__=="__main__":
    unittest.main()
