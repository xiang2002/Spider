# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import requests
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class GanDataPipeline(ImagesPipeline):
    # def open_spider(self, spider):
    #     self.f = open('job2.json', 'w', encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     self.f.write(json.dumps(dict(item), ensure_ascii=False))
    #     self.f.write('\n')
    #     return item
    #
    # def close_spider(self, spider):
    #     self.f.close()
    # def process_item(self, item, spider):
    #     with open("data/"+item['name'], 'ab+') as f:
    #         f.write(requests.get(item['src']).content)
    #     return item
    def get_media_requests(self, item, info):
        img_link = item['src']
        yield Request(img_link, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        img_name = item['name']
        filename = u'{0}'.format(img_name)
        return filename
