"""
itchat模拟Get请求
"""

import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

get_url = "http://gank.io/api/data/" + urllib.request.quote("福利") + "/1/1"
get_resp = urllib.request.urlopen(get_url)
get_result = json.loads(get_resp.read().decode('utf-8'))
# 这里后面的参数用于格式化Json输出格式
get_result_format = json.dumps(get_result, indent=2,
                               sort_keys=True,  ensure_ascii=False)
print(get_result_format)