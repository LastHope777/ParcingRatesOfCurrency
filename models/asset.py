"""
Модели данных для Asset Tracker
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Asset:
    """Базовый класс актива"""
    symbol: str
    name: str
    price: float
    change: Optional[float] = None  # Изменение в %
    change_percent: Optional[float] = None
    last_update: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": self.price,
            "change": self.change,
            "change_percent": self.change_percent,
            "last_update": self.last_update.isoformat() if self.last_update else None
        }


@dataclass
class Currency(Asset):
    """Валюта"""
    code: str = ""
    nominal: int = 1  # Номинал (например, 10 для некоторых валют)
    source: str = "CBR"


@dataclass
class Crypto(Asset):
    """Криптовалюта"""
    coin_id: str = ""
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    source: str = "CoinGecko"


@dataclass
class Stock(Asset):
    """Акция"""
    ticker: str = ""
    open_price: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[int] = None
    source: str = "Yahoo Finance"
