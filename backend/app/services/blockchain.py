from decimal import Decimal
import httpx
from app.models.schema import AddressBalance, Transaction

class BlockchainService:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.base_url = "https://blockchain.info"
    
    async def get_address_balance(self, address: str) -> AddressBalance:
        balance_url = f"{self.base_url}/balance?active={address}"
        txs_url = f"{self.base_url}/rawaddr/{address}"
        
        async with httpx.AsyncClient() as client:
            balance_resp = await client.get(balance_url)
            balance_data = balance_resp.json()
            
            txs_resp = await client.get(txs_url)
            txs_data = txs_resp.json()
            
            return AddressBalance(
                address=address,
                balance=Decimal(balance_data[address]['final_balance']) / Decimal('100000000'),
                transactions=self._parse_transactions(txs_data['txs'][:10])
            )
    
    def _parse_transactions(self, txs):
        return [
            Transaction(
                hash=tx['hash'],
                time=tx['time'],
                amount=Decimal(sum(out['value'] for out in tx['out'])) / Decimal('100000000'),
                amount_usd=Decimal('0'),  # To be calculated with current price
                from_addresses=[inp.get('prev_out', {}).get('addr', 'Unknown') for inp in tx.get('inputs', [])],
                to_addresses=[out.get('addr', 'Unknown') for out in tx.get('out', [])]
            )
            for tx in txs
        ]
