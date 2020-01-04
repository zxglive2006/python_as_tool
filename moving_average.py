# encoding: UTF-8
import pandas as pd
import numpy as np


def sma_cal(price, k):
    sma = pd.Series(0.0, index=price.index)
    for i in range(k-1, len(price)):
        sma[i] = sum(price[(i - k + 1):(i + 1)]) / k
    return sma


def wma_cal(price, weight):
    k = len(weight)
    arrWeight = np.array(weight)
    wma = pd.Series(0.0, index=price.index)
    for i in range(k-1, len(price)):
        wma[i] = sum(arrWeight * price[(i - k + 1):(i + 1)])
    return wma


def ewma_cal(price, period=5, exponential=0.2):
    ewma = pd.Series(0.0, index=price.index)
    ewma[period - 1] = np.mean(price[:period])
    for i in range(period, len(price)):
        ewma[i] = exponential * price[i] + (1 - exponential) * ewma[i - 1]
    return ewma
