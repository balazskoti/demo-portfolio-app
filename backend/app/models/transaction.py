from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


class TxType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    FEE = "fee"
    CASH_IN = "cash_in"
    CASH_OUT = "cash_out"


@dataclass
class Transaction:
    id: str
    portfolio_id: str
    instrument_id: str
    tx_type: TxType
    quantity: Decimal
    price: Decimal
    trade_date: datetime
    settle_date: datetime
    fees: Decimal = Decimal("0")

    @property
    def gross_amount(self) -> Decimal:
        return self.quantity * self.price

    @property
    def net_amount(self) -> Decimal:
        return self.gross_amount - self.fees
