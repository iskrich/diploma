import numpy as np
"""
Methods help calculate fitness value
"""

#recursive method, return LONG or SHOT
def getAdvice(node,item):
	if (node.type == 'NonTerminal'):
		if (node.Equal(item)):
			return getAdvice(node.right,item)
		else:
			return getAdvice(node.left, item)
	else:
		return node.signal

def getFitness(data,tree,show=False, setResults=False):
	total_cost = 100.0
	buyPrice = 0.0
	prevSignal = "SHORT"
	fitness = 0.0
	i = 0
	for index in data.index:
		signal = getAdvice(tree, data.iloc[i])
		if setResults:
			val = 1 if signal == "LONG" else -1
			data.set_value(index, "Weight", val)
		if signal == "LONG" and prevSignal =="SHORT":
			prevSignal = "LONG"
			buyPrice = float(data['Open'][index])
			total_cost = total_cost / buyPrice
		elif signal == "SHORT" and prevSignal == "LONG":
			prevSignal = signal
			if (show):
				print str(index)+" BUY for "+str(buyPrice)+" SELL for "+ str(data['Open'][index])
				print "Current fitness" + str(fitness)
			fitness += float(data['Open'][index])- buyPrice
		i+=1
	return fitness
