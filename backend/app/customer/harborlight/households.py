"""Household account grouping.

Harborlight advisors work with households — e.g. the two spouses plus
the family trust are viewed together. This module groups accounts into
a household and produces rolled-up NAV, contributions and fee numbers
(HBL-096).
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List


@dataclass
class Household:
    id: str
    name: str
    account_ids: List[str] = field(default_factory=list)


@dataclass
class HouseholdSummary:
    household_id: str
    household_name: str
    account_count: int
    total_nav: Decimal


def rollup(
    households: List[Household], nav_by_account: Dict[str, Decimal]
) -> List[HouseholdSummary]:
    out: List[HouseholdSummary] = []
    for h in households:
        total = sum(
            (nav_by_account.get(a, Decimal("0")) for a in h.account_ids),
            Decimal("0"),
        )
        out.append(
            HouseholdSummary(
                household_id=h.id,
                household_name=h.name,
                account_count=len(h.account_ids),
                total_nav=total,
            )
        )
    return out
