"""Quarterly realised gain/loss report.

Feeds the tax export that Harborlight's advisors hand to clients for
their accountants (HBL-084). Rows are produced per realised lot,
classified short-term vs long-term based on the 12-month holding rule.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Iterable, List


LONG_TERM_THRESHOLD = timedelta(days=365)


@dataclass
class RealisedRow:
    account_id: str
    instrument_id: str
    acquired: date
    disposed: date
    quantity: Decimal
    proceeds: Decimal
    cost_basis: Decimal

    @property
    def gain(self) -> Decimal:
        return self.proceeds - self.cost_basis

    @property
    def holding_days(self) -> int:
        return (self.disposed - self.acquired).days

    @property
    def is_long_term(self) -> bool:
        return (self.disposed - self.acquired) >= LONG_TERM_THRESHOLD


@dataclass
class Summary:
    short_term_gain: Decimal
    long_term_gain: Decimal
    rows: List[RealisedRow]


def summarise(rows: Iterable[RealisedRow]) -> Summary:
    rows = list(rows)
    st = sum((r.gain for r in rows if not r.is_long_term), Decimal("0"))
    lt = sum((r.gain for r in rows if r.is_long_term), Decimal("0"))
    return Summary(short_term_gain=st, long_term_gain=lt, rows=rows)
