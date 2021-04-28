"""
urllib修改请求头代码示例
"""
import urllib.request

# 修改头信息
novel_url = "http://www.biqukxs.com/book/1.html"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/63.0.3239.84 Safari/537.36',
           'Host': 'www.biqukxs.com',
           'Referer': 'http://www.biqukxs.com/',
           'Connection': 'keep-alive'}
novel_req = urllib.request.Request(novel_url, headers=headers)
novel_resp = urllib.request.urlopen(novel_req)
print(novel_resp.read().decode('gbk'))
