from ..config import settings
import aiohttp
from .base import BaseAggregator
from typing import Dict, Any
import json

class UniswapXAPI(BaseAggregator):
    def __init__(self):
        self.base_url = "https://api.uniswap.org/v1"
        self.headers = {
            "Origin": "https://app.uniswap.org",
            "Content-Type": "application/json"
        }
    
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
                    "tokenInAddress": from_token,
                    "tokenOutAddress": to_token,
                    "amount": str(amount_wei),
                    "type": "exactIn"
                }
                
                async with session.post(quote_url, headers=self.headers, json=payload) as response:
                    if response.status != 200:
                        error_data = await response.text()
                        raise Exception(f"UniswapX API error: {error_data}")
                    
                    data = await response.json()
                    
                    return {
                        "price": float(data["quote"]["amount"]) / 10**18,
                        "slippage": float(data["quote"].get("slippage", 0.5)),
                        "gas_estimate": int(data["quote"].get("gasEstimate", 45000)),
                        "execution_time": 25  # Estimated execution time
                    }
                    
        except Exception as e:
            print(f"UniswapX API error: {str(e)}")
            return None