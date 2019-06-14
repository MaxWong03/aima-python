# a1.py

import time
from search import *
from random import *
from tests.test_search import *

class YPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a Y-Shape board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) 

    The indices of the Y-Shape board will look like this

    0   1
    2 3 4
    5 6 7
      8



"""
 
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']       
        index_blank_square = self.find_blank_square(state)
        cantMoveUp = (0,1,3) #tuple that contains squares that can't move up
        cantMoveDown = (5,7,8) #tuple that contains squares that can't move down
        cantMoveLeft = (0,1,2,5,8) #tuple that contains squares that can't move left
        cantMoveRight = (0,1,4,7,8) #tuples that contains squares that can't move right 

        if index_blank_square in cantMoveLeft:
            possible_actions.remove('LEFT')
        if index_blank_square in cantMoveUp:
            possible_actions.remove('UP')
        if index_blank_square in cantMoveRight:
            possible_actions.remove('RIGHT')
        if index_blank_square in cantMoveDown:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        """
        The Y shaped borad leads to 2 exceptions:
        
        0   1
        2 3 4
        5 6 7
          8

        1) going from index 0 to index 2 ( and vice versa) 
        2) going from index 6 to index 8 ( and vice versa)
        
        The index changes going up and down should be 2 in these 2 incases
        """

        deltaException = {'UP':-2, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
        blankException = (0,2,6,8)
        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        if blank in blankException:
           neighbor = blank + deltaException[action]
        else:
           neighbor = blank + delta[action]
        
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

  


    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
                    inversion += 1
     
        return inversion % 2 == 0
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        x, y = 0, 0
        
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        mhdx = 0
        mhdy = 0
        
        for i in range(9):
           mhdx = abs(index_goal[i][0] - index_state[i][0]) + mhdx
           mhdy = abs(index_goal[i][1] - index_state[i][1]) + mhdy
        
        return (mhdx + mhdy)

    def maxHeuristic(self, node):
        """
        Return the max value between the heuristic value obtained from using the
        Manhattan Distance heuristic and Misplaced Tile heuristic
        """
        misplacedH = self.h(node)
        manhattanH = self.manhattan(node)
        return (max(misplacedH, manhattanH))
# ____________________________________________________________End of YPuzzle

def displayY(state):
    """
    Helper function to display the state of YPuzzle
    the implementation of this function is similar to that of display 
    """
    stateDisplay = [0,0,0,0,0,0,0,0,0] 
    for x in range(9):
        stateDisplay[x] = state[x]
        if (stateDisplay[x] == 0):
              stateDisplay[x] = "*"
    print(stateDisplay[0]," " ,stateDisplay[1])
    print(stateDisplay[2],stateDisplay[3],stateDisplay[4])
    print(stateDisplay[5],stateDisplay[6],stateDisplay[7])
    print(" ",stateDisplay[8]," ")


#____________________________________________________________End of displayY

def make_rand_Ypuzzle():
	# helper function that makes a random instnaces of the Ypuzzle, the logic behind the implementation of this function as the same as make_rand_8puzzle()
	
	puzzleNum = [9,9,9,9,9,9,9,9,9]
	for x in range(9):
		num = randint(0, 8)
		while num in puzzleNum:
			num = randint(0,8)
		puzzleNum[x] = num

	puzzleSet = (puzzleNum[0],puzzleNum[1],puzzleNum[2],puzzleNum[3],puzzleNum[4],puzzleNum[5],puzzleNum[6],puzzleNum[7],puzzleNum[8])

	puzzle = YPuzzle(puzzleSet)

	while (puzzle.check_solvability(puzzle.initial) == False):
		puzzleNum = [9,9,9,9,9,9,9,9,9]
		for x in range(9):
			num = randint(0, 8)
			while num in puzzleNum:
				num = randint(0,8)
			puzzleNum[x] = num
		puzzleSet = (puzzleNum[0],puzzleNum[1],puzzleNum[2],puzzleNum[3],puzzleNum[4],puzzleNum[5],puzzleNum[6],puzzleNum[7],puzzleNum[8])

		puzzle = YPuzzle(puzzleSet)


	return puzzle

#______________________________________________________End of make_rand_Ypuzzle
class EightPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """
 
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']       
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]


        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
                    inversion += 1

        return inversion % 2 == 0
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        state = node.state
        index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
        index_state = {}
        index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        x, y = 0, 0
        
        for i in range(len(state)):
            index_state[state[i]] = index[i]
        
        mhdx = 0
        mhdy = 0
        
        for i in range(9):
           mhdx = abs(index_goal[i][0] - index_state[i][0]) + mhdx
           mhdy = abs(index_goal[i][1] - index_state[i][1]) + mhdy
        
        return (mhdx + mhdy)

    def maxHeuristic(self, node):
        """
        Return the max value between the heuristic value obtained from using the
        Manhattan Distance heuristic and Misplaced Tile heuristic
        """
        misplacedH = self.h(node)
        manhattanH = self.manhattan(node)
        return (max(misplacedH, manhattanH))
# ___________________________________________________________End of EightPuzzle

def astar_searchMaxHeuristic(problem, h=None):
    # A*-search using the Max value between Manhattan distance heurisitic and Misplaced tile heuristic 

    h = memoize(h or problem.maxHeuristic, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def astar_searchManhattan(problem, h=None):
    # A*-search using the Manhattan distance heuristic 

    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

#__________________________________________________________End of astar_Searches

def make_rand_8puzzle():
	"""
	Helper functino that make a random instances of the 8 puzzle
	

	Since the state is a tuple and the tuple values can not be change, we
	first use an array of number 9s, to represet the state. And then with 
	each iteration in the for loop we generate a random number between 0-8
        
        Then we check rather or not the number already exists in the array
        And if it does we generate another random number until the number is 
        unqiue

	We repeat this process until each number in the array (state) is unique

	We then create a tuple with the value and order of the array and check 		rather or not the puzzle created is solvable, if it is not then we 		repeat the puzzle generation process until the puzzle is solvable

	""" 

	puzzleNum = [9,9,9,9,9,9,9,9,9]
	for x in range(9):
		num = randint(0, 8)
		while num in puzzleNum:
			num = randint(0,8)
		puzzleNum[x] = num

	puzzleSet = (puzzleNum[0],puzzleNum[1],puzzleNum[2],puzzleNum[3],puzzleNum[4],puzzleNum[5],puzzleNum[6],puzzleNum[7],puzzleNum[8])

	puzzle = EightPuzzle(puzzleSet)

	while (puzzle.check_solvability(puzzle.initial) == False):
		puzzleNum = [9,9,9,9,9,9,9,9,9]
		for x in range(9):
			num = randint(0, 8)
			while num in puzzleNum:
				num = randint(0,8)
			puzzleNum[x] = num
		puzzleSet = (puzzleNum[0],puzzleNum[1],puzzleNum[2],puzzleNum[3],puzzleNum[4],puzzleNum[5],puzzleNum[6],puzzleNum[7],puzzleNum[8])

		puzzle = EightPuzzle(puzzleSet)


	return puzzle

#_______________________________________________________End of make_rand_8puzzle


def display(state):
	"""
        Helper function that display the state of a 8 puzzle problem

	Similar to make_rand_8puzzle, since the state is a tuple and the value inside can not be changed, we simply use an array to store the values and indices of the tuple, and when we encounter 0 we change the array value to * so that we can display it as * 
	"""
	stateDisplay = [0,0,0,0,0,0,0,0,0] 
	for x in range(9):
		stateDisplay[x] = state[x]
		if (stateDisplay[x] == 0):
			stateDisplay[x] = "*"
	print(stateDisplay[0],stateDisplay[1],stateDisplay[2])
	print(stateDisplay[3],stateDisplay[4],stateDisplay[5])
	print(stateDisplay[6],stateDisplay[7],stateDisplay[8])


#______________________________________________________________End of display

def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    removedFrontier = 0 #variable that keep tracks of the number of nodes removed from frontier
    while frontier:
        node = frontier.pop()
        removedFrontier += 1
        if problem.goal_test(node.state):
            return [node, removedFrontier]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

#______________________________________________end of best_first_graph_search

"""
8-Puzzle Probelm Analysis

"""



for i in range(10): 

	puzzle = make_rand_8puzzle()
	display(puzzle.initial)

	#recording the time, pathcost, and #of frontier removed for default heurstic search algorithm
	start = time.time()
	result = astar_search(puzzle)
	end = time.time()
	print("Data for A*-Search using misplaced tile heuristic...")
	print ("Time it took to solve the problem: ",end-start)
	print("Path cost is: ",result[0].path_cost)
	print ("# of nodes removed from frontier is: ",result[1], "\n")


	#recording the time, pathcost, and #of frontier removed for manhattan algorithm
	startMan = time.time()
	resultMan = astar_searchManhattan(puzzle)
	endMan = time.time()
	print("Data for A*-Search using Manhattan distance heuristic...")
	print ("Time it took to solve the problem: ",endMan-startMan)
	print("Path cost is: ",resultMan[0].path_cost)
	print ("# of nodes removed from frontier is: ",resultMan[1], "\n")


	#recording the time, pathcost, and #of frontier removed for max herustic
	startMax = time.time()
	resultMax = astar_searchMaxHeuristic(puzzle)
	endMax = time.time()
	print("Data for A*-Search using the max of misplaced tile heuristic and Manhattan distance heuristic...")
	print ("Time it took to solve the problem: ",endMax-startMax)
	print("Path cost is: ",resultMax[0].path_cost)
	print ("# of nodes removed from frontier is: ",resultMax[1], "\n")




"""
Y-Puzzle Problem Analysis

Since the check_solveability function doesn't always return the correct answer, we will put the result of the A*-search in a while loop

If the puzzle is unsolveable (which result will be None) then we will keep generating new instances of the Y puzzle problem until the puzzle is solveable

"""



startY = time.time()
ypuzzle = make_rand_Ypuzzle()
resultY = astar_search(ypuzzle)
endY = time.time()

for i in range(10):
	while resultY == None:
		ypuzzle = make_rand_Ypuzzle()
		startY = time.time()
		resultY = astar_search(ypuzzle)
		endY = time.time()

	#recording the time, pathcost, and #of frontier removed for default heurstic search algorithm
	displayY(ypuzzle.initial)

	print("Data for A*-Search using misplaced tile heuristic...")
	print ("Time it took to solve the problem: ",endY-startY)
	print("Path cost is: ",resultY[0].path_cost)
	print ("# of nodes removed from frontier is: ",resultY[1], "\n")
	
	

	#recording the time, pathcost, and #of frontier removed for manhattan algorithm
	startManY = time.time()
	resultManY = astar_searchManhattan(ypuzzle)
	endManY = time.time()
	print("Data for A*-Search using Manhattan distance heuristic...")
	print ("Time it took to solve the problem: ", endManY-startManY)
	print("Path cost is: ",resultManY[0].path_cost)
	print ("# of nodes removed from frontier is: ",resultManY[1], "\n")

	#recording the time, pathcost, and #of frontier removed for max herustic
	startMaxY = time.time()
	resultMaxY = astar_searchMaxHeuristic(ypuzzle)
	endMaxY = time.time()
	print("Data for A*-Search using the max of misplaced tile heuristic and Manhattan distance heuristic...")
	print ("Time it took to solve the problem: ",endMaxY-startMaxY)
	print("Path cost is: ",resultMaxY[0].path_cost)
	print ("# of nodes removed from frontier is: ",resultMaxY[1], "\n")

	#Make new instances of the ypuzzle problem 
	
	ypuzzle = make_rand_Ypuzzle()
	startY = time.time()
	resultY = astar_search(ypuzzle)
	endY = time.time()









			


