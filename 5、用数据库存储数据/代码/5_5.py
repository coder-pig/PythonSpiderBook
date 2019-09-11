"""
PyMongo库的基本操作示例
"""

import pymongo

# 1.连接MongoDB数据库(默认没有密码，如果设置了密码要调用db.auth("用户名","密码")）
conn = pymongo.MongoClient(host='localhost', port=27017)
# 或者采用MongoDB连接字符串的形式也可以：
# conn = pymongo.MongoClient('mongodb://localhost:27017')

# 2.选择数据库，也可以使用conn['test']这一的方式选择，等价
# db = conn.test
#
# # 3.选择collection
# collection = db.user
# print(collection)


# # 4.创建数据库
# db = conn['test_db']
#
# # 5.创建collection
# collection = db['test_collection']

# 6.插入一条数据
# db = conn['test_db']
# collection = db['test_collection']
# dic = {'id': '1', 'name': 'Jay'}
# collection.insert_one(dic)

db = conn.test_db
collection = db.test_collection

# 7.插入多条数据（传入一个字典的列表）
# data_list = [{'id': '2', 'name': 'Tom'},{'id': '3', 'name': 'Jack'}]
# collection.insert_many(data_list)


# 8.查找数据

# 查找一条
# print(collection.find_one({'name': 'Tom'}))


# 查找多条
# data_list = [{'id': '4', 'name': 'Mary'},{'id': '4', 'name': 'Lucy'}]
# collection.insert_many(data_list)
# results = collection.find({'id':'4'})
# for result in results:
#     print(result)

# 正则匹配
# for result in collection.find({'name':{'$regex':'^J.*'}}):
#     print(result)

# 9.修改数据

# 方法一：需要整条记录参与
# person = collection.find_one({'name':'Jack'})
# person['name'] = 'Jacky'
# collection.update({'name':'Jack'}, person)

# 方法二：部分修改字段内容的方式
# result = collection.update_one({'name': 'Tom'}, {'$set': {"name": "Tony"}})
# print(result)
# print("匹配的数据条数：",result.matched_count, "受影响的数据条数：",result.modified_count)

# 10.删除数据
# result = collection.delete_many({'id': {'$lte': 3}})
# print("删除的数据条数：", result.deleted_count)

# 11.计数
# print("数据库中有%d条记录。" % collection.find().count())

# 12.排序
# data_list = [{'id': 2, 'name': 'Tom'},{'id': 3, 'name': 'Jack'},{'id': 5, 'name': 'Daisy'}]
# collection.insert_many(data_list)
# # 降序排列，升序可以传入pymongo.ASCENDING
# results = collection.find().sort('id', pymongo.DESCENDING)
# for result in results:
#     print(result)

# 13.偏移
results = collection.find().sort('id', pymongo.ASCENDING).skip(1)
for result in results:
    print(result)

