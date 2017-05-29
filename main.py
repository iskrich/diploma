# -*- coding: utf-8 -*-

from parseData import *
from evolution import *
from BackTest import getFitness, getAdvice
import random
import pandas as pd
from Node import NonTerminalNode, TerminalNode
from realTimeBT import Test, HoldAndBuy
from statistics import Statistics
from pyalgotrade.tools import yahoofinance, quandl
from datetime import datetime, date, time, timedelta
import warnings
import os, shutil
from reporter import generatePDF
import argparse

def parseInputSignal(input, leveler, tree):
	signals = input.split(";")
	assert len(signals) == 3
	forAd = {}
	for s in signals:
		res = s.split("=")
		levelName = res[0]
		value = leveler.getLevel(levelName, float(res[1]))
		forAd[levelName] = value
	return getAdvice(tree, forAd)


def calcStrategy(instrument, start, end, size, gens):
	data = get_stock(instrument, start, end, save=True)
	tech_indicators = get_indicators(data)
	result = parse_data_to_levels(data, tech_indicators)
	data = result["data"]
	calc_str = genetic_algoritm(size, gens, 0.25, 0.3, data, tech_indicators, instrument, start)

	start_year2 = int(start.split('-')[2]) + 1
	start2      =  start.split('-')[0] + "-" + start.split('-')[1] + "-" +  str(start_year2)
	end2        =  end.split('-')[0] + "-"  + end.split('-')[1] + "-" + str(start_year2)
	data2       = get_stock(instrument, start2, end2)
	data2       = parse_data_to_levels(data2, tech_indicators)
	getFitness(data2["data"],calc_str, setResults=True)
	result      = data2["data"]
	weights     = result["Weight"]
	t = Test(quandl.build_feed("WIKI", [instrument], start_year2, start_year2, "."), instrument, weights)
	stats = Statistics(t)
	#generatePDF(stats, start+" по " +end, start2 + " по " + end2)
	stats.printResults()

def fitnessProgressTest(instrument, start, end):
	start_year = int(start.split('-')[0])
	data = get_stock(instrument, start, end, save=True)
	tech_indicators = get_indicators(data)
	result = parse_data_to_levels(data, tech_indicators)

	data = result["data"]
	maxDr = 0.0
	ret = 0.0
	unprofit = 0
	profit = 0
	sharpe = 0.0
	streak = 0.0
	train_maxDr = 0.0
	train_ret = 0.0
	train_profit = 0
	train_unprofit = 0
	train_sharpe = 0.0
	train_streak = 0
	lens = 1
	for i in range(lens):

		import time
		start1 = time.time()
		print "Start GENETIC"
		calc_str = genetic_algoritm(100, 1, 0.25, 0.3, data, tech_indicators, instrument, start)

		end = time.time()
		elapsed = end - start1
		print "Total time: %f" % elapsed
		train_maxDr += calc_str.stats.drawDownAnalyzer.getMaxDrawDown() * 100
		train_ret += calc_str.stats.retAnalyzer.getCumulativeReturns()[-1] * 100
		train_profit += calc_str.stats.tradesAnalyzer.getProfitableCount()
		train_unprofit += calc_str.stats.tradesAnalyzer.getUnprofitableCount()
		train_sharpe +=  calc_str.stats.sharpeRatioAnalyzer.getSharpeRatio(0.025)
		train_streak +=  calc_str.stats.streak

		start2 = '%d-01-03' % (start_year + 1)
		end2 = '%d-12-30' % (start_year + 1)

		data2       = get_stock(instrument, start2, end2)
		data2       = parse_data_to_levels(data2, tech_indicators)
		getFitness(data2["data"], calc_str, setResults=True)

		weights = data2["data"]["Weight"]
		t = Test(yahoofinance.build_feed([instrument], start_year + 1, start_year + 1, "."), instrument, weights)
		stats = Statistics(t)
		maxDr += stats.drawDownAnalyzer.getMaxDrawDown() * 100
		ret += stats.retAnalyzer.getCumulativeReturns()[-1] * 100
		profit += stats.tradesAnalyzer.getProfitableCount()
		unprofit += stats.tradesAnalyzer.getUnprofitableCount()
		sharpe += stats.sharpeRatioAnalyzer.getSharpeRatio(0.025)
		streak += stats.streak

	result3 = []
	result3.append(train_sharpe)
	result3.append(train_ret)
	result3.append(train_maxDr)
	result3.append(train_profit)
	result3.append(train_unprofit)
	result3.append(train_streak)

	result3.append(sharpe)
	result3.append(ret)
	result3.append(maxDr)
	result3.append(profit)
	result3.append(unprofit)
	result3.append(streak)
	return result3

def clean_data():
	folder = 'data'
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			# elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process commands.')
	parser.add_argument('-instrument', metavar='I', type=str, nargs='+',
                    help='Target instrument')
	parser.add_argument('-year', metavar='S', type=str, nargs='+',
                    help='Start date')
	args = parser.parse_args()

	calcStrategy("AAPL", "01-05-2015", "12-28-2015", 20, 2)
	clean_data()