# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class FirstspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLPipeline():
    def __init__(self):
        self.host = 'localhost'
        self.database = 'bcy'
        self.user = 'root'
        self.password = 'Jay12345'
        self.port = 3306

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(["%s"] * len(data))
        sql = "INSERT INTO draw (%s) VALUES (%s)" % (keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
