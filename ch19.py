# encoding: UTF-8
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy import linalg


# 设置DataFrame显示宽度和列数
pd.set_option("display.width", 200)
pd.set_option('display.max_columns', 16)


class MeanVariance:
    """
    求解资产配置比例以期待在达到目标收益率时将风险最小化
    """
    def __init__(self, returns):
        """
        定义构造器，传入收益率数据
        :param returns:
        """
        self.returns = returns

    def minVar(self, goalRet):
        """
        定义最小化方差的函数，即求解二次规划
        :param goalRet:
        :return:
        """
        covs = np.array(self.returns.cov())
        means = np.array(self.returns.mean())
        L1 = np.append(np.append(covs.swapaxes(0, 1), [means], 0), [np.ones(len(means))], 0).swapaxes(0, 1)




def cal_mean(frac):
    return 0.08 * frac + 0.15 * (1 - frac)


def plot_mean_sd():
    """
    绘制收益的均值方差图
    :return:
    """
    mean = list(map(cal_mean, [x / 50 for x in range(51)]))
    print("mean length: ", len(mean))
    print("mean[:5] ", mean[:5])
    sd_mat = np.array(
        [
            list(
                map(
                    lambda x: math.sqrt((x ** 2) * 0.12 ** 2 + ((1 - x) ** 2) * 0.25 ** 2 + 2 * x * (1 - x) * (
                                -1.0 + i * 0.5) * 0.12 * 0.25),
                    [x / 50 for x in range(51)]
                )
            )
            for i in range(5)
        ]
    )
    print(sd_mat.shape)
    plt.plot(sd_mat[0, :], mean, label='-1')
    plt.plot(sd_mat[1, :], mean, label='-0.5')
    plt.plot(sd_mat[2, :], mean, label='0')
    plt.plot(sd_mat[3, :], mean, label='0.5')
    plt.plot(sd_mat[4, :], mean, label='1')
    plt.legend(loc='upper left')
    plt.show()


def cal_corr():
    stock = pd.read_csv(r"./data/019/stock.txt", sep="\t", index_col="Trddt")
    byjc = stock.loc[stock.Stkcd == 600004, "Dretwd"]
    byjc.name = "byjc"
    fjgs = stock.loc[stock.Stkcd == 600033, "Dretwd"]
    fjgs.name = "fjgs"
    hxyh = stock.loc[stock.Stkcd == 600015, "Dretwd"]
    hxyh.name = "hxyh"
    sykj = stock.loc[stock.Stkcd == 600183, "Dretwd"]
    sykj.name = "sykj"
    zndl = stock.loc[stock.Stkcd == 600023, "Dretwd"]
    zndl.name = "zndl"
    sh_return = pd.concat([byjc, fjgs, hxyh, sykj, zndl], axis=1)
    print(sh_return.head())
    sh_return = sh_return.dropna()
    cumreturn = (1 + sh_return).cumprod()
    # sh_return.plot()
    # plt.title("Daily Return of 5 Stocks(2014-2015)")
    # plt.legend(loc="lower center", ncol=5, fancybox=True, shadow=True)
    # plt.show()
    # cumreturn.plot()
    # plt.show()
    print(sh_return.corr())


if __name__ == '__main__':
    print("ch19")
    cal_corr()
