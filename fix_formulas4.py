#!/usr/bin/env python3
"""Fix formula references by locating InvariantScript values and replacing them directly."""
import re

BASE = "/home/user/jax-plumbing-powerapps/apps/asset-app/src/Controls"


def replace_invariant(content, search_snippet, new_value, label):
    """Find the InvariantScript that contains search_snippet and replace its entire value."""
    idx = content.find(search_snippet)
    if idx == -1:
        print(f"  [{label}] NOT FOUND snippet: {search_snippet[:60]!r}")
        return content, False
    # Walk back to the InvariantScript key+opening-quote
    key = '"InvariantScript":"'
    start = content.rfind(key, 0, idx)
    if start == -1:
        print(f"  [{label}] ERROR: no InvariantScript before snippet")
        return content, False
    val_start = start + len(key)   # points at first char of the value (includes the opening `"`)
    # Find end: the closing `"` that ends the value — it's followed by ,"RuleProviderType"
    end_marker = '","RuleProviderType"'
    end = content.find(end_marker, val_start)
    if end == -1:
        print(f"  [{label}] ERROR: no end marker found")
        return content, False
    old_value = content[val_start:end]
    # Wrap new_value in the same leading `"` (val_start already includes it)
    result = content[:val_start] + '"' + new_value + content[end:]
    print(f"  [{label}] Replaced {len(old_value)} chars → {len(new_value)+1} chars")
    return result, True


# ── Controls/11.json ────────────────────────────────────────────────────────
with open(f"{BASE}/11.json", "r", encoding="utf-8") as f:
    c11 = f.read()

print("=== 11.json ===")

# 1. Availability label
c11, _ = replace_invariant(
    c11,
    "ThisItem.NumberOfUnits - ThisItem.NumberOnLoan &",
    r'"Status: " & ThisItem.Status.Value',
    "avail-label",
)

# 2. Borrow / check-out Patch (identified by BorrowEmail)
NEW_BORROW = (
    r"Set(varShowSpinner, true);\r\n"
    r"Patch('Asset Register', varRecord2, {Status: {Value: \"Checked Out\"}, CheckedOutDate: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\r\n"
    r"Patch('Asset Log', Defaults('Asset Log'), {Title: varRecord2.Title & \" – \" & Text(Now(), \"dd/mm/yyyy hh:mm\"), AssetID: {Id: varRecord2.ID, Value: varRecord2.Title}, Action: {Value: \"Check Out\"}, DateTime: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\r\n"
    r"Select(icnCancel);\r\n"
    r"Set(varShowSpinner, false)"
)
c11, _ = replace_invariant(c11, "BorrowEmail: User().Email", NEW_BORROW, "borrow-patch")

# 3. Admin reset (already has Asset Log/Register names but still has NumberOnLoan)
NEW_RESET = r'Notify(\"Admin reset disabled in this version.\", NotificationType.Warning)'
c11, _ = replace_invariant(c11, "NumberOnLoan:0}", NEW_RESET, "reset")

with open(f"{BASE}/11.json", "w", encoding="utf-8") as f:
    f.write(c11)
print("[11.json] Written.\n")


# ── Controls/34.json ────────────────────────────────────────────────────────
with open(f"{BASE}/34.json", "r", encoding="utf-8") as f:
    c34 = f.read()

print("=== 34.json ===")

# 1. Gallery filter (BorrowEmail in toggle branch)
c34, _ = replace_invariant(
    c34,
    "Filter('Asset Log', BorrowEmail",
    r"Filter('Asset Register', Status.Value = \"Checked Out\")",
    "filter-toggle",
)

# 2. QTY Borrowed label
c34, _ = replace_invariant(
    c34,
    "QTYBorrowed",
    r'\"Checked out: \" & Text(ThisItem.CheckedOutDate, \"dd/mm/yyyy\")',
    "qty-label",
)

# 3. Status label with DateActualReturn
c34, _ = replace_invariant(
    c34,
    "ThisItem.DateActualReturn)",
    r'\"Status: \" & ThisItem.Status.Value',
    "status-label",
)

# 4. Full return/check-in Patch (identified by NumberOnLoan in 34.json)
NEW_RETURN = (
    "Patch('Asset Register', varRecord3, {Status: {Value: \\\"Available\\\"}, CurrentAssignedTo: Blank(), CheckedOutDate: Blank(), ExpectedReturnDate: Blank()});\\n"
    "Patch('Asset Log', Defaults('Asset Log'), {Title: varRecord3.Title & \\\" \\u2013 \\\" & Text(Now(), \\\"dd/mm/yyyy hh:mm\\\"), AssetID: {Id: varRecord3.ID, Value: varRecord3.Title}, Action: {Value: \\\"Check In\\\"}, DateTime: Now()});\\n"
    "Set(varShowConfirm, false);\\n"
    "Set(varRecord3, Blank())"
)
c34, _ = replace_invariant(c34, "NumberOnLoan: SharedItemToPatch.NumberOnLoan", NEW_RETURN, "return-patch")

with open(f"{BASE}/34.json", "w", encoding="utf-8") as f:
    f.write(c34)
print("[34.json] Written.\n")


# ── Sanity check ────────────────────────────────────────────────────────────
print("=== Sanity Check ===")
for name, content in [("11.json", c11), ("34.json", c34)]:
    bad_found = False
    for bad in ["BorrowEmail", "NumberOnLoan", "NumberOfUnits", "QTYBorrowed",
                "ItemBorrowedTitle", "DatePlannedReturn", "DateActualReturn",
                "ItemBorrowed:"]:
        if bad in content:
            print(f"  WARNING [{name}]: still contains '{bad}'")
            bad_found = True
    if not bad_found:
        print(f"  [{name}] OK — no old references found.")
