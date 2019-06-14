# a2_q1.py

import random 


#Q1

"""
n = number of people
p = probability 
"""

def rand_graph(n,p):
	graph = {}
	#creating an empty graph of size n (n being # of people)
	for x in range(n):
		graph[x] = []
	#loop through the graph and if p > random generated number between [0,1), assign 2 people to be friends 
	for y in range(n):
		for z in range(y+1, n):
			if (random.random() < p):
				graph[y].append(z)
				graph[z].append(y)
	return graph
	


