#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import os

root = '/Users/libing/Desktop/Projects/kk_trader/all_stock_data'
type = 'price'
file_root = os.path.join(root, type)
file_path = file_root + '/' + '600111.xshg' + '.csv'
print(file_path)