from backend.config  import settings
import aiohttp
from .base import BaseAggregator
from typing import Dict, Any
import json

class CowSwapAPI(BaseAggregator):
    def __init__(self):
        self.base_url = "https://api.cow.fi/mainnet/api/v1"
        
    def _get_token_address(self, token: str) -> str:
        """Get token address from symbol"""
        address = settings.TOKEN_ADDRESSES.get(token.upper())
        if not address:
            raise ValueError(f"Token {token} not supported")
        return address
    
    async def get_quote(self, input_token: str, output_token: str, amount: float) -> Dict[str, Any]:
        try:
            input_token = self._validate_token(input_token)
            output_token = self._validate_token(output_token)
            amount = self._validate_amount(amount)
            
            # Convert amount to wei
            amount_wei = int(amount * 10**18)
            
            # Get token addresses
            from_token = self._get_token_address(input_token)
            to_token = self._get_token_address(output_token)
            
            async with aiohttp.ClientSession() as session:
                quote_url = f"{self.base_url}/quote"
                payload = {
                    "sellToken": from_token,
                    "buyToken": to_token,
                    "sellAmountBeforeFee": str(amount_wei),
                    "kind": "sell"
                }
                
                async with session.post(quote_url, json=payload) as response:
                    if response.status != 200:
                        error_data = await response.text()
                        raise Exception(f"CowSwap API error: {error_data}")
                    
                    data = await response.json()
                    
                    return {
                        "price": float(data["buyAmount"]) / 10**18,
                        "slippage": float(data.get("slippagePercentage", 0.5)),
                        "gas_estimate": int(data.get("estimatedGas", 50000)),
                        "execution_time": int(data.get("validTo", 30))  # Time until quote expiry
                    }
                    
        except Exception as e:
            print(f"CowSwap API error: {str(e)}")
            return None