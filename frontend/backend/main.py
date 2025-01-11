from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from backend.aggregators.cowswap import CowSwapAPI
from backend.aggregators.uniswapx import UniswapXAPI
from backend.aggregators.oneinch import OneInchAPI
from backend.utils.rateLimiter import RateLimiter
from backend.utils.quote_comparator import QuoteComparator

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize aggregator APIs
cowswap = CowSwapAPI()
uniswapx = UniswapXAPI()
oneinch = OneInchAPI()

# Initialize rate limiter
rate_limiter = RateLimiter()

class SwapRequest(BaseModel):
    input_token: str
    output_token: str
    amount: float
    preference: Optional[str] = "best_price"  # best_price, lowest_slippage, fastest

@app.post("/api/quotes")
async def get_quotes(request: SwapRequest):
    try:
        # Apply rate limiting
        if not rate_limiter.allow_request():
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # Gather quotes from different aggregators
        quotes = []
        
        # Get CowSwap quote
        cowswap_quote = await cowswap.get_quote(
            request.input_token,
            request.output_token,
            request.amount
        )
        if cowswap_quote:
            quotes.append({"provider": "cowswap", "quote": cowswap_quote})

        # Get UniswapX quote
        uniswapx_quote = await uniswapx.get_quote(
            request.input_token,
            request.output_token,
            request.amount
        )
        if uniswapx_quote:
            quotes.append({"provider": "uniswapx", "quote": uniswapx_quote})

        # Get 1inch quote
        oneinch_quote = await oneinch.get_quote(
            request.input_token,
            request.output_token,
            request.amount
        )
        if oneinch_quote:
            quotes.append({"provider": "1inch", "quote": oneinch_quote})

        # Compare quotes based on user preference
        quote_comparator = QuoteComparator()
        best_quote = quote_comparator.get_best_quote(quotes, request.preference)

        return {
            "quotes": quotes,
            "best_quote": best_quote
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)