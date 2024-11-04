from fourCornerProblem import Problem
from tkinter import *
import time
from itertools import combinations
from problemGraphics import pacmanGraphic 
import heapq
import time

def construct_path(node, visited):
    path = []
    while node:
        food = tuple(node[1])
        node, action = visited[(node[0], food)]
        if action != None:
                if type(action) == list: path = action + path
                else: path = [action] + path
    return path

def bfs(p):
    start = p.startState()
    frontier = [(start, None, None)]
    visited = {}
    count = 0
    while frontier:
        node, parent, action = frontier.pop(0)
        food = tuple(node[1])
        if (node[0], food) in visited: continue
        visited[(node[0], food)] = (parent, action)
        if p.isGoal(node):
            print ('BFS number of nodes explored: ', count)
            return construct_path(node, visited)
        count += 1
        neighbors = p.transition(node)
        for n, a, c in neighbors:
            food = tuple(n[1])
            if (n, node, a) not in frontier and (n[0], food) not in visited:
                frontier.append ((n, node, a))
    return []

def ucs(p):
    # define priority queue: pq
    pq = [(0, p.startState(), None, None)]
    visited = {}
    count = 0
    while pq:
        gCost, node, parent, action = heapq.heappop(pq)

        # Check if node is visited
        food = tuple(node[1])
        if (node[0], food) in visited: continue
        visited[(node[0], food)] = (parent, action)

        # Check if node is the goal node
        if p.isGoal(node):
            print ('ucs number of nodes explored: ', count)
            return gCost, construct_path(node, visited)

        count += 1
        # get neighbors
        neighbors = p.nextStates(node)
        for stepCost, n, a in neighbors:
            food = tuple(n[1])
            newState = (stepCost+gCost, n, node, a)
            heapq.heappush(pq, newState)
    return None

def AStar (p):
    start = p.startState() # get the start state from the Problem
    # define priority queue:
    #   queue element: (heuristic, gCost, node, parent, action)
    pq = [(p.h(start), 0, start, None, None)]
    
    visited = {}
    count = 0 # counter to count the number of nodes explored.
    while pq:
        # pop one node from the priority queue
        fCost, gCost, node, parent, action = heapq.heappop(pq)

        # check if the node is in visited
        food = tuple(node[1])
        if (node[0], food) in visited: continue
        # Add node to visited
        visited[(node[0], food)] = (parent, action)
        # check if the node is a goal node

        if p.isGoal(node):
            print ('A* number of nodes explored: ', count)
            # return total cost and path
            return gCost, construct_path(node, visited)
        
        # count keeps track of the number of nodes explored.
        count += 1

        # Complete one line of code here
        neighbors = p.nextStates(node)
        # get next states or neighbor states by calling nextState
        # from the FourCornerProblem passing in the node.
        
        # loop on all neighbors to add them with their cost
        # to the priority queue
        for step_cost, neighbor, a in neighbors:
            f = gCost + step_cost + p.h(neighbor)
            # Add nodes to priority queue
            newState= (f, gCost+step_cost, neighbor, node, a)
            # complete one line of code here
            # insert newState to the priority queue pq
            heapq.heappush(pq, newState)
            
    return None, None

filename = 'smallSearch.txt'


# Get an instance of the problem:
p = Problem(filename)


# -------------------------------------------------------
# BFS:
# -------------------------------------------------------
 
# record start time
startTime = time.time()
plan = bfs(p)
endTime = time.time()
print (plan)
print ('plan length:', len(plan))
print ('Time: ', (endTime - startTime) * 10**3, "ms")

pac = pacmanGraphic(1300, 700)
pac.setup(p)
pac.runPlan(p, plan)
print ('------------------------')


# -------------------------------------------------------
# UCS:
# -------------------------------------------------------

p = Problem(filename)
startTime = time.time()
p.compute_distances()
cost, plan = ucs(p)
endTime = time.time()
if plan is not None:
    print(plan)
    print('plan length=', len(plan))
    print('cost: ', cost)
    print ('Time: ', (endTime - startTime) * 10**3, "ms")
else:
    print("No valid plan found")


pac = pacmanGraphic(1300, 700)
pac.setup(p)
pac.runPlan(p, plan)
print ('------------------------')


# -------------------------------------------------------
# A*
# -------------------------------------------------------

# Complete one line of code here:
# get an instance of the Problem passing
#    in the file name
p = Problem(filename)

startTime = time.time()
# Complete two lines of code here
# 1) call compute distances method in FourCornersProblem
p.compute_distances()
# 2) Call Astar passing in the instance of the Problem,
#    it returns the cost and the plan similar to ucs
cost, plan = AStar(p)
endTime = time.time()
if plan is not None:
    print('cost: ', cost)
    print(plan)
    print('plan length=', len(plan))
    print ('Time: ', (endTime - startTime) * 10**3, "ms")
else:
    print("No valid plan found")
# 3) print the cost, the plan and the plan length


# Leave this code for plan execute and
# moves pacman to collect the dots.
pac = pacmanGraphic(1300, 700)
pac.setup(p)
pac.runPlan(p, plan)
print ('------------------------')

