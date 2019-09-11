"""
urllib.parse.urlencode函数使用代码示例
"""
from urllib import parse

params = {
    'q': 'parse',
    'check_keywords': 'yes',
    'area': 'default'
}
url = 'https://docs.python.org/3/search.html?' + parse.urlencode(params)
print("拼接后的URL：", url)
