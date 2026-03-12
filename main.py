"""
Asset Tracker - Трекер финансовых активов
Валюты | Криптовалюты | Акции

Версия: 1.0.0
"""

import sys
import io

# Исправление кодировки для Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from services.currency import CurrencyService
from services.crypto import CryptoService
from services.stocks import StockService
from database.db_manager import DatabaseManager
from config import DEFAULT_CURRENCIES, DEFAULT_CRYPTO, DEFAULT_STOCKS


def main():
    """Основная функция - демонстрация работы сервисов"""
    print("=" * 50)
    print("Asset Tracker - Демонстрация работы")
    print("=" * 50)
    
    # Инициализация базы данных
    db = DatabaseManager()
    
    # === Валюты ===
    print("\nКурсы валют ЦБ РФ:")
    print("-" * 30)
    
    currency_service = CurrencyService()
    currencies = currency_service.get_currencies(DEFAULT_CURRENCIES)
    
    for curr in currencies:
        print(f"  {curr.code}: {curr.price:.2f} RUB (номинал: {curr.nominal})")
        db.add_favorite("currency", curr.code, curr.name)
    
    # === Криптовалюты ===
    print("\nКурсы криптовалют:")
    print("-" * 30)
    
    crypto_service = CryptoService()
    cryptos = crypto_service.get_crypto_list(DEFAULT_CRYPTO)
    
    for crypto in cryptos:
        change_str = f"{crypto.change_percent:+.2f}%" if crypto.change_percent else "N/A"
        print(f"  {crypto.symbol}: ${crypto.price:.2f} ({change_str})")
        db.add_favorite("crypto", crypto.coin_id, crypto.name)
    
    # === Акции ===
    print("\nКотировки акций:")
    print("-" * 30)
    
    stock_service = StockService()
    stocks = stock_service.get_stocks(DEFAULT_STOCKS)
    
    for stock in stocks:
        change_str = f"{stock.change_percent:+.2f}%" if stock.change_percent else "N/A"
        print(f"  {stock.symbol}: ${stock.price:.2f} ({change_str})")
        db.add_favorite("stocks", stock.ticker, stock.name)
    
    # === Избранные активы ===
    print("\nИзбранные активы (сохранено в БД):")
    print("-" * 30)
    
    favorites = db.get_favorites()
    for fav in favorites:
        print(f"  [{fav['asset_type']}] {fav['symbol']} - {fav['name']}")
    
    print("\n" + "=" * 50)
    print("Демонстрация завершена!")
    print("Данные сохранены в assets.db")
    print("=" * 50)
    
    db.close()


if __name__ == "__main__":
    main()
