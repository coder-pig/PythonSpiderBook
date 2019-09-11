"""
urllib.parse.urlunparse，urlunsplit和urljoin函数使用示例
"""
import urllib.parse

url = urllib.parse.urlunparse(['https','docs.python.org', '/3/search.html', 'q=parse&check_keywords=yes&area=default' , '', ''])
print('urlunparse函数拼接的URL：',url)

url = urllib.parse.urlunsplit(['https','docs.python.org', '/3/search.html', 'q=parse&check_keywords=yes&area=default',''])
print('urlunsplit函数拼接的URL：',url)

url = urllib.parse.urljoin('https://docs.python.org','/3/search.html')
url = urllib.parse.urljoin(url,'?q=parse&check_keywords=yes&area=default')
print('urljoin函数拼接的URL：',url)