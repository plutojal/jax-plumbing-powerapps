# SharePoint Schema – Jax Plumbing CRM Hub

**Site:** `https://jaxplumbinggy.sharepoint.com/sites/JaxPlumbingCRMHub-Live`

> **Internal column names:** SharePoint display names (shown here) may differ from internal
> column names used in Power Automate flows and REST API calls (e.g. a column called
> "Notes" may have an internal name like `field_1`). If a flow or API call behaves
> unexpectedly, verify the internal name via List Settings → click the column → check the URL.

---

## Customers
**URL:** `.../Lists/Customer/AllItems.aspx`

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | Auto-generated or used as reference |
| Status | Choice | e.g. Active, Do not contact, etc. |
| Full Name | Single line of text | Combined name |
| Honorific | Single line of text | e.g. Mr, Mrs |
| Honorific Title | Choice | Choice version of honorific |
| First Name | Single line of text | |
| Last Name | Single line of text | |
| Company Name | Single line of text | |
| Full Address | Single line of text | Combined address string |
| Building/House Number | Single line of text | |
| Street Address | Single line of text | |
| Town/City | Single line of text | |
| Region/County | Single line of text | |
| Postcode | Single line of text | |
| Landline | Single line of text | |
| Mobile | Single line of text | |
| Email | Single line of text | Primary email |
| 2nd Email | Single line of text | |
| Notes | Multiple lines of text | |
| Reminders Enabled | Yes/No | |
| SMS Reminders Enabled | Yes/No | |
| Email Reminders Enabled | Yes/No | |
| SMS Marketing Enabled | Yes/No | |
| Email Marketing Enabled | Yes/No | |
| SMS Transactional Enabled | Yes/No | |
| Email Transactional Enabled | Yes/No | |
| SMS Servicing Enabled | Yes/No | |
| Email Servicing Enabled | Yes/No | |
| On Stop | Yes/No | Flags account as on stop |
| Archive | Yes/No | |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Job Addresses
**URL:** `.../Lists/Job Addresses/AllItems.aspx`
**Size:** ~4,252 items (approaching 5,000 list view threshold)

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | |
| Status | Choice | |
| Full Address | Single line of text | |
| Building/House Number | Single line of text | |
| Street Address | Single line of text | |
| Town/City | Single line of text | |
| Region/County | Single line of text | |
| Postcode | Single line of text | |
| Email | Single line of text | Contact email for this address |
| Access Notes | Multiple lines of text | Site access instructions |
| Install Name | Single line of text | Name of person at install |
| Install Phone | Single line of text | Phone at install location |
| Service Due | Date and Time | Next service date |
| Scheduling Notes | Multiple lines of text | |
| Customer | Lookup | → Customers |
| Priority | Choice | |
| SMS Reminders Enabled | Yes/No | |
| Email Reminders Enabled | Yes/No | |
| SMS Marketing Enabled | Yes/No | |
| Email Marketing Enabled | Yes/No | |
| SMS Transactional Enabled | Yes/No | |
| Email Transactional Enabled | Yes/No | |
| SMS Servicing Enabled | Yes/No | |
| Email Servicing Enabled | Yes/No | |
| ID Val | Number | Custom numeric ID |
| Archive | Yes/No | |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Appliances
**URL:** `.../Lists/Appliances/AllItems.aspx`
**Size:** ~4,471 items (approaching 5,000 list view threshold)

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | |
| Appliance Type | Single line of text | e.g. Boiler, Fire |
| Appliance Make | Single line of text | Brand/manufacturer |
| Appliance Model | Single line of text | |
| Appliance Location | Single line of text | Where in property |
| Fuel Type | Choice | e.g. Gas, Oil, Electric |
| Serial Number | Single line of text | |
| Gas Council Number | Single line of text | |
| Service Due | Date and Time | |
| Service Interval Months | Choice | e.g. 12, 24 months |
| Status | Choice | |
| Notes | Multiple lines of text | |
| Scheduling Notes | Multiple lines of text | |
| Customer | Lookup | → Customers |
| Job Address | Lookup | → Job Addresses |
| ID Val | Number | Custom numeric ID |
| Archive | Yes/No | |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Appointments
**URL:** `.../Lists/Appointments/AllItems.aspx`
**Size:** ~3,458 items

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | |
| Activity Type | Choice | Type of appointment |
| Date | Date and Time | Appointment date |
| Time | Choice | Appointment time slot |
| Staff | Lookup | → Staff list |
| Customer | Lookup | → Customers |
| Job Address | Lookup | → Job Addresses |
| Appliances | Lookup | → Appliances |
| Job | Lookup | → Jobs |
| Job Status | Choice | Current status of job |
| Activity Notes | Multiple lines of text | |
| Description of Works | Multiple lines of text | |
| Appointment Access Notes | Multiple lines of text | |
| Rates | Multiple lines of text | Pricing notes |
| Priority | Choice | |
| Outlook Calendar ID | Single line of text | ID for linked Outlook calendar event |
| Planner Task ID | Single line of text | ID for linked Planner task |
| Job Id | Single line of text | Reference to Jobs list |
| Update Calendar | Yes/No | Flag to trigger calendar sync |
| Update Planner | Yes/No | Flag to trigger Planner sync |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Jobs
**URL:** `.../Lists/Jobs/AllItems.aspx`

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | |
| Job Id | Single line of text | Human-readable reference ID |
| Job Type | Choice | e.g. Service, Repair, Installation |
| Status | Choice | |
| Priority | Choice | |
| Customer | Lookup | → Customers |
| Job Address | Lookup | → Job Addresses |
| Project Owner | Lookup | → Staff (person responsible) |
| Job Description | Multiple lines of text | |
| Notes | Multiple lines of text | |
| Planner Task ID | Single line of text | |
| Update Planner | Yes/No | |
| Bookable | Yes/No | Whether job can be booked via app |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Job Scheduling
**URL:** `.../Lists/Job Scheduling/AllItems.aspx`
Used by **ProjectSchedulerScreen** in the Appointment App.

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | |
| Schedule Description | Single line of text | |
| Job | Lookup | → Jobs |
| Visit Type | Choice | Type of visit/visit category |
| Staff | Lookup | → Staff |
| Start Date | Date and Time | |
| End Date | Date and Time | |
| Start Time | Choice | Time slot |
| End Time | Choice | Time slot |
| Working Days | Choice | Days covered by schedule |
| Schedule Notes | Multiple lines of text | |
| Planner Task ID | Single line of text | |
| Outlook Calendar ID | Single line of text | |
| Update Calendar | Yes/No | Flag to trigger calendar sync |
| Update Planner | Yes/No | Flag to trigger Planner sync |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Staff
**URL:** `.../Lists/Staff/AllItems.aspx`
Referenced by Appointments, Job Scheduling, Jobs (Project Owner), Qualification Records, Vehicles.

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | Staff member name/reference |
| Profile | Person or Group | Links to M365 user account |
| Staff Type | Choice | e.g. Engineer, Admin, etc. |
| Calendar Access Allowed | Yes/No | Whether staff can access calendar features |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Qualification Types
**URL:** `.../Lists/Qualification Types/AllItems.aspx`
Reference list for types of qualifications held by staff.

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | Qualification name |
| Code | Single line of text | Short reference code |
| Renewal (Years) | Number | How often the qualification must be renewed |
| Training Provider | Single line of text | |
| Description | Single line of text | |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Qualification Records
**URL:** `.../Lists/Qualification Records/AllItems.aspx`
Individual qualification records per staff member.

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | |
| Staff | Lookup | → Staff |
| Qualification Name | Lookup | → Qualification Types |
| Qualification Name: Code | Lookup | → Qualification Types (Code field) |
| Start Date | Date and Time | When qualification was obtained |
| Expiry Date | Date and Time | When qualification expires |
| Certificate Link | Hyperlink or Picture | Link to certificate document |
| Notes | Multiple lines of text | |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Vehicles
**URL:** `.../Lists/Vehicles/AllItems.aspx`
Company vehicle fleet records.

| Column | Type | Notes |
|---|---|---|
| Title | Single line of text | Vehicle name/reference |
| Registration | Single line of text | Number plate |
| Driver | Lookup | → Staff (assigned driver) |
| Year | Number | Year of manufacture |
| Make | Single line of text | e.g. Ford, Vauxhall |
| Model | Single line of text | |
| Description | Single line of text | |
| Colour | Single line of text | |
| Transmission | Choice | e.g. Manual, Automatic |
| Fuel Type | Choice | e.g. Diesel, Petrol, Electric |
| Vehicle Type | Choice | e.g. Van, Car |
| Tracker | Yes/No | Whether vehicle has a GPS tracker |
| Next Service Date | Date and Time | |
| Tax Due Date | Date and Time | |
| MOT Due Date | Date and Time | |
| VIN | Single line of text | Vehicle Identification Number |
| Created | Date and Time | |
| Modified | Date and Time | |
| Created By | Person or Group | |
| Modified By | Person or Group | |

---

## Shared Equipment
**URL:** `.../Lists/Shared Equipment/AllItems.aspx`
Used by the **Asset Check In/Out app**. Master list of all company assets.
**Note:** The `Title` column has been renamed to display as `AssetID` — the internal SharePoint name is still `Title`.

| Column | Internal Name | Type | Notes |
|---|---|---|---|
| AssetID | Title | Single line | e.g. JX100001. Required. Unique. |
| AssetCategory | AssetCategory | Choice | Office \| Yard / Tool Store \| Van \| Engineer Owned |
| BarCode | BarCode | Single line | For future barcode scanning |
| ItemDescription | ItemDescription | Single line | What the asset is |
| Make | Make | Single line | Brand |
| Model | Model | Single line | Model number |
| SerialNumber | SerialNumber | Single line | Manufacturer serial |
| PowerType | PowerType | Choice | 240V \| 110V \| Battery \| N/A |
| Location | Location | Single line | Where it's stored |
| Status | Status | Choice | Available \| Checked Out \| Under Repair \| Retired |
| CurrentAssignedTo | CurrentAssignedTo | Person or Group | Null when available |
| CheckedOutDate | CheckedOutDate | Date and Time | Null when available |
| ExpectedReturnDate | ExpectedReturnDate | Date and Time | Set on check-out |
| RequiresPATTest | RequiresPATTest | Yes/No | |
| PATTestDue | PATTestDue | Date and Time | |
| TestFrequencyMonths | TestFrequencyMonths | Number | Default 12 |
| RequiresCalibration | RequiresCalibration | Yes/No | |
| CalibrationDue | CalibrationDue | Date and Time | |
| Notes | Notes | Multiple lines | General notes |
| PurchaseDate | PurchaseDate | Date and Time | |
| PurchaseValue | PurchaseValue | Currency | |
| WarrantyExpiry | WarrantyExpiry | Date and Time | |
| IsActive | IsActive | Yes/No | Soft delete. Default true. |

**Asset ID prefix convention:**
- `JX1xxxxx` = Office equipment
- `JX2xxxxx` = Yard / Tool Store equipment
- `JX3xxxxx` = Van-based equipment
- `JX4xxxxx` = Engineer Owned equipment

**Current count:** 79 assets (39 Office, 39 Yard/Tool Store, 1 Van partial)

---

## Equipment List Log
**URL:** `.../Lists/Equipment List Log/AllItems.aspx`
Used by the **Asset Check In/Out app**. Append-only audit trail — never delete rows.

| Column | Internal Name | Type | Notes |
|---|---|---|---|
| Title | Title | Single line | Auto-generated: `AssetID – DD/MM/YYYY HH:MM` |
| AssetID | AssetID | Lookup → Shared Equipment | Links to asset record |
| Action | Action | Choice | Check Out \| Check In \| Under Repair \| Returned from Repair |
| StaffMember | StaffMember | Person or Group | Who performed the action |
| ActionDateTime | ActionDateTime | Date and Time | Includes time |
| ExpectedReturnDate | ExpectedReturnDate | Date and Time | Check-outs only |
| Notes | Notes | Multiple lines | Reason, job ref, condition notes |
| Condition | Condition | Choice | Good \| Damaged \| Needs Service |

---

## Other Lists (schema not yet captured)
The following lists exist in the SharePoint site but schemas have not been captured yet.
They may be relevant for future apps or automations.

| List | Notes |
|---|---|
| Planner: Servicing | Planner board for servicing jobs |
| Planner: Breakdown | Planner board for breakdown callouts |
| Planner: Quotes | Planner board for quotes |
| Planner: Quoted Works | Planner board for quoted works in progress |
| Planner: General Jobs | Planner board for general jobs |
| Planner: Projects | Planner board for project work |
| Asset Register | Company asset tracking |

---

## Relationships Overview
```
Customers
  ├── Job Addresses         (Job Addresses.Customer → Customers)
  │     └── Appliances      (Appliances.Customer → Customers,
  │                          Appliances.Job Address → Job Addresses)
  └── Jobs                  (Jobs.Customer → Customers,
        │                    Jobs.Job Address → Job Addresses,
        │                    Jobs.Project Owner → Staff)
        ├── Appointments     (Appointments.Customer, .Job Address,
        │                     .Appliances, .Job → respective lists,
        │                     .Staff → Staff)
        └── Job Scheduling   (Job Scheduling.Job → Jobs,
                              Job Scheduling.Staff → Staff)

Staff
  ├── Appointments          (.Staff → Staff)
  ├── Job Scheduling        (.Staff → Staff)
  ├── Jobs                  (.Project Owner → Staff)
  ├── Vehicles              (.Driver → Staff)
  └── Qualification Records (.Staff → Staff)
        └── Qualification Types  (.Qualification Name → Qualification Types)
```
