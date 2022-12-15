# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose

class DWItemLoader(ItemLoader):
    created_at_in = MapCompose(lambda value: datetime.datetime.fromisoformat(value)) 


class DWItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    value_plus = scrapy.Field()
    value_total = scrapy.Field()
    created_at = scrapy.Field()
    sentiment = scrapy.Field()
    # pass
