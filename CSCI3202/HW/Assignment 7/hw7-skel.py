from scipy import stats
import unittest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## For the sake of brevity...
T, F = True, False

def P(var, value, evidence={}):
    '''The probability distribution for P(var | evidence), 
    when all parent variables are known (in evidence)'''
    if len(var.parents)==1:
        # only one parent
        row = evidence[var.parents[0]]
    else:
        # multiple parents
        # print(var.parents)
        print(evidence)
        for parent in var.parents:
            print(parent)
        row = tuple(evidence[parent] for parent in var.parents)
    return var.cpt[row] if value else 1-var.cpt[row]

class BayesNode:
    
    def __init__(self, name, parents, values, cpt):
        if isinstance(parents, str):
            parents = parents.split()
            
        if len(parents)==0:
            # if no parents, empty dict key for cpt
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            # if there is only one parent, only one tuple argument
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(v): p for v, p in cpt.items()}

        self.variable = name
        self.parents = parents
        self.cpt = cpt
        self.values = values
        self.children = []
        
    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))    

    
##===============================================##
## Suggested skeleton codes for a BayesNet class ##
##===============================================##

class BayesNet:
    '''Bayesian network containing only boolean-variable nodes.'''

    def __init__(self, nodes):
        '''Initialize the Bayes net by adding each of the nodes,
        which should be a list BayesNode class objects ordered
        from parents to children (`top` to `bottom`, from causes
        to effects)'''
        
        # your code goes here...
        self.variables = []
        self.net = []
        for node in nodes:
            self.variables.append(node.variable)
            if len(node.parents) == 0:
                self.net.append((node.variable,node.parents,node.children,node))
        for node in nodes:
            if len(node.parents) !=0:
                self.net.append((node.variable,node.parents,node.children,node))
        for node in self.net: #assigns children to parent nodes
            if len(node[1]) != 0:
                for parent in node[1]:
                    for assignNode in self.net:
                        if parent == assignNode[0]:
                            assignNode[2].append(node[0])
                            assignNode[3].children.append(node[0])

                
    def add(self, node):
        '''Add a new BayesNode to the BayesNet. The parents should all
        already be in the net, and the variable itself should not be'''
        assert node.variable not in self.variables
        assert all((parent in self.variables) for parent in node.parents)
        self.variables.append(node.variable)
        self.net.append((node.variable,node.parents,node.children,node))
        for node in self.net: #assigns children to parent nodes
            if len(node[1]) != 0:
                for parent in node[1]:
                    for assignNode in self.net:
                        if parent == assignNode[0]:
                            assignNode[2].append(node[0])



        
        
        

            
    def find_node(self, var):
        '''Find and return the BayesNode in the net with name `var`'''
        
        # your code goes here...
        for node in self.net:
            if var == node[0]:
                return node[3]
        

        
    def find_values(self, var):
        '''Return the set of possible values for variable `var`'''
        
        # your code goes here...

        return(self.find_node(var).values)
        

    
    def __repr__(self):
        return 'BayesNet({})'.format(self.nodes)

class Tests_Problem1(unittest.TestCase):
    def setUp(self):
        self.p1 = BayesNode('p1', '', [T,F], 0.3)
        self.p2 = BayesNode('p2', '', [T,F], 0.6)
        self.c  = BayesNode('c', ['p1', 'p2'], [T,F], {(T,T):0.1, (T,F):0.2, (F,T):0.3, (F,F):0.4})
        
    def test_onenode(self):
        self.assertEqual(P(self.p1, T), 0.3)
    def test_twonode(self):
        self.assertEqual(P(self.c, F, {'p1':T, 'p2':F}), 0.8)


def normalize(QX):
    total = 0.0
    for val in QX.values():
        total += val
    for key in QX.keys():
        QX[key] /= total
    return QX

def enumerateAll(varss, e,bn):

    if len(varss) == 0: return 1.0
    Y = varss.pop()
    if Y in e:
        print(bn.find_node(Y))
        val = P(bn.find_node(Y),e[Y],e) * enumerateAll(varss,e,bn)
        varss.append(Y)
        return val
    else:
        total = 0
        e[Y] = T
        total += P(bn.find_node(Y),T,e) * enumerateAll(varss,e,bn)
        e[Y] = F
        total += P(bn.find_node(Y),F,e) * enumerateAll(varss,e,bn)
        del e[Y]
        varss.append(Y)
        return total


def get_prob(X,e,bn): #calculates P(X|e)
    ''' Enumeration function
        P(B|j,m) = (P(B,j,m)/P(j,m)) = alpha = 1 / P(j,m) => P(B|j,m) = alpha * P(B,j,m)
      '''

    Q = {}
    if not e:
        return P(bn.find_node(X.variable),T,bn.find_values(X.variable))
    else:
        for xi in [F,T]:
            e[X] = xi
            Q[xi] = enumerateAll(bn.variables,e,bn)
            del e[X]
        return normalize(Q)


nodes = []

p1 = BayesNode('p1', '', [T,F], 0.3)
p2 = BayesNode('p2', '', [T,F], 0.6)

c  = BayesNode('c', ['p1', 'p2'], [T,F], {(T,T):0.1, (T,F):0.2, (F,T):0.3, (F,F):0.4})
Sm = BayesNode('Sm', '', [T,F], 0.2)
ME = BayesNode('ME', '', [T,F], 0.5)
Ath = BayesNode('Ath', '', [T,F], 0.53)
FH = BayesNode('FH', '', [T,F], 0.15)
HBP = BayesNode('HBP', ['Sm','ME'], [T,F], {(T,T):0.6, (T,F):0.72, (F,T):0.33, (F,F):0.51})
HD = BayesNode('HD', ['Ath','HBP','FH'], [T,F], {(T,T,T):0.92, (T,T,F):0.91, (T,F,T):0.81, (T,F,F):0.77, (F,T,T):0.75, (F,T,F):0.69, (F,F,T):0.38,(F,F,F):0.23})
Ang = BayesNode('Ang', ['HD'], [T,F], {(T):.85,(F):.40})
Rapid = BayesNode('Rapid', ['HD'], [T,F], {(T):.99,(F):.3})


BN = BayesNet(nodes)
BN.add(Sm)
BN.add(ME)
BN.add(Ath)
BN.add(FH)
BN.add(HBP)
BN.add(HD)
BN.add(Ang)
BN.add(Rapid)

print(BN.find_node('HD'))
# print(BN.variables)
# #print probability value of p1 when it is true using the function 'P'
# #print("P1 = True:",P(BN.find_node('p1'),BN.find_values('p1')))
# print(get_prob(FH,{},BN))
print(get_prob(Ang,{"HD":T}, BN))
#print probability value of 'C', given that 'p1' is True and 'p2' is False using the function 'P'



# a = get_prob(FH,{},BN)
# print("1. ",a[0])

# b= get_prob(Ang,{"HD" : T}, BN)
# print("2. ",b[1])

# c= get_prob(HBP,{"Sm" : T, "ME" : F}, BN)
# print("3. ",c[0])
