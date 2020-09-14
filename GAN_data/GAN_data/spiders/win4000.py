import uuid

import scrapy

from GAN_data.items import GanDataItem


class Win4000Spider(scrapy.Spider):
    name = 'win4000'
    # allowed_domains = ['http://www.win4000.com/meinvtag34.html']
    start_urls = ['http://www.win4000.com/meinvtag34.html/']

    def parse(self, response):
        for src in response.xpath("//div[@class='Left_bar']//div[@class='tab_tj']/div[@class='tab_box']/div/ul[@class='clearfix']/li/a/@href").extract():
            yield scrapy.Request(src, callback=self.parse_img_link)
        if response.xpath("//div[@class='pages']/div/a[text()='下一页']/@href").extract():
            next_page = response.xpath("//div[@class='pages']/div/a[text()='下一页']/@href").get()
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_img_link(self, response):
        item = GanDataItem()
        img_link = response.xpath("//div[@class='main-wrap']/div[@class='pic-meinv']/a/img/@url").get()
        img_id = response.url.split("/")[-1].split(".")[0].split('_')[0]
        item['name'] = str(uuid.uuid4()).replace("-", "") + '.jpg'
        item['src'] = img_link
        yield item
        if img_id in response.xpath("//div[@class='main-wrap']/div[@class='pic-meinv']/a/@href").get():
            next_img = response.xpath("//div[@class='main-wrap']/div[@class='pic-meinv']/a/@href").get()
            yield scrapy.Request(response.urljoin(next_img), callback=self.parse_img_link)
