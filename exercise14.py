# encoding: UTF-8
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from scipy import stats

# 设置DataFrame显示宽度
pd.set_option("display.width", 160)
pd.set_option('display.max_columns', 15)

plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号


def question1():
    Bwages = pd.read_csv(r".\exercise_data\Bwages.csv")
    print(Bwages.head())
    Bwages.wage.hist(normed=True)
    plt.show()
    Bwages.wage.hist(normed=True, cumulative=True)
    plt.show()
    density = stats.gaussian_kde(Bwages.wage)
    bins = np.arange(0, 50, 0.02)
    plt.plot(bins, density(bins).cumsum())
    plt.title("工人工资累计分布函数图")
    plt.show()


def question2():
    history = pd.read_csv(r".\exercise_data\history.csv", index_col='Date')
    print("history shape:{}".format(history.shape))
    revenue = len(history[history["Emerging.Markets"] > 0])
    loss = len(history[history["Emerging.Markets"] < 0])
    print("revenue size:{}, loss size:{}".format(revenue, loss))
    p = float(revenue) / (revenue + loss)
    print("p:{}".format(p))
    prob = 1 - stats.binom.cdf(6, 12, p)
    print("prob:{}".format(prob))


def question3():
    from math import sqrt
    norm_bins = np.linspace(-5, 5, num=200)
    plt.plot(norm_bins, stats.norm.pdf(norm_bins, loc=0, scale=1), label="N(0, 1)")
    plt.plot(norm_bins, stats.norm.pdf(norm_bins, loc=0, scale=sqrt(0.5)), label="N(0, 0.5)")
    plt.plot(norm_bins, stats.norm.pdf(norm_bins, loc=0, scale=sqrt(2)), label="N(0, 2)")
    plt.plot(norm_bins, stats.norm.pdf(norm_bins, loc=2, scale=1), label="N(2, 1)")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    print("exercise14")
    question3()
