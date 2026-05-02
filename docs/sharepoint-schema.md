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
> Schema not yet captured — used by ProjectSchedulerScreen in the Appointment App.

---

## Other Lists (not yet in Appointment App)
The following lists exist in the SharePoint site but are not currently connected
to the Appointment App. They may be relevant for future apps or automations.

| List | Notes |
|---|---|
| Staff | Staff/engineer records |
| Qualification Types | Types of engineer qualifications |
| Qualification Records | Individual qualification records per staff member |
| Vehicles | Company vehicle records |
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
  ├── Job Addresses       (Job Addresses.Customer → Customers)
  │     └── Appliances    (Appliances.Customer → Customers,
  │                        Appliances.Job Address → Job Addresses)
  └── Jobs                (Jobs.Customer → Customers,
                           Jobs.Job Address → Job Addresses)
                             └── Appointments  (Appointments.Customer, .Job Address,
                                                .Appliances, .Job → respective lists)
```
