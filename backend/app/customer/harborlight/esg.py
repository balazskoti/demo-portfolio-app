"""ESG screening filter.

Harborlight offers a *values-based* portfolio option. Clients can
exclude instruments that fail the house ESG screen; a screened account
will not be allowed to buy an instrument on the exclusion list, and a
compliance flag is raised if one is held due to a corporate action
(HBL-048).

The screen is sourced from the Sustainalytics feed and refreshed nightly.
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Set


class ScreenCategory(str, Enum):
    TOBACCO = "tobacco"
    CONTROVERSIAL_WEAPONS = "controversial_weapons"
    THERMAL_COAL = "thermal_coal"
    GAMBLING = "gambling"
    ADULT_ENTERTAINMENT = "adult_entertainment"


@dataclass
class ScreenPolicy:
    account_id: str
    excluded: Set[ScreenCategory]
    min_overall_score: Decimal = Decimal("0")


class EsgUniverse:
    def __init__(self, exclusions_by_category, scores):
        # exclusions_by_category: dict[ScreenCategory, set[str]]
        # scores: dict[instrument_id, Decimal]  (0–100)
        self._by_cat = exclusions_by_category
        self._scores = scores

    def is_blocked(self, instrument_id: str, policy: ScreenPolicy) -> bool:
        for cat in policy.excluded:
            if instrument_id in self._by_cat.get(cat, set()):
                return True
        score = self._scores.get(instrument_id, Decimal("0"))
        if score < policy.min_overall_score:
            return True
        return False
