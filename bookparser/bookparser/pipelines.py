# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['books_db']

    def process_item(self, item, spider):
        id = item.get('url')
        if spider.name == 'book24ru':
            item['_id'] = id.split('-')[-1].replace('/', '')
        elif spider.name == 'labirintru':
            item['_id'] = id.replace('/', ' ').split()[-1]
        self.db[spider.name].update_one({'_id': {"$eq": item["_id"]}}, {"$set": item}, upsert=True)

        return item

    def close_spider(self, spider):
        self.client.close()
