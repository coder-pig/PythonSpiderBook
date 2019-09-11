"""
urllib.parse.parse_qs和parse_qsl函数使用代码示例
"""
from urllib import parse

params_str = 'q=parse&check_keywords=yes&area=default'

print("parse_qs 反序列化结果：", parse.parse_qs(params_str))
print("parse_qsl 反序列化结果：", parse.parse_qsl(params_str))
