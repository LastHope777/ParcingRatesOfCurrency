"""
Виджет для отображения актива (карточка)
"""

import customtkinter as ctk
from typing import Callable, Optional
from models.asset import Asset


class AssetWidget(ctk.CTkFrame):
    """Виджет карточки актива"""
    
    def __init__(
        self,
        master,
        asset: Asset,
        on_toggle_favorite: Optional[Callable] = None,
        is_favorite: bool = False,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.asset = asset
        self.on_toggle_favorite = on_toggle_favorite
        self.is_favorite = is_favorite
        
        self.configure(
            corner_radius=10,
            fg_color="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f5f5f5"
        )
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создание элементов виджета"""
        # Верхняя панель с названием и кнопкой избранного
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Символ и название
        symbol_label = ctk.CTkLabel(
            top_frame,
            text=self.asset.symbol,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#3b82f6"
        )
        symbol_label.pack(side="left")
        
        name_label = ctk.CTkLabel(
            top_frame,
            text=self.asset.name[:20] + "..." if len(self.asset.name) > 20 else self.asset.name,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        name_label.pack(side="left", padx=(10, 0))
        
        # Кнопка избранного
        fav_icon = "⭐" if self.is_favorite else "☆"
        self.fav_button = ctk.CTkButton(
            top_frame,
            text=fav_icon,
            width=30,
            height=30,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color="#3b82f6",
            command=self._toggle_favorite
        )
        self.fav_button.pack(side="right")
        
        # Цена
        price_frame = ctk.CTkFrame(self, fg_color="transparent")
        price_frame.pack(fill="x", padx=10, pady=5)
        
        price_label = ctk.CTkLabel(
            price_frame,
            text=f"${self.asset.price:,.2f}" if self.asset.price > 1 else f"{self.asset.price:,.4f}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        price_label.pack(side="left")
        
        # Изменение в %
        if self.asset.change_percent is not None:
            change_color = "#22c55e" if self.asset.change_percent >= 0 else "#ef4444"
            change_sign = "+" if self.asset.change_percent >= 0 else ""
            change_label = ctk.CTkLabel(
                price_frame,
                text=f"{change_sign}{self.asset.change_percent:.2f}%",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=change_color
            )
            change_label.pack(side="right")
        
        # Источник данных
        source_label = ctk.CTkLabel(
            self,
            text=getattr(self.asset, 'source', 'Unknown'),
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        source_label.pack(anchor="w", padx=10, pady=(0, 10))
    
    def _toggle_favorite(self):
        """Переключение статуса избранного"""
        self.is_favorite = not self.is_favorite
        fav_icon = "⭐" if self.is_favorite else "☆"
        self.fav_button.configure(text=fav_icon)
        
        if self.on_toggle_favorite:
            self.on_toggle_favorite(self.asset, self.is_favorite)
    
    def update_data(self, asset: Asset):
        """Обновление данных актива"""
        self.asset = asset
        self._create_widgets()
