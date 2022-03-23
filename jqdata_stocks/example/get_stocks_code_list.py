#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import jqdata_stocks.stock_data.get_stock_data as std
"""
分类获取股票代码列表
"""
# 获取所有上市公司股票代码
stock_list = std.get_all_stock_code()
# print(stock_list)
print(len(stock_list))
sh_code_list = []
sz_code_list = []
cy_code_list = []
for code in stock_list:
    if code.startswith('6'):
        sh_code_list.append(code)
    if code.startswith('0'):
        sz_code_list.append(code)
    if code.startswith('3'):
        cy_code_list.append(code)

print(len(sh_code_list), len(sz_code_list), len(cy_code_list))