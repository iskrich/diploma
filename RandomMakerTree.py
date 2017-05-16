 # -*- coding: utf-8 -*-
class RandomMakerTree(object):
	"""RandomMakerTree
	служит для генерации дерева,на входе только csv файл 
	нужен чтобы знать кол-во индикаторов и их имена"""
	
	
	def __init__(self, indicators):
		self.headers = self.set_names(indicators)
		self.count = len(indicators)

	def set_names(self,indicators):
		headers = []
		for i in range(len(indicators)):
			headers.append(str(indicators[i])+"_level")
		return headers

	def RandomNonTerminal(self):
		#создаёт случайный нетерминальный узел
		from Node import NonTerminalNode
		import random
		from params import VALUES
		return NonTerminalNode(random.choice(self.headers),random.choice(VALUES))


	def RandomTerminal(self):
		from Node import TerminalNode
		
		import random
		return TerminalNode(random.choice(['LONG','SHORT']))


	def RandomNode(self):
		import random

		if (random.choice([True,False])):
			return self.RandomNonTerminal()
		else:
			return self.RandomTerminal()

	def MakeTreeRecursive(self,current,level):
		if (current.type == 'NonTerminal'):
			if (level==self.count):
				left = self.RandomTerminal()
				current.left = left
				left.setParent(current)

				right = left.get_mutate()
				current.right = right
				right.setParent(current)

				return

			left = self.RandomNode()
			right = self.RandomNode()

			if (left.type == "NonTerminal"):
				while current.have(left.index):
					left = self.RandomNonTerminal()

			if (right.type == "NonTerminal"): 
				while current.have(right.index):
					right = self.RandomNonTerminal()

			if (str(left) == str(right)):
				right = left.get_mutate()

			left.setParent(current)
			current.setLeft(left)
			self.MakeTreeRecursive(current.left,level+1)
			
			right.setParent(current)
			current.setRight(right)
			self.MakeTreeRecursive(current.right,level+1)

	def MakeTree(self):
		self.root = self.RandomNonTerminal()
		self.MakeTreeRecursive(self.root,0)
		self.root.detect_all_child()
		return self.root

