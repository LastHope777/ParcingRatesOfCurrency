"""
Окно настроек приложения
"""

import customtkinter as ctk
from typing import Callable, Dict
from database.db_manager import DatabaseManager


class SettingsWindow(ctk.CTkToplevel):
    """Окно настроек"""
    
    def __init__(self, parent, db: DatabaseManager, on_save: Callable = None):
        super().__init__(parent)
        
        self.db = db
        self.on_save = on_save
        
        self.title("Настройки ⚙️")
        self.geometry("500x650")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        # Цвета для светлой темы
        self.light_text = "#000000"
        self.dark_text = "#FFFFFF"
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создание элементов окна"""
        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="Настройки приложения",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Контейнер для настроек
        settings_frame = ctk.CTkScrollableFrame(self)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # === Тема оформления ===
        theme_section = ctk.CTkFrame(settings_frame, fg_color="transparent")
        theme_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            theme_section,
            text="🎨 Тема оформления",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        ).pack(anchor="w")
        
        self.theme_var = ctk.StringVar(value=self.db.get_setting("theme", "dark"))
        
        theme_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=5)
        
        ctk.CTkRadioButton(
            theme_frame,
            text="Тёмная",
            variable=self.theme_var,
            value="dark"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            theme_frame,
            text="Светлая",
            variable=self.theme_var,
            value="light"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            theme_frame,
            text="Системная",
            variable=self.theme_var,
            value="system"
        ).pack(side="left", padx=10)
        
        # === Интервал обновления ===
        interval_section = ctk.CTkFrame(settings_frame, fg_color="transparent")
        interval_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            interval_section,
            text="🔄 Интервал обновления (секунды)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        ).pack(anchor="w")
        
        self.interval_var = ctk.StringVar(value=self.db.get_setting("refresh_interval", "60"))
        
        interval_slider = ctk.CTkSlider(
            settings_frame,
            from_=10,
            to=300,
            number_of_steps=29,
            command=lambda v: self.interval_var.set(str(int(v)))
        )
        interval_slider.set(float(self.interval_var.get()))
        interval_slider.pack(fill="x", pady=10)
        
        interval_label = ctk.CTkLabel(
            settings_frame,
            textvariable=self.interval_var,
            font=ctk.CTkFont(size=12)
        )
        interval_label.pack()
        
        # === Отображение типов активов ===
        visibility_section = ctk.CTkFrame(settings_frame, fg_color="transparent")
        visibility_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            visibility_section,
            text="👁️ Отображение типов активов",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        ).pack(anchor="w")
        
        self.show_currency = ctk.StringVar(
            value=self.db.get_setting("show_currency", "true")
        )
        self.show_crypto = ctk.StringVar(
            value=self.db.get_setting("show_crypto", "true")
        )
        self.show_stocks = ctk.StringVar(
            value=self.db.get_setting("show_stocks", "true")
        )
        
        ctk.CTkCheckBox(
            settings_frame,
            text="💱 Валюты",
            variable=self.show_currency,
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        ).pack(anchor="w", pady=5)
        
        ctk.CTkCheckBox(
            settings_frame,
            text="₿ Криптовалюты",
            variable=self.show_crypto,
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        ).pack(anchor="w", pady=5)
        
        ctk.CTkCheckBox(
            settings_frame,
            text="📈 Акции",
            variable=self.show_stocks,
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        ).pack(anchor="w", pady=5)
        
        # === Кнопки ===
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Сохранить",
            command=self._save_settings,
            width=120,
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Отмена",
            command=self.destroy,
            fg_color="transparent",
            border_width=1,
            width=120,
            text_color=self.light_text if ctk.get_appearance_mode() == "Light" else self.dark_text
        )
        cancel_btn.pack(side="left", padx=10)
    
    def _save_settings(self):
        """Сохранение настроек"""
        self.db.set_setting("theme", self.theme_var.get())
        self.db.set_setting("refresh_interval", self.interval_var.get())
        self.db.set_setting("show_currency", self.show_currency.get())
        self.db.set_setting("show_crypto", self.show_crypto.get())
        self.db.set_setting("show_stocks", self.show_stocks.get())
        
        if self.on_save:
            self.on_save()
        
        self.destroy()
