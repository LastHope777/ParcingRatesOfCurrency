"""
Сервис для получения данных об акциях через Yahoo Finance
"""

import yfinance as yf
from datetime import datetime
from typing import List, Optional

from models.asset import Stock


class StockService:
    """Сервис для получения данных об акциях"""
    
    def __init__(self):
        pass
    
    def get_stock(self, ticker: str) -> Optional[Stock]:
        """Получить данные об конкретной акции"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            
            current_price = info.get("last_price") or info.get("regularMarketPrice")
            if current_price is None:
                hist = stock.history(period="1d")
                if hist.empty:
                    return None
                current_price = hist["Close"].iloc[-1]
            
            stock_obj = Stock(
                symbol=ticker,
                name=info.get("long_name", ticker),
                price=float(current_price),
                change=info.get("regularMarketChange"),
                change_percent=info.get("regularMarketChangePercent"),
                ticker=ticker,
                open_price=info.get("open"),
                high=info.get("dayHigh"),
                low=info.get("dayLow"),
                volume=info.get("volume"),
                last_update=datetime.now()
            )
            
            return stock_obj
            
        except Exception as e:
            print(f"Ошибка получения данных акции {ticker}: {e}")
            return None
    
    def get_stocks(self, tickers: List[str]) -> List[Stock]:
        """Получить данные о выбранных акциях"""
        stocks = []
        for ticker in tickers:
            stock = self.get_stock(ticker)
            if stock:
                stocks.append(stock)
        return stocks
    
    def search_stocks(self, query: str) -> List[dict]:
        """Поиск акций по названию"""
        try:
            results = yf.Ticker(query).info
            if results:
                return [{
                    "symbol": results.get("symbol", query),
                    "name": results.get("longName", results.get("shortName", query)),
                    "exchange": results.get("exchange", "")
                }]
            return []
        except Exception as e:
            print(f"Ошибка поиска акций: {e}")
            return []
