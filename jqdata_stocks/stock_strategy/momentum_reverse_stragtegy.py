#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import jqdata_stocks.stock_strategy.base as strat
import jqdata_stocks.stock_strategy.momentum_strategy as mmt
import pandas as pd
import matplotlib.pyplot as plt

"""
计算动量策略（反向）
"""


def momentum_reverse(data_concat, shift_n=1, top_n=1):
    """
    计算动量因子(反向), 等权重下的投资组合收益率
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
    buy_signal = mmt.get_pct_sorted(-1 * shift_return, top_n=top_n)
    sell_signal = mmt.get_pct_sorted(shift_return, top_n=top_n)
    signal = buy_signal - sell_signal

    # 计算投资组合收益率
    profolio_result = strat.calculate_protfolio_profit(data=shift_return, signal=signal, n_stock=top_n * 2)

    # 评估策略收益情况：总收益率，年化收益率，最大回撤，夏普比率
    strat.evaluate_strategy(profolio_result)

    return profolio_result


if __name__ == '__main__':
    # 测试动量策略（反向） 获取股票数据 get_stocks_data()
    stocks = ['600111.XSHG', '000831.XSHE', '600392.XSHG']
    df = mmt.get_stocks_data(stocks=stocks, start_date='2021-01-01', end_date='2022-01-01', col_index=['date', 'close'])
    returns = momentum_reverse(data_concat=df, shift_n=1, top_n=1)

    # 可视化
    returns['cum_profit'].plot()
    plt.show()
