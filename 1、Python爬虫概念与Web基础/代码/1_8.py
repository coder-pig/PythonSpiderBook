"""
urllib.parse.urlparse和urlsplit函数使用示例
"""
import urllib.parse

urp = urllib.parse.urlparse('https://docs.python.org/3/search.html?q=parse&check_keywords=yes&area=default')
print('urlparse执行结果：', urp)
# 可以通过.的方式获取某个部分
print('urp.scheme：', urp.scheme)
print('urp.netloc：', urp.netloc)

urp = urllib.parse.urlsplit('https://docs.python.org/3/search.html?q=parse&check_keywords=yes&area=default')
print('urlsplit执行结果：', urp)
