"""Offline operator copy retention review with no real customer content."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from operator_copy_retention import (
    CONTRACT, parse_metadata, review_copy, synthetic_example,
    validate_metadata, validate_result, write_new_report,
)


NOW = datetime(2026, 11, 14, 12, 0, tzinfo=timezone.utc)


def doc_at(days_ago=0):
    record=synthetic_example()
    record["received_at_utc"]=(NOW-timedelta(days=days_ago)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    record["per_order_rights_claimed"]=True
    record["per_order_plaintext_ack_claimed"]=True
    return record


class OperatorCopyRetentionTests(unittest.TestCase):
    def test_within_policy_window_still_not_customer_approval(self):
        record=review_copy(doc_at(6),as_of=NOW)
        self.assertEqual(record["retention_due_utc"],"2026-11-15T12:00:00Z")
        self.assertEqual(record["reason_code"],"WITHIN_7_DAYS_MANUAL_REVIEW_STILL_REQUIRED")
        self.assertFalse(record["sale_approved"])
        self.assertFalse(record["customer_rights_independently_verified"])
        self.assertFalse(record["independent_disposal_verified"])
        self.assertFalse(record["automatic_deletion_performed"])
        self.assertEqual(record["score_addition"],0)

    def test_seven_day_deadline_and_overdue_are_action_due(self):
        for n in (7,8,35):
            with self.subTest(days_ago=n):
                record=review_copy(doc_at(n),as_of=NOW)
                self.assertEqual(record["reason_code"],"MANUAL_DISPOSAL_ACTION_DUE_NO_AUTO_DELETE")
                self.assertTrue(record["manual_disposal_action_due"])

    def test_purpose_completion_prompts_manual_action_before_7_days(self):
        doc=doc_at(1)
        doc["purpose_completed"]=True
        report=review_copy(doc,as_of=NOW)
        self.assertTrue(report["manual_disposal_action_due"])
        self.assertEqual(report["reason_code"],"MANUAL_DISPOSAL_ACTION_DUE_NO_AUTO_DELETE")

    def test_sensitive_confidential_and_unknown_scope_are_hold(self):
        for scope in ("PERSONAL_OR_SENSITIVE","THIRD_PARTY_CONFIDENTIAL","UNDETERMINED"):
            with self.subTest(scope=scope):
                doc=doc_at(2)
                doc["source_scope"]=scope
                report=review_copy(doc,as_of=NOW)
                self.assertEqual(report["reason_code"],"PERSONAL_CONFIDENTIAL_OR_UNKNOWN_SCOPE_HOLD")
                self.assertFalse(report["actual_customer_consent_verified"])

    def test_unproven_rights_or_plaintext_ack_stays_hold(self):
        for name in ("per_order_rights_claimed","per_order_plaintext_ack_claimed"):
            doc=doc_at(1)
            doc[name]=False
            self.assertEqual(
                review_copy(doc,as_of=NOW)["reason_code"],
                "PER_ORDER_RIGHTS_OR_PLAINTEXT_CONSENT_PENDING",
            )

    def test_statutory_exception_requires_evidence_not_fake_clearance(self):
        doc=doc_at(15)
        doc["legal_retention_exception_claimed"]=True
        record=review_copy(doc,as_of=NOW)
        self.assertEqual(record["reason_code"],"LEGAL_EXCEPTION_REQUIRES_MANUAL_EVIDENCE_REVIEW")
        self.assertFalse(record["independent_disposal_verified"])
        self.assertFalse(record["manual_disposal_action_due"])

    def test_no_copy_reported_does_not_certify_disposal(self):
        doc=doc_at(1)
        doc["operator_copy_present"]=False
        doc["received_at_utc"]=None
        result=review_copy(doc,as_of=NOW)
        self.assertEqual(result["reason_code"],"NO_OPERATOR_COPY_REPORTED_NOT_VERIFIED")
        self.assertIsNone(result["retention_due_utc"])
        self.assertFalse(result["independent_disposal_verified"])
        self.assertFalse(result["sale_approved"])

    def test_backdated_future_and_invalid_timestamps_rejected(self):
        for value in ("2026-11-15T00:00:00Z","2026-11-14T12:00:00+00:00",
                      "2026-02-30T12:00:00Z","not-a-time"):
            with self.subTest(value=value):
                doc=doc_at(1)
                doc["received_at_utc"]=value
                with self.assertRaises(ValueError):
                    review_copy(doc,as_of=NOW)

    def test_extreme_receipt_timestamp_fails_closed(self):
        doc=doc_at(1)
        doc["received_at_utc"]="9999-12-31T23:59:59Z"
        with self.assertRaises(ValueError):
            review_copy(doc,as_of=datetime(9999,12,31,23,59,59,tzinfo=timezone.utc))

    def test_closed_schema_rejects_identifiers_and_free_text(self):
        for key in ("customer_email","file_path","customer_name","actual_data_values","disposal_proof"):
            with self.subTest(field=key):
                doc=doc_at(1)
                doc[key]="synthetic-not-to-be-stored"
                with self.assertRaises(ValueError):
                    validate_metadata(doc)
        with self.assertRaises(ValueError):
            parse_metadata(b'{"contract":"a","contract":"b"}')
        with self.assertRaises(ValueError):
            parse_metadata(b'{"n":NaN}')
        with self.assertRaises(ValueError):
            parse_metadata(b"x"*4097)

    def test_booleans_and_input_date_must_be_exact(self):
        doc=doc_at(1)
        doc["operator_copy_present"]="false"
        with self.assertRaises(ValueError):
            review_copy(doc,as_of=NOW)
        doc=doc_at(1)
        doc["operator_copy_present"]=False
        with self.assertRaises(ValueError):
            review_copy(doc,as_of=NOW)
        doc=doc_at(1)
        doc["source_scope"]="UNSUPPORTED"
        with self.assertRaises(ValueError):
            validate_metadata(doc)

    def test_report_forgeries_never_can_claim_rights_or_deletion(self):
        base=review_copy(doc_at(1),as_of=NOW)
        for name,value in (
            ("sale_approved",True), ("automatic_deletion_performed",True),
            ("independent_disposal_verified",True),
            ("customer_rights_independently_verified",True),
            ("actual_customer_consent_verified",True),
            ("score_addition",2),
            ("reason_code","CUSTOMER_SAID_YES"),
        ):
            with self.subTest(field=name):
                record=deepcopy(base)
                record[name]=value
                with self.assertRaises(ValueError):
                    validate_result(record)

    def test_sensitive_or_unconsented_overdue_copy_still_writes_hold_report(self):
        for scenario in ("sensitive", "unconsented", "purpose_completed"):
            with self.subTest(scenario=scenario):
                doc=doc_at(8 if scenario != "purpose_completed" else 1)
                if scenario=="sensitive":
                    doc["source_scope"]="PERSONAL_OR_SENSITIVE"
                elif scenario=="unconsented":
                    doc["per_order_rights_claimed"]=False
                else:
                    doc["source_scope"]="PERSONAL_OR_SENSITIVE"
                    doc["purpose_completed"]=True
                report=review_copy(doc,as_of=NOW)
                self.assertTrue(report["manual_disposal_action_due"])
                self.assertEqual(report["status"],"REVIEW_ONLY_RELEASE_HOLD")
                self.assertFalse(report["sale_approved"])
                with tempfile.TemporaryDirectory() as tmp:
                    target=Path(tmp)/"retention.json"
                    write_new_report(target,report)
                    self.assertEqual(json.loads(target.read_text("utf-8")),report)

    def test_report_cannot_forge_deadline_or_disposal_consistency(self):
        present=review_copy(doc_at(8),as_of=NOW)
        absent=doc_at(1)
        absent["operator_copy_present"]=False
        absent["received_at_utc"]=None
        no_copy=review_copy(absent,as_of=NOW)
        variants=[
            (present,"retention_due_utc",None),
            (present,"retention_due_utc","2026-12-31T12:00:00Z"),
            (present,"operator_copy_present_claimed",False),
            (present,"manual_disposal_action_due",False),
            (present,"reason_code","NO_OPERATOR_COPY_REPORTED_NOT_VERIFIED"),
            (present,"reason_code","WITHIN_7_DAYS_MANUAL_REVIEW_STILL_REQUIRED"),
            (no_copy,"retention_due_utc","2026-11-21T12:00:00Z"),
            (no_copy,"manual_disposal_action_due",True),
            (no_copy,"reason_code","WITHIN_7_DAYS_MANUAL_REVIEW_STILL_REQUIRED"),
        ]
        for base,key,value in variants:
            with self.subTest(field=key,value=value):
                forged=deepcopy(base)
                forged[key]=value
                with self.assertRaises(ValueError):
                    validate_result(forged)

    def test_report_create_only_and_redacted(self):
        record=review_copy(doc_at(1),as_of=NOW)
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"report.json"
            write_new_report(target,record)
            before=target.read_bytes()
            self.assertNotIn(b"@",before)
            self.assertNotIn(b"source.csv",before)
            self.assertEqual(json.loads(before),record)
            with self.assertRaises(FileExistsError):
                write_new_report(target,record)
            self.assertEqual(target.read_bytes(),before)

    def test_cli_invalid_utf8_returns_hold_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/"malformed.json"
            source.write_bytes(bytes((255,254,128)))
            proc=subprocess.run(
                [sys.executable,"operator_copy_retention.py",
                 "--metadata-file",str(source)],
                cwd=Path(__file__).resolve().parent,
                encoding="utf-8",capture_output=True,timeout=30,
            )
            self.assertEqual(proc.returncode,2,proc.stdout+proc.stderr)
            self.assertEqual(json.loads(proc.stdout),{
                "status":"HOLD",
                "reason_code":"INVALID_LOCAL_RETENTION_METADATA",
                "sale_approved":False,
            })
            self.assertNotIn("Traceback",proc.stderr)

    def test_cli_synthetic_no_customer_data_or_auto_deletion(self):
        proc=subprocess.run(
            [sys.executable,"operator_copy_retention.py","--synthetic-self-check"],
            cwd=Path(__file__).resolve().parent,encoding="utf-8",
            capture_output=True,timeout=30,
        )
        self.assertEqual(proc.returncode,2,proc.stdout+proc.stderr)
        result=json.loads(proc.stdout)
        self.assertFalse(result["customer_source_bytes_read"])
        self.assertFalse(result["automatic_deletion_performed"])
        self.assertFalse(result["sale_approved"])
        self.assertEqual(result["retention_policy_max_days"],7)


if __name__=="__main__":
    unittest.main()
