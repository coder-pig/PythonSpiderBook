"""
csv库使用代码示例
"""

import csv
import os

save_file_name_1 = os.path.join(os.getcwd(), '1.csv')
save_file_name_2 = os.path.join(os.getcwd(), '2.csv')
save_file_name_3 = os.path.join(os.getcwd(), '3.csv')

data_1 = [['id', '姓名', '性别', '年龄', '工作'],
          [1, '小明', '男', '18', '学生'],
          [2, '小红', '女', '24', '老师'],
          [3, '小光', '男', '25', 'Python工程师']]

headers = ['id', '姓名', '性别', '年龄', '工作']
data_2 = [{'id': 1, '姓名': '小明', '性别': '男', '年龄': '18', '工作': '学生'},
          {'id': 2, '姓名': '小红', '性别': '女', '年龄': '24', '工作': '老师'},
          {'id': 3, '姓名': '小光', '性别': '男', '年龄': '25', '工作': 'Python工程师'}]

# 单行写入示例
with open(save_file_name_1, 'w', newline='') as f:
    writer = csv.writer(f)
    for row in data_1:
        writer.writerow(row)

# 多行写入
with open(save_file_name_2, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data_1)

# 字典写入
with open(save_file_name_3, 'w', newline='') as f:
    # 标头在这里传入，作为第一行数据
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    for row in data_2:
        writer.writerow(row)



if __name__ == '__main__':
    with open(save_file_name_1) as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['姓名'])
        # reader = csv.reader(f)
        # print(list(reader)[0][1])
        # for row in reader:
        #     print(reader.line_num, row)

