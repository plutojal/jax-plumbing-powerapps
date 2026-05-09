# Jax Plumbing – Power Apps Repo

## Repo Purpose
This repo stores Power Apps canvas apps for Jax Plumbing as editable source (YAML/JSON),
with pre-built import zips ready to upload to Power Apps.

## Repo Structure
```
apps/
  appointment-app/
    src/          ← editable YAML/JSON source – edit these
    export/       ← original export package metadata
    build/        ← AppointmentApp_import.zip (ready to import)
  asset-app/
    src/          ← editable Controls/ JSON + References/ source
    export/       ← original Shane Young export (source of truth for .msapp base)
    build/        ← AssetApp_import.zip (ready to import)
    build_asset_app.py  ← Python build script (see below)
docs/
  sharepoint-schema.md  ← full column schema for all SharePoint lists
  asset-model.md        ← Asset Register + Asset Log column reference + Power Fx patterns
.github/
  workflows/
    build-powerapps.yml  ← auto-rebuilds both app zips when src/ changes on main
```

## How to Import to Power Apps
1. Download the zip from `apps/<app>/build/`
2. Go to make.powerapps.com → Apps → Import package → upload zip
3. Set import action to **Create as new** (avoids overwriting live app)

## SharePoint Environment
- **Site:** `https://jaxplumbinggy.sharepoint.com/sites/JaxPlumbingCRMHub-Live`
- **Tenant:** jaxplumbinggy
- **SharePoint connection ID:** `4144a835cec941aba09a9f666e33d99a` (data@jaxplumbing.co.uk)

---

## Asset App (JAX Asset Manager)

### Overview
Originally Shane Young's "Check out" demo app (2021), re-wired to JAX's SharePoint lists.
The app has two screens: browse/check-out (Controls/11.json) and my-items/return (Controls/34.json).

### SharePoint Lists
| List | GUID | Power Fx name |
|---|---|---|
| Asset Register | `a87e1127-225f-4577-94d3-e8b1e3fcb448` | `'Asset Register'` |
| Asset Log | `e8ea6875-63fd-44ba-a636-2a32e2e9cbfa` | `'Asset Log'` |

List Settings URLs:
- Asset Register: `https://jaxplumbinggy.sharepoint.com/sites/JaxPlumbingCRMHub-Live/_layouts/15/listedit.aspx?List=%7Ba87e1127-225f-4577-94d3-e8b1e3fcb448%7D`
- Asset Log: `https://jaxplumbinggy.sharepoint.com/sites/JaxPlumbingCRMHub-Live/_layouts/15/listedit.aspx?List=%7Be8ea6875-63fd-44ba-a636-2a32e2e9cbfa%7D`

### Key Technical Facts
- **Column types:** `Status` and `Action` are plain **Text** in the SharePoint connector (not Choice).
  Use `Status = "Checked Out"` not `Status.Value`. Use `Status: "Checked Out"` not `Status: {Value: "Checked Out"}`.
- **AssetID** in Asset Log is plain **Text** (single line), not a Lookup. Use `AssetID: varRecord.Title`.
- **CurrentAssignedTo** column does not exist or has a different internal name — do not use in Patch.
- **Header.json** must stay at `DocVersion: "1.309" / MSAppStructureVersion: "2.0"` (2021 Controls only compatible with this version).
- **checksum.json** must NOT be in src/ — the proprietary Microsoft algorithm cannot be recalculated after any edit.

### Build Script
`apps/asset-app/build_asset_app.py` — use this for all builds, never `zip -r src/`:
- Patches original `.msapp` entry-by-entry (preserves binary format)
- Skips `checksum.json` (always stale)
- Validates all JSON before writing output
- Produces correct `Microsoft.PowerApps/apps/{id}/` import package structure

```bash
python3 apps/asset-app/build_asset_app.py
```

### Connection Configuration
`src/Properties.json` → `LocalConnectionReferences` is wired to:
- Connection ID: `4144a835cec941aba09a9f666e33d99a` (data@jaxplumbing.co.uk SharePoint)
- dataSources: `["Asset Register", "Asset Log"]`
- datasets: both list GUIDs mapped under the JAX site URL

`src/References/DataSources.json` uses real SharePoint GUIDs as `TableName` (not slugs).

### Current Known Issue — Data Source "Not Connected"
After importing `AssetApp_import.zip`, `Asset Register` and `Asset Log` show as **"Not connected"**
even though the connection ID and GUIDs are correct in `Properties.json` and `DataSources.json`.
Manually adding them in Studio works (they connect as `Asset Register_1` / `Asset Log_1`).

**Suspected cause:** Our hand-crafted `DataSources.json` is missing fields that Power Apps generates
from a live connection (e.g. `CdpRevision` block, full internal field name mappings in
`ConnectedDataSourceInfoNameMapping`). The appointment app's DataSources.json has `CdpRevision`
on every entry; ours does not.

**Next step to fix:** 
1. In Studio (with Asset Register_1 / Asset Log_1 connected), save the app (Ctrl+S)
2. File → Save as → This computer → Download (gets a `.msapp` file)
3. Rename to `.zip`, open it, extract `References/DataSources.json` and `Properties.json`
4. Replace `apps/asset-app/src/References/DataSources.json` and `src/Properties.json` with those files
5. Rebuild: `python3 apps/asset-app/build_asset_app.py`
6. Commit and push — future imports will auto-connect

### Formula Patterns (Controls/11.json and Controls/34.json)
```
// Check-out (Controls/11.json)
Patch('Asset Register', varRecord2, {Status: "Checked Out", CheckedOutDate: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});
Patch('Asset Log', Defaults('Asset Log'), {Title: varRecord2.Title & " - " & Text(Now(), "dd/mm/yyyy hh:mm"), AssetID: varRecord2.Title, Action: "Check Out", DateTime: Now(), ExpectedReturnDate: DatePicker1.SelectedDate});

// Check-in (Controls/34.json)
Patch('Asset Register', varRecord3, {Status: "Available", CheckedOutDate: Blank(), ExpectedReturnDate: Blank()});
Patch('Asset Log', Defaults('Asset Log'), {Title: varRecord3.Title & " - " & Text(Now(), "dd/mm/yyyy hh:mm"), AssetID: varRecord3.Title, Action: "Check In", DateTime: Now()});

// Gallery filter
Filter('Asset Register', Status = "Checked Out")
```

---

## Appointment App

### Lists Used
| List | Purpose |
|---|---|
| Customers | Customer CRM records |
| Job Addresses | ~4,252 property/site addresses |
| Appliances | ~4,471 appliances at job addresses |
| Appointments | ~3,458 appointment/activity log |
| Jobs | Job records |
| Job Scheduling | Scheduling entries (ProjectSchedulerScreen) |

### Key List Relationships
```
Customers
  └── Job Addresses (Customer → Customers)
        └── Appliances (Customer → Customers, Job Address → Job Addresses)
              └── Appointments (Customer, Job Address, Appliances, Job lookups)
Jobs (Customer → Customers, Job Address → Job Addresses)
```

---

## General Notes
- Some SharePoint columns have internal names that differ from display names.
  Internal names matter in Power Automate flows and REST API calls.
  See `docs/sharepoint-schema.md` for full column details.
- Appointment app uses connectors: SharePoint Online, Office 365 Outlook, Office 365 Users
- Asset app uses connector: SharePoint Online only
- Always develop on `main` branch
- Git push via local proxy may fail with 403 — use `git push https://plutojal:<PAT>@github.com/plutojal/jax-plumbing-powerapps.git main` with the PAT the user provides
