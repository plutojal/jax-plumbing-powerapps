# Asset App – Data Model Reference

**App:** JAX Asset Manager  
**SharePoint site:** `https://jaxplumbinggy.sharepoint.com/sites/JaxPlumbingCRMHub-Live`

---

## Asset Register
**URL:** `.../Lists/Asset Register/AllItems.aspx`  
**Internal table name (Power Apps connector):** `asset-register`  
**Purpose:** Master list of every company asset.

| Column | Type | Power Fx field | Notes |
|---|---|---|---|
| Title | Single line | `Title` | Asset ID e.g. JX100001 |
| AssetCategory | Choice | `AssetCategory.Value` | Office / Yard / Van / Engineer Owned |
| BarCode | Single line | `BarCode` | For future barcode scanning |
| ItemDescription | Single line | `ItemDescription` | What the asset is |
| Make | Single line | `Make` | Brand |
| Model | Single line | `Model` | Model number |
| SerialNumber | Single line | `SerialNumber` | Manufacturer serial |
| PowerType | Choice | `PowerType.Value` | 240V / 110V / Battery / N/A |
| Location | Single line | `Location` | Where it's stored |
| Status | Choice | `Status.Value` | Available / Checked Out / Under Repair / Retired |
| CurrentAssignedTo | Lookup → Staff | `CurrentAssignedTo` | `{Id: staffRecord.ID, Value: staffRecord.Title}` |
| CheckedOutDate | Date/Time | `CheckedOutDate` | Set on check-out, Blank() on return |
| ExpectedReturnDate | Date/Time | `ExpectedReturnDate` | Set on check-out, Blank() on return |
| RequiresPATTest | Yes/No | `RequiresPATTest` | |
| PATTestDue | Date/Time | `PATTestDue` | |
| TestFrequencyMonths | Number | `TestFrequencyMonths` | |
| RequiresCalibration | Yes/No | `RequiresCalibration` | |
| CalibrationDue | Yes/No | `CalibrationDue` | Flag only — not a date |
| Notes | Multi-line | `Notes` | General notes |
| PurchaseDate | Date/Time | `PurchaseDate` | |
| PurchaseValue | Currency | `PurchaseValue` | |
| WarrantyExpiry | Date/Time | `WarrantyExpiry` | |
| IsActive | Yes/No | `IsActive` | Soft delete — default true |

### Common Patch patterns

**Check out an asset:**
```
Patch('Asset Register', record, {
    Status: {Value: "Checked Out"},
    CurrentAssignedTo: {Id: staffRecord.ID, Value: staffRecord.Title},
    CheckedOutDate: Now(),
    ExpectedReturnDate: selectedReturnDate
})
```

**Return an asset:**
```
Patch('Asset Register', record, {
    Status: {Value: "Available"},
    CurrentAssignedTo: Blank(),
    CheckedOutDate: Blank(),
    ExpectedReturnDate: Blank()
})
```

**Filter available assets:**
```
Filter('Asset Register', Status.Value = "Available", IsActive = true)
```

**Filter checked-out assets:**
```
Filter('Asset Register', Status.Value = "Checked Out")
```

---

## Asset Log
**URL:** `.../Lists/Asset Log/AllItems.aspx`  
**Internal table name (Power Apps connector):** `asset-log`  
**Purpose:** Append-only audit trail — never delete rows.

| Column | Type | Power Fx field | Notes |
|---|---|---|---|
| Title | Single line | `Title` | Auto-label e.g. "JX100001 – 08/05/2026 14:30" |
| AssetID | Lookup → Asset Register | `AssetID` | `{Id: assetRecord.ID, Value: assetRecord.Title}` |
| Action | Choice | `Action.Value` | Check Out / Check In / Under Repair / Returned from Repair |
| StaffMember | Lookup → Staff | `StaffMember` | `{Id: staffRecord.ID, Value: staffRecord.Title}` |
| DateTime | Date/Time | `DateTime` | When action occurred (column name is `DateTime`, not `ActionDateTime`) |
| Notes | Single line | `Notes` | Reason, condition notes, job ref |
| ExpectedReturnDate | Date/Time | `ExpectedReturnDate` | Check-outs only |

### Common Patch patterns

**Log a check-out:**
```
Patch('Asset Log', Defaults('Asset Log'), {
    Title: assetRecord.Title & " - " & Text(Now(), "dd/mm/yyyy hh:mm"),
    AssetID: {Id: assetRecord.ID, Value: assetRecord.Title},
    Action: {Value: "Check Out"},
    DateTime: Now(),
    ExpectedReturnDate: selectedReturnDate
})
```

**Log a check-in:**
```
Patch('Asset Log', Defaults('Asset Log'), {
    Title: assetRecord.Title & " - " & Text(Now(), "dd/mm/yyyy hh:mm"),
    AssetID: {Id: assetRecord.ID, Value: assetRecord.Title},
    Action: {Value: "Check In"},
    DateTime: Now()
})
```

---

## Status values (Choice columns)

### Asset Register — Status
| Value | Meaning |
|---|---|
| `Available` | In stock, can be checked out |
| `Checked Out` | Currently with a staff member |
| `Under Repair` | Sent for repair |
| `Retired` | Decommissioned |

### Asset Log — Action
| Value | Meaning |
|---|---|
| `Check Out` | Asset taken by staff |
| `Check In` | Asset returned |
| `Under Repair` | Sent for repair |
| `Returned from Repair` | Back from repair |

---

## Relationships

```
Staff
  └── Asset Register  (CurrentAssignedTo → Staff)
        └── Asset Log  (AssetID → Asset Register,
                        StaffMember → Staff)
```

> **Note:** `CurrentAssignedTo` and `StaffMember` are **Lookup** columns (→ Staff),
> not Person or Group. Use `{Id: record.ID, Value: record.Title}` syntax in Patch,
> not the `'@odata.type'` Person syntax.
