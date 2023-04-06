import scrapy
from scrapy.exceptions import CloseSpider
from datetime import date

from hyundaikz.items import HyundaiItem


class HyundaiSpiderSpider(scrapy.Spider):
    name = "hyundai"
    start_urls = ["https://hyundai-astana.kz/cars/"]

    def parse(self, response):
        for car in response.css(".carItem"):
            item = HyundaiItem()
            item["name"] = car.css(".carName::text").get()
            item["price"] = car.css(".carPrice::text").get()
            item["url"] = car.css("a::attr(href)").get()
            item["parseDate"] = date.today()
            yield item

