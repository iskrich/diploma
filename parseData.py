import pandas as pd
import pandas.io.data as web
import numpy as np
import math
import pyalgotrade
import talib
from utils import draw_series
import matplotlib.pyplot as plt



class Leveler:
	def __init__(self, levels):
		self.levels = levels

	def getLevel(self, levelName, value):
		if math.isnan(value):
			return -1
		max = self.levels[levelName]["max"]
		min = self.levels[levelName]["min"]
		if value > max:
			self.levels[levelName]["max"] = value
			return 4
		if value < min:
			self.levels[levelName]["min"] = value
			return 0

		step = abs((max - min) / 4.0)
		level = 0
		start = min
		while start < value:
			start+=step
			level+=1
		return level


def STO(df, save=False):
	slowk, slowd = talib.STOCH(df["High"].values, df["Low"].values, df["Close"].values, 5, 3, 0, 3, 0)
	sto_series = pd.Series(slowk, name = "Stochastic", index = df.index)
	if save:
		save_series(sto_series, "Stochastic")
	df = df.join(sto_series)
	return df

def Chaikin(df, save=False):
	chaikin = talib.AD(df["High"].values, df["Low"].values, df["Close"].values,  df["Volume"].values.astype(float))
	cha_series = pd.Series(chaikin, name = "Chaikin", index = df.index)
	if save:
		save_series(cha_series, "Chaikin")
	df = df.join(cha_series)
	return df

def RSI(df, save=False):
	rsi = talib.RSI(df["Close"].values, 5)
	rsi_series = pd.Series(rsi, name="RSI", index=df.index)
	if save:
		save_series(rsi_series, "RSI")
	df = df.join(rsi_series)
	return df

def ATR(df, save=False):
	atr = talib.ATR(df["High"].values, df["Low"].values, df["Close"].values, timeperiod=14)
	atr_series = pd.Series(atr, name="ATR", index=df.index)
	if save:
		save_series(atr_series, "ATR")
	df = df.join(atr_series)
	return df


def save_series(series, name):
	plt.cla()
	plot = series.plot(title=name)
	fig = plot.get_figure()
	fig.savefig("data/" + name + ".png")

def get_stock(stock_name,start,end, save=False):
	print "Download %s data" % stock_name
	data = web.DataReader(stock_name, 'yahoo',start, end)
	if save:
		save_series(data["Open"], "Price")
	#ROFL
	print "Calc addition indicators"
	data = RSI(ATR(STO(data, save), save), save)
	return data


def parse_data_to_levels(data,indicators):
	indicators_len = len(indicators)
	levels = {}
	for indicator in indicators:
		min = 99999
		max = -99999
		level_name = str(indicator)+"_level"
		data[level_name] = 0
		for index in data.index:
			value = data[indicator][index]
			if math.isnan(value):
				data.set_value(index, level_name, -1)
				continue
			if value > max:
				max = value
				data.set_value(index, level_name, 4)
				continue
			if value < min:
				min = value
				data.set_value(index, level_name, 0)
				continue
			step = abs((max - min) / 4.0)
			level = 0
			start = min
			while start<value:
				start+=step
				level+=1
			data.set_value(index, level_name, level)

		levels[level_name] = {"min": min, "max": max}
	#Create some weight for signal (neccessary in PyAlgoTrade strategy)
	data["Weight"] = 0.0
	for index in data.index:
		data.set_value(index, "Weight", 0.0)
	return {"data" : data, "leveler" : Leveler(levels)}

def add_crossing(data,name1,name2):
	name = name1+" cross "+name2
	data["test"] = data[name1] - data[name2]
	data[name] = 0
	for index in data.index:
		
		number = data.index.get_loc(index)
		if number<data.index.size:
			if (data["test"][index]>0 and data.irow(number-1)["test"]<0):
				data[name][index]=1
			elif (data["test"][index]<=0 and data.irow(number-1)["test"]>=0):
				data[name][index]=-1
		else:
			data[name][index] = 0
	data = data.drop("test", 1)	
	return data

def get_indicators(data):
	allColumn = set(data.columns)
	indicators = allColumn - set(['Close','Open','High','Low','Volume', 'Adj Close'])
	return list(indicators)
