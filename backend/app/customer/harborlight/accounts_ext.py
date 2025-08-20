"""Harborlight-specific account configuration.

Layered on top of the shared ``Account`` model rather than modifying it,
so that forward-porting from mainline stays clean.
"""

from dataclasses import dataclass

from .tax_lots import CostBasisMethod


@dataclass
class HarborlightAccountConfig:
    account_id: str
    default_cost_basis: CostBasisMethod = CostBasisMethod.FIFO
    display_currency: str = "USD"
    household_id: str | None = None
