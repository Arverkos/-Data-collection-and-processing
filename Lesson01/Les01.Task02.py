import requests
import json

"""Обращаемся к сервису NASA, который предоставляет информацию об астероидах около Земли в заданных
    временных рамках"""

service = 'https://api.nasa.gov/neo/rest/v1/feed'

APIkey = 'qpPA0rdqTmezYeFxM5SdBvPy7VNSZeDzkdspxaJ8'  # APIkey - получаем при регистрации

start_date = '2021-01-24'
end_date = '2021-01-25'

req = requests.get(f'{service}?start_date={start_date}&end_date={end_date}&api_key={APIkey}')
print(req.text)

if req.ok:
    with open('req.json', 'w') as f:
        json.dump(req.json(), f)
