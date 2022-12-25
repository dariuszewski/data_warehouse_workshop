# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime
import re
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class ArticleLoader(ItemLoader):
    created_at_in = MapCompose(datetime.datetime.fromisoformat) 
    value_plus_in = MapCompose(lambda value: re.sub("[^*\d]", '', value), int)
    value_total_in = MapCompose(lambda value: re.sub("[^*\d]", '', value), int)

    created_at_out = TakeFirst()
    value_plus_out = TakeFirst()
    value_total_out = TakeFirst()
    article_id_out = TakeFirst()


class CommentLoader(ItemLoader):
    created_at_in = MapCompose(datetime.datetime.fromisoformat) 
    value_plus_in = MapCompose(int)
    value_total_in = MapCompose(int)

    created_at_out = TakeFirst()
    value_plus_out = TakeFirst()
    value_total_out = TakeFirst()
    article_id_out = TakeFirst()

class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()
    text = scrapy.Field()
    value_plus = scrapy.Field()
    value_total = scrapy.Field()
    created_at = scrapy.Field()
    sentiment = scrapy.Field()
    category = scrapy.Field()

class CommentItem(scrapy.Item):
    article_id = scrapy.Field()
    text = scrapy.Field()
    value_plus = scrapy.Field()
    value_total = scrapy.Field()
    created_at = scrapy.Field()
    sentiment = scrapy.Field()
    category = scrapy.Field()

def get_article(response):
    itemLoader = ArticleLoader(item=ArticleItem(), response=response)
    itemLoader.add_value("article_id", response.url.split("/")[-1])
    itemLoader.add_css("text", "*.pic_image.type_text::text")
    itemLoader.add_css("value_plus", '.value_plus::text')
    itemLoader.add_css("value_total", '.value_total::text')
    itemLoader.add_css("created_at", 'time::attr("datetime")')
    yield itemLoader.load_item()

def get_comment(selector, response):
    itemLoader = CommentLoader(item=CommentItem(), selector=selector)
    itemLoader.add_value("article_id", response.url.split("/")[-1])
    itemLoader.add_css("text", "*.commcontent::text")
    itemLoader.add_css("value_plus", '.points::text')
    itemLoader.add_css("value_total", '.count::text')
    itemLoader.add_css("created_at", 'time::attr("datetime")')
    yield itemLoader.load_item()
