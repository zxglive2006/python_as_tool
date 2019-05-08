# encoding: UTF-8
from __future__ import division

import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from scipy import stats

# 设置DataFrame显示宽度
pd.set_option("display.width", 120)
pd.set_option('display.max_columns', 8)

plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号


def basic_random_variable():
    RandomNumber = np.random.choice([1, 2, 3, 4, 5], size=100, replace=True, p=[0.1, 0.1, 0.3, 0.3, 0.2])
    print(pd.Series(RandomNumber).value_counts())
    print(pd.Series(RandomNumber).value_counts() / 100)
    HSRet300 = pd.read_csv('./data/return300.csv')
    print(HSRet300.head())
    density = stats.kde.gaussian_kde(HSRet300.iloc[:,1])
    bins = np.arange(-5, 5, 0.02)
    plt.subplot(211)
    plt.plot(bins, density(bins))
    plt.title(u'沪深300收益率序列的概率密度曲线图')
    plt.subplot(212)
    plt.plot(bins, density(bins).cumsum())
    plt.title(u'沪深300收益率序列的累计分布函数图')
    plt.show()


def binomial_demo():
    print(np.random.binomial(100, 0.5, 20))
    print(np.random.binomial(10, 0.5, 3))
    print(stats.binom.pmf(20, 100, 0.5))
    print(stats.binom.pmf(50, 100, 0.5))
    dd = stats.binom.pmf(np.arange(0, 21, 1), 100, 0.5)
    print("sum of pmf:{}".format(dd.sum()))
    print("call of cdf:{}".format(stats.binom.cdf(20, 100, 0.5)))
    HSRet300 = pd.read_csv('./data/return300.csv')
    print(HSRet300.head())
    ret = HSRet300.iloc[:, 1]
    p = len(ret[ret > 0]) / len(ret)
    print(p)
    print(stats.binom.pmf(6, 10, p))


def normal_demo():
    Norm = np.random.normal(size=5)
    print(Norm)
    print("pdf:{}".format(stats.norm.pdf(Norm)))
    print("cdf:{}".format(stats.norm.cdf(Norm)))
    HSRet300 = pd.read_csv('./data/return300.csv')
    print(HSRet300.head())
    ret = HSRet300["return"]
    HS300_RetMean = ret.mean()
    print(HS300_RetMean)
    HS300_RetVariance = ret.var()
    print(HS300_RetVariance)
    print(stats.norm.ppf(0.05, HS300_RetMean, HS300_RetVariance ** 0.5))


def other_continuous_demo():
    # 卡方分布
    plt.plot(np.arange(0, 5, 0.002), stats.chi.pdf(np.arange(0, 5, 0.002), 3))
    plt.title('Probability Density Plot of Chi-Square Distribution')
    plt.show()
    # t分布
    x = np.arange(-4, 4.004, 0.004)
    plt.plot(x, stats.norm.pdf(x), label='Normal')
    plt.plot(x, stats.t.pdf(x, 5), label='df=5')
    plt.plot(x, stats.t.pdf(x, 30), label='df=30')
    plt.legend()
    plt.show()
    # F分布
    plt.plot(np.arange(0, 5, 0.002), stats.f.pdf(np.arange(0, 5, 0.002), 4, 40))
    plt.show()


def joint_demo():
    TRD_index = pd.read_csv('./data/TRD_Index.txt', sep='\t')
    SHIndex = TRD_index[TRD_index.Indexcd == 1]
    print(SHIndex.head())
    SZIndex = TRD_index[TRD_index.Indexcd == 399106]
    print(SHIndex.head())
    plt.scatter(SHIndex.Retindex, SZIndex.Retindex)
    plt.title(u'上证综指与深圳成指收益率的散点图')
    plt.xlabel(u'上证综指收益率')
    plt.ylabel(u'深圳成指收益率')
    plt.show()
    SZIndex.index = SHIndex.index
    print(SZIndex.Retindex.corr(SHIndex.Retindex))


if __name__ == '__main__':
    print("ch14")
    basic_random_variable()
