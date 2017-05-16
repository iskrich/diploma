
history = []
MAX_VALUES = [-99999.0 for i in range(6)]
MIN_VALUES = [99999.0 for i in range(6)]
STEP_VALUES = [-1 for i in range(6)]


def get_index(x, i):
	global MAX_VALUES
	global MIN_VALUES
	global STEP_VALUES

	x = float(x)
	if x <= (MIN_VALUES[i]+STEP_VALUES[i]):
		return 0
	elif x <= (MIN_VALUES[i]+2*STEP_VALUES[i]):
		return 1
	elif x <= (MIN_VALUES[i] + 3*STEP_VALUES[i]):
		return 2
	elif x <= (MIN_VALUES[i] + 4*STEP_VALUES[i]):
		return 3
	elif x <= (MIN_VALUES[i] + 5*STEP_VALUES[i]):
		return 4
	elif x <= (MIN_VALUES[i] + 6*STEP_VALUES[i]):
		return 5
	else:
		return 6
def parse(path):
	global MAX_VALUES
	global MIN_VALUES
	global STEP_VALUES
	global history
	history = []
	f = open(path)
	next(f)
	for line in iter(f):
	    info = line.split(',')
	    for i in range(6):
	    	if float(info[i+3]) > MAX_VALUES[i]:
	    		MAX_VALUES[i] = float(info[i+3])
	    	if float(info[i+3]) < MIN_VALUES[i]:
	    		MIN_VALUES[i] = float(info[i+3])
	    history.append({"time": info[0], "open": info[2], "a": info[3], "b": info[4], "c": info[5], "d": info[6], "e": info[7], "f": info[8]})
	f.close()

	for i in range(6):
		STEP_VALUES[i] = abs((MAX_VALUES[i] - MIN_VALUES[i]) / 7.0)

	for i in range(len(history)):
		history[i]["a"] = get_index(history[i]["a"], 0)
		history[i]["b"] = get_index(history[i]["b"], 1)
		history[i]["c"] = get_index(history[i]["c"], 2)
		history[i]["d"] = get_index(history[i]["d"], 3)
		history[i]["e"] = get_index(history[i]["e"], 4)
		history[i]["f"] = get_index(history[i]["f"], 5)
	f = open('history.txt', 'w')
	for item in history:
	    f.write("%s \n" % item)
	f.close()
def dynamic_parse(path):
	global MAX_VALUES
	global MIN_VALUES
	global STEP_VALUES
	global history

	f = open(path)
	next(f)
	for line in iter(f):
		info = line.split(',')
		for i in range(6):
			if float(info[i+3]) < MIN_VALUES[i]:
				MIN_VALUES[i] = float(info[i+3])
	    		STEP_VALUES[i] = abs((MAX_VALUES[i] - MIN_VALUES[i]) / 7.0)
		
			if float(info[i+3]) > MAX_VALUES[i]:
				MAX_VALUES[i] = float(info[i+3])
				STEP_VALUES[i] = abs((MAX_VALUES[i] - MIN_VALUES[i]) / 7.0)
		atr = get_index(float(info[3]),0)
		cci = get_index(float(info[4]),1)
		macd = get_index(float(info[5]),2)
		rsi = get_index(float(info[6]),3)
		stoch = get_index(float(info[7]),4)
		wpr = get_index(float(info[8]),5)
		history.append({"time":info[0],"open":info[2],"a":atr, "b":cci, "c":macd, "d":rsi, "e":stoch,"f":wpr})
		del history[0]

	f = open( 'history.txt', 'w' )
	for item in history:
	    f.write("%s \n" % item)
	f.close()
	
	MAX_VALUES = [-99999.0 for i in range(6)]
	MIN_VALUES = [ 99999.0 for i in range(6)]
	STEP_VALUES =[0 for i in range(6)]
#parse('test.csv')
#dynamic_parse('test.csv')
