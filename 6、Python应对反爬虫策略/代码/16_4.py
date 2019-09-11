"""
selenium爬取简单网无聊图示例
"""
import os
from selenium import webdriver
import redis
import requests as r
from bs4 import BeautifulSoup

# 请求基地址
base_url = 'http://jandan.net/pic'
# 图片的保存路径
pic_save_path = os.path.join(os.getcwd(), 'JianDan/')
# 图片需要，作为Reids键用
pic_count = 0

# 下载图片用headers
pic_headers = {
    'Host': 'wx2.sinaimg.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36 '
}


# 打开浏览器模拟请求
def browser_get():
    browser = webdriver.Chrome()
    browser.get(base_url)
    html_text = browser.page_source
    page_count = get_page_count(html_text)
    # 循环拼接URL访问
    for page in range(page_count, 0, -1):
        page_url = base_url + '/page-' + str(page)
        print('解析：' + page_url)
        browser.get(page_url)
        html = browser.page_source
        get_meizi_url(html)
    # 没有更多了关闭浏览器
    browser.quit()


# 获取总页码
def get_page_count(html):
    bs = BeautifulSoup(html, 'lxml')
    page_count = bs.find('span', attrs={'class': 'current-comment-page'})
    return int(page_count.get_text()[1:-1]) - 1


# 获取每页的图片
def get_meizi_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    ol = soup.find('ol', attrs={'class': 'commentlist'})
    href = ol.findAll('a', attrs={'class': 'view_img_link'})
    global pic_count
    for a in href:
        dan_redis.set(str(pic_count), a['href'])
        pic_count += 1


# 下载图片
def download_pic(url):
    correct_url = url
    if url.startswith('//'):
        correct_url = url[2:]
    if not url.startswith('http'):
        correct_url = 'http://' + correct_url
    print("下载：", correct_url)
    try:
        resp = r.get(correct_url, headers=pic_headers).content
        pic_name = correct_url.split("/")[-1]
        with open(pic_save_path + pic_name, "wb+") as f:
            f.write(resp)
    except (OSError, r.ConnectionError, r.HTTPError, Exception) as reason:
        print(str(reason))


if __name__ == '__main__':
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='Zpj12345', db=1)
    dan_redis = redis.StrictRedis(connection_pool=pool)
    if not os.path.exists(pic_save_path):
        os.makedirs(pic_save_path)
    browser_get()
    results = dan_redis.mget(dan_redis.keys())
    for result in results:
        download_pic(result.decode('utf-8'))
    print("图片下载完毕！")
