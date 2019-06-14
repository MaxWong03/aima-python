#a2_q4.py

import time
from a2_q1 import *
from a2_q2 import *
from a2_q3 import *
from csp import *


class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases. (For example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(N^4) for the
    explicit representation.) In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints, unassigns):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
        self.unassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            self.unassigns += 1

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP:', self, 'with assignment:', assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: nonconflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    def getUnassign(self):
        return self.unassigns

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

# ______________________________________________________________________________

def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors,
               different_values_constraint, 0)
#_______________________________________________________________________________



#Q4



def run_q4():

	#Generate 5 random friendship graphs

	graphs = [rand_graph(100,0.1), rand_graph(100,0.2), rand_graph(100,0.3), rand_graph(100,0.4), rand_graph(100,0.5)]

	#Ice Breaker Problem 1	
	
	stop0 = False
	#begin tracking running time of solver
	cspStartTime0 = time.time()
	for z in range(100):
		if stop0 == False:
			#generating domain
			domain = createColor(z+1, 100)
			#creating CSP
			iceBreaker0 = MapColoringCSP(domain, graphs[0])
			#make CSP Arc consistent
			AC3(iceBreaker0)
			#using min_conflicts to solve CSP
			csp_sol0 = min_conflicts(iceBreaker0)
			
			if csp_sol0 != None:
				#end tracking running time of solver
				cspEndTime0 = time.time()
				print("Ice Breaker Problem for n = 100, p = 0.1")
				print("Solution: ", csp_sol0)
				print("Time it took to solve Ice Breaker Problem 1: ", cspEndTime0-cspStartTime0)
				print("Number of teams people are divided into: ", count_teams(csp_sol0))
				print("Number of assigned CSP variables: ", iceBreaker0.nassigns)
				print("Number of unassigned CSP variables: ", iceBreaker0.getUnassign())
				print("Member count for the largest team: ", countMaxTeam(csp_sol0))
				print("\n")
				stop0 = True
	#Ice Breaker Problem 2	
	
	stop1 = False
	#begin tracking running time of solver
	cspStartTime1 = time.time()
	for z in range(100):
		if stop1 == False:
			#generating domain
			domain = createColor(z+1, 100)
			#creating CSP
			iceBreaker1 = MapColoringCSP(domain, graphs[1])
			#make CSP Arc consistent
			AC3(iceBreaker1)
		
			#using min_conflicts to solve CSP
			csp_sol1 = min_conflicts(iceBreaker1)
			
			if csp_sol1 != None:
				#end tracking running time of solver
				cspEndTime1 = time.time() 
				print("Ice Breaker Problem for n = 100, p = 0.2")
				print("Solution: ", csp_sol1)
				print("Time it took to solve Ice Breaker Problem 2: ", cspEndTime1-cspStartTime1)
				print("Number of teams people are divided into: ", count_teams(csp_sol1))
				print("Number of assigned CSP variables: ", iceBreaker1.nassigns)
				print("Number of unassigned CSP variables: ", iceBreaker1.getUnassign())
				print("Member count for the largest team: ", countMaxTeam(csp_sol1))
				print("\n")
				stop1 = True

	#Ice Breaker Problem 3	
	
	stop2 = False
	#begin tracking running time of solver
	cspStartTime2 = time.time()
	for z in range(100):
		if stop2 == False:
			#generating domain
			domain = createColor(z+1, 100)
			#creating CSP
			iceBreaker2 = MapColoringCSP(domain, graphs[2])
			#make CSP Arc consistent
			AC3(iceBreaker2)
			
			csp_sol2 = min_conflicts(iceBreaker2)
			
			if csp_sol2 != None:
				#end tracking running time of solver
				cspEndTime2 = time.time() 
				print("Ice Breaker Problem for n = 100, p = 0.3")
				print("Solution: ", csp_sol2)
				print("Time it took to solve Ice Breaker Problem 3: ", cspEndTime2-cspStartTime2)
				print("Number of teams people are divided into: ", count_teams(csp_sol2))
				print("Number of assigned CSP variables: ", iceBreaker2.nassigns)
				print("Number of unassigned CSP variables: ", iceBreaker2.getUnassign())
				print("Member count for the largest team: ", countMaxTeam(csp_sol2))
				print("\n")
				stop2 = True

	#Ice Breaker Problem 4	
	
	stop3 = False
	#begin tracking running time of solver
	cspStartTime3 = time.time()
			

	for z in range(100):
		if stop3 == False:
			#generating domain
			domain = createColor(z+1, 100)
			#creating CSP
			iceBreaker3 = MapColoringCSP(domain, graphs[3])
			#make CSP Arc consistent
			AC3(iceBreaker3)
			
			#using min_conflicts to solve CSP
			csp_sol3 = min_conflicts(iceBreaker3)
			
			if csp_sol3 != None:
				#end tracking running time of solver
				cspEndTime3 = time.time() 
				print("Ice Breaker Problem for n = 100, p = 0.4")
				print("Solution: ", csp_sol3)
				print("Time it took to solve Ice Breaker Problem 4: ", cspEndTime3-cspStartTime3)
				print("Number of teams people are divided into: ", count_teams(csp_sol3))
				print("Number of assigned CSP variables: ", iceBreaker3.nassigns)
				print("Number of unassigned CSP variables: ", iceBreaker3.getUnassign())
				print("Member count for the largest team: ", countMaxTeam(csp_sol3))
				print("\n")
				stop3 = True

	#Ice Breaker Problem 5	
	
	stop4 = False
	#begin tracking running time of solver
	cspStartTime4 = time.time()
	for z in range(100):
		if stop4 == False:
			#generating domain
			domain = createColor(z+1, 100)
			#creating CSP
			iceBreaker4 = MapColoringCSP(domain, graphs[4])
			#make CSP Arc consistent
			AC3(iceBreaker4)

			#using min_conflicts to solve CSP
			csp_sol4 = min_conflicts(iceBreaker4)
			
			if csp_sol4 != None:
				#end tracking running time of solver
				cspEndTime4 = time.time() 
				print("Ice Breaker Problem for n = 100, p = 0.5")
				print("Solution: ", csp_sol4)
				print("Time it took to solve Ice Breaker Problem 5: ", cspEndTime4-cspStartTime4)
				print("Number of teams people are divided into: ", count_teams(csp_sol4))
				print("Number of assigned CSP variables: ", iceBreaker4.nassigns)
				print("Number of unassigned CSP variables: ", iceBreaker4.getUnassign())
				print("Member count for the largest team: ", countMaxTeam(csp_sol4))
				print("\n")
				stop4 = True
	

	return True






