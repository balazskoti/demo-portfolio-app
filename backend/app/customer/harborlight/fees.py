"""Tiered management-fee schedule.

Harborlight charges a management fee that steps down as assets under
management grow (HBL-025). Fee tiers are stored per household; the same
schedule is applied to the sum of account NAVs inside the household.

Example schedule:

    0 – 500k      : 1.20 %
    500k – 2m     : 1.00 %
    2m – 10m      : 0.75 %
    > 10m         : 0.50 %

Fees are accrued daily and billed quarterly.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class FeeTier:
    upper_bound: Decimal  # inclusive upper bound; last tier uses Decimal("Infinity")
    rate: Decimal  # annualised


@dataclass
class FeeSchedule:
    household_id: str
    tiers: List[FeeTier]


def annual_fee(schedule: FeeSchedule, aum: Decimal) -> Decimal:
    remaining = aum
    prev = Decimal("0")
    total = Decimal("0")
    for tier in schedule.tiers:
        if remaining <= 0:
            break
        slice_top = tier.upper_bound
        slice_size = min(remaining, slice_top - prev)
        total += slice_size * tier.rate
        remaining -= slice_size
        prev = slice_top
    return total


def daily_accrual(schedule: FeeSchedule, aum: Decimal, days: int = 365) -> Decimal:
    return annual_fee(schedule, aum) / Decimal(days)
