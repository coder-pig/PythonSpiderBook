# -*- coding: utf-8 -*-
from scrapy import Request, Spider, Selector
import datetime

from FirstSpider.items import *


def parse_index(response):
    items = response.xpath('//li[@class="js-smallCards _box"]')
    for item in items:
        bcy_item = BcyItem()
        bcy_item['author'] = item.xpath('a[@class="db posr ovf"]/@title').extract_first()
        bcy_item['pic_url'] = item.xpath('a/img/@src').extract_first().replace('/2X3', '')
        yield bcy_item


class BcySpider(Spider):
    name = 'bcy'
    allowed_domains = ['bcy.net']

    index_url = 'https://bcy.net/illust/toppost100?type=lastday&date={d}'

    ajax_url = 'https://bcy.net/illust/index/ajaxloadtoppost?p=1&type=lastday&date={d}'

    date_list = []  # 日期范围列表

    ajax_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36',
        'Host': 'bcy.net',
        'Origin': 'https://bcy.net',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        self.init_date_list()
        for date in self.date_list:
            yield Request(self.index_url.format(d=date), callback=parse_index)
        for date in self.date_list:
            yield Request(self.ajax_url.format(d=date), callback=parse_index)

    # 构造一个日期列表
    def init_date_list(self):
        begin_date = datetime.datetime.strptime("20150918", "%Y%m%d")
        end_date = datetime.datetime.strptime("20180827", "%Y%m%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y%m%d")
            self.date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
