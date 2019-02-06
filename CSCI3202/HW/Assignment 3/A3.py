from collections import deque
from collections import OrderedDict
import heapq
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
map_distances = dict(
    chi=OrderedDict([("det",283), ("cle",345), ("ind",182)]),
    cle=OrderedDict([("chi",345), ("det",169), ("col",144), ("pit",134), ("buf",189)]),
    ind=OrderedDict([("chi",182), ("col",176)]),
    col=OrderedDict([("ind",176), ("cle",144), ("pit",185)]),
    det=OrderedDict([("chi",283), ("cle",169), ("buf",256)]),
    buf=OrderedDict([("det",256), ("cle",189), ("pit",215), ("syr",150)]),
    pit=OrderedDict([("col",185), ("cle",134), ("buf",215), ("phi",305), ("bal",247)]),
    syr=OrderedDict([("buf",150), ("phi",253), ("new",254), ("bos",312)]),
    bal=OrderedDict([("phi",101), ("pit",247)]),
    phi=OrderedDict([("pit",305), ("bal",101), ("syr",253), ("new",97)]),
    new=OrderedDict([("syr",254), ("phi",97), ("bos",215), ("pro",181)]),
    pro=OrderedDict([("bos",50), ("new",181)]),
    bos=OrderedDict([("pro",50), ("new",215), ("syr",312), ("por",107)]),
    por=OrderedDict([("bos",107)]))

map_times = dict(
    chi=dict(det=280, cle=345, ind=200),
    cle=dict(chi=345, det=170, col=155, pit=145, buf=185),
    ind=dict(chi=200, col=175),
    col=dict(ind=175, cle=155, pit=185),
    det=dict(chi=280, cle=170, buf=270),
    buf=dict(det=270, cle=185, pit=215, syr=145),
    pit=dict(col=185, cle=145, buf=215, phi=305, bal=255),
    syr=dict(buf=145, phi=245, new=260, bos=290),
    bal=dict(phi=145, pit=255),
    phi=dict(pit=305, bal=145, syr=245, new=150),
    new=dict(syr=260, phi=150, bos=270, pro=260),
    pro=dict(bos=90, new=260),
    bos=dict(pro=90, new=270, syr=290, por=120),
    por=dict(bos=120))

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





# Solution:
def breadth_first(start,goal,state_cost,return_cost):
	numVerticies = 14 
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
	nodes = dict()
	nodes[start] = None
	queue = []
	path2 = []
	cost = 0
	queue.append(start)
	visited[start] = True
	while queue:
		s = queue.pop(0)
		if s == goal:
			path2 = path(nodes,goal)
			if return_cost == True:
				cost = pathcost(path2,map_distances)
				return path2,cost
			else:
				return path2
		for keys,values in state_cost[s].items():
			if visited[keys] == False:
				nodes[keys] = s
				queue.append(keys)
				visited[keys] = True
	return nodes

def depth_first(start,goal,state_cost,return_cost):
	nodes = dict()
	nodes[start] = None
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
	queue = []
	path2 = []
	cost = 0
	stack = []
	stack.append(start)
	while stack:
		nodes[start] = None
		#print(nodes)
		s = stack.pop(0)
		if s == goal:
			path2 = path(nodes,goal)
			if return_cost == True:
				cost = pathcost(path2,map_distances)
				return path2,cost
			else:
				return path2
		for keys,values in state_cost[s].items():
			if visited[keys] == False:
				visited[keys] = True
				stack.insert(0,keys)
				nodes[keys] = s


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

    


    			

    
    # add your code here

# Solution:

def uniform_cost(start, goal, state_graph, return_cost=False):
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

	while pQueue:
		cost,state = pQueue.pop()
		if visited[state] == False:
			visited[state] = True

			if state == goal:
				return path(pQueue.states,goal),cost
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



    # add your code here
#print(uniform_cost('chi','pit',map_distances,True))
#print(path)
#print(cost)
#print(uniform_cost('new','chi',map_distances,True))
#print(breadth_first('new','chi',map_distances,True))
#print(depth_first('new','chi',map_distances,True))
# add your code here                
# first, grab the time-optimal route from New York to Chicago, using the uniform cost search
start = 'chi'
goal = 'new'
graph = map_times
route, time = uniform_cost(start, goal, graph, True)
#print(route)
# set parameters
i = 0
m = map_times[route[i]][route[i+1]]
sigma = np.log(1.1)

# sample step costs
sample = stats.lognorm.rvs(s=sigma, scale=m, size=10000)


# Solution:

# set up numpy array to hold the samples from the uncertain step cost distributions, for each step along the route
# (have -1 as number of columns for step_costs because with N states, there are N-1 steps between them)


n_sample = 10000
step_costs = np.zeros((n_sample,len(route)-1))
#print(step_costs)

# set parameters (now m changes with location)
sigma = np.log(1.1)

# sample step costs
for i in range(0,len(route)-1):
	m = map_times[route[i]][route[i+1]]
	step_costs[:,i]= stats.lognorm.rvs(s=sigma, scale=m, size=10000)
    # add your code here
    
    # add your code here               
# add up the total path costs

path_costs = np.zeros(n_sample)
for i in range(0,len(route)-1):
	path_costs +=  step_costs[:,i]# add your code here 
# add your code here   
 
print(step_costs[:,1])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(step_costs[:,0], 'auto', density=True, label = 'new->syr')
ax.hist(step_costs[:,1], 'auto', density=True, label = 'syr->buf')
ax.hist(step_costs[:,2], 'auto', density=True, label = 'buf->cle')
ax.hist(step_costs[:,3], 'auto', density=True, label = 'cle->chi')
ax.legend(loc='upper-right')
fig.canvas.draw()
plt.xlabel("Cost per step")
plt.ylabel("Distribution")
plt.title('Uncertainty in Travel Steps')
plt.show()         
print('probability that Neal making it to Chicago in time for that turkey: {:0.1f}'.format(np.sum(path_costs <= 940)/len(path_costs)))


