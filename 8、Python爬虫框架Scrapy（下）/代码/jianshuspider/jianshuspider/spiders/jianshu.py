# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from jianshuspider.items import JianshuspiderItem


class JianshuSpider(Spider):
    name = 'jianshu'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['http://www.jianshu.com/']

    def start_requests(self):
        yield Request('https://www.jianshu.com', callback=self.parse)

    def parse(self, response):
        li_s = response.xpath('//ul[@class="note-list"]/li')
        for li in li_s:
            item = JianshuspiderItem()
            item['title'] = li.xpath('.//div/a[@class="title"]/text()').extract_first()
            item['content'] = str(li.xpath('.//div/p[@class="abstract"]/text()').extract_first()).replace(
                " ", "").replace(
                "\n", "")
            item['url'] = 'https://www.jianshu.com/p/' + str(
                li.xpath('.//div/a[@class="title"]/@href').extract_first())
            item['nickname'] = li.xpath('.//div/a[@class="nickname"]/text()').extract_first()
            yield item
