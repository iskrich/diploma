from RandomMakerTree import RandomMakerTree
from pyalgotrade.tools import yahoofinance, quandl

global data_set	
global y_info

global total_mutate
global total_crossovers
global inst

def del_logic_volation(individ):
	nodes = individ.nodes
	nodes.append(individ)

	for node in nodes:
		if (node.type == "NonTerminal"):
			if node.right.type == "NonTerminal":
				rights = node.right.detect_all_child()
				rights.append(node.right)
				for r_node in rights:
					if (r_node.type == "NonTerminal" and r_node.index == node.index and r_node.rate == node.rate):
						if (r_node == r_node.parent.left):
							r_node.parent.setLeft(r_node.right)
						else:
							r_node.parent.setRight(r_node.right)
					elif (r_node.type == "NonTerminal" and r_node.index == node.index):
						if (r_node == r_node.parent.left):
							r_node.parent.setLeft(r_node.left)
						else:
							r_node.parent.setRight(r_node.left)
				
			if node.left.type == "NonTerminal":
				lefts = node.left.detect_all_child()
				lefts.append(node.left)
				for l_node in lefts:
					if (l_node.type == "NonTerminal" and l_node.index == node.index and l_node.rate == node.rate):
						if (l_node == l_node.parent.left):
							l_node.parent.setLeft(l_node.left)
						else:
							l_node.parent.setRight(l_node.left)
	individ.detect_all_child()

def strIndivid(individ):
	returnVal = ""
	for terminal in individ.nodes:
		if (terminal.type == "Terminal"):

			returnVal += "if ("
			curNode = terminal
			parent = curNode.parent

			while (True):
				if parent == None:
					break

				if (parent.left == curNode):
					returnVal += str(parent.index) + "!=" + str(parent.rate)
				else:
					returnVal += str(parent.index) + "==" + str(parent.rate)

				curNode = curNode.parent
				parent = curNode.parent
				if (parent!=None):
					returnVal += " && "
			returnVal+=")\n"
			action = "sell()" if str(terminal) == "SHORT" else "buy()"
			returnVal+="\t then " + action + "\n" 
	print "____"
	print returnVal

def createPic(population,name):
	t = Tree()
	setVisualTree(population,t)
	ts = TreeStyle()
	ts.title.add_face(TextFace(str(population.fitness), fsize=20), column=2)
	ts.show_leaf_name = True
	ts.show_scale   = False
	t.render(name+".png", w=800,h=600, units="px",tree_style = ts)

def setVisualTree(nodeGen, nodeTree, label=""):
	if (nodeGen == None):
		return

	if (nodeGen.type == "NonTerminal"):
		child = nodeTree.add_child(name = label + str(nodeGen))
		child.add_face(TextFace(label + str(nodeGen)), column = 0, position = "branch-top")
		setVisualTree(nodeGen.left,child)
		setVisualTree(nodeGen.right,child)
	else:
		nodeTree.add_child(name = label + str(nodeGen))

def makePopulation(data,tech_indicators,n):
	global  inst
	print "Start creating population with size %d" % n
	global data_set, y_info
	data_set = data
	population = []
	for i in range(n):
		rmt = RandomMakerTree(tech_indicators)
		root = rmt.MakeTree()
		population.append(root)
		nodes = root.detect_all_child()
		root.getFitness(data_set, y_info, inst)
	population = sorted(population,reverse = False, key=lambda x : x.fitness)
	print("Population created")
	return population

def mutate_tree(tree):
	global total_mutate
	total_mutate += 1
	import random
	nodes = find_not_red_nodes(tree)
	if len(nodes)==0:
		return
	first = random.choice(nodes)	
	other_nodes = []
	if first.type == "NonTerminal":
		first_nodes = first.detect_all_child()
		for item in nodes:
			if item not in first_nodes:
				other_nodes.append(item)
	else:
		other_nodes = nodes

	second = random.choice(other_nodes)

	temp = first.clone()

	if (first.parent.left == first):
		first.parent.left = second

	else:
		first.parent.right = second

	second.setParent(first.parent)

	if (second.parent.left == second):
		second.parent.left = temp
	else:
		second.parent.right = temp
	
	temp.setParent(second.parent)
	global data_set
	tree.detect_all_child()

def crossover_tree(tree1,tree2):
	import random
	global total_crossovers
	total_crossovers += 1
	child1 = tree1.clone()
	child2 = tree2.clone()

	nodes1 = find_not_red_nodes(child1)
	nodes2 = find_not_red_nodes(child2)
	if (len(nodes1)==0 or len(nodes2)==0):
		return []
	first = random.choice(nodes1)
	temp = first.clone()
	second = random.choice(nodes2)
	temp2 = second.clone()

	if (first.parent.left == first):
		first.parent.left = temp2
	else:
		first.parent.right = temp2
	temp2.setParent(first.parent)

	if (second.parent.left==second):
		second.parent.left = temp
	else:
		second.parent.right = temp
	temp.setParent(second.parent)
	
	child1.detect_all_child()
	child2.detect_all_child()
	return [child1,child2]

def roulette_wheel(population):
	import random

	minimal_fitness = min(p.fitness for p in population)
	normal_fitness = [p.fitness+abs(minimal_fitness) for p in population]
	sum_fitness = sum(normal_fitness)+0.0001
	result_population = []
	for i  in range(len(normal_fitness)):
		if random.random() < normal_fitness[i]/sum_fitness:
			result_population.append(population[i])

	return result_population

def set_red_rules(population,red_rules):
	global inst
	new_population = []
	for i in range(len(population)):
		root = red_rules.clone()
		tail = find_red_tail(root)
		tail.setLeft(population[i])
		new_population.append(root)
		
	for individ in new_population:
		individ.getFitness(data_set, y_info, inst)
		individ.detect_all_child()
	return new_population

def find_red_tail(node):
	if node.left == None:
		return node
	return find_red_tail(node.left)

def find_not_red_nodes(individ):
	nodes = []
	individ.detect_all_child()
	for node in individ.nodes:
		if (node.type=="Terminal" and "cross" not in node.parent.index):
			nodes.append(node)
		elif (node.type=="NonTerminal" and "cross" not in node.index):
			nodes.append(node)
	return nodes

def genetic_algoritm(N, gens, s,m,data,tech_indicators, instrument, year, red_rules=None):
	global data_set, total_crossovers, total_mutate, y_info, inst
	inst = instrument
	start = int(year.split('-')[2])
	y_info = quandl.build_feed("WIKI", [instrument], start, start, ".")

	total_crossovers = 0
	total_mutate = 0
	population = makePopulation(data,tech_indicators,N)
	if red_rules is not None:
		population = set_red_rules(population,red_rules)

	for i in range(gens):
		print "Create %d generation" % i
		population = next_generation(s,m,population)

	#createPic(population[len(population)-1],"1")
	print "Delete logic violation"
	print "Testing stage is over, best fitness is %f" % population[len(population)-1].fitness
	print "Total mutates %d" % total_mutate
	print "Total crossovers %d" % total_crossovers
	#createPic(population[len(population)-1],"data/strat_fruct")
	#population[len(population)-1].getFitness(data_set,False)
	return population[len(population)-1]

def next_generation(s,m,population):
	import random
	N = len(population)
	next = []
	s = 1-s
	while s*N > len(next):
		new = roulette_wheel(population)
		for item in new:
			next.append(item)

	while N > len(next):
		next+=crossover_tree(random.choice(next),random.choice(next))
	
	for i in range(int(m*N)):
		mutate_tree(random.choice(next))

	for i in range(int(N/4)):
		next[i].invert()

	global data_set, inst

	for individ in next:
		individ.getFitness(data_set, y_info, inst)
		individ.detect_all_child()

	next = sorted(next,reverse = False, key=lambda x : x.fitness)
	return next