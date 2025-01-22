from dataclasses import dataclass, field
from typing import List

from .position import Position


@dataclass
class Portfolio:
    id: str
    account_id: str
    name: str
    strategy: str = "balanced"
    positions: List[Position] = field(default_factory=list)

    def total_quantity(self) -> float:
        return sum(p.quantity for p in self.positions)
