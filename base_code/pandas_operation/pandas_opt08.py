#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import pandas as pd
import os

# pd.set_option('display.max_rows', 1000)  # 最大显示1000行数据
# pd.set_option('display.max_columns', 10)  # 最大显示10列数据
pd.set_option('expand_frame_repr', False)

file_location = '../../test_data/basic-trading-data/stock_data'


"""
批量导入数据
"""
# os.walk()方法可以遍历文件夹下的所有文件和子文件夹，递归遍历
file_list = []
for root, dirs, files in os.walk(file_location):
   for filename in files:
       file_path = os.path.join(root, filename)  # 路径拼接
       file_path = os.path.abspath(file_path)  # 获取绝对路径
       if file_path.endswith('.csv'):
           file_list.append([filename, file_path])


# all_data = pd.DataFrame()
# for fp in file_list:
#     df = pd.read_csv(filepath_or_buffer=fp,
#                      skiprows=1,
#                      encoding='gbk',
#                      # parse_dates=['交易日期']
#                      )
#     all_data = all_data.append(df, ignore_index=True)
#
# 对数据进行排序，按照交易日期和股票代码两列进行排序
# all_data.sort_values(by=['股票代码', '交易日期'], inplace=True)

# 保存到本地csv文件
# all_data.to_csv(path_or_buf=file_location + '/all_data.csv',
#                 encoding='utf-8',
#                 index=False)


"""
保存到本地HDF文件
"""
h5_store = pd.HDFStore(path=file_location + '/all_stock.h5', mode='w')
for filename, file_path in sorted(file_list):
    stock_code = filename.split('.')[0]
    # print(stock_code, filename, file_path)
    df = pd.read_csv(filepath_or_buffer=file_path, skiprows=1, encoding='gbk', parse_dates=['交易日期'], index_col=['交易日期'])
    # 存储数据到h5文件，每个数据库文件的表名为stock_code
    h5_store[stock_code] = df
h5_store.close()  # 写完文件记得关闭

"""
从HDF文件中读取数据
"""
h5_store = pd.HDFStore(path=file_location + '/all_stock.h5', mode='r')

# 产看h5数据库中有多少个表名，通过keys()方法实现
print(h5_store.keys())

# 读取某个key指向的数据，可以使用get()方法，也可以像字典一样直接通过key值获取
key_list = h5_store.keys()
for key in key_list:
    print(h5_store.get(key.split('/')[1]))

h5_store.close()  # 读完文件也要记得关闭
