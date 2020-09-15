import uuid

import scrapy

from GAN_data.items import GanDataItem


class AitaotuSpider(scrapy.Spider):
    name = 'aitaotu'
    # allowed_domains = ['https://www.aitaotu.com/tag/tmnh.html']
    start_urls = ['https://www.aitaotu.com/tag/qingchunmeinv.html']

    def parse(self, response):
        for src in response.xpath("//div[@class='libox']/a/@href").extract():
            yield scrapy.Request(response.urljoin(src), callback=self.parse_img_link)
        if response.xpath("//a[text()='下一页']/@href").extract():
            next_page = response.xpath("//a[text()='下一页']/@href").get()
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_img_link(self, response):
        item = GanDataItem()
        img_link = response.xpath("//p/a/img/@src").get()
        item['name'] = str(uuid.uuid4()).replace("-", "") + '.jpg'
        item['src'] = img_link
        yield item
        img_id = response.url.split("/")[-1].split(".")[0].split("_")[0]
        if img_id in response.xpath("//li[@class='tal']/p/a/@href").get():
            next_img = response.xpath("//li[@class='tal']/p/a/@href").get()
            yield scrapy.Request(response.urljoin(next_img), callback=self.parse_img_link)

