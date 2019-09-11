"""
正则表达式实战示例：采集所有城市编码
"""
import requests as r
from bs4 import BeautifulSoup
import re
import os

base_url = 'http://www.weather.com.cn'
city_referer_url = 'http://www.weather.com.cn/textFC/hb.shtml'

# 获取城市编码的正则
code_regex = re.compile('^.*?weather/(.*?).shtml$', re.S)
# 城市编码的保存文件
save_file_name = os.path.join(os.getcwd(), 'city_codes.txt')
# 城市编码列表
city_code_list = []


# 获取所有的城市列表
def fetch_city_url_list():
    city_url_list = []
    resp = r.get(city_referer_url)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    content = bs.find('div', attrs={'class': 'lqcontentBoxheader'})
    if content is not None:
        a_s = content.find_all('a')
        if a_s is not None:
            for a in a_s:
                city_url_list.append(base_url + a.get('href'))
    return city_url_list


# 获取城市天气跳转链接列表
def fetch_city_weather_url_list(url):
    resp = r.get(url)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    a_s = bs.select('div.conMidtab a')
    for a in a_s:
        if a.get("href") is not None and a.text != '详情' and a.text != '返回顶部':
            # 提取城市编码
            result = code_regex.match(a.get("href"))
            if result is not None:
                city_code_list.append(a.text + ":" + result.group(1))


# 把列表写入到文件中的方法
def write_list_to_file(data):
    try:
        with open(save_file_name, "w+",  encoding='utf-8') as f:
            for content in data:
                f.write(content + "\n")
    except OSError as reason:
        print(str(reason))


if __name__ == '__main__':
    city_list = fetch_city_url_list()
    for city in city_list:
        print("解析：", city)
        fetch_city_weather_url_list(city)
    write_list_to_file(city_code_list)
