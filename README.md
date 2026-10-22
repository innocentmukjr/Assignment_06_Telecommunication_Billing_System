# 📱 Telecommunication Billing System

**Assignment 06 — MIJ Technologies Python Programming Series**
*From Complete Beginner to Software Engineer Foundations — Functions, Loops & Conditionals*

A command-line program that simulates a telecom provider's billing engine: it records a customer's plan and usage for the month (peak/off-peak minutes, SMS, data), applies per-plan allowances and tiered overage pricing, prints a full usage and billing breakdown, and produces a daily report with plan popularity tracking.

---

## 🎯 Overview

This project is **Assignment 6**, and it's the most structurally varied assignment in the series so far — not because the math is harder, but because the *display logic itself branches* by plan type. Prepaid has no base fee or allowance and is billed from minute one; Gold has unlimited calls/SMS and only data can overage; Bronze and Silver sit in between with real allowances. Rather than duplicating near-identical overage logic four times, the solution generalizes tiered-bracket billing (the same bucket-filling idea from the electricity and parking assignments) into one reusable `get_tier_breakdown()` helper that every usage type — calls, SMS, data — calls into, just with different lookup tables.

| | |
|---|---|
| **Topics Covered** | Functions, Loops & Conditionals |
| **Difficulty** | Hard |
| **Total Marks** | 30 |
| **Estimated Time** | 5–6 hours |

---

## ✨ Features

- **Repeated customer entry** — the operator can bill as many customers as needed in a single session before stopping.
- **Four distinct plan types** (Prepaid, Bronze, Silver, Gold), each with its own base fee, allowance, and display treatment.
- **Prepaid pay-as-you-go billing** — no base fee, no allowance, every minute/SMS/MB billed from the first unit at Tier 1 rates.
- **Gold unlimited calls & SMS** — only data usage is ever billed for Gold customers; calls and SMS always show "Unlimited plan."
- **Allowance-aware usage summary** — for Bronze/Silver/Gold, shows exactly how far under or over each allowance the customer's usage fell, with correct singular/plural and unit-specific wording.
- **Off-peak minutes billed with no allowance at all** — off-peak usage is never covered by any plan's minute allowance and is billed from the first minute on every plan except Prepaid's blended treatment.
- **Genuine tiered overage calculation**, shared across calls, SMS, and data via one reusable bracket-filling function rather than three separate implementations.
- **Itemized overage/usage charges** — every tier actually touched is listed with its unit count, rate, and subtotal; untouched tiers are silently skipped.
- **Daily billing report** — total customers, total revenue, average bill, a full per-plan breakdown, and the most popular plan with tie handling.
- **Defensive input validation** — empty fields, non-integer usage figures, and invalid plan names are all caught and re-prompted rather than crashing the program.
- **Graceful exit handling** — `Ctrl+C` / `Ctrl+D` are caught so the program never crashes on interrupt.

---

## 🧮 Business Rules

**Monthly Base Fee by Plan**

| Plan | Base Fee |
|---|---|
| Prepaid | 0 UGX (pay-as-you-go) |
| Bronze | 20,000 UGX |
| Silver | 50,000 UGX |
| Gold | 100,000 UGX |

**Plan Allowances**

| Plan | Peak Minutes | SMS | Data |
|---|---|---|---|
| Prepaid | 0 | 0 | 0 |
| Bronze | 50 | 100 | 1 GB |
| Silver | 200 | 500 | 5 GB |
| Gold | Unlimited | Unlimited | 20 GB |

Off-peak minutes are **never** covered by any allowance on any plan — they're billed from the first minute using the call overage tiers.

**Call Overage Tiers** (per minute, UGX)

| Minutes Over Allowance | Peak Rate | Off-Peak Rate |
|---|---|---|
| 0 – 50 | 500 | 300 |
| 50 – 200 | 400 | 250 |
| 200+ | 300 | 200 |

**SMS Overage Tiers** (per message, UGX)

| Messages Over Allowance | Rate |
|---|---|
| 0 – 100 | 200 |
| 100 – 500 | 150 |
| 500+ | 100 |

**Data Overage Tiers** (per GB, UGX)

| GB Over Allowance | Rate |
|---|---|
| 0 – 5 | 5,000 |
| 5 – 20 | 4,000 |
| 20+ | 3,000 |

`Total Bill = Base Fee + Overage Charges` (for Prepaid, the "overage" tiers apply to total usage from zero, since there is no base fee or allowance to offset against)

**Worked Example — Bronze, 80 peak min, 500 MB data**
```
Allowance: 50 peak min, 1 GB data
Peak overage: 30 min over allowance
  First 50 min @ 500 = n/a (within the 0-50-over bracket, only 30 min used)
  30 min x 500 UGX/min = 15,000 UGX
Data: 0.5 GB used, within 1 GB allowance -> no data overage
Base Fee: 20,000 UGX
Total Bill: 20,000 + 15,000 = 35,000 UGX
```

---

## 🏗️ Code Structure

Every customer's data lives in a single dictionary (`d`), and the overage calculation is deliberately generalized rather than duplicated per usage type.

| Function | Responsibility |
|---|---|
| `collect_customer_details()` | Collects name, plan, peak/off-peak minutes, SMS, and data used |
| `get_input()` / `get_text_input()` | Raw and title-cased text input helpers that refuse empty answers |
| `get_nonnegative_integer()` | Ensures usage fields are valid non-negative integers |
| `validate_plan()` | Ensures plan matches one of the four accepted options |
| `get_base_fee()` | Looks up the monthly base fee for a plan |
| `display_plan_allowances()` | Prints the customer's plan allowances, with Gold shown as unlimited |
| `display_usage_summary()` | Shows usage against allowance, including the free/unlimited case for Gold |
| `allowance_note()` | Builds the "X below/over/at allowance" phrase for a single usage figure, unit-aware |
| `get_tier_breakdown()` | **The core reusable function** — given a usage total, an allowance, and a tier table, walks the tiers and returns exactly which brackets were touched and what each cost |
| `print_tier_charges()` | Renders a tier breakdown as aligned, multi-line output, or "No overage charges" if empty |
| `display_overage_charges()` | Orchestrates the overage/usage display per plan type (Prepaid vs. Gold vs. Bronze/Silver), calling `get_tier_breakdown()` once per usage type |
| `display_customer_bill()` | Prints the final consolidated bill |
| `ask_another_customer()` | Yes/No loop for whether to bill another customer |
| `display_daily_report()` | Aggregates totals, per-plan breakdown, and most popular plan (with ties) |
| `main()` | Orchestrates the loop: input → allowances/usage (if not Prepaid) → overage → bill → repeat/exit → report |

`get_tier_breakdown()` is the structural centerpiece: instead of writing near-identical tier-walking code four separate times (peak calls, off-peak calls, SMS, data), the same function is called four times with different tier tables and allowance values — the same table-driven pattern used for the progressive tariff in Assignment 3 and the duration tiers in Assignment 4, taken one step further into a fully shared, reusable helper.

---

## ▶️ How to Run

```bash
python3 telecommunication_billing_system.py
```

You'll be prompted for customer and usage details. Depending on the plan, the allowance summary, usage summary, overage/usage charges, and final bill are displayed in sequence, then you're asked whether to bill another customer. Answering **No** ends the session and prints the daily billing report.

---

## 🖥️ Sample Session

```
Enter Customer Name: John Smith
Enter Plan (Prepaid/Bronze/Silver/Gold): Bronze
Enter Peak Hour Minutes: 80
Enter Off-Peak Minutes: 10
Enter SMS Sent: 120
Enter Data Used (GB): 0

===============================================================================
   PLAN ALLOWANCES (Bronze)
===============================================================================
  Calls (Peak only)    : 50 minutes
  SMS                   : 100 messages
  Data                  : 1 GB

===============================================================================
   USAGE SUMMARY
===============================================================================
  Peak Minutes          : 80 (30 over the 50-min allowance)
  Off-Peak Minutes      : 10 (not covered by allowance - billed from min 1)
  SMS                   : 120 (20 over allowance)
  Data                  : 0 GB (1 GB below allowance)

===============================================================================
   OVERAGE CHARGES
===============================================================================
  Peak Call Overage     : 30 min @ 500 UGX/min  =     15,000 UGX
  Off-Peak Call Charge  : 10 min @ 300 UGX/min  =      3,000 UGX
  SMS Overage           : 20 SMS @ 200 UGX      =      4,000 UGX
  Data Overage          : No overage charges
                          ---------------------------------------
  TOTAL OVERAGE         =     22,000 UGX

===============================================================================
   CUSTOMER BILL
===============================================================================
  Customer              : John Smith
  Plan                  : Bronze
  Base Fee              : 20,000 UGX
  Overage                : 22,000 UGX
  TOTAL BILL            =     42,000 UGX

Add another customer? (yes/no): no

===============================================================================
   DAILY BILLING REPORT
===============================================================================
  Total Customers       : 1
  Total Revenue         : 42,000 UGX
  Average Bill          : 42,000.00 UGX
  Plan Breakdown        : Prepaid: 0 | Bronze: 1 | Silver: 0 | Gold: 0
  Most Popular Plan     : Bronze
```

---

## ✅ Test Cases Verified

| Customer | Plan | Peak Min | Off-Peak Min | SMS | Data (GB) | Total Bill |
|---|---|---|---|---|---|---|
| John Smith | Bronze | 80 | 10 | 120 | 0 | 42,000 UGX |
| Mary Jane | Gold | 300 | 50 | 1000 | 25 | 115,000 UGX |
| Peter Okello | Prepaid | 20 | 5 | 30 | 1 | (billed entirely from Tier 1, no base fee) |

---

## 🧠 What This Assignment Reinforced

- Generalizing a tiered-bracket calculation into one reusable function (`get_tier_breakdown`) shared across multiple usage types, instead of duplicating the same bucket-filling loop three or four times
- Branching display logic — not just calculation logic — cleanly by category (Prepaid vs. Gold vs. standard plans), while keeping the underlying overage math identical
- Passing a tier table's rate column index as a parameter (`rate_index`) so the same tier-walking function can read different rate columns for peak vs. off-peak minutes from the same table
- Building unit-aware helper text (`allowance_note`) that adapts its wording ("below", "over", "at") and unit label based on two numbers and a unit string, instead of writing the same comparison three times
- Designing print helpers (`print_tier_charges`) that gracefully handle the "zero tiers touched" case without extra branching at the call site

---

## 📂 Repository Contents

```
├── Assignment_06_Telecommunication_Billing_System.pdf   # Original assignment brief
├── telecommunication_billing_system.py                  # My solution
└── README.md                                              # This file
```

---

## 🧵 Series Note

This is part of an ongoing, sequential set of assignments from the **MIJ Technologies Python Programming Series**, each building on the last. Every solution in this repo series is written and understood by me before being committed — assignments are reviewed line-by-line for syntax and logic before upload.

**⬅️ Previous in series:** Assignment_05_Hospital_Patient_Billing_System
**➡️ Next in series:** *Assignment 07 (coming soon)*
