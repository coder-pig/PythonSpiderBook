"""
爬取Gank.io API接口的数据到MySQL
"""
import requests as r
from bs4 import BeautifulSoup
import pymysql

# 接口地址
search_api_base_url = 'https://gank.io/api/v2/data/'

# 各种分类的表名：Android，iOS，休息视频，福利，拓展资源，前端，瞎推荐，App
category_list = ["android", "ios", "video", "meizi", "other", "fed", "random", "app"]

# 图片表名
pic_table_name = 'pics'

# 请求分类字段列表
type_list = ["Android", "iOS", "休息视频", "福利", "拓展资源", "前端", "瞎推荐", "App"]

# 表字段名
column_list = ('_id', 'createdAt', 'dsec', 'publishedAt', 'source', 'type', 'url', 'used', 'who')

# 图片表字段名
pic_column_list = ('_id', 'url')


# 创建数据库
def create_db():
    conn = pymysql.connect(host='localhost', user='root', password='Zpj12345', port=3306)
    cursor = conn.cursor()
    cursor.execute("Create Database If Not Exists gank Character Set UTF8MB4")
    conn.close()
    conn = pymysql.connect(host='localhost', user='root', password='Zpj12345', port=3306, db='gank')
    return conn


# 创建数据库表
def init_tables(c, table):
    c.execute(
        ("CREATE TABLE IF Not Exists {table}"
         "(_id CHAR(24) PRIMARY KEY,"
         "createdAt TEXT NOT NULL,"
         "dsec TEXT NOT NULL,"
         "publishedAt TEXT NOT NULL,"
         "source TEXT NOT NULL,"
         "type TEXT NOT NULL,"
         "url TEXT NOT NULL,"
         "used TEXT NOT NULL,"
         "who TEXT NOT NULL)").format(table=table))


# 创建图表
def init_pic_table(c, table):
    c.execute(
        ("CREATE TABLE IF Not Exists {table} "
         "(id INT AUTO_INCREMENT PRIMARY KEY,"
         "_id CHAR(24),"
         "url TEXT NOT NULL)").format(table=table))


# 把数据插入到数据库中
def insert_data(c, table, column, data):
    try:
        keys = ', '.join(column)
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        c.execute(sql, tuple(data))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


# 查询数据库表的方法
def query_data(c, table):
    try:
        sql = 'SELECT * FROM {table}'.format(table=table)
        c.execute(sql)
        print('共有 %d 行数据' % c.rowcount)
        row = c.fetchone()
        while row:
            print(row)
            row = c.fetchone()
    except Exception as e:
        print(e)


# 爬取接口数据的方法
def fetch_data(c, pos):
    page_count = 1
    while True:
        resp = r.get(search_api_base_url + type_list[pos] + '/50/' + str(page_count))
        result_json = resp.json()
        print("抓取：", resp.url)
        if len(result_json['results']) > 0:
            for result in result_json['results']:
                data_list = [result['_id'],
                             result['createdAt'],
                             result['desc'],
                             result['publishedAt'],
                             result.get('source', ''),
                             result['type'],
                             result['url'],
                             1 if result['used'] else 0,
                             result.get('who', '') if result.get('who', '') is not None else '']
                insert_data(c, category_list[pos], column_list, data_list)
                if 'images' in result:
                    for image in result['images']:
                        insert_data(c, pic_table_name, pic_column_list, [result['_id'], image])
            page_count += 1
        else:
            break


if __name__ == '__main__':
    db = create_db()
    cursor = db.cursor()
    # for category in category_list:
    #     init_tables(cursor, category)
    # init_pic_table(cursor, pic_table_name)
    # for i in range(0, len(category_list)):
    #     fetch_data(cursor, i)
    query_data(cursor, 'Android')
    cursor.close()
