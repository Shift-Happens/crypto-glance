from fastapi import APIRouter, HTTPException
from app.services.crypto_monitor import crypto_monitor

router = APIRouter()

@router.get("/")
async def get_prices():
    prices = await crypto_monitor.get_crypto_prices()
    if prices is None:
        raise HTTPException(status_code=500, detail="Failed to fetch prices")
    return prices
