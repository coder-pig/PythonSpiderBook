"""
fake_useragent库使用示例
"""

from fake_useragent import UserAgent
import random

if __name__ == '__main__':
    ua = UserAgent(use_cache_server=False)
    print("Chrome浏览器：", ua.chrome)
    print("FireFox浏览器：", ua.firefox)
    print("Ubuntu FireFox浏览器：", ua.ff)
    print("IE浏览器：", ua.ie)
    print("Safari浏览器：", ua.safari)
    print("Mac Chrome：", ua.google)
    print("Opera浏览器：", ua.opera)
    print("随机：",ua.random)
