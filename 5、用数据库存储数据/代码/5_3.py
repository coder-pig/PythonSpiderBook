"""
redis-py库的基本操作示例
"""
import redis

# ====================== 连接Redis ============================

# 1.普通连接
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

# 2.连接池（一般）
# redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、
# 释放连接的开销。这种方式实现多个Redis实例共享一个连接池
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='Zpj12345')
r = redis.StrictRedis(connection_pool=pool)

# 3.管道
# redis-py,默认情况下，每次都会进行连接池的连接和断开。若是想一次执行多条命令，进行
# 事务性操作，就要用管道。(虽然有这个功能，但是不建议使用，慢而且没什么必要。)
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.StrictRedis(connection_pool=pool)
pipe = r.pipeline(transaction=True)
# 执行多条命令
pipe.execute()

# ====================== 通用操作 ============================

r.delete('name')  # 根据键删除redis中的任意数据类型
r.exists('name')  # 检测redis的键是否存在
r.keys(pattern='*')  # 根据* ？等通配符匹配获取redis的键
r.expire('name', time=3000)  # 为某个键设置超时时间
r.rename('name', 'name1')  # 重命名键
r.move('name', 'db1')  # 将redis的某个值移动到指定的db下
r.randomkey()  # 随机获取一个redis的键（不删除）
r.type('name')  # 获取键对应值的类型
r.dbsize()  # 获得当前数据库中键的数目
r.ttl('name')  # 获得键的过期时间
r.flushdb()  # 删除当前选择数据库中所有的键
r.flushall()  # 删除所有数据库中的所有键


# ====================== String操作 ============================

# 设置键值对，默认不存在则创建，存在则修改
# set(name, value, ex=None, px=None, nx=False, xx=False)
#      ex，过期时间（秒）
#      px，过期时间（毫秒）
#      nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
#      xx，如果设置为True，则只有name存在时，当前set操作才执行

r.set('name', value)    #设置值
r.setnx('name',value)   #如果name这个键不存在，把这个键对应的值设置为value
r.setex('name', value, time) #设置值，并指定此键值的有效期
r.setrange(name, offset, value) #修改字符串内容，从指定字符串索引开始向后替换
r.mset({"name3":'xxx', "name4":'xxx'})   #批量设置值
r.msetnx({"name3":'xxx', "name4":'xxx'}) #键都不存在是才批量赋值

r.get('name')   # 获取值
r.getset('name', 'yyy') # 为键为name的值赋值为yyy，并返回上次的值xxx
r.mget(['name1','name2']) # 返回多个键对应的值
r.getrange(key, start, end) # 返回键为name的值的字符串，截取索引为start到end的字符
r.strlen("name") #返回name对应值的字节长度（一个汉字3个字节）

r.append('name',value)  # 为键为name的值后追加value
r.incr('name',amount) # 字符串转化为整型，再自增属性name对应的值，当属性name不存在时，
                      # 则创建name＝amount，否则，则自增,amount为自增数(整数)
r.decr('name',amount)   #自减name对应的值,当name不存在时,则创建name＝amount，
                        #否则，则自减，amount为自增数(整数)
r.substr('name',start, end) # 返回键为name的值的字符串截取索引为start到end的字符

