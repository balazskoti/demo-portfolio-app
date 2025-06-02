from decimal import Decimal

from backend.app.services.pricing import PricingService, StaticPriceFeed


def test_price_is_quantised_to_four_decimals():
    svc = PricingService(StaticPriceFeed({"X": Decimal("1.23456789")}))
    assert svc.price("X") == Decimal("1.2346")


def test_missing_price_raises():
    svc = PricingService(StaticPriceFeed({}))
    try:
        svc.price("Z")
    except KeyError:
        return
    raise AssertionError("expected KeyError")
