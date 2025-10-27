"""Performance attribution by strategy tag.

Ironhold tags every position with a *strategy* (e.g. ``long_equity``,
``macro``, ``credit_rv``). The PM team wants the weekly review to
break P&L and contribution down by that tag (IRN-067).
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List


@dataclass
class AttributionRow:
    strategy: str
    contribution: Decimal
    weight: Decimal


def by_strategy(
    pnl_by_position: Dict[str, Decimal],
    weight_by_position: Dict[str, Decimal],
    strategy_tag: Dict[str, str],
) -> List[AttributionRow]:
    agg: Dict[str, Decimal] = {}
    wgt: Dict[str, Decimal] = {}
    for pos_id, pnl in pnl_by_position.items():
        tag = strategy_tag.get(pos_id, "unclassified")
        agg[tag] = agg.get(tag, Decimal("0")) + pnl
        wgt[tag] = wgt.get(tag, Decimal("0")) + weight_by_position.get(
            pos_id, Decimal("0")
        )
    return [
        AttributionRow(strategy=tag, contribution=agg[tag], weight=wgt[tag])
        for tag in sorted(agg)
    ]
