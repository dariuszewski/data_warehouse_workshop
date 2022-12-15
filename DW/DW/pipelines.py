# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sentimentpl.models import SentimentPLModel

from .items import DWItem

class DWPipeline:
    def process_item(self, item: DWItem, spider):
        model = SentimentPLModel(from_pretrained='latest')

        item["text"] = "".join(item['text']).strip()
        item['sentiment'] = model(item["text"][0:500]).item()
        return item
