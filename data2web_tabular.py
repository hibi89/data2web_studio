"""Fail-closed, offline XLSX and TSV importer for DATA2WEB.

Only the Excel Open XML spreadsheet *value* subset is supported. This module
never runs formulas, macros, external links, code, or remote requests. Unsupported
workbooks are rejected rather than silently dropping meaningful content.
"""
from __future__ import annotations

import csv
import io
import posixpath
import re
import zipfile
from pathlib import PurePosixPath
from xml.etree import ElementTree as ET

MAX_MEMBERS = 120
MAX_UNCOMPRESSED = 48_000_000
MAX_PART = 24_000_000
MAX_RATIO = 180
MAX_SHEETS = 30
MAX_SHARED = 100_000
MAX_ROWS = 10_000
MAX_COLS = 40
MAX_CELL = 16_000

X = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CELL = re.compile(r"([A-Z]{1,3})([1-9][0-9]{0,6})\Z")
SHEET_PART = re.compile(r"xl/worksheets/sheet[1-9][0-9]{0,2}\.xml\Z")
THEME = re.compile(r"xl/theme/theme[1-9][0-9]{0,2}\.xml\Z")
ALLOWED_PARTS = {
    "[Content_Types].xml", "_rels/.rels", "xl/workbook.xml",
    "xl/_rels/workbook.xml.rels", "xl/sharedStrings.xml",
    "xl/styles.xml", "docProps/app.xml", "docProps/core.xml",
}
ARCHIVE_PATH = re.compile(r"[A-Za-z0-9_\[\]\.\-/]+\Z")

def _valid_name(name):
    if (not name or not ARCHIVE_PATH.fullmatch(name) or "\\" in name
            or name.startswith("/") or "//" in name or
            any(x in (".", "..", "") for x in name.split("/"))):
        return False
    return name in ALLOWED_PARTS or bool(SHEET_PART.fullmatch(name) or THEME.fullmatch(name))

def _preflight(raw):
    if not raw.startswith(b"PK\x03\x04"):
        raise ValueError("XLSX must have a ZIP file signature")
    try:
        archive = zipfile.ZipFile(io.BytesIO(raw), "r")
        parts = archive.infolist()
        if not parts or len(parts) > MAX_MEMBERS:
            raise ValueError("XLSX ZIP member count is unsafe")
        seen = set()
        total = 0
        for item in parts:
            name = item.filename
            lower = name.casefold()
            if lower in seen or not _valid_name(name) or item.is_dir():
                raise ValueError("Unsupported or unsafe XLSX ZIP member")
            seen.add(lower)
            if item.flag_bits & 0x1 or item.compress_type not in (zipfile.ZIP_DEFLATED, zipfile.ZIP_STORED):
                raise ValueError("Encrypted or unusual XLSX ZIP member")
            kind = (item.external_attr >> 16) & 0o170000
            if kind == 0o120000:
                raise ValueError("XLSX ZIP symlink forbidden")
            total += item.file_size
            if (item.file_size > MAX_PART or total > MAX_UNCOMPRESSED or
                    (item.compress_size == 0 and item.file_size != 0) or
                    item.file_size > MAX_RATIO * max(1, item.compress_size)):
                raise ValueError("XLSX decompression safety limit")
        essential = {"[Content_Types].xml", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"}
        if not essential.issubset({x.filename for x in parts}):
            raise ValueError("Missing XLSX metadata")
        # testzip checks each member's CRC. Do not extract to disk or trust ZIP headers.
        if archive.testzip() is not None:
            raise ValueError("Invalid XLSX ZIP CRC")
        return archive
    except (zipfile.BadZipFile, zipfile.LargeZipFile, EOFError, RuntimeError) as e:
        raise ValueError("Malformed XLSX archive") from e

def _xml(archive, name):
    if name not in archive.namelist():
        raise ValueError("Required XLSX XML component missing")
    raw = archive.read(name)
    if b"<!doctype" in raw.lower() or b"<!entity" in raw.lower():
        raise ValueError("XLSX DTD/entity forbidden")
    try:
        return ET.fromstring(raw)
    except ET.ParseError as e:
        raise ValueError("Malformed XLSX XML") from e

def _metadata(archive):
    content = archive.read("[Content_Types].xml").lower()
    if b"spreadsheetml.sheet.main+xml" not in content:
        raise ValueError("Not a macro-free XLSX workbook")
    # All relationships in the accepted profile are internal. No hyperlink fetching.
    for part in archive.namelist():
        if part.endswith(".rels"):
            root = _xml(archive, part)
            for rel in root:
                target = rel.get("Target", "")
                if (rel.get("TargetMode", "Internal").lower() != "internal"
                        or re.match(r"^[a-z]+:", target, re.I)
                        or "\\" in target):
                    raise ValueError("External workbook relationship rejected")
    workbook = _xml(archive, "xl/workbook.xml")
    relations = _xml(archive, "xl/_rels/workbook.xml.rels")
    lookup = {}
    for rel in relations.findall(PKG + "Relationship"):
        ident = rel.get("Id", "")
        target = rel.get("Target", "")
        if not ident or ident in lookup:
            raise ValueError("Invalid workbook relationship IDs")
        if rel.get("Type", "").endswith("/worksheet"):
            if (".." in target.split("/") or not target or target.startswith("//")):
                raise ValueError("Unsafe worksheet target")
            if target.startswith("/xl/"):
                canonical = target[1:]
            elif target.startswith("xl/"):
                canonical = target
            else:
                canonical = posixpath.normpath(posixpath.join("xl", target))
            if not SHEET_PART.fullmatch(canonical) or canonical not in archive.namelist():
                raise ValueError("Worksheet path not permitted")
            lookup[ident] = canonical
    sheet_node = workbook.find(X + "sheets")
    if sheet_node is None:
        raise ValueError("Workbook has no sheets")
    sheets = []
    seen = set()
    paths = set()
    for item in sheet_node.findall(X + "sheet"):
        name = item.get("name", "")
        ident = item.get(R + "id", "")
        state = item.get("state", "visible")
        if (not name or len(name) > 100 or name in seen or
                ident not in lookup or lookup[ident] in paths or
                state not in ("visible", "hidden", "veryHidden")):
            raise ValueError("Malformed or duplicate workbook sheet")
        seen.add(name)
        paths.add(lookup[ident])
        sheets.append({"name": name, "state": state, "part": lookup[ident]})
    if not sheets or len(sheets) > MAX_SHEETS:
        raise ValueError("Unsupported workbook sheet count")
    return sheets

def list_xlsx_sheets(raw):
    with _preflight(raw) as archive:
        sheets = _metadata(archive)
        return [{"name": s["name"], "state": s["state"]} for s in sheets]

def _string_text(element):
    return "".join(x.text or "" for x in element.iter(X + "t"))

def _shared_strings(archive):
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = _xml(archive, "xl/sharedStrings.xml")
    strings = []
    for item in root.findall(X + "si"):
        if len(strings) >= MAX_SHARED:
            raise ValueError("Too many XLSX shared strings")
        value = _string_text(item)
        if len(value) > MAX_CELL:
            raise ValueError("Oversized XLSX shared-string cell")
        strings.append(value)
    return strings

def _col_index(letter):
    value = 0
    for char in letter:
        value = value * 26 + ord(char) - ord("A") + 1
    return value - 1

def _value(node, strings, allow_cached_formulas):
    formula = node.find(X + "f")
    cached = node.find(X + "v")
    if formula is not None and not allow_cached_formulas:
        raise ValueError("XLSX formula found; explicit cached-value approval required")
    if formula is not None and (cached is None or cached.text is None):
        raise ValueError("XLSX formula without cached value")
    typ = node.get("t", "n")
    if typ == "e":
        raise ValueError("XLSX error cell forbidden")
    if typ == "inlineStr":
        child = node.find(X + "is")
        if child is None:
            raise ValueError("Inline string missing")
        result = _string_text(child)
    elif typ == "s":
        if cached is None or cached.text is None or not cached.text.isdecimal():
            raise ValueError("Invalid shared string index")
        index = int(cached.text)
        if index >= len(strings):
            raise ValueError("Shared string index out of bounds")
        result = strings[index]
    elif typ == "b":
        if cached is None or cached.text not in ("0", "1"):
            raise ValueError("Invalid Boolean cell")
        result = "TRUE" if cached.text == "1" else "FALSE"
    elif typ in ("n", "str", "d"):
        result = cached.text if cached is not None and cached.text is not None else ""
        if typ == "n" and result:
            # Never calculate spreadsheet formulas, convert large numeric IDs to
            # floating point, or silently claim to reproduce Excel date formatting.
            if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?", result):
                raise ValueError("Invalid numeric cell cache")
    else:
        raise ValueError("Unsupported XLSX cell type")
    if len(result) > MAX_CELL:
        raise ValueError("XLSX cell exceeds size limit")
    return result

def parse_xlsx(raw, *, sheet=None, header_row=1, allow_cached_formulas=False):
    if isinstance(header_row, bool) or not isinstance(header_row, int) or not 1 <= header_row <= 50:
        raise ValueError("Header row must be between 1 and 50")
    with _preflight(raw) as archive:
        sheets = _metadata(archive)
        visible = [s for s in sheets if s["state"] == "visible"]
        if sheet is None:
            if len(visible) != 1:
                raise ValueError("Select a sheet by name")
            selected = visible[0]
        else:
            matching = [s for s in visible if s["name"] == sheet]
            if len(matching) != 1:
                raise ValueError("Selected sheet is missing or hidden")
            selected = matching[0]
        strings = _shared_strings(archive)
        root = _xml(archive, selected["part"])
        if root.find(X + "mergeCells") is not None:
            raise ValueError("Merged worksheet cells are unsupported")
        # Hidden worksheet content may contain values the owner did not review.
        # Never silently publish or discard it; require a new visible-source SHA.
        sheet_format = root.find(X + "sheetFormatPr")
        if (sheet_format is not None and
                sheet_format.get("zeroHeight", "0").strip().lower() not in ("0", "false")):
            raise ValueError("Hidden XLSX default rows: unhide and re-approve source")
        cols = root.find(X + "cols")
        if cols is not None:
            for col in cols.findall(X + "col"):
                if col.get("hidden", "0").strip().lower() not in ("0", "false"):
                    raise ValueError("Hidden XLSX columns: unhide and re-approve source")
        sheetdata = root.find(X + "sheetData")
        if sheetdata is None:
            raise ValueError("Missing worksheet rows")
        headers = None
        rowdata = []
        row_seen = set()
        previous_row = 0
        for node in sheetdata.findall(X + "row"):
            try:
                number = int(node.get("r", "0"))
            except ValueError as e:
                raise ValueError("Invalid worksheet row number") from e
            if (number <= previous_row or number in row_seen or number > header_row + MAX_ROWS
                    or number < 1):
                raise ValueError("Unsorted, repeated, or oversized worksheet row")
            row_seen.add(number)
            previous_row = number
            if node.get("hidden", "0").strip().lower() not in ("0", "false"):
                raise ValueError("Hidden XLSX rows: unhide and re-approve source")
            if number < header_row:
                continue
            cells = {}
            # Formatting-only empty cells are not data. A deliberately present
            # empty XML string/value is data and must not be dropped as an
            # invisible blank row (a missing mapped ID must then HOLD).
            explicit_values = False
            explicit_columns = set()
            for cell in node.findall(X + "c"):
                address = cell.get("r", "")
                m = CELL.fullmatch(address)
                if not m or int(m.group(2)) != number:
                    raise ValueError("Invalid cell reference")
                col = _col_index(m.group(1))
                if col >= MAX_COLS or col in cells:
                    raise ValueError("Duplicate or oversized worksheet column")
                cells[col] = _value(cell, strings, allow_cached_formulas)
                cached_value = cell.find(X + "v")
                if cell.find(X + "is") is not None or cached_value is not None:
                    explicit_values = True
                    explicit_columns.add(col)
            if number == header_row:
                if not cells:
                    raise ValueError("Empty worksheet header")
                last = max(cells)
                if set(cells) != set(range(last + 1)):
                    raise ValueError("Worksheet header has blank columns")
                headers = [cells[i] for i in range(last + 1)]
                if any(not h or len(h) > 200 for h in headers) or len(set(headers)) != len(headers):
                    raise ValueError("Invalid or duplicate XLSX headers")
            elif cells and (explicit_values or any(v != "" for v in cells.values())):
                if headers is None:
                    raise ValueError("Selected header row does not exist")
                if any(col >= len(headers) and (value or col in explicit_columns)
                       for col, value in cells.items()):
                    raise ValueError("Data extends beyond approved headers")
                rowdata.append({h: cells.get(i, "") for i, h in enumerate(headers)})
                if len(rowdata) > MAX_ROWS:
                    raise ValueError("XLSX row count limit")
        if headers is None:
            raise ValueError("Selected XLSX header row does not exist")
        return headers, rowdata, selected["name"]

def parse_tsv(raw):
    try:
        text = raw.decode("utf-8-sig")
        with io.StringIO(text, newline="") as stream:
            reader = csv.reader(stream, delimiter="\t", strict=True)
            headers = next(reader, None)
            if not headers or len(headers) > MAX_COLS:
                raise ValueError("TSV requires bounded nonempty header")
            if any(not x or len(x) > 200 for x in headers) or len(set(headers)) != len(headers):
                raise ValueError("Duplicate or empty TSV header")
            rows = []
            for record in reader:
                if len(rows) >= MAX_ROWS:
                    raise ValueError("TSV row count limit")
                if len(record) != len(headers):
                    raise ValueError("TSV row has inconsistent column count")
                rows.append(dict(zip(headers, record)))
    except (UnicodeDecodeError, csv.Error) as e:
        raise ValueError("Invalid TSV encoding or quoting") from e
    return headers, rows
