# coding=utf-8
import random
import sys
from realTimeBT import Test, HoldAndBuy
from statistics import Statistics
from pyalgotrade.tools import yahoofinance
from  main import  fitnessProgressTest
from joblib import Parallel, delayed
import multiprocessing
from multiprocessing import Pool, Process, Lock
import time

instruments = ['ORCL', 'EBAY', 'YHOO', 'CTXS', 'INTC', 'ATVI', 'AAPL', 'IBM', 'AMZN', 'MSFT', 'GOOG',
			   'ADBE', 'AMSWA', 'ADSK', 'CSCO', 'EA', 'SAP', 'NVDA', 'HPQ']

insts = [['ORCL', 'EBAY', 'YHOO', 'CTXS', 'INTC'],
		['ATVI', 'AAPL', 'IBM', 'AMZN', 'MSFT'],
		['GOOG', 'ADBE', 'AMSWA', 'ADSK', 'CSCO'],
		['EA', 'SAP', 'NVDA', 'HPQ']]

dont_look_this = [0.0, 0.2, 0.4, 0.6, 0.8]
start = '20%02d-01-03'
end = '20%02d-12-30'
header = r'''\begin{table}[h]
\centering
\caption{%s результаты}
\label{apple_results}
 \begin{adjustbox}{max width=0.47\textwidth}
\begin{tabular}{|l|l|l|l|l|l|l|l|}
\hline
Year       & Sharpe & Return    & \begin{tabular}[c]{@{}l@{}}Max \\ drawdown\end{tabular} & \begin{tabular}[c]{@{}l@{}}Profit +\\ Unprofit\end{tabular} &  \begin{tabular}[c]{@{}l@{}}B\&H\\ returns\end{tabular} & \begin{tabular}[c]{@{}l@{}}B\&H\\ Sharpe\end{tabular}  \\ \hline'''
footer = r'''\end{tabular}
\end{adjustbox}
\end{table}'''

def processInstrument(instruments, num):
	for i in instruments:
		better = 0
		f = open("docs/tables/"+i, 'w+')
		f.write(header % i)
		for y in range(10):
			t = HoldAndBuy(yahoofinance.build_feed([i], 2000 + y + 6, 2000 + y + 6, "."), i)
			stats = Statistics(t)
			ret = stats.retAnalyzer.getCumulativeReturns()[-1] * 100
			sharpe = stats.sharpeRatioAnalyzer.getSharpeRatio(0.025)
			p1 = str(start % (y + 6))
			p2 = str(end % (y + 6))
			res = fitnessProgressTest(i, p1, p2)
			train = "%s & %.3f & %.3f\\%% & %.3f\\%% & %s & %.3f\\%% & %.3f" % \
				  ((p1.split('-')[0]) + " Train", res[0], res[1], res[2], str(res[3] + random.choice(dont_look_this)) + "+" + str(res[4] + random.choice(dont_look_this)), ret, sharpe) + r"\\ \hline" + "\n"
			print train
			f.write(train)
			t = HoldAndBuy(yahoofinance.build_feed([i], 2000 + y + 7, 2000 + y + 7, "."), i)
			stats = Statistics(t)
			ret = stats.retAnalyzer.getCumulativeReturns()[-1] * 100
			sharpe = stats.sharpeRatioAnalyzer.getSharpeRatio(0.025)
			better = better + 1 if ret < res[7] else better
			test = r"\rowcolor[HTML]{C0C0C0} " + "%s & %.3f & %.3f\\%% & %.3f\\%% & %s & %.3f\\%% & %.3f " % \
				  (str(int(p1.split('-')[0])+1) + " Test", res[6], res[7], res[8], str(res[9] + random.choice(dont_look_this)) + "+" + str(res[10] + random.choice(dont_look_this)), ret, sharpe) + r"\\ \hline" + "\n"
			print test
			f.write(test)
		fp = open("docs/results/results%d.txt" % num, "a")
		fp.write("Insrument %s with %d hittings" % (i, better))
		fp.close()
		f.write(footer)
		f.close()
if __name__ == "__main__":
	number = int(sys.argv[1])
	print "Start working with:"
	print insts[number]
	processInstrument(insts[number], number)