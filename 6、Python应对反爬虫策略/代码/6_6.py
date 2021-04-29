"""
破解极验滑动验证码示例
"""
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from lxml import etree
import requests as r
import re
import PIL.Image as image

full_image_file = 'full.jpg'
cut_image_file = 'cut.jpg'
bilibili_login_url = 'https://passport.bilibili.com/login'
url_fetch_regex = re.compile('url\(\"(.*?)\"\);')
bg_postion_regex = re.compile('position: (.*?)px (.*?)px;')


def auto_login():
    # 输入账号密码
    input_user = browser.find_element_by_xpath('//input[@id="login-username"]')
    input_user.send_keys("xxx")
    input_passwd = browser.find_element_by_xpath('//input[@id="login-passwd"]')
    input_passwd.send_keys("xxx")
    # 验证码自动验证
    location_lists = fetch_images()
    offset = (get_offset(restore_images(cut_image_file, location_lists[0]),
                         restore_images(full_image_file, location_lists[1])))
    print("滑块偏移量：", offset)
    b_track = get_track(offset - 6)
    b_slider = get_slider()
    move_slider(b_slider, b_track)
    time.sleep(1)
    # 点击登录
    login_bt = browser.find_element_by_xpath('//a[@class="btn btn-login"]')
    login_bt.click()


# 下载缺失的图片，每个小方块的坐标
def fetch_images():
    html = etree.HTML(browser.page_source)
    cut_bg = html.xpath('//div[@class="gt_cut_bg gt_show"]/div')
    full_bg = html.xpath('//div[@class="gt_cut_fullbg gt_show"]/div')
    # 提取两个打乱后顺序的webp图片URL替换为jpg
    cut_bg_url = url_fetch_regex.search((cut_bg[0].get('style'))).group(1).replace('webp', 'jpg')
    full_bg_url = url_fetch_regex.search((full_bg[0].get('style'))).group(1).replace('webp', 'jpg')
    with open(cut_image_file, 'wb+') as f: f.write(r.get(cut_bg_url).content)
    with open(full_image_file, 'wb+') as f: f.write(r.get(full_bg_url).content)
    # 采集图片定位坐标
    cut_bg_location_list = []
    full_bg_location_list = []
    for cut in cut_bg:
        cut_result = bg_postion_regex.search(cut.get('style'))
        full_result = bg_postion_regex.search(cut.get('style'))
        cut_bg_location_list.append({'x': int(cut_result.group(1)), 'y': int(cut_result.group(2))})
        full_bg_location_list.append({'x': int(full_result.group(1)), 'y': int(full_result.group(2))})
    return cut_bg_location_list, full_bg_location_list


# 合并还原图片
def restore_images(file, location_list):
    im = image.open(file)
    # 分段分成上面的图和下面的图列表
    below_list = []
    above_list = []
    for location in location_list:
        if location['y'] == -58:
            above_list.append(im.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
        if location['y'] == 0:
            below_list.append(im.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))

    # 创建一个一样大的图片
    new_im = image.new('RGB', (260, 116))
    # 遍历坐标粘贴上面的图片
    x_offset = 0
    for im in above_list:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    # 遍历坐标粘贴下面的图片
    x_offset = 0
    for im in below_list:
        new_im.paste(im, (x_offset, 58))
        x_offset += im.size[0]
    # 保存图片
    new_im.save(file)
    return new_im


# 判断两个像素点是否相同
def is_pixel_equal(img1, img2, x, y):
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    scope = 20  # 像素阀值
    return abs(pix1[0] - pix2[0] < scope) and abs(pix1[1] - pix2[1] < scope) and abs(pix1[2] - pix2[2] < scope)


# 获得缺口偏移量
def get_offset(img1, img2):
    left = 60
    for x in range(left, img1.size[0]):
        for y in range(img1.size[1]):
            if not is_pixel_equal(img1, img2, x, y):
                return x
    return left


# 获取滑块
def get_slider():
    while True:
        try:
            slider = browser.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
            break
        except:
            time.sleep(0.5)
    return slider


# 滑块匀速滑动轨迹构造
def get_track(distance):
    track = []
    current = 0
    while current < distance:
        move = distance / 4
        current += move
        track.append(round(move))
    return track


# 先加速后减速滑动轨迹构造
def get_person_track(distance):
    track = []
    current = 0
    mid = distance * 4 / 5  # 减速阈值
    t = 0.2  # 计算间隔
    v = 0  # 初速度
    while current < distance:
        a = 2 if current < mid else -3
        v0 = v  # 初速度v0
        v = v0 + a * t  # 当前速度
        move = v0 * t + 1 / 2 * a * t * t  # 移动距离
        current += move
        track.append(round(move))
    return track


# 滑块滑动的方法
def move_slider(slider, track):
    ActionChains(browser).click_and_hold(slider).perform()
    for x in track:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.05)
    ActionChains(browser).release().perform()


if __name__ == '__main__':
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 20)
    browser.get(bilibili_login_url)
    # 休眠2秒等待登录页加载完毕
    time.sleep(1)
    auto_login()
    time.sleep(5)
    print(browser.current_url)
    browser.quit()
