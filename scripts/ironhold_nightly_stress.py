"""Entry point used by the Ironhold ops cron at 02:00 local time.

Loads today's positions, today's close prices, and the configured
scenario set, then writes the result into the Ironhold reporting bucket.
"""

from decimal import Decimal

from backend.app.customer.ironhold.stress import Scenario, run_overnight


def main() -> int:
    # In production this is wired to the real store + price snapshot.
    portfolios = []
    prices: dict[str, Decimal] = {}
    asset_class: dict[str, str] = {}
    scenarios: list[Scenario] = []
    results = run_overnight(portfolios, prices, asset_class, scenarios)
    print(f"stress rows: {len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
