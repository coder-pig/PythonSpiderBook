"""
urllib.robotparser使用示例
"""

from urllib import robotparser

rp = robotparser.RobotFileParser()
# 设置rebots.txt文件的链接
rp.set_url('http://www.taobao.com/robots.txt')
# 读取rebots.txt文件并进行分析
rp.read()

url = 'https://www.douban.com'
user_agent = 'Baiduspider'
op_info = rp.can_fetch(user_agent, url)
print("Elsespider 代理用户访问情况：",op_info)

bdp_info = rp.can_fetch(user_agent, url)
print("Baiduspider 代理用户访问情况：",bdp_info)
user_agent = 'Elsespider'