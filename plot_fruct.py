import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

instruments = ['AMZN', 'IBM', 'AAPL', 'MSFT', 'GOOG']

years = ["%02d" % i for i in xrange(8,17,1)]

ctxsSharpe = [-0.82, -0.05, 1.64, 0.29, 0.65, -0.78, 1.85, 3.00, 1.16]
eaSharpe = [-1.30, 1.87, 0.54, -0.05, -0.58, 1.38, 2.53, 1.46, 0.44]
ebaySharpe = [-0.77, 3.38, 0.83, 0.85, 1.72, -1.57, 0.68, -0.38, 0.14]
intcSharpe = [-0.57, 1.35, -1.11, 0.66, 0.62, 0.48, 3.53, 3.11, -0.35]
orclSharpe = [0.12, 4.25, 1.82, -0.27, 0.73, -0.38, 3.89, 2.19, -1.48]

maxDrowdown = [28.1762, 7.2414, 13.7655, 18.5244, 56.4504]
sharpe = 	  [1.0521, 0.9530, 0.3965, 0.4719,  0.2175]
returns = 	  [125.9863, 38.3530, 71.4093, 113.6551, 44.9792]
totalProfit = [43.8, 35.2, 43.6, 12.8, 31.6]
totalUnprofit=[34.2, 23.6, 34.2, 11.4, 27.8]

maxDrowdown2 = [21.5373, 10.5532, 11.9844, 12.4916, 8.1857]
sharpe2 = 	   [1.08, 0.59, 0.470, 0.23, 0.25]
returns2 = 	   [5.5823, -1.0228, 14.8096, 8.3387, 12.4305]
totalProfit2 = [22.2, 17.4, 14.6, 13.4, 21.4]
totalUnprofit2=[14.4, 18.0, 11.6, 10.0, 11.6]

maxDrowdownCTXS = (36.6 + 6.57 + 4.08 + 28.5 + 9.25 + 9.68 + 3 + 4.37 + 3.88) / 9.0
maxDrowdownEA = (44.81 + 4.35 + 9.25 + 13.33 + 33.46 + 4.34 + 3.33 + 11.97 + 12.76) / 9.0 
maxDrowdownEBAY = (40.55 + 8.52 + 6.39 + 7.84 + 4.96 + 27.20 + 6.12 + 48.15 + 18.19) / 9.0
maxDrowdownINTC = (38.93 + 5.21 + 13.79 + 1.16 + 8.15 + 6.0 + 4.03+ 2.43 + 7.26) / 9.0
maxDrowdownORCL = (15.15 + 2.49 + 5.00 + 6.75 + 5 + 17.23 + 2 + 5.39 + 9.41) / 9.0

totalCTXS = (28 + 16 + 18 + 14 + 21 + 18 + 34 + 34 + 35) / 9.0
totalEA =   (38 + 30 + 22 + 34 + 12 + 44 + 46 + 41 + 52) / 9.0
totalEBAY = (24 + 37 + 12 + 7  + 20 + 31 + 37 + 25 + 16) / 9.0
totalINTC = (19 + 49 + 11 + 7  + 30 + 30 + 38 + 42 + 17) / 9.0
totalORCL = (42 + 46 + 58 + 12 + 35 + 30 + 39 + 42 + 16) / 9.0

totals = [totalCTXS, totalEA, totalEBAY, totalINTC, totalORCL]

instruments = ["CTXS", "EA", "EBAY", "INTC", "ORCL"]

maxDr = [11.77, 15.288, 18.657, 9.662, 7.60]

d = {"Instrument" : instruments, "Max Drawdown (%)": maxDrowdown, "Profit Trades": totalProfit,
"Unprofit Trades": totalUnprofit, "Sharpe Ratio": sharpe2, "Max drawdown": maxDrowdown, "Return (%)": returns}

d2 = {"Max drawdown" : maxDr, "Instrument": instruments, "Total trades": totals}#, "Year" : years, "SharpeCTXS": ctxsSharpe, "SharpeEA": eaSharpe, "SharpeEBAY": ebaySharpe, "SharpeINTC": intcSharpe, "SharpeORCL":orclSharpe}

df = pd.DataFrame(d2)

x = instruments

g = sns.factorplot(x="Instrument", y="Total trades", data=df, kind="bar", label='small');
plt.savefig('../../totals.png', format='png', dpi=1000)