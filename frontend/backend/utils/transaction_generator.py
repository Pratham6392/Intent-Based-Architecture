from typing import Dict, Any
from .token_validator import TokenValidator

class TransactionGenerator:
    @staticmethod
    def generate_transaction_data(quote: Dict[str, Any], from_address: str) -> Dict[str, Any]:
        """Generate transaction data for the selected quote"""
        if not quote or "quote" not in quote:
            raise ValueError("Invalid quote data")
            
        # Extract necessary information
        provider = quote["provider"]
        quote_data = quote["quote"]
        
        # Basic transaction template
        transaction = {
            "from": from_address,
            "gasLimit": str(int(quote_data.get("gas_estimate", 50000) * 1.1)),  # Add 10% buffer
            "value": "0",  # For token transfers
            "data": "0x",  # Placeholder for transaction data
        }
        
        # Add provider-specific data
        if provider == "1inch":
            transaction["to"] = "0x1111111254EEB25477B68fb85Ed929f73A960582"  # 1inch router
        elif provider == "uniswap":
            transaction["to"] = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"  # Uniswap router
        elif provider == "cowswap":
            transaction["to"] = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"  # CoW Protocol
            
        return transaction