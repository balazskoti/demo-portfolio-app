"""Reporting service.

Produces tabular extracts that can be rendered as CSV or JSON. The core
output right now is the daily NAV report used by the operations team for
end-of-day reconciliation.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable, List

from ..models import Portfolio
from .valuation import ValuationEngine


@dataclass
class NavRow:
    as_of: date
    portfolio_id: str
    portfolio_name: str
    nav: Decimal


class ReportingService:
    def __init__(self, valuation: ValuationEngine):
        self._valuation = valuation

    def daily_nav(
        self, as_of: date, portfolios: Iterable[Portfolio]
    ) -> List[NavRow]:
        out: List[NavRow] = []
        for p in portfolios:
            v = self._valuation.value(p)
            out.append(
                NavRow(
                    as_of=as_of,
                    portfolio_id=p.id,
                    portfolio_name=p.name,
                    nav=v.nav,
                )
            )
        return out

    def to_csv(self, rows: List[NavRow]) -> str:
        lines = ["as_of,portfolio_id,portfolio_name,nav"]
        for r in rows:
            lines.append(f"{r.as_of.isoformat()},{r.portfolio_id},{r.portfolio_name},{r.nav}")
        return "\n".join(lines) + "\n"
