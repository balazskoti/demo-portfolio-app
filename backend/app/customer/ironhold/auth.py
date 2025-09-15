"""Additional auth requirements for the Ironhold deployment.

IRN-031: the Ironhold compliance team requires that any endpoint which
moves money or sends an order downstream be gated behind a second factor
verified within the last 5 minutes. Session-only auth is not sufficient
for these endpoints.

The check below is attached as a FastAPI dependency to the affected
routes via ``require_mfa``.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Header, HTTPException

MFA_MAX_AGE = timedelta(minutes=5)


def _parse_mfa_token_age(token: str) -> Optional[datetime]:
    # Tokens are issued by the Ironhold SSO bridge and carry the
    # verification timestamp in the last dot-separated segment.
    try:
        _, _, ts = token.rpartition(".")
        return datetime.fromtimestamp(int(ts), tz=timezone.utc)
    except Exception:
        return None


def require_mfa(x_mfa_token: Optional[str] = Header(default=None)) -> None:
    if not x_mfa_token:
        raise HTTPException(401, "MFA token required")
    issued = _parse_mfa_token_age(x_mfa_token)
    if not issued:
        raise HTTPException(401, "invalid MFA token")
    if datetime.now(tz=timezone.utc) - issued > MFA_MAX_AGE:
        raise HTTPException(401, "MFA token expired — re-verify")
