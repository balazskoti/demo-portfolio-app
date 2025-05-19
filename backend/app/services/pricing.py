"""Pricing service.

Wraps the market data feed. For local/dev we use a static snapshot loaded
from config. In production a live adapter replaces ``StaticPriceFeed``.

Prices are always quantised to 4 decimal places before leaving the service,
which keeps downstream valuation numbers deterministic regardless of the
feed's native precision (PT-142).
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Protocol

_Q = Decimal("0.0001")


class PriceFeed(Protocol):
    def get_price(self, instrument_id: str) -> Decimal: ...


class StaticPriceFeed:
    def __init__(self, snapshot: Dict[str, Decimal]):
        self._snapshot = snapshot

    def get_price(self, instrument_id: str) -> Decimal:
        if instrument_id not in self._snapshot:
            raise KeyError(f"no price for {instrument_id}")
        return self._snapshot[instrument_id]


def _quantise(px: Decimal) -> Decimal:
    return px.quantize(_Q, rounding=ROUND_HALF_UP)


class PricingService:
    def __init__(self, feed: PriceFeed):
        self._feed = feed

    def price(self, instrument_id: str) -> Decimal:
        return _quantise(self._feed.get_price(instrument_id))

    def price_many(self, ids):
        return {i: self.price(i) for i in ids}
