"""Display-currency conversion for Harborlight clients.

Harborlight onboards clients from 14 countries. Each client picks a
display currency once; we continue to book and custody in USD but the
portal and statements present everything in their preferred currency
(HBL-071).

This module is a thin layer that:

1. Resolves the display currency for an account.
2. Converts a USD amount to that currency using the daily ECB reference
   fix (cached for 24 hours).
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict


@dataclass
class FxQuote:
    pair: str  # e.g. "USD/EUR"
    rate: Decimal


class FxCache:
    def __init__(self, quotes: Dict[str, Decimal]):
        # quotes keyed on "USD/<CCY>"
        self._quotes = quotes

    def convert_from_usd(self, amount: Decimal, target_ccy: str) -> Decimal:
        if target_ccy == "USD":
            return amount
        rate = self._quotes.get(f"USD/{target_ccy}")
        if rate is None:
            raise KeyError(f"no fx rate for USD/{target_ccy}")
        return amount * rate
