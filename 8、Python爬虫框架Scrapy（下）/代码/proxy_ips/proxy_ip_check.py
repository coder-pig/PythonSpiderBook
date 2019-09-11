import asyncio

import aiohttp
from aiohttp import ClientError, ClientConnectionError, ClientHttpProxyError, ServerDisconnectedError
from redis import StrictRedis

test_url = 'https://ip.cn/'


class ProxyCheck:
    def __init__(self):
        self.redis_db = StrictRedis(
            host="127.0.0.1",
            port=6379,
            password="Jay12345",
            db=0
        )

    # 检测代理IP是否可用
    async def check_ip(self, proxy_ip):
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                async with session.get(test_url, proxy=proxy_ip.replace("https", "http"), headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/68.0.3440.106 Safari/537.36'
                }) as resp:
                    if resp.status in [200]:
                        print("代理可用：", proxy_ip)
                    else:
                        print("移除不可用代理ip：", proxy_ip)
                        self.redis_db.srem('proxy_ips:proxy_pool', proxy_ip)
            except (ClientError, ClientConnectionError, ClientHttpProxyError, ServerDisconnectedError, TimeoutError,
                    AttributeError):
                print("代理请求失败移除代理ip：", proxy_ip)
                self.redis_db.srem('proxy_ips:proxy_pool', proxy_ip)

    def check_all_ip(self):
        print("开始检测代理ip是否可用")
        loop = asyncio.get_event_loop()
        tasks = []
        for ip in self.redis_db.smembers('proxy_ips:proxy_pool'):
            tasks.append(self.check_ip(ip.decode()))
        loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    ProxyCheck().check_all_ip()
