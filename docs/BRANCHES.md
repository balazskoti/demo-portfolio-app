# Branch strategy

This repository uses a **mainline + customer branch** model.

## `main`

The canonical trunk. All generic product work lands here first. `main`
should always be in a shippable state: the CI pipeline gates merges, and
the product owner signs off on the weekly cut.

`main` contains no customer-specific code, no customer branding, and no
customer-specific configuration. If a change is only relevant for a single
customer it belongs on that customer's branch, not on `main`.

## Customer deployment branches

Each production customer has its own long-lived branch forked from `main`.
These branches contain everything `main` has, plus the modifications,
integrations, configuration and branding that a particular customer has
paid for or negotiated.

Current customer branches:

| Branch              | Customer            | Deployment                          |
|---------------------|---------------------|-------------------------------------|
| `customer/ironhold` | Ironhold Capital    | EU-West, production since 2025-10   |
| `customer/harborlight` | Harborlight Wealth Management | US-East, production since 2025-10 |

Ticket prefixes tell you which tracker an item came from:

- `PT-xxx` — Meridian Systems product backlog (lands on `main`)
- `IRN-xxx` — Ironhold Capital change requests
- `HBL-xxx` — Harborlight Wealth change requests

### Working on a customer branch

1. Branch from the customer branch, not from `main`.
2. Reference the customer's ticket id in the subject line.
3. Keep customer-specific code behind clearly-named modules (under
   `backend/app/customer/…` or inside files whose names identify the
   customer). Do not sprinkle `if customer == "…"` checks through shared
   code.
4. When a change looks generally useful, copy it (or lift the generic
   slice of it) back to `main` in a separate PR.

### Forward-porting from `main`

Each customer branch is rebased onto `main` at the start of every release
cycle. Conflicts are expected in customer-owned files; the rule of thumb
is **prefer the customer side for customer-owned files, prefer `main` for
everything else**. See the runbook in `docs/DEVELOPMENT.md` for the
mechanical steps.

### What is *not* documented here

This document intentionally does **not** enumerate what each customer
branch contains. The set of modifications per customer drifts over time
as new tickets land, and keeping a hand-maintained list accurate has
historically been a losing battle. To understand what a particular
customer's deployment does differently, read:

1. The customer-specific modules and config on that branch.
2. The commit history of that branch compared to `main`
   (`git log main..customer/<name>`).
3. The customer's ticket tracker (prefix filter).

An automated "branch diff report" is being developed to replace this
section. Until it lands, the branch itself is the source of truth.
