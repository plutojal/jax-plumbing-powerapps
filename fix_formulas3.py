#!/usr/bin/env python3
"""Fix remaining old formula references — using exact byte-level strings."""

BASE = "/home/user/jax-plumbing-powerapps/apps/asset-app/src/Controls"

# In these JSON files:
#   single quotes  →  literal '  (0x27, unescaped)
#   double quotes  →  \"  (backslash + quote, i.e. \\" in the raw file)
#   line endings   →  \r\n  (literal backslash-r-backslash-n in file)
# In Python source we use r"..." raw strings so we don't have to double-escape.

def rep(content, old, new, label):
    count = content.count(old)
    if count:
        print(f"  [{label}] {count}x: {old[:60]!r}")
        return content.replace(old, new)
    else:
        print(f"  [{label}] NOT FOUND: {old[:60]!r}")
        return content


# ── Controls/11.json ────────────────────────────────────────────────────────
with open(f"{BASE}/11.json", "r", encoding="utf-8") as f:
    c11 = f.read()

print("=== 11.json ===")

# 1. Availability label  (double quotes escaped as \\")
c11 = rep(
    c11,
    r'ThisItem.NumberOfUnits - ThisItem.NumberOnLoan & \" of \" & ThisItem.NumberOfUnits & \" are available to borrow\"',
    r'"Status: " & ThisItem.Status.Value',
    "avail-label",
)

# 2. Full borrow/check-out Patch
OLD_BORROW = (
    r"Set(varShowSpinner, true);\r\n"
    r"//Update the count in the SharePoint list for tracking inventory\r\n"
    r"Patch('Asset Register', varRecord2, {NumberOnLoan: varRecord2.NumberOnLoan + Dropdown1.Selected.Value});\r\n"
    r"//Turn the pen input into a base64 string\r\n"
    r"Set(varPenInput, JSON(PenInput1.Image,JSONFormat.IncludeBinaryData));\r\n"
    r"Set(varPenInputClean, Mid(varPenInput, 2, Len(varPenInput)-2));\r\n"
    r"//Update the list of who has borrowed what including a copy of their signature\r\n"
    r'Patch(\'Asset Log\', Defaults(\'Asset Log\'), {Title: User().FullName, BorrowEmail: User().Email, QTYBorrowed: Dropdown1.Selected.Value,  DateBorrowed: Today(), DatePlannedReturn:DatePicker1.SelectedDate, Status: \"Borrowing\", ItemBorrowed: varRecord2.ID, ItemBorrowedTitle: varRecord2.Title, Signature: varPenInputClean });\r\n'
    r"//The cancel button already had the logic to reset my variables so lets use it\r\n"
    r"Select(icnCancel);\r\n"
    r"Set(varShowSpinner, false)"
)
NEW_BORROW = (
    r"Set(varShowSpinner, true);\r\n"
    r"Patch('Asset Register', varRecord2, {Status: {Value: \"Checked Out\"}, CheckedOutDate: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\r\n"
    r'Patch(\'Asset Log\', Defaults(\'Asset Log\'), {Title: varRecord2.Title & \" – \" & Text(Now(), \"dd/mm/yyyy hh:mm\"), AssetID: {Id: varRecord2.ID, Value: varRecord2.Title}, Action: {Value: \"Check Out\"}, DateTime: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\r\n'
    r"Select(icnCancel);\r\n"
    r"Set(varShowSpinner, false)"
)
c11 = rep(c11, OLD_BORROW, NEW_BORROW, "borrow-patch")

# 3. Admin reset
c11 = rep(
    c11,
    r"RemoveIf('Asset Log', true);\r\nUpdateIf('Asset Register', true, {NumberOnLoan:0})",
    r'Notify(\"Admin reset disabled in this version.\", NotificationType.Warning)',
    "reset",
)

with open(f"{BASE}/11.json", "w", encoding="utf-8") as f:
    f.write(c11)
print("[11.json] Written.\n")


# ── Controls/34.json ────────────────────────────────────────────────────────
with open(f"{BASE}/34.json", "r", encoding="utf-8") as f:
    c34 = f.read()

print("=== 34.json ===")

# 1. Gallery filter (BorrowEmail branch partially replaced already)
c34 = rep(
    c34,
    r"If(Toggle1.Value, Filter('Asset Register', Status.Value = \"Checked Out\"), Filter('Asset Log', BorrowEmail = User().Email And Status = \"Borrowing\"))",
    r"Filter('Asset Register', Status.Value = \"Checked Out\")",
    "filter-toggle",
)

# 2. QTY Borrowed label
c34 = rep(
    c34,
    r'\"QTY Borrowed: \" & ThisItem.QTYBorrowed',
    r'\"Checked out: \" & Text(ThisItem.CheckedOutDate, \"dd/mm/yyyy\")',
    "qty-label",
)

# 3. Status label with DateActualReturn
c34 = rep(
    c34,
    r'\"Status: \" & ThisItem.Status & If(ThisItem.Status = \"Returned\", \" on \" & ThisItem.DateActualReturn)',
    r'\"Status: \" & ThisItem.Status.Value',
    "status-label",
)

# 4. Full return/check-in Patch (pretty-printed with \n)
OLD_RETURN = (
    "With(\\n"
    "    {\\n"
    "        SharedItemToPatch: LookUp(\\n"
    "            'Asset Register',\\n"
    "            ID = varRecord3.ItemBorrowed\\n"
    "        )\\n"
    "    },\\n"
    "    Patch(\\n"
    "        'Asset Register',\\n"
    "        SharedItemToPatch,\\n"
    "        {NumberOnLoan: SharedItemToPatch.NumberOnLoan - varRecord3.QTYBorrowed}\\n"
    "    )\\n"
    ");\\n"
    "Patch(\\n"
    "    'Asset Log',\\n"
    "    varRecord3,\\n"
    "    {\\n"
    '        Status: \\"Returned\\",\\n'
    "        DateActualReturn: Today()\\n"
    "    }\\n"
    ");\\n"
    "Set(\\n"
    "    varShowConfirm,\\n"
    "    false\\n"
    ");\\n"
)
NEW_RETURN = (
    "Patch('Asset Register', varRecord3, {Status: {Value: \\\"Available\\\"}, CurrentAssignedTo: Blank(), CheckedOutDate: Blank(), ExpectedReturnDate: Blank()});\\n"
    "Patch('Asset Log', Defaults('Asset Log'), {Title: varRecord3.Title & \\\" \\u2013 \\\" & Text(Now(), \\\"dd/mm/yyyy hh:mm\\\"), AssetID: {Id: varRecord3.ID, Value: varRecord3.Title}, Action: {Value: \\\"Check In\\\"}, DateTime: Now()});\\n"
    "Set(varShowConfirm, false);\\n"
    "Set(varRecord3, Blank())"
)
c34 = rep(c34, OLD_RETURN, NEW_RETURN, "return-patch")

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
