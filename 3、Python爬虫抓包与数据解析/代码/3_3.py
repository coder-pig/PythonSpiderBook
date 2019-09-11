"""
正则使用示例
"""

import re

ret = re.match(r'^(\d{4})-(\d{3,8})$', '0756-3890993')
print(ret.group())
print(ret.group(0))
print(ret.group(1))
print(ret.group(2))

str_count = "您的网站被访问了10000次"
match = re.match(r"^您的网站被访问了(\d{1,6})次$", str_count)
print(match.group(1))

