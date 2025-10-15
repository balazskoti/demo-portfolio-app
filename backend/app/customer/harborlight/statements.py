"""Monthly client statement generator.

Harborlight sends each household a branded PDF statement on the first
business day of the month covering the prior month (HBL-059). The
template lives in ``backend/app/customer/harborlight/templates/statement.html``
and is rendered to PDF via the ``weasyprint`` adapter wired in at
deploy time.

The generator here is framework-agnostic — it produces a ``StatementData``
object that the renderer turns into bytes.
"""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List


@dataclass
class StatementLine:
    description: str
    amount: Decimal


@dataclass
class StatementData:
    household_id: str
    period_start: date
    period_end: date
    opening_balance: Decimal
    closing_balance: Decimal
    contributions: Decimal
    withdrawals: Decimal
    realised_gain: Decimal
    unrealised_gain: Decimal
    fees: Decimal
    lines: List[StatementLine] = field(default_factory=list)

    @property
    def net_change(self) -> Decimal:
        return self.closing_balance - self.opening_balance


def build(
    household_id: str,
    period_start: date,
    period_end: date,
    opening: Decimal,
    closing: Decimal,
    activity: List[StatementLine],
    realised_gain: Decimal,
    unrealised_gain: Decimal,
    fees: Decimal,
) -> StatementData:
    contribs = sum((l.amount for l in activity if l.amount > 0), Decimal("0"))
    withdrawals = -sum(
        (l.amount for l in activity if l.amount < 0), Decimal("0")
    )
    return StatementData(
        household_id=household_id,
        period_start=period_start,
        period_end=period_end,
        opening_balance=opening,
        closing_balance=closing,
        contributions=contribs,
        withdrawals=withdrawals,
        realised_gain=realised_gain,
        unrealised_gain=unrealised_gain,
        fees=fees,
        lines=activity,
    )
