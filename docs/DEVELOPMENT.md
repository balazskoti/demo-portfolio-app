# Development

## Prerequisites

- Python 3.11
- Node 20
- `pip` and `npm`

## Backend

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

Tests:

```bash
pytest backend/tests -q
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Branch strategy

Mainline development happens on `main`. Customer-specific deployments live
on long-running branches (see `docs/BRANCHES.md`). Features land on `main`
first and are forward-ported to customer branches on a regular cadence.

## Commit conventions

- Short imperative subject (≤ 72 chars).
- Reference the ticket id in the subject when one exists (e.g. `PT-142`,
  `IRN-014`, `HBL-025`). Ticket prefixes tell you which tracker the item
  came from.
