from fastapi import APIRouter, HTTPException
from app.models.schema import AddressBalance
from app.services.blockchain import BlockchainService

router = APIRouter()
blockchain_service = BlockchainService()

@router.get("/{address}", response_model=AddressBalance)
async def get_address_info(address: str):
    try:
        return await blockchain_service.get_address_balance(address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
