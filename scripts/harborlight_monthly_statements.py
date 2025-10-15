"""Cron entry point for Harborlight monthly statements.

Runs at 06:00 America/New_York on the first business day of the month.
Generates one PDF per household and pushes it to the secure portal.
"""

from datetime import date

from backend.app.customer.harborlight.statements import build


def main() -> int:
    period_end = date.today().replace(day=1)
    # period_start = first of previous month …
    print(f"(stub) would generate statements ending {period_end}")
    _ = build
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
