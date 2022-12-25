# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sentimentpl.models import SentimentPLModel

from .items import ArticleItem, CommentItem

class DWPipeline:

    def open_spider(self, spider):
        self.model = SentimentPLModel(from_pretrained='latest')

    def process_item(self, item, spider):

        if isinstance(item, ArticleItem):
            # print('ArticleItem')
            item.setdefault('category', 'article')
        if isinstance(item, CommentItem):
            # print('CommentItem')
            item.setdefault('category', 'comment')

        item["text"] = "".join(item['text']).strip()
        item['sentiment'] = self.model(item["text"][0:500]).item()
        return item
