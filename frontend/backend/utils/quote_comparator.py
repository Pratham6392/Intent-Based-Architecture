from typing import List, Dict, Any

class QuoteComparator:
    def get_best_quote(self, quotes: List[Dict[str, Any]], preference: str = "best_price") -> Dict[str, Any]:
        if not quotes:
            return None

        if preference == "best_price":
            return self._get_best_price_quote(quotes)
        elif preference == "lowest_slippage":
            return self._get_lowest_slippage_quote(quotes)
        elif preference == "fastest":
            return self._get_fastest_execution_quote(quotes)
        else:
            return self._get_best_price_quote(quotes)  # Default to best price

    def _get_best_price_quote(self, quotes: List[Dict[str, Any]]) -> Dict[str, Any]:
        return max(quotes, key=lambda x: x["quote"]["price"])

    def _get_lowest_slippage_quote(self, quotes: List[Dict[str, Any]]) -> Dict[str, Any]:
        return min(quotes, key=lambda x: x["quote"]["slippage"])

    def _get_fastest_execution_quote(self, quotes: List[Dict[str, Any]]) -> Dict[str, Any]:
        return min(quotes, key=lambda x: x["quote"]["execution_time"])