"""Tax-lot tracking for the Harborlight deployment.

Harborlight's advisors need realised-gain numbers for every sell, which
means the platform has to track individual purchase lots rather than a
single average cost per position (HBL-013).

Three cost-basis methods are supported:

- ``FIFO`` — earliest lots are relieved first. The default.
- ``LIFO`` — most recent lots first.
- ``HIFO`` — the highest-cost lot still open is relieved first. Used for
  tax-loss-harvesting workflows.

Each account has a method on file; it can be overridden on a per-sell
basis when the advisor flags a specific lot.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Tuple


class CostBasisMethod(str, Enum):
    FIFO = "fifo"
    LIFO = "lifo"
    HIFO = "hifo"


@dataclass
class Lot:
    lot_id: str
    opened_at: datetime
    quantity: Decimal
    cost_basis: Decimal  # per-unit
    closed_quantity: Decimal = Decimal("0")

    @property
    def remaining(self) -> Decimal:
        return self.quantity - self.closed_quantity


@dataclass
class RealisedGain:
    lot_id: str
    quantity: Decimal
    proceeds: Decimal
    cost_basis: Decimal

    @property
    def gain(self) -> Decimal:
        return self.proceeds - self.cost_basis


@dataclass
class LotBook:
    instrument_id: str
    lots: List[Lot] = field(default_factory=list)

    def open_lot(self, lot: Lot) -> None:
        self.lots.append(lot)

    def relieve(
        self,
        quantity: Decimal,
        price: Decimal,
        method: CostBasisMethod,
        preferred_lot_id: Optional[str] = None,
    ) -> List[RealisedGain]:
        order = self._order(method, preferred_lot_id)
        remaining = quantity
        gains: List[RealisedGain] = []
        for lot in order:
            if remaining <= 0:
                break
            take = min(lot.remaining, remaining)
            if take <= 0:
                continue
            lot.closed_quantity += take
            remaining -= take
            gains.append(
                RealisedGain(
                    lot_id=lot.lot_id,
                    quantity=take,
                    proceeds=take * price,
                    cost_basis=take * lot.cost_basis,
                )
            )
        if remaining > 0:
            raise ValueError("insufficient open lots to satisfy sell")
        return gains

    def _order(
        self, method: CostBasisMethod, preferred: Optional[str]
    ) -> List[Lot]:
        open_lots = [l for l in self.lots if l.remaining > 0]
        if preferred:
            pick = [l for l in open_lots if l.lot_id == preferred]
            rest = [l for l in open_lots if l.lot_id != preferred]
            return pick + self._by_method(rest, method)
        return self._by_method(open_lots, method)

    @staticmethod
    def _by_method(
        lots: List[Lot], method: CostBasisMethod
    ) -> List[Lot]:
        if method == CostBasisMethod.FIFO:
            return sorted(lots, key=lambda l: l.opened_at)
        if method == CostBasisMethod.LIFO:
            return sorted(lots, key=lambda l: l.opened_at, reverse=True)
        if method == CostBasisMethod.HIFO:
            return sorted(lots, key=lambda l: l.cost_basis, reverse=True)
        raise ValueError(f"unknown method: {method}")
