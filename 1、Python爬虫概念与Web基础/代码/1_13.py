"""
刷CSDN博客文章访问量的脚本
"""
import random
import urllib.request
import threading as t
import os
import ssl

# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 代理ip文件
proxy_ips_file = 'proxy_ips.txt'

# 代理ip列表
proxy_ips = []

# 文章地址
article_url = 'https://blog.csdn.net/JackLang/article/details/81592985'

# 请求头
headers = {
    'Host': 'blog.csdn.net',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

read_count = 0


# 读取文件里的代理ip，返回一个列表
def load_ips(file_path):
    if os.path.exists(file_path):
        data_list = []
        with open(file_path, "r+", encoding='utf-8') as f:
            for ip in f:
                data_list.append(ip.replace("\n", ""))
        return data_list


# 访问网页
def read_article():
    # 随机取出一枚代理ip
    proxy_ip = proxy_ips[random.randint(0, len(proxy_ips) - 1)]
    proxy_support = urllib.request.ProxyHandler({'http': proxy_ip})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    try:
        req = urllib.request.Request(article_url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=20).read()
        # 如果返回码是200代表访问成功
        if resp is not None and resp.status == 200:
            global read_count
            read_count += 1
            print("累计访问成功次数： %d" % read_count)
            return None
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 读取代理ip列表
    proxy_ips = load_ips(proxy_ips_file)
    read_article()
    if len(proxy_ips) > 0:
        for i in range(100):
            read_article()