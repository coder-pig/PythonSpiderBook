"""
itchat模拟Post请求
"""
import urllib.request
import urllib.parse
import json

post_url = "http://xxx.xxx.login"
phone = "13555555555"
password = "111111"
values = {
    'phone': phone,
    'password': password
}
data = urllib.parse.urlencode(values).encode(encoding='utf-8')
req = urllib.request.Request(post_url, data)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())    # Byte结果转Json
print(json.dumps(result, sort_keys=True,
                 indent=2, ensure_ascii=False)) # 格式化输出Json


