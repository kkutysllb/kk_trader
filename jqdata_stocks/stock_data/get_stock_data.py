#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


from jqdatasdk import *
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
import time

auth('15619292819', 'Oms_2600')
pd.set_option('expand_frame_repr', False)

# 全局变量
root = '/Users/libing/Desktop/Projects/kk_trader/all_stock_data'

"""
获取股票数据并实时更新
"""


def init_db_stock_price(stock_type=None, stock_code=None):
    """
    初始化股票数据库
    :param stock_type: 股票类型：sh-沪市，sz-深市，cy-创业板，默认为None则不通过分市场获取
    :param stock_code: 股票代码，默认为None，则获取全量股票数据，如果指定为某个股票代码，则获取指定股票数据
    :return: 返回分市场统计的股票个数 total_num, sh_num, sz_num, cy_num
    """
    # 获取全市场所有股票代码列表
    stock_list = get_all_stock_code()

    # 分市场统计股票
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
    total_num = len(stock_list)
    sh_num = len(sh_code_list)
    sz_num = len(sz_code_list)
    cy_num = len(cy_code_list)

    # 股票代码未指定，但是股票市场类型指定
    if stock_code is None:
        if stock_type == 'sh':
            for code in sh_code_list:
                df = get_stock_price(code=code, freq='daily')
                export_stock_price(filename=code, data=df, data_type='price')
        if stock_type == 'sz':
            for code in sz_code_list:
                df = get_stock_price(code=code, freq='daily')
                export_stock_price(filename=code, data=df, data_type='price')
        if stock_type == 'cy':
            for code in cy_code_list:
                df = get_stock_price(code=code, freq='daily')
                export_stock_price(filename=code, data=df, data_type='price')
    else:
        df = get_stock_price(code=stock_code, freq='daily')
        export_stock_price(filename=stock_code, data=df, data_type='price')

    return total_num, sh_num, sz_num, cy_num


def get_all_stock_code():
    """
    获取A股市场所有股票标的代码
    :return: 返回一个列表，里面元素是A股市场所有股票代码
    """
    stocks = list(get_all_securities(types=['stock']).index)
    return stocks


def get_stock_price(code, freq='daily', start_date=None, end_date=None):
    """
    获取单个股票行情数据
    :param code: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param freq: 时间频率，默认取值为日K：daily
    :return: price_data,返回查询股票的行情数据，DataFrame格式
    """
    # 如果start_date为None， 则获取股票上市日期
    if start_date is None:
        start_date = get_security_info(code).start_date
    # 如果end_date为None， 则获取当前时间
    if end_date is None:
        end_date = datetime.datetime.today()
    price_data = get_price(security=code, start_date=start_date, end_date=end_date, frequency=freq, panel=False)
    return price_data


def get_stock_period_price(code, count, unit, end_dt):
    """
    获取其他周期股票行情数据
    :param code: 股票代码
    :param count: 相关周期获取的数据个数
    :param unit: 支持时间周期：'1m','5m', '15m', '30m', '60m', '120m', '1w', '1M
    :param end_dt: 数据获取截止时间
    :return: period_df，其他时间周期股票行情数据
    """
    period_df = get_bars(security=code,  # 股票代码
                         count=count,  # 获取的时间周期数据个数，本例取15分钟周期，所以一天就是16个周期
                         unit=unit,  # 时间周期单位，取值如上描述所示
                         fields=['date', 'open', 'close', 'high', 'low', 'volume', 'money'],  # 返回数据包含的字段
                         end_dt=end_dt  # 数据获取截止时间
                         )
    return period_df


def export_stock_price(filename, data, data_type, mode='w'):
    """
    导出股票行情数据到本地csv文件
    :param filename: 文件名
    :param data: 查询到的股票行情数据
    :param data_type: 股票数据类型，可以是行情数据price，也可以是财务数据finance
    :param mode: 写入模式：a-追加，w-新写
    :return:
    """
    file_root = os.path.join(root, data_type)
    # 拼接文件路径目录，如果路径上级目录不存在则创建上级目录
    try:
        if not os.path.exists(file_root):
            os.mkdir(file_root)
        file_path = file_root + '/' + filename + '.csv'
        data.index.names = ['date']  # 设置索引index为date
        try:
            # 追加写入模式
            if mode == 'a':
                data.to_csv(file_path, encoding='utf-8', header=False, mode=mode)
                # 删除重复数据
                data = pd.read_csv(file_path)  # 读取数据
                data.drop_duplicates(subset=['date'], inplace=True)  # 以时间戳为准删除重复值
                data.to_csv(file_path, index=False)  # 重新写入
            # 新写入模式
            else:
                data.to_csv(file_path, encoding='utf-8')
            print('已成功存储至: ', file_path)
        except Exception:
            print('写入模式输入错误：a-追加，w-新写')

    except Exception as e:
        print(e)


def get_data_from_csv(code, data_type):
    """
    从csv文件中获取数据
    :param code: 股票代码
    :param data_type: 股票数据类型，可以是行情数据price，也可以是财务数据finance
    :return: stock_data，返回从csv文件中获取的股票数据
    """
    file_root = os.path.join(root, data_type)
    file_path = file_root + '/' + code + '.csv'
    try:
        stock_data = pd.read_csv(filepath_or_buffer=file_path, encoding='utf-8')
        print('数据读取成功！')
        return stock_data
    except Exception as e:
        print(e)


def get_csv_price_data(code, start_date, end_date, col_index=None):
    """
    从本地数据库获取股票行情数据，按照时间自动筛选
    :param code: 股票代码
    :param start_date: 起始日期
    :param end_date: 终止日期
    :param col_index: list, 指定列索引，默认为None表示全量数据，传递列索引字符串列表
    :return: DataFrame，返回筛选后的行情数据
    """
    # 首先使用update更新数据
    update_stock_data(code=code, data_type='price')
    # 从本地获取筛选后的数据
    file_root = os.path.join(root, 'price')
    file_path = file_root + '/' + code + '.csv'
    # 如果start_date为None， 则获取股票上市日期
    # if start_date is None:
    #     start_date = get_security_info(code).start_date
    # 如果end_date为None， 则获取当前时间
    # if end_date is None:
    #     end_date = time.strptime(str(datetime.datetime.today()), '%Y-%m-%d')
    # 读取全量数据
    if col_index is None:
        data = pd.read_csv(filepath_or_buffer=file_path,
                           encoding='utf-8',
                           index_col=['date'])
    # 读取指定列数据
    else:
        data = pd.read_csv(filepath_or_buffer=file_path,
                           encoding='utf-8',
                           index_col=['date'],
                           usecols=col_index)
    return data[(data.index >= start_date) & (data.index <= end_date)]


def transfer_price_data(rule, data):
    """
    转换股票行情周期数据
    :param rule: 转换周期取值，参考pd.resample()方法的取值
    :param data: 行情数据
    :return: period_data， 返回一个转换后的周期行情数据，DataFrame格式
    """
    period_data = pd.DataFrame()
    period_data['open'] = data['open'].resample(rule, label='right').first()
    period_data['close'] = data['close'].resample(rule, label='right').last()
    period_data['high'] = data['high'].resample(rule, label='right').max()
    period_data['low'] = data['low'].resample(rule, label='right').min()
    period_data['volume'] = data['volume'].resample(rule, label='right').sum()
    period_data['money'] = data['money'].resample(rule, label='right').sum()

    return period_data


def get_stock_indicator(code, statdate, date=None):
    """
    获取指定股票的财务指标数据
    :param code: 股票代码
    :param statdate: 查询 statDate 指定的季度或者年份的财务数据
    :param date: 查询指定日期date收盘后所能看到的最近(对市值表来说, 最近一天, 对其他表来说, 最近一个季度)的数据
    :return: indicator_data，财务数据报表，DataFrame格式
    """
    indicator_data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=statdate)
    return indicator_data


def get_stock_valuation(code, statdate, date=None):
    """
    获取指定股票的财务指标数据
    :param code: 股票代码
    :param statdate: 查询 statDate 指定的季度或者年份的财务数据
    :param date: 查询指定日期date收盘后所能看到的最近(对市值表来说, 最近一天, 对其他表来说, 最近一个季度)的数据
    :return: valuation_data，估值数据报表，DataFrame格式
    """
    valuation_data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statdate)
    return valuation_data


# 使用shift函数计算涨跌幅
def calculate_change_pct(data):
    """
    计算股票收盘价涨跌幅数据和成交量变化数据： 使用pct_change()和shift()方法
    :param data: DataFrame，股票行情数据
    :return: new_data，DataFrame，带涨跌幅的股票行情数据
    """
    data['close_pct'] = data['close'].pct_change(1)
    data['volume_delta'] = data['volume'] - data['volume'].shift(1)
    new_data = data
    return new_data


# 更新股票数据
def update_stock_data(code, data_type):
    """
    更新股票数据，根据已有文件的时间戳自动更新
    :param code: 股票代码
    :param data_type: 数据类型，price或finance
    :return:
    """
    # 获取股票数据文件路径
    file_root = os.path.join(root, data_type)
    file_path = file_root + '/' + code + '.csv'
    if os.path.exists(file_path):
        # 如果文件存在则更新数据
        start_date = pd.read_csv(file_path, usecols=['date'])['date'].iloc[-1]
        data = get_stock_price(code=code,
                               freq='daily',
                               start_date=start_date,
                               end_date=None)

        export_stock_price(code, data, data_type, mode='a')
    else:
        # 如果文件不存在则创建
        data = get_stock_price(code=code,
                               freq='daily',
                               start_date=None,
                               end_date=None)
        export_stock_price(code, data, data_type)

    print("股票数据更新/创建成功: ", code)


def get_index_stock_list(index_symbol='000300.XSHG'):
    """
    获取指数成分股，指数表的代码查询: https://www.joinquant.com/indexData
    :param index_symbol: 指数代码, 默认为000300.XSHG，沪深300代码
    :return: list, 指数成分股列表
    """
    stocks = get_index_stocks(index_symbol=index_symbol)
    return stocks


if __name__ == '__main__':
    # 测试指数成分股获取
    st_list = get_index_stock_list()  # 获取沪深300成分股列表
    print(st_list)
