#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


from pyalgotrade import strategy
from pyalgotrade_tushare import tools, barfeed
from pyalgotrade.technical import ma
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
"""
使用开源框架pyalgotrade回测数据
"""


def safe_round(value, digits):
    """
    调整数据小数位
    :param value: 原始数据
    :param digits: 调整小数位的个数
    :return:
    """
    if value is not None:
        value = round(value, digits)
    return value


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, sma_short, sma_long):
        """
        策略回测初始化属性
        :param feed: 股票行情数据
        :param instrument: 股票代码
        :param sma_short: 双均线短周期值
        :param sma_long: 双均线长周期值
        """
        super(MyStrategy, self).__init__(feed, 100000)  # 10000表示现金额
        self.__position = None
        self.__instrument = instrument
        # 计算smaPeriod天简单移动平均线
        # self.setUseAdjustedValues(True)  # 是否使用复权价
        self.__sma_short = ma.SMA(feed[instrument].getPriceDataSeries(), sma_short)
        self.__sma_long = ma.SMA(feed[instrument].getPriceDataSeries(), sma_long)

    def getSMAShort(self):  # 获取SMA短周期均线值
        return self.__sma_short

    def getSMALong(self):  # 获取SMA长周期均线值
        return self.__sma_long

    def onEnterOk(self, position):  # 买入成功
        execInfo = position.getEntryOrder().getExecutionInfo()
        # self.info("BUY at ¥%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):  # 买入取消
        self.__position = None

    def onExitOk(self, position):  # 卖出成功
        execInfo = position.getExitOrder().getExecutionInfo()
        # self.info("SELL at ¥%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):  # 卖出取消
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # 当长周期均线值为None时，直接返回，策略不执行
        if self.__sma_long[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            # 买入条件：当短周期上穿长周期时，买入
            if self.__sma_short[-1] > self.__sma_long[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 100, True)  # 100表示买入100股
        # 卖出条件：当短周期下穿长周期时，且持仓不为0就卖出.
        elif self.__sma_short[-1] < self.__sma_long[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def run_strategy(sma_short, sma_long):
    # 从本地获取数据信息
    instruments = ['600111']
    feeds = tools.build_feed(instruments=instruments, fromYear=2020, toYear=2022, storage='hisdata')

    # Evaluate the strategy with the feed.
    # myStrategy = MyStrategy(feeds, instruments[0], smaPeriod)
    # myStrategy.run()
    # print("Final portfolio value: ¥%.2f" % myStrategy.getBroker().getEquity())

    # Evaluate the strategy with the feed's bars.
    myStrategy = MyStrategy(feeds, instruments[0], sma_short, sma_long)

    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)

    # 策略效果可视化
    plt = plotter.StrategyPlotter(myStrategy)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("SMA_short", myStrategy.getSMAShort())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("SMA_long", myStrategy.getSMALong())
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    # Run the strategy.
    myStrategy.run()
    myStrategy.info("Final portfolio value: ¥%.2f" % myStrategy.getResult())

    # Plot the strategy.
    plt.plot()


run_strategy(5, 10)

