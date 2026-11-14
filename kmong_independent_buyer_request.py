"""Generate a synthetic-only independent buyer TEST REQUEST, never acceptance.

Create-only deterministic archive. An external human must execute on their
own real device; this file and all CI evidence are merely preparation.
No real customer data, personal identifiers, tokens or customer upload.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
from zipfile import ZipFile, ZipInfo, ZIP_STORED

from kmong_weekend_demo import LEAF, REPORT, SOURCE, sample_csv_bytes
from path_policy import assert_no_links, read_bounded_source
from verify_customer_folder import verify_customer_folder

CONTRACT = "DATA2WEB_INDEPENDENT_BUYER_TEST_REQUEST_V1"
ROOT_FILES = ("index.html", "delivery.zip", "receipt.json", SOURCE)
EXTRA_FILES = ("README_INDEPENDENT_TEST_KO.txt", "REVIEW_FORM_BLANK.json")
ZIP_NAMES = set(ROOT_FILES + EXTRA_FILES + ("REQUEST_MANIFEST.json",))
MAX_ZIP = 28_000_000
SHA40 = re.compile(r"[0-9a-f]{40}\Z")


def _no_duplicate_keys(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise ValueError("Duplicate acceptance template/manifest key")
        d[key] = value
    return d


def _read_json(blob):
    result = json.loads(blob.decode("utf-8"),
                        object_pairs_hook=_no_duplicate_keys,
                        parse_constant=lambda x: (_ for _ in ()).throw(ValueError("Nonfinite")))
    if not isinstance(result, dict):
        raise ValueError("Evidence object must be JSON")
    return result


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


GUIDE = (
    "DATA2WEB — 독립 구매자 기기 수용 요청 (합성 데이터 전용)\n"
    "\n"
    "이 ZIP은 고객이 아닌 가상 상품 8개의 오프라인 시험요청서이며, "
    "이미 합격한 고객 결과·보안 인증·상업판매 허가가 아닙니다.\n"
    "1. 새 시험 폴더에 본 ZIP을 압축 해제하십시오. 실제 고객 파일은 추가하지 마세요.\n"
    "2. index.html을 Chrome 또는 Edge에서 오프라인(file://)으로 엽니다.\n"
    "3. 검색에 '가상 노트'를 넣고 1건 표시되는지, 분류·정렬·상세·인쇄가 동작하는지 확인하세요.\n"
    "4. 개발자 도구 Network/Console 등 가능한 수단으로 외부 요청과 오류를 확인하세요.\n"
    "5. delivery.zip / receipt.json은 원본 무결성 확인 시연 자료입니다.\n"
    "6. 본인의 실제 OS·브라우저 버전과 각 확인 PASS/FAIL/NOT_RUN, 재현단계를 "
    "별도 결과로 기록하세요. 실명·이메일·전화번호·장비 ID·계정·고객 자료는 제공하지 마세요.\n"
    "7. REVIEW_FORM_BLANK.json은 전부 NOT_RUN/FALSE 초기값이며, 실제 시험 후에도 "
    "기술 테스트를 판매권·법적자료사용동의·외부 독립 보안감사로 해석하면 안 됩니다.\n"
    "8. 검토 결과와 원본 Git SHA는 당사자 간 권한이 확인된 경로로 전달해야 합니다. "
    "GitHub 저장소에 자동 전송하는 기능은 없습니다.\n"
    "9. 검토자도 평가자의 독립성·기기 소유·실제 실행 여부를 증빙해야 하며 "
    "개발팀 내부 CI만으로 독립 수용이 아닙니다.\n"
).encode("utf-8")


def _blank_form(source_sha):
    return {
        "contract": "DATA2WEB_BUYER_REAL_DEVICE_RESULT_FORM_V1",
        "request_source_sha": source_sha,
        "synthetic_only": True,
        "actual_real_device_run": False,
        "reviewer_independent_of_development": False,
        "reviewer_device_os": "NOT_RECORDED",
        "browser_and_version": "NOT_RECORDED",
        "steps": {
            "offline_file_open": "NOT_RUN",
            "search_single_result": "NOT_RUN",
            "category_sort_detail": "NOT_RUN",
            "print": "NOT_RUN",
            "network_zero": "NOT_RUN",
            "console_no_runtime_errors": "NOT_RUN",
            "zip_receipt_review": "NOT_RUN",
        },
        "observed_result": "NOT_RUN",
        "buyer_acceptance_verified": False,
        "independent_human_security_audit_completed": False,
        "source_data_rights_verified": False,
        "sale_approved": False,
        "claim_to_100_points": False,
        "requires_further_human_review": True,
    }


def _collect_demo(preview, sha):
    if not isinstance(sha, str) or not SHA40.fullmatch(sha):
        raise ValueError("Exact source commit SHA must be supplied")
    assert_no_links(preview)
    if not preview.is_dir():
        raise ValueError("Existing synthetic preview directory required")
    source = read_bounded_source(preview / SOURCE, max_bytes=8_000_000)
    if source != sample_csv_bytes():
        raise ValueError("Non-synthetic data refused")
    report = _read_json(read_bounded_source(preview / REPORT, max_bytes=20_000))
    if (report.get("contract") != "DATA2WEB_KMONG_SYNTHETIC_DEMO_V1"
            or report.get("sample_only") is not True
            or report.get("customer_data_used") is not False
            or report.get("sale_approved") is not False
            or report.get("rows") != 8
            or report.get("source_sha256") != _sha(source)):
        raise ValueError("Unapproved or altered synthetic evidence")
    delivery = preview / LEAF
    checked = verify_customer_folder(delivery)
    if (checked.get("verified") is not True
            or checked.get("sale_approved") is not False
            or checked.get("zip_sha256") != report.get("zip_sha256")):
        raise ValueError("Original synthetic customer folder integrity missing")
    blobs = {SOURCE: source}
    for name, limit in (("index.html", 20_000_000),
                        ("delivery.zip", 24_000_000),
                        ("receipt.json", 256_000)):
        blobs[name] = read_bounded_source(delivery / name, max_bytes=limit)
    blobs["README_INDEPENDENT_TEST_KO.txt"] = GUIDE
    blobs["REVIEW_FORM_BLANK.json"] = (json.dumps(
        _blank_form(sha), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n").encode("utf-8")
    return blobs


def verify_request(path):
    raw = read_bounded_source(path, max_bytes=MAX_ZIP)
    with ZipFile(io.BytesIO(raw), "r") as archive:
        entries = archive.infolist()
        names = [x.filename for x in entries]
        if (len(entries) != len(ZIP_NAMES)
                or len(names) != len(set(names))
                or set(names) != ZIP_NAMES
                or archive.comment
                or archive.testzip() is not None
                or any(x.extra or x.comment or x.flag_bits or x.is_dir()
                       or x.compress_type != ZIP_STORED for x in entries)):
            raise ValueError("Unsafe buyer-test request ZIP")
        manifest = _read_json(archive.read("REQUEST_MANIFEST.json"))
        sha = manifest.get("source_commit_sha")
        if (manifest.get("contract") != CONTRACT
                or not isinstance(sha, str) or not SHA40.fullmatch(sha)
                or manifest.get("reviewer_test_completed") is not False
                or manifest.get("buyer_accepted") is not False
                or manifest.get("independent_security_audit_completed") is not False
                or manifest.get("sale_approved") is not False
                or manifest.get("real_customer_data_included") is not False):
            raise ValueError("Request cannot assert human acceptance or sale approval")
        expected = manifest.get("files_sha256")
        if not isinstance(expected, dict) or set(expected) != ZIP_NAMES - {"REQUEST_MANIFEST.json"}:
            raise ValueError("Incomplete request inventory")
        for name, hash_value in expected.items():
            if hash_value != _sha(archive.read(name)):
                raise ValueError("Request member hash mismatch")
        if archive.read(SOURCE) != sample_csv_bytes():
            raise ValueError("Non-synthetic source found in acceptance request")
        form = _read_json(archive.read("REVIEW_FORM_BLANK.json"))
        if form != _blank_form(sha):
            raise ValueError("An altered or preapproved acceptance form is forbidden")
    return {
        "request_prepared": True,
        "human_test_completed": False,
        "buyer_acceptance_verified": False,
        "independent_security_audit_completed": False,
        "sale_approved": False,
        "members": len(ZIP_NAMES),
        "sha256": _sha(raw),
    }


def create_request(output, preview, *, source_sha):
    members = _collect_demo(Path(preview), source_sha)
    members["REQUEST_MANIFEST.json"] = (
        json.dumps({
            "contract": CONTRACT,
            "source_commit_sha": source_sha,
            "reviewer_test_completed": False,
            "buyer_accepted": False,
            "independent_security_audit_completed": False,
            "sale_approved": False,
            "real_customer_data_included": False,
            "files_sha256": {name: _sha(blob) for name, blob in sorted(members.items())},
        }, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n"
    ).encode("ascii")
    target = Path(output)
    assert_no_links(target, allow_missing_leaf=True)
    if (target.suffix.lower() != ".zip" or target.exists() or target.is_symlink()
            or not target.parent.is_dir() or target.parent.is_symlink()):
        raise FileExistsError("A fresh ZIP output under existing safe parent is required")
    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                 | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "wb") as out:
        with ZipFile(out, "w", compression=ZIP_STORED, allowZip64=False) as archive:
            for name, blob in sorted(members.items()):
                member = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                member.compress_type = ZIP_STORED
                member.external_attr = 0o100600 << 16
                archive.writestr(member, blob)
    return verify_request(target)


def main():
    parser = argparse.ArgumentParser(description="Synthetic independent buyer test request, NOT approval")
    parser.add_argument("--preview", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()
    print(json.dumps(create_request(args.output, args.preview, source_sha=args.source_sha),
                     ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
