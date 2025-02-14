"""Pricing service.

Wraps the market data feed. For local/dev we use a static snapshot loaded
from config. In production a live adapter replaces ``StaticPriceFeed``.
"""

from decimal import Decimal
from typing import Dict, Protocol


class PriceFeed(Protocol):
    def get_price(self, instrument_id: str) -> Decimal: ...


class StaticPriceFeed:
    def __init__(self, snapshot: Dict[str, Decimal]):
        self._snapshot = snapshot

    def get_price(self, instrument_id: str) -> Decimal:
        if instrument_id not in self._snapshot:
            raise KeyError(f"no price for {instrument_id}")
        return self._snapshot[instrument_id]


class PricingService:
    def __init__(self, feed: PriceFeed):
        self._feed = feed

    def price(self, instrument_id: str) -> Decimal:
        return self._feed.get_price(instrument_id)

    def price_many(self, ids):
        return {i: self._feed.get_price(i) for i in ids}
