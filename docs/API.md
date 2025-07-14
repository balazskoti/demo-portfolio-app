# API reference

All endpoints live under `/api`. All non-public endpoints require a valid
session cookie; unauthenticated requests return `401`.

## Portfolios

### `GET /api/portfolios`
List portfolios visible to the current user.

Response: `[{ "id": "p1", "name": "Core Growth" }, ...]`

### `GET /api/portfolios/{portfolio_id}`
Return full portfolio record including positions.

### `GET /api/portfolios/{portfolio_id}/valuation`
Return an as-of valuation:

```json
{
  "portfolio_id": "p1",
  "nav": "123456.7800",
  "positions": [
    {
      "instrument_id": "AAPL",
      "quantity": "100",
      "price": "180.1234",
      "market_value": "18012.34",
      "unrealized_pnl": "1012.34",
      "weight": "0.1459"
    }
  ]
}
```

## Transactions

Transactions are written through the `TransactionService`. The service is
idempotent on the transaction `id`: replaying the same id returns the
previously recorded transaction unchanged.
