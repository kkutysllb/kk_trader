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
数据时间周期转换，resample()方法
"""
df = pd.read_hdf(path_or_buf=file_location + '/all_stock.h5', key='sh600000')

rule_type = '1W'  # 1W表示一周，也就是意味着转为周线周期
df_week = pd.DataFrame()
df_week['收盘价'] = df[['收盘价']].resample(rule=rule_type).last()  # last()方法表示取最后一天
df_week['开盘价'] = df[['开盘价']].resample(rule=rule_type).first()  # first()方法表示取第一天
df_week['最高价'] = df[['最高价']].resample(rule=rule_type).max()  # max()方法表示取最大的一天
df_week['最低价'] = df[['最低价']].resample(rule=rule_type).min()  # min()方法表示取最小的一天
df_week['成交量'] = df[['成交量']].resample(rule=rule_type).sum()  # sum()表示求和
df_week['成交额'] = df[['成交额']].resample(rule=rule_type).sum()  # sum()表示求和

print(df_week)
