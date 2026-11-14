"""Create-only synthetic DATA2WEB example for an eventual product listing.

Uses no real customer data, paid services, external network, or sale approval.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from data2web_single import deliver_single
from path_policy import assert_no_links
from verify_customer_folder import verify_customer_folder
from verify_delivery import verify_zip

DEMO_ROWS = (
    ("D001", "가상 노트", "문구", "2900"),
    ("D002", "가상 볼펜", "문구", "1500"),
    ("D003", "가상 서류함", "사무", "4900"),
    ("D004", "가상 스탠드", "사무", "17900"),
    ("D005", "가상 머그컵", "생활", "6500"),
    ("D006", "가상 수납함", "생활", "8700"),
    ("D007", "가상 파일", "문구", "2500"),
    ("D008", "가상 메모지", "문구", "1100"),
)
HEADER = ("id", "title", "category", "price")
LEAF = "example_customer_delivery"
SOURCE = "synthetic_inventory.csv"
NOTICE = "SYNTHETIC_DEMO_README.txt"
REPORT = "SYNTHETIC_DEMO_EVIDENCE.json"


def sample_csv_bytes():
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(DEMO_ROWS)
    return buffer.getvalue().encode("utf-8")


def _exclusive_bytes(path, content):
    with Path(path).open("xb") as output:
        output.write(content)


def build_demo(destination):
    root = Path(destination)
    assert_no_links(root, allow_missing_leaf=True)
    if root.is_symlink() or root.exists() or not root.parent.is_dir():
        raise FileExistsError("A fresh sample directory under an existing real parent is required")
    # Failure is fail-closed: leave any partial folder for explicit inspection.
    root.mkdir(mode=0o700, exist_ok=False)
    source = root / SOURCE
    content = sample_csv_bytes()
    _exclusive_bytes(source, content)
    digest = hashlib.sha256(content).hexdigest()
    folder = root / LEAF
    deliver_single(
        source, folder,
        expected_sha256=digest,
        id_column="id", title_column="title", category_column="category",
        confirm="APPROVE", ack_plaintext=True,
        privacy_classification="NO_PERSONAL_DATA_REVIEWED",
        name="DATA2WEB 가상 샘플", theme="office",
    )
    evidence = verify_customer_folder(folder)
    verified_zip = verify_zip(folder / "delivery.zip")
    if (not evidence["verified"] or evidence["sale_approved"] is not False
            or not verified_zip["verified"] or verified_zip["sale_approved"] is not False
            or source.read_bytes() != content
            or evidence["rows"] != len(DEMO_ROWS)):
        raise RuntimeError("Synthetic preview integrity failed; HOLD")
    expected = {"index.html", "delivery.zip", "receipt.json"}
    if {p.name for p in folder.iterdir()} != expected:
        raise RuntimeError("Unexpected sample delivery member; HOLD")
    guide = (
        "DATA2WEB Studio - 100% 합성 데이터 데모 (판매/실고객 납품 아님)\n"
        "1. example_customer_delivery/index.html을 Chrome/Edge에서 오프라인 열기\n"
        "2. 검색·카테고리 필터·정렬·상세·페이지를 시연\n"
        "3. example_customer_delivery/delivery.zip / receipt.json은 무결성 시연용\n"
        "4. synthetic_inventory.csv는 가상 문구·생활 상품 8개만 수록\n"
        "5. 출력 HTML에 내용이 평문 포함됨. 인터넷에 실제 고객자료 게시 금지\n"
        "6. 외부 라이선스·고객 자료 사용권·상품 판매 승인을 증명하지 않음\n"
        "7. 기존 파일은 수정/삭제하지 않으며 이미 있는 폴더 재생성을 거부함\n"
    )
    _exclusive_bytes(root / NOTICE, guide.encode("utf-8"))
    report = {
        "contract": "DATA2WEB_KMONG_SYNTHETIC_DEMO_V1",
        "sample_only": True,
        "customer_data_used": False,
        "new_cash_spend_krw": 0,
        "source_file": SOURCE,
        "source_sha256": digest,
        "delivery_folder": LEAF,
        "rows": len(DEMO_ROWS),
        "fields": list(HEADER),
        "html_sha256": evidence["html_sha256"],
        "zip_sha256": evidence["zip_sha256"],
        "receipt_sha256": evidence["receipt_sha256"],
        "independent_local_integrity_verified": True,
        "independent_security_audit_completed": False,
        "sale_approved": False,
        "status": "SYNTHETIC_PREVIEW_ONLY_RELEASE_HOLD",
    }
    _exclusive_bytes(root / REPORT, (
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8"))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Create-only synthetic Kmong demo")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(build_demo(args.output), ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
