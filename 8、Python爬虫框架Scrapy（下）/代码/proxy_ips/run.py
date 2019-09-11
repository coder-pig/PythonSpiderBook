import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from redis import StrictRedis

fetch_ip_time = 0

redis_db = StrictRedis(
    host="127.0.0.1",
    port=6379,
    password="Jay12345",
    db=0
)


def check_ip():
    global fetch_ip_time
    proxy_poll = redis_db.smembers("proxy_ips:proxy_pool")
    if len(proxy_poll) == 0:
        print("可用代理IP数目为0，激活爬虫...")
        os.system("scrapy crawl fetch_ip")
        fetch_ip_time = int(time.time())
    else:
        if len(proxy_poll) < 5:
            if int(time.time() - fetch_ip_time) < 600:
                if len(proxy_poll) == 0:
                    print("虽然处于保护状态，但是可用代理IP数目为0，激活爬虫...")
                    os.system("scrapy crawl fetch_ip")
                    fetch_ip_time = int(time.time())
                else:
                    print("当前可用代理IP少于5，但是还处于保护状态，不激活爬虫")
            else:
                print("当前可用代理IP少于5，且处于非保护状态，激活爬虫...")
                os.system("scrapy crawl fetch_ip")
                fetch_ip_time = int(time.time())
        else:
            print("日常自检...")
            os.system("python proxy_ip_check.py")


if __name__ == '__main__':
    check_ip()
    scheduler = BlockingScheduler()
    # 每隔20s执行一次
    scheduler.add_job(check_ip, 'interval', max_instances=10, seconds=20)
    scheduler.start()
