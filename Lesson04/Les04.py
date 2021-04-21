import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint
import unidecode


client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
news_db = db.news_db


"""Скрапер новостей с ресурса lenta.ru"""


def get_news_lenta():

    url = "https://lenta.ru/"

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/84.0.4147.125 Safari/537.36'}

    r = requests.get(url, headers=headers)

    xpath_for_item = '//div[@class="b-yellow-box__wrap"]/div[@class="item"]/a/@href'
    dom = html.fromstring(r.text)
    items = dom.xpath(xpath_for_item)

    news_lenta_list = []

    for item in items:

        news_el = {}
        news_el['url'] = url + item

        lenta_news_request = requests.get(news_el['url'], headers=headers)
        dom_news = html.fromstring(lenta_news_request.text)
        news_el['name'] = unidecode.unidecode(dom_news.xpath('//h1/text()')[0])
        news_el['time'] = dom_news.xpath('//div[@class="b-topic__info"]/time/text()')[0]

        news_el['source'] = 'lenta.ru'

        news_lenta_list.append(news_el)

    return news_lenta_list


"""Скрапер новостей с ресурса news.mail.ru"""


def get_news_mailru():

    url = "https://news.mail.ru/"

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/84.0.4147.125 Safari/537.36'}

    r = requests.get(url, headers=headers)

    xpath_for_item = '//a[contains(@class , "js-topnews")]/@href'
    dom = html.fromstring(r.text)
    items_main = dom.xpath(xpath_for_item)
    items_minor = dom.xpath('//ul[@class="list list_type_square list_half js-module"]/li[@class="list__item"]/a/@href')

    items_main.extend(items_minor)

    news_mailru_list = []

    for item in items_main:

        news_el = {}
        news_el['url'] = item

        mailru_news_request = requests.get(news_el['url'], headers=headers)
        dom_news = html.fromstring(mailru_news_request.text)
        news_el['name'] = unidecode.unidecode(dom_news.xpath('//h1[@class = "hdr__inner"]/text()')[0])
        news_el['time'] = dom_news.xpath('//span[contains(@class, "js-ago")]/@datetime')[0]
        news_el['source'] = dom_news.xpath('//span[@class="note"]/a/span[@class = "link__text"]/text()')[0]

        news_mailru_list.append(news_el)

    return news_mailru_list

def add_news_to_db(db, news_list):
    for el in news_list:
        db.update_one({"$and": [{'name': {"$eq": el["name"]}}, {'source': {"$eq": el["source"]}}]},
                      {"$set": el}, upsert=True)
    print("Новости добавлены")


news_list = get_news_lenta()
pprint(news_list)
add_news_to_db(news_db, news_list)

print('___________________________')

news_list = get_news_mailru()
pprint(news_list)
add_news_to_db(news_db, news_list)
