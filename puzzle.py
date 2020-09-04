
from __future__ import division
from __future__ import print_function
from PuzzleState import PuzzleState

import sys
import math
import time
import queue as Q

import psutil

path_to_goal = []
cost_of_path = 0
nodes_expanded =0
search_depth = 0
max_search_depth = 0
running_time = 0
max_ram_usage = 0

goal_state = None

def write_output(path_to_goal, nodes_expanded, search_depth, max_search_depth, t):
    '''
    Writes output to output.txt 

    :param config->path_to_goal : solution of the puzzle, list of strings, e.g. ['Up','Down','Left']
    :param node_expanded->int : number of nodes expanded before finding a solution
    :param search_depth->int : search depth of the solution
    :param max_search_depth->string : search depth reached before finding the solution
    :param t->float : runtime
    '''
    
    f = open("output.txt", "w+")
    
    f.write("path_to_goal: " + str(path_to_goal))
    f.write("\ncost_of_path: " + str(len(path_to_goal)))
    f.write("\nnodes_expanded: " + str(nodes_expanded))
    f.write("\nsearch_depth: " + str(search_depth))
    f.write("\nmax_search_depth: " + str(max_search_depth))
    f.write("\nrunning_time: " + format(t, '.8f'))
    f.write("\nmax_ram_usage: " + format(psutil.Process().memory_info().rss/1000, '.8f'))
    
    f.close()



def bfs_search(initial_state):
    """BFS search"""
    
    start_time  = time.time()
    
    global path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage
     
    #Initialize Priority Queue:
    frontier = Q.Queue()
    frontier.put(initial_state)
     
    #set of frontier config for testing purposes
    frontier_set = set()
    frontier_set.add(tuple(initial_state.config))
     
    #Initialize explored set:
    explored = set()
    
    while not frontier.empty():
        
        state =  frontier.get()
        explored.add(tuple(state.config))
        
        if test_goal(state):
            search_depth = state.cost
            while(state!=None):
                path_to_goal.append(state.action)
                state=state.parent
            path_to_goal = path_to_goal[::-1]
            path_to_goal = list(path_to_goal[1:])
            end_time = time.time()
            t = end_time - start_time
            write_output(path_to_goal, nodes_expanded, search_depth, max_search_depth,t)
            return state
        
        children = state.expand()
        nodes_expanded +=1
        for child in children:
            if (tuple(child.config) not in explored ) and (tuple(child.config) not in frontier_set):
                frontier_set.add(tuple(child.config))
                frontier.put(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
    return None

def dfs_search(initial_state):
    """DFS search"""
    start_time  = time.time()
    
    global path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage
     
    #Initialize Priority Queue:
    frontier = Q.LifoQueue()
    frontier.put(initial_state)
    
    #set of frontier config for testing purposes
    frontier_set = set()
    frontier_set.add(tuple(initial_state.config))
     
    #Initialize explored set:
    explored = set()
    
    while not frontier.empty():
        
        state =  frontier.get()
        explored.add(tuple(state.config))
        
        if test_goal(state):
            search_depth = state.cost
            while(state!=None):
                path_to_goal.append(state.action)
                state=state.parent
                
            #prepare stats for writeoutput
            path_to_goal = path_to_goal[::-1]
            path_to_goal = list(path_to_goal[1:])
            end_time = time.time()
            t = end_time - start_time
            
            write_output(path_to_goal, nodes_expanded, search_depth, max_search_depth,t)
            return state
        
        children = state.expand()
        children.reverse()
        nodes_expanded +=1
        for child in children:
            if (tuple(child.config) not in explored ) and (tuple(child.config) not in frontier_set):
                frontier_set.add(tuple(child.config))
                frontier.put(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
    return None

def A_star_search(initial_state):
    """A * search"""
    
    start_time  = time.time()
    
    global path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage
     
    #Initialize Priority Queue:
    frontier = Q.PriorityQueue()
    frontier.put(initial_state)

    #set of frontier config for testing purposes
    frontier_set = set()
    frontier_set.add(tuple(initial_state.config))
     
    #Initialize explored set:
    explored = set()
    
    while not frontier.empty():
        
        state =  frontier.get()
        explored.add(tuple(state.config))
        
        if test_goal(state):
            search_depth = state.cost
            while(state!=None):
                path_to_goal.append(state.action)
                state=state.parent
                
            #prepare stats for writeoutput
            path_to_goal = path_to_goal[::-1]
            path_to_goal = list(path_to_goal[1:])
            end_time = time.time()
            t = end_time - start_time
            
            write_output(path_to_goal, nodes_expanded, search_depth, max_search_depth,t)
            return state
        
        children = state.expand()
        children.reverse()
        nodes_expanded +=1
        for child in children:
            if (tuple(child.config) not in explored ) and (tuple(child.config) not in frontier_set):
                frontier_set.add(tuple(child.config))
                frontier.put(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
    return None



def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    for i in range(1, puzzle_state.n ** 2):
        if ((puzzle_state.config[i] - 1) != puzzle_state.config[i-1]):
            return False
    
    return True

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()