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
    src/          ← original Controls/ JSON source (2021, no YAML yet)
    export/       ← original export package metadata
    build/        ← AssetApp_original_import.zip (original Shane Young version)
docs/
  sharepoint-schema.md  ← full column schema for all SharePoint lists
.github/
  workflows/
    build-powerapps.yml  ← auto-rebuilds appointment-app zip when src/ changes on main
```

## How to Import to Power Apps
1. Download `apps/appointment-app/build/AppointmentApp_import.zip`
2. Go to make.powerapps.com → Apps → Import package → upload zip
3. Set import action to **Create as new** (avoids overwriting live app)

## SharePoint Environment
- **Site:** `https://jaxplumbinggy.sharepoint.com/sites/JaxPlumbingCRMHub-Live`
- **Tenant:** jaxplumbinggy

## Lists Used by the Appointment App
| List | Items | Purpose |
|---|---|---|
| Customers | ~n/a | Customer CRM records |
| Job Addresses | ~4,252 | Property/site addresses linked to customers |
| Appliances | ~4,471 | Appliances at job addresses |
| Appointments | ~3,458 | Appointment/activity log |
| Jobs | — | Job records linked to customers and addresses |
| Job Scheduling | — | Scheduling entries (used in ProjectSchedulerScreen) |

## Key List Relationships
```
Customers
  └── Job Addresses (Customer → Customers)
        └── Appliances (Customer → Customers, Job Address → Job Addresses)
              └── Appointments (Customer, Job Address, Appliances, Job lookups)
Jobs (Customer → Customers, Job Address → Job Addresses)
```

## Other SharePoint Lists (not yet in app)
Staff, Qualification Types, Qualification Records, Vehicles — schemas documented in `docs/sharepoint-schema.md`
Planner: Servicing, Breakdown, Quotes, Quoted Works, General Jobs, Projects, Asset Register — schemas not yet captured

## Notes
- Some SharePoint columns have internal names that differ from display names
  (e.g. a column called "Notes" might have internal name `field_1`).
  Internal names matter in Power Automate flows and REST API calls.
  See `docs/sharepoint-schema.md` for full column details.
- App uses connectors: SharePoint Online, Office 365 Outlook, Office 365 Users
- Branch: always develop on `main`
