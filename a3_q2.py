#a3_q2.py

import os

import random 

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

#________________________________________________________________________Begin of all helper functions

#Every node can be exactly one color
#function for writing out the propositional logic sentence for "exactly one" for a given # of literal
def exactly_one(rc):
    exactly_one = ""
    for i in range(len(rc)):
        if i == 0:
            exactly_one += rc[i]
        else:
            exactly_one += (" " + rc[i])
    
    exactly_one += " 0"

    for i in range(len(rc)):
        for j in range(i+1, len(rc)):
            exactly_one += ("\n" + "-" + rc[i] + " " + "-" + rc[j] + " 0")

    
   

    return exactly_one



#Every connected edge can be at most one color 
#function for writing out the propositional logic sentence for "at most one" for a given # of literal
def at_most_one(diagonals):
    at_most_one = ""
    for i in range(len(diagonals)):
        for j in range(i+1, len(diagonals)):
            if i == 0:
                if j == 1:
                    at_most_one += ("-" + diagonals[i] + " " + "-" + diagonals[j] + " 0")
                else:
                    at_most_one += ("\n" + "-" + diagonals[i] + " " + "-" + diagonals[j] + " 0")
            else:
                at_most_one += ("\n" + "-" + diagonals[i] + " " + "-" + diagonals[j] + " 0")
                


    return at_most_one

def notEqual(var1, var2):
  constraints = []
  for i in range(len(var1)):
    constraints.append("-" + str(var1[i]) + " " + "-" + var2[i] + " 0")
  return constraints


def getClauseCount(inputFile):
    clauseCount = 0
    with open(inputFile, 'r') as reader:
        for lines in enumerate(reader):
            clauseCount += 1 
    return clauseCount - 2
        
def writeClauseCount(inputFile, numOfVariables, clauseCount):
    with open(inputFile, 'r') as reader:
        lines = reader.readlines()
    lines[1] = "p cnf " + str (numOfVariables) + " " + str(clauseCount) + "\n"
    with open(inputFile, 'w') as writer:
        for line in lines:
            writer.write(line)

def makeVariables(graph):
  variables = []
  variablesTracker = 0
  for i in range(len(graph)):
    variables.append([str(variablesTracker+1)])
    variablesTracker += 1
    for j in range(len(graph)-1):
      variables[i].append(str(variablesTracker+1))
      variablesTracker += 1
  return variables


def freeColors(var1, var2):
  freeColors = []
  for i in range(len(var1)):
    for j in range(len(var2)):
      freeColors.append(str(var1[i]) + " " + str(var2[j]) + " 0 \n")
  return freeColors

def constraintColors(var1, var2):
  constraintColors = []
  for i in range(len(var1)):
    for j in range(len(var2)):
      if i != j:
        constraintColors.append(str(var1[i]) + " " + str(var2[j]) + " 0 \n")
  return constraintColors 

def makeEdges (graph):
  allEdges = []
  for i in range(len(graph)):
    allEdges.append(i)
  return allEdges

def getEdge(graph, iteration):
  isEdge = []
  for j in range(len(graph[iteration])):
    isEdge.append(graph[iteration][j])
  return isEdge

def getNotEdge(allEdges, graph, iteration, isEdge):
  notEdge = []
  for k in allEdges:
    if k not in isEdge and k != iteration:
      notEdge.append(k)
  return notEdge

def make_ice_breaker_sat(graph,k):
  variables = makeVariables(graph)  
  miniSatInput = ""
  allEdges = makeEdges(graph)
  for i in variables:
    miniSatInput += (exactly_one(i) + "\n")
  for i in range(len(graph)):
    for j in range(len(graph[i])):
     constraint = notEqual(variables[i], variables[(graph[i][j])])
     for c in constraint:
       miniSatInput += c + "\n"
 



  fileName = "N=" + str(k) + "-icebreaker-problem.txt"
  firstLine = "c N=" + str(k) + " ice breaker problem" + "\n"
  secondLine = "p cnf " + str(k*k) + " " + str(0) + "\n"
  with open(fileName, 'w') as writer:
        writer.write(firstLine)
        writer.write(secondLine)
        writer.write(miniSatInput)
  clauseCount = getClauseCount(fileName)
  writeClauseCount(fileName, k*k, clauseCount)  


def find_min_teams(graph):
  make_ice_breaker_sat(graph, len(graph))
  numOfTeam = 0
  teamTrack = {}
  for i in range(len(graph)):
    teamTrack[i] = 0
  miniSatInputName = "N=" + str(len(graph)) + "-icebreaker-problem.txt"
  os.system("minisat " + miniSatInputName + " result.txt")
  fileName = "result.txt"
  with open(fileName, 'r') as reader:
    sol = reader.readlines()
  sol = sol[1].split(" ")
  sol.remove("0\n")
  teams = ([sol[x:x+len(graph)] for x in range(0, len(sol), len(graph))])
  for assignment in teams:
    for j in range(len(assignment)):
      if int(assignment[j]) > 0:
        teamTrack[j] += 1
  for i in range(len(teamTrack)):
    if teamTrack[i] != 0:
      numOfTeam += 1
  return numOfTeam

