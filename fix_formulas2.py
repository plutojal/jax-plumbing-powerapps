#!/usr/bin/env python3
"""Fix remaining old Shane Young formula references — exact strings from file inspection."""

BASE = "/home/user/jax-plumbing-powerapps/apps/asset-app/src/Controls"

# ── Controls/11.json ────────────────────────────────────────────────────────
with open(f"{BASE}/11.json", "r", encoding="utf-8") as f:
    c11 = f.read()

# 1. Availability label
OLD_AVAIL_LABEL = (
    r'ThisItem.NumberOfUnits - ThisItem.NumberOnLoan & \" of \" & ThisItem.NumberOfUnits & \" are available to borrow\"'
)
NEW_AVAIL_LABEL = '"Status: " & ThisItem.Status.Value'
c11 = c11.replace(OLD_AVAIL_LABEL, NEW_AVAIL_LABEL)

# 2. Borrow (check-out) Patch — full formula with \r\n line endings
OLD_BORROW = (
    "Set(varShowSpinner, true);\\r\\n"
    "//Update the count in the SharePoint list for tracking inventory\\r\\n"
    "Patch(\\'Asset Register\\', varRecord2, {NumberOnLoan: varRecord2.NumberOnLoan + Dropdown1.Selected.Value});\\r\\n"
    "//Turn the pen input into a base64 string\\r\\n"
    "Set(varPenInput, JSON(PenInput1.Image,JSONFormat.IncludeBinaryData));\\r\\n"
    "Set(varPenInputClean, Mid(varPenInput, 2, Len(varPenInput)-2));\\r\\n"
    "//Update the list of who has borrowed what including a copy of their signature\\r\\n"
    "Patch(\\'Asset Log\\', Defaults(\\'Asset Log\\'), {Title: User().FullName, BorrowEmail: User().Email, QTYBorrowed: Dropdown1.Selected.Value,  DateBorrowed: Today(), DatePlannedReturn:DatePicker1.SelectedDate, Status: \\\"Borrowing\\\", ItemBorrowed: varRecord2.ID, ItemBorrowedTitle: varRecord2.Title, Signature: varPenInputClean });\\r\\n"
    "//The cancel button already had the logic to reset my variables so lets use it\\r\\n"
    "Select(icnCancel);\\r\\n"
    "Set(varShowSpinner, false)"
)
NEW_BORROW = (
    "Set(varShowSpinner, true);\\r\\n"
    "Patch(\\'Asset Register\\', varRecord2, {Status: {Value: \\\"Checked Out\\\"}, CheckedOutDate: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\\r\\n"
    "Patch(\\'Asset Log\\', Defaults(\\'Asset Log\\'), {Title: varRecord2.Title & \\\" \\u2013 \\\" & Text(Now(), \\\"dd/mm/yyyy hh:mm\\\"), AssetID: {Id: varRecord2.ID, Value: varRecord2.Title}, Action: {Value: \\\"Check Out\\\"}, DateTime: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\\r\\n"
    "Select(icnCancel);\\r\\n"
    "Set(varShowSpinner, false)"
)
c11 = c11.replace(OLD_BORROW, NEW_BORROW)

# 3. Admin reset formula
OLD_RESET = "RemoveIf(\\'Asset Log\\', true);\\r\\nUpdateIf(\\'Asset Register\\', true, {NumberOnLoan:0})"
NEW_RESET = "Notify(\\\"Admin reset disabled in this version.\\\", NotificationType.Warning)"
c11 = c11.replace(OLD_RESET, NEW_RESET)

with open(f"{BASE}/11.json", "w", encoding="utf-8") as f:
    f.write(c11)
print("[11.json] Written.")


# ── Controls/34.json ────────────────────────────────────────────────────────
with open(f"{BASE}/34.json", "r", encoding="utf-8") as f:
    c34 = f.read()

# 1. Gallery filter — partial replacement (BorrowEmail branch already partially replaced)
OLD_FILTER = (
    "If(Toggle1.Value, Filter(\\'Asset Register\\', Status.Value = \\\"Checked Out\\\"), "
    "Filter(\\'Asset Log\\', BorrowEmail = User().Email And Status = \\\"Borrowing\\\"))"
)
NEW_FILTER = "Filter(\\'Asset Register\\', Status.Value = \\\"Checked Out\\\")"
c34 = c34.replace(OLD_FILTER, NEW_FILTER)

# 2. QTY Borrowed label
OLD_QTY = '\\\"QTY Borrowed: \\\" & ThisItem.QTYBorrowed'
NEW_QTY = '\\\"Checked out: \\\" & Text(ThisItem.CheckedOutDate, \\\"dd/mm/yyyy\\\")'
c34 = c34.replace(OLD_QTY, NEW_QTY)

# 3. Status label with DateActualReturn
OLD_STATUS = '\\\"Status: \\\" & ThisItem.Status & If(ThisItem.Status = \\\"Returned\\\", \\\" on \\\" & ThisItem.DateActualReturn)'
NEW_STATUS = '\\\"Status: \\\" & ThisItem.Status.Value'
c34 = c34.replace(OLD_STATUS, NEW_STATUS)

# 4. Return (check-in) Patch — full formula with \n line endings (pretty-printed)
OLD_RETURN = (
    "With(\\n"
    "    {\\n"
    "        SharedItemToPatch: LookUp(\\n"
    "            \\'Asset Register\\',\\n"
    "            ID = varRecord3.ItemBorrowed\\n"
    "        )\\n"
    "    },\\n"
    "    Patch(\\n"
    "        \\'Asset Register\\',\\n"
    "        SharedItemToPatch,\\n"
    "        {NumberOnLoan: SharedItemToPatch.NumberOnLoan - varRecord3.QTYBorrowed}\\n"
    "    )\\n"
    ");\\n"
    "Patch(\\n"
    "    \\'Asset Log\\',\\n"
    "    varRecord3,\\n"
    "    {\\n"
    "        Status: \\\"Returned\\\",\\n"
    "        DateActualReturn: Today()\\n"
    "    }\\n"
    ");\\n"
    "Set(\\n"
    "    varShowConfirm,\\n"
    "    false\\n"
    ");\\n"
)
NEW_RETURN = (
    "Patch(\\'Asset Register\\', varRecord3, {Status: {Value: \\\"Available\\\"}, CurrentAssignedTo: Blank(), CheckedOutDate: Blank(), ExpectedReturnDate: Blank()});\\n"
    "Patch(\\'Asset Log\\', Defaults(\\'Asset Log\\'), {Title: varRecord3.Title & \\\" \\u2013 \\\" & Text(Now(), \\\"dd/mm/yyyy hh:mm\\\"), AssetID: {Id: varRecord3.ID, Value: varRecord3.Title}, Action: {Value: \\\"Check In\\\"}, DateTime: Now()});\\n"
    "Set(varShowConfirm, false);\\n"
    "Set(varRecord3, Blank())"
)
c34 = c34.replace(OLD_RETURN, NEW_RETURN)

with open(f"{BASE}/34.json", "w", encoding="utf-8") as f:
    f.write(c34)
print("[34.json] Written.")


# ── Sanity check ────────────────────────────────────────────────────────────
for name, content in [("11.json", c11), ("34.json", c34)]:
    bad_found = False
    for bad in ["Shared Equipment", "Equipment List Log", "BorrowEmail",
                "NumberOnLoan", "NumberOfUnits", "QTYBorrowed",
                "ItemBorrowedTitle", "DatePlannedReturn", "DateActualReturn",
                "ItemBorrowed:" ]:
        if bad in content:
            print(f"WARNING [{name}]: still contains '{bad}'")
            bad_found = True
    if not bad_found:
        print(f"[{name}] OK — no old references found.")
