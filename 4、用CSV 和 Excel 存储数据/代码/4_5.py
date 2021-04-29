"""
pymysql库使用代码示例
"""

import pymysql


# 连接数据库
def db_connect():
    conn = pymysql.connect(host='localhost', user='root', password='Zpj12345', port=3306, db='test')
    return conn


# 创建一个数据库表
def create_table(c):
    c.execute(
        "CREATE TABLE IF Not Exists person(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(30) NOT NULL DEFAULT '',age INT,sex CHAR(2))")


# 插入数据
def insert_data(c, table, data_dict):
    try:
        keys = ', '.join(data_dict.keys())
        values = ', '.join(['%s'] * len(data_dict))
        sql = 'INSERT INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        print(sql)
        c.execute(sql, tuple(data_dict.values()))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


# 删除数据
def delete_data(c, table, condition):
    try:
        sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
        c.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


# 修改数据
def update_data(c, table, old, new):
    try:
        sql = 'UPDATE {table} SET {old} WHERE {new}'.format(table=table, old=old, new=new)
        c.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


# 查看数据
def inquire_data(c, table, condition):
    try:
        sql = 'SELECT * FROM {table} WHERE {condition}'.format(table=table, condition=condition)
        c.execute(sql)
        print('共有 %d 行数据' % c.rowcount)
        row = c.fetchone()
        while row:
            print(row)
            row = c.fetchone()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    db = db_connect()
    cursor = db.cursor()
    create_table(cursor)
    # data = {
    #     'name': '大黄',
    #     'age': '17',
    #     'sex': '男',
    # }
    # insert_data(cursor, 'person', data)
    # delete_data(cursor, 'person', 'age < 10')
    # update_data(cursor, 'person', 'age = 10', "name = '小红'")
    inquire_data(cursor, 'person', 'age > 15')
    db.close()
