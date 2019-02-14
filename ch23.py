# encoding: UTF-8
from statsmodels.tsa import stattools
from statsmodels.graphics.tsaplots import *
import pandas as pd
import matplotlib.pylab as plt

# 设置DataFrame显示宽度
pd.set_option("display.width", 120)
pd.set_option('display.max_columns', 16)

plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号


def autocorrelation_demo():
    data = pd.read_csv(r"data\TRD_Index.txt", sep="\t", index_col="Trddt")
    SHIndex = data[data.Indexcd == 1]
    SHIndex.index = pd.to_datetime(SHIndex.index)
    print(SHIndex.head())
    SHRet = SHIndex.Retindex
    print("SHRet type: {}".format(type(SHRet)))
    print(SHRet.head())
    print(SHRet.tail())
    acfs = stattools.acf(SHRet)
    print(acfs[:5])
    pacfs = stattools.pacf(SHRet)
    print(pacfs[:5])
    plot_acf(SHRet, use_vlines=True, lags=30)
    plt.show()
    plot_pacf(SHRet, use_vlines=True, lags=30)
    plt.show()


def stationary_demo():
    data = pd.read_csv(r"data\TRD_Index.txt", sep="\t", index_col="Trddt")
    SHIndex = data[data.Indexcd == 1]
    SHIndex.index = pd.to_datetime(SHIndex.index)
    print(SHIndex.head())
    SHclose = SHIndex.Clsindex
    # SHclose.plot()
    plot_acf(SHclose, use_vlines=True, lags=30)
    plt.show()
    SHRet = SHIndex.Retindex
    # SHRet.plot()
    plot_acf(SHRet, use_vlines=True, lags=30)
    plt.show()
    plot_pacf(SHRet, use_vlines=True, lags=30)
    plt.show()


if __name__ == '__main__':
    print("ch23")
    stationary_demo()
