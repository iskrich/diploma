import os
from  workbench import header, footer
import re
table_folder = 'docs/tables'
def calcSharpe():
	dic = {}
	for filename in os.listdir(table_folder):
		if filename == '.DS_Store' or filename == 'withBfSharpe':
			continue
		count = 0
		table_with_bf = ""
		with open(table_folder + '//' + filename, 'r') as file:
			while True:
				table_with_bf += file.readline()
				line = file.readline()
				if not line: break
				if float(line.split('&')[1]) > float(line.split('&')[6].split(r'\\')[0]):
					count+=1
					test_year = re.search(r'[0-9]{4} Test', line).group(0)
					line = re.sub(test_year, r"\\textbf{" + test_year + '}', line)
				table_with_bf += line
		with open(table_folder + "//" + 'withBfSharpe' + "//" + filename, 'w+') as l:
			l.write(table_with_bf)
		dic.__setitem__(filename, count)
	items = sorted(dic, key=dic.__getitem__, reverse=True)
	#for item in items[:5]:
	#	createTable(item)
	createTable(items[5])

def newRequirements():
	boombadaboom = ""
	for filename in os.listdir('docs/results/latex'):
		count = 0
		if filename == '.DS_Store':
			continue
		with open('docs/results/latex' + '//' + filename, 'r') as file:
			while True:
				line = file.readline()
				if not line: break
				lst = re.findall('\d+\.\d{3}', line)
				trades = re.findall('\d+.\d\+\d+.\d', line)
				print line
				profit = re.findall(r'Profit +\\ Unprofit', line)
				if len(profit) !=0:
					print profit
					line = line.replace(profit[0], r'Trades\\ Count')
				if len(trades) != 0:
					if count < 2:
						count+=1
						continue
					expr = trades[0]
					line = line.replace(expr, str(int(float(expr.split('+')[0]) + float(expr.split('+')[0]))))
				if len(lst) != 0:
					for num in lst:
						line = line.replace(num, ("%.2f" % round(float(num), 2)))
				boombadaboom += line
		with open('docs/final', 'w+') as file:
			file.write(boombadaboom)

def allBold(file):
	text = ""
	with open(file, 'r') as file:
		while True:
			line = file.readline()
			if not line: break
			if line.__contains__("textbf"):
				vals = line.split('&')
				for i in range(1,7):
					if i == 6:
						vals[i] = r" & \textbf{" + vals[i].split('\\')[0] + "}" + vals[i].split('\\')[1] + "\\\\ \\hline"

					else:
						vals[i] = r" & \textbf{" + vals[i] + "}"
				line = "".join(vals)
			text += line
		with open('docs/change2', 'w+') as out:
			out.write(text)


def createTable(file):
	latex_file = open(table_folder + "//" + 'withBfSharpe' + "//" + file, 'r')
	latex = latex_file.read()
	latex_file.close()

	table = open('docs/results/latex/%s.txt' % file, 'w+')
	table.write(header % file)
	table.write('\n')
	table.write(latex)
	table.write('\n')
	table.write(footer)
	table.close()

allBold('docs/change')