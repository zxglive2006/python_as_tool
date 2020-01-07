# encoding: UTF-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import moving_average as ma

pd.set_option("display.width", 120)
# 设定字体类型，用于正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_tsingtao_close():
    TsingTao = pd.read_csv(r"./data/TsingTao.csv")
    TsingTao.index = TsingTao.iloc[:, 1]
    TsingTao.index = pd.to_datetime(TsingTao.index, format="%Y-%m-%d")
    TsingTao = TsingTao.iloc[:, 2:]
    return TsingTao.Close


def show_sma():
    Close = get_tsingtao_close()
    # plt.subplot(111)
    # plt.plot(Close, 'k')
    # plt.xlabel('date')
    # plt.ylabel('Close')
    # plt.title("2014年青岛啤酒股票收盘价时序图")
    Sma5 = ma.sma_cal(Close, 5)
    print(Sma5.tail())
    plt.plot(Close[4:], label="Close", color="g")
    plt.plot(Sma5[4:], label="Sma5", color="r", linestyle="dashed")
    plt.title("青岛啤酒收盘价与简单移动平均线")
    plt.ylim(35, 50)
    plt.legend()


def show_wma():
    b = np.array([1, 2, 3, 4, 5])
    w = b / sum(b)
    print(w)
    Close = get_tsingtao_close()
    m1Close = Close[0:5]
    wec = w * m1Close
    print(sum(wec))
    Wma5 = ma.wma_cal(Close, w)
    for i in range(4, len(Wma5)):
        Wma5[i] = sum(w * Close[(i-4):(i+1)])
    print(Wma5[2:7])
    plt.plot(Close[4:], label="Close", color="g")
    plt.plot(Wma5[4:], label="Wma5", color="r", linestyle="dashed")
    plt.title("青岛啤酒收盘价与加权移动平均线")
    plt.ylim(35, 50)
    plt.legend()


def show_ewma():
    Close = get_tsingtao_close()
    Ema5 = ma.ewma_cal(Close, 5, 0.2)
    print(Ema5.head())
    print(Ema5.tail())
    plt.plot(Close[4:], label="Close", color="k")
    plt.plot(Ema5[4:], label="Ema5", color="g", linestyle="-.")
    plt.title("青岛啤酒收盘价指数移动平均线")
    plt.ylim(35, 50)
    plt.legend()


def show_chinabank():
    CBClose = get_CBClose()
    print(CBClose.describe())
    Close15 = CBClose["2015"]
    Sma10 = ma.sma_cal(Close15, 10)
    print(Sma10.tail())
    weight = np.array(range(1, 11)) / sum(range(1, 11))
    Wma10 = ma.wma_cal(Close15, weight)
    print(Wma10.tail(n=3))
    expo = 2 / (len(Close15) + 1)
    Ema10 = ma.ewma_cal(Close15, 10, expo)
    print(Ema10.tail(n=3))
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.plot(Close15[10:], label="Close", color="k")
    plt.plot(Sma10[10:], label="Sma10", color="r", linestyle="dashed")
    plt.plot(Wma10[10:], label="Wma10", color="b", linestyle=":")
    plt.plot(Ema10[10:], label="Ema10", color="G", linestyle="-.")
    plt.title("中国银行价格均线")
    plt.ylim(3.5, 5.5)
    plt.legend()
    plt.show()


def show_chinabank_2():
    CBClose = get_CBClose()
    Close15 = CBClose["2015"]
    Sma5 = ma.sma_cal(Close15, 5)
    Sma30 = ma.sma_cal(Close15, 30)
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.plot(Close15[30:], label="Close", color="k")
    plt.plot(Sma5[30:], label="Sma5", color="b", linestyle="dashed")
    plt.plot(Sma30[30:], label="Sma30", color="r", linestyle=":")
    plt.title("中国银行股票价格的长短期均线")
    plt.ylim(3.5, 5.5)
    plt.legend()
    plt.show()


def trade_single_ma():
    """
    单均线交易策略
    :return:
    """
    cb_close = get_CBClose()
    cb_sma10 = ma.sma_cal(cb_close, 10)
    sma_signal = pd.Series(0, cb_close.index)
    for i in range(10, len(cb_close)):
        if all([cb_close[i] > cb_sma10[i], cb_close[i - 1] < cb_sma10[i - 1]]):
            sma_signal[i] = 1
        elif all([cb_close[i] < cb_sma10[i], cb_close[i - 1] > cb_sma10[i - 1]]):
            sma_signal[i] = -1
    sma_trade = sma_signal.shift(1).dropna()
    sma_buy = sma_trade[sma_trade == 1]
    print(sma_buy.head())
    sma_sell = sma_trade[sma_trade == -1]
    print(sma_sell.head())
    cb_ret = cb_close / cb_close.shift(1) - 1
    sma_ret = (cb_ret * sma_trade).dropna()
    print(sma_ret.head())
    cum_stock = np.cumprod(1 + cb_ret[sma_ret.index[0]:]) - 1
    cumTrade = np.cumprod(1 + sma_ret) - 1
    cumdate = pd.DataFrame({
        'cumTrade': cumTrade,
        'cumStock': cum_stock
    })
    print(cumdate.iloc[-6:, :])
    # SmaRet[SmaRet == (-0)] = 0
    smaWinrate = len(sma_ret[sma_ret > 0]) / len(sma_ret[sma_ret != 0])
    print(smaWinrate)
    plt.plot(cum_stock, label='cumStock', color='k')
    plt.plot(cumTrade, label='cumTrade', color='r', linestyle=':')
    plt.title('股票本身与均线交易的累计收益率')
    plt.legend()


def trade_double_ma():
    """
    双均线交易策略
    :return:
    """
    CBClose = get_CBClose()
    print(CBClose.head())
    Ssma5 = ma.sma_cal(CBClose, 5)
    Lsma30 = ma.sma_cal(CBClose, 30)
    SLSignal = pd.Series(0, index=Lsma30.index)
    for i in range(1, len(Lsma30)):
        if all([Ssma5[i] > Lsma30[i], Ssma5[i - 1] < Lsma30[i - 1]]):
            SLSignal[i] = 1
        elif all([Ssma5[i] < Lsma30[i], Ssma5[i - 1] > Lsma30[i - 1]]):
            SLSignal[i] = -1
    print(SLSignal[SLSignal==1])
    print(SLSignal[SLSignal==-1])
    SLTrade = SLSignal.shift(1)
    Long = pd.Series(0, index=Lsma30.index)
    Long[SLTrade == 1] = 1
    CBRet = CBClose / CBClose.shift(1) - 1
    LongRet = (Long * CBRet).dropna()
    winLrate = len(LongRet[LongRet > 0]) / len(LongRet[LongRet != 0])
    print(winLrate)
    Short = pd.Series(0, index=Lsma30.index)
    Short[SLTrade == -1] = -1
    ShortRet = (Short * CBRet).dropna()
    winSrate = len(ShortRet[ShortRet > 0]) / len(ShortRet[ShortRet != 0])
    print(winSrate)
    SLtradeRet = (SLTrade * CBRet).dropna()
    winRate = len(SLtradeRet[SLtradeRet > 0]) / len(SLtradeRet[SLtradeRet != 0])
    print(winRate)
    cumLong = np.cumprod(1 + LongRet) - 1
    cumShort = np.cumprod(1 + ShortRet) - 1
    cumSLtrade = np.cumprod(1 + SLtradeRet) - 1
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(cumSLtrade, label='cumSLtrade', color='k')
    plt.plot(cumLong, label='cumLong', color='b', linestyle='dashed')
    plt.plot(cumShort, label='cumShort', color='r', linestyle=':')
    plt.title('长短期均线交易累计收益率')
    plt.legend()


def get_CBClose():
    ChinaBank = pd.read_csv(r"./data/ChinaBank.csv")
    ChinaBank.index = ChinaBank.iloc[:, 1]
    ChinaBank.index = pd.to_datetime(ChinaBank.index, format="%Y-%m-%d")
    ChinaBank = ChinaBank.iloc[:, 2:]
    return ChinaBank.Close


def show_macd():
    """
    MACD交易策略
    :return:
    """
    CBClose = get_CBClose()
    DIF = ma.ewma_cal(CBClose, 12, 2 / (1 + 12)) - ma.ewma_cal(CBClose, 26, 2 / (1 + 26))
    print(DIF.tail(n=3))
    DEA = ma.ewma_cal(DIF, 9, 2 / (1 + 9))
    print(DEA.tail())
    MACD = DIF - DEA
    print("MACD tail")
    print(MACD.tail(n=3))
    # plt.subplot(211)
    # plt.plot(DIF['2015'], label='DIF', color='k')
    # plt.plot(DEA['2015'], label='DEA', color='b', linestyle='dashed')
    # plt.title("信号线DIF与DEA")
    # plt.legend()
    # plt.subplot(212)
    # plt.bar(left=MACD['2015'].index, height=MACD['2015'], label='MACD', color='r')
    # plt.legend()
    macddata = pd.DataFrame()
    macddata['DIF'] = DIF['2015']
    macddata['DEA'] = DEA['2015']
    macddata['MACD'] = MACD['2015']
    import candle
    ChinaBank = pd.read_csv(r"./data/ChinaBank.csv")
    candle.candleLinePlots(
        ChinaBank['2015'],
        candleTitle='中国银行2015年日K线图',
        splitFigures=True,
        Data=macddata,
        ylabel='MACD'
    )


def trade_macd():
    """
    根据macd产生信号交易
    :return:
    """
    CBClose = get_CBClose()
    DIF = ma.ewma_cal(CBClose, 12, 2 / (1 + 12)) - ma.ewma_cal(CBClose, 26, 2 / (1 + 26))
    DEA = ma.ewma_cal(DIF, 9, 2 / (1 + 9))
    macdSignal = pd.Series(0, index=DIF.index[1:])
    for i in range(1, len(DIF)):
        if all([DIF[i] > DEA[i] > 0.0, DIF[i - 1] < DEA[i - 1]]):
            macdSignal[i] = 1
        elif all([DIF[i] < DEA[i] < 0.0, DIF[i - 1] > DEA[i - 1]]):
            macdSignal[i] = -1
    print(macdSignal.tail())
    macdTrade = macdSignal.shift(1)
    CBRet = CBClose / CBClose.shift(1) - 1
    macdRet = (CBRet * macdTrade).dropna()
    macdWinRate = len(macdRet[macdRet > 0]) / len(macdRet[macdRet != 0])
    print(macdWinRate)


def trade_multi():
    cb_close = get_CBClose()
    cb_sma10 = ma.sma_cal(cb_close, 10)
    SmaSignal = pd.Series(0, cb_close.index)
    for i in range(10, len(cb_close)):
        if all([cb_close[i] > cb_sma10[i], cb_close[i - 1] < cb_sma10[i - 1]]):
            SmaSignal[i] = 1
        elif all([cb_close[i] < cb_sma10[i], cb_close[i - 1] > cb_sma10[i - 1]]):
            SmaSignal[i] = -1
    Ssma5 = ma.sma_cal(cb_close, 5)
    Lsma30 = ma.sma_cal(cb_close, 30)
    SLSignal = pd.Series(0, index=Lsma30.index)
    for i in range(1, len(Lsma30)):
        if all([Ssma5[i] > Lsma30[i], Ssma5[i - 1] < Lsma30[i - 1]]):
            SLSignal[i] = 1
        elif all([Ssma5[i] < Lsma30[i], Ssma5[i - 1] > Lsma30[i - 1]]):
            SLSignal[i] = -1
    DIF = ma.ewma_cal(cb_close, 12, 2 / (1 + 12)) - ma.ewma_cal(cb_close, 26, 2 / (1 + 26))
    DEA = ma.ewma_cal(DIF, 9, 2 / (1 + 9))
    macdSignal = pd.Series(0, index=DIF.index[1:])
    for i in range(1, len(DIF)):
        if all([DIF[i] > DEA[i] > 0.0, DIF[i - 1] < DEA[i - 1]]):
            macdSignal[i] = 1
        elif all([DIF[i] < DEA[i] < 0.0, DIF[i - 1] > DEA[i - 1]]):
            macdSignal[i] = -1
    AllSignal = SmaSignal + SLSignal + macdSignal
    for i in AllSignal.index:
        if AllSignal[i] > 1:
            AllSignal[i] = 1
        elif AllSignal[i] < -1:
            AllSignal[i] = -1
        else:
            AllSignal[i] = 0
    print(AllSignal[AllSignal == 1])
    print(AllSignal[AllSignal == -1])
    tradSig = AllSignal.shift(1).dropna()
    cb_close = cb_close[-len(tradSig):]
    asset = pd.Series(0.0, index=cb_close.index)
    cash = pd.Series(0.0, index=cb_close.index)
    share = pd.Series(0, index=cb_close.index)
    entry = 3
    cash[:entry] = 20000
    while entry < len(cb_close):
        cash[entry] = cash[entry - 1]
        if all([cb_close[entry - 1] >= cb_close[entry - 2],
                cb_close[entry - 2] >= cb_close[entry - 3],
                AllSignal[entry - 1] != -1]):
            share[entry] = 1000
            cash[entry] = cash[entry] - 1000 * cb_close[entry]
            break
        entry += 1
    i = entry + 1
    while i < len(tradSig):
        cash[i] = cash[i - 1]
        share[i] = share[i - 1]
        flag = 1
        if tradSig[i] == 1:
            share[i] = share[i] + 3000
            cash[i] = cash[i] - 3000 * cb_close[i]
        if all([tradSig[i] == -1, share[i] > 0]):
            share[i] = share[i] - 1000
            cash[i] = cash[i] + 1000 * cb_close[i]
        i += 1
    plt.subplot(411)
    plt.title("2014-2015年上:中国银行均线交易账户")
    plt.plot(cb_close, color='b')
    plt.ylabel("Pricce")
    plt.subplot(412)
    plt.plot(share, color='b')
    plt.ylabel("Share")
    plt.ylim(0, max(share) + 1000)
    plt.subplot(413)
    plt.plot(asset, label="asset", color='r')
    plt.ylabel("Asset")
    plt.ylim(min(asset) - 5000, max(asset) + 5000)
    plt.subplot(414)
    plt.plot(cash, label="cash", color='g')
    plt.ylabel("Cash")
    plt.ylim(0, max(cash) + 5000)
    TradeReturn = (asset[-1] - 20000) / 20000
    print(TradeReturn)
    plt.show()


if __name__ == '__main__':
    print("ch30")
    # show_chinabank()
    # show_chinabank_2()
    # trade_single_ma()
    trade_multi()
