"""
requests抓取微信公众号文章的图片，音视频
"""
import requests
from lxml import etree
import time
import os

# 资源的保存文件夹
save_dir = os.path.join(os.getcwd(), 'tmp')

# 测试文章的URL
test_url = 'https://mp.weixin.qq.com/s/4oLnJvfGCZneoErkrh0sHw'

# 语音获取的基URL
music_res_url = 'http://res.wx.qq.com/voice/getvoice'

# 视频获取的接口URL
video_parse_url = 'http://v.ranks.xin/video-parse.php'

# 微信公众号文章请求头
headers = {
    'Host': 'mp.weixin.qq.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 视频获取接口的请求头
video_parse_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Host': 'v.ranks.xin',
    'Referer': 'http://v.ranks.xin/',
    'X-Requested-With': 'XMLHttpRequest'
}


# 获取标题
def get_title(content):
    return content.xpath("//h2[@class='rich_media_title']/text()")[0].strip()


# 解析下载图片
def get_pic(content, path):
    img_list = content.xpath("//img/@data-src")
    for img in img_list:
        download_pic(img, path)


# 解析获得音频
def get_sound(content, path):
    sound_list = content.xpath("//mpvoice/@voice_encode_fileid")
    for sound in sound_list:
        download_sound(sound, path)


# 解析获得视频
def get_video(content, path):
    video_list = content.xpath("//iframe/@data-src")
    for video in video_list:
        download_video(video, path)


# 下载图片的方法
def download_pic(url, path):
    print("下载图片：" + url)
    try:
        pic_name = str(int(time.time()))  # 使用当前时间戳作为图片名字
        fmt = url.split('=')[-1]  # 图片格式
        img_resp = requests.get(url).content
        with open(path + pic_name + "." + fmt, "wb+") as f:
            f.write(img_resp)
    except Exception as reason:
        print(str(reason))


# 下载音频的方法
def download_sound(file_id, path):
    try:
        sound_resp = requests.get(music_res_url, params={'mediaid': file_id, 'voice_type': '1'})
        if sound_resp is not None:
            music_name = str(int(time.time())) + '.mp3'  # 使用当前时间戳作为音频名字
            print("开始下载音频: " + sound_resp.url)
            with open(path + music_name, "wb+") as f:
                f.write(sound_resp.content)
                print("音频下载完成:" + music_name)
    except Exception as reason:
        print(str(reason))


# 下载视频的方法
def download_video(url, path):
    print("开始解析视频链接：" + url)
    video_resp = requests.get(video_parse_url, headers=video_parse_headers, params={'url': url})
    if video_resp is not None:
        video_url = video_resp.json()['data'][0]['url']
        print("解析完成，开始下载视频:" + video_url)
        try:
            video_name = str(int(time.time())) + '.mp4'  # 使用当前时间戳作为视频名字
            video_resp = requests.get(video_url).content
            if video_resp is not None:
                with open(path + video_name, "wb+") as f:
                    f.write(video_resp)
                    print("视频下载完成:" + video_name)
        except Exception as reason:
            print(str(reason))


if __name__ == '__main__':
    while True:
        print("请输入你要抓取的微信文章链接：(输出Q回车或者按Ctrl+C可以退出～)")
        input_url = input()
        if input_url == 'Q':
            exit()
        else:
            resp = requests.get(url=input_url.strip(), headers=headers).text
            html = etree.HTML(resp)
            title = get_title(html)
            res_save_dir = os.path.join(save_dir, title)
            if not os.path.exists(res_save_dir):
                os.makedirs(res_save_dir)
            get_pic(html,res_save_dir)
            get_sound(html,res_save_dir)
            get_video(html,res_save_dir)
            print("所有资源下载完成！")