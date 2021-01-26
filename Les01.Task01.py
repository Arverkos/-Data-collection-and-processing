import requests

service = 'https://api.github.com/users/'
user = 'arverkos'   # имя пользователя моего аккаунта

# Формируем get-запрос к API

req = requests.get(f'{service}{user}/repos')

# Выводим построчно список репозиториев пользователя

print(f'Список репозиториев пользователя {user}:')

for el in req.json():
    print(el['name'])
