import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/бестселлеры/?stype=0']

    def parse(self, response: HtmlResponse):
        parent_url = 'https://www.labirint.ru'
        links = response.xpath('//a[contains(@class, "product-title-link")]/@href').getall()
        for link in links:
            yield response.follow(parent_url + link, callback=self.process_item)

        next_page = response.xpath('//div[@class="pagination-next"]/a/@href').get()
        if next_page:
            yield response.follow(parent_url + next_page, callback=self.parse)

    def process_item(self, response=HtmlResponse):
        item = BookparserItem()
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').get()
        item['author'] = response.xpath('//a[@data-event-label="author"]/text()').get()
        item['price'] = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        item['rating'] = response.xpath('//div[@id="rate"]/text()').get()
        yield item
