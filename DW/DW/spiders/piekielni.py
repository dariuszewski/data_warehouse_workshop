import scrapy

from DW.items import get_comment, get_article

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
            yield response.follow('/pic/komentarze' + article_link.getall().pop(), self.parse_comment)

        # 'https://piekielni.pl/pic/komentarze/89989'

    def parse_article(self, response):
        # print('CURRENT USER AGENT: ' + str(response.request.headers['User-Agent']))
        yield from get_article(response)

    
    def parse_comment(self, response):
        for comment in response.css('.comment'):
            yield from get_comment(comment, response)