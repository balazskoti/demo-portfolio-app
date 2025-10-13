"""Nightly stress tests.

Ironhold's risk committee mandates a standard set of shock scenarios
applied to the book each night (IRN-058). The scenarios are versioned
and stored in ``config/ironhold/stress_scenarios.yaml``; this module
loads them and reports the portfolio-level P&L under each.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List

from ...models import Portfolio


@dataclass
class Scenario:
    name: str
    # Multiplicative shocks keyed by asset class.
    shocks: Dict[str, Decimal]


@dataclass
class ScenarioResult:
    scenario: str
    portfolio_id: str
    shocked_nav: Decimal
    delta: Decimal


def apply_scenario(
    portfolio: Portfolio,
    base_prices: Dict[str, Decimal],
    shocks: Dict[str, Decimal],
    asset_class: Dict[str, str],
) -> Decimal:
    total = Decimal("0")
    for pos in portfolio.positions:
        ac = asset_class.get(pos.instrument_id, "equity")
        px = base_prices.get(pos.instrument_id, Decimal("0"))
        shocked = px * (Decimal("1") + shocks.get(ac, Decimal("0")))
        total += pos.quantity * shocked
    return total


def run_overnight(
    portfolios: List[Portfolio],
    base_prices: Dict[str, Decimal],
    asset_class: Dict[str, str],
    scenarios: List[Scenario],
) -> List[ScenarioResult]:
    out: List[ScenarioResult] = []
    for pf in portfolios:
        base_nav = sum(
            (pos.quantity * base_prices.get(pos.instrument_id, Decimal("0")))
            for pos in pf.positions
        )
        for sc in scenarios:
            shocked = apply_scenario(pf, base_prices, sc.shocks, asset_class)
            out.append(
                ScenarioResult(
                    scenario=sc.name,
                    portfolio_id=pf.id,
                    shocked_nav=shocked,
                    delta=shocked - Decimal(base_nav),
                )
            )
    return out
