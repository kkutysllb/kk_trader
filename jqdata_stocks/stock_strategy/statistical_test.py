#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import jqdata_stocks.stock_data.get_stock_data as std
import jqdata_stocks.stock_strategy.ma_strategy as ma
import matplotlib.pyplot as plt
from scipy import stats


def ttest(data_return):
    """
    对策略收益进行t检验
    :param data_return: DataFrame，策略单次收益率数据样本
    :return: t_value, p_value
    """
    # 调用假设检验ttest函数，scipy库
    t, p = stats.ttest_1samp(a=data_return,  # 数据样本
                             popmean=0,  # 期望值0，表示没有收益
                             nan_policy='omit'
                             )
    t_value = t
    p_value = p / 2
    print('t_value: ', t_value)
    print('p_value: ', p_value)
    print("是否可以拒绝[H0]收益均值=0：", p_value < 0.05)

    return t_value, p_value


if __name__ == '__main__':
    # 获取某只股票的单次收益率
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    for code in stocks:
        print(code)
        df = std.get_csv_price_data(code=code, start_date='2018-01-01', end_date='2022-01-01')
        # 调用双均线策略
        df = ma.tow_ma_strategy(df)
        # 策略的单次收益率数据样本
        returns = df['profit_pct']

        # 绘制一下分布图，用于观察
        # plt.hist(returns, bins=30)
        # plt.show()

        # 对数据样本进行t检验
        ttest(data_return=returns)