"""Audit trail extensions for Ironhold.

Every mutating call against the API is recorded with:

- the acting user,
- the session id,
- the source IP,
- the MFA token id (if the endpoint required one),
- the request body hash.

Records are shipped to the immutable audit bucket configured in
``deployment.yaml``. Retention is 7 years, per IRN-079 (reflects
Ironhold's regulator commitment; the product default of 90 days is not
acceptable here).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

RETENTION_YEARS = 7


@dataclass
class AuditEntry:
    at: datetime
    user_id: str
    session_id: str
    source_ip: str
    route: str
    body_sha256: str
    mfa_token_id: Optional[str] = None


class AuditSink:
    """Forwarder to the immutable storage bucket."""

    def write(self, entry: AuditEntry) -> None:
        # Real implementation writes to the customer's WORM bucket.
        _ = entry
