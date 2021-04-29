# -*- coding: utf-8 -*-

# Scrapy settings for FirstSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FirstSpider'

SPIDER_MODULES = ['FirstSpider.spiders']
NEWSPIDER_MODULE = 'FirstSpider.spiders'

ROBOTSTXT_OBEY = False


DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.106 Safari/537.36',
    'Host': 'bcy.net',
    'Origin': 'https://bcy.net',
}

DOWNLOADER_MIDDLEWARES = {
    'FirstSpider.middlewares.ProxyMiddleware': 555
}

ITEM_PIPELINES = {
    'FirstSpider.pipelines.MySQLPipeline': 300,
}
