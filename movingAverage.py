# encoding: UTF-8
import pandas as pd
import numpy as np

def smaCal(tsPrice, k):
    Sma = pd.Series(0.0, index=tsPrice.index)
    for i in range(k-1, len(tsPrice)):
        Sma[i] = sum(tsPrice[(i-k+1):(i+1)]) / k
    return Sma


def wmaCal(tsPrice, weight):
    k = len(weight)
    arrWeight = np.array(weight)
    Wma = pd.Series(0.0, index=tsPrice.index)
    for i in range(k-1, len(tsPrice)):
        Wma[i] = sum(arrWeight * tsPrice[(i-k+1):(i+1)]) / k
    return Wma


def ewmaCal(tsprice, period=5, exponential=0.2):
    Ewma = pd.Series(0.0, index=tsprice.index)
    Ewma[period - 1] = np.mean(tsprice[:period])
    for i in range(period, len(tsprice)):
        Ewma[i] = exponential * tsprice[i] + (1 - exponential) * Ewma[i - 1]
    return Ewma