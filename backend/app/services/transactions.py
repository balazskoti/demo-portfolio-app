"""Transaction service.

Records buys, sells and corporate actions. A transaction's ``id`` is used
as an idempotency key: replaying the same id is a no-op.
"""

from decimal import Decimal
from typing import Optional

from ..db import store
from ..models import Transaction, TxType


class DuplicateTransaction(Exception):
    pass


class TransactionService:
    def record(self, tx: Transaction) -> Transaction:
        for existing in store.transactions:
            if existing.id == tx.id:
                # Idempotent replay — return the already-stored record.
                return existing
        store.transactions.append(tx)
        self._apply_to_position(tx)
        return tx

    def _apply_to_position(self, tx: Transaction) -> None:
        pf = store.portfolios.get(tx.portfolio_id)
        if not pf:
            return
        pos = next(
            (p for p in pf.positions if p.instrument_id == tx.instrument_id),
            None,
        )
        if tx.tx_type == TxType.BUY:
            if pos is None:
                from ..models import Position

                pf.positions.append(
                    Position(
                        portfolio_id=pf.id,
                        instrument_id=tx.instrument_id,
                        quantity=tx.quantity,
                        avg_cost=tx.price,
                    )
                )
            else:
                new_qty = pos.quantity + tx.quantity
                pos.avg_cost = (
                    pos.avg_cost * pos.quantity + tx.price * tx.quantity
                ) / new_qty
                pos.quantity = new_qty
        elif tx.tx_type == TxType.SELL and pos is not None:
            pos.quantity -= tx.quantity
