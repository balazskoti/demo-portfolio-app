"""Trade-execution endpoints for the Ironhold deployment.

Every route here is gated behind MFA in addition to the regular session
check (IRN-031).
"""

from fastapi import APIRouter, Depends

from ...api.auth import current_user
from .auth import require_mfa

router = APIRouter(
    prefix="/trading",
    dependencies=[Depends(require_mfa)],
)


@router.post("/orders")
def place_order(user: str = Depends(current_user)):
    # Order placement is routed through the Goldcrest prime broker
    # adapter in a later commit.
    return {"status": "accepted", "submitted_by": user}


@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str, user: str = Depends(current_user)):
    return {"status": "cancelled", "order_id": order_id}
