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
        ones = np.ones(len(means))
        zeros = np.zeros(len(means))
        temp = np.append(covs, [means], 0)
        temp2 = np.append(temp, [ones], 0)
        L1 = temp2.swapaxes(0, 1)
        L2 = list(ones)
        L2.extend([0, 0])
        L3 = list(means)
        L3.extend([0, 0])
        L4 = np.array([L2, L3])
        L = np.append(L1, L4, 0)
        temp3 = np.append(zeros, [1, goalRet], 0)
        results = linalg.solve(L, temp3)
        return np.array([list(self.returns.columns), results[:-2]])

    def meanRet(self, fracs):
        """
        给定各资产的比例，计算收益率均值
        :param fracs:
        :return:
        """
        from ffn import to_returns
        meanRisky = to_returns(self.returns).mean()
        assert len(meanRisky) == len(fracs)     # Length of fractions must be equal to naumber of assets
        return np.sum(np.multiply(meanRisky, np.array(fracs)))

    def calVar(self, fraces):
        """
        给定各资产的比例，计算收益率方差
        :param fraces:
        :return:
        """
        return np.dot(np.dot(fraces, self.returns.cov()), fraces)

    def cal_func(self, x):
        return self.calVar(self.minVar(x)[1, :].astype(np.float))

    def frontierCurve(self):
        """
        定义绘制最小方差边缘曲线函数
        :return:
        """
        goals = [x/50000 for x in range(-100, 4000)]
        variances = list(map(self.cal_func, goals))
        plt.plot(variances, goals)


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


def get_sh_return():
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
    # print(sh_return.head())
    sh_return = sh_return.dropna()
    sh_return.index = pd.to_datetime(sh_return.index)
    # print(sh_return.corr())
    # cumreturn = (1 + sh_return).cumprod()
    # sh_return.plot()
    # plt.title("Daily Return of 5 Stocks(2014-2015)")
    # plt.legend(loc="lower center", ncol=5, fancybox=True, shadow=True)
    # plt.show()
    # cumreturn.plot()
    return sh_return


def markowitz_model(_sh_return):
    minVar = MeanVariance(_sh_return)
    # minVar.frontierCurve()
    print(minVar.minVar(0.003))
    train_set = _sh_return["2014"]
    test_set = _sh_return["2015"]
    varMinimizer = MeanVariance(train_set)
    goal_return = 0.003
    portfolio_weight = varMinimizer.minVar(goal_return)
    print(portfolio_weight)
    temp = np.array([portfolio_weight[1,:].astype(np.float)]).swapaxes(0, 1)
    print(temp)
    test_return = np.dot(test_set, temp)
    test_return = pd.DataFrame(test_return, index=test_set.index)
    test_cum_return = (1 + test_return).cumprod()
    sim_weight = np.random.uniform(0, 1, (100, 5))
    sim_return = np.dot(test_set, sim_weight.swapaxes(0, 1))
    sim_return = pd.DataFrame(sim_return, index=test_return.index)
    sim_cum_return = (1 + sim_return).cumprod()
    plt.plot(sim_cum_return.index, sim_cum_return, color='green')
    plt.plot(test_cum_return.index, test_cum_return, color="red")
    plt.show()


def blacklitterman(returns, tau, P, Q):
    mu = returns.mean()
    sigma = returns.cov()
    pi1 = mu
    ts = tau * sigma
    Omega = np.dot(np.dot(P, ts), P.T) * np.eye(Q.shape[0])
    middle = linalg.inv(np.dot(np.dot(P, ts), P.T) + Omega)
    er = np.expand_dims(pi1, axis=0).T + np.dot(np.dot(np.dot(ts, P.T), middle),
                                                (Q - np.expand_dims(np.dot(P, pi1.T), axis=1)))
    posteriorSigma = sigma + ts - np.dot(ts.dot(P.T).dot(middle).dot(P), ts)
    return [er, posteriorSigma]


def blminVar(blres, goalRet):
    covs = np.array(blres[1])
    means = np.array(blres[0])
    L1 = np.append(np.append((covs.swapaxes(0, 1)), [means.flatten()], 0),
                   [np.ones(len(means))], 0).swapaxes(0, 1)
    L2 = list(np.ones(len(means)))
    L2.extend([0, 0])
    L3 = list(means)
    L3.extend([0, 0])
    L4 = np.array([L2, L3])
    L = np.append(L1, L4, 0)
    results = linalg.solve(L, np.append(np.zeros(len(means)), [1, goalRet], 0))
    return (pd.DataFrame(results[:-2], index=blres[1].columns, columns=['p_weight']))


def test_blacklitterman():
    pick1 = np.array([1, 0, 1, 1, 1])
    q1 = np.array([0.003 * 4])
    pick2 = np.array([0.5, 0.5, 0, 0, -1])
    q2 = np.array([0.001])
    P = np.array([pick1, pick2])
    Q = np.array([q1, q2])
    print(P)
    print(Q)
    sh_return = get_sh_return()
    res = blacklitterman(sh_return, 0.1, P, Q)
    print(res)


if __name__ == '__main__':
    print("ch19")
    test_blacklitterman()
