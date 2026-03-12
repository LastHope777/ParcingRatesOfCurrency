"""
Сервисы для получения данных об активах
"""

from .currency import CurrencyService
from .crypto import CryptoService
from .stocks import StockService

__all__ = ["CurrencyService", "CryptoService", "StockService"]
