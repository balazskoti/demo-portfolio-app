"""Portfolio valuation.

Computes market value, unrealized P&L and weights for each position,
plus an aggregate NAV for the portfolio.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List

from ..models import Portfolio
from .pricing import PricingService


@dataclass
class PositionValuation:
    instrument_id: str
    quantity: Decimal
    price: Decimal
    market_value: Decimal
    unrealized_pnl: Decimal
    weight: Decimal


@dataclass
class PortfolioValuation:
    portfolio_id: str
    nav: Decimal
    positions: List[PositionValuation]


class ValuationEngine:
    def __init__(self, pricing: PricingService):
        self._pricing = pricing

    def value(self, portfolio: Portfolio) -> PortfolioValuation:
        rows: List[PositionValuation] = []
        total = Decimal("0")
        for pos in portfolio.positions:
            px = self._pricing.price(pos.instrument_id)
            mv = pos.quantity * px
            pnl = (px - pos.avg_cost) * pos.quantity
            rows.append(
                PositionValuation(
                    instrument_id=pos.instrument_id,
                    quantity=pos.quantity,
                    price=px,
                    market_value=mv,
                    unrealized_pnl=pnl,
                    weight=Decimal("0"),
                )
            )
            total += mv
        if total > 0:
            for r in rows:
                r.weight = r.market_value / total
        return PortfolioValuation(
            portfolio_id=portfolio.id, nav=total, positions=rows
        )
