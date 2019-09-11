"""
Selenium+Tesserocr实现自动登陆知乎
"""
import os
from selenium import webdriver
import requests as r
import time
from PIL import Image
from aip import AipOcr
from hashlib import md5
import base64

zhihu_login_url = 'https://www.zhihu.com/signup'

config = {
    'appId': 'd4ed8d211abd4f20b3xxe0f55xxx173f',
    'apiKey': 'Nk3RSGAh0gFEGdoFC7GxxaCQ',
    'secretKey': '63TyYDkI5R0x21tDsCxxBoF8EEmiDfEd'
}
client = AipOcr(**config)

# 超级鹰参数
cjy_params = {
    'user': 'CoderPig',
    'pass2': md5('zpj12345'.encode('utf8')).hexdigest(),
    'softid': '897137',
}

# 超级鹰请求头
cjy_headers = {
    'Connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
}


# 打开浏览器模拟请求
def auto_login():
    browser = webdriver.Chrome()
    while True:
            browser.get(zhihu_login_url)
            # 判断是否处于注册页(底部有登录字样，是的话点击跳转)
            signup_switch_bt = browser.find_element_by_xpath('//div[@class="SignContainer-switch"]/span')
            if signup_switch_bt.text == '登录':
                signup_switch_bt.click()
                # 输入用户名
            username_input = browser.find_element_by_xpath('//input[@name="username"]')
            username_input.send_keys('xx@qq.com')
            # 输入密码
            password_input = browser.find_element_by_xpath('//input[@name="password"]')
            password_input.send_keys('xxx')
            # 等待一会儿，等验证码刷出来
            time.sleep(5)
            # 判断是否包含英文字符验证码，是的话处理，否则跳出
            if is_elements_existed(browser, "//div[@class='Captcha-englishContainer']"):
                if len(browser.find_element_by_xpath("//img[@class='Captcha-englishImg']").get_attribute('src')) > 30:
                    code_img = browser.find_element_by_xpath('//img[@alt="图形验证码"]')
                    code = cjy_fetch_code(base64.b64decode(code_img.get_attribute('src')[22:].replace("%0A", "")), 1902)
                    # 输入验证码
                    code_input = browser.find_element_by_xpath('//input[@name="captcha"]')
                    code_input.send_keys(code)
                    time.sleep(2)
                    # 点击登录按钮
                    login_bt = browser.find_element_by_xpath('//button[@type="submit"]')
                    login_bt.click()
                    time.sleep(3)
                    break
            else:
                continue
    time.sleep(10)
    # 打印当前的网页链接，以此判断是否跳转成功
    print(browser.current_url)


# 判断xpath定位的元素是否存在
def is_elements_existed(browser, element):
    flag = True
    try:
        browser.find_element_by_xpath(element)
        return flag
    except:
        flag = False
        return flag


# 读取图片
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


# 百度OCR文字识别
def baidu_ocr(file):
    image = get_file_content(file)
    # 调用通用文字识别, 图片参数为本地图片
    result = client.basicAccurate(image)
    print(result)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])


# 重置图片大小，并进行灰度和二值化处理
def resize_pic(file, width=1200, height=480):
    img = Image.open(file)
    try:
        new_img = img.resize((width, height), Image.BILINEAR)
        # 转灰度处理
        new_img = new_img.convert('L')
        # 二值化处理
        table = []
        for i in range(256):
            if i < 150:
                table.append(0)
            else:
                table.append(1)
        # 通过表格转换为二进制图片
        new_img = new_img.point(table, "1")
        new_img.save(os.path.join(os.getcwd(), os.path.basename(file)))
    except Exception as e:
        print(e)


# 超级鹰识别验证码
def cjy_fetch_code(im, codetype):
    cjy_params.update({'codetype': codetype})
    files = {'userfile': ('ccc.jpg', im)}
    resp = r.post('http://upload.chaojiying.net/Upload/Processing.php', data=cjy_params, files=files,
                  headers=cjy_headers).json()
    print(resp)
    if resp.get('err_no', 0) == 0:
        return resp.get('pic_str')


if __name__ == '__main__':
    # resize_pic('code.png')
    # baidu_ocr('code.png')
    # im = open('code.png', 'rb').read()
    # print(cjy_fetch_code(im, 1902))
    auto_login()
