"""Risk metrics for the Ironhold deployment.

Ironhold's investment committee receives a daily risk pack. The numbers
produced here feed that pack.

The two VaR methodologies below are the ones the committee signed off on
(IRN-014):

- *Historical simulation*: rank the last N daily P&L observations and
  pick the empirical quantile.
- *Parametric (variance-covariance)*: assume P&L is normal and scale the
  standard deviation by the inverse-normal at the chosen confidence.

Both are reported; the pack shows the more conservative of the two.
"""

from dataclasses import dataclass
from decimal import Decimal
from math import sqrt
from statistics import NormalDist, stdev
from typing import List


@dataclass
class VaRResult:
    confidence: float
    horizon_days: int
    historical: Decimal
    parametric: Decimal

    @property
    def reported(self) -> Decimal:
        return max(self.historical, self.parametric)


def historical_var(pnl_series: List[Decimal], confidence: float) -> Decimal:
    if not pnl_series:
        return Decimal("0")
    ordered = sorted(pnl_series)
    idx = max(0, int(len(ordered) * (1 - confidence)) - 1)
    loss = -ordered[idx]
    return loss if loss > 0 else Decimal("0")


def parametric_var(
    pnl_series: List[Decimal], confidence: float, horizon_days: int = 1
) -> Decimal:
    if len(pnl_series) < 2:
        return Decimal("0")
    floats = [float(x) for x in pnl_series]
    sigma = stdev(floats)
    z = NormalDist().inv_cdf(confidence)
    return Decimal(str(z * sigma * sqrt(horizon_days)))


def compute_var(
    pnl_series: List[Decimal],
    confidence: float = 0.99,
    horizon_days: int = 1,
) -> VaRResult:
    return VaRResult(
        confidence=confidence,
        horizon_days=horizon_days,
        historical=historical_var(pnl_series, confidence),
        parametric=parametric_var(pnl_series, confidence, horizon_days),
    )
