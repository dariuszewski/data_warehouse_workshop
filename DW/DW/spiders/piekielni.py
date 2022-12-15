import scrapy

from DW.items import DWItem, DWItemLoader

class PiekielniSpider(scrapy.Spider):
    name = 'piekielni'
    allowed_domains = ['piekielni.pl']
    start_urls = ['http://piekielni.pl/']

    # UNCOMMENT FOR PRODUCTION
    # def start_requests(self):
    #     return [scrapy.Request(f'http://piekielni.pl/page/{page}', self.parse) for page in range(10)]

    custom_settings = {'CLOSESPIDER_PAGECOUNT': 10}

    def parse(self, response):
        next_link = response.css("a.list_next_page_button::attr(href)").get()
        if next_link:
            yield response.follow(next_link, self.parse)

        for article_link in response.css(".pics_list .picture a::attr(href)"):
            yield response.follow(article_link, self.parse_article)

    def parse_article(self, response):
        print('CURRENT USER AGENT: ' + str(response.request.headers['User-Agent']))

        itemLoader = DWItemLoader(item=DWItem(), response=response)
        itemLoader.add_css("text", "*.pic_image.type_text::text")
        itemLoader.add_css("value_plus", '.value_plus::text')
        itemLoader.add_css("value_total", '.value_total::text')
        itemLoader.add_css("created_at", 'time::attr("datetime")')
        yield itemLoader.load_item()
