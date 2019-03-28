# encoding: UTF-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from movingAverage import smaCal, wmaCal, ewmaCal

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
    Sma5 = smaCal(Close, 5)
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
    Wma5 = wmaCal(Close, w)
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
    Ema5 = ewmaCal(Close, 5, 0.2)
    print(Ema5.head())
    print(Ema5.tail())
    plt.plot(Close[4:], label="Close", color="k")
    plt.plot(Ema5[4:], label="Ema5", color="g", linestyle="-.")
    plt.title("青岛啤酒收盘价指数移动平均线")
    plt.ylim(35, 50)
    plt.legend()


if __name__ == '__main__':
    print("ch30")
    show_ewma()
