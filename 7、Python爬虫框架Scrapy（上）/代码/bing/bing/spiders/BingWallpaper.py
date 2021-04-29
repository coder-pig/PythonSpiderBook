# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import time
import json

from bing.items import BingItem


class BingWallpaperSpider(Spider):
    name = 'BingWallpaper'
    allowed_domains = ['cn.bing.com']

    def start_requests(self):
        yield Request(
            'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=1&n=7&nc={ts}&pid=hp'.format(ts=int(time.time())),
            callback=self.parse)

    def parse(self, response):
        json_result = json.loads(response.body.decode('utf8'))
        images = json_result['images']
        if images is not None:
            item = BingItem()
            url_list = []
            for image in images:
                url_list.append('https://cn.bing.com' + image['url'])
            item['image_urls'] = url_list
            yield item
