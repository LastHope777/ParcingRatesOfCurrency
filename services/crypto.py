"""
Сервис для получения курсов криптовалют через CoinGecko API
"""

import requests
from datetime import datetime
from typing import List, Optional, Dict

from models.asset import Crypto


class CryptoService:
    """Сервис для получения данных о криптовалютах"""
    
    API_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })
    
    def get_all_prices(self, currency: str = "usd") -> Dict[str, float]:
        """Получить цены всех популярных криптовалют"""
        try:
            response = self.session.get(
                f"{self.API_URL}/coins/markets",
                params={"vs_currency": currency, "order": "market_cap_desc", "per_page": 100},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            return {item["symbol"].upper(): item["current_price"] for item in data}
            
        except Exception as e:
            print(f"Ошибка получения цен криптовалют: {e}")
            return {}
    
    def get_crypto_list(self, coin_ids: List[str], currency: str = "usd") -> List[Crypto]:
        """Получить данные о выбранных криптовалютах"""
        try:
            ids = ",".join(coin_ids)
            response = self.session.get(
                f"{self.API_URL}/coins/markets",
                params={
                    "vs_currency": currency,
                    "ids": ids,
                    "order": "market_cap_desc"
                },
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            cryptos = []
            
            for item in data:
                crypto = Crypto(
                    symbol=item["symbol"].upper(),
                    name=item["name"],
                    price=item["current_price"],
                    change=item.get("price_change_percentage_24h"),
                    change_percent=item.get("price_change_percentage_24h"),
                    coin_id=item["id"],
                    market_cap=item.get("market_cap"),
                    volume_24h=item.get("total_volume"),
                    last_update=datetime.now()
                )
                cryptos.append(crypto)
            
            return cryptos
            
        except Exception as e:
            print(f"Ошибка получения данных криптовалют: {e}")
            return []
    
    def get_crypto(self, coin_id: str, currency: str = "usd") -> Optional[Crypto]:
        """Получить данные о конкретной криптовалюте"""
        result = self.get_crypto_list([coin_id], currency)
        return result[0] if result else None
    
    def search_coins(self, query: str) -> List[Dict]:
        """Поиск криптовалют по названию"""
        try:
            response = self.session.get(
                f"{self.API_URL}/coins/list",
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            query_lower = query.lower()
            
            results = [
                coin for coin in data
                if query_lower in coin["name"].lower() or query_lower in coin["symbol"].lower()
            ][:10]
            
            return results
            
        except Exception as e:
            print(f"Ошибка поиска криптовалют: {e}")
            return []
