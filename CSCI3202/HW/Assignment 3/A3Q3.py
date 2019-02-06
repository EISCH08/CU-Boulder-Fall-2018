import numpy as np
def maze_to_graph(maze):
	graph = dict()
	rows=len(maze)
	colums = len(maze[0])
	for i in range(0,rows):
		for j in range(0,colums): 
			 if maze[i][j] == 0:
			 	graph[(j,i)] = dict()       
	

	for x,y in graph:
		if(x,y+1) in graph:
			graph[x,y][x,y+1] = "N"
		if(x,y-1) in graph:
			graph[x,y][x,y-1] = "S"
		if(x+1,y) in graph:
			graph[x,y][x+1,y] = "E"
		if(x-1,y) in graph:
			graph[x,y][x-1,y] = "W"
		

	return graph
# Example 1 to print output
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

#print(testgraph[(1,1)])
#print(testgraph[(1,2)])
#print(testgraph[(2,2)])
maze = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                 [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
                 [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                 [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                 [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
                 [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

testgraph = maze_to_graph(maze)
print(testgraph[1,1])
def DFSUntil(v,visited):
	visited[v] = True


def depth_first(start,goal,state_cost):
	nodes = dict()
	nodes[start] = None
	visited =[]
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
			return path2
		for keys,values in state_cost[s].items():
			if keys not in visited:
				visited.append(keys)
				stack.insert(0,keys)
				nodes[keys] = s






def breadth_first(start,goal,graph):
	nodes = dict()
	nodes[start] = None
	visited = [start]
	steps = 0
	queue = []
	queue.append(start)
	while queue:
		s = queue.pop(0)
		if s == goal:
			return path(nodes,goal)
		for i in graph[s]:
			if i not in visited:
				queue.append(i)
				visited.append(i)
				nodes[i] = s
maze_sol_dfs = depth_first((1,1), (10,10), testgraph)
#print(maze_sol_dfs)
########### Example 2 ######
#[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (8, 2), (8, 3), (9, 3), (10, 3), (10, 4), (10, 5), (9, 5), (8, 5), (7, 5), (6, 5), (6, 6), (6, 7), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (10, 9), (10, 10)]
#([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (8, 2), (8, 3), (9, 3), (10, 3), (10, 4), (10, 5), (10, 6), (9, 5), (8, 5), (7, 5), (6, 5), (6, 6), (6, 7), (6, 8), (7, 8), (8, 8), (8, 7), (9, 8), (10, 8), (10, 9), (10, 10)], 31)
#testmaze = np.array([[1, 1, 1, 1, 1],[1, 0, 0, 0, 1],[1, 0, 0, 0, 1],[1, 1, 1, 1, 1]])
#print(maze_to_graph(testmaze))
# testgraph = maze_to_graph(testmaze)
# print(testgraph[(1,1)])
# print(testgraph[(1,2)])
# print(testgraph[(2,1)])
# print(testgraph[(2,2)])
# print(testgraph[(3,1)])
# print(testgraph[(3,2)])
