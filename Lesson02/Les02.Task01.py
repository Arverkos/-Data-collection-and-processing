""" Парсер сделан только для сайта hh.ru"""


from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re


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

        vacansies.append(vacancy_data)

    if not soup.find('a', {'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}):
        break

    params['page'] += 1

pprint(vacansies)