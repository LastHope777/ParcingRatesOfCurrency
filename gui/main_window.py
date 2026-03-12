"""
Главное окно приложения Asset Tracker
"""

import customtkinter as ctk
from typing import Dict, List
import threading

from models.asset import Currency, Crypto, Stock
from services.currency import CurrencyService
from services.crypto import CryptoService
from services.stocks import StockService
from database.db_manager import DatabaseManager
from gui.widgets import AssetWidget
from gui.settings import SettingsWindow
from config import APP_NAME, APP_VERSION, APP_WIDTH, APP_HEIGHT, DEFAULT_CURRENCIES


class MainWindow(ctk.CTk):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(1000, 700)
        
        # Инициализация сервисов
        self.db = DatabaseManager()
        self.currency_service = CurrencyService()
        self.crypto_service = CryptoService()
        self.stock_service = StockService()
        
        # Настройка темы
        self._apply_theme()
        
        # Создание интерфейса
        self._create_sidebar()
        self._create_main_area()
        
        # Данные
        self.assets_data: Dict[str, List] = {
            "currency": [],
            "crypto": [],
            "stocks": []
        }
        
        # Загрузка данных
        self._load_data()
        
        # Обработчик закрытия
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _apply_theme(self):
        """Применение темы из настроек"""
        theme = self.db.get_setting("theme", "dark")
        if theme == "system":
            ctk.set_appearance_mode("System")
        else:
            ctk.set_appearance_mode(theme)
        
        ctk.set_default_color_theme("blue")
    
    def _create_sidebar(self):
        """Создание боковой панели"""
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        # Логотип
        logo = ctk.CTkLabel(
            sidebar,
            text="💰 Asset\nTracker",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        logo.pack(pady=30)
        
        # Кнопки навигации
        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10)
        
        self.btn_currency = self._create_nav_button(
            nav_frame, "💱 Валюты", self._show_currency, pack=True
        )
        self.btn_crypto = self._create_nav_button(
            nav_frame, "₿ Криптовалюты", self._show_crypto, pack=True
        )
        self.btn_stocks = self._create_nav_button(
            nav_frame, "📈 Акции", self._show_stocks, pack=True
        )
        self.btn_all = self._create_nav_button(
            nav_frame, "📊 Всё", self._show_all, pack=True
        )
        
        # Разделитель
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="gray")
        separator.pack(fill="x", pady=20, padx=10)
        
        # Кнопка настроек
        settings_btn = ctk.CTkButton(
            sidebar,
            text="⚙️ Настройки",
            command=self._open_settings,
            fg_color="transparent",
            border_width=1,
            hover_color="#3b82f6"
        )
        settings_btn.pack(pady=10, padx=10)
        
        # Кнопка обновления
        refresh_btn = ctk.CTkButton(
            sidebar,
            text="🔄 Обновить",
            command=self._load_data,
            hover_color="#22c55e"
        )
        refresh_btn.pack(pady=10, padx=10)
        
        # Активные виджеты
        ctk.CTkLabel(
            sidebar,
            text="Избранное ⭐",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(20, 10))
        
        self.favorites_frame = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        self.favorites_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Статус бар
        self.status_label = ctk.CTkLabel(
            sidebar,
            text="Готов",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.status_label.pack(side="bottom", pady=10)
    
    def _create_nav_button(self, parent, text, command, pack=False):
        """Создание кнопки навигации"""
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color="transparent",
            anchor="w",
            hover_color="#3b82f6"
        )
        if pack:
            btn.pack(fill="x", pady=5)
        return btn
    
    def _create_main_area(self):
        """Создание основной области"""
        # Верхняя панель
        top_bar = ctk.CTkFrame(self, height=60, corner_radius=0)
        top_bar.pack(side="top", fill="x")
        top_bar.pack_propagate(False)
        
        title = ctk.CTkLabel(
            top_bar,
            text="Обзор активов",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left", padx=20, pady=20)
        
        self.last_update_label = ctk.CTkLabel(
            top_bar,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.last_update_label.pack(side="right", padx=20, pady=20)
        
        # Основная область с прокруткой
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.pack(side="top", fill="both", expand=True)
        
        # Контейнеры для типов активов
        self.currency_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.crypto_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.stocks_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
    
    def _load_data(self):
        """Загрузка данных о активах"""
        self.status_label.configure(text="Загрузка...")
        
        def fetch_data():
            try:
                # Валюты
                self.assets_data["currency"] = self.currency_service.get_currencies(
                    DEFAULT_CURRENCIES
                )
                
                # Криптовалюты
                self.assets_data["crypto"] = self.crypto_service.get_crypto_list(
                    ["bitcoin", "ethereum", "binancecoin", "solana", "ripple"]
                )
                
                # Акции
                self.assets_data["stocks"] = self.stock_service.get_stocks(
                    ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
                )
                
                # Обновление GUI в главном потоке
                self.after(0, self._update_gui)
                
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self.after(0, lambda: self.status_label.configure(text="Ошибка!"))
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=fetch_data, daemon=True)
        thread.start()
    
    def _update_gui(self):
        """Обновление GUI"""
        from datetime import datetime
        
        # Очистка фреймов
        for frame in [self.currency_frame, self.crypto_frame, self.stocks_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        
        # Создание виджетов
        self._create_asset_widgets(
            self.currency_frame,
            self.assets_data["currency"],
            "currency"
        )
        self._create_asset_widgets(
            self.crypto_frame,
            self.assets_data["crypto"],
            "crypto"
        )
        self._create_asset_widgets(
            self.stocks_frame,
            self.assets_data["stocks"],
            "stocks"
        )
        
        # Обновление избранного
        self._update_favorites()
        
        # Обновление метки времени
        now = datetime.now().strftime("%H:%M:%S")
        self.last_update_label.configure(text=f"Обновлено: {now}")
        self.status_label.configure(text="Готов")
        
        # Показ текущей вкладки
        current = self._get_current_view()
        if current == "currency":
            self._show_currency()
        elif current == "crypto":
            self._show_crypto()
        elif current == "stocks":
            self._show_stocks()
        else:
            self._show_all()
    
    def _create_asset_widgets(self, parent, assets, asset_type):
        """Создание виджетов активов"""
        if not assets:
            ctk.CTkLabel(
                parent,
                text="Нет данных",
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Заголовок секции
        titles = {
            "currency": "💱 Валюты",
            "crypto": "₿ Криптовалюты",
            "stocks": "📈 Акции"
        }
        
        ctk.CTkLabel(
            parent,
            text=titles.get(asset_type, ""),
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        # Сетка для виджетов
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="x")
        
        for i, asset in enumerate(assets):
            row = i // 3
            col = i % 3
            
            is_fav = self.db.is_favorite(asset_type, getattr(asset, 'code', getattr(asset, 'symbol', '')))
            
            widget = AssetWidget(
                grid_frame,
                asset=asset,
                on_toggle_favorite=lambda a, f, t=asset_type: self._toggle_favorite(t, a, f),
                is_favorite=is_fav,
                corner_radius=10
            )
            widget.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(2, weight=1)
    
    def _toggle_favorite(self, asset_type: str, asset, is_favorite: bool):
        """Переключение статуса избранного"""
        symbol = getattr(asset, 'code', getattr(asset, 'symbol', ''))
        name = asset.name
        
        if is_favorite:
            self.db.add_favorite(asset_type, symbol, name)
        else:
            self.db.remove_favorite(asset_type, symbol)
        
        self._update_favorites()
    
    def _update_favorites(self):
        """Обновление списка избранного"""
        for widget in self.favorites_frame.winfo_children():
            widget.destroy()
        
        favorites = self.db.get_favorites()
        
        if not favorites:
            ctk.CTkLabel(
                self.favorites_frame,
                text="Нет избранных активов",
                text_color="gray",
                font=ctk.CTkFont(size=10)
            ).pack(pady=10)
            return
        
        for fav in favorites[:10]:  # Показываем до 10
            ctk.CTkLabel(
                self.favorites_frame,
                text=f"{fav['symbol'][:8]}",
                font=ctk.CTkFont(size=11),
                anchor="w"
            ).pack(fill="x", pady=2)
    
    def _get_current_view(self) -> str:
        """Получение текущего представления"""
        # Простая реализация - можно улучшить
        return "all"
    
    def _show_currency(self):
        """Показать валюты"""
        self._clear_main()
        self.currency_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _show_crypto(self):
        """Показать криптовалюты"""
        self._clear_main()
        self.crypto_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _show_stocks(self):
        """Показать акции"""
        self._clear_main()
        self.stocks_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _show_all(self):
        """Показать всё"""
        self._clear_main()
        self.currency_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.crypto_frame.pack(fill="x", padx=20, pady=10)
        self.stocks_frame.pack(fill="x", padx=20, pady=(10, 20))
    
    def _clear_main(self):
        """Очистка основной области"""
        for frame in [self.currency_frame, self.crypto_frame, self.stocks_frame]:
            frame.pack_forget()
    
    def _open_settings(self):
        """Открытие окна настроек"""
        SettingsWindow(self, self.db, on_save=self._on_settings_saved)
    
    def _on_settings_saved(self):
        """Сохранение настроек"""
        self._apply_theme()
        self._load_data()
    
    def _on_close(self):
        """Закрытие приложения"""
        self.db.close()
        self.destroy()
