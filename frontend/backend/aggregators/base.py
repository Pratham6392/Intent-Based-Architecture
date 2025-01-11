from abc import ABC, abstractmethod

class BaseAggregator(ABC):
    @abstractmethod
    async def get_quote(self, input_token: str, output_token: str, amount: float):
        pass

    def _validate_token(self, token: str):
        # Basic token validation
        if not token or not isinstance(token, str):
            raise ValueError("Invalid token format")
        return token.upper()

    def _validate_amount(self, amount: float):
        if not amount or amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return amount