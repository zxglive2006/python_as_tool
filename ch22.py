# encoding: UTF-8
import pandas as pd
import matplotlib.pylab as plt

# 设置DataFrame显示宽度
pd.set_option("display.width", 120)
pd.set_option('display.max_columns', 16)

plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号


def basic_time_series():
    Index = pd.read_csv(".\data\TRD_Index.txt", sep="\t", index_col="Trddt")
    SHIndex = Index[Index.Indexcd == 1]
    print(SHIndex.head())
    print(type(SHIndex))
    Clsindex = SHIndex.Clsindex
    print(Clsindex.head())
    print(type(Clsindex))
    print(type(Clsindex.index))
    Clsindex.index = pd.to_datetime(Clsindex.index)
    print(Clsindex.head())
    print(type(Clsindex.index))
    Clsindex.plot()
    plt.show()


def select_time_series():
    Index = pd.read_csv(".\data\TRD_Index.csv", index_col="Trddt")
    SHIndex = Index[Index.Indexcd == 1]
    SHIndex.index = pd.to_datetime(SHIndex.index)
    SHIndexPart = SHIndex["2014-10-08":"2014-10-31"]
    print(SHIndexPart.head())
    print(SHIndexPart.tail())


def describe_time_series():
    Index = pd.read_csv(".\data\TRD_Index.txt", sep="\t", index_col="Trddt")
    SHIndex = Index[Index.Indexcd == 1]
    Clsindex = SHIndex.Clsindex
    print(Clsindex.head())
    print(Clsindex.tail())
    print(Clsindex.max())
    print(Clsindex.min())
    print(Clsindex.mean())
    print(Clsindex.median())
    print(Clsindex.std())
    print(Clsindex.describe())
    Clsindex.hist()
    plt.show()


if __name__ == '__main__':
    print("ch22")
    describe_time_series()
