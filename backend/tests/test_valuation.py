from decimal import Decimal

from backend.app.models import Portfolio, Position
from backend.app.services.pricing import PricingService, StaticPriceFeed
from backend.app.services.valuation import ValuationEngine


def _engine(prices):
    return ValuationEngine(PricingService(StaticPriceFeed(prices)))


def test_nav_is_sum_of_market_values():
    eng = _engine({"AAA": Decimal("10"), "BBB": Decimal("20")})
    p = Portfolio(
        id="p1",
        account_id="a1",
        name="Core",
        positions=[
            Position("p1", "AAA", Decimal("5"), Decimal("9")),
            Position("p1", "BBB", Decimal("3"), Decimal("15")),
        ],
    )
    v = eng.value(p)
    assert v.nav == Decimal("110.0000")


def test_weights_sum_to_one():
    eng = _engine({"AAA": Decimal("10"), "BBB": Decimal("10")})
    p = Portfolio(
        id="p1",
        account_id="a1",
        name="Core",
        positions=[
            Position("p1", "AAA", Decimal("5"), Decimal("10")),
            Position("p1", "BBB", Decimal("5"), Decimal("10")),
        ],
    )
    v = eng.value(p)
    assert sum(r.weight for r in v.positions) == Decimal("1")
