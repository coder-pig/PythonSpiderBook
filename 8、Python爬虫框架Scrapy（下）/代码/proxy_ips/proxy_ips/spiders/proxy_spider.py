import asyncio

import aiohttp
from aiohttp import ClientError, ClientConnectionError, ClientHttpProxyError, ServerDisconnectedError
from redis import StrictRedis
from scrapy import Spider, Request
import time

test_url = 'https://ip.cn/'


# 获取代理IP的爬虫
class FetchIpSpider(Spider):
    name = "fetch_ip"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_db = StrictRedis(
            host="127.0.0.1",
            port=6379,
            password="Jay12345",
            db=0
        )

    def start_requests(self):
        # for i in range(1, 5):
        #     yield Request(url="http://www.xicidaili.com/nn/" + str(i), callback=self.parse_xici, headers={
        #         'Host': 'www.xicidaili.com',
        #         'Referer': 'http://www.xicidaili.com/',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #                       'Chrome/68.0.3440.106 Safari/537.36'
        #     })

        for i in range(1, 5):
            time.sleep(3)
            yield Request(url='https://www.kuaidaili.com/free/inha/' + str(i) + '/', callback=self.parse_kuaidaili,
                          headers={
                              'Host': 'www.kuaidaili.com',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                            'like Gecko) '
                                            'Chrome/68.0.3440.106 Safari/537.36'
                          })

    def parse_xici(self, response):
        loop = asyncio.get_event_loop()
        proxy_ips = []
        for tr in response.css('#ip_list tr'):
            td_list = tr.css('td::text')
            if len(td_list) < 3:
                continue
            ip_address = td_list[0].extract()  # IP
            port = td_list[1].extract()  # 端口
            if len(td_list) == 11:
                proto = td_list[4].extract()
            else:
                proto = td_list[5].extract()  # 协议类型
            proxy_ip = '%s://%s:%s' % (proto.lower(), ip_address, port)
            # 获取响应时间，超过2s的丢弃
            latency = tr.css('div.bar::attr(title)').re_first('(\d+\.\d+)')
            if float(latency) > 2:
                self.logger.info("跳过慢速代理：%s 响应时间：%s" % (proxy_ip, latency))
            else:
                self.logger.info("可用代理加入队列：%s 响应时间：%s" % (proxy_ip, latency))
                proxy_ips.append(proxy_ip)
        tasks = []
        for ip in proxy_ips:
            tasks.append(self.check_ip(ip))
        loop.run_until_complete(asyncio.wait(tasks))


    def parse_kuaidaili(self, response):
        loop = asyncio.get_event_loop()
        proxy_ips = []
        for tr in response.css('tbody tr'):
            td_list = tr.css('td::text')
            ip_address = td_list[0].extract()  # IP
            port = td_list[1].extract()  # 端口
            proto = td_list[3].extract()  # 协议
            proxy_ip = '%s://%s:%s' % (proto.lower(), ip_address, port)
            # 获取响应时间，超过2s的丢弃
            latency = float((td_list[5].extract())[:-1])
            if float(latency) > 2:
                self.logger.info("跳过慢速代理：%s 响应时间：%s" % (proxy_ip, latency))
            else:
                self.logger.info("可用代理加入队列：%s 响应时间：%s" % (proxy_ip, latency))
                proxy_ips.append(proxy_ip)
        tasks = []
        for ip in proxy_ips:
            tasks.append(self.check_ip(ip))
        loop.run_until_complete(asyncio.wait(tasks))

    # 检测代理IP是否可用
    async def check_ip(self, proxy_ip):
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                async with session.get(test_url, proxy=proxy_ip.replace("https", "http")) as resp:
                    if resp.status in [200]:
                        print("代理可用：", proxy_ip)
                        self.redis_db.sadd('proxy_ips:proxy_pool', proxy_ip)
                    else:
                        print("代理不可用：", proxy_ip)
            except (ClientError, ClientConnectionError, ClientHttpProxyError, ServerDisconnectedError, TimeoutError,
                    AttributeError):
                print("代理请求失败：", proxy_ip)
