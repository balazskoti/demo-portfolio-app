"""Goldcrest prime broker integration.

Ironhold's prime broker is Goldcrest. Positions, cash balances and
executed trades flow from Goldcrest's SFTP drop three times a day; this
module consumes those files and reconciles them against our internal
state (IRN-044).

This is currently a stubbed adapter — file parsing is real, but the SFTP
client lives behind an interface that is mocked in tests and replaced by
a paramiko-backed implementation at deploy time.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable, List, Protocol


@dataclass
class GoldcrestPosition:
    account_code: str
    instrument: str
    quantity: Decimal
    avg_cost: Decimal
    as_of: datetime


class SftpClient(Protocol):
    def list(self, path: str) -> List[str]: ...
    def read(self, path: str) -> bytes: ...


class GoldcrestFeed:
    # Drop path is assigned per-environment by deployment config.
    DROP_PATH = "/outbound/meridian/positions"

    def __init__(self, sftp: SftpClient):
        self._sftp = sftp

    def latest_positions(self) -> Iterable[GoldcrestPosition]:
        for fname in sorted(self._sftp.list(self.DROP_PATH)):
            if not fname.endswith(".csv"):
                continue
            yield from self._parse(self._sftp.read(f"{self.DROP_PATH}/{fname}"))

    def _parse(self, blob: bytes) -> Iterable[GoldcrestPosition]:
        text = blob.decode("utf-8")
        lines = [l for l in text.splitlines() if l.strip()]
        for line in lines[1:]:  # skip header
            account, instrument, qty, cost, ts = line.split(",")
            yield GoldcrestPosition(
                account_code=account,
                instrument=instrument,
                quantity=Decimal(qty),
                avg_cost=Decimal(cost),
                as_of=datetime.fromisoformat(ts),
            )
