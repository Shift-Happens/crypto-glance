from pydantic import BaseModel, EmailStr
from typing import List, Optional
from decimal import Decimal

class Transaction(BaseModel):
    hash: str
    time: str
    amount: Decimal
    amount_usd: Decimal
    from_addresses: List[str]
    to_addresses: List[str]

class AddressBalance(BaseModel):
    address: str
    balance: Decimal
    transactions: List[Transaction]
    error: Optional[str] = None

class PriceAlert(BaseModel):
    crypto: str
    email: EmailStr
    target_price: Decimal
    above: bool = True
