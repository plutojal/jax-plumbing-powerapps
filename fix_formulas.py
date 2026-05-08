#!/usr/bin/env python3
"""Fix old Shane Young formula references in Controls/11.json and Controls/34.json."""
import json
import re

BASE = "/home/user/jax-plumbing-powerapps/apps/asset-app/src/Controls"

# ── Controls/11.json ────────────────────────────────────────────────────────

with open(f"{BASE}/11.json", "r", encoding="utf-8") as f:
    raw11 = f.read()

replacements_11 = [
    # Availability check → Status.Value
    (
        "ThisItem.NumberOfUnits - ThisItem.NumberOnLoan > 0",
        'ThisItem.Status.Value = "Available"',
    ),
    # Availability label
    (
        'ThisItem.NumberOfUnits - ThisItem.NumberOnLoan & " of " & ThisItem.NumberOfUnits & " are available to borrow"',
        '"Status: " & ThisItem.Status.Value',
    ),
    # Sequence for quantity dropdown
    (
        "Sequence(varRecord2.NumberOfUnits -varRecord2.NumberOnLoan)",
        "[1]",
    ),
    # Borrow / Check-out Patch — full replacement (JSON-escaped newlines)
    (
        "Set(varShowSpinner, true);\\nPatch('Shared Equipment', varRecord2, {NumberOnLoan: varRecord2.NumberOnLoan + Dropdown1.Selected.Value});\\nSet(varPenInput, JSON(PenInput1.Image,JSONFormat.IncludeBinaryData));\\nSet(varPenInputClean, Mid(varPenInput, 2, Len(varPenInput)-2));\\nPatch('Equipment List Log', Defaults('Equipment List Log'), {Title: User().FullName, BorrowEmail: User().Email, QTYBorrowed: Dropdown1.Selected.Value, DateBorrowed: Today(), DatePlannedReturn:DatePicker1.SelectedDate, Status: \"Borrowing\", ItemBorrowed: varRecord2.ID, ItemBorrowedTitle: varRecord2.Title, Signature: varPenInputClean });\\nSelect(icnCancel);\\nSet(varShowSpinner, false)",
        "Set(varShowSpinner, true);\\nPatch('Asset Register', varRecord2, {Status: {Value: \\\"Checked Out\\\"}, CheckedOutDate: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\\nPatch('Asset Log', Defaults('Asset Log'), {Title: varRecord2.Title & \\\" \\u2013 \\\" & Text(Now(), \\\"dd/mm/yyyy hh:mm\\\"), AssetID: {Id: varRecord2.ID, Value: varRecord2.Title}, Action: {Value: \\\"Check Out\\\"}, DateTime: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\\nSelect(icnCancel);\\nSet(varShowSpinner, false)",
    ),
    # Admin reset → warning
    (
        "RemoveIf('Equipment List Log', true);\\nUpdateIf('Shared Equipment', true, {NumberOnLoan:0})",
        'Notify("Admin reset disabled in this version.", NotificationType.Warning)',
    ),
    # List name fallback (catch-all for any remaining references)
    ("'Shared Equipment'", "'Asset Register'"),
    ("'Equipment List Log'", "'Asset Log'"),
]

out11 = raw11
for old, new in replacements_11:
    count = out11.count(old)
    if count:
        print(f"[11.json] Replacing ({count}x): {old[:60]!r}")
        out11 = out11.replace(old, new)
    else:
        print(f"[11.json] NOT FOUND (skipped): {old[:60]!r}")

with open(f"{BASE}/11.json", "w", encoding="utf-8") as f:
    f.write(out11)
print("[11.json] Written.\n")


# ── Controls/34.json ────────────────────────────────────────────────────────

with open(f"{BASE}/34.json", "r", encoding="utf-8") as f:
    raw34 = f.read()

replacements_34 = [
    # Gallery filter — with-toggle variant
    (
        "If(Toggle1.Value, Filter('Equipment List Log', BorrowEmail = User().Email), Filter('Equipment List Log', BorrowEmail = User().Email And Status = \"Borrowing\"))",
        "Filter('Asset Register', Status.Value = \"Checked Out\")",
    ),
    # Gallery filter — simpler variant (in case it appears without the If)
    (
        "Filter('Equipment List Log', BorrowEmail = User().Email And Status = \"Borrowing\")",
        "Filter('Asset Register', Status.Value = \"Checked Out\")",
    ),
    (
        "Filter('Equipment List Log', BorrowEmail = User().Email)",
        "Filter('Asset Register', Status.Value = \"Checked Out\")",
    ),
    # Column name fixes
    ("ThisItem.ItemBorrowedTitle", "ThisItem.ItemDescription"),
    ("varRecord3.ItemBorrowedTitle", "varRecord3.ItemDescription"),
    (
        "ThisItem.Status = \"Borrowing\"",
        'ThisItem.Status.Value = "Checked Out"',
    ),
    (
        '"QTY Borrowed: " & ThisItem.QTYBorrowed',
        '"Checked out: " & Text(ThisItem.CheckedOutDate, "dd/mm/yyyy")',
    ),
    ("ThisItem.DatePlannedReturn", "ThisItem.ExpectedReturnDate"),
    (
        'varRecord3.DatePlannedReturn',
        'varRecord3.ExpectedReturnDate',
    ),
    (
        '"Status: " & ThisItem.Status & If(ThisItem.Status = "Returned", " on " & ThisItem.DateActualReturn)',
        '"Status: " & ThisItem.Status.Value',
    ),
    # Return / Check-in Patch — full replacement
    (
        "With({SharedItemToPatch: LookUp('Shared Equipment', ID = varRecord3.ItemBorrowed)}, Patch('Shared Equipment', SharedItemToPatch, {NumberOnLoan: SharedItemToPatch.NumberOnLoan - varRecord3.QTYBorrowed}));\\nPatch('Equipment List Log', varRecord3, {Status: \"Returned\", DateActualReturn: Today()});\\nSet(varShowConfirm, false);",
        "Patch('Asset Register', varRecord3, {Status: {Value: \\\"Available\\\"}, CurrentAssignedTo: Blank(), CheckedOutDate: Blank(), ExpectedReturnDate: Blank()});\\nPatch('Asset Log', Defaults('Asset Log'), {Title: varRecord3.Title & \\\" \\u2013 \\\" & Text(Now(), \\\"dd/mm/yyyy hh:mm\\\"), AssetID: {Id: varRecord3.ID, Value: varRecord3.Title}, Action: {Value: \\\"Check In\\\"}, DateTime: Now()});\\nSet(varShowConfirm, false);\\nSet(varRecord3, Blank())",
    ),
    # List name fallback
    ("'Shared Equipment'", "'Asset Register'"),
    ("'Equipment List Log'", "'Asset Log'"),
]

out34 = raw34
for old, new in replacements_34:
    count = out34.count(old)
    if count:
        print(f"[34.json] Replacing ({count}x): {old[:60]!r}")
        out34 = out34.replace(old, new)
    else:
        print(f"[34.json] NOT FOUND (skipped): {old[:60]!r}")

with open(f"{BASE}/34.json", "w", encoding="utf-8") as f:
    f.write(out34)
print("[34.json] Written.")

# ── Sanity check ────────────────────────────────────────────────────────────
for name, content in [("11.json", out11), ("34.json", out34)]:
    for bad in ["Shared Equipment", "Equipment List Log", "BorrowEmail",
                "NumberOnLoan", "NumberOfUnits", "QTYBorrowed",
                "ItemBorrowedTitle", "DatePlannedReturn", "DateActualReturn",
                "ItemBorrowed:", "NumberOnLoan"]:
        if bad in content:
            print(f"WARNING [{name}]: still contains '{bad}'")
