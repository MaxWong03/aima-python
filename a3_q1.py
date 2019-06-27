#a3_q1.py

import numpy as np
import os
import math


#________________________________________________________________________Begin of all helper functions

#Rows and columns can have exactly one queen
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



#Diagonals can at most one queen
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

#return the diagonals of the queens problem
def getDiagonals(N):
    queen_matrix = np.arange(N*N).reshape(N,N)

    diagonals = [queen_matrix[::-1,:].diagonal(i) for i in range(-queen_matrix.shape[0]+1,queen_matrix.shape[1])]
    diagonals.extend(queen_matrix.diagonal(i) for i in range(queen_matrix.shape[1]-1,-queen_matrix.shape[0],-1))

    #the above method returns all digonals of a matrix but also return the "corner" of a matrix whic isnt what we want, so the following for loop delete all instances of the "corners"
    all_diagonals = []

    for i in diagonals:
        if len(i) != 1:
            all_diagonals.append(i)

    #make all the diagonals a string for later input
    strDiagonals = []
    for i in range(len(all_diagonals)):
        strDiagonals.append([])
        for j in range(len(all_diagonals[i])):
            strDiagonals[i].append(str(all_diagonals[i][j]+1))
            

    return strDiagonals

#return all the rows of the queens problem
def getRows(N):
    queen_matrix = np.arange(N*N).reshape(N,N)
    strRow = []
    #make all the rows to a string for later input
    for i in range(len(queen_matrix)):
        strRow.append([])
        for j in range(len(queen_matrix[i])):
            strRow[i].append(str(queen_matrix[i][j]+1))
    return strRow


    

#return all the columns of the queens problem
def getColumns(N):
    queen_matrix = np.arange(N*N).reshape(N,N)
    strColumn = []
    #make all the columns to a string for later input
    for i in range(N):
        strColumn.append([])
        for j in range(N):
            strColumn[i].append(str(queen_matrix[j][i]+1))       

    return strColumn


def nQueenProblem(N):
    rows = getRows(N)
    columns = getColumns(N)
    diagonals = getDiagonals(N)
    miniSatInput = ""
    for i in range(len(rows)):
        miniSatInput += (exactly_one(rows[i]) + "\n")
    for j in range(len(columns)):
        miniSatInput += (exactly_one(columns[j]) + "\n")
    for z in range(len(diagonals)):
        if z != (len(diagonals) - 1):
            miniSatInput += (at_most_one(diagonals[z]) + "\n")
        else:
            miniSatInput += (at_most_one(diagonals[z]))
    if N == 2:
        miniSatInput += ("\n" + "3 2 0" + "\n")
        miniSatInput += ("1 4 0") 
    return miniSatInput

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

def parseSolution(sol):
    if sol == "UNSAT":
        return sol
    else:
        sol = sol.split(" ")
        sol.remove("0")
        return sol

def getSolution(inputFile):
    with open(inputFile, 'r') as reader:
        sol = reader.readlines()
    if len(sol) == 1:
        return "UNSAT"
    else: 
        queenPlacement = sol[1].split(" ")
        queenPlacement.remove("0\n")
        return(queenPlacement)


#________________________________________________________________________End of all helper functions

#Q1

def make_queen_sat(N):
    numOfQueen = str(N)
    miniSatInput = nQueenProblem(N)
    fileName = numOfQueen + '-queen.txt'
    firstLine = "c N=" + str(N) + " queens problem" + "\n"
    secondLine = "p cnf " + str(N*N) + " " + str(0) + "\n"
    with open(fileName, 'w') as writer:
        writer.write(firstLine)
        writer.write(secondLine)
        writer.write(miniSatInput)
    clauseCount = getClauseCount(fileName)
    writeClauseCount(fileName, N*N, clauseCount)

def draw_queen_sat_sol(sol):
    sol = parseSolution(sol)
    if sol == "UNSAT":
        print("No Solution")

    elif math.sqrt(len(sol)) > 40:
        print("Too big: N must be less than 40” if N > 40")
        
    else:
        queenSol = []
        for i in range(len(sol)):
            queenSol.append(".")
        for j in range(len(sol)):
            if sol[j][0] != "-":
                queenSol[j] = "Q"
        varPerRow = math.sqrt(len(sol))
        display = ""
        for i in range(len(queenSol)):
            if (i+1)%varPerRow != 0:
                display += queenSol[i] + " "
            else:
                display += (queenSol[i] + "\n")
        print(display)
