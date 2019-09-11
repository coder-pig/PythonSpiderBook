"""
selenium使用示例
"""
from selenium import webdriver

browser = webdriver.Chrome()  # 调用本地的Chrome浏览器
browser.get('http://www.baidu.com')  # 请求页面，会打开一个浏览器窗口
html_text = browser.page_source  # 获得页面代码
# browser.quit()  # 关闭浏览器
print(html_text)