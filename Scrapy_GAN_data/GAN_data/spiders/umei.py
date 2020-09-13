# -*- coding: utf-8 -*-
import uuid
import scrapy
from scrapy import Selector

from GAN_data.items import GanDataItem


class UmeiSpider(scrapy.Spider):
    name = 'umei'
    # allowed_domains = ['https://www.umei.cc/tags/meinv_1.htm']
    start_urls = ['https://www.umei.cc/tags/meinv_1.htm']

    def parse(self, response):
        for src in Selector(response).xpath("//div[@class='TypeList']/ul/li/a/@href").extract():
            yield scrapy.Request(src, callback=self.parse_img_link)
        if response.xpath("//div[@class='NewPages']/ul/li/a[text()='下一页']/@href").extract():
            next_page = response.xpath("//div[@class='NewPages']/ul/li/a[text()='下一页']/@href").get()
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_img_link(self, response):
        item = GanDataItem()
        img_link = Selector(response).xpath("//div[@class='ImageBody']/p/a/img/@src").get()
        item['name'] = str(uuid.uuid4()).replace("-", "")+'.jpg'
        item['src'] = img_link
        yield item
        if response.xpath("//div[@class='NewPages']/ul/li/a[text()='下一页']/@href").get() != "#":
            next_img = response.xpath("//div[@class='NewPages']/ul/li/a[text()='下一页']/@href").get()
            yield scrapy.Request(response.urljoin(next_img), callback=self.parse_img_link)
