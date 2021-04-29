"""
利用redis保存bilibili弹幕
"""
import requests as r
from bs4 import BeautifulSoup
import re
import redis

video_url = 'https://www.bilibili.com/video/av28989880'
cid_regex = re.compile(r'.*?cid=(\d*?)\&amp.*', re.S)
xml_base_url = 'http://comment.bilibili.com/'


# 获取弹幕的cid
def get_cid():
    resp = r.get(video_url).text
    bs = BeautifulSoup(resp, 'lxml')
    src = bs.select('div.share-address ul li')[1].input
    cid = cid_regex.match(str(src)).group(1)
    print("获取到的cid：", cid)


# 解析获取弹幕
def analysis_d(cid):
    count = 1
    url = xml_base_url + cid + '.xml'
    resp = r.get(url)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    d_s = bs.find_all('d')
    for d in d_s:
        dan_redis.set(str(count), d.text)
        count += 1


if __name__ == '__main__':
    # 连接redis
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='Zpj12345', db = 0)
    dan_redis = redis.StrictRedis(connection_pool=pool)
    # analysis_d('50280136')
    results = dan_redis.mget(dan_redis.keys())
    print("总共有%d条数据" % len(results))
    for result in results:
        print(result.decode('utf-8'))