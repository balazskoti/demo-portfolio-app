"""Session-based authentication.

Advisors sign in with username + password. The server issues a signed
session cookie; each request validates the cookie against the session
store before the route handler runs.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Cookie, Depends, HTTPException, Request
from jose import jwt

from ..config import settings

ALGO = "HS256"
SESSION_TTL = timedelta(hours=8)


def issue_session(user_id: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + SESSION_TTL).timestamp()),
    }
    return jwt.encode(payload, settings.session_secret, algorithm=ALGO)


def current_user(
    request: Request, session: Optional[str] = Cookie(default=None)
) -> str:
    if not session:
        raise HTTPException(401, "not authenticated")
    try:
        payload = jwt.decode(session, settings.session_secret, algorithms=[ALGO])
    except Exception:
        raise HTTPException(401, "invalid session")
    return payload["sub"]


def require_role(role: str):
    def _dep(user: str = Depends(current_user)):
        # Role resolution from a user directory; stubbed for now.
        return user

    return _dep
