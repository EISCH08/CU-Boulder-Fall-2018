from collections import OrderedDict

canada = OrderedDict(
    [("AB"  , ["BC","NT","SK"]),
    ("BC" , ["AB","NT","YT"]),
    ("LB" , ["NF", "NS", "PE","QC"]),
    ("MB" , ["ON","NV","SK"]),
    ("NB" , ["NS","QC"]),
    ("NF" , ["LB","QC"]),
    ("NS" , ["LB","NB","PE"]),
    ("NT" , ["AB","BC","NV","SK","YT"]),
    ("NV" , ["MB","NT"]),
    ("ON" , ["MB","QC"]),
    ("PE" , ["LB","NS","QC"]),
    ("QC" , ["LB","NB","NF","ON","PE"]),  
    ("SK" , ["AB","MB","NT"]),
    ("YT" , ["BC","NT"])])
    
states = ["AB", "BC", "LB", "MB", "NB", "NF", "NS", "NT", "NV", "ON", "PE", "QC", "SK", "YT"]
colors = ["blue", "green", "red"]

class CSP:
    def __init__(self,vars,neighbors,domain):
        self.vars = vars
        self.neighbors = neighbors
        self.domain = domain


def select_most_constraining_variable(csp, assignment):
    constraining = OrderedDict()
    for nodes in csp.vars: #grabs variables
        count = 0 #figures out which has the most edges
        for color in csp.domain:
            if(constraintCheck(assignment,nodes,color,csp)):
                count+=1
        constraining[nodes] = count
    constraining = sorted(constraining.items(), key = lambda x:x[1], reverse = False)
    for nodes,keys in constraining:
        if nodes not in assignment:
            return nodes

def select_least_constraining_variable(csp, assignment):
    constraining = OrderedDict()
    for nodes in csp.vars: #grabs variables
        count = 0 #figures out which has the most edges
        for color in csp.domain:
            if(constraintCheck(assignment,nodes,color,csp)):
                count+=1
        constraining[nodes] = count
    constraining = sorted(constraining.items(), key = lambda x:x[1], reverse = True)
    for nodes,keys in constraining:
        if nodes not in assignment:
            return nodes

def backtracking_search(csp,mcv,lcv):

    

    if (mcv == False) & (lcv == False):
        check,a,count2=recursive_backtracking({},csp,0)
        aNew = OrderedDict(sorted(a.items()))
        #print((aNew,count2))
        return aNew,count2
    elif mcv:
        check2,b,count1 = backtrackingMCV(OrderedDict(),csp,0)
        return((b,count1))
    elif lcv:
        check3,c,count3 = backtrackingLCV(OrderedDict(),csp,0)
        #print(c,count3)
        c = OrderedDict(sorted(c.items()))
        return((c,count3))


def constraintCheck(assignment,node,color,csp): #checks to see if that color can be used
    blueCheck,greenCheck, redCheck = False,False,False

    for neighbors in csp.neighbors[node]: #checks neighbors of checked node
        if neighbors in assignment:
            if(assignment[neighbors] == color):
                return False 
    return True

def recursive_backtracking(assignment,csp,count):
    if len(assignment) == len(csp.neighbors):
        value = count
        return True,assignment,int(value) 
    for neighbor in csp.neighbors: #checks neighbors of assigned nodes
        if neighbor not in assignment:
            for color in csp.domain:
                if constraintCheck(assignment,neighbor,color,csp):
                    assignment[neighbor] = color
                    result = recursive_backtracking(assignment,csp,count+1)
                    if result != False:
                        return result
                    del assignment[neighbor]


            return False


def backtrackingMCV(assignment,csp,count):
    if len(assignment) == len(csp.neighbors):
        return True,assignment,int(count) 
    neighbor = select_most_constraining_variable(csp,assignment)
    if neighbor not in assignment:
        for color in csp.domain:
            if constraintCheck(assignment,neighbor,color,csp):
                assignment[neighbor] = color
                result = backtrackingMCV(assignment,csp,count)
                if result != False:
                    return result
                del assignment[neighbor]


        return False

def backtrackingLCV(assignment,csp,count):
    if len(assignment) == len(csp.neighbors):
        return True,assignment,int(count) 
    neighbor = select_least_constraining_variable(csp,assignment)
    count+=.5
    if neighbor not in assignment:
        for color in csp.domain:
            if constraintCheck(assignment,neighbor,color,csp):
                assignment[neighbor] = color
                result = backtrackingLCV(assignment,csp,count)
                if result != False:
                    count+=1
                    return result
                del assignment[neighbor]

        return False










            

csp = CSP(states, canada, colors)
backtracking_search(csp,False,True)
backtracking_search(csp,True,True)

