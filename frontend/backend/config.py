

from typing import ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ONEINCH_API_KEY: str = "8A0gJKa1wgn1COsr7jE3wee34z0cN3vK"
    COWSWAP_API_KEY: str = ""  # if required
    UNISWAP_API_KEY: str = ""  # if required
    
     # Token address mappings (class-level constant)
    TOKEN_ADDRESSES: ClassVar[dict[str, str]] = {
        "ETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    }

settings = Settings()