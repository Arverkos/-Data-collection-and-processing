from bs4 import BeautifulSoup as bs
import requests
import re

from pymongo import MongoClient
from pprint import pprint


def salary_parsing(salary):
    currency = re.findall('\D*', salary)[-2][1:]
    if 'договор' in salary:
        salary_min, salary_max, currency = None, None, None
    elif '-' in salary:
        salary_min = int(''.join(re.findall('\d', salary.split('-')[0])))
        salary_max = int(''.join(re.findall('\d', salary.split('-')[1])))
    elif '—' in salary:
        salary_min = int(''.join(re.findall('\d', salary.split('-')[0])))
        salary_max = int(''.join(re.findall('\d', salary.split('-')[1])))
    elif 'от' in salary:
        salary_min = int(''.join(re.findall('\d', salary)))
        salary_max = None
    elif 'до' in salary:
        salary_min = None
        salary_max = int(''.join(re.findall('\d', salary)))
    else:
        salary_min, salary_max, currency = None, None, None
    return salary_min, salary_max, currency


"""Функция  для добавления вакансии в базу данных с проверкой уникальности вакансии, если вакансия уже есть,
   то она добавлена не будет. Проверка уникальности производится с помощью сравнения поля "_id", которому 
   присваивается значение URL вакансии"""

def vac_add_db(vacancies_db, vacancy_data):
    if not vacancies_db.find_one({'_id': vacancy_data['_id']}):
        vacancies_db.insert_one(vacancy_data)

"""Функция  для поиска вакансий с зарплатой больше введенной суммы"""

def vac_salary_search(vacancies_db, salary):
    for vacancy in vacancies_db.find({'$or': [{'min_salary': {'$gt': salary}}, {'max_salary': {'$gt': salary}}]}):
        pprint(vacancy)


client = MongoClient('127.0.0.1', 27017)
db = client['users_db']

vacancies_db = db.vacancies_db


vacancy_name = input('Введите название вакансии: ',)

vacansies = []

"""Парсинг данных с сайта hh.ru"""

params = {'clusters':'true',
         'enable_snippets':'true',
         'search_field':'name',
         'text': vacancy_name,
         'showClusters': 'true',
         'page': 0}


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'

main_link = 'https://hh.ru'

while True:

    response = requests.get(main_link+'/search/vacancy', headers={'User-Agent':user_agent}, params=params)
    soup = bs(response.text,'lxml')

    vacancy_block = soup.find('div', {'class':'vacancy-serp'})

    vacancy_list = vacancy_block.find_all('div', {'class':'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_data['name'] = vacancy.find('a').getText()
        vacancy_data['URL'] = vacancy.find('a')['href']
        vacancy_data['_id'] = vacancy.find('a')['href']

        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            vacancy_data['min_salary'] = None
            vacancy_data['max_salary'] = None
            vacancy_data['currency'] = None
        else:
            min_salary, max_salary, currency = salary_parsing(salary.getText())

            vacancy_data['min_salary'] = min_salary
            vacancy_data['max_salary'] = max_salary
            vacancy_data['currency'] = currency
        vacancy_data['source'] = main_link

        vac_add_db(vacancies_db, vacancy_data)
        # vacansies.append(vacancy_data)

    if not soup.find('a', {'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}):
        break

    params['page'] += 1


for vacancy in vacancies_db.find({}):
    pprint(vacancy)

salary = int(input('Введите величину зарплаты, свыше которой будет производиться поиск вакансий: ',))

vac_salary_search(vacancies_db, salary)