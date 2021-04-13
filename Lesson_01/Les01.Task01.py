import requests
import json

def getrepos(user):

    service = 'https://api.github.com/users/'

    # Формируем get-запрос к API

    req = requests.get(f'{service}{user}/repos')

    # Записываем результат get-запроса в json файл

    if req.ok:
        with open(f'{user}_repos.json', 'w') as f:
            json.dump(req.json(), f)

    # Формируем список репозиториев пользователя

    repos_list = []

    for el in req.json():
        repos_list.append(el['name'])

    return repos_list


user = 'arverkos'   # имя пользователя в качестве примера (мой аккаунт)

repos_list_user = getrepos(user)

print(f'Список репозиториев пользователя {user}:')

for el in repos_list_user:
    print(el)
