# Architecture

## Overview

The Meridian Portfolio System is split into a Python FastAPI backend and
a React + Vite frontend. The backend owns the domain model and all
business rules; the frontend is a thin rendering layer that talks to the
backend over JSON.

```
+----------------+     HTTPS/JSON     +-----------------+
|  React client  | <----------------> |  FastAPI app    |
|  (advisors)    |                    |  (backend/)     |
+----------------+                    +-----------------+
                                              |
                                              v
                                       +-------------+
                                       |  Store /    |
                                       |  market data|
                                       +-------------+
```

## Backend layout

```
backend/app/
  models/      # dataclasses for the domain (Account, Portfolio, Position, …)
  services/    # business logic (pricing, valuation, reporting, transactions)
  api/         # FastAPI routers and auth
  config.py    # environment-driven settings
  db.py        # storage abstraction (in-memory stub, SQLAlchemy in prod)
  main.py      # app factory
```

### Key services

- **PricingService** — uniform access to a market data feed. All prices are
  quantised to 4 decimal places at the boundary.
- **ValuationEngine** — computes per-position market value, unrealized P&L
  and weights, and aggregates into a portfolio NAV.
- **ReportingService** — produces the daily NAV extract and other scheduled
  reports.
- **TransactionService** — records buys/sells and applies them to positions,
  idempotent on transaction id.

## Frontend layout

```
frontend/src/
  api/         # thin fetch wrapper
  components/  # reusable UI primitives
  pages/       # route-level screens (Dashboard, Portfolios, PositionList)
  App.tsx      # router
```

## Authentication

Session-based auth (signed JWT cookie). `auth.current_user` is a FastAPI
dependency that must be attached to every non-public route. Role-aware
routes use `auth.require_role(...)`.

## Environments

Settings come from env vars (`MERIDIAN_ENV`, `BASE_CCY`, `SESSION_SECRET`).
Per-deployment config files live under `config/`.
