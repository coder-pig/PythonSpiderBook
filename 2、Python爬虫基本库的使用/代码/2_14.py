"""
爬取笔趣看的小说脚本示例
"""

import urllib
import urllib.request
import urllib.parse
from lxml import etree
from urllib import error
import lxml.html
import os
import time

# 小说站点的URL
novel_base_url = 'http://www.biqukan.com'

# 拉取小说的URL
novel_url = urllib.parse.urljoin(novel_base_url, '/0_790/')

# 每章小说的链接
chapter_url_list = []

# 小说的保存文件夹
novel_save_dir = os.path.join(os.getcwd(), 'novel_cache/')

# 请求头
headers = {
    'Host': 'www.biqukan.com',
    'Referer': 'http://www.biqukan.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 获取章节链接列表
def fetch_chapter_urls():
    req = urllib.request.Request(url=novel_url, headers=headers)
    html = lxml.html.parse(urllib.request.urlopen(req))
    hrefs = html.xpath('//dd/a/@href')
    # 过滤前面的最新章节列表和无用章节
    for href in hrefs[16:]:
        chapter_url_list.append(urllib.parse.urljoin(novel_base_url, href))

# 解析每个页面获得章节正文
def parsing_chapter(url):
    req = urllib.request.Request(url=url, headers=headers)
    html = lxml.html.parse(urllib.request.urlopen(req))
    title = html.xpath('//h1/text()')[0]
    contents = html.xpath('//*[@id="content"]/text()')
    content = ''
    for i in contents:
        content += i.strip()
    save_novel(title, content)

# 把章节正文写到本地
def save_novel(name, content):
    try:
        with open(novel_save_dir + name + '.txt', "w+") as f:
            f.write(content.strip())
    except (error.HTTPError, OSError) as reason:
        print(str(reason))
    else:
        print("下载完成：" + name)


if __name__ == '__main__':
    # 判断存储的文件夹是否存在，不存在新建
    if not os.path.exists(novel_save_dir):
        os.mkdir(novel_save_dir)
    # 爬取小说文章链接列表
    fetch_chapter_urls()
    # 遍历抓取所有的小说内容
    for chapter in chapter_url_list:
        # 定时休眠1s防止ip被封
        time.sleep(1)
        parsing_chapter(chapter)