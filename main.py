"""
Asset Tracker - Трекер финансовых активов
Валюты | Криптовалюты | Акции

Версия: 1.0.0
"""

import sys
import customtkinter as ctk

from gui.main_window import MainWindow


def main():
    """Основная функция - запуск GUI приложения"""
    # Настройка внешнего вида
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Создание и запуск приложения
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
