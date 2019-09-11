"""
PyMongo库实战示例：爬取一号店关键词搜索结果保存到MongoDB中
"""
import pymongo
import requests as r
from lxml import etree

search_word = "羽毛球"
search_base_url = 'https://search.yhd.com/c0-0/k'


def search_goods(key):
    data_list = []
    resp = r.get(search_base_url + key)
    resp.encoding = 'utf-8'
    html = etree.HTML(resp.text)
    ul_list = html.xpath('//div[@id="itemSearchList"]/div')
    for ul in ul_list:
        # 商品名称
        title = ul.xpath('div//p[@class="proName clearfix"]/a/@title')[0]
        # 商品链接
        link = ul.xpath('div//p[@class="proName clearfix"]/a/@href')[0]
        # 商品价格
        price = ul.xpath('div//p[@class="proPrice"]/em/@yhdprice')[0]
        # 店铺名称
        store = ul.xpath('div//p[@class="storeName limit_width"]/a/@title')
        store_name = store[0] if len(store) > 0 else ''
        # 评论数
        comment_count = ul.xpath('div//p[@class="proPrice"]/span[@class="comment"]/a/text()')[1]
        # 好评率
        favorable_rate = ul.xpath('div//span[@class="positiveRatio"]/text()')[0]
        data_list.append({'title': title, 'link': 'https:' + link, 'price': price, 'store_name': store_name, 'comment_count': comment_count,
                          'favorable_rate': favorable_rate})
    return data_list


if __name__ == '__main__':
    conn = pymongo.MongoClient(host='localhost', port=27017)
    search_goods(search_word)
    db = conn['yhd']
    collection = db['羽毛球']
    search_result_list = search_goods(search_word)
    collection.insert_many(search_result_list)
    conn.close()
