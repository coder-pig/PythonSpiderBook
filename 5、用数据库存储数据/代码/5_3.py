"""
Excel操作库xlwt，xlrd库使用代码示例
"""

import xlwt
import xlrd
import os

if __name__ == '__main__':
    # 新建一个工作薄
    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('工作表1',cell_overwrite_ok=True)
    # sheet.write(0, 0, '姓名')
    # sheet.write(0, 1, '学号')
    # sheet.write(1, 0, '小猪')
    # sheet.write(1, 1, '1')
    # workbook.save(os.path.join(os.getcwd(), 'result.xlsx'))
    workbook = xlrd.open_workbook(os.path.join(os.getcwd(), 'result.xlsx'))
    sheet = workbook.sheets()[0]
    # 获得行数
    row_count = sheet.nrows
    for row in range(0, row_count):
        print(sheet.row_values(row))