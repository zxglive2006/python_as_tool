# encoding: UTF-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import movingAverage as ma

pd.set_option("display.width", 120)
# 设定字体类型，用于正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def show_sma():
    TsingTao = pd.read_csv(r"./data/TsingTao.csv")
    TsingTao.index = TsingTao.iloc[:,1]
    TsingTao.index = pd.to_datetime(TsingTao.index, format="%Y-%m-%d")
    TsingTao = TsingTao.iloc[:, 2:]
    print(TsingTao.head(n=3))
    Close = TsingTao.Close
    # plt.subplot(111)
    # plt.plot(Close, 'k')
    # plt.xlabel('date')
    # plt.ylabel('Close')
    # plt.title("2014年青岛啤酒股票收盘价时序图")
    Sma5 = ma.smaCal(Close, 5)
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
    TsingTao = pd.read_csv(r"./data/TsingTao.csv")
    TsingTao.index = TsingTao.iloc[:, 1]
    TsingTao.index = pd.to_datetime(TsingTao.index, format="%Y-%m-%d")
    TsingTao = TsingTao.iloc[:, 2:]
    print(TsingTao.head(n=3))
    Close = TsingTao.Close
    m1Close = Close[0:5]
    wec = w * m1Close
    print(sum(wec))
    Wma5 = ma.wmaCal(Close, w)
    for i in range(4, len(Wma5)):
        Wma5[i] = sum(w * Close[(i-4):(i+1)])
    print(Wma5[2:7])
    plt.plot(Close[4:], label="Close", color="g")
    plt.plot(Wma5[4:], label="Wma5", color="r", linestyle="dashed")
    plt.title("青岛啤酒收盘价与加权移动平均线")
    plt.ylim(35, 50)
    plt.legend()


def show_ewma():
    TsingTao = pd.read_csv(r"./data/TsingTao.csv")
    TsingTao.index = TsingTao.iloc[:, 1]
    TsingTao.index = pd.to_datetime(TsingTao.index, format="%Y-%m-%d")
    TsingTao = TsingTao.iloc[:, 2:]
    print(TsingTao.head(n=10))
    Close = TsingTao.Close
    Ema5 = ma.ewmaCal(Close, 5, 0.2)
    print(Ema5.head())
    print(Ema5.tail())
    plt.plot(Close[4:], label="Close", color="k")
    plt.plot(Ema5[4:], label="Ema5", color="g", linestyle="-.")
    plt.title("青岛啤酒收盘价指数移动平均线")
    plt.ylim(35, 50)
    plt.legend()


def show_chinaback():
    ChinaBank = pd.read_csv(r"./data/ChinaBank.csv")
    ChinaBank.index = ChinaBank.iloc[:, 1]
    ChinaBank.index = pd.to_datetime(ChinaBank.index, format="%Y-%m-%d")
    ChinaBank = ChinaBank.iloc[:, 2:]
    print(ChinaBank.head())
    CBClose = ChinaBank.Close
    print(CBClose.describe())
    Close15 = CBClose["2015"]
    Sma10 = ma.smaCal(Close15, 10)
    print(Sma10.tail())
    weight = np.array(range(1, 11)) / sum(range(1, 11))
    Wma10 = ma.wmaCal(Close15, weight)
    print(Wma10.tail())
    expo = 2 / (len(Close15) + 1)
    Ema10 = ma.ewmaCal(Close15, 10, expo)
    print(Ema10.tail())
    Sma5 = ma.smaCal(Close15, 5)
    Sma30 = ma.smaCal(Close15, 30)
    # plt.plot(Close15[10:], label="Close", color="k")
    # plt.plot(Sma10[10:], label="Sma10", color="r", linestyle="dashed")
    # plt.plot(Wma10[10:], label="Wma10", color="b", linestyle=":")
    # plt.plot(Ema10[10:], label="Ema10", color="G", linestyle="-.")
    # plt.title("中国银行价格均线")
    plt.plot(Close15[30:], label="Close", color="k")
    plt.plot(Sma5[30:], label="Sma5", color="b", linestyle="dashed")
    plt.plot(Sma30[30:], label="Sma30", color="r", linestyle=":")
    plt.title("中国银行股票价格的长短期均线")
    plt.ylim(3.5, 5.5)
    plt.legend()


if __name__ == '__main__':
    print("ch30")
    show_chinaback()
