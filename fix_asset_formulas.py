#!/usr/bin/env python3
"""
Fix asset app: update DataSources + all formula references in Controls.
Uses regex to find and replace InvariantScript values by their exact content.
"""
import re, json, os, zipfile

BASE = "/home/user/jax-plumbing-powerapps/apps/asset-app/src"

# ── Helper ──────────────────────────────────────────────────────────────────

def replace_invariant(content, old_value, new_value, label):
    """Replace an exact InvariantScript value."""
    # Escape for use as literal search string in re
    marker = '"InvariantScript":"' + old_value + '","RuleProviderType"'
    replacement = '"InvariantScript":"' + new_value + '","RuleProviderType"'
    count = content.count(marker)
    if count:
        print(f"  [{label}] {count}x replaced")
        return content.replace(marker, replacement)
    print(f"  [{label}] NOT FOUND")
    return content

# ── 1. DataSources.json ─────────────────────────────────────────────────────
print("=== DataSources.json ===")

with open(f"{BASE}/References/DataSources.json") as f:
    raw_ds = f.read()

# Replace list names and table references
raw_ds = raw_ds.replace('"Shared Equipment"', '"Asset Register"')
raw_ds = raw_ds.replace('"Equipment List Log"', '"Asset Log"')
raw_ds = raw_ds.replace('"shared-equipment"', '"asset-register"')
raw_ds = raw_ds.replace('"equipment-list-log"', '"asset-log"')
raw_ds = raw_ds.replace('shanescows.sharepoint.com/sites/pa', 'jaxplumbinggy.sharepoint.com/sites/JaxPlumbingCRMHub-Live')

with open(f"{BASE}/References/DataSources.json", "w") as f:
    f.write(raw_ds)
print("  DataSources.json updated")

# ── 2. Controls/11.json ─────────────────────────────────────────────────────
print("\n=== Controls/11.json ===")

with open(f"{BASE}/Controls/11.json", "r") as f:
    c11 = f.read()

# 2a. List-name-only label (e.g. used in a text label showing list name)
c11 = replace_invariant(c11,
    "'Shared Equipment'",
    "'Asset Register'",
    "list-name-label")

# 2b. Availability visible check
c11 = replace_invariant(c11,
    "ThisItem.NumberOfUnits - ThisItem.NumberOnLoan > 0",
    'ThisItem.Status.Value = "Available"',
    "avail-visible")

# 2c. Availability label text
c11 = replace_invariant(c11,
    r'ThisItem.NumberOfUnits - ThisItem.NumberOnLoan & \" of \" & ThisItem.NumberOfUnits & \" are available to borrow\"',
    r'"Status: " & ThisItem.Status.Value',
    "avail-label")

# 2d. Sequence for qty dropdown
c11 = replace_invariant(c11,
    "Sequence(varRecord2.NumberOfUnits -varRecord2.NumberOnLoan)",
    "[1]",
    "sequence")

# 2e. Full borrow / check-out Patch
OLD_BORROW = (
    r"Set(varShowSpinner, true);\r\n"
    r"//Update the count in the SharePoint list for tracking inventory\r\n"
    r"Patch('Shared Equipment', varRecord2, {NumberOnLoan: varRecord2.NumberOnLoan + Dropdown1.Selected.Value});\r\n"
    r"//Turn the pen input into a base64 string\r\n"
    r"Set(varPenInput, JSON(PenInput1.Image,JSONFormat.IncludeBinaryData));\r\n"
    r"Set(varPenInputClean, Mid(varPenInput, 2, Len(varPenInput)-2));\r\n"
    r"//Update the list of who has borrowed what including a copy of their signature\r\n"
    r"Patch('Equipment List Log', Defaults('Equipment List Log'), {Title: User().FullName, BorrowEmail: User().Email, QTYBorrowed: Dropdown1.Selected.Value,  DateBorrowed: Today(), DatePlannedReturn:DatePicker1.SelectedDate, Status: \"Borrowing\", ItemBorrowed: varRecord2.ID, ItemBorrowedTitle: varRecord2.Title, Signature: varPenInputClean });\r\n"
    r"//The cancel button already had the logic to reset my variables so lets use it\r\n"
    r"Select(icnCancel);\r\n"
    r"Set(varShowSpinner, false)"
)
NEW_BORROW = (
    r"Set(varShowSpinner, true);\r\n"
    r"Patch('Asset Register', varRecord2, {Status: {Value: \"Checked Out\"}, CheckedOutDate: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\r\n"
    r"Patch('Asset Log', Defaults('Asset Log'), {Title: varRecord2.Title & \" - \" & Text(Now(), \"dd/mm/yyyy hh:mm\"), AssetID: {Id: varRecord2.ID, Value: varRecord2.Title}, Action: {Value: \"Check Out\"}, DateTime: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});\r\n"
    r"Select(icnCancel);\r\n"
    r"Set(varShowSpinner, false)"
)
c11 = replace_invariant(c11, OLD_BORROW, NEW_BORROW, "borrow-patch")

# 2f. Admin reset → warning
c11 = replace_invariant(c11,
    r"RemoveIf('Equipment List Log', true);\r\nUpdateIf('Shared Equipment', true, {NumberOnLoan:0})",
    r"Notify(\"Admin reset disabled in this version.\", NotificationType.Warning)",
    "reset")

with open(f"{BASE}/Controls/11.json", "w") as f:
    f.write(c11)
print("  Controls/11.json written")

# ── 3. Controls/34.json ─────────────────────────────────────────────────────
print("\n=== Controls/34.json ===")

with open(f"{BASE}/Controls/34.json", "r") as f:
    c34 = f.read()

# 3a. Gallery filter
c34 = replace_invariant(c34,
    r"If(Toggle1.Value, Filter('Equipment List Log', BorrowEmail = User().Email), Filter('Equipment List Log', BorrowEmail = User().Email And Status = \"Borrowing\"))",
    r"Filter('Asset Register', Status.Value = \"Checked Out\")",
    "filter")

# 3b. Item title
c34 = replace_invariant(c34,
    "ThisItem.ItemBorrowedTitle",
    "ThisItem.ItemDescription",
    "item-title")

# 3c. QTY label
c34 = replace_invariant(c34,
    r"\"QTY Borrowed: \" & ThisItem.QTYBorrowed",
    r"\"Checked out: \" & Text(ThisItem.CheckedOutDate, \"dd/mm/yyyy\")",
    "qty-label")

# 3d. Planned return date
c34 = replace_invariant(c34,
    "ThisItem.DatePlannedReturn",
    "ThisItem.ExpectedReturnDate",
    "planned-return")

# 3e. Status label
c34 = replace_invariant(c34,
    r"\"Status: \" & ThisItem.Status & If(ThisItem.Status = \"Returned\", \" on \" & ThisItem.DateActualReturn)",
    r"\"Status: \" & ThisItem.Status.Value",
    "status-label")

# 3f. Confirm message
c34 = replace_invariant(c34,
    r"\"Are you sure you have returned \" & varRecord3.ItemBorrowedTitle & \"?\"",
    r"\"Are you sure you have returned \" & varRecord3.ItemDescription & \"?\"",
    "confirm-msg")

# 3g. Full return / check-in Patch
OLD_RETURN = (
    "With(\\n"
    "    {\\n"
    "        SharedItemToPatch: LookUp(\\n"
    "            'Shared Equipment',\\n"
    "            ID = varRecord3.ItemBorrowed\\n"
    "        )\\n"
    "    },\\n"
    "    Patch(\\n"
    "        'Shared Equipment',\\n"
    "        SharedItemToPatch,\\n"
    "        {NumberOnLoan: SharedItemToPatch.NumberOnLoan - varRecord3.QTYBorrowed}\\n"
    "    )\\n"
    ");\\n"
    "Patch(\\n"
    "    'Equipment List Log',\\n"
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
    "Patch('Asset Log', Defaults('Asset Log'), {Title: varRecord3.Title & \\\" - \\\" & Text(Now(), \\\"dd/mm/yyyy hh:mm\\\"), AssetID: {Id: varRecord3.ID, Value: varRecord3.Title}, Action: {Value: \\\"Check In\\\"}, DateTime: Now()});\\n"
    "Set(varShowConfirm, false);\\n"
    "Set(varRecord3, Blank())"
)
c34 = replace_invariant(c34, OLD_RETURN, NEW_RETURN, "return-patch")

with open(f"{BASE}/Controls/34.json", "w") as f:
    f.write(c34)
print("  Controls/34.json written")

# ── Sanity check ────────────────────────────────────────────────────────────
print("\n=== Sanity Check ===")
with open(f"{BASE}/Controls/11.json") as f:
    c11 = f.read()
with open(f"{BASE}/Controls/34.json") as f:
    c34 = f.read()

BAD = ["Shared Equipment", "Equipment List Log", "BorrowEmail", "NumberOnLoan",
       "NumberOfUnits", "QTYBorrowed", "ItemBorrowedTitle", "DatePlannedReturn",
       "DateActualReturn", "ItemBorrowed:"]

for name, content in [("11.json", c11), ("34.json", c34)]:
    bad_found = False
    for bad in BAD:
        # Only flag if in an active InvariantScript (not AutoRuleBindingString)
        idx = content.find(bad)
        while idx != -1:
            seg = content[max(0,idx-150):idx+10]
            if "InvariantScript" in seg and "AutoRuleBinding" not in seg:
                print(f"  WARNING [{name}]: '{bad}' still in active formula")
                bad_found = True
            idx = content.find(bad, idx+1)
    if not bad_found:
        print(f"  [{name}] OK")
