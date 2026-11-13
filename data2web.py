"""DATA2WEB standalone CSV/JSON to offline HTML builder (stdlib only)."""
import argparse
import csv
import hashlib
import html
import json
import os
from pathlib import Path

MAX_BYTES = 8_000_000
MAX_ROWS = 10000
MAX_COLS = 40
MAX_CELL = 16000

def read_table(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.suffix.lower() not in (".csv", ".json"):
        raise ValueError("Unsupported or unsafe input")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Input too large")
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            fields = reader.fieldnames
            if not fields:
                raise ValueError("Missing header")
            rows = list(reader)
    else:
        def unique_pairs(pairs):
            obj = {}
            for key, value in pairs:
                if key in obj:
                    raise ValueError("Duplicate JSON key")
                obj[key] = value
            return obj
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_pairs)
        if not isinstance(data, list) or not data or not all(isinstance(row, dict) for row in data):
            raise ValueError("Expected nonempty JSON object array")
        fields = list(data[0])
        if any(set(row) != set(fields) for row in data):
            raise ValueError("Inconsistent JSON keys")
        rows = data
    if len(fields) > MAX_COLS or len(rows) > MAX_ROWS or len(set(fields)) != len(fields):
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
            if isinstance(value, (dict, list)):
                raise ValueError("Nested value not supported")
            cell = "" if value is None else str(value)
            if len(cell) > MAX_CELL:
                raise ValueError("Cell too large")
            record[key] = cell
        normalized.append(record)
    if path.read_bytes() != raw:
        raise ValueError("Input changed during read")
    return fields, normalized, digest

def build(input_file, output_file, id_column, title_column, category_column, approved=False):
    if not approved:
        raise ValueError("Explicit plaintext/ownership approval required")
    fields, rows, digest = read_table(input_file)
    mapping = [id_column, title_column, category_column]
    if len(set(mapping)) != 3 or not all(col in fields for col in mapping):
        raise ValueError("Select three distinct existing columns")
    ids = [r[id_column] for r in rows]
    if any(not i for i in ids) or len(ids) != len(set(ids)):
        raise ValueError("Missing or duplicate IDs")
    target = Path(output_file)
    if target.is_symlink() or target.exists() or not target.parent.is_dir():
        raise FileExistsError("Output must be a new file in an existing directory")
    payload = json.dumps({"columns": fields, "rows": rows, "mapping": mapping, "source_sha256": digest}, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    markup = """<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'"><title>DATA2WEB</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:1rem;background:#111827;color:#f9fafb}input,select{padding:.7rem;margin:.5rem;background:#fff;color:#111}table{width:100%;border-collapse:collapse}td,th{padding:.7rem;border-bottom:1px solid #4b5563;text-align:left}button{padding:.5rem}#details{white-space:pre-wrap}</style><h1>DATA2WEB</h1><p>오프라인 데이터 조회 · 원본 데이터가 HTML에 평문으로 포함됩니다.</p><label>검색 <input id="search"></label><label>분류 <select id="category"><option value="">전체</option></select></label><p id="count"></p><table><thead id="head"></thead><tbody id="body"></tbody></table><button id="prev">이전</button><span id="page"></span><button id="next">다음</button><pre id="details"></pre><script id="dataset" type="application/json">__PAYLOAD__</script><script>(function(){'use strict';const data=JSON.parse(document.getElementById('dataset').textContent);const [id,title,cat]=data.mapping;const search=document.getElementById('search'),category=document.getElementById('category'),body=document.getElementById('body');let page=0;const size=50;for(const c of [...new Set(data.rows.map(r=>r[cat]))].sort()){const o=document.createElement('option');o.value=c;o.textContent=c;category.append(o)}const tr=document.createElement('tr');for(const key of data.columns){const th=document.createElement('th');th.textContent=key;tr.append(th)}document.getElementById('head').append(tr);function render(){const q=search.value.toLocaleLowerCase();const rows=data.rows.filter(r=>(!category.value||r[cat]===category.value)&&data.columns.some(k=>r[k].toLocaleLowerCase().includes(q)));page=Math.min(page,Math.max(0,Math.ceil(rows.length/size)-1));body.replaceChildren();for(const r of rows.slice(page*size,(page+1)*size)){const row=document.createElement('tr');for(const key of data.columns){const cell=document.createElement('td');cell.textContent=r[key];row.append(cell)}row.addEventListener('click',()=>{document.getElementById('details').textContent=JSON.stringify(r,null,2)});body.append(row)}document.getElementById('count').textContent=rows.length+'건';document.getElementById('page').textContent=(page+1)+' / '+Math.max(1,Math.ceil(rows.length/size))}search.addEventListener('input',()=>{page=0;render()});category.addEventListener('change',()=>{page=0;render()});document.getElementById('prev').onclick=()=>{page=Math.max(0,page-1);render()};document.getElementById('next').onclick=()=>{page++;render()};render()})();</script></html>""".replace("__PAYLOAD__", payload)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(target, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(markup)
    return {"source_sha256": digest, "output_sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "rows": len(rows)}

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
