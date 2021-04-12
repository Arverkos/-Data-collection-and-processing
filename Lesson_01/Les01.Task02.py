import requests
import json

"""Обращаемся к сервису NASA, который предоставляет информацию об астероидах около Земли в заданных
    временных рамках"""


def asteroid_info(start_date, end_date):

    service = 'https://api.nasa.gov/neo/rest/v1/feed'

    APIkey = 'qpPA0rdqTmezYeFxM5SdBvPy7VNSZeDzkdspxaJ8'  # APIkey - получаем при регистрации

    # Формируем get-запрос к сервису

    req = requests.get(f'{service}?start_date={start_date}&end_date={end_date}&api_key={APIkey}')

    # Если запрос произведен успешно, выводим информацию об астероидах, а также записываем результат в json-файл

    if req.ok:
        print(req.text)

        with open('req.json', 'w') as f:
            json.dump(req.json(), f)


start_date = '2021-03-24'
end_date = '2021-03-25'

asteroid_info(start_date, end_date)
