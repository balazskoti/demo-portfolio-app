"""Risk-adjusted performance ratios.

Requested by the Ironhold investment committee (IRN-022) for the daily
risk pack. These numbers sit alongside VaR in the same report.
"""

from decimal import Decimal
from math import sqrt
from statistics import mean, pstdev
from typing import List


def _annualise_factor(period_per_year: int) -> float:
    return sqrt(period_per_year)


def sharpe_ratio(
    returns: List[Decimal],
    risk_free: Decimal = Decimal("0"),
    periods_per_year: int = 252,
) -> Decimal:
    if len(returns) < 2:
        return Decimal("0")
    excess = [float(r - risk_free) for r in returns]
    sigma = pstdev(excess)
    if sigma == 0:
        return Decimal("0")
    raw = mean(excess) / sigma * _annualise_factor(periods_per_year)
    return Decimal(str(raw))


def sortino_ratio(
    returns: List[Decimal],
    target: Decimal = Decimal("0"),
    periods_per_year: int = 252,
) -> Decimal:
    if len(returns) < 2:
        return Decimal("0")
    diffs = [float(r - target) for r in returns]
    downside = [d * d for d in diffs if d < 0]
    if not downside:
        return Decimal("0")
    downside_dev = sqrt(sum(downside) / len(returns))
    if downside_dev == 0:
        return Decimal("0")
    raw = mean(diffs) / downside_dev * _annualise_factor(periods_per_year)
    return Decimal(str(raw))
