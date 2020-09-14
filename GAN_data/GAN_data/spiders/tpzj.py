import uuid

import scrapy

from GAN_data.items import GanDataItem


class TpzjSpider(scrapy.Spider):
    name = 'tpzj'
    # allowed_domains = ['https://m.tupianzj.com/meinv/xiezhen/']
    start_urls = ['https://m.tupianzj.com/meinv/xiezhen/']

    def parse(self, response):
        for src in response.xpath("//div[@class='IndexList']/ul[@class='IndexListult']/li/a/@href").extract():
            yield scrapy.Request(src, callback=self.parse_img_link)
        if response.xpath("//div[@id='pageNum']/span/li/a[text()='下一页']/@href").extract():
            next_page = response.xpath("//div[@id='pageNum']/span/li/a[text()='下一页']/@href").get()
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_img_link(self, response):
        if response.url.split("_")[0] != response.url:
            item = GanDataItem()
            img_link = response.xpath("//div[@class='show-simg']/a/img/@src").get()
            item['name'] = str(uuid.uuid4()).replace("-", "")+'.jpg'
            item['src'] = img_link
            yield item
        img_id = response.url.split("/")[-1].split(".")[0].split("_")[0]
        if img_id in response.xpath("//div[@class='show-simg']/a/@href").get():
            next_img = response.xpath("//div[@class='show-simg']/a/@href").get()
            yield scrapy.Request(response.urljoin(next_img), callback=self.parse_img_link)
