from fastapi import APIRouter, HTTPException
from app.models.schema import PriceAlert
from app.services.crypto_monitor import crypto_monitor

router = APIRouter()

@router.post("/")
async def create_alert(alert: PriceAlert):
    success = await crypto_monitor.set_alert(
        alert.crypto,
        alert.email,
        float(alert.target_price),
        alert.above
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set alert")
    return {"success": True}
