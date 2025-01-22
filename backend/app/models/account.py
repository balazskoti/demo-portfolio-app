from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    id: str
    name: str
    client_id: str
    base_currency: str = "USD"
    opened_at: datetime = field(default_factory=datetime.utcnow)
    closed_at: Optional[datetime] = None

    @property
    def is_active(self) -> bool:
        return self.closed_at is None
