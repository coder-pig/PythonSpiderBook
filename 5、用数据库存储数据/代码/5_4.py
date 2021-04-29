"""
xlwt和xlrd库实战示例：爬取豆瓣音乐top 250
"""
import xlwt
import xlrd
import requests as r
import os
from bs4 import BeautifulSoup

base_url = 'https://music.douban.com/top250'

headers = {
    'Host': 'music.douban.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

save_file = 'douban.xlsx'

# 提取音乐信息的方法
def fetch_data(start_pos):
    result = []
    resp = r.get(base_url, headers=headers, params={'start': str(start_pos)}).text
    bs = BeautifulSoup(resp, 'lxml')
    trs = bs.select('tr.item')
    for tr in trs:
        tds = tr.select('td')
        # 歌名
        music_name = tds[1].div.a.text.strip().split("\n")[0]
        # 歌曲封面
        music_pic_url = tds[0].img.get('src')
        # 歌手
        msg_list = tds[1].div.p.text.split('/')
        singer = msg_list[0]
        # 发行时间
        public_time = msg_list[1]
        # 分类
        albums = ''
        for album in msg_list[2:]:
            albums += album.strip() + "/"
        # 评分
        spans = tds[1].select('div div span')
        score = spans[1].text
        # 评分人数
        score_num = (spans[2].text.replace(' ','').replace('\n','').replace('人评价','')[1:-1])
        # 歌曲详情页
        music_detail_url = tds[0].a.get('href')
        result.append([music_name, music_pic_url, singer, public_time, albums, score, score_num, music_detail_url])
    return result

class ExcelHelper:
    def __init__(self):
        if not os.path.exists(save_file):
            # 1.创建工作薄
            self.workbook = xlwt.Workbook()
            # 2.创建工作表，第二个参数用于确认同一个cell单元是否可以重设值
            self.sheet = self.workbook.add_sheet(u"豆瓣音乐Top 250", cell_overwrite_ok=True)
            # 3.初始化表头
            self.headTitles = [u'歌名', u'歌曲封面', u'歌手', u'发行时间', u'分类', u'评分', u'评分人数', u'歌曲详情页']
            for i, item in enumerate(self.headTitles):
                self.sheet.write(0, i, item, self.style('Monaco', 220, bold=True))
            self.workbook.save(save_file)

    # 参数依次是：字体名称，字体高度，是否加粗
    def style(self, name, height, bold=False):
        style = xlwt.XFStyle()  # 赋值style为XFStyle()，初始化样式
        font = xlwt.Font()  # 为样式创建字体样式
        font.name = name
        font.height = height
        font.bold = bold
        return style

    # 往单元格里插入数据
    def insert_data(self, data_group):
        try:
            xlsx = xlrd.open_workbook(save_file)  # 读取Excel文件
            table = xlsx.sheets()[0]  # 根据索引获得表
            row_count = table.nrows  # 获取当前行数，新插入的数据从这里开始
            count = 0
            for data in data_group:
                for i in range(len(data)):
                    self.sheet.write(row_count + count, i, data[i], self.style('Monaco', 220, bold=True))
                count += 1
        except Exception as e:
            print(e)
        finally:
            self.workbook.save(save_file)

    # 读取Excel里的数据
    def read_data(self):
        xlsx = xlrd.open_workbook(save_file)
        table = xlsx.sheets()[0]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        # 从第一行开始，0是表头
        for i in range(1, nrows):
            # 读取某行数据
            row_value = table.row_values(i)
            print(row_value)


if __name__ == '__main__':
    data_group = []
    offsets = [x for x in range(0, 250, 25)]
    for offset in offsets:
        data_group += fetch_data(offset)
    print(data_group)
    excel = ExcelHelper()
    excel.insert_data(data_group)
    excel.read_data()