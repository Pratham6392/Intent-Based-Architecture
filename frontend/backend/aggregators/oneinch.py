from ..config import settings
import aiohttp
from .base import BaseAggregator
from typing import Dict, Any
import json

class OneInchAPI(BaseAggregator):
    def __init__(self):
        self.base_url = "https://api.1inch.io/v5.0/1"  # 1 for Ethereum mainnet
        self.headers = {
            "Authorization": f"Bearer {settings.ONEINCH_API_KEY}",
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
            
            # Convert amount to wei (assuming 18 decimals)
            amount_wei = int(amount * 10**18)
            
            # Get token addresses
            from_token = self._get_token_address(input_token)
            to_token = self._get_token_address(output_token)
            
            async with aiohttp.ClientSession() as session:
                # Get quote from 1inch
                quote_url = f"{self.base_url}/quote"
                params = {
                    "fromTokenAddress": from_token,
                    "toTokenAddress": to_token,
                    "amount": str(amount_wei)
                }
                
                async with session.get(quote_url, headers=self.headers, params=params) as response:
                    if response.status != 200:
                        error_data = await response.text()
                        raise Exception(f"1inch API error: {error_data}")
                    
                    data = await response.json()
                    
                    # Extract relevant information
                    return {
                        "price": float(data["toTokenAmount"]) / 10**18,
                        "slippage": float(data.get("estimatedGas", 0)) / 100,
                        "gas_estimate": int(data.get("estimatedGas", 0)),
                        "execution_time": 30  # Estimated execution time in seconds
                    }
                    
        except Exception as e:
            print(f"1inch API error: {str(e)}")
            return None