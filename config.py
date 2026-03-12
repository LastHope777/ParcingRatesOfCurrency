"""
Конфигурация приложения Asset Tracker
"""

# Настройки приложения
APP_NAME = "Asset Tracker 💰"
APP_VERSION = "1.0.0"
APP_WIDTH = 1200
APP_HEIGHT = 800

# Цветовая тема
THEME = "dark"  # dark | light
COLOR_PRIMARY = "#2563eb"

# Интервалы обновления (в секундах)
REFRESH_INTERVAL = {
    "currency": 300,    # 5 минут
    "crypto": 60,       # 1 минута
    "stocks": 30        # 30 секунд
}

# API настройки
API_ENDPOINTS = {
    "cbr": "https://cbr.ru/currency_base/daily/",
    "coingecko": "https://api.coingecko.com/api/v3",
}

# Валюты по умолчанию
DEFAULT_CURRENCIES = ["USD", "EUR", "CNY"]

# Криптовалюты по умолчанию
DEFAULT_CRYPTO = ["bitcoin", "ethereum", "binancecoin"]

# Акции по умолчанию
DEFAULT_STOCKS = ["AAPL", "GOOGL", "MSFT", "TSLA"]
