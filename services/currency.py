"""
Сервис для получения курсов валют с сайта ЦБ РФ
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional

from models.asset import Currency


class CurrencyService:
    """Сервис для парсинга курсов валют с cbr.ru"""
    
    URL = "https://cbr.ru/currency_base/daily/"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def get_all_rates(self) -> List[Currency]:
        """Получить все курсы валют"""
        try:
            response = self.session.get(self.URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"class": "data"})
            
            if not table:
                return []
            
            currencies = []
            rows = table.find_all("tr")[1:]  # Пропускаем заголовок
            
            for row in rows:
                columns = row.find_all("td")
                if len(columns) >= 5:
                    # Column 0: numeric code, Column 1: currency code, Column 2: nominal
                    # Column 3: currency name, Column 4: rate
                    numeric_code = columns[0].text.strip()
                    code = columns[1].text.strip()  # Буквенный код (USD, EUR)
                    nominal = int(columns[2].text.strip().replace(",", ""))
                    name = columns[3].text.strip()
                    rate_str = columns[4].text.strip().replace(",", ".")
                    
                    try:
                        rate = float(rate_str)
                    except ValueError:
                        continue
                    
                    currency = Currency(
                        symbol=code,
                        name=name,
                        price=rate,
                        nominal=nominal,
                        code=code,
                        last_update=datetime.now()
                    )
                    currencies.append(currency)
            
            return currencies
            
        except Exception as e:
            print(f"Ошибка получения курсов валют: {e}")
            return []
    
    def get_currency(self, code: str) -> Optional[Currency]:
        """Получить курс конкретной валюты"""
        all_rates = self.get_all_rates()
        for currency in all_rates:
            if currency.code.upper() == code.upper():
                return currency
        return None
    
    def get_currencies(self, codes: List[str]) -> List[Currency]:
        """Получить курсы выбранных валют"""
        all_rates = self.get_all_rates()
        codes_upper = [c.upper() for c in codes]
        return [c for c in all_rates if c.code.upper() in codes_upper]
