"""Render a self-contained, network-free HTML data browser."""
from __future__ import annotations
import html
import json

THEMES = ("office", "cafe", "inventory")
TEMPLATE = r'''<!doctype html>
<html lang="ko" data-theme="__THEME__">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'none'; connect-src 'none'; form-action 'none'; base-uri 'none'">
<title>__TITLE__ · DATA2WEB</title>
<style>
:root{color-scheme:dark;--bg:#0c1625;--surface:#152438;--edge:#29405b;--ink:#ecf4ff;--muted:#a6bed6;--accent:#77dbd4}
:root[data-theme="cafe"]{--bg:#211711;--surface:#33261f;--edge:#634a39;--ink:#fff7ee;--muted:#dbc6b4;--accent:#f1c08a}
:root[data-theme="inventory"]{--bg:#101d19;--surface:#1c3129;--edge:#365b4b;--ink:#e8fff3;--muted:#add4c2;--accent:#7fddb1}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,"Malgun Gothic",sans-serif}
main{max-width:1200px;margin:auto;padding:clamp(16px,4vw,40px)}h1{font-size:clamp(1.5rem,4vw,2.5rem);margin:.2em 0}
p{color:var(--muted)}.surface{background:var(--surface);border:1px solid var(--edge);border-radius:15px;padding:20px;margin-top:24px}
.controls{display:flex;gap:12px;flex-wrap:wrap;align-items:end}label{display:grid;gap:5px;color:var(--muted);font-size:.9em}
input,select,button{font:inherit;padding:10px 12px;border:1px solid var(--edge);border-radius:9px;background:var(--bg);color:var(--ink)}
input[type=checkbox]{width:18px;height:18px}button{cursor:pointer}button:hover{border-color:var(--accent)}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--accent)}
table{border-collapse:collapse;width:100%;min-width:540px}th,td{text-align:left;padding:12px;border-bottom:1px solid var(--edge);max-width:360px;overflow-wrap:anywhere}
th{color:var(--accent)}tbody tr{cursor:pointer}tbody tr:hover{background:var(--edge)}
.table-scroll{overflow:auto}.pages{display:flex;gap:12px;align-items:center;margin-top:16px}pre{white-space:pre-wrap;overflow-wrap:anywhere}
small{color:var(--muted)}.warning{border-left:3px solid #e9b46f;padding-left:12px}
@media print{body{background:white;color:black}.controls,.pages,.import{display:none!important}.surface{border:1px solid #888}th{color:black}}
</style></head>
<body><main>
<header><small>DATA2WEB Studio · LOCAL ONLY</small><h1>__TITLE__</h1>
<p>승인된 표 데이터로 만든 독립 HTML입니다. 서버·계정·외부 통신이 없으며 데이터는 이 HTML 파일에 평문으로 포함됩니다.</p></header>
<section class="surface" aria-label="표 검색">
<div class="controls"><label>검색 <input id="search" type="search" placeholder="모든 열에서 검색"></label>
<label>분류 <select id="category"><option value="">전체</option></select></label>
<label>정렬 <select id="sort"></select></label>
<button id="direction" type="button">오름차순</button></div>
<p id="count" role="status"></p><div class="table-scroll"><table><thead id="head"></thead><tbody id="body"></tbody></table></div>
<nav class="pages" aria-label="페이지"><button id="prev" type="button">이전</button><span id="page"></span><button id="next" type="button">다음</button></nav></section>
<section class="surface"><h2>선택한 항목</h2><pre id="details" aria-live="polite">항목을 선택하세요.</pre></section>
<section class="surface import"><h2>동일 구조 CSV 교체</h2>
<p class="warning">컬럼명과 순서가 같은 CSV만 선택할 수 있습니다. 교체는 로컬 메모리에서만 반영되고, 새 HTML을 저장해야 유지됩니다. 새 HTML에도 모든 셀의 평문이 포함됩니다.</p>
<label>로컬 CSV <input id="csv" type="file" accept=".csv,text/csv"></label>
<label><span><input id="ack" type="checkbox"> 교체 데이터의 소유권·평문 저장을 확인했습니다</span></label>
<button id="replace" type="button">선택 CSV 반영</button>
<button id="save" type="button">새 HTML 저장</button><p id="notice" role="status"></p>
</section>
<footer><small>표형 자료를 읽기 위한 오프라인 뷰어 · 판매/배포 승인과 별개입니다.</small></footer>
</main><script type="application/json" id="dataset">__PAYLOAD__</script>
<script>
(function(){"use strict";
const $=id=>document.getElementById(id);
const d=JSON.parse($("dataset").textContent);
const state={rows:d.rows.slice(),columns:d.columns.slice(),mapping:d.mapping.slice(),sourceSha:d.source_sha256,changed:false};
const [idKey,titleKey,categoryKey]=state.mapping;
let page=0,descending=false;
const PAGE=50,MAX_FILE=8000000,MAX_ROWS=10000,MAX_CELL=16000;
const collator=new Intl.Collator("ko",{numeric:true,sensitivity:"base"});
$("sort").replaceChildren();
for(const k of state.columns){const opt=document.createElement("option");opt.value=k;opt.textContent=k;$("sort").append(opt)}
$("sort").value=titleKey;
const header=document.createElement("tr");
for(const name of state.columns){const th=document.createElement("th");th.textContent=name;header.append(th)}
$("head").replaceChildren(header);
function categoryOptions(){const current=$("category").value;$("category").replaceChildren();const all=document.createElement("option");all.value="";all.textContent="전체";$("category").append(all);
for(const name of [...new Set(state.rows.map(r=>r[categoryKey]))].sort(collator.compare)){const opt=document.createElement("option");opt.value=name;opt.textContent=name;$("category").append(opt)}
$("category").value=[...$("category").options].some(x=>x.value===current)?current:""}
function render(){const query=$("search").value.toLocaleLowerCase();
const sortKey=$("sort").value;
const filtered=state.rows.filter(r=>(!$("category").value||r[categoryKey]===$("category").value)&&state.columns.some(k=>r[k].toLocaleLowerCase().includes(query)));
filtered.sort((a,b)=>{let v=collator.compare(a[sortKey],b[sortKey]);if(v===0)v=collator.compare(a[idKey],b[idKey]);return descending?-v:v});
const pages=Math.max(1,Math.ceil(filtered.length/PAGE));page=Math.max(0,Math.min(page,pages-1));$("body").replaceChildren();
for(const record of filtered.slice(page*PAGE,(page+1)*PAGE)){const tr=document.createElement("tr");tr.tabIndex=0;
for(const key of state.columns){const td=document.createElement("td");td.textContent=record[key];tr.append(td)}
const detail=()=>{$("details").textContent=JSON.stringify(record,null,2)};
tr.addEventListener("click",detail);tr.addEventListener("keydown",e=>{if(e.key==="Enter")detail()});$("body").append(tr)}
$("count").textContent=filtered.length+"건";$("page").textContent=(page+1)+" / "+pages;
$("prev").disabled=page===0;$("next").disabled=page===pages-1}
$("search").addEventListener("input",()=>{page=0;render()});$("category").addEventListener("change",()=>{page=0;render()});
$("sort").addEventListener("change",()=>{page=0;render()});
$("direction").onclick=()=>{descending=!descending;$("direction").textContent=descending?"내림차순":"오름차순";render()};
$("prev").onclick=()=>{page--;render()};$("next").onclick=()=>{page++;render()};
function parseCSV(text){
 if(text.charCodeAt(0)===0xfeff)text=text.slice(1);
 const table=[];let record=[],cell="",quoted=false,closed=false;
 function pushCell(){record.push(cell);cell="";closed=false}
 function pushRow(){pushCell();table.push(record);record=[]}
 for(let i=0;i<text.length;i++){const c=text[i];
 if(quoted){if(c==='"'){if(text[i+1]==='"'){cell+='"';i++}else{quoted=false;closed=true}}else cell+=c;continue}
 if(c==='"'&&!cell&&!closed){quoted=true;continue}
 if(c===","){pushCell();continue}
 if(c==="\r"||c==="\n"){pushRow();if(c==="\r"&&text[i+1]==="\n")i++;continue}
 if(closed)throw Error("닫힌 따옴표 뒤에 잘못된 문자가 있습니다");
 if(c==='"')throw Error("인용 형식이 잘못되었습니다");
 cell+=c;if(cell.length>MAX_CELL)throw Error("셀 길이 제한 초과")
 }
 if(quoted)throw Error("닫히지 않은 따옴표");
 if(cell!==""||record.length)pushRow();
 return table;
}
$("replace").onclick=async()=>{
 try{
  if(!$("ack").checked)throw Error("데이터 권리 및 평문 저장 확인이 필요합니다");
  const f=$("csv").files[0];if(!f||f.size>MAX_FILE||!f.name.toLowerCase().endsWith(".csv"))throw Error("8MB 이하 CSV 파일을 선택하세요");
  const table=parseCSV(await f.text());if(table.length<1)throw Error("CSV 헤더가 없습니다");
  if(table[0].length!==state.columns.length||table[0].some((h,i)=>h!==state.columns[i]))throw Error("승인된 헤더/순서와 다릅니다");
  if(table.length-1>MAX_ROWS)throw Error("행수 제한 초과");
  const draft=[],ids=new Set();
  for(const row of table.slice(1)){if(row.length!==state.columns.length||row.some(v=>v.length>MAX_CELL))throw Error("행 길이/셀 상한 오류");
   const item={};state.columns.forEach((name,i)=>{item[name]=row[i]});
   if(!item[idKey]||ids.has(item[idKey]))throw Error("ID 누락 또는 중복");ids.add(item[idKey]);draft.push(item)}
  state.rows=draft;state.changed=true;page=0;$("search").value="";categoryOptions();render();
  $("notice").textContent=draft.length+"개 행을 로컬 메모리에 반영했습니다. 새 HTML 저장을 누르세요.";
 }catch(error){$("notice").textContent="HOLD: "+error.message}
};
function safeJSON(obj){
 const escaped={"<":"\\u003c",">":"\\u003e","&":"\\u0026","\u2028":"\\u2028","\u2029":"\\u2029"};
 return JSON.stringify(obj).replace(/[<>&\u2028\u2029]/g,c=>escaped[c]);
}
$("save").onclick=()=>{
 try{
 if(!state.changed||!$("ack").checked)throw Error("명시적으로 승인된 CSV 교체 후에만 저장합니다");
 const doc={...d,rows:state.rows,source_sha256:null,import_status:"USER_LOCAL_CSV_REPLACEMENT_NOT_VERIFIED"};
 $("dataset").textContent=safeJSON(doc);
 const blob=new Blob(["<!doctype html>\n"+document.documentElement.outerHTML],{type:"text/html;charset=utf-8"});
 const a=document.createElement("a");const url=URL.createObjectURL(blob);a.href=url;a.download="DATA2WEB-local-updated.html";document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 $("notice").textContent="새 HTML 저장을 요청했습니다. 다운로드된 파일을 다시 열어 확인하세요.";
 }catch(error){$("notice").textContent="HOLD: "+error.message}
};
categoryOptions();render();window.DATA2WEB_READY=true;
})();
</script></body></html>'''

def render_html(columns, rows, mapping, source_sha256, *, name="DATA2WEB", theme="office"):
    if theme not in THEMES or not name.strip() or len(name) > 100:
        raise ValueError("Invalid theme/title")
    payload = {
        "contract": "DATA2WEB_HTML_V1", "columns": columns, "rows": rows,
        "mapping": mapping, "source_sha256": source_sha256,
        "import_status": "OWNER_APPROVED_LOCAL_BUILD",
    }
    safe_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    for original, escaped in (("&", r"\u0026"), ("<", r"\u003c"), (">", r"\u003e"),
                              ("\u2028", r"\u2028"), ("\u2029", r"\u2029")):
        safe_json = safe_json.replace(original, escaped)
    if TEMPLATE.count("__PAYLOAD__") != 1:
        raise RuntimeError("Broken renderer template")
    return (TEMPLATE.replace("__THEME__", theme)
            .replace("__TITLE__", html.escape(name, quote=True))
            .replace("__PAYLOAD__", safe_json))
