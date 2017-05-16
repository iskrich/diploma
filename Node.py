# -*- coding: utf-8 -*-
from abc import ABCMeta
from realTimeBT import Test
from BackTest import getFitness
from statistics import Statistics, SharpeStatistics
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
import copy

class Node:
	"""Abstract Node Class"""
	@property
	def type(self):
		raise NotImplementedError

class TerminalNode(Node):
	"""Terminal node can have value
		buy, sell"""

	type = "Terminal"

	def __init__(self,signal):
		self.signal = signal
		self.parent = None
	

	#mutation (reverse)
	def get_mutate(self):
		return TerminalNode('LONG') if self.signal == 'SHORT' else TerminalNode('SHORT')

	def setParent(self, node):
		self.parent = node

	def clone(self):
		return TerminalNode(self.signal)

	def __str__(self):
		return str(self.signal)

class NonTerminalNode(Node):
	"""NonTerminal Node contain predicat,
	left and right child.
	predicat go to right if true, else left """

	type = "NonTerminal"
	
	def __init__(self, index, rate):
		self.index = index
		self.rate = rate
		self.parent = None
		self.left = None
		self.right = None

	def detect_all_child(self):
		temp = []
		self.recursive_detect(temp)
		self.nodes = temp
		return self.nodes

	def recursive_detect(node,nodes):
		nodes.append(node.right)
		if (node.right.type!="Terminal"):
			node.right.recursive_detect(nodes)
		nodes.append(node.left)
		if (node.left.type!="Terminal"):
			node.left.recursive_detect(nodes)

	def setLeft(self,left):
		self.left = left
		left.parent = self

	def setRight(self,right):
		self.right = right
		right.parent = self
	
	def setParent(self,node):
		self.parent = node

	def Equal(self,item):
		return item[self.index] == self.rate

	def have(self,candidate):
		#recursive detect is node child
		if (self.parent == None):
			return False
		if (self.index == candidate):
			return True
		else:
			return self.parent.have(candidate)
			
	def get_mutate(self):
		import random	
		from params import VALUES
		return NonTerminalNode(self.index,random.choice(VALUES))

	def invert(self):
		#invert nonterminal nodes except crossing nodes
		if (self.left.type=="NonTerminal"):
			self.left.invert()
		if ("cross" not in self.index):
			self.rate = (self.rate+3)%6
		if (self.right=="NonTerminal"):
			self.right.invert()

	def clone(self):
		node = NonTerminalNode(self.index,self.rate)
		node.setRight(self.right.clone())
		if (self.left!=None):
			node.setLeft(self.left.clone())
		return node

	def getFitness(self,data, y_info, instrument, show=False):
		test_y = copy.deepcopy(y_info)
		getFitness(data, self, setResults=True)
		weights = data["Weight"]
		t = Test(test_y, instrument, weights)
		stats = Statistics(t)
		self.fitness = stats.Sharpe()
		self.stats = stats


		return  stats.Sharpe()
		#from BackTest import getFitness
		#self.fitness = 		getFitness(data, self, show, setResults=True)
		#self.Weight =  data["Weight"]
		#return  self.fitness

	def setStats(self, instrument):
		y_info = yahoofinance.build_feed([instrument], 2008, 2008, ".")
		t = Test(y_info, instrument, self.Weight)
		stats = Statistics(t)
		self.stats = stats

	def __str__(self):
		return str(self.index) + " is " + str(self.rate)
