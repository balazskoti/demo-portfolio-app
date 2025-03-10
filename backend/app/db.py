"""Placeholder in-memory store. Replaced by SQLAlchemy session in prod."""

from typing import Dict, List

from .models import Account, Portfolio, Transaction


class Store:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.portfolios: Dict[str, Portfolio] = {}
        self.transactions: List[Transaction] = []


store = Store()
