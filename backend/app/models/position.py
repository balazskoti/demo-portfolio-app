from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Position:
    portfolio_id: str
    instrument_id: str
    quantity: Decimal
    avg_cost: Decimal

    def market_value(self, price: Decimal) -> Decimal:
        return self.quantity * price
