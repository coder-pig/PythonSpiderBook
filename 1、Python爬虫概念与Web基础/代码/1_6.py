"""
urllib配置代理示例
"""

import urllib.request

# 使用ip代理
ip_query_url = "http://ip.chinaz.com/"

# 1.创建代理处理器，ProxyHandler参数是一个字典{类型:代理ip:端口}
proxy_support = urllib.request.ProxyHandler({'http': '219.141.153.43:80'})

# 2.定制，创建一个opener
opener = urllib.request.build_opener(proxy_support)

# 3.安装opener
urllib.request.install_opener(opener)

# 请求头
headers = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (X11; Linux x86_64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/63.0.3239.84 Safari/537.36',
    'Host': 'ip.chinaz.com'
}


req = urllib.request.Request(ip_query_url, headers=headers)
resp = urllib.request.urlopen(req, timeout=20)
html = resp.read().decode('utf-8')
print(html)
