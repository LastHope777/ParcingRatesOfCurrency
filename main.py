import requests  # Импорт библиотеки requests
from bs4 import BeautifulSoup  # Импорт класса BeautifulSoup из библиотеки BeautifulSoup
import matplotlib.pyplot as plt  # Импорт библиотеки для построения графиков

def get_currency_rates():
    url = 'https://cbr.ru/currency_base/daily/'  # Задание URL-адреса страницы с курсами валют
    response = requests.get(url)  # Отправка GET-запроса к указанному URL

    if response.status_code != 200:  # Проверка успешности запроса (код 200 означает успех).
        print(f"Ошибка: Невозможно получить доступ к странице. Код ошибки: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')  # Создание объекта BeautifulSoup для анализа HTML-кода страницы
    table = soup.find('table', {'class': 'data'})  # Поиск таблицы с курсами валют на странице

    if not table:  # Проверка наличия таблицы с курсами валют
        print("Ошибка: Таблица с курсами валют не найдена на странице.")
        return None

    currency_rates = {}  # Создание пустого словаря для хранения курсов валют
    rows = table.find_all('tr')  # Поиск всех строк (строчек) в таблице
    for row in rows[1:]:  # Цикл по всем строкам, начиная со второй (первая строка - заголовки)
        columns = row.find_all('td')  # Поиск всех ячеек (столбцов) в текущей строке
        if len(columns) >= 5:  # Проверка, что в текущей строке есть хотя бы 5 ячеек (необходимые данные)
            currency_name = columns[1].text.strip()  # Получение названия валюты из второй ячейки и удаление пробелов
            currency_rate = columns[4].text.strip()  # Получение курса валюты из пятой ячейки и удаление пробелов
            currency_rates[currency_name] = currency_rate  # Добавление пары валюта-курс в словарь

    return currency_rates  # Возврат словаря с курсами валют

if __name__ == "__main__":
    rates = get_currency_rates()  # Вызов функции get_currency_rates и сохранение результата в переменную rates
    if rates:
        print("Курсы валют Центрального банка России:")
        for currency, rate in rates.items():
            print(f"{currency}: {rate}")

        # # Визуализация курсов валют с помощью графика
        # currencies = list(rates.keys())  # Получение списка валют из ключей словаря
        # rates_values = [float(rate.replace(',', '.')) for rate in rates.values()]  # Преобразование значений курсов валют из строк в числа типа float
        # 
        # plt.figure(figsize=(10, 6))  # Создание графика с указанным размером
        # plt.bar(currencies, rates_values, color='blue')  # Построение столбчатой диаграммы
        # plt.xlabel('Валюта')  # Название оси X
        # plt.ylabel('Курс')  # Название оси Y
        # plt.title('Курсы валют Центрального банка России')  # Заголовок графика
        # plt.xticks(rotation=45)  # Поворот названий валют на оси X
        # plt.tight_layout()  # Улучшение отображения графика (уменьшение перекрытий)
        # plt.show()  # Отображение графика
