import pytest
from ..utils.quote_comparator import QuoteComparator
from ..utils.gas_estimator import GasEstimator

@pytest.fixture
def sample_quotes():
    return [
        {
            "provider": "uniswap",
            "quote": {
                "price": 1000.0,
                "slippage": 0.1,
                "gas_estimate": 50000,
                "execution_time": 30
            }
        },
        {
            "provider": "1inch",
            "quote": {
                "price": 995.0,
                "slippage": 0.2,
                "gas_estimate": 55000,
                "execution_time": 35
            }
        },
        {
            "provider": "cowswap",
            "quote": {
                "price": 1005.0,
                "slippage": 0.15,
                "gas_estimate": 45000,
                "execution_time": 25
            }
        }
    ]

@pytest.mark.asyncio
async def test_best_price_preference(sample_quotes):
    comparator = QuoteComparator()
    best_quote = await comparator.get_best_quote(sample_quotes, "best_price")
    assert best_quote["provider"] == "cowswap"  # Highest price

@pytest.mark.asyncio
async def test_lowest_slippage_preference(sample_quotes):
    comparator = QuoteComparator()
    best_quote = await comparator.get_best_quote(sample_quotes, "lowest_slippage")
    assert best_quote["provider"] == "uniswap"  # Lowest slippage

@pytest.mark.asyncio
async def test_fastest_preference(sample_quotes):
    comparator = QuoteComparator()
    best_quote = await comparator.get_best_quote(sample_quotes, "fastest")
    assert best_quote["provider"] == "cowswap"  # Lowest execution time

@pytest.mark.asyncio
async def test_gas_estimation():
    estimator = GasEstimator()
    gas_prices = await estimator.get_gas_price()
    assert "safe_low" in gas_prices
    assert "standard" in gas_prices
    assert "fast" in gas_prices

@pytest.mark.asyncio
async def test_empty_quotes():
    comparator = QuoteComparator()
    best_quote = await comparator.get_best_quote([], "best_price")
    assert best_quote is None