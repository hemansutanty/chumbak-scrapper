import scrapy
from scrapy_splash import SplashRequest

class ChumbakProductSpider(scrapy.Spider):
    name = "chumbak"

    def start_requests(self):
        urls = [
            'https://www.chumbak.com/women-apparel/GY1/c/',
        ]
        for url in urls:
            yield SplashRequest(url, self.parse, args={'wait': 15})

    def parse(self, response):
        sidebar_dropdowns = response.css('ul.category-sidebar-dropdown')
        for dropdown_item in sidebar_dropdowns:
            cat = dropdown_item.css('a::text')[0].extract()
            if cat.strip() == 'Clothing':
                sub_categories = dropdown_item.css('li > ul > li')

        for sub_category in sub_categories:
            url = 'https://www.chumbak.com/'+sub_category.css('a::attr(href)').extract_first().strip()
            yield SplashRequest(url, self.parse_subcategory, args={'wait':15})

    def parse_subcategory(self, response):
        print('\n'+response.css('h2.header-with-underline::text').extract_first().strip())
        print('=========================================')
        products = response.css('div.product-details-bottom-wrap')
        for product in products :
            print(product.css('div > div > h2::text')[0].extract()+"\t"+product.css('div > div > h3 > span > span::text')[0].extract())
        