"""
Author: Tommy Fiedler
Date: 02/27/2023

Description:
    Calculate the volatility of a stock using a weighted average.

"""

import yfinance as yf
from pandas import DataFrame
from math import log, sqrt

def calcReturns(ticker):

    stock = yf.Ticker(ticker)
    data = DataFrame(stock.history(period="1mo"))
    
    col = data.shape[0]
    #data["Average"] = data.apply(lambda row: (row["High"] + row["Low"]) / 2, axis=1)
    returns = [log(data["High"].loc[data.index[i]] / data["Low"].loc[data.index[i]]) for i in range(col-1, 1, -1)] 
    return returns

def getInput():

    ticker = input("Enter the company ticker -> ")
    return ticker

def calcVolatility(data):
    
    weight = 0.95
    
    vol = (1 - weight) * sum([weight**(i-1) * data[i-1] * data[i-1] 
                            for i in range(1, len(data) + 1)])
    return sqrt(vol)

def std(data):

    avg = sum(data)/len(data)
    std = sum([(x - avg)**2 for x in data])
    
    return (std/len(data))**0.5

def correlation(x, y):
    
    spy = calcReturns("SPY")
    N = leb(x)
    sigx = std(x)
    sigy = std(y)

    co_variance = 1/N * sum([(x[i]-(sum(x)/N)) / (y[i]-(sum(y)/n)) for i in range(N)])
    correlation = co_variance / sigx*sigy
    return correlation

def main():
    
    ticker = getInput()
    returns = calcReturns(ticker)
    vol = calcVolatility(returns)

    # Estimate annualized volatility by multiplying percent by 16
    annual_vol = vol*16*100
    print("Annualized Volatility: {0:4.1f}".format(annual_vol))

if __name__ == "__main__":
    main()
