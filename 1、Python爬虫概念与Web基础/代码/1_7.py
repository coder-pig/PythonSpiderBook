"""
urllib使用cookie代码示例
"""

import urllib.request
from http import cookiejar

# ============ 获得Cookie ============

# 1.实例化CookieJar对象


cookie = cookiejar.CookieJar()

# 2.创建Cookie处理器
handler = urllib.request.HTTPCookieProcessor(cookie)

# 3.通过CookieHandler创建opener
opener = urllib.request.build_opener(handler)

# 4.打开网页
resp = opener.open("http://www.baidu.com")

for i in cookie:
    print("Name = %s" % i.name)
    print("Name = %s" % i.value)

# ============ 保存Cookie到文件 ============
# 1.用于保存cookie的文件
cookie_file = "cookie.txt"

# 2.创建MozillaCookieJar对象保存Cookie
cookie = cookiejar.MozillaCookieJar(cookie_file)

# 3.创建Cookie处理器
handler = urllib.request.HTTPCookieProcessor(cookie)

# 4.通过CookieHandler创建opener
opener = urllib.request.build_opener(handler)

# 5.打开网页
resp = opener.open("http://www.baidu.com")

# 6.保存Cookie到文件中，参数依次是:
# ignore_discard：即使cookies将被丢弃也将它保存下来
# ignore_expires：如果在该文件中cookies已存在，覆盖原文件写入
cookie.save(ignore_discard=True, ignore_expires=True)

# ============ 读取Cookie文件 ============

cookie_file = "cookie.txt"

# 1.创建MozillaCookieJar对象保存Cookie
cookie = cookiejar.MozillaCookieJar(cookie_file)

# 2.从文件中读取cookie内容
cookie.load(cookie_file, ignore_expires=True, ignore_discard=True)

handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
resp = opener.open("http://www.baidu.com")
print(resp.read().decode('utf-8'))

