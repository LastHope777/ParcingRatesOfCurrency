"""
Менеджер базы данных для хранения настроек и избранных активов
"""

import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path


class DatabaseManager:
    """Управление SQLite базой данных"""
    
    def __init__(self, db_path: str = "assets.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Подключение к базе данных"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
    
    def _create_tables(self):
        """Создание таблиц"""
        cursor = self.conn.cursor()
        
        # Таблица настроек
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        # Таблица избранных активов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(asset_type, symbol)
            )
        """)
        
        # Таблица истории обновлений
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS update_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                price REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        
        # Инициализация настроек по умолчанию
        self._init_default_settings()
    
    def _init_default_settings(self):
        """Инициализация настроек по умолчанию"""
        defaults = {
            "theme": "dark",
            "refresh_interval": "60",
            "default_currency": "RUB",
            "show_currency": "true",
            "show_crypto": "true",
            "show_stocks": "true"
        }
        
        cursor = self.conn.cursor()
        for key, value in defaults.items():
            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                (key, value)
            )
        self.conn.commit()
    
    # === Настройки ===
    
    def get_setting(self, key: str, default: str = "") -> str:
        """Получить настройку"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default
    
    def set_setting(self, key: str, value: str):
        """Установить настройку"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()
    
    def get_all_settings(self) -> Dict[str, str]:
        """Получить все настройки"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        return {row["key"]: row["value"] for row in cursor.fetchall()}
    
    # === Избранные активы ===
    
    def add_favorite(self, asset_type: str, symbol: str, name: str = "") -> bool:
        """Добавить актив в избранное"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO favorites (asset_type, symbol, name) VALUES (?, ?, ?)",
                (asset_type, symbol, name)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления в избранное: {e}")
            return False
    
    def remove_favorite(self, asset_type: str, symbol: str) -> bool:
        """Удалить актив из избранного"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM favorites WHERE asset_type = ? AND symbol = ?",
                (asset_type, symbol)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка удаления из избранного: {e}")
            return False
    
    def get_favorites(self, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Получить избранные активы"""
        cursor = self.conn.cursor()
        
        if asset_type:
            cursor.execute(
                "SELECT asset_type, symbol, name, created_at FROM favorites WHERE asset_type = ?",
                (asset_type,)
            )
        else:
            cursor.execute("SELECT asset_type, symbol, name, created_at FROM favorites")
        
        return [dict(row) for row in cursor.fetchall()]
    
    def is_favorite(self, asset_type: str, symbol: str) -> bool:
        """Проверить, есть ли актив в избранном"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT 1 FROM favorites WHERE asset_type = ? AND symbol = ?",
            (asset_type, symbol)
        )
        return cursor.fetchone() is not None
    
    # === История обновлений ===
    
    def log_price(self, asset_type: str, symbol: str, price: float):
        """Записать цену в историю"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO update_history (asset_type, symbol, price) VALUES (?, ?, ?)",
            (asset_type, symbol, price)
        )
        self.conn.commit()
    
    def get_price_history(self, asset_type: str, symbol: str, limit: int = 100) -> List[Dict]:
        """Получить историю цен"""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT price, timestamp FROM update_history 
               WHERE asset_type = ? AND symbol = ? 
               ORDER BY timestamp DESC LIMIT ?""",
            (asset_type, symbol, limit)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Закрыть соединение"""
        if self.conn:
            self.conn.close()
            self.conn = None
