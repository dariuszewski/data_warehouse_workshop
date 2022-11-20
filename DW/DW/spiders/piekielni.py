import scrapy

from DW.items import DwItem

class PiekielniSpider(scrapy.Spider):
    name = 'piekielni'
    allowed_domains = ['piekielni.pl']
    start_urls = ['http://piekielni.pl/']
    custom_settings = {'CLOSESPIDER_PAGECOUNT': 10}

    def parse(self, response):
        next_link = response.css("a.list_next_page_button::attr(href)").get()
        if next_link:
            yield response.follow(next_link, self.parse)

        for article_link in response.css(".pics_list .picture a::attr(href)"):
            yield response.follow(article_link, self.parse_article)

    def parse_article(self, response):
        print('CURRENT USER AGENT: ' + str(response.request.headers['User-Agent']))
        yield DwItem(text=response.css("*.pic_image.type_text::text").getall())
