import numpy as np
import heapq
import unittest

def path(previous, s): 
    '''
    `previous` is a dictionary chaining together the predecessor state that led to each state
    `s` will be None for the initial state
    otherwise, start from the last state `s` and recursively trace `previous` back to the initial state,
    constructing a list of states visited as we go
    '''
    if s is None:
        return []
    else:
        return path(previous, previous[s])+[s]

def pathcost(path, step_costs):
    '''
    add up the step costs along a path, which is assumed to be a list output from the `path` function above
    '''
    cost = 0
    for s in range(len(path)-1):
        cost += step_costs[path[s]][path[s+1]]
    return cost

map_distances = dict(
    chi=dict(det=283, cle=345, ind=182),
    cle=dict(chi=345, det=169, col=144, pit=134, buf=189),
    ind=dict(chi=182, col=176),
    col=dict(ind=176, cle=144, pit=185),
    det=dict(chi=283, cle=169, buf=256),
    buf=dict(det=256, cle=189, pit=215, syr=150),
    pit=dict(col=185, cle=134, buf=215, phi=305, bal=247),
    syr=dict(buf=150, phi=253, new=254, bos=312),
    bal=dict(phi=101, pit=247),
    phi=dict(pit=305, bal=101, syr=253, new=97),
    new=dict(syr=254, phi=97, bos=215, pro=181),
    pro=dict(bos=50, new=181),
    bos=dict(pro=50, new=215, syr=312, por=107),
    por=dict(bos=107))

sld_providence = dict(
    chi=833,
    cle=531,
    ind=782,
    col=618,
    det=596,
    buf=385,
    pit=458,
    syr=253,
    bal=325,
    phi=236,
    new=157,
    pro=0,
    bos=38,
    por=136)

class Frontier_PQ:
    ''' frontier class for uniform search, ordered by path cost '''
    def __init__(self,start,cost):
        self.start = start
        self.cost = 0
        self.states = dict() #lowest cost to each state
        self.states[start] = None
        self.q = [(cost,start)] #keeps track of  
    def find(self,state):
        index = 0
        for cost,st in self.q:
            if st == state:
                return index
            index += 1


    def replace(self,state,cost):
        heapq.heapreplace(self.q,(cost,state))

    def add(self,state, cost):
        heapq.heappush(self.q,(cost,state))

    def pop(self):
        return heapq.heappop(self.q)

    


def uniform_cost(start, goal, state_graph, return_cost = False, return_nexp=False):
    # add your code here
    pQueue = Frontier_PQ(start,0)
    visited =dict(chi= False,
    cle=False,
    ind=False,
    col=False,
    det=False,
    buf=False,
    pit=False,
    syr=False,
    bal=False,
    phi=False,
    new=False,
    pro=False,
    bos=False,
    por=False)
    nodesExpanded = []
    while pQueue:
        cost,state = pQueue.pop()
        if visited[state] == False:
            visited[state] = True

            if state == goal:
                nodesExpanded.append(state)
                if(return_cost):
                    if(return_nexp):
                        return path(pQueue.states,goal),cost,len(nodesExpanded)
                    else:
                        return path(pQueue.states,goal),cost
                else:
                    if(return_nexp):
                        return path(pQueue.states,goal),len(nodesExpanded)
                    else:
                        return path(pQueue.states,goal)
            for keys,values in state_graph[state].items():
                if visited[keys] == False:
                    total_Cost = cost + values
                    if pQueue.find(keys) == None:
                        
                        pQueue.add(keys,total_Cost)
                        pQueue.states[keys] = state
                    else:
                        index = pQueue.find(keys)
                        value,key = pQueue.q[index]
                        if value > total_Cost:
                            pQueue.q[index] = (total_Cost,key)
                            pQueue.states[key] = state
            nodesExpanded.append(state)




def heuristic_sld_providence(state):
    return sld_providence[state]


def astar_search(start, goal, state_graph, heuristic, return_cost, return_nexp=False):
    openList = Frontier_PQ(start,0)
    closedList = []
    gFunction = dict() #movement cost from one point to another
    hFunction = dict() #direct cost from the heuristic function
    fFunction = dict() # sum of both gFunction and hFunction
    for value in state_graph:
        fFunction[value] = 1000000
        gFunction[value] = 0
        hFunction[value] = heuristic(value)
    fFunction[start] = 0 
    nodesExpanded = 0 
    while openList:
        cost,state = openList.pop()
        closedList.append(state)
        for value,key in state_graph[state].items():
            if value == goal:
                gFunction[value] = gFunction[state] + state_graph[state][value]
                fFunction[value] = gFunction[value] + hFunction[value]
                closedList.append(value)
                openList.states[value] = state
                if(return_cost):
                    if(return_nexp):
                        return path(openList.states,goal),pathcost(path(openList.states,goal),state_graph),len(closedList)
                    else:
                        return path(openList.states,goal),pathcost(path(openList.states,goal),state_graph)
                else:
                    if(return_nexp):
                        return path(openList.states,goal),len(closedList)
                    else:
                        return path(openList.states,goal)
            if value not in closedList: #nodes that haven't been explored yet
                if fFunction[value] > (gFunction[value] + state_graph[state][value] + hFunction[state] + fFunction[state]): #fFunction needs to be updated to the lower value and added to pQueue
                    gFunction[value] = gFunction[value] + state_graph[state][value]
                    fFunction[value] = gFunction[value] + hFunction[value] + fFunction[state]
                    openList.add(value,fFunction[value])
                    openList.states[value] = state
        



                
        







path,cost,nodesExpanded= uniform_cost('phi','pro',map_distances,return_cost=True,return_nexp=True)

print(nodesExpanded)
#print(nexp)
#print(heuristic_sld_providence('cle'))






