"""Cross-check approved internal SKU defaults against the commercial policy draft.

This is a consistency lint only. It cannot approve a listing, tax treatment,
consumer-law interpretation, customer contract, or sale.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from order_intake_preflight import BASIC_FORMATS, CANDIDATE_REASONS, FORMATS

ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / "docs" / "COMMERCIAL_OPERATION_POLICY_DRAFT_20261114.md"
INTERNAL_DEFAULTS_PATH = ROOT / "data" / "zero_cost_owner_policy_v1.json"


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate internal SKU policy key")
        result[key] = value
    return result


def _internal_skus(doc):
    if not isinstance(doc, dict):
        raise ValueError("Internal SKU policy must be a JSON object")
    if (doc.get("sku_policy_status") != "OWNER_APPROVED_INTERNAL_DEFAULTS_NOT_PUBLISHED"
            or doc.get("actual_marketplace_listing_approved") is not False
            or doc.get("release_status") != "RELEASE_HOLD_SALE_NO_GO"):
        raise ValueError("SKU defaults must remain internal and unpublished")
    skus = doc.get("skus")
    if not isinstance(skus, list) or len(skus) != 3:
        raise ValueError("Exactly three approved internal SKUs are expected")
    result = {}
    for sku in skus:
        if not isinstance(sku, dict) or sku.get("name") in result:
            raise ValueError("Invalid or duplicate SKU")
        for field in ("name", "price_krw", "source_limit", "row_limit",
                      "revision_count", "defect_support_days"):
            expected_type = str if field == "name" else int
            if type(sku.get(field)) is not expected_type:
                raise ValueError("Invalid internal SKU field: " + field)
        result[sku["name"]] = sku
    if set(result) != {"BASIC", "PRO", "BUSINESS"}:
        raise ValueError("Unexpected internal SKU set")
    return result


def _table_rows(markdown):
    lines = markdown.splitlines()
    header = next((i for i, line in enumerate(lines)
                   if line.strip().startswith("| SKU |")), None)
    if header is None or header + 1 >= len(lines):
        raise ValueError("SKU decision table is missing")
    rows = {}
    for line in lines[header + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] in rows:
            raise ValueError("SKU table must have five columns and unique rows")
        rows[cells[0]] = cells
    return rows


def validate_preorder_catalog(skus, candidate_reasons=None, basic_formats=None, formats=None):
    """Bind pre-order candidate prices and accepted formats to approved defaults."""
    candidate_reasons = CANDIDATE_REASONS if candidate_reasons is None else candidate_reasons
    basic_formats = BASIC_FORMATS if basic_formats is None else basic_formats
    formats = FORMATS if formats is None else formats
    expected_reasons = {
        name: (name + "_CANDIDATE_REAL_SOURCE_REVIEW_PENDING", sku["price_krw"])
        for name, sku in skus.items()
    }
    if dict(candidate_reasons) != expected_reasons:
        raise ValueError("Pre-order candidate names/prices disagree with approved SKU defaults")
    if set(basic_formats) != {"CSV", "TSV", "JSON"} or set(formats) != {
            "CSV", "TSV", "JSON", "XLSX"}:
        raise ValueError("Pre-order format scope disagrees with commercial matrix")


def validate_commercial_terms(markdown, internal_policy):
    """Raise ValueError on drift; otherwise return a non-sale approval report."""
    skus = _internal_skus(internal_policy)
    validate_preorder_catalog(skus)
    rows = _table_rows(markdown)
    if set(rows) != set(skus):
        raise ValueError("Commercial policy SKU rows disagree with approved defaults")
    for name, sku in skus.items():
        _, price_cell, scope, revisions, support = rows[name]
        price = re.fullmatch(r"\*{0,2}([0-9,]+)원\*{0,2}", price_cell)
        source_counts = [int(value.replace(",", ""))
                         for value in re.findall(r"([0-9][0-9,]*)개", scope)]
        row_limit = re.search(r"최대\s*([0-9][0-9,]*)행", scope)
        column_limit = re.search(r"([0-9][0-9,]*)열", scope)
        revision_count = re.search(r"([0-9]+)회", revisions)
        support_days = re.search(r"([0-9]+)일", support)
        if (not price or int(price.group(1).replace(",", "")) != sku["price_krw"]
                or not source_counts or max(source_counts) != sku["source_limit"]
                or not row_limit or int(row_limit.group(1).replace(",", "")) != sku["row_limit"]
                or not column_limit or int(column_limit.group(1).replace(",", "")) != 20
                or not revision_count or int(revision_count.group(1)) != sku["revision_count"]
                or not support_days or int(support_days.group(1)) != sku["defect_support_days"]):
            raise ValueError("Commercial policy row disagrees with internal SKU: " + name)
    disclosures = (
        "내부 기준가", "실제 게시/판매를 허용하지 않는다", "플랫폼 수수료",
        "부가세", "법률상", "전면 환불불가 금지",
        "법령상 청약철회·환불·손해배상 권리는 제한하지 않는다",
        "RELEASE HOLD", "SALE NO-GO",
    )
    if any(term not in markdown for term in disclosures):
        raise ValueError("Commercial policy boundary or consumer-rights disclosure is missing")
    return {
        "contract": "DATA2WEB_COMMERCIAL_TERMS_CONSISTENCY_V1",
        "internal_terms_consistent": True,
        "owner_approved_internal_defaults": True,
        "marketplace_listing_approved": False,
        "tax_or_legal_review_completed": False,
        "sale_approved": False,
        "score_added": 0,
    }


def inspect_commercial_terms(policy_path=POLICY_PATH,
                             internal_defaults_path=INTERNAL_DEFAULTS_PATH):
    markdown = Path(policy_path).read_text(encoding="utf-8")
    raw = Path(internal_defaults_path).read_bytes()
    if len(raw) > 20_000:
        raise ValueError("Internal SKU policy exceeds size limit")
    defaults = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_no_duplicate_keys,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError("Non-finite internal SKU policy value: " + value)
        ),
    )
    return validate_commercial_terms(markdown, defaults)


if __name__ == "__main__":
    print(json.dumps(inspect_commercial_terms(), sort_keys=True, ensure_ascii=True))
