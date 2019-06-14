# a2_q2.py

from a2_q1 import *
from csp import *
from a2_q3 import *



# Q2



def check_teams(graph, csp_sol):
	solSize = len(csp_sol)
	for i in range (solSize):
		for j in range(1, solSize):
			if csp_sol[i] == csp_sol[j]:
				if j in graph[i]:
					return false
	return True








