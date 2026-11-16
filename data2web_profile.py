"""Privacy-conservative aggregate schema preview; never print a customer's cell values.

Column names are owner-supplied metadata and may still be sensitive. No heuristic
can certify that a dataset is free from personal information.
"""
from __future__ import annotations
import re
from collections import Counter

NUMBER=re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
ISO_DATE=re.compile(r"^\d{4}-\d{2}-\d{2}(?:[T ][0-9:.+Z-]+)?$")
BOOL={"true","false","yes","no"}
def _kind(nonempty):
    if not nonempty:
        return "empty"
    if all(NUMBER.fullmatch(x) for x in nonempty):
        return "number_text"
    if all(ISO_DATE.fullmatch(x) for x in nonempty):
        return "iso_date_text"
    if all(x.lower() in BOOL for x in nonempty):
        return "boolean_text"
    return "text"

def profile_table(columns, rows):
    """Bounded counts/hints only; never emit distinct literal values."""
    output=[]
    for col in columns:
        values=[r[col] for r in rows]
        used=[v for v in values if v.strip()]
        output.append({
            "name":col,
            "kind_hint":_kind(used),
            "blank_cells":len(values)-len(used),
            "distinct_nonblank":len(set(used)),
            "duplicate_nonblank":len(used)-len(set(used)),
        })
    unique_rows={tuple(row[col] for col in columns) for row in rows}
    return {
        "row_count":len(rows),"column_count":len(columns),
        "duplicate_full_rows":len(rows)-len(unique_rows),
        "columns":output,
        "personal_data_status":"OWNER_REVIEW_REQUIRED_NOT_AUTOMATICALLY_CLEARED",
        "values_revealed":False,
    }
