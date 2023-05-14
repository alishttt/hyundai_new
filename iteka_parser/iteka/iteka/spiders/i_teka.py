import scrapy
from scrapy import Request
from scrapy import Selector
from scrapy.exceptions import CloseSpider
from datetime import date


class ITekaSpider(scrapy.Spider):
    name = "i-teka"
    # start_urls = ['https://i-teka.kz/astana/drug-categories/glyukometry-test-poloski-dlya-glyukometrov-lancety-ruchki']

    def __init__(self, city='astana', category='glyukometry-test-poloski-dlya-glyukometrov-lancety-ruchki', *args, **kwargs):
        super(ITekaSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.city = city

    def start_requests(self):
        yield scrapy.Request(f'https://i-teka.kz/{self.city}/drug-categories/{self.category}', callback=self.parse)


    def parse(self, response):
        products = response.css('.list-item a::attr(href)').getall()
        for product_url in products:
            yield response.follow(product_url, callback=self.parse_product)

        next_page_url = response.css('.next > a::attr(href)').extract_first()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_product(self, response):
        product_name = response.css('div.name.w-full h1::text').get().strip()
        pharmacies = response.css('.list-item.gtm_block_apteka')
        for pharmacy in pharmacies:
            crown_element = pharmacy.css('.title .crown')
            if crown_element:
                pharmacy_name = crown_element.xpath('following-sibling::text()').get().strip()
            else:
                pharmacy_name = pharmacy.css('.title-row > a:not(.button)::text').get().strip()
            pharmacy_price = pharmacy.css('.price::text').get().strip()
            parseDate = date.today()
            url = response.url



            yield {
                'product_name': product_name,
                'pharmacy_name': pharmacy_name,
                'pharmacy_price': pharmacy_price,
                'parseDate': parseDate,
                'url': url

            }





