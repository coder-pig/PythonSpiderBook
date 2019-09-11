"""
Beautiful Soup使用示例，抓取壁纸网站的壁纸
"""
import requests as r
from bs4 import BeautifulSoup
import os
import time

base_url = "http://www.win4000.com"
theme_base_url = "http://www.win4000.com/zt/xiaoqingxin_"

# 利用列表表达式生成每页链接列表
theme_url_list = [theme_base_url + str(x) + '.html' for x in range(1, 6)]

# 套图链接列表
series_url_lists = []

# 保存文件名
save_root_dir = os.path.join(os.getcwd(), 'tmp/')


# 获取所有套图的链接列表
def get_series_url_lists(url):
    resp = r.get(url)
    if resp is not None:
        result = resp.text
        bs = BeautifulSoup(result, 'html.parser')
        ul = bs.find('div', attrs={'class': 'tab_tj'})
        a_s = ul.find_all('a')
        for a in a_s:
            series_url_lists.append(a.get('href'))


# 获取某个套图里的所有图片
def fetch_all_series_pic(url):
    cur_page = 1
    while True:
        current_url = url
        if cur_page > 1:
            current_url = url.replace('.html', '_' + str(cur_page) + '.html')
        resp = r.get(current_url)
        if resp.status_code == 404:
            break
        else:
            if resp is not None:
                result = resp.text
                bs = BeautifulSoup(result, 'lxml')
                # 使用lxml来获取标题，用作文件夹名
                title_name = bs.find('div', attrs={'class': 'ptitle'}).h1.text
                save_dir = os.path.join(save_root_dir, title_name)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                # 使用CSS选择器选择图片结点
                imgs = bs.select('img.pic-large')
                for img in imgs:
                    download_pic(img.attrs.get('src'), save_dir)
                cur_page += 1


# 下载图片的方法
def download_pic(url, path):
    print("下载图片：" + url)
    try:
        pic_name = url.split('/')[-1]
        img_resp = r.get(url).content
        with open(path + '/' +pic_name, "wb+") as f:
            f.write(img_resp)
    except Exception as reason:
        print(str(reason))


if __name__ == '__main__':
    for url in theme_url_list:
        get_series_url_lists(url)
    for url in series_url_lists:
        fetch_all_series_pic(url)
