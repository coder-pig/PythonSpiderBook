"""
csv库实战示例：爬取星座运势
"""
import csv
import requests as r
from bs4 import BeautifulSoup
import re
import os

# 抓取站点
constellation_url = 'http://www.xzw.com/fortune/'

# 提取信息的正则
fetch_regex = re.compile(r'^.*?<strong>(.*?)</strong><small>(.*?)</small>.*?width:(\d*)%.*?p>(.*)\[<a.*$', re.S)

# 数据保存文件名
save_path = os.path.join(os.getcwd(), 'constellation.csv')

# 表头
headers = ['星座','生日时间','运势评分','今日运势']

# 爬取星座运势相关信息保存
def fetch_constellation_msg():
    resp = r.get(constellation_url).text
    bs = BeautifulSoup(resp, 'lxml')
    dls = bs.select('div.alb div dl')
    result_list = [headers]
    for dl in dls:
        # 正则提取信息
        result = fetch_regex.match(str(dl))
        if result is not None:
            result_list.append([result.group(1),result.group(2), str(int(result.group(3))/20) + '颗星', result.group(4)])
    # 数据写入csv文件中
    with open(save_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result_list)

if __name__ == '__main__':
    fetch_constellation_msg()