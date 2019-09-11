"""
urllib下载图片
"""
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# pic_url = "https://www.baidu.com/img/bd_logo1.png"
# pic_resp = urllib.request.urlopen(pic_url,context=context)
# pic = pic_resp.read()
# with open("bg_logo.png", "wb") as f:
#     f.write(pic)

urllib.request.urlretrieve('https://www.baidu.com/img/bd_logo1.png', 'bd_logo.png')


