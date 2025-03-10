from fastapi import APIRouter, HTTPException

from ..db import store
from ..services.pricing import PricingService, StaticPriceFeed
from ..services.valuation import ValuationEngine

router = APIRouter()

_feed = StaticPriceFeed({})
_pricing = PricingService(_feed)
_valuation = ValuationEngine(_pricing)


@router.get("/portfolios")
def list_portfolios():
    return [{"id": p.id, "name": p.name} for p in store.portfolios.values()]


@router.get("/portfolios/{portfolio_id}")
def get_portfolio(portfolio_id: str):
    p = store.portfolios.get(portfolio_id)
    if not p:
        raise HTTPException(404, "portfolio not found")
    return p


@router.get("/portfolios/{portfolio_id}/valuation")
def valuation(portfolio_id: str):
    p = store.portfolios.get(portfolio_id)
    if not p:
        raise HTTPException(404, "portfolio not found")
    return _valuation.value(p)
