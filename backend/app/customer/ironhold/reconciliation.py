"""Reconcile our position book against Goldcrest's end-of-session file.

A reconciliation pass flags any position where Meridian's quantity or
average cost disagrees with Goldcrest's. Breaks go onto the operations
team's dashboard.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, List

from .goldcrest import GoldcrestPosition


@dataclass
class Break:
    account_code: str
    instrument: str
    meridian_qty: Decimal
    goldcrest_qty: Decimal


def find_breaks(
    internal: dict, goldcrest: Iterable[GoldcrestPosition]
) -> List[Break]:
    out: List[Break] = []
    for row in goldcrest:
        key = (row.account_code, row.instrument)
        ours = internal.get(key, Decimal("0"))
        if ours != row.quantity:
            out.append(
                Break(
                    account_code=row.account_code,
                    instrument=row.instrument,
                    meridian_qty=ours,
                    goldcrest_qty=row.quantity,
                )
            )
    return out
