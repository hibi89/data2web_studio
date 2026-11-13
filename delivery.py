"""Deterministic, create-only delivery packaging of already approved HTML."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from path_policy import assert_no_links, read_bounded_source
from zipfile import ZipFile, ZipInfo, ZIP_STORED
from verify_delivery import verify_zip

GUIDE = ("DATA2WEB Studio — 로컬 열람 안내\n"
         "1. index.html을 Chrome 또는 Edge에서 로컬로 엽니다.\n"
         "2. 검색·분류·정렬·상세·페이지 기능은 오프라인으로 동작합니다.\n"
         "3. 원본 데이터는 HTML에 평문 포함됩니다. 공유 전 권리를 확인하십시오.\n"
         "4. 교체는 동일 헤더 CSV만 허용됩니다. 변경 후 새 HTML을 저장해 재열기하세요.\n"
         "5. 이 ZIP의 SHA256 검증은 진위/서명/판매허가를 보증하지 않습니다.\n"
         "6. 원본 파일과 이전 결과를 보관하십시오. 판매/배포 승인: HOLD.\n").encode("utf-8")

def package_html(html_path, zip_path, receipt):
    html_path, zip_path = Path(html_path), Path(zip_path)
    assert_no_links(html_path)
    assert_no_links(zip_path,allow_missing_leaf=True)
    if (not html_path.is_file() or html_path.is_symlink() or zip_path.is_symlink()
            or zip_path.exists() or not zip_path.parent.is_dir()
            or zip_path.parent.is_symlink() or zip_path.suffix.lower() != ".zip"):
        raise ValueError("Package output must be a fresh, safe ZIP path")
    html = read_bounded_source(html_path,max_bytes=20_000_000)
    if hashlib.sha256(html).hexdigest() != receipt.get("output_sha256"):
        raise ValueError("HTML receipt/hash mismatch")
    manifest = {
        "contract":"DATA2WEB_PACKAGE_V1", "source_sha256":receipt["source_sha256"],
        "html_sha256":hashlib.sha256(html).hexdigest(), "guide_sha256":hashlib.sha256(GUIDE).hexdigest(),
        "rows":receipt["rows"], "sheet":receipt.get("sheet"),
        "header_row":receipt.get("header_row",1),
        "cached_formulas":receipt.get("cached_formulas",False),
        "source_receipts":receipt.get("source_receipts"),
        "plaintext_ack":True, "sale_approved":False,
        "status":"RELEASE_HOLD",
    }
    encoded = (json.dumps(manifest,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
    with zip_path.open("xb") as file:
        with ZipFile(file,"w",compression=ZIP_STORED,allowZip64=False) as zf:
            for name,data in (("index.html",html),("manifest.json",encoded),("README_KO.txt",GUIDE)):
                info = ZipInfo(name, date_time=(1980,1,1,0,0,0))
                info.compress_type = ZIP_STORED
                info.external_attr = 0o100600 << 16
                zf.writestr(info,data)
    return verify_zip(zip_path)
