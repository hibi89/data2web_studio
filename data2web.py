"""DATA2WEB standalone CSV/JSON to offline HTML builder (stdlib only)."""
import argparse
import csv
import hashlib
import html
import json
import os
from pathlib import Path
from path_policy import assert_no_links, read_bounded_source

MAX_BYTES = 8_000_000
MAX_ROWS = 10000
MAX_COLS = 40
MAX_CELL = 16000

def read_table(path, *, sheet=None, header_row=1, allow_cached_formulas=False):
    path = Path(path)
    assert_no_links(path)
    if path.is_symlink() or not path.is_file() or path.suffix.lower() not in (".csv", ".json", ".tsv", ".xlsx"):
        raise ValueError("Unsupported or unsafe input")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Input too large")
    raw = read_bounded_source(path,max_bytes=MAX_BYTES)
    digest = hashlib.sha256(raw).hexdigest()
    if path.suffix.lower() == ".csv":
        from io import StringIO
        with StringIO(raw.decode("utf-8-sig"), newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            fields = reader.fieldnames
            if not fields:
                raise ValueError("Missing header")
            rows = list(reader)
    elif path.suffix.lower() == ".tsv":
        from data2web_tabular import parse_tsv
        fields, rows = parse_tsv(raw)
    elif path.suffix.lower() == ".xlsx":
        from data2web_tabular import parse_xlsx
        fields, rows, _ = parse_xlsx(raw, sheet=sheet, header_row=header_row,
                                     allow_cached_formulas=allow_cached_formulas)
    else:
        def unique_pairs(pairs):
            obj = {}
            for key, value in pairs:
                if key in obj:
                    raise ValueError("Duplicate JSON key")
                obj[key] = value
            return obj
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              ValueError("Non-finite JSON numeric constant")))
        # A flat JSON object is one record; arrays of flat records remain unchanged.
        # Never guess a nested records container or silently flatten nested content.
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list) or not data or not all(isinstance(row, dict) for row in data):
            raise ValueError("Expected a flat JSON object or nonempty object array")
        fields = list(data[0])
        if any(set(row) != set(fields) for row in data):
            raise ValueError("Inconsistent JSON keys")
        rows = data
    if len(fields) > MAX_COLS or len(rows) > MAX_ROWS or len(set(fields)) != len(fields) or any(f in ("__proto__", "prototype", "constructor") for f in fields):
        raise ValueError("Invalid column or row count")
    if any(not isinstance(f, str) or not f or len(f) > 200 for f in fields):
        raise ValueError("Invalid header")
    normalized = []
    for row in rows:
        if set(row) != set(fields):
            raise ValueError("Invalid row")
        record = {}
        for key in fields:
            value = row[key]
            if not isinstance(value, (str, int, float, bool, type(None))) or (
                    isinstance(value, float) and not __import__("math").isfinite(value)) or isinstance(value, (dict, list)):
                raise ValueError("Nested value not supported")
            cell = "" if value is None else str(value)
            if len(cell) > MAX_CELL:
                raise ValueError("Cell too large")
            record[key] = cell
        normalized.append(record)
    if read_bounded_source(path,max_bytes=MAX_BYTES) != raw:
        raise ValueError("Input changed during parsing")
    return fields, normalized, digest

def build(input_file, output_file, id_column, title_column, category_column, approved=False, expected_sha256=None, name='DATA2WEB', theme='office', sheet=None, header_row=1, allow_cached_formulas=False):
    if not approved:
        raise ValueError("Explicit plaintext/ownership approval required")
    if Path(input_file).suffix.lower() == ".xlsx" and not sheet:
        raise ValueError("XLSX requires explicit owner sheet selection")
    fields, rows, digest = read_table(input_file, sheet=sheet, header_row=header_row,
                                     allow_cached_formulas=allow_cached_formulas)
    if expected_sha256 is not None and digest != expected_sha256:
        raise ValueError("Source SHA256 changed since owner inspection")
    mapping = [id_column, title_column, category_column]
    if len(set(mapping)) != 3 or not all(col in fields for col in mapping):
        raise ValueError("Select three distinct existing columns")
    ids = [r[id_column] for r in rows]
    if any(not i for i in ids) or len(ids) != len(set(ids)):
        raise ValueError("Missing or duplicate IDs")
    target = Path(output_file)
    if target.is_symlink() or target.exists():
        raise FileExistsError("Output must be a new file")
    assert_no_links(target,allow_missing_leaf=True)
    if target.suffix.lower() != ".html" or target.is_symlink() or target.exists() or not target.parent.is_dir() or target.parent.is_symlink():
        raise FileExistsError("Output must be a new file in an existing directory")
    from data2web_web import render_html
    markup = render_html(fields, rows, mapping, digest, name=name, theme=theme,
                         source_sheet=sheet, source_header_row=header_row,
                         cached_formulas=allow_cached_formulas)
    output_bytes = markup.encode("utf-8")
    if len(output_bytes) > 20_000_000:
        raise ValueError("Output HTML exceeds local delivery limit")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(target, flags, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(output_bytes)
    if hashlib.sha256(read_bounded_source(input_file,max_bytes=MAX_BYTES)).hexdigest() != digest:
        raise ValueError("Source modified after generation; output HOLD")
    # Reopen using an identity-checked, size-bounded descriptor. A mutable
    # output pathname must not bypass the same safety checks as source input.
    output_digest = hashlib.sha256(read_bounded_source(target,max_bytes=20_000_000)).hexdigest()
    if output_digest != hashlib.sha256(output_bytes).hexdigest():
        raise ValueError("Output integrity mismatch; output HOLD")
    return {"source_sha256": digest, "output_sha256": output_digest, "rows": len(rows),
            "columns": fields, "mapping": {"id": id_column, "title": title_column, "category": category_column},
            "theme": theme, "sheet": sheet, "header_row": header_row,
            "cached_formulas": allow_cached_formulas, "sale_approved": False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--approve-plaintext-and-rights", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(args.source,args.output,args.id,args.title,args.category,args.approve_plaintext_and_rights)))

if __name__ == "__main__":
    main()
