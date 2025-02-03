from dataclasses import dataclass
from enum import Enum


class AssetClass(str, Enum):
    EQUITY = "equity"
    FIXED_INCOME = "fixed_income"
    CASH = "cash"
    FUND = "fund"
    DERIVATIVE = "derivative"


@dataclass
class Instrument:
    id: str
    symbol: str
    name: str
    asset_class: AssetClass
    currency: str = "USD"
