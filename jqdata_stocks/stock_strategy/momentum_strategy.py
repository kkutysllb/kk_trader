#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import jqdata_stocks.stock_data.get_stock_data as std
import jqdata_stocks.stock_strategy.base as strat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
计算动量策略（正向）
"""


def get_stocks_data(stocks, start_date, end_date, col_index):
    """
    获取股票相关列行情数据，整合拼接为一个DataFrame
    :param stocks: list, 股票代码列表
    :param start_date: 股票数据查询起始日期
    :param end_date: 股票数据查询终止日期
    :param col_index: list, 要查询的股票数据列索引
    :return:
    """

    # 创建股票收盘价的容器
    data_concat = pd.DataFrame()

    # 获取股票数据, 预览股票数据
    for code in stocks:  # 测试取前10个股票数据
        print("========= code ===========", code)
        stock_data = std.get_csv_price_data(code=code, start_date=start_date, end_date=end_date,
                                            col_index=col_index)
        # 将close列索引转换为股票代码
        stock_data.columns = [code]
        # 数据拼接
        data_concat = pd.concat([data_concat, stock_data], axis=1)  # axis=1表示纵向拼接

    return data_concat


def momentum(data_concat, shift_n=1, top_n=1):
    """
    计算动量因子, 等权重下的投资组合收益率
    :param data_concat: DataFrame, 投资组合标的整合数据
    :param shift_n: 计算过去美n个月的收益率，默认为过去每个月的收益率，shift_n=1
    :param top_n: 排名前几的设定，默认为排面前1的设定top_n=1
    :return: DataFrame, profolio_result投资组合每n个月的收益率数据
    """
    # 计算过去n个月的收益率
    # 简单收益率计算: 期末值/期初值 - 1
    # 对数收益率计算: log(期末值/期初值)

    # 设置索引为datetime格式
    data_concat.index = pd.to_datetime(data_concat.index)
    # 转换为原始数据周期为月
    data_month = data_concat.resample('M').last()

    shift_return = data_month / data_month.shift(shift_n) - 1

    # 生成交易信号
    buy_signal = get_pct_sorted(shift_return, top_n=top_n)
    sell_signal = get_pct_sorted(-1 * shift_return, top_n=top_n)
    signal = buy_signal - sell_signal

    # 计算投资组合收益率
    profolio_result = strat.calculate_protfolio_profit(data=shift_return, signal=signal, n_stock=top_n * 2)

    # 评估策略收益情况：总收益率，年化收益率，最大回撤，夏普比率
    strat.evaluate_strategy(profolio_result)

    return profolio_result


# 对收益率数据按行排序
def get_pct_sorted(data, top_n=1):
    """
    对收益率数据按行排序
    :param data: DataFrame, 数据整合后的DataFrame
    :param top_n: 取排前几名的设定
    :return:
    """
    # 初始化信号容器
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    print(data)
    # 对data的每一行进行遍历，找到最大值，并用bool函数标注信号0或1
    for index, row in data.iterrows():
        # 按行排序找出每行最大值，标注为1，其余标注为0
        print(row)
        exit()
        signals.loc[index] = row.isin(row.nlargest(top_n)).astype(np.int32)
    return signals


if __name__ == '__main__':
    # 测试 获取股票数据 get_stocks_data()
    stocks = ['600111.XSHG', '000831.XSHE', '600392.XSHG']
    df = get_stocks_data(stocks=stocks, start_date='2021-01-01', end_date='2022-01-01', col_index=['date', 'close'])
    returns = momentum(df, shift_n=1)

    # # 可视化
    # returns.plot()
    # plt.show()
