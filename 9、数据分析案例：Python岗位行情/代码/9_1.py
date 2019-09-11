"""
numpy使用代码示例
"""

import numpy as np

print("1.生成一个一维数组:\n %s" % np.array([1, 2]))
print("2.生成一个二维数组:\n %s" % np.array([[1, 2], [3, 4]]))
print("3.生成一个元素初始值都为0的，4行3列矩阵:\n %s" % np.zeros((4, 3)))
print("4.生成一个元素初始值都为1的，3行4列矩阵:\n %s" % np.ones((3, 4)))
print("5.创建一个空数组，元素为随机值：\n %s" % np.empty([2, 3], dtype=int))
a1 = np.arange(0, 30, 2)
print("6.生成一个等间隔数字的数组:\n %s" % a1)
a2 = a1.reshape(3, 5)
print("7.转换数组的维度，比如把一维的转为3行5列的数组:\n %s" % a2)

# ndarray常用属性
print("8.a1的维度: %d \t a2的维度：%d" % (a1.ndim, a2.ndim))
print("9.a1的行列数：%s \t a2的行列数：%s" % (a1.shape, a2.shape))
print("10.a1的元素个数：%d \t a2的元素个数：%d" % (a1.size, a2.size))
print("11.a1的元素数据类型：%s 数据类型大小：%s" % (a1.dtype, a1.itemsize))
