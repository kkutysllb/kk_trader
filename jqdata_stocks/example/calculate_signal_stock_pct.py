#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import jqdata_stocks.stock_data.get_stock_data as std


"""
计算单只股票的收益情况：单次收益率，累计收益率
"""
# 获取一支股票的行情数据
code = '600486.XSHG'
price_data = std.get_stock_price(code=code, freq='daily')
# price_data = std.get_csv_price_data(code=code, start_date='2022-01-14', end_date='2022-01-18')

# 存入本地csv文件中
std.export_stock_price(data=price_data, filename=code, data_type='price')

# 从本地csv文件中读取数据
# data = std.get_data_from_csv(code=code, data_type='price')

# 测试涨跌幅计算
# new_data = std.calculate_change_pct(price_data)
# print(new_data)

# 更新股票数据
# std.update_stock_data(code, 'price')

